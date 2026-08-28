"""Fixed namespace mutator for the M174 Windows coordination-lock probe."""

from __future__ import annotations

import ctypes
import json
import os
import sys
from collections.abc import Callable
from ctypes import wintypes
from typing import Protocol, cast

_SCHEMA = "ludoweave.test.windows-coordination-lock-substitution/1"
_SOURCE_NAME = r"live\coordination.lock"
_DISPLACED_NAME = r"live\coordination.displaced"
_PAYLOAD = b"ludoweave-m173-coordination-v1\n"
_GENERIC_WRITE = 0x40000000
_FILE_SHARE_READ = 0x00000001
_FILE_SHARE_WRITE = 0x00000002
_FILE_SHARE_DELETE = 0x00000004
_CREATE_NEW = 1
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


def _emit(phase: str, *, error_code: int = 0) -> None:
    print(
        json.dumps(
            {"error_code": error_code, "phase": phase, "schema": _SCHEMA},
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )


def main() -> int:
    if sys.platform != "win32":
        return 2

    win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
    get_last_error = cast(Callable[[], int], vars(ctypes)["get_last_error"])
    kernel32 = win_dll("kernel32", use_last_error=True)
    move_file = _load_function(
        kernel32,
        "MoveFileExW",
        [wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD],
        wintypes.BOOL,
    )
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
    write_file = _load_function(
        kernel32,
        "WriteFile",
        [
            wintypes.HANDLE,
            ctypes.c_void_p,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        ],
        wintypes.BOOL,
    )
    close_handle = _load_function(
        kernel32,
        "CloseHandle",
        [wintypes.HANDLE],
        wintypes.BOOL,
    )

    if not cast(bool, move_file(_SOURCE_NAME, _DISPLACED_NAME, 0)):
        _emit("rename_failed", error_code=get_last_error())
        return 0

    raw_handle = create_file(
        _SOURCE_NAME,
        _GENERIC_WRITE,
        _FILE_SHARE_READ | _FILE_SHARE_WRITE | _FILE_SHARE_DELETE,
        None,
        _CREATE_NEW,
        _FILE_ATTRIBUTE_NORMAL,
        None,
    )
    handle = cast(int | None, raw_handle)
    if handle is None or handle == _INVALID_HANDLE_VALUE:
        _emit("create_failed", error_code=get_last_error())
        return 0
    if os.get_handle_inheritable(handle):
        close_handle(wintypes.HANDLE(handle))
        _emit("inheritable_handle")
        return 0

    buffer = ctypes.create_string_buffer(_PAYLOAD)
    written = wintypes.DWORD()
    if not cast(
        bool,
        write_file(
            wintypes.HANDLE(handle),
            ctypes.cast(buffer, ctypes.c_void_p),
            len(_PAYLOAD),
            ctypes.byref(written),
            None,
        ),
    ):
        error_code = get_last_error()
        close_handle(wintypes.HANDLE(handle))
        _emit("write_failed", error_code=error_code)
        return 0
    if written.value != len(_PAYLOAD):
        close_handle(wintypes.HANDLE(handle))
        _emit("short_write")
        return 0
    if not cast(bool, close_handle(wintypes.HANDLE(handle))):
        _emit("close_failed", error_code=get_last_error())
        return 0

    _emit("substituted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
