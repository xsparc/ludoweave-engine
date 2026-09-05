"""Test-only Windows junction refusal probe for M150.

The fixture uses the documented ``mklink /j`` command only beneath pytest-owned
temporary storage. The cleanup probe and every native handle remain private to
the test suite.
"""

from __future__ import annotations

import ctypes
import os
import subprocess
import sys
from collections.abc import Callable
from ctypes import wintypes
from pathlib import Path
from typing import Protocol, cast

import pytest
from test_windows_cache_cleanup_capability_probe import (
    _UnsafeComponent,  # pyright: ignore[reportPrivateUsage]
    _WindowsCapabilityProbe,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M150 probes documented Windows directory-junction behavior",
)

_FILE_SUPPORTS_REPARSE_POINTS = 0x00000080
_FILESYSTEM_NAME_CAPACITY = 64


class _NativeFunction(Protocol):
    argtypes: list[object] | None
    restype: object

    def __call__(self, *arguments: object) -> object: ...


def _load_function(
    library: ctypes.CDLL,
    name: str,
    argument_types: list[object],
    return_type: object,
) -> _NativeFunction:
    function = cast(_NativeFunction, getattr(library, name))
    function.argtypes = argument_types
    function.restype = return_type
    return function


def _filesystem_information(handle: int) -> tuple[str, int]:
    win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
    library = win_dll("kernel32", use_last_error=True)
    function = _load_function(
        library,
        "GetVolumeInformationByHandleW",
        [
            wintypes.HANDLE,
            wintypes.LPWSTR,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            ctypes.POINTER(wintypes.DWORD),
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPWSTR,
            wintypes.DWORD,
        ],
        wintypes.BOOL,
    )
    flags = wintypes.DWORD()
    filesystem_name = ctypes.create_unicode_buffer(_FILESYSTEM_NAME_CAPACITY)
    result = function(
        wintypes.HANDLE(handle),
        None,
        0,
        None,
        None,
        ctypes.byref(flags),
        filesystem_name,
        len(filesystem_name),
    )
    if not cast(bool, result):
        get_last_error = cast(Callable[[], int], vars(ctypes)["get_last_error"])
        error_code = get_last_error()
        raise OSError(error_code, "GetVolumeInformationByHandleW failed")
    return filesystem_name.value, flags.value


def _create_directory_junction(working_directory: Path) -> None:
    completed = subprocess.run(
        ["cmd.exe", "/d", "/c", "mklink", "/j", "linked", r"..\target"],
        check=False,
        capture_output=True,
        cwd=working_directory,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"mklink /j failed with exit code {completed.returncode}") from None


def test_windows_probe_refuses_an_ntfs_directory_junction(tmp_path: Path) -> None:
    live_path = tmp_path / "live"
    target_path = tmp_path / "target"
    junction_path = live_path / "linked"
    marker_path = target_path / "marker.bin"
    live_path.mkdir()
    target_path.mkdir()
    marker_path.write_bytes(b"m150-target-remains-owned")

    with _WindowsCapabilityProbe() as probe:
        root = probe.open_root(tmp_path)
        filesystem_name, filesystem_flags = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M150 junction fixture requires an NTFS pytest volume")
        assert filesystem_flags & _FILE_SUPPORTS_REPARSE_POINTS

        try:
            _create_directory_junction(live_path)
            assert os.path.isjunction(junction_path)
            live = probe.open_directory(root, "live")

            with pytest.raises(_UnsafeComponent, match="reparse component refused"):
                probe.open_directory(live, "linked")

            assert probe.owned_count == 2
            assert marker_path.read_bytes() == b"m150-target-remains-owned"
        finally:
            if os.path.lexists(junction_path):
                os.rmdir(junction_path)

    assert marker_path.read_bytes() == b"m150-target-remains-owned"
    assert not os.path.lexists(junction_path)
