"""Test-only Windows handle-capability probe for M149.

The probe is deliberately not production code. It exercises documented native
filesystem primitives only inside pytest-owned temporary directories and keeps
every native handle private to this module.
"""

from __future__ import annotations

import ctypes
import os
import sys
from collections.abc import Callable
from ctypes import wintypes
from pathlib import Path
from types import TracebackType
from typing import Protocol, cast

import pytest

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M149 probes documented Windows filesystem-handle behavior",
)

_DELETE = 0x00010000
_FILE_LIST_DIRECTORY = 0x00000001
_FILE_READ_ATTRIBUTES = 0x00000080
_SYNCHRONIZE = 0x00100000

_FILE_SHARE_READ = 0x00000001
_FILE_SHARE_WRITE = 0x00000002
_FILE_SHARE_DELETE = 0x00000004
_SHARE_ALL = _FILE_SHARE_READ | _FILE_SHARE_WRITE | _FILE_SHARE_DELETE

_OPEN_EXISTING = 3
_FILE_OPEN = 1
_FILE_ATTRIBUTE_NORMAL = 0x00000080
_FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
_FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
_FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
_FILE_DIRECTORY_FILE = 0x00000001
_FILE_NON_DIRECTORY_FILE = 0x00000040
_FILE_SYNCHRONOUS_IO_NONALERT = 0x00000020
_FILE_OPEN_REPARSE_POINT = 0x00200000
_OBJ_CASE_INSENSITIVE = 0x00000040

_FILE_RENAME_INFO_CLASS = 3
_FILE_DISPOSITION_INFO_CLASS = 4
_FILE_ATTRIBUTE_TAG_INFO_CLASS = 9
_FILE_RENAME_INFORMATION_CLASS = 10
_FILE_ID_INFO_CLASS = 18

_INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value


class _NativeFunction(Protocol):
    argtypes: list[object] | None
    restype: object

    def __call__(self, *arguments: object) -> object: ...


class _UnicodeString(ctypes.Structure):
    _fields_ = [
        ("Length", wintypes.USHORT),
        ("MaximumLength", wintypes.USHORT),
        ("Buffer", wintypes.LPWSTR),
    ]


class _ObjectAttributes(ctypes.Structure):
    _fields_ = [
        ("Length", wintypes.ULONG),
        ("RootDirectory", wintypes.HANDLE),
        ("ObjectName", ctypes.POINTER(_UnicodeString)),
        ("Attributes", wintypes.ULONG),
        ("SecurityDescriptor", ctypes.c_void_p),
        ("SecurityQualityOfService", ctypes.c_void_p),
    ]


class _IoStatusValue(ctypes.Union):
    _fields_ = [  # noqa: RUF012 - ctypes requires this mutable class descriptor.
        ("Status", wintypes.LONG),
        ("Pointer", ctypes.c_void_p),
    ]


class _IoStatusBlock(ctypes.Structure):
    _fields_ = [("Value", _IoStatusValue), ("Information", ctypes.c_size_t)]


class _FileId128(ctypes.Structure):
    _fields_ = [("Identifier", wintypes.BYTE * 16)]


class _FileIdInfo(ctypes.Structure):
    _fields_ = [("VolumeSerialNumber", ctypes.c_ulonglong), ("FileId", _FileId128)]


class _FileAttributeTagInfo(ctypes.Structure):
    _fields_ = [("FileAttributes", wintypes.DWORD), ("ReparseTag", wintypes.DWORD)]


class _FileTime(ctypes.Structure):
    _fields_ = [("Low", wintypes.DWORD), ("High", wintypes.DWORD)]


class _ByHandleFileInformation(ctypes.Structure):
    _fields_ = [
        ("FileAttributes", wintypes.DWORD),
        ("CreationTime", _FileTime),
        ("LastAccessTime", _FileTime),
        ("LastWriteTime", _FileTime),
        ("VolumeSerialNumber", wintypes.DWORD),
        ("FileSizeHigh", wintypes.DWORD),
        ("FileSizeLow", wintypes.DWORD),
        ("NumberOfLinks", wintypes.DWORD),
        ("FileIndexHigh", wintypes.DWORD),
        ("FileIndexLow", wintypes.DWORD),
    ]


class _FileRenameInformation(ctypes.Structure):
    _fields_ = [
        ("ReplaceIfExists", wintypes.BOOLEAN),
        ("RootDirectory", wintypes.HANDLE),
        ("FileNameLength", wintypes.DWORD),
        ("FileName", wintypes.WCHAR * 1),
    ]


class _FileDispositionInfo(ctypes.Structure):
    _fields_ = [("DeleteFile", wintypes.BOOLEAN)]


class _NativeFailure(RuntimeError):
    def __init__(self, operation: str, code: int) -> None:
        self.operation = operation
        self.code = code
        super().__init__(f"{operation} failed with native code {code}")


class _UnsafeComponent(RuntimeError):
    pass


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


def _validate_component(name: str) -> None:
    if not name or name in {".", ".."} or "/" in name or "\\" in name or "\0" in name:
        raise ValueError("a single non-special relative component is required")


class _WindowsCapabilityProbe:
    def __init__(self) -> None:
        win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
        self._get_last_error = cast(Callable[[], int], vars(ctypes)["get_last_error"])
        kernel32 = win_dll("kernel32", use_last_error=True)
        ntdll = win_dll("ntdll", use_last_error=True)
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
        self._get_file_information = _load_function(
            kernel32,
            "GetFileInformationByHandle",
            [wintypes.HANDLE, ctypes.POINTER(_ByHandleFileInformation)],
            wintypes.BOOL,
        )
        self._get_file_information_ex = _load_function(
            kernel32,
            "GetFileInformationByHandleEx",
            [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD],
            wintypes.BOOL,
        )
        self._set_file_information = _load_function(
            kernel32,
            "SetFileInformationByHandle",
            [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD],
            wintypes.BOOL,
        )
        self._close_handle = _load_function(
            kernel32,
            "CloseHandle",
            [wintypes.HANDLE],
            wintypes.BOOL,
        )
        self._nt_create_file = _load_function(
            ntdll,
            "NtCreateFile",
            [
                ctypes.POINTER(wintypes.HANDLE),
                wintypes.DWORD,
                ctypes.POINTER(_ObjectAttributes),
                ctypes.POINTER(_IoStatusBlock),
                ctypes.c_void_p,
                wintypes.ULONG,
                wintypes.ULONG,
                wintypes.ULONG,
                wintypes.ULONG,
                ctypes.c_void_p,
                wintypes.ULONG,
            ],
            wintypes.LONG,
        )
        self._nt_set_information_file = _load_function(
            ntdll,
            "NtSetInformationFile",
            [
                wintypes.HANDLE,
                ctypes.POINTER(_IoStatusBlock),
                ctypes.c_void_p,
                wintypes.ULONG,
                ctypes.c_int,
            ],
            wintypes.LONG,
        )
        self._nt_status_to_error = _load_function(
            ntdll,
            "RtlNtStatusToDosError",
            [wintypes.LONG],
            wintypes.ULONG,
        )
        self._owned: list[int] = []

    @property
    def owned_count(self) -> int:
        return len(self._owned)

    def __enter__(self) -> _WindowsCapabilityProbe:
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        while self._owned:
            self._close_owned(self._owned[-1])

    def open_root(self, path: Path) -> int:
        result = cast(
            int | None,
            self._create_file(
                str(path),
                _FILE_LIST_DIRECTORY | _FILE_READ_ATTRIBUTES | _SYNCHRONIZE,
                _SHARE_ALL,
                None,
                _OPEN_EXISTING,
                _FILE_FLAG_BACKUP_SEMANTICS | _FILE_FLAG_OPEN_REPARSE_POINT,
                None,
            ),
        )
        if result is None or result == _INVALID_HANDLE_VALUE:
            raise _NativeFailure("CreateFileW(root)", self._get_last_error())
        handle = self._adopt(result)
        try:
            self._reject_reparse(handle)
        except BaseException:
            self._close_owned(handle)
            raise
        return handle

    def open_directory(self, root: int, name: str) -> int:
        handle = self._open_relative(root, name, directory=True, delete_access=False)
        try:
            self._reject_reparse(handle)
        except BaseException:
            self._close_owned(handle)
            raise
        return handle

    def open_file(self, root: int, name: str, *, delete_access: bool) -> int:
        handle = self._open_relative(root, name, directory=False, delete_access=delete_access)
        try:
            self._reject_reparse(handle)
        except BaseException:
            self._close_owned(handle)
            raise
        return handle

    def identity(self, handle: int) -> tuple[int, bytes]:
        information = _FileIdInfo()
        self._require_win32(
            "GetFileInformationByHandleEx(FileIdInfo)",
            self._get_file_information_ex(
                wintypes.HANDLE(handle),
                _FILE_ID_INFO_CLASS,
                ctypes.byref(information),
                ctypes.sizeof(information),
            ),
        )
        return information.VolumeSerialNumber, bytes(information.FileId.Identifier)

    def link_count(self, handle: int) -> int:
        information = _ByHandleFileInformation()
        self._require_win32(
            "GetFileInformationByHandle",
            self._get_file_information(wintypes.HANDLE(handle), ctypes.byref(information)),
        )
        return information.NumberOfLinks

    def quarantine(self, handle: int, directory: int, name: str) -> None:
        _validate_component(name)
        encoded_name = name.encode("utf-16-le")
        file_name_offset = _FileRenameInformation.FileName.offset
        payload_size = ctypes.sizeof(_FileRenameInformation) + len(encoded_name)
        buffer = ctypes.create_string_buffer(payload_size)
        information = _FileRenameInformation.from_buffer(buffer)
        information.ReplaceIfExists = False
        information.RootDirectory = wintypes.HANDLE(directory)
        information.FileNameLength = len(encoded_name)
        ctypes.memmove(ctypes.addressof(buffer) + file_name_offset, encoded_name, len(encoded_name))
        io_status = _IoStatusBlock()
        status = cast(
            int,
            self._nt_set_information_file(
                wintypes.HANDLE(handle),
                ctypes.byref(io_status),
                buffer,
                payload_size,
                _FILE_RENAME_INFORMATION_CLASS,
            ),
        )
        self._require_ntstatus("NtSetInformationFile(FileRenameInformation)", status)

    def mark_delete(self, handle: int) -> None:
        information = _FileDispositionInfo(DeleteFile=True)
        self._require_win32(
            "SetFileInformationByHandle(FileDispositionInfo)",
            self._set_file_information(
                wintypes.HANDLE(handle),
                _FILE_DISPOSITION_INFO_CLASS,
                ctypes.byref(information),
                ctypes.sizeof(information),
            ),
        )

    def _open_relative(
        self,
        root: int,
        name: str,
        *,
        directory: bool,
        delete_access: bool,
    ) -> int:
        _validate_component(name)
        name_buffer = ctypes.create_unicode_buffer(name)
        encoded_length = len(name.encode("utf-16-le"))
        unicode_name = _UnicodeString(
            Length=encoded_length,
            MaximumLength=encoded_length + 2,
            Buffer=ctypes.cast(name_buffer, wintypes.LPWSTR),
        )
        attributes = _ObjectAttributes(
            Length=ctypes.sizeof(_ObjectAttributes),
            RootDirectory=wintypes.HANDLE(root),
            ObjectName=ctypes.pointer(unicode_name),
            Attributes=_OBJ_CASE_INSENSITIVE,
            SecurityDescriptor=None,
            SecurityQualityOfService=None,
        )
        output_handle = wintypes.HANDLE()
        io_status = _IoStatusBlock()
        desired_access = _FILE_READ_ATTRIBUTES | _SYNCHRONIZE
        if directory:
            desired_access |= _FILE_LIST_DIRECTORY
        if delete_access:
            desired_access |= _DELETE
        create_options = (
            (_FILE_DIRECTORY_FILE if directory else _FILE_NON_DIRECTORY_FILE)
            | _FILE_SYNCHRONOUS_IO_NONALERT
            | _FILE_OPEN_REPARSE_POINT
        )
        status = cast(
            int,
            self._nt_create_file(
                ctypes.byref(output_handle),
                desired_access,
                ctypes.byref(attributes),
                ctypes.byref(io_status),
                None,
                _FILE_ATTRIBUTE_NORMAL,
                _SHARE_ALL,
                _FILE_OPEN,
                create_options,
                None,
                0,
            ),
        )
        if status < 0 or output_handle.value is None:
            self._require_ntstatus("NtCreateFile(relative)", status)
            raise _NativeFailure("NtCreateFile(relative)", 0)
        return self._adopt(output_handle.value)

    def _reject_reparse(self, handle: int) -> None:
        information = _FileAttributeTagInfo()
        self._require_win32(
            "GetFileInformationByHandleEx(FileAttributeTagInfo)",
            self._get_file_information_ex(
                wintypes.HANDLE(handle),
                _FILE_ATTRIBUTE_TAG_INFO_CLASS,
                ctypes.byref(information),
                ctypes.sizeof(information),
            ),
        )
        if information.FileAttributes & _FILE_ATTRIBUTE_REPARSE_POINT:
            raise _UnsafeComponent(f"reparse component refused: tag={information.ReparseTag}")

    def _require_win32(self, operation: str, result: object) -> None:
        if not cast(bool, result):
            raise _NativeFailure(operation, self._get_last_error())

    def _require_ntstatus(self, operation: str, status: int) -> None:
        if status < 0:
            code = cast(int, self._nt_status_to_error(status))
            raise _NativeFailure(operation, code)

    def _adopt(self, handle: int) -> int:
        self._owned.append(handle)
        return handle

    def _close_owned(self, handle: int) -> None:
        self._require_win32("CloseHandle", self._close_handle(wintypes.HANDLE(handle)))
        self._owned.remove(handle)


def test_windows_handle_chain_quarantines_and_deletes_the_same_identity(tmp_path: Path) -> None:
    live_path = tmp_path / "live"
    quarantine_path = tmp_path / "quarantine"
    live_path.mkdir()
    quarantine_path.mkdir()
    source_path = live_path / "candidate.bin"
    quarantined_path = quarantine_path / "candidate.quarantined"
    source_path.write_bytes(b"m149-owned-candidate")

    probe = _WindowsCapabilityProbe()
    with probe:
        root = probe.open_root(tmp_path)
        live = probe.open_directory(root, "live")
        quarantine = probe.open_directory(root, "quarantine")
        candidate = probe.open_file(live, "candidate.bin", delete_access=True)
        before = probe.identity(candidate)

        probe.quarantine(candidate, quarantine, "candidate.quarantined")

        assert probe.identity(candidate) == before
        assert not source_path.exists()
        assert quarantined_path.is_file()
        reopened = probe.open_file(quarantine, "candidate.quarantined", delete_access=False)
        assert probe.identity(reopened) == before
        probe.mark_delete(candidate)

    assert probe.owned_count == 0
    assert not quarantined_path.exists()


def test_windows_handle_chain_detects_hard_link_aliases(tmp_path: Path) -> None:
    live_path = tmp_path / "live"
    live_path.mkdir()
    candidate_path = live_path / "candidate.bin"
    alias_path = live_path / "alias.bin"
    candidate_path.write_bytes(b"same-object")
    os.link(candidate_path, alias_path)

    with _WindowsCapabilityProbe() as probe:
        root = probe.open_root(tmp_path)
        live = probe.open_directory(root, "live")
        candidate = probe.open_file(live, "candidate.bin", delete_access=False)
        alias = probe.open_file(live, "alias.bin", delete_access=False)

        assert probe.identity(candidate) == probe.identity(alias)
        assert probe.link_count(candidate) >= 2
        assert probe.link_count(alias) >= 2


def test_windows_handle_chain_refuses_a_reparse_component(tmp_path: Path) -> None:
    live_path = tmp_path / "live"
    target_path = tmp_path / "target"
    live_path.mkdir()
    target_path.mkdir()
    link_path = live_path / "linked"
    try:
        link_path.symlink_to(target_path, target_is_directory=True)
    except OSError as error:
        if error.winerror == 1314:
            pytest.skip("Windows symlink creation privilege is unavailable")
        raise

    with _WindowsCapabilityProbe() as probe:
        root = probe.open_root(tmp_path)
        live = probe.open_directory(root, "live")

        with pytest.raises(_UnsafeComponent, match="reparse component refused"):
            probe.open_directory(live, "linked")

        assert probe.owned_count == 2


def test_windows_handle_chain_does_not_replace_a_quarantine_collision(tmp_path: Path) -> None:
    live_path = tmp_path / "live"
    quarantine_path = tmp_path / "quarantine"
    live_path.mkdir()
    quarantine_path.mkdir()
    source_path = live_path / "candidate.bin"
    collision_path = quarantine_path / "occupied.bin"
    source_path.write_bytes(b"candidate")
    collision_path.write_bytes(b"existing")

    with _WindowsCapabilityProbe() as probe:
        root = probe.open_root(tmp_path)
        live = probe.open_directory(root, "live")
        quarantine = probe.open_directory(root, "quarantine")
        candidate = probe.open_file(live, "candidate.bin", delete_access=True)

        with pytest.raises(
            _NativeFailure,
            match=r"NtSetInformationFile\(FileRenameInformation\) failed",
        ):
            probe.quarantine(candidate, quarantine, "occupied.bin")

    assert source_path.read_bytes() == b"candidate"
    assert collision_path.read_bytes() == b"existing"


@pytest.mark.parametrize("name", ["", ".", "..", "nested/name", "nested\\name", "x\0y"])
def test_windows_handle_chain_rejects_non_component_names(tmp_path: Path, name: str) -> None:
    with _WindowsCapabilityProbe() as probe:
        root = probe.open_root(tmp_path)

        with pytest.raises(ValueError, match="single non-special relative component"):
            probe.open_file(root, name, delete_access=False)

        assert probe.owned_count == 1
