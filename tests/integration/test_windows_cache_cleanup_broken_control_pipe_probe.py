"""Test-only Windows blocker broken-control-pipe probe for M159."""

from __future__ import annotations

import ctypes
import msvcrt
import os
import subprocess
import sys
from collections.abc import Callable
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, cast

import pytest
from test_windows_cache_cleanup_capability_probe import (
    _load_function,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_child_owned_blocker_probe import (
    _CHILD,  # pyright: ignore[reportPrivateUsage]
    _MAX_LINE_BYTES,  # pyright: ignore[reportPrivateUsage]
    _RELEASE_TOKEN,  # pyright: ignore[reportPrivateUsage]
    _TIMEOUT_SECONDS,  # pyright: ignore[reportPrivateUsage]
    _close_child,  # pyright: ignore[reportPrivateUsage]
    _read_ready,  # pyright: ignore[reportPrivateUsage]
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
    reason="M159 probes a broken Windows blocker control pipe",
)

_ERROR_NO_DATA = 232


@dataclass(frozen=True, slots=True)
class _NativePipeWriteResult:
    succeeded: bool
    error_code: int
    bytes_written: int


def _attempt_native_pipe_write(stream: BinaryIO) -> _NativePipeWriteResult:
    win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
    kernel32 = win_dll("kernel32", use_last_error=True)
    write_file = _load_function(
        kernel32,
        "WriteFile",
        [
            wintypes.HANDLE,
            wintypes.LPVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        ],
        wintypes.BOOL,
    )
    payload = (wintypes.BYTE * len(_RELEASE_TOKEN)).from_buffer_copy(_RELEASE_TOKEN)
    written = wintypes.DWORD()
    native_handle = msvcrt.get_osfhandle(stream.fileno())
    ctypes.set_last_error(0)
    succeeded = cast(
        bool,
        write_file(
            wintypes.HANDLE(native_handle),
            ctypes.byref(payload),
            wintypes.DWORD(len(payload)),
            ctypes.byref(written),
            None,
        ),
    )
    return _NativePipeWriteResult(
        succeeded=succeeded,
        error_code=0 if succeeded else ctypes.get_last_error(),
        bytes_written=written.value,
    )


def test_late_release_write_observes_broken_pipe_after_blocker_exit(
    tmp_path: Path,
) -> None:
    live_path = tmp_path / "live"
    displaced_path = tmp_path / "displaced"
    candidate_path = live_path / "candidate.bin"
    displaced_candidate = displaced_path / "candidate.bin"
    live_path.mkdir()
    candidate_path.write_bytes(b"m159-broken-control-pipe")

    filesystem_probe = _ShareDeleteProbe()
    with filesystem_probe:
        root = filesystem_probe.open_root(tmp_path)
        filesystem_name, _ = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M159 broken-pipe fixture requires an NTFS pytest volume")
    assert filesystem_probe.owned_count == 0

    blocker = subprocess.Popen(
        (sys.executable, "-I", "-B", str(_CHILD)),
        close_fds=True,
        cwd=tmp_path,
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        assert _read_ready(blocker) == "ready"
        assert blocker.poll() is None

        assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
            succeeded=False,
            error_code=_ERROR_SHARING_VIOLATION,
        )
        assert blocker.poll() is None
        assert live_path.is_dir()
        assert not os.path.isjunction(live_path)
        assert not os.path.lexists(displaced_path)
        assert candidate_path.read_bytes() == b"m159-broken-control-pipe"

        stdin = blocker.stdin
        stdout = blocker.stdout
        stderr = blocker.stderr
        if stdin is None or stdout is None or stderr is None:
            raise RuntimeError("share-delete blocker pipes are unavailable") from None

        blocker.kill()
        return_code = blocker.wait(timeout=_TIMEOUT_SECONDS)
        assert return_code != 0

        assert stdout.read(_MAX_LINE_BYTES + 1) == b""
        assert stderr.read(_MAX_LINE_BYTES + 1) == b""

        assert _attempt_native_pipe_write(cast(BinaryIO, stdin)) == _NativePipeWriteResult(
            succeeded=False,
            error_code=_ERROR_NO_DATA,
            bytes_written=0,
        )
        stdin.close()
        assert stdin.closed

        assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
            succeeded=True,
            error_code=0,
        )
        assert not os.path.lexists(live_path)
        assert displaced_path.is_dir()
        assert not os.path.isjunction(displaced_path)
        assert displaced_candidate.read_bytes() == b"m159-broken-control-pipe"
    finally:
        _close_child(blocker)

    assert blocker.returncode is not None
    assert blocker.returncode != 0
    assert displaced_candidate.read_bytes() == b"m159-broken-control-pipe"
