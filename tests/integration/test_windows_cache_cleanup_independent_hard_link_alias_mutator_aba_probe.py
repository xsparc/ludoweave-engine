"""Test-only Windows independent hard-link alias mutator ABA probe."""

from __future__ import annotations

import json
import os
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
from test_windows_cache_cleanup_expected_identity_guardian_admission_probe import (
    _read_identity_guardian_event,  # pyright: ignore[reportPrivateUsage]
    _release_identity_guardian,  # pyright: ignore[reportPrivateUsage]
    _start_identity_guardian,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_protected_guardian_handoff_probe import (
    _assert_exclusive_available,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M186 probes an independent Windows hard-link alias mutation actor",
)

_CHILD = Path(__file__).parents[1] / "fixtures/windows_hard_link_alias_mutator_child.py"
_SCHEMA = "ludoweave.test.windows-hard-link-alias-mutator/1"
_RECREATE_TOKEN = b"+"
_CLOSE_TOKEN = b"!"
_ERROR_SHARING_VIOLATION = 32
_MAX_LINE_BYTES = 192
_TIMEOUT_SECONDS = 15.0


def _start_alias_mutator(working_directory: Path) -> subprocess.Popen[bytes]:
    return subprocess.Popen(
        (sys.executable, "-I", "-B", str(_CHILD)),
        close_fds=True,
        cwd=working_directory,
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _parse_alias_mutator_event(line: bytes) -> str:
    if not line.endswith(b"\n") or len(line) > _MAX_LINE_BYTES:
        raise RuntimeError("alias mutator returned invalid structured output") from None
    try:
        payload: object = json.loads(line)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RuntimeError("alias mutator returned invalid structured output") from None
    if not isinstance(payload, dict):
        raise RuntimeError("alias mutator returned invalid structured output") from None
    document = cast(dict[object, object], payload)
    if set(document) != {"phase", "schema"} or document["schema"] != _SCHEMA:
        raise RuntimeError("alias mutator returned invalid structured output") from None
    phase = document["phase"]
    if type(phase) is not str or phase not in {"deleted", "recreated", "closed"}:
        raise RuntimeError("alias mutator returned invalid structured output") from None
    return phase


def _read_alias_mutator_event(process: subprocess.Popen[bytes]) -> str:
    stdout = process.stdout
    if stdout is None:
        raise RuntimeError("alias mutator stdout is unavailable") from None
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
        raise RuntimeError("alias mutator event timed out") from None
    reader.join(timeout=_TIMEOUT_SECONDS)
    if reader.is_alive():
        raise RuntimeError("alias mutator event did not settle") from None
    if isinstance(result, BaseException):
        raise RuntimeError("alias mutator event failed") from result
    return _parse_alias_mutator_event(result)


def _send_alias_mutator_token(process: subprocess.Popen[bytes], token: bytes) -> str:
    stdin = process.stdin
    if stdin is None:
        raise RuntimeError("alias mutator stdin is unavailable") from None
    stdin.write(token)
    stdin.flush()
    return _read_alias_mutator_event(process)


def _close_alias_mutator(process: subprocess.Popen[bytes]) -> str:
    stdin = process.stdin
    stdout = process.stdout
    stderr = process.stderr
    if stdin is None or stdout is None or stderr is None:
        raise RuntimeError("alias mutator pipes are unavailable") from None
    closed = _send_alias_mutator_token(process, _CLOSE_TOKEN)
    stdin.close()
    try:
        return_code = process.wait(timeout=_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=_TIMEOUT_SECONDS)
        raise RuntimeError("alias mutator close timed out") from None
    if return_code != 0 or stdout.read(_MAX_LINE_BYTES + 1) or stderr.read(_MAX_LINE_BYTES + 1):
        raise RuntimeError("alias mutator returned invalid closure output") from None
    return closed


def test_independent_mutator_changes_alias_membership_during_guardian_lifetime(
    tmp_path: Path,
) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    peer_path = tmp_path / "peer"
    peer_path.mkdir()
    alias_path = peer_path / "coordination.alias"
    displaced_path = coordination_path.with_name("coordination.displaced")
    os.link(coordination_path, alias_path)

    guardian: subprocess.Popen[bytes] | None = None
    mutator: subprocess.Popen[bytes] | None = None
    identity_probe = _WindowsCapabilityProbe()
    lock_probe = _CoordinationLockProbe()
    try:
        with identity_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            peer = identity_probe.open_directory(root, "peer")
            original = identity_probe.open_file(live, "coordination.lock", delete_access=False)
            alias = identity_probe.open_file(peer, "coordination.alias", delete_access=False)
            original_identity = identity_probe.identity(original)
            assert identity_probe.identity(alias) == original_identity
            assert identity_probe.link_count(original) == 2
            assert identity_probe.link_count(alias) == 2

        assert identity_probe.owned_count == 0
        guardian = _start_identity_guardian(tmp_path, original_identity)
        assert _read_identity_guardian_event(guardian) == "ready"
        assert guardian.poll() is None

        with identity_probe, lock_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            peer = identity_probe.open_directory(root, "peer")
            original = identity_probe.open_file(live, "coordination.lock", delete_access=False)
            assert identity_probe.identity(original) == original_identity
            assert identity_probe.link_count(original) == 2

            with pytest.raises(OSError) as blocked_coordination:
                coordination_path.rename(displaced_path)
            assert blocked_coordination.value.winerror == _ERROR_SHARING_VIOLATION

            mutator = _start_alias_mutator(tmp_path)
            assert mutator.pid != guardian.pid
            assert mutator.pid != os.getpid()
            assert _read_alias_mutator_event(mutator) == "deleted"
            assert mutator.poll() is None
            assert guardian.poll() is None
            assert not alias_path.exists()
            assert identity_probe.identity(original) == original_identity
            assert identity_probe.link_count(original) == 1
            assert coordination_path.read_bytes() == payload
            _assert_exclusive_available(lock_probe, coordination_path)

            assert _send_alias_mutator_token(mutator, _RECREATE_TOKEN) == "recreated"
            assert mutator.poll() is None
            assert guardian.poll() is None
            alias = identity_probe.open_file(peer, "coordination.alias", delete_access=False)
            assert identity_probe.identity(original) == original_identity
            assert identity_probe.identity(alias) == original_identity
            assert identity_probe.link_count(original) == 2
            assert identity_probe.link_count(alias) == 2
            assert coordination_path.read_bytes() == payload
            assert alias_path.read_bytes() == payload
            _assert_exclusive_available(lock_probe, coordination_path)
            _assert_exclusive_available(lock_probe, alias_path)

            with pytest.raises(OSError) as still_blocked_coordination:
                coordination_path.rename(displaced_path)
            assert still_blocked_coordination.value.winerror == _ERROR_SHARING_VIOLATION

            assert _close_alias_mutator(mutator) == "closed"
            assert mutator.returncode == 0
            assert guardian.poll() is None
            with pytest.raises(OSError) as blocked_after_mutator_close:
                coordination_path.rename(displaced_path)
            assert blocked_after_mutator_close.value.winerror == _ERROR_SHARING_VIOLATION

            assert _release_identity_guardian(guardian) == "closed"
            assert guardian.returncode == 0

        coordination_path.rename(displaced_path)
        with identity_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            peer = identity_probe.open_directory(root, "peer")
            displaced = identity_probe.open_file(
                live,
                "coordination.displaced",
                delete_access=False,
            )
            alias = identity_probe.open_file(peer, "coordination.alias", delete_access=False)
            assert identity_probe.identity(displaced) == original_identity
            assert identity_probe.identity(alias) == original_identity
            assert identity_probe.link_count(displaced) == 2
            assert identity_probe.link_count(alias) == 2
            assert displaced_path.read_bytes() == payload
            assert alias_path.read_bytes() == payload
    finally:
        if mutator is not None:
            _close_participant(mutator)
        if guardian is not None:
            _close_participant(guardian)

    assert mutator is not None and mutator.returncode == 0
    assert guardian is not None and guardian.returncode == 0
    for process in (mutator, guardian):
        for stream in (process.stdin, process.stdout, process.stderr):
            assert stream is not None and stream.closed
    assert identity_probe.owned_count == 0
    assert lock_probe.owned_count == 0
    assert displaced_path.read_bytes() == payload
    assert alias_path.read_bytes() == payload
    assert not coordination_path.exists()
