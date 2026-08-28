"""Test-only Windows protected coordination-lock abrupt-settlement probe."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
from test_windows_cache_cleanup_capability_probe import (
    _NativeFailure,  # pyright: ignore[reportPrivateUsage]
    _WindowsCapabilityProbe,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_live_substitution_exclusion_probe import (
    _ERROR_SHARING_VIOLATION,  # pyright: ignore[reportPrivateUsage]
    _start_protected_participant,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_probe import (
    _ERROR_LOCK_VIOLATION,  # pyright: ignore[reportPrivateUsage]
    _MAX_LINE_BYTES,  # pyright: ignore[reportPrivateUsage]
    _TIMEOUT_SECONDS,  # pyright: ignore[reportPrivateUsage]
    _close_participant,  # pyright: ignore[reportPrivateUsage]
    _CoordinationLockProbe,  # pyright: ignore[reportPrivateUsage]
    _create_fixture,  # pyright: ignore[reportPrivateUsage]
    _read_event,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_substitution_probe import (
    _attempt_substitution,  # pyright: ignore[reportPrivateUsage]
    _SubstitutionResult,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M176 probes protected Windows coordination-lock abrupt settlement",
)


def _terminate_and_assert_abrupt(process: subprocess.Popen[bytes]) -> int:
    stdout = process.stdout
    stderr = process.stderr
    if stdout is None or stderr is None:
        raise RuntimeError("protected participant output pipes are unavailable") from None
    process.kill()
    return_code = process.wait(timeout=_TIMEOUT_SECONDS)
    assert return_code != 0
    assert stdout.read(_MAX_LINE_BYTES + 1) == b""
    assert stderr.read(_MAX_LINE_BYTES + 1) == b""
    return return_code


def test_abrupt_participant_settlement_preserves_survivor_then_releases_last_owner(
    tmp_path: Path,
) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    displaced_path = coordination_path.with_name("coordination.displaced")
    first: subprocess.Popen[bytes] | None = None
    second: subprocess.Popen[bytes] | None = None

    try:
        first = _start_protected_participant(tmp_path)
        second = _start_protected_participant(tmp_path)
        identity_probe = _WindowsCapabilityProbe()
        lock_probe = _CoordinationLockProbe()
        with identity_probe, lock_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            original = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            original_identity = identity_probe.identity(original)

            assert _read_event(first) == ("ready", 0)
            assert _read_event(second) == ("ready", 0)
            assert first.poll() is None
            assert second.poll() is None
            assert _attempt_substitution(tmp_path) == _SubstitutionResult(
                phase="rename_failed",
                error_code=_ERROR_SHARING_VIOLATION,
            )
            with pytest.raises(_NativeFailure) as both_locking:
                lock_probe.acquire_exclusive(coordination_path)
            assert both_locking.value.code == _ERROR_LOCK_VIOLATION
            assert lock_probe.owned_count == 0

            first_return_code = _terminate_and_assert_abrupt(first)
            assert first.poll() == first_return_code
            assert second.poll() is None
            assert _attempt_substitution(tmp_path) == _SubstitutionResult(
                phase="rename_failed",
                error_code=_ERROR_SHARING_VIOLATION,
            )
            with pytest.raises(_NativeFailure) as survivor_locking:
                lock_probe.acquire_exclusive(coordination_path)
            assert survivor_locking.value.code == _ERROR_LOCK_VIOLATION
            assert lock_probe.owned_count == 0

            second_return_code = _terminate_and_assert_abrupt(second)
            assert second.poll() == second_return_code
            exclusive = lock_probe.acquire_exclusive(coordination_path)
            assert os.get_handle_inheritable(exclusive) is False
            lock_probe.release_exclusive(exclusive)
            assert lock_probe.owned_count == 0

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
        if first is not None:
            _close_participant(first)
        if second is not None:
            _close_participant(second)

    assert first is not None and first.returncode is not None and first.returncode != 0
    assert second is not None and second.returncode is not None and second.returncode != 0
    for process in (first, second):
        for stream in (process.stdin, process.stdout, process.stderr):
            assert stream is not None and stream.closed
    assert displaced_path.read_bytes() == payload
    assert coordination_path.read_bytes() == payload
