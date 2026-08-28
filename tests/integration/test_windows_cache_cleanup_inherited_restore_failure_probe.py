"""Test-only inherited-handle restoration-failure ownership probe for M165."""

from __future__ import annotations

import errno
import os
import subprocess
import sys
from pathlib import Path

import pytest
import test_windows_cache_cleanup_inherited_handle_probe as inherited_probe
from test_windows_cache_cleanup_child_owned_blocker_probe import (
    _close_child,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_junction_probe import (
    _filesystem_information,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_native_error_probe import (
    _ERROR_SHARING_VIOLATION,  # pyright: ignore[reportPrivateUsage]
    _attempt_native_child_rename,  # pyright: ignore[reportPrivateUsage]
    _NativeRenameResult,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_share_delete_probe import (
    _ShareDeleteProbe,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M165 probes inherited-handle restoration-failure ownership",
)


class _InjectedRestoreFailure(OSError):
    """Fixed test-only failure raised before the native restore call."""


def test_restore_failure_reaps_child_and_preserves_parent_repair_duty(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    live_path = tmp_path / "live"
    displaced_path = tmp_path / "displaced"
    candidate_path = live_path / "candidate.bin"
    displaced_candidate = displaced_path / "candidate.bin"
    live_path.mkdir()
    candidate_path.write_bytes(b"m165-inherited-restore-failure")

    filesystem_probe = _ShareDeleteProbe()
    with filesystem_probe:
        root = filesystem_probe.open_root(tmp_path)
        filesystem_name, _ = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M165 inherited-restore fixture requires an NTFS pytest volume")
    assert filesystem_probe.owned_count == 0

    blocker_probe = _ShareDeleteProbe()
    with blocker_probe:
        blocker_handle = blocker_probe.open_directory_without_delete_sharing(live_path)
        original_set_handle_inheritable = os.set_handle_inheritable
        original_close_child = inherited_probe._close_child  # pyright: ignore[reportPrivateUsage]
        injected = _InjectedRestoreFailure(errno.EIO, "injected handle restore failure")
        closed_processes: list[subprocess.Popen[bytes]] = []
        preclose_returncodes: list[int | None] = []
        restore_attempts = 0

        def fail_first_restore(handle: int, inheritable: bool) -> None:
            nonlocal restore_attempts
            if handle == blocker_handle and inheritable is False and restore_attempts == 0:
                restore_attempts += 1
                raise injected
            original_set_handle_inheritable(handle, inheritable)

        def capture_close(process: subprocess.Popen[bytes]) -> None:
            closed_processes.append(process)
            preclose_returncodes.append(process.poll())
            original_close_child(process)

        monkeypatch.setattr(
            inherited_probe.os,
            "set_handle_inheritable",
            fail_first_restore,
        )
        monkeypatch.setattr(inherited_probe, "_close_child", capture_close)

        returned_process: subprocess.Popen[bytes] | None = None
        caught: _InjectedRestoreFailure | None = None
        try:
            try:
                returned_process = inherited_probe._spawn_inherited_blocker(  # pyright: ignore[reportPrivateUsage]
                    blocker_handle,
                    tmp_path,
                )
            except _InjectedRestoreFailure as candidate:
                caught = candidate

            assert returned_process is None
            assert caught is injected
            assert restore_attempts == 1
            assert len(closed_processes) == 1
            assert preclose_returncodes == [None]
            closed_process = closed_processes[0]
            assert closed_process.returncode is not None
            assert closed_process.poll() == closed_process.returncode
            for stream in (
                closed_process.stdin,
                closed_process.stdout,
                closed_process.stderr,
            ):
                assert stream is not None and stream.closed

            assert os.get_handle_inheritable(blocker_handle) is True
            assert blocker_probe.owned_count == 1
        finally:
            if os.get_handle_inheritable(blocker_handle):
                original_set_handle_inheritable(blocker_handle, False)
            if returned_process is not None:  # pragma: no cover - injected restore must fail
                _close_child(returned_process)

        assert os.get_handle_inheritable(blocker_handle) is False
        assert blocker_probe.owned_count == 1
        assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
            succeeded=False,
            error_code=_ERROR_SHARING_VIOLATION,
        )
        assert live_path.is_dir()
        assert not os.path.isjunction(live_path)
        assert not os.path.lexists(displaced_path)
        assert candidate_path.read_bytes() == b"m165-inherited-restore-failure"

        blocker_probe.release(blocker_handle)
        assert blocker_probe.owned_count == 0
        assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
            succeeded=True,
            error_code=0,
        )
        assert not os.path.lexists(live_path)
        assert displaced_path.is_dir()
        assert not os.path.isjunction(displaced_path)
        assert displaced_candidate.read_bytes() == b"m165-inherited-restore-failure"

    assert blocker_probe.owned_count == 0
    assert displaced_candidate.read_bytes() == b"m165-inherited-restore-failure"
