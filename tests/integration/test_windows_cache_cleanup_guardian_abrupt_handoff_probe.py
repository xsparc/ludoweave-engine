"""Test-only Windows guardian abrupt-handoff probe."""

from __future__ import annotations

import json
import queue
import subprocess
import sys
import threading
from pathlib import Path
from typing import cast

import pytest
from test_windows_cache_cleanup_capability_probe import (
    _WindowsCapabilityProbe,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_abrupt_settlement_probe import (
    _terminate_and_assert_abrupt,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_live_substitution_exclusion_probe import (
    _start_protected_participant,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_probe import (
    _MAX_LINE_BYTES,  # pyright: ignore[reportPrivateUsage]
    _TIMEOUT_SECONDS,  # pyright: ignore[reportPrivateUsage]
    _close_participant,  # pyright: ignore[reportPrivateUsage]
    _CoordinationLockProbe,  # pyright: ignore[reportPrivateUsage]
    _create_fixture,  # pyright: ignore[reportPrivateUsage]
    _read_event,  # pyright: ignore[reportPrivateUsage]
    _release_and_read_closed,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_substitution_probe import (
    _attempt_substitution,  # pyright: ignore[reportPrivateUsage]
    _SubstitutionResult,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_protected_guardian_handoff_probe import (
    _assert_exclusive_available,  # pyright: ignore[reportPrivateUsage]
    _assert_exclusive_refused,  # pyright: ignore[reportPrivateUsage]
    _assert_substitution_refused,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M178 probes abrupt Windows guardian-to-participant handoff",
)

_CHILD = Path(__file__).parents[1] / "fixtures/windows_coordination_guardian_child.py"
_SCHEMA = "ludoweave.test.windows-coordination-guardian/1"
_RELEASE_TOKEN = b"!"


def _parse_guardian_event(line: bytes) -> str:
    if not line.endswith(b"\n") or len(line) > _MAX_LINE_BYTES:
        raise RuntimeError("coordination guardian returned invalid structured output") from None
    try:
        payload: object = json.loads(line)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RuntimeError("coordination guardian returned invalid structured output") from None
    if not isinstance(payload, dict):
        raise RuntimeError("coordination guardian returned invalid structured output") from None
    document = cast(dict[object, object], payload)
    if set(document) != {"phase", "schema"} or document["schema"] != _SCHEMA:
        raise RuntimeError("coordination guardian returned invalid structured output") from None
    phase = document["phase"]
    if type(phase) is not str or phase not in {"ready", "closed"}:
        raise RuntimeError("coordination guardian returned invalid structured output") from None
    return phase


def _read_guardian_event(process: subprocess.Popen[bytes]) -> str:
    stdout = process.stdout
    if stdout is None:
        raise RuntimeError("coordination guardian stdout is unavailable") from None
    results: queue.Queue[bytes | BaseException] = queue.Queue(maxsize=1)

    def read_one_line() -> None:
        try:
            results.put(stdout.readline(_MAX_LINE_BYTES + 1))
        except BaseException as error:  # pragma: no cover - defensive pipe failure
            results.put(error)

    reader = threading.Thread(target=read_one_line, daemon=True)
    reader.start()
    try:
        result = results.get(timeout=_TIMEOUT_SECONDS)
    except queue.Empty:
        process.kill()
        process.wait(timeout=_TIMEOUT_SECONDS)
        reader.join(timeout=_TIMEOUT_SECONDS)
        raise RuntimeError("coordination guardian event timed out") from None
    reader.join(timeout=_TIMEOUT_SECONDS)
    if reader.is_alive():
        raise RuntimeError("coordination guardian event did not settle") from None
    if isinstance(result, BaseException):
        raise RuntimeError("coordination guardian event failed") from result
    return _parse_guardian_event(result)


def _start_guardian(working_directory: Path) -> subprocess.Popen[bytes]:
    return subprocess.Popen(
        (sys.executable, "-I", "-B", str(_CHILD)),
        close_fds=True,
        cwd=working_directory,
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _release_guardian(process: subprocess.Popen[bytes]) -> str:
    stdin = process.stdin
    stdout = process.stdout
    stderr = process.stderr
    if stdin is None or stdout is None or stderr is None:
        raise RuntimeError("coordination guardian pipes are unavailable") from None
    stdin.write(_RELEASE_TOKEN)
    stdin.flush()
    stdin.close()
    try:
        return_code = process.wait(timeout=_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=_TIMEOUT_SECONDS)
        raise RuntimeError("coordination guardian close timed out") from None
    closed = _parse_guardian_event(stdout.readline(_MAX_LINE_BYTES + 1))
    if return_code != 0 or stdout.read(_MAX_LINE_BYTES + 1) or stderr.read(_MAX_LINE_BYTES + 1):
        raise RuntimeError("coordination guardian returned invalid closure output") from None
    return closed


def test_guardian_fixture_acknowledged_close_releases_namespace(tmp_path: Path) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    displaced_path = coordination_path.with_name("coordination.displaced")
    guardian: subprocess.Popen[bytes] | None = None
    lock_probe = _CoordinationLockProbe()

    try:
        with lock_probe:
            guardian = _start_guardian(tmp_path)
            assert _read_guardian_event(guardian) == "ready"
            assert guardian.poll() is None
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_available(lock_probe, coordination_path)

            assert _release_guardian(guardian) == "closed"
            assert guardian.returncode == 0
            _assert_exclusive_available(lock_probe, coordination_path)
            assert _attempt_substitution(tmp_path) == _SubstitutionResult(
                phase="substituted",
                error_code=0,
            )
            assert displaced_path.read_bytes() == payload
            assert coordination_path.read_bytes() == payload
    finally:
        if guardian is not None:
            _close_participant(guardian)

    assert guardian is not None and guardian.returncode == 0
    for stream in (guardian.stdin, guardian.stdout, guardian.stderr):
        assert stream is not None and stream.closed
    assert lock_probe.owned_count == 0


def test_abrupt_guardian_settlement_preserves_live_participant_protection(
    tmp_path: Path,
) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    displaced_path = coordination_path.with_name("coordination.displaced")
    guardian: subprocess.Popen[bytes] | None = None
    participant: subprocess.Popen[bytes] | None = None

    identity_probe = _WindowsCapabilityProbe()
    lock_probe = _CoordinationLockProbe()
    try:
        with identity_probe, lock_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            original = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            original_identity = identity_probe.identity(original)

            guardian = _start_guardian(tmp_path)
            assert _read_guardian_event(guardian) == "ready"
            assert guardian.poll() is None
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_available(lock_probe, coordination_path)

            participant = _start_protected_participant(tmp_path)
            assert _read_event(participant) == ("ready", 0)
            assert participant.poll() is None
            joined = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            assert identity_probe.identity(joined) == original_identity
            assert guardian.poll() is None
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_refused(lock_probe, coordination_path)

            guardian_return_code = _terminate_and_assert_abrupt(guardian)
            assert guardian.poll() == guardian_return_code
            assert participant.poll() is None
            retained = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            assert identity_probe.identity(retained) == original_identity
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_refused(lock_probe, coordination_path)

            assert _release_and_read_closed(participant) == ("closed", 0)
            assert participant.returncode == 0
            _assert_exclusive_available(lock_probe, coordination_path)

            assert _attempt_substitution(tmp_path) == _SubstitutionResult(
                phase="substituted",
                error_code=0,
            )
            displaced = identity_probe.open_file(
                live,
                "coordination.displaced",
                delete_access=False,
            )
            replacement = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            assert identity_probe.identity(displaced) == original_identity
            assert identity_probe.identity(replacement) != original_identity
            assert displaced_path.read_bytes() == payload
            assert coordination_path.read_bytes() == payload
    finally:
        if guardian is not None:
            _close_participant(guardian)
        if participant is not None:
            _close_participant(participant)

    assert guardian is not None and guardian.returncode is not None
    assert guardian.returncode != 0
    assert participant is not None and participant.returncode == 0
    for process in (guardian, participant):
        for stream in (process.stdin, process.stdout, process.stderr):
            assert stream is not None and stream.closed
    assert lock_probe.owned_count == 0
    assert displaced_path.read_bytes() == payload
    assert coordination_path.read_bytes() == payload
