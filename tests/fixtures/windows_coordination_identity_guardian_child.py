"""Expected-identity guardian for the M181 Windows coordination probe."""

from __future__ import annotations

import ctypes
import json
import os
import sys
from collections.abc import Callable
from ctypes import wintypes
from typing import Protocol, cast

_SCHEMA = "ludoweave.test.windows-coordination-identity-guardian/1"
_FILE_NAME = r"live\coordination.lock"
_RELEASE_TOKEN = b"!"
_GENERIC_READ = 0x80000000
_FILE_SHARE_READ = 0x00000001
_FILE_SHARE_WRITE = 0x00000002
_OPEN_EXISTING = 3
_FILE_ATTRIBUTE_NORMAL = 0x00000080
_FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
_FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
_FILE_ATTRIBUTE_TAG_INFO_CLASS = 9
_FILE_ID_INFO_CLASS = 18
_INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
_HEX_DIGITS = frozenset("0123456789abcdef")


class _NativeFunction(Protocol):
    argtypes: list[object] | None
    restype: object

    def __call__(self, *arguments: object) -> object: ...


class _FileAttributeTagInfo(ctypes.Structure):
    _fields_ = [
        ("FileAttributes", wintypes.DWORD),
        ("ReparseTag", wintypes.DWORD),
    ]


class _FileId128(ctypes.Structure):
    _fields_ = [("Identifier", wintypes.BYTE * 16)]


class _FileIdInfo(ctypes.Structure):
    _fields_ = [("VolumeSerialNumber", ctypes.c_ulonglong), ("FileId", _FileId128)]


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


def _parse_expected_identity() -> tuple[int, bytes] | None:
    if len(sys.argv) != 3:
        return None
    volume_text, file_id_text = sys.argv[1:]
    if not volume_text.isascii() or not volume_text.isdecimal():
        return None
    volume_serial = int(volume_text)
    if volume_text != str(volume_serial) or not 0 <= volume_serial <= 0xFFFFFFFFFFFFFFFF:
        return None
    if len(file_id_text) != 32 or any(character not in _HEX_DIGITS for character in file_id_text):
        return None
    return volume_serial, bytes.fromhex(file_id_text)


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
    expected_identity = _parse_expected_identity()
    if expected_identity is None:
        return 3

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
    get_file_information = _load_function(
        kernel32,
        "GetFileInformationByHandleEx",
        [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD],
        wintypes.BOOL,
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
        _FILE_SHARE_READ | _FILE_SHARE_WRITE,
        None,
        _OPEN_EXISTING,
        _FILE_ATTRIBUTE_NORMAL | _FILE_FLAG_OPEN_REPARSE_POINT,
        None,
    )
    handle = cast(int | None, raw_handle)
    if handle is None or handle == _INVALID_HANDLE_VALUE:
        return 4
    if os.get_handle_inheritable(handle):
        close_handle(wintypes.HANDLE(handle))
        return 5

    attributes = _FileAttributeTagInfo()
    if not cast(
        bool,
        get_file_information(
            wintypes.HANDLE(handle),
            _FILE_ATTRIBUTE_TAG_INFO_CLASS,
            ctypes.byref(attributes),
            ctypes.sizeof(attributes),
        ),
    ):
        error_code = get_last_error()
        close_handle(wintypes.HANDLE(handle))
        return 6 if error_code != 0 else 7
    if attributes.FileAttributes & _FILE_ATTRIBUTE_REPARSE_POINT:
        close_handle(wintypes.HANDLE(handle))
        return 8

    identity = _FileIdInfo()
    if not cast(
        bool,
        get_file_information(
            wintypes.HANDLE(handle),
            _FILE_ID_INFO_CLASS,
            ctypes.byref(identity),
            ctypes.sizeof(identity),
        ),
    ):
        error_code = get_last_error()
        close_handle(wintypes.HANDLE(handle))
        return 9 if error_code != 0 else 10

    observed_identity = identity.VolumeSerialNumber, bytes(identity.FileId.Identifier)
    if observed_identity != expected_identity:
        if not cast(bool, close_handle(wintypes.HANDLE(handle))):
            return 11
        _emit("identity_mismatch")
        return 0

    exit_code = 0
    try:
        _emit("ready")
        if sys.stdin.buffer.read(1) != _RELEASE_TOKEN:
            exit_code = 12
    finally:
        if not cast(bool, close_handle(wintypes.HANDLE(handle))):
            exit_code = 13

    if exit_code != 0:
        return exit_code
    _emit("closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
