"""Fixed descendant-file holder for the M172 Windows non-exclusion probe."""

from __future__ import annotations

import ctypes
import json
import os
import sys
from collections.abc import Callable
from ctypes import wintypes
from typing import Protocol, cast

_SCHEMA = "ludoweave.test.windows-descendant-file-holder/1"
_FILE_NAME = r"live\candidate.bin"
_RELEASE_TOKEN = b"!"
_GENERIC_READ = 0x80000000
_FILE_SHARE_READ = 0x00000001
_FILE_SHARE_WRITE = 0x00000002
_FILE_SHARE_DELETE = 0x00000004
_OPEN_EXISTING = 3
_FILE_ATTRIBUTE_NORMAL = 0x00000080
_INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value


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


def _emit(phase: str) -> None:
    print(
        json.dumps(
            {"phase": phase, "schema": _SCHEMA},
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ),
        flush=True,
    )


def main() -> int:
    if sys.platform != "win32":
        return 2

    win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
    kernel32 = win_dll("kernel32", use_last_error=True)
    create_file = _load_function(
        kernel32,
        "CreateFileW",
        [
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.HANDLE,
        ],
        wintypes.HANDLE,
    )
    close_handle = _load_function(
        kernel32,
        "CloseHandle",
        [wintypes.HANDLE],
        wintypes.BOOL,
    )

    raw_handle = create_file(
        _FILE_NAME,
        _GENERIC_READ,
        _FILE_SHARE_READ | _FILE_SHARE_WRITE | _FILE_SHARE_DELETE,
        None,
        _OPEN_EXISTING,
        _FILE_ATTRIBUTE_NORMAL,
        None,
    )
    handle = cast(int | None, raw_handle)
    if handle is None or handle == _INVALID_HANDLE_VALUE:
        return 3
    if os.get_handle_inheritable(handle):
        close_handle(wintypes.HANDLE(handle))
        return 6

    exit_code = 0
    try:
        _emit("ready")
        if sys.stdin.buffer.read(1) != _RELEASE_TOKEN:
            exit_code = 4
    finally:
        if not cast(bool, close_handle(wintypes.HANDLE(handle))):
            exit_code = 5

    if exit_code != 0:
        return exit_code
    _emit("closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
