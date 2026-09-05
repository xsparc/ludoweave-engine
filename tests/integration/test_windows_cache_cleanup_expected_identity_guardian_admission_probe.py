"""Test-only Windows expected-identity guardian admission probe."""

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
from test_windows_cache_cleanup_cooperative_lock_probe import (
    _close_participant,  # pyright: ignore[reportPrivateUsage]
    _CoordinationLockProbe,  # pyright: ignore[reportPrivateUsage]
    _create_fixture,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_substitution_probe import (
    _attempt_substitution,  # pyright: ignore[reportPrivateUsage]
    _SubstitutionResult,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_protected_guardian_handoff_probe import (
    _assert_exclusive_available,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M181 probes expected-identity Windows guardian admission",
)

_CHILD = Path(__file__).parents[1] / "fixtures/windows_coordination_identity_guardian_child.py"
_SCHEMA = "ludoweave.test.windows-coordination-identity-guardian/1"
_RELEASE_TOKEN = b"!"
_ERROR_SHARING_VIOLATION = 32
_MAX_LINE_BYTES = 192
_TIMEOUT_SECONDS = 15.0


def _start_identity_guardian(
    working_directory: Path,
    expected_identity: tuple[int, bytes],
) -> subprocess.Popen[bytes]:
    volume_serial, file_id = expected_identity
    if not 0 <= volume_serial <= 0xFFFFFFFFFFFFFFFF or len(file_id) != 16:
        raise ValueError("a Windows FILE_ID_INFO identity is required")
    return subprocess.Popen(
        (
            sys.executable,
            "-I",
            "-B",
            str(_CHILD),
            str(volume_serial),
            file_id.hex(),
        ),
        close_fds=True,
        cwd=working_directory,
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _parse_identity_guardian_event(line: bytes) -> str:
    if not line.endswith(b"\n") or len(line) > _MAX_LINE_BYTES:
        raise RuntimeError("identity guardian returned invalid structured output") from None
    try:
        payload: object = json.loads(line)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RuntimeError("identity guardian returned invalid structured output") from None
    if not isinstance(payload, dict):
        raise RuntimeError("identity guardian returned invalid structured output") from None
    document = cast(dict[object, object], payload)
    if set(document) != {"phase", "schema"} or document["schema"] != _SCHEMA:
        raise RuntimeError("identity guardian returned invalid structured output") from None
    phase = document["phase"]
    if type(phase) is not str or phase not in {"ready", "closed", "identity_mismatch"}:
        raise RuntimeError("identity guardian returned invalid structured output") from None
    return phase


def _read_identity_guardian_event(process: subprocess.Popen[bytes]) -> str:
    stdout = process.stdout
    if stdout is None:
        raise RuntimeError("identity guardian stdout is unavailable") from None
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
        raise RuntimeError("identity guardian event timed out") from None
    reader.join(timeout=_TIMEOUT_SECONDS)
    if reader.is_alive():
        raise RuntimeError("identity guardian event did not settle") from None
    if isinstance(result, BaseException):
        raise RuntimeError("identity guardian event failed") from result
    return _parse_identity_guardian_event(result)


def _release_identity_guardian(process: subprocess.Popen[bytes]) -> str:
    stdin = process.stdin
    stdout = process.stdout
    stderr = process.stderr
    if stdin is None or stdout is None or stderr is None:
        raise RuntimeError("identity guardian pipes are unavailable") from None
    stdin.write(_RELEASE_TOKEN)
    stdin.flush()
    stdin.close()
    try:
        return_code = process.wait(timeout=_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=_TIMEOUT_SECONDS)
        raise RuntimeError("identity guardian close timed out") from None
    closed = _parse_identity_guardian_event(stdout.readline(_MAX_LINE_BYTES + 1))
    if return_code != 0 or stdout.read(_MAX_LINE_BYTES + 1) or stderr.read(_MAX_LINE_BYTES + 1):
        raise RuntimeError("identity guardian returned invalid closure output") from None
    return closed


def _finish_identity_mismatch(process: subprocess.Popen[bytes]) -> None:
    stdin = process.stdin
    stdout = process.stdout
    stderr = process.stderr
    if stdin is None or stdout is None or stderr is None:
        raise RuntimeError("identity guardian pipes are unavailable") from None
    stdin.close()
    try:
        return_code = process.wait(timeout=_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=_TIMEOUT_SECONDS)
        raise RuntimeError("identity guardian mismatch timed out") from None
    if return_code != 0 or stdout.read(_MAX_LINE_BYTES + 1) or stderr.read(_MAX_LINE_BYTES + 1):
        raise RuntimeError("identity guardian returned invalid mismatch output") from None


def test_expected_identity_guardian_admits_matching_opened_identity(tmp_path: Path) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    displaced_path = coordination_path.with_name("coordination.displaced")
    guardian: subprocess.Popen[bytes] | None = None
    identity_probe = _WindowsCapabilityProbe()
    lock_probe = _CoordinationLockProbe()
    try:
        with identity_probe, lock_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            original = identity_probe.open_file(live, "coordination.lock", delete_access=False)
            original_identity = identity_probe.identity(original)

            guardian = _start_identity_guardian(tmp_path, original_identity)
            assert _read_identity_guardian_event(guardian) == "ready"
            assert guardian.poll() is None
            with pytest.raises(OSError) as blocked:
                coordination_path.rename(displaced_path)
            assert blocked.value.winerror == _ERROR_SHARING_VIOLATION
            _assert_exclusive_available(lock_probe, coordination_path)

            assert _release_identity_guardian(guardian) == "closed"
            assert guardian.returncode == 0
            coordination_path.rename(displaced_path)
            moved = identity_probe.open_file(live, "coordination.displaced", delete_access=False)
            assert identity_probe.identity(moved) == original_identity
            assert displaced_path.read_bytes() == payload
    finally:
        if guardian is not None:
            _close_participant(guardian)

    assert guardian is not None and guardian.returncode == 0
    for stream in (guardian.stdin, guardian.stdout, guardian.stderr):
        assert stream is not None and stream.closed
    assert identity_probe.owned_count == 0
    assert lock_probe.owned_count == 0
    assert not coordination_path.exists()
    assert displaced_path.read_bytes() == payload


def test_expected_identity_guardian_rejects_preexisting_replacement(tmp_path: Path) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    displaced_path = coordination_path.with_name("coordination.displaced")
    second_displaced_path = coordination_path.with_name("coordination.second-displaced")
    guardian: subprocess.Popen[bytes] | None = None
    identity_probe = _WindowsCapabilityProbe()
    lock_probe = _CoordinationLockProbe()
    try:
        with identity_probe, lock_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            original = identity_probe.open_file(live, "coordination.lock", delete_access=False)
            original_identity = identity_probe.identity(original)
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
            replacement_identity = identity_probe.identity(replacement)
            assert identity_probe.identity(displaced) == original_identity
            assert replacement_identity != original_identity

            guardian = _start_identity_guardian(tmp_path, original_identity)
            assert _read_identity_guardian_event(guardian) == "identity_mismatch"
            _finish_identity_mismatch(guardian)
            assert guardian.returncode == 0
            coordination_path.rename(second_displaced_path)
            _assert_exclusive_available(lock_probe, second_displaced_path)
            moved_replacement = identity_probe.open_file(
                live,
                "coordination.second-displaced",
                delete_access=False,
            )
            assert identity_probe.identity(moved_replacement) == replacement_identity
            assert identity_probe.identity(displaced) == original_identity
            assert displaced_path.read_bytes() == payload
            assert second_displaced_path.read_bytes() == payload
    finally:
        if guardian is not None:
            _close_participant(guardian)

    assert guardian is not None and guardian.returncode == 0
    for stream in (guardian.stdin, guardian.stdout, guardian.stderr):
        assert stream is not None and stream.closed
    assert identity_probe.owned_count == 0
    assert lock_probe.owned_count == 0
    assert not coordination_path.exists()
    assert displaced_path.read_bytes() == payload
    assert second_displaced_path.read_bytes() == payload
