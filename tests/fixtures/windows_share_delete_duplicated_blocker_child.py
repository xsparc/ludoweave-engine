"""Fixed duplicated-handle blocker for the M162 Windows probe."""

from __future__ import annotations

import ctypes
import json
import sys
from collections.abc import Callable
from ctypes import wintypes
from typing import Protocol, cast

_SCHEMA = "ludoweave.test.windows-duplicated-share-delete-blocker/1"
_DIRECTORY_NAME = "live"
_CLOSE_ORIGINAL_TOKEN = b"1"
_CLOSE_DUPLICATE_TOKEN = b"2"
_FILE_LIST_DIRECTORY = 0x00000001
_FILE_READ_ATTRIBUTES = 0x00000080
_FILE_SHARE_READ = 0x00000001
_FILE_SHARE_WRITE = 0x00000002
_SYNCHRONIZE = 0x00100000
_OPEN_EXISTING = 3
_FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
_FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
_DUPLICATE_SAME_ACCESS = 0x00000002
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
    get_current_process = _load_function(
        kernel32,
        "GetCurrentProcess",
        [],
        wintypes.HANDLE,
    )
    duplicate_handle = _load_function(
        kernel32,
        "DuplicateHandle",
        [
            wintypes.HANDLE,
            wintypes.HANDLE,
            wintypes.HANDLE,
            ctypes.POINTER(wintypes.HANDLE),
            wintypes.DWORD,
            wintypes.BOOL,
            wintypes.DWORD,
        ],
        wintypes.BOOL,
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
        _FILE_SHARE_READ | _FILE_SHARE_WRITE,
        None,
        _OPEN_EXISTING,
        _FILE_FLAG_BACKUP_SEMANTICS | _FILE_FLAG_OPEN_REPARSE_POINT,
        None,
    )
    opened_handle = cast(int | None, raw_handle)
    if opened_handle is None or opened_handle == _INVALID_HANDLE_VALUE:
        return 3

    source_handle: int | None = opened_handle
    duplicate_value: int | None = None
    exit_code = 0
    try:
        process_handle = cast(int | None, get_current_process())
        if process_handle is None:
            exit_code = 4
        else:
            duplicate_result = wintypes.HANDLE()
            duplicated = cast(
                bool,
                duplicate_handle(
                    wintypes.HANDLE(process_handle),
                    wintypes.HANDLE(opened_handle),
                    wintypes.HANDLE(process_handle),
                    ctypes.byref(duplicate_result),
                    0,
                    False,
                    _DUPLICATE_SAME_ACCESS,
                ),
            )
            candidate = duplicate_result.value
            if not duplicated or candidate is None or candidate == _INVALID_HANDLE_VALUE:
                exit_code = 5
            else:
                duplicate_value = candidate
                _emit("ready")
                if sys.stdin.buffer.read(1) != _CLOSE_ORIGINAL_TOKEN:
                    exit_code = 6
                else:
                    source_to_close = source_handle
                    source_handle = None
                    if not cast(
                        bool,
                        close_handle(wintypes.HANDLE(source_to_close)),
                    ):
                        exit_code = 7
                    else:
                        _emit("original-closed")
                        if sys.stdin.buffer.read(1) != _CLOSE_DUPLICATE_TOKEN:
                            exit_code = 8
                        else:
                            duplicate_to_close = duplicate_value
                            duplicate_value = None
                            if not cast(
                                bool,
                                close_handle(wintypes.HANDLE(duplicate_to_close)),
                            ):
                                exit_code = 9
    finally:
        if source_handle is not None and not cast(
            bool,
            close_handle(wintypes.HANDLE(source_handle)),
        ):
            exit_code = 10
        if duplicate_value is not None and not cast(
            bool,
            close_handle(wintypes.HANDLE(duplicate_value)),
        ):
            exit_code = 11

    if exit_code != 0:
        return exit_code
    _emit("closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
