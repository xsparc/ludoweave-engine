"""Test-only inherited-handle launch-failure rollback probe for M164."""

from __future__ import annotations

import errno
import os
import subprocess
import sys
from pathlib import Path

import pytest
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
    reason="M164 probes explicit inherited-handle launch-failure rollback",
)

_MISSING_EXECUTABLE_NAME = "m164-missing-launch-target.exe"
_ERROR_FILE_NOT_FOUND = 2


def _attempt_missing_executable_launch(
    handle: int,
    working_directory: Path,
) -> FileNotFoundError:
    missing_executable = working_directory / _MISSING_EXECUTABLE_NAME
    if os.path.lexists(missing_executable):
        raise RuntimeError("missing launch target unexpectedly exists") from None

    startup_info = subprocess.STARTUPINFO()
    startup_info.lpAttributeList = {"handle_list": [handle]}
    if os.get_handle_inheritable(handle):
        raise RuntimeError("blocker handle was unexpectedly inheritable") from None

    process: subprocess.Popen[bytes] | None = None
    error: FileNotFoundError | None = None
    os.set_handle_inheritable(handle, True)
    try:
        try:
            process = subprocess.Popen(
                (str(missing_executable),),
                close_fds=True,
                cwd=working_directory,
                executable=str(missing_executable),
                shell=False,
                startupinfo=startup_info,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError as candidate:
            error = candidate
    finally:
        try:
            os.set_handle_inheritable(handle, False)
        except BaseException:
            if process is not None:
                _close_child(process)
            raise

    if process is not None:  # pragma: no cover - missing path must not start
        _close_child(process)
        raise RuntimeError("missing launch target unexpectedly started") from None
    if error is None:  # pragma: no cover - Popen either returns or raises
        raise RuntimeError("missing launch did not return an error") from None
    return error


def test_failed_launch_restores_inheritability_and_parent_denial(tmp_path: Path) -> None:
    live_path = tmp_path / "live"
    displaced_path = tmp_path / "displaced"
    missing_executable = tmp_path / _MISSING_EXECUTABLE_NAME
    candidate_path = live_path / "candidate.bin"
    displaced_candidate = displaced_path / "candidate.bin"
    live_path.mkdir()
    candidate_path.write_bytes(b"m164-inherited-launch-failure")
    assert not os.path.lexists(missing_executable)

    filesystem_probe = _ShareDeleteProbe()
    with filesystem_probe:
        root = filesystem_probe.open_root(tmp_path)
        filesystem_name, _ = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M164 inherited-launch fixture requires an NTFS pytest volume")
    assert filesystem_probe.owned_count == 0

    blocker_probe = _ShareDeleteProbe()
    with blocker_probe:
        blocker_handle = blocker_probe.open_directory_without_delete_sharing(live_path)
        error = _attempt_missing_executable_launch(blocker_handle, tmp_path)

        assert type(error) is FileNotFoundError
        assert error.errno == errno.ENOENT
        assert error.winerror == _ERROR_FILE_NOT_FOUND
        assert os.get_handle_inheritable(blocker_handle) is False
        assert blocker_probe.owned_count == 1
        assert not os.path.lexists(missing_executable)

        assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
            succeeded=False,
            error_code=_ERROR_SHARING_VIOLATION,
        )
        assert live_path.is_dir()
        assert not os.path.isjunction(live_path)
        assert not os.path.lexists(displaced_path)
        assert candidate_path.read_bytes() == b"m164-inherited-launch-failure"

        blocker_probe.release(blocker_handle)
        assert blocker_probe.owned_count == 0
        assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
            succeeded=True,
            error_code=0,
        )
        assert not os.path.lexists(live_path)
        assert displaced_path.is_dir()
        assert not os.path.isjunction(displaced_path)
        assert displaced_candidate.read_bytes() == b"m164-inherited-launch-failure"

    assert blocker_probe.owned_count == 0
    assert not os.path.lexists(missing_executable)
    assert displaced_candidate.read_bytes() == b"m164-inherited-launch-failure"
