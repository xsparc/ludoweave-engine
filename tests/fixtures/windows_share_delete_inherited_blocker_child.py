"""Fixed inherited-handle blocker for the M163 Windows probe."""

from __future__ import annotations

import ctypes
import json
import sys
from collections.abc import Callable
from ctypes import wintypes
from typing import Protocol, cast

_SCHEMA = "ludoweave.test.windows-inherited-share-delete-blocker/1"
_RELEASE_TOKEN = b"!"


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


def _parse_handle_argument() -> int | None:
    if len(sys.argv) != 2:
        return None
    argument = sys.argv[1]
    if not argument.isascii() or not argument.isdecimal():
        return None
    value = int(argument)
    if value <= 0 or argument != str(value):
        return None
    return value


def main() -> int:
    if sys.platform != "win32":
        return 2

    inherited_handle = _parse_handle_argument()
    if inherited_handle is None:
        return 3

    win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
    kernel32 = win_dll("kernel32", use_last_error=True)
    close_handle = _load_function(
        kernel32,
        "CloseHandle",
        [wintypes.HANDLE],
        wintypes.BOOL,
    )

    owned_handle: int | None = inherited_handle
    exit_code = 0
    try:
        _emit("ready")
        if sys.stdin.buffer.read(1) != _RELEASE_TOKEN:
            exit_code = 4
        else:
            handle_to_close = owned_handle
            owned_handle = None
            if not cast(
                bool,
                close_handle(wintypes.HANDLE(handle_to_close)),
            ):
                exit_code = 5
    finally:
        if owned_handle is not None and not cast(
            bool,
            close_handle(wintypes.HANDLE(owned_handle)),
        ):
            exit_code = 6

    if exit_code != 0:
        return exit_code
    _emit("closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
