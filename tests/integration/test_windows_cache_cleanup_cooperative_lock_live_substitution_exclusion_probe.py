"""Test-only Windows live coordination-substitution exclusion probe for M175."""

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
    reason="M175 probes live Windows coordination-lock substitution exclusion",
)

_CHILD = (
    Path(__file__).parents[1] / "fixtures/windows_coordination_lock_protected_participant_child.py"
)
_ERROR_SHARING_VIOLATION = 32


def _start_protected_participant(working_directory: Path) -> subprocess.Popen[bytes]:
    return subprocess.Popen(
        (sys.executable, "-I", "-B", str(_CHILD)),
        close_fds=True,
        cwd=working_directory,
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_live_protected_participants_exclude_substitution_until_last_close(
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

            assert _release_and_read_closed(first) == ("closed", 0)
            assert first.returncode == 0
            assert second.poll() is None
            assert _attempt_substitution(tmp_path) == _SubstitutionResult(
                phase="rename_failed",
                error_code=_ERROR_SHARING_VIOLATION,
            )
            with pytest.raises(_NativeFailure) as one_locking:
                lock_probe.acquire_exclusive(coordination_path)
            assert one_locking.value.code == _ERROR_LOCK_VIOLATION
            assert lock_probe.owned_count == 0

            assert _release_and_read_closed(second) == ("closed", 0)
            assert second.returncode == 0
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

    assert displaced_path.read_bytes() == payload
    assert coordination_path.read_bytes() == payload
