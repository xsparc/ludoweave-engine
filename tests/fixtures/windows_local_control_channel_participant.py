"""Fixed participant for the M212 Windows local control-channel probe."""

from __future__ import annotations

import ctypes
import json
import string
import sys
from collections.abc import Callable, Mapping
from ctypes import wintypes
from typing import Protocol, cast

_SCHEMA = "ludoweave.test.windows-local-control-channel/1"
_PIPE_PREFIX = r"\\.\pipe\ludoweave-m212-"
_MAX_MESSAGE_BYTES = 1_024

_GENERIC_READ = 0x80000000
_GENERIC_WRITE = 0x40000000
_OPEN_EXISTING = 3
_SECURITY_SQOS_PRESENT = 0x00100000
_SECURITY_IDENTIFICATION = 0x00010000

_ERROR_BROKEN_PIPE = 109
_ERROR_NO_DATA = 232
_ERROR_PIPE_NOT_CONNECTED = 233
_INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

_EXIT_USAGE = 2
_EXIT_CONNECT = 10
_EXIT_PROTOCOL = 11
_EXIT_CHALLENGE = 12
_EXIT_DISCONNECT = 13


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


def _handle_value(handle: int | wintypes.HANDLE) -> int | None:
    value = handle if isinstance(handle, int) else handle.value
    if value is None or value == 0 or value == _INVALID_HANDLE_VALUE:
        return None
    return value


def _valid_pipe_name(value: str) -> bool:
    if not value.startswith(_PIPE_PREFIX):
        return False
    suffix = value[len(_PIPE_PREFIX) :]
    return len(suffix) == 32 and all(character in string.hexdigits[:16] for character in suffix)


def _canonical_document(kind: str, challenge: str, sequence: int) -> dict[str, object]:
    return {
        "challenge": challenge,
        "kind": kind,
        "schema": _SCHEMA,
        "sequence": sequence,
    }


def _encode(document: Mapping[str, object]) -> bytes:
    return json.dumps(document, sort_keys=True, separators=(",", ":")).encode()


def _decode(message: bytes) -> dict[str, object]:
    if not message or len(message) > _MAX_MESSAGE_BYTES:
        raise ValueError("message size is invalid")
    try:
        parsed: object = json.loads(message)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ValueError("message is not canonical JSON") from None
    if not isinstance(parsed, dict):
        raise ValueError("message is not a JSON object")
    document = cast(dict[str, object], parsed)
    if _encode(document) != message:
        raise ValueError("message is not canonical JSON")
    if set(document) != {"challenge", "kind", "schema", "sequence"}:
        raise ValueError("message shape is invalid")
    if document["schema"] != _SCHEMA:
        raise ValueError("message schema is invalid")
    challenge = document["challenge"]
    if (
        type(challenge) is not str
        or len(challenge) != 64
        or any(character not in string.hexdigits[:16] for character in challenge)
    ):
        raise ValueError("challenge is invalid")
    if type(document["kind"]) is not str or type(document["sequence"]) is not int:
        raise ValueError("message fields are invalid")
    return document


class _PipeClient:
    def __init__(self) -> None:
        win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
        self._get_last_error = cast(Callable[[], int], vars(ctypes)["get_last_error"])
        kernel32 = win_dll("kernel32", use_last_error=True)
        self._create_file = _load_function(
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
        self._read_file = _load_function(
            kernel32,
            "ReadFile",
            [
                wintypes.HANDLE,
                ctypes.c_void_p,
                wintypes.DWORD,
                ctypes.POINTER(wintypes.DWORD),
                ctypes.c_void_p,
            ],
            wintypes.BOOL,
        )
        self._write_file = _load_function(
            kernel32,
            "WriteFile",
            [
                wintypes.HANDLE,
                ctypes.c_void_p,
                wintypes.DWORD,
                ctypes.POINTER(wintypes.DWORD),
                ctypes.c_void_p,
            ],
            wintypes.BOOL,
        )
        self._close_handle = _load_function(
            kernel32,
            "CloseHandle",
            [wintypes.HANDLE],
            wintypes.BOOL,
        )

    def connect(self, pipe_name: str) -> int | None:
        raw = cast(
            wintypes.HANDLE,
            self._create_file(
                pipe_name,
                _GENERIC_READ | _GENERIC_WRITE,
                0,
                None,
                _OPEN_EXISTING,
                _SECURITY_SQOS_PRESENT | _SECURITY_IDENTIFICATION,
                None,
            ),
        )
        handle = _handle_value(raw)
        return handle

    def read(self, pipe: int) -> bytes | None:
        buffer = ctypes.create_string_buffer(_MAX_MESSAGE_BYTES)
        received = wintypes.DWORD()
        if not cast(
            bool,
            self._read_file(
                wintypes.HANDLE(pipe),
                buffer,
                len(buffer),
                ctypes.byref(received),
                None,
            ),
        ):
            if self._get_last_error() in {
                _ERROR_BROKEN_PIPE,
                _ERROR_NO_DATA,
                _ERROR_PIPE_NOT_CONNECTED,
            }:
                return None
            raise RuntimeError("ReadFile failed") from None
        return bytes(buffer.raw[: received.value])

    def write(self, pipe: int, document: Mapping[str, object]) -> bool:
        message = _encode(document)
        if not message or len(message) > _MAX_MESSAGE_BYTES:
            return False
        buffer = ctypes.create_string_buffer(message)
        written = wintypes.DWORD()
        if not cast(
            bool,
            self._write_file(
                wintypes.HANDLE(pipe),
                buffer,
                len(message),
                ctypes.byref(written),
                None,
            ),
        ):
            return False
        return written.value == len(message)

    def close(self, pipe: int) -> None:
        self._close_handle(wintypes.HANDLE(pipe))


def _run(pipe_name: str) -> int:
    client = _PipeClient()
    pipe = client.connect(pipe_name)
    if pipe is None:
        return _EXIT_CONNECT
    try:
        challenge_message = client.read(pipe)
        if challenge_message is None:
            return _EXIT_DISCONNECT
        try:
            challenge_document = _decode(challenge_message)
        except ValueError:
            return _EXIT_PROTOCOL
        challenge = cast(str, challenge_document["challenge"])
        if challenge_document["kind"] != "challenge" or challenge_document["sequence"] != 0:
            return _EXIT_PROTOCOL
        if not client.write(pipe, _canonical_document("ready", challenge, 1)):
            return _EXIT_DISCONNECT

        release_message = client.read(pipe)
        if release_message is None:
            return _EXIT_DISCONNECT
        try:
            release_document = _decode(release_message)
        except ValueError:
            return _EXIT_PROTOCOL
        if release_document["kind"] != "release" or release_document["sequence"] != 2:
            return _EXIT_PROTOCOL
        if release_document["challenge"] != challenge:
            return _EXIT_CHALLENGE
        if not client.write(pipe, _canonical_document("released", challenge, 3)):
            return _EXIT_DISCONNECT
        return 0
    finally:
        client.close(pipe)


def main() -> int:
    if len(sys.argv) != 2 or not _valid_pipe_name(sys.argv[1]):
        return _EXIT_USAGE
    return _run(sys.argv[1])


if __name__ == "__main__":
    raise SystemExit(main())
