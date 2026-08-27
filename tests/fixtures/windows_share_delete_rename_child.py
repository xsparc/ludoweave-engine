"""Fixed isolated child for the M154 Windows native-rename probe."""

from __future__ import annotations

import ctypes
import json
import sys
from collections.abc import Callable
from ctypes import wintypes
from typing import Protocol, cast

_SCHEMA = "ludoweave.test.windows-native-rename/1"
_SOURCE_NAME = "live"
_DESTINATION_NAME = "displaced"


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

    succeeded = bool(move_file(_SOURCE_NAME, _DESTINATION_NAME, 0))
    error_code = 0 if succeeded else get_last_error()
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
