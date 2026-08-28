"""Fixed one-shot directory-open child for the M171 Windows exclusion probe."""

from __future__ import annotations

import ctypes
import json
import sys
from collections.abc import Callable
from ctypes import wintypes
from typing import Protocol, cast

_SCHEMA = "ludoweave.test.windows-directory-open/1"
_DIRECTORY_NAME = "live"
_FILE_LIST_DIRECTORY = 0x00000001
_FILE_READ_ATTRIBUTES = 0x00000080
_FILE_SHARE_READ = 0x00000001
_FILE_SHARE_WRITE = 0x00000002
_FILE_SHARE_DELETE = 0x00000004
_SYNCHRONIZE = 0x00100000
_OPEN_EXISTING = 3
_FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
_FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
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


def _emit(*, succeeded: bool, error_code: int) -> None:
    print(
        json.dumps(
            {
                "error_code": error_code,
                "schema": _SCHEMA,
                "succeeded": succeeded,
            },
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
        _DIRECTORY_NAME,
        _FILE_LIST_DIRECTORY | _FILE_READ_ATTRIBUTES | _SYNCHRONIZE,
        _FILE_SHARE_READ | _FILE_SHARE_WRITE | _FILE_SHARE_DELETE,
        None,
        _OPEN_EXISTING,
        _FILE_FLAG_BACKUP_SEMANTICS | _FILE_FLAG_OPEN_REPARSE_POINT,
        None,
    )
    handle = cast(int | None, raw_handle)
    if handle is None or handle == _INVALID_HANDLE_VALUE:
        _emit(succeeded=False, error_code=get_last_error())
        return 0

    if not cast(bool, close_handle(wintypes.HANDLE(handle))):
        return 3
    _emit(succeeded=True, error_code=0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
