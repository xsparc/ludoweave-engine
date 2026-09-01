"""Test-only Windows retained process-image binding probe."""

from __future__ import annotations

import ctypes
import hashlib
import os
import sys
from collections.abc import Callable
from ctypes import wintypes
from dataclasses import dataclass, replace
from pathlib import Path
from types import TracebackType
from typing import Protocol, cast

import pytest

from tests.integration.test_windows_local_control_channel_probe import (
    _DIRECT_PYTHON,  # pyright: ignore[reportPrivateUsage]
    _canonical_document,  # pyright: ignore[reportPrivateUsage]
    _challenge,  # pyright: ignore[reportPrivateUsage]
    _start_or_skip,  # pyright: ignore[reportPrivateUsage]
    _WindowsControlProbe,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_local_control_token_binding_probe import (
    _NativeSessionBinding,  # pyright: ignore[reportPrivateUsage]
    _RetainedTokenBinding,  # pyright: ignore[reportPrivateUsage]
    _verify_same_logon,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_local_control_token_binding_probe import (
    _verify_stable as _verify_token_stable,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M214 probes native Windows retained process-image binding",
)

_GENERIC_READ = 0x80000000
_FILE_SHARE_READ = 0x00000001
_FILE_SHARE_WRITE = 0x00000002
_FILE_SHARE_DELETE = 0x00000004
_OPEN_EXISTING = 3
_FILE_ATTRIBUTE_NORMAL = 0x00000080
_FILE_BEGIN = 0
_FILE_ID_INFO_CLASS = 18
_MAX_IMAGE_BYTES = 64 * 1_024 * 1_024
_READ_CHUNK_BYTES = 64 * 1_024
_IMAGE_PATH_CAPACITY = 32_768
_INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value


class _NativeFunction(Protocol):
    argtypes: list[object] | None
    restype: object

    def __call__(self, *arguments: object) -> object: ...


class _FILE_ID_128(ctypes.Structure):
    _fields_ = [("Identifier", wintypes.BYTE * 16)]


class _FILE_ID_INFO(ctypes.Structure):
    _fields_ = [
        ("VolumeSerialNumber", ctypes.c_ulonglong),
        ("FileId", _FILE_ID_128),
    ]


@dataclass(frozen=True, slots=True)
class _ImageSnapshot:
    normalized_name: str
    volume_serial: int
    file_id: bytes
    size: int
    sha256: bytes


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


def _handle_value(handle: int | wintypes.HANDLE, operation: str) -> int:
    value = handle if isinstance(handle, int) else handle.value
    if value is None or value == 0 or value == _INVALID_HANDLE_VALUE:
        raise RuntimeError(f"{operation} returned an invalid handle") from None
    return value


def _normalized_name(path: str | Path) -> str:
    absolute = os.path.abspath(str(path))
    return os.path.normcase(os.path.realpath(absolute))


class _ImageApi:
    def __init__(self) -> None:
        win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
        self.get_last_error = cast(Callable[[], int], vars(ctypes)["get_last_error"])
        kernel32 = win_dll("kernel32", use_last_error=True)
        self.close_handle = _load_function(
            kernel32, "CloseHandle", [wintypes.HANDLE], wintypes.BOOL
        )
        self.create_file = _load_function(
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
        self.get_file_information = _load_function(
            kernel32,
            "GetFileInformationByHandleEx",
            [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD],
            wintypes.BOOL,
        )
        self.get_file_size = _load_function(
            kernel32,
            "GetFileSizeEx",
            [wintypes.HANDLE, ctypes.POINTER(ctypes.c_longlong)],
            wintypes.BOOL,
        )
        self.set_file_pointer = _load_function(
            kernel32,
            "SetFilePointerEx",
            [
                wintypes.HANDLE,
                ctypes.c_longlong,
                ctypes.POINTER(ctypes.c_longlong),
                wintypes.DWORD,
            ],
            wintypes.BOOL,
        )
        self.read_file = _load_function(
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
        self.query_process_image = _load_function(
            kernel32,
            "QueryFullProcessImageNameW",
            [
                wintypes.HANDLE,
                wintypes.DWORD,
                wintypes.LPWSTR,
                ctypes.POINTER(wintypes.DWORD),
            ],
            wintypes.BOOL,
        )

    def fail(self, operation: str) -> RuntimeError:
        code = self.get_last_error()
        return RuntimeError(f"{operation} failed with native code {code}")


class _RetainedImageFile:
    """Own one read-only image file handle and produce bounded private snapshots."""

    def __init__(self, path: str | Path) -> None:
        self._api = _ImageApi()
        self._close_handle = self._api.close_handle
        self._name = _normalized_name(path)
        raw = cast(
            wintypes.HANDLE,
            self._api.create_file(
                self._name,
                _GENERIC_READ,
                _FILE_SHARE_READ | _FILE_SHARE_WRITE | _FILE_SHARE_DELETE,
                None,
                _OPEN_EXISTING,
                _FILE_ATTRIBUTE_NORMAL,
                wintypes.HANDLE(),
            ),
        )
        self.handle = _handle_value(raw, "CreateFileW")

    def __enter__(self) -> _RetainedImageFile:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        handle = self.handle
        if handle == 0:
            return
        if not cast(bool, self._close_handle(wintypes.HANDLE(handle))):
            raise self._api.fail("CloseHandle") from None
        self.handle = 0

    def _size(self) -> int:
        size = ctypes.c_longlong()
        if not cast(
            bool,
            self._api.get_file_size(wintypes.HANDLE(self.handle), ctypes.byref(size)),
        ):
            raise self._api.fail("GetFileSizeEx") from None
        if size.value <= 0 or size.value > _MAX_IMAGE_BYTES:
            raise RuntimeError("image file size was outside the fixed bound") from None
        return size.value

    def _identity(self) -> tuple[int, bytes]:
        information = _FILE_ID_INFO()
        if not cast(
            bool,
            self._api.get_file_information(
                wintypes.HANDLE(self.handle),
                _FILE_ID_INFO_CLASS,
                ctypes.byref(information),
                ctypes.sizeof(information),
            ),
        ):
            raise self._api.fail("GetFileInformationByHandleEx") from None
        return information.VolumeSerialNumber, bytes(information.FileId.Identifier)

    def _digest(self, size: int) -> bytes:
        position = ctypes.c_longlong()
        if not cast(
            bool,
            self._api.set_file_pointer(
                wintypes.HANDLE(self.handle),
                ctypes.c_longlong(0),
                ctypes.byref(position),
                _FILE_BEGIN,
            ),
        ):
            raise self._api.fail("SetFilePointerEx") from None
        if position.value != 0:
            raise RuntimeError("image file pointer did not return to the start") from None

        digest = hashlib.sha256()
        remaining = size
        while remaining:
            requested = min(remaining, _READ_CHUNK_BYTES)
            buffer = ctypes.create_string_buffer(requested)
            received = wintypes.DWORD()
            if not cast(
                bool,
                self._api.read_file(
                    wintypes.HANDLE(self.handle),
                    buffer,
                    requested,
                    ctypes.byref(received),
                    None,
                ),
            ):
                raise self._api.fail("ReadFile") from None
            if received.value == 0 or received.value > requested:
                raise RuntimeError("image file read did not make bounded progress") from None
            digest.update(buffer.raw[: received.value])
            remaining -= received.value
        return digest.digest()

    def snapshot(self, *, normalized_name: str | None = None) -> _ImageSnapshot:
        size = self._size()
        volume_serial, file_id = self._identity()
        digest = self._digest(size)
        if self._size() != size or self._identity() != (volume_serial, file_id):
            raise RuntimeError("image file identity changed during snapshot") from None
        return _ImageSnapshot(
            normalized_name=self._name if normalized_name is None else normalized_name,
            volume_serial=volume_serial,
            file_id=file_id,
            size=size,
            sha256=digest,
        )


class _RetainedProcessImage:
    """Retain the image opened from one retained process handle."""

    def __init__(self, process: int) -> None:
        self._api = _ImageApi()
        self._process = process
        self._image = _RetainedImageFile(self._query_name())

    def __enter__(self) -> _RetainedProcessImage:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        self._image.close()

    def _query_name(self) -> str:
        buffer = ctypes.create_unicode_buffer(_IMAGE_PATH_CAPACITY)
        length = wintypes.DWORD(len(buffer))
        if not cast(
            bool,
            self._api.query_process_image(
                wintypes.HANDLE(self._process),
                0,
                buffer,
                ctypes.byref(length),
            ),
        ):
            raise self._api.fail("QueryFullProcessImageNameW") from None
        if length.value == 0 or length.value >= len(buffer):
            raise RuntimeError("process image name length was invalid") from None
        return _normalized_name(buffer.value[: length.value])

    def snapshot(self) -> _ImageSnapshot:
        return self._image.snapshot(normalized_name=self._query_name())


def _verify_expected_image(expected: _ImageSnapshot, observed: _ImageSnapshot) -> None:
    if observed != expected:
        raise RuntimeError("retained process image did not match the expected image") from None


def _verify_stable(before: _ImageSnapshot, after: _ImageSnapshot) -> None:
    if after != before:
        raise RuntimeError("retained process image changed before release") from None


def test_retained_process_image_is_stable() -> None:
    probe = _WindowsControlProbe()
    with probe, _RetainedImageFile(_DIRECT_PYTHON) as expected_file:
        expected = expected_file.snapshot()
        session = _start_or_skip(probe)
        with (
            _RetainedTokenBinding(0) as controller_binding,
            _RetainedTokenBinding(session.process) as participant_binding,
            _RetainedProcessImage(session.process) as observed,
        ):
            controller = controller_binding.snapshot()
            participant = participant_binding.snapshot()
            _verify_same_logon(controller, participant)
            _NativeSessionBinding().verify(session.pipe, session.pid, participant)
            participant_logon_sid = ctypes.create_string_buffer(participant.logon_sid)
            probe._verify_pipe_dacl(  # pyright: ignore[reportPrivateUsage]
                session.pipe, ctypes.addressof(participant_logon_sid)
            )
            before = observed.snapshot()
            _verify_expected_image(expected, before)
            _challenge(probe, session)
            _verify_token_stable(participant, participant_binding.snapshot())
            _verify_stable(expected, expected_file.snapshot())
            _verify_stable(before, observed.snapshot())
            probe.write_document(
                session.pipe,
                _canonical_document("release", session.challenge, 2),
            )
            released = probe.read_document(session.pipe)
            assert released == _canonical_document("released", session.challenge, 3)
        probe.settle(session, 0)
    assert probe.owned_count == 0


def _sample_snapshot() -> _ImageSnapshot:
    return _ImageSnapshot("c:\\pythonw.exe", 1, b"file-id", 2, b"digest")


@pytest.mark.parametrize(
    "changed",
    [
        {"normalized_name": "c:\\other.exe"},
        {"volume_serial": 2},
        {"file_id": b"other"},
        {"size": 3},
        {"sha256": b"other"},
    ],
)
def test_unexpected_process_image_fails_closed(changed: dict[str, object]) -> None:
    expected = _sample_snapshot()
    with pytest.raises(RuntimeError, match="did not match"):
        _verify_expected_image(expected, replace(expected, **changed))


@pytest.mark.parametrize(
    "changed",
    [
        {"normalized_name": "c:\\other.exe"},
        {"volume_serial": 2},
        {"file_id": b"other"},
        {"size": 3},
        {"sha256": b"other"},
    ],
)
def test_retained_process_image_drift_fails_closed(changed: dict[str, object]) -> None:
    before = _sample_snapshot()
    with pytest.raises(RuntimeError, match="changed before release"):
        _verify_stable(before, replace(before, **changed))


def test_identical_process_image_snapshot_is_accepted() -> None:
    snapshot = _sample_snapshot()
    _verify_expected_image(snapshot, snapshot)
    _verify_stable(snapshot, snapshot)
