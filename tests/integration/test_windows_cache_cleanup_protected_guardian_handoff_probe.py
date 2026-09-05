"""Test-only Windows protected coordination guardian-handoff probe."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest
from test_windows_cache_cleanup_capability_probe import (
    _FILE_ATTRIBUTE_NORMAL,  # pyright: ignore[reportPrivateUsage]
    _FILE_SHARE_READ,  # pyright: ignore[reportPrivateUsage]
    _FILE_SHARE_WRITE,  # pyright: ignore[reportPrivateUsage]
    _INVALID_HANDLE_VALUE,  # pyright: ignore[reportPrivateUsage]
    _OPEN_EXISTING,  # pyright: ignore[reportPrivateUsage]
    _NativeFailure,  # pyright: ignore[reportPrivateUsage]
    _WindowsCapabilityProbe,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_live_substitution_exclusion_probe import (
    _ERROR_SHARING_VIOLATION,  # pyright: ignore[reportPrivateUsage]
    _start_protected_participant,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_probe import (
    _ERROR_LOCK_VIOLATION,  # pyright: ignore[reportPrivateUsage]
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

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M177 probes protected Windows coordination guardian handoff",
)

_GENERIC_READ = 0x80000000


class _ProtectedCoordinationGuardianProbe(_WindowsCapabilityProbe):
    def acquire(self, path: Path) -> int:
        raw_handle = cast(
            int | None,
            self._create_file(
                str(path),
                _GENERIC_READ,
                _FILE_SHARE_READ | _FILE_SHARE_WRITE,
                None,
                _OPEN_EXISTING,
                _FILE_ATTRIBUTE_NORMAL,
                None,
            ),
        )
        if raw_handle is None or raw_handle == _INVALID_HANDLE_VALUE:
            raise _NativeFailure("CreateFileW(guardian)", self._get_last_error())
        handle = self._adopt(raw_handle)
        try:
            self._reject_reparse(handle)
        except BaseException:
            self._close_owned(handle)
            raise
        return handle

    def release(self, handle: int) -> None:
        self._close_owned(handle)


def _assert_substitution_refused(tmp_path: Path) -> None:
    assert _attempt_substitution(tmp_path) == _SubstitutionResult(
        phase="rename_failed",
        error_code=_ERROR_SHARING_VIOLATION,
    )


def _assert_exclusive_refused(
    lock_probe: _CoordinationLockProbe,
    coordination_path: Path,
) -> None:
    with pytest.raises(_NativeFailure) as locking:
        lock_probe.acquire_exclusive(coordination_path)
    assert locking.value.code == _ERROR_LOCK_VIOLATION
    assert lock_probe.owned_count == 0


def _assert_exclusive_available(
    lock_probe: _CoordinationLockProbe,
    coordination_path: Path,
) -> None:
    exclusive = lock_probe.acquire_exclusive(coordination_path)
    assert os.get_handle_inheritable(exclusive) is False
    lock_probe.release_exclusive(exclusive)
    assert lock_probe.owned_count == 0


def test_guardian_bridges_participant_free_interval_then_hands_off_protection(
    tmp_path: Path,
) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    displaced_path = coordination_path.with_name("coordination.displaced")
    guardian: int | None = None
    first: subprocess.Popen[bytes] | None = None
    second: subprocess.Popen[bytes] | None = None

    identity_probe = _WindowsCapabilityProbe()
    guardian_probe = _ProtectedCoordinationGuardianProbe()
    lock_probe = _CoordinationLockProbe()
    try:
        with identity_probe, guardian_probe, lock_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            original = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            original_identity = identity_probe.identity(original)

            guardian = guardian_probe.acquire(coordination_path)
            assert os.get_handle_inheritable(guardian) is False
            assert guardian_probe.identity(guardian) == original_identity
            assert guardian_probe.owned_count == 1
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_available(lock_probe, coordination_path)

            first = _start_protected_participant(tmp_path)
            assert _read_event(first) == ("ready", 0)
            assert first.poll() is None
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_refused(lock_probe, coordination_path)

            assert _release_and_read_closed(first) == ("closed", 0)
            assert first.returncode == 0
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_available(lock_probe, coordination_path)

            second = _start_protected_participant(tmp_path)
            assert _read_event(second) == ("ready", 0)
            assert second.poll() is None
            joined = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            assert identity_probe.identity(joined) == original_identity

            guardian_probe.release(guardian)
            guardian = None
            assert guardian_probe.owned_count == 0
            assert second.poll() is None
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_refused(lock_probe, coordination_path)

            assert _release_and_read_closed(second) == ("closed", 0)
            assert second.returncode == 0
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
        if first is not None:
            _close_participant(first)
        if second is not None:
            _close_participant(second)

    assert first is not None and first.returncode == 0
    assert second is not None and second.returncode == 0
    for process in (first, second):
        for stream in (process.stdin, process.stdout, process.stderr):
            assert stream is not None and stream.closed
    assert guardian_probe.owned_count == 0
    assert lock_probe.owned_count == 0
    assert displaced_path.read_bytes() == payload
    assert coordination_path.read_bytes() == payload
