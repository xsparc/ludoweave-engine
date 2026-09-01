"""Fixed Windows access-only contender for the M218 integration probe."""

from __future__ import annotations

import ctypes
import sys
from collections.abc import Callable
from ctypes import wintypes
from pathlib import Path
from typing import Protocol, cast

_TARGET = Path(__file__).with_name("windows_local_control_channel_participant.py")

_DELETE = 0x00010000
_GENERIC_WRITE = 0x40000000
_FILE_SHARE_READ = 0x00000001
_FILE_SHARE_WRITE = 0x00000002
_FILE_SHARE_DELETE = 0x00000004
_OPEN_EXISTING = 3
_FILE_ATTRIBUTE_NORMAL = 0x00000080
_INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
_ERROR_SHARING_VIOLATION = 32
_COMPETING_SHARE_MODE = _FILE_SHARE_READ | _FILE_SHARE_WRITE | _FILE_SHARE_DELETE

_EXIT_INVALID_INVOCATION = 64
_EXIT_TARGET_MISSING = 65
_EXIT_UNEXPECTED_SUCCESS = 70
_EXIT_UNEXPECTED_ERROR = 80
_EXIT_CLOSE_FAILURE = 90


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


def _attempt_access(desired_access: int, ordinal: int) -> int:
    win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
    get_last_error = cast(Callable[[], int], vars(ctypes)["get_last_error"])
    set_last_error = cast(Callable[[int], None], vars(ctypes)["set_last_error"])
    kernel32 = win_dll("kernel32", use_last_error=True)
    create_file = _load_function(
        kernel32,
        "CreateFileW",
        [
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            ctypes.c_void_p,
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

    set_last_error(0)
    raw = cast(
        wintypes.HANDLE,
        create_file(
            str(_TARGET),
            desired_access,
            _COMPETING_SHARE_MODE,
            None,
            _OPEN_EXISTING,
            _FILE_ATTRIBUTE_NORMAL,
            wintypes.HANDLE(),
        ),
    )
    value = raw if isinstance(raw, int) else raw.value
    error_code = get_last_error()
    if value is not None and value != 0 and value != _INVALID_HANDLE_VALUE:
        if not cast(bool, close_handle(wintypes.HANDLE(value))):
            return _EXIT_CLOSE_FAILURE + ordinal
        return _EXIT_UNEXPECTED_SUCCESS + ordinal
    if error_code != _ERROR_SHARING_VIOLATION:
        return _EXIT_UNEXPECTED_ERROR + ordinal
    return 0


def main() -> int:
    if len(sys.argv) != 1:
        return _EXIT_INVALID_INVOCATION
    if not _TARGET.is_file():
        return _EXIT_TARGET_MISSING
    for ordinal, desired_access in enumerate((_GENERIC_WRITE, _DELETE)):
        result = _attempt_access(desired_access, ordinal)
        if result != 0:
            return result
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
