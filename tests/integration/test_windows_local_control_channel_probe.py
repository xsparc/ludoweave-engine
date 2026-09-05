"""Test-only Windows local named-pipe control-channel probe."""

from __future__ import annotations

import ctypes
import json
import secrets
import string
import subprocess
import sys
from collections.abc import Callable, Mapping
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Protocol, cast

import pytest

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M212 probes a native Windows local named-pipe control channel",
)

_ROOT = Path(__file__).parents[2]
_PARTICIPANT = _ROOT / "tests/fixtures/windows_local_control_channel_participant.py"
_DIRECT_PYTHON = Path(sys.base_prefix) / "pythonw.exe"
_SCHEMA = "ludoweave.test.windows-local-control-channel/1"
_PIPE_PREFIX = r"\\.\pipe\ludoweave-m212-"
_MAX_MESSAGE_BYTES = 1_024

_CREATE_SUSPENDED = 0x00000004
_CREATE_NO_WINDOW = 0x08000000
_JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
_JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION = 1
_JOB_OBJECT_BASIC_PROCESS_ID_LIST = 3
_JOB_OBJECT_EXTENDED_LIMIT_INFORMATION = 9

_PIPE_ACCESS_DUPLEX = 0x00000003
_FILE_FLAG_FIRST_PIPE_INSTANCE = 0x00080000
_FILE_FLAG_OVERLAPPED = 0x40000000
_PIPE_TYPE_MESSAGE = 0x00000004
_PIPE_READMODE_MESSAGE = 0x00000002
_PIPE_WAIT = 0x00000000
_PIPE_REJECT_REMOTE_CLIENTS = 0x00000008
_CONTROL_PIPE_ACCESS = 0x0012019F

_TOKEN_QUERY = 0x0008
_TOKEN_LOGON_SID = 28
_SDDL_REVISION_1 = 1
_SE_KERNEL_OBJECT = 6
_DACL_SECURITY_INFORMATION = 0x00000004
_SE_DACL_PROTECTED = 0x1000
_ACCESS_ALLOWED_ACE_TYPE = 0

_PROCESS_QUERY_LIMITED_INFORMATION = 0x00001000
_SYNCHRONIZE = 0x00100000
_WAIT_OBJECT_0 = 0x00000000
_WAIT_TIMEOUT = 0x00000102
_DWORD_FAILURE = 0xFFFFFFFF
_STILL_ACTIVE = 259
_ERROR_ACCESS_DENIED = 5
_ERROR_INSUFFICIENT_BUFFER = 122
_ERROR_OPERATION_ABORTED = 995
_ERROR_IO_PENDING = 997
_ERROR_PIPE_CONNECTED = 535
_ERROR_NOT_FOUND = 1168
_TERMINATION_EXIT_CODE = 0x4C57
_TIMEOUT_MILLISECONDS = 5_000

_EXIT_PROTOCOL = 11
_EXIT_CHALLENGE = 12
_EXIT_DISCONNECT = 13
_INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value


class _NativeFunction(Protocol):
    argtypes: list[object] | None
    restype: object

    def __call__(self, *arguments: object) -> object: ...


class _SecurityAttributes(ctypes.Structure):
    _fields_ = [
        ("nLength", wintypes.DWORD),
        ("lpSecurityDescriptor", ctypes.c_void_p),
        ("bInheritHandle", wintypes.BOOL),
    ]


class _StartupInfoW(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPWSTR),
        ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", ctypes.POINTER(wintypes.BYTE)),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    ]


class _ProcessInformation(ctypes.Structure):
    _fields_ = [
        ("hProcess", wintypes.HANDLE),
        ("hThread", wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    ]


class _IoCounters(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_ulonglong),
        ("WriteOperationCount", ctypes.c_ulonglong),
        ("OtherOperationCount", ctypes.c_ulonglong),
        ("ReadTransferCount", ctypes.c_ulonglong),
        ("WriteTransferCount", ctypes.c_ulonglong),
        ("OtherTransferCount", ctypes.c_ulonglong),
    ]


class _JobBasicLimitInformation(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_longlong),
        ("PerJobUserTimeLimit", ctypes.c_longlong),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    ]


class _JobExtendedLimitInformation(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", _JobBasicLimitInformation),
        ("IoInfo", _IoCounters),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


class _JobBasicAccountingInformation(ctypes.Structure):
    _fields_ = [
        ("TotalUserTime", ctypes.c_longlong),
        ("TotalKernelTime", ctypes.c_longlong),
        ("ThisPeriodTotalUserTime", ctypes.c_longlong),
        ("ThisPeriodTotalKernelTime", ctypes.c_longlong),
        ("TotalPageFaultCount", wintypes.DWORD),
        ("TotalProcesses", wintypes.DWORD),
        ("ActiveProcesses", wintypes.DWORD),
        ("TotalTerminatedProcesses", wintypes.DWORD),
    ]


class _JobProcessIdList(ctypes.Structure):
    _fields_ = [
        ("NumberOfAssignedProcesses", wintypes.DWORD),
        ("NumberOfProcessIdsInList", wintypes.DWORD),
        ("ProcessIdList", ctypes.c_size_t * 4),
    ]


class _Overlapped(ctypes.Structure):
    _fields_ = [
        ("Internal", ctypes.c_size_t),
        ("InternalHigh", ctypes.c_size_t),
        ("Offset", wintypes.DWORD),
        ("OffsetHigh", wintypes.DWORD),
        ("hEvent", wintypes.HANDLE),
    ]


class _SidAndAttributes(ctypes.Structure):
    _fields_ = [("Sid", ctypes.c_void_p), ("Attributes", wintypes.DWORD)]


class _TokenGroupsOne(ctypes.Structure):
    _fields_ = [("GroupCount", wintypes.DWORD), ("Groups", _SidAndAttributes * 1)]


class _Acl(ctypes.Structure):
    _fields_ = [
        ("AclRevision", wintypes.BYTE),
        ("Sbz1", wintypes.BYTE),
        ("AclSize", wintypes.WORD),
        ("AceCount", wintypes.WORD),
        ("Sbz2", wintypes.WORD),
    ]


class _AceHeader(ctypes.Structure):
    _fields_ = [
        ("AceType", wintypes.BYTE),
        ("AceFlags", wintypes.BYTE),
        ("AceSize", wintypes.WORD),
    ]


class _AccessAllowedAce(ctypes.Structure):
    _fields_ = [
        ("Header", _AceHeader),
        ("Mask", wintypes.DWORD),
        ("SidStart", wintypes.DWORD),
    ]


class _NativeFailure(RuntimeError):
    def __init__(self, operation: str, code: int) -> None:
        self.operation = operation
        self.code = code
        super().__init__(f"{operation} failed with native code {code}")


@dataclass(frozen=True, slots=True)
class _PendingConnect:
    event: int
    overlapped: _Overlapped
    pending: bool


@dataclass(frozen=True, slots=True)
class _SuspendedProcess:
    process: int
    thread: int
    pid: int


@dataclass(frozen=True, slots=True)
class _Session:
    job: int
    pipe: int
    process: int
    pid: int
    challenge: str


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
        raise RuntimeError("control message size was invalid") from None
    try:
        parsed: object = json.loads(message)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RuntimeError("control message was not canonical JSON") from None
    if not isinstance(parsed, dict):
        raise RuntimeError("control message was not a JSON object") from None
    document = cast(dict[str, object], parsed)
    if _encode(document) != message:
        raise RuntimeError("control message was not canonical JSON") from None
    if set(document) != {"challenge", "kind", "schema", "sequence"}:
        raise RuntimeError("control message shape was invalid") from None
    if document["schema"] != _SCHEMA:
        raise RuntimeError("control message schema was invalid") from None
    challenge = document["challenge"]
    if (
        type(challenge) is not str
        or len(challenge) != 64
        or any(character not in string.hexdigits[:16] for character in challenge)
    ):
        raise RuntimeError("control message challenge was invalid") from None
    if type(document["kind"]) is not str or type(document["sequence"]) is not int:
        raise RuntimeError("control message fields were invalid") from None
    return document


class _WindowsControlProbe:
    def __init__(self) -> None:
        win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
        self._get_last_error = cast(Callable[[], int], vars(ctypes)["get_last_error"])
        kernel32 = win_dll("kernel32", use_last_error=True)
        advapi32 = win_dll("advapi32", use_last_error=True)

        self._create_job = _load_function(
            kernel32, "CreateJobObjectW", [ctypes.c_void_p, wintypes.LPCWSTR], wintypes.HANDLE
        )
        self._set_job_information = _load_function(
            kernel32,
            "SetInformationJobObject",
            [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD],
            wintypes.BOOL,
        )
        self._query_job_information = _load_function(
            kernel32,
            "QueryInformationJobObject",
            [
                wintypes.HANDLE,
                ctypes.c_int,
                ctypes.c_void_p,
                wintypes.DWORD,
                ctypes.POINTER(wintypes.DWORD),
            ],
            wintypes.BOOL,
        )
        self._assign_process = _load_function(
            kernel32,
            "AssignProcessToJobObject",
            [wintypes.HANDLE, wintypes.HANDLE],
            wintypes.BOOL,
        )
        self._is_process_in_job = _load_function(
            kernel32,
            "IsProcessInJob",
            [wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)],
            wintypes.BOOL,
        )
        self._terminate_job = _load_function(
            kernel32,
            "TerminateJobObject",
            [wintypes.HANDLE, wintypes.UINT],
            wintypes.BOOL,
        )
        self._create_process = _load_function(
            kernel32,
            "CreateProcessW",
            [
                wintypes.LPCWSTR,
                wintypes.LPWSTR,
                ctypes.c_void_p,
                ctypes.c_void_p,
                wintypes.BOOL,
                wintypes.DWORD,
                ctypes.c_void_p,
                wintypes.LPCWSTR,
                ctypes.POINTER(_StartupInfoW),
                ctypes.POINTER(_ProcessInformation),
            ],
            wintypes.BOOL,
        )
        self._resume_thread = _load_function(
            kernel32, "ResumeThread", [wintypes.HANDLE], wintypes.DWORD
        )
        self._get_process_id = _load_function(
            kernel32, "GetProcessId", [wintypes.HANDLE], wintypes.DWORD
        )
        self._get_exit_code = _load_function(
            kernel32,
            "GetExitCodeProcess",
            [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)],
            wintypes.BOOL,
        )
        self._wait = _load_function(
            kernel32,
            "WaitForSingleObject",
            [wintypes.HANDLE, wintypes.DWORD],
            wintypes.DWORD,
        )
        self._terminate_process = _load_function(
            kernel32,
            "TerminateProcess",
            [wintypes.HANDLE, wintypes.UINT],
            wintypes.BOOL,
        )
        self._create_pipe = _load_function(
            kernel32,
            "CreateNamedPipeW",
            [
                wintypes.LPCWSTR,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.DWORD,
                ctypes.POINTER(_SecurityAttributes),
            ],
            wintypes.HANDLE,
        )
        self._connect_pipe = _load_function(
            kernel32,
            "ConnectNamedPipe",
            [wintypes.HANDLE, ctypes.POINTER(_Overlapped)],
            wintypes.BOOL,
        )
        self._disconnect_pipe = _load_function(
            kernel32, "DisconnectNamedPipe", [wintypes.HANDLE], wintypes.BOOL
        )
        self._get_pipe_client_pid = _load_function(
            kernel32,
            "GetNamedPipeClientProcessId",
            [wintypes.HANDLE, ctypes.POINTER(wintypes.ULONG)],
            wintypes.BOOL,
        )
        self._peek_pipe = _load_function(
            kernel32,
            "PeekNamedPipe",
            [
                wintypes.HANDLE,
                ctypes.c_void_p,
                wintypes.DWORD,
                ctypes.POINTER(wintypes.DWORD),
                ctypes.POINTER(wintypes.DWORD),
                ctypes.POINTER(wintypes.DWORD),
            ],
            wintypes.BOOL,
        )
        self._read_file = _load_function(
            kernel32,
            "ReadFile",
            [
                wintypes.HANDLE,
                ctypes.c_void_p,
                wintypes.DWORD,
                ctypes.POINTER(wintypes.DWORD),
                ctypes.POINTER(_Overlapped),
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
                ctypes.POINTER(_Overlapped),
            ],
            wintypes.BOOL,
        )
        self._create_event = _load_function(
            kernel32,
            "CreateEventW",
            [ctypes.c_void_p, wintypes.BOOL, wintypes.BOOL, wintypes.LPCWSTR],
            wintypes.HANDLE,
        )
        self._get_overlapped_result = _load_function(
            kernel32,
            "GetOverlappedResult",
            [
                wintypes.HANDLE,
                ctypes.POINTER(_Overlapped),
                ctypes.POINTER(wintypes.DWORD),
                wintypes.BOOL,
            ],
            wintypes.BOOL,
        )
        self._cancel_io = _load_function(
            kernel32,
            "CancelIoEx",
            [wintypes.HANDLE, ctypes.POINTER(_Overlapped)],
            wintypes.BOOL,
        )
        self._get_current_process = _load_function(
            kernel32, "GetCurrentProcess", [], wintypes.HANDLE
        )
        self._local_free = _load_function(kernel32, "LocalFree", [ctypes.c_void_p], ctypes.c_void_p)
        self._close_handle = _load_function(
            kernel32, "CloseHandle", [wintypes.HANDLE], wintypes.BOOL
        )

        self._open_process_token = _load_function(
            advapi32,
            "OpenProcessToken",
            [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)],
            wintypes.BOOL,
        )
        self._get_token_information = _load_function(
            advapi32,
            "GetTokenInformation",
            [
                wintypes.HANDLE,
                ctypes.c_int,
                ctypes.c_void_p,
                wintypes.DWORD,
                ctypes.POINTER(wintypes.DWORD),
            ],
            wintypes.BOOL,
        )
        self._convert_sid_to_string = _load_function(
            advapi32,
            "ConvertSidToStringSidW",
            [ctypes.c_void_p, ctypes.POINTER(wintypes.LPWSTR)],
            wintypes.BOOL,
        )
        self._convert_sddl = _load_function(
            advapi32,
            "ConvertStringSecurityDescriptorToSecurityDescriptorW",
            [wintypes.LPCWSTR, wintypes.DWORD, ctypes.POINTER(ctypes.c_void_p), ctypes.c_void_p],
            wintypes.BOOL,
        )
        self._get_security_info = _load_function(
            advapi32,
            "GetSecurityInfo",
            [
                wintypes.HANDLE,
                ctypes.c_int,
                wintypes.DWORD,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_void_p),
                ctypes.c_void_p,
                ctypes.POINTER(ctypes.c_void_p),
            ],
            wintypes.DWORD,
        )
        self._get_security_descriptor_dacl = _load_function(
            advapi32,
            "GetSecurityDescriptorDacl",
            [
                ctypes.c_void_p,
                ctypes.POINTER(wintypes.BOOL),
                ctypes.POINTER(ctypes.c_void_p),
                ctypes.POINTER(wintypes.BOOL),
            ],
            wintypes.BOOL,
        )
        self._get_security_descriptor_control = _load_function(
            advapi32,
            "GetSecurityDescriptorControl",
            [ctypes.c_void_p, ctypes.POINTER(wintypes.WORD), ctypes.POINTER(wintypes.DWORD)],
            wintypes.BOOL,
        )
        self._get_ace = _load_function(
            advapi32,
            "GetAce",
            [ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(ctypes.c_void_p)],
            wintypes.BOOL,
        )
        self._equal_sid = _load_function(
            advapi32, "EqualSid", [ctypes.c_void_p, ctypes.c_void_p], wintypes.BOOL
        )
        self._owned: set[int] = set()

    @property
    def owned_count(self) -> int:
        return len(self._owned)

    def __enter__(self) -> _WindowsControlProbe:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def _failure(self, operation: str) -> _NativeFailure:
        return _NativeFailure(operation, self._get_last_error())

    def _own(self, handle: int) -> int:
        self._owned.add(handle)
        return handle

    def close_handle(self, handle: int) -> None:
        if handle not in self._owned:
            return
        if not cast(bool, self._close_handle(wintypes.HANDLE(handle))):
            raise self._failure("CloseHandle")
        self._owned.remove(handle)

    def close(self) -> None:
        for handle in tuple(self._owned):
            self.close_handle(handle)

    def create_job(self) -> int:
        raw = cast(wintypes.HANDLE, self._create_job(None, None))
        job = self._own(_handle_value(raw, "CreateJobObjectW"))
        limits = _JobExtendedLimitInformation()
        limits.BasicLimitInformation.LimitFlags = _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not cast(
            bool,
            self._set_job_information(
                wintypes.HANDLE(job),
                _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION,
                ctypes.byref(limits),
                ctypes.sizeof(limits),
            ),
        ):
            raise self._failure("SetInformationJobObject")
        return job

    def accounting(self, job: int) -> tuple[int, int]:
        information = _JobBasicAccountingInformation()
        returned = wintypes.DWORD()
        if not cast(
            bool,
            self._query_job_information(
                wintypes.HANDLE(job),
                _JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION,
                ctypes.byref(information),
                ctypes.sizeof(information),
                ctypes.byref(returned),
            ),
        ):
            raise self._failure("QueryInformationJobObject")
        if returned.value != ctypes.sizeof(information):
            raise RuntimeError("Job Object accounting size was invalid") from None
        return information.TotalProcesses, information.ActiveProcesses

    def process_ids(self, job: int) -> tuple[int, ...]:
        information = _JobProcessIdList()
        returned = wintypes.DWORD()
        if not cast(
            bool,
            self._query_job_information(
                wintypes.HANDLE(job),
                _JOB_OBJECT_BASIC_PROCESS_ID_LIST,
                ctypes.byref(information),
                ctypes.sizeof(information),
                ctypes.byref(returned),
            ),
        ):
            raise self._failure("QueryInformationJobObject")
        count = information.NumberOfProcessIdsInList
        if information.NumberOfAssignedProcesses != count or count > len(information.ProcessIdList):
            raise RuntimeError("Job Object process membership exceeded its bound") from None
        return tuple(information.ProcessIdList[index] for index in range(count))

    def _process_is_in_job(self, process: int, job: int) -> bool:
        result = wintypes.BOOL()
        if not cast(
            bool,
            self._is_process_in_job(
                wintypes.HANDLE(process), wintypes.HANDLE(job), ctypes.byref(result)
            ),
        ):
            raise self._failure("IsProcessInJob")
        return bool(result.value)

    def _current_logon_sid(
        self,
    ) -> tuple[ctypes.Array[ctypes.c_char], int, str]:
        token = wintypes.HANDLE()
        current_process = cast(wintypes.HANDLE, self._get_current_process())
        if not cast(
            bool,
            self._open_process_token(current_process, _TOKEN_QUERY, ctypes.byref(token)),
        ):
            raise self._failure("OpenProcessToken")
        token_value = self._own(_handle_value(token, "OpenProcessToken"))
        try:
            required = wintypes.DWORD()
            self._get_token_information(
                wintypes.HANDLE(token_value),
                _TOKEN_LOGON_SID,
                None,
                0,
                ctypes.byref(required),
            )
            if self._get_last_error() != _ERROR_INSUFFICIENT_BUFFER or required.value == 0:
                raise self._failure("GetTokenInformation")
            buffer = ctypes.create_string_buffer(required.value)
            if not cast(
                bool,
                self._get_token_information(
                    wintypes.HANDLE(token_value),
                    _TOKEN_LOGON_SID,
                    buffer,
                    len(buffer),
                    ctypes.byref(required),
                ),
            ):
                raise self._failure("GetTokenInformation")
            groups = ctypes.cast(buffer, ctypes.POINTER(_TokenGroupsOne)).contents
            sid = groups.Groups[0].Sid
            if groups.GroupCount != 1 or sid is None or sid == 0:
                raise RuntimeError("current token had no single logon SID") from None
            string_pointer = wintypes.LPWSTR()
            if not cast(
                bool,
                self._convert_sid_to_string(ctypes.c_void_p(sid), ctypes.byref(string_pointer)),
            ):
                raise self._failure("ConvertSidToStringSidW")
            try:
                sid_string = string_pointer.value
                if sid_string is None:
                    raise RuntimeError("logon SID string was unavailable") from None
            finally:
                self._local_free(ctypes.cast(string_pointer, ctypes.c_void_p))
            return buffer, sid, sid_string
        finally:
            self.close_handle(token_value)

    def _verify_pipe_dacl(self, pipe: int, logon_sid: int) -> None:
        dacl = ctypes.c_void_p()
        descriptor = ctypes.c_void_p()
        error = cast(
            int,
            self._get_security_info(
                wintypes.HANDLE(pipe),
                _SE_KERNEL_OBJECT,
                _DACL_SECURITY_INFORMATION,
                None,
                None,
                ctypes.byref(dacl),
                None,
                ctypes.byref(descriptor),
            ),
        )
        if error != 0:
            raise _NativeFailure("GetSecurityInfo", error)
        if descriptor.value is None:
            raise RuntimeError("named pipe security descriptor was unavailable") from None
        try:
            present = wintypes.BOOL()
            defaulted = wintypes.BOOL()
            checked_dacl = ctypes.c_void_p()
            if not cast(
                bool,
                self._get_security_descriptor_dacl(
                    descriptor,
                    ctypes.byref(present),
                    ctypes.byref(checked_dacl),
                    ctypes.byref(defaulted),
                ),
            ):
                raise self._failure("GetSecurityDescriptorDacl")
            if not present.value or defaulted.value or checked_dacl.value != dacl.value:
                raise RuntimeError("named pipe DACL was not explicit") from None
            control = wintypes.WORD()
            revision = wintypes.DWORD()
            if not cast(
                bool,
                self._get_security_descriptor_control(
                    descriptor, ctypes.byref(control), ctypes.byref(revision)
                ),
            ):
                raise self._failure("GetSecurityDescriptorControl")
            if not control.value & _SE_DACL_PROTECTED:
                raise RuntimeError("named pipe DACL was not protected") from None
            acl = ctypes.cast(dacl, ctypes.POINTER(_Acl)).contents
            if acl.AceCount != 1:
                raise RuntimeError("named pipe DACL contained an unexpected ACE") from None
            ace_pointer = ctypes.c_void_p()
            if not cast(bool, self._get_ace(dacl, 0, ctypes.byref(ace_pointer))):
                raise self._failure("GetAce")
            if ace_pointer.value is None:
                raise RuntimeError("named pipe DACL ACE was unavailable") from None
            ace = ctypes.cast(ace_pointer, ctypes.POINTER(_AccessAllowedAce)).contents
            sid_pointer = ace_pointer.value + _AccessAllowedAce.SidStart.offset
            if (
                ace.Header.AceType != _ACCESS_ALLOWED_ACE_TYPE
                or ace.Mask != _CONTROL_PIPE_ACCESS
                or not cast(
                    bool,
                    self._equal_sid(ctypes.c_void_p(sid_pointer), ctypes.c_void_p(logon_sid)),
                )
            ):
                raise RuntimeError("named pipe DACL did not bind the logon SID") from None
        finally:
            self._local_free(descriptor)

    def create_control_pipe(self) -> tuple[int, str]:
        sid_buffer, logon_sid, sid_string = self._current_logon_sid()
        descriptor = ctypes.c_void_p()
        sddl = f"D:P(A;;0x{_CONTROL_PIPE_ACCESS:08x};;;{sid_string})"
        if not cast(
            bool,
            self._convert_sddl(
                sddl,
                _SDDL_REVISION_1,
                ctypes.byref(descriptor),
                None,
            ),
        ):
            raise self._failure("ConvertStringSecurityDescriptorToSecurityDescriptorW")
        if descriptor.value is None:
            raise RuntimeError("named pipe security descriptor was unavailable") from None
        pipe_name = _PIPE_PREFIX + secrets.token_hex(16)
        security = _SecurityAttributes(
            nLength=ctypes.sizeof(_SecurityAttributes),
            lpSecurityDescriptor=descriptor.value,
            bInheritHandle=False,
        )
        try:
            raw = cast(
                wintypes.HANDLE,
                self._create_pipe(
                    pipe_name,
                    _PIPE_ACCESS_DUPLEX | _FILE_FLAG_FIRST_PIPE_INSTANCE | _FILE_FLAG_OVERLAPPED,
                    _PIPE_TYPE_MESSAGE
                    | _PIPE_READMODE_MESSAGE
                    | _PIPE_WAIT
                    | _PIPE_REJECT_REMOTE_CLIENTS,
                    1,
                    _MAX_MESSAGE_BYTES,
                    _MAX_MESSAGE_BYTES,
                    _TIMEOUT_MILLISECONDS,
                    ctypes.byref(security),
                ),
            )
            pipe = self._own(_handle_value(raw, "CreateNamedPipeW"))
        finally:
            self._local_free(descriptor)
        self._verify_pipe_dacl(pipe, logon_sid)
        del sid_buffer
        return pipe, pipe_name

    def assert_first_instance_exclusive(self, pipe_name: str) -> None:
        raw = cast(
            wintypes.HANDLE,
            self._create_pipe(
                pipe_name,
                _PIPE_ACCESS_DUPLEX | _FILE_FLAG_FIRST_PIPE_INSTANCE | _FILE_FLAG_OVERLAPPED,
                _PIPE_TYPE_MESSAGE
                | _PIPE_READMODE_MESSAGE
                | _PIPE_WAIT
                | _PIPE_REJECT_REMOTE_CLIENTS,
                1,
                _MAX_MESSAGE_BYTES,
                _MAX_MESSAGE_BYTES,
                _TIMEOUT_MILLISECONDS,
                None,
            ),
        )
        value = raw if isinstance(raw, int) else raw.value
        if value is not None and value != 0 and value != _INVALID_HANDLE_VALUE:
            unexpected = self._own(value)
            self.close_handle(unexpected)
            raise RuntimeError("a second named-pipe server instance was admitted") from None
        if self._get_last_error() != _ERROR_ACCESS_DENIED:
            raise self._failure("CreateNamedPipeW")

    def launch_suspended(self, job: int, pipe_name: str) -> _SuspendedProcess:
        if not _DIRECT_PYTHON.is_file():
            raise RuntimeError("direct Windows Python executable is unavailable") from None
        command_line = ctypes.create_unicode_buffer(
            subprocess.list2cmdline((str(_DIRECT_PYTHON), "-I", "-B", str(_PARTICIPANT), pipe_name))
        )
        startup = _StartupInfoW()
        startup.cb = ctypes.sizeof(startup)
        information = _ProcessInformation()
        created = cast(
            bool,
            self._create_process(
                str(_DIRECT_PYTHON),
                command_line,
                None,
                None,
                False,
                _CREATE_SUSPENDED | _CREATE_NO_WINDOW,
                None,
                str(_ROOT),
                ctypes.byref(startup),
                ctypes.byref(information),
            ),
        )
        if not created:
            raise self._failure("CreateProcessW")
        process = self._own(_handle_value(information.hProcess, "CreateProcessW"))
        thread = self._own(_handle_value(information.hThread, "CreateProcessW"))
        assigned = cast(
            bool,
            self._assign_process(wintypes.HANDLE(job), wintypes.HANDLE(process)),
        )
        if not assigned:
            code = self._get_last_error()
            self._terminate_process(wintypes.HANDLE(process), _TERMINATION_EXIT_CODE)
            self._wait(wintypes.HANDLE(process), _TIMEOUT_MILLISECONDS)
            self.close_handle(thread)
            self.close_handle(process)
            raise _NativeFailure("AssignProcessToJobObject", code)
        if not self._process_is_in_job(process, job):
            raise RuntimeError("control participant escaped the private Job Object") from None
        if self.accounting(job) != (1, 1) or self.process_ids(job) != (information.dwProcessId,):
            raise RuntimeError("control Job Object membership was not exact") from None
        if cast(int, self._wait(wintypes.HANDLE(process), 0)) != _WAIT_TIMEOUT:
            raise RuntimeError("suspended control participant was not live") from None
        return _SuspendedProcess(process, thread, information.dwProcessId)

    def begin_connect(self, pipe: int) -> _PendingConnect:
        raw_event = cast(wintypes.HANDLE, self._create_event(None, True, False, None))
        event = self._own(_handle_value(raw_event, "CreateEventW"))
        overlapped = _Overlapped()
        overlapped.hEvent = wintypes.HANDLE(event)
        connected = cast(
            bool,
            self._connect_pipe(wintypes.HANDLE(pipe), ctypes.byref(overlapped)),
        )
        if connected:
            return _PendingConnect(event, overlapped, False)
        code = self._get_last_error()
        if code == _ERROR_PIPE_CONNECTED:
            return _PendingConnect(event, overlapped, False)
        if code != _ERROR_IO_PENDING:
            self.close_handle(event)
            raise _NativeFailure("ConnectNamedPipe", code)
        return _PendingConnect(event, overlapped, True)

    def resume(self, suspended: _SuspendedProcess) -> None:
        previous = cast(int, self._resume_thread(wintypes.HANDLE(suspended.thread)))
        if previous == _DWORD_FAILURE:
            raise self._failure("ResumeThread")
        if previous != 1:
            raise RuntimeError("control participant suspend count was invalid") from None
        self.close_handle(suspended.thread)

    def complete_connect(self, pipe: int, pending: _PendingConnect) -> None:
        try:
            if pending.pending:
                outcome = cast(
                    int,
                    self._wait(wintypes.HANDLE(pending.event), _TIMEOUT_MILLISECONDS),
                )
                if outcome != _WAIT_OBJECT_0:
                    wait_error = self._get_last_error() if outcome == _DWORD_FAILURE else None
                    self.cancel_pending(pipe, pending)
                    if wait_error is not None:
                        raise _NativeFailure("WaitForSingleObject", wait_error)
                    raise RuntimeError("control-channel connection timed out") from None
                transferred = wintypes.DWORD()
                if not cast(
                    bool,
                    self._get_overlapped_result(
                        wintypes.HANDLE(pipe),
                        ctypes.byref(pending.overlapped),
                        ctypes.byref(transferred),
                        False,
                    ),
                ):
                    raise self._failure("GetOverlappedResult")
        finally:
            self.close_handle(pending.event)

    def cancel_pending(self, pipe: int, pending: _PendingConnect) -> None:
        cancelled = cast(
            bool,
            self._cancel_io(wintypes.HANDLE(pipe), ctypes.byref(pending.overlapped)),
        )
        if not cancelled and self._get_last_error() != _ERROR_NOT_FOUND:
            raise self._failure("CancelIoEx")
        self._await_cancelled_io(pipe, pending.event, pending.overlapped)

    def _await_cancelled_io(self, pipe: int, event: int, overlapped: _Overlapped) -> None:
        outcome = cast(int, self._wait(wintypes.HANDLE(event), _TIMEOUT_MILLISECONDS))
        if outcome != _WAIT_OBJECT_0:
            raise RuntimeError("cancelled control-channel I/O did not settle") from None
        transferred = wintypes.DWORD()
        completed = cast(
            bool,
            self._get_overlapped_result(
                wintypes.HANDLE(pipe),
                ctypes.byref(overlapped),
                ctypes.byref(transferred),
                False,
            ),
        )
        if not completed and self._get_last_error() != _ERROR_OPERATION_ABORTED:
            raise self._failure("GetOverlappedResult")

    def verify_client_identity(self, pipe: int, suspended: _SuspendedProcess) -> None:
        client_pid = wintypes.ULONG()
        if not cast(
            bool,
            self._get_pipe_client_pid(wintypes.HANDLE(pipe), ctypes.byref(client_pid)),
        ):
            raise self._failure("GetNamedPipeClientProcessId")
        retained_pid = cast(int, self._get_process_id(wintypes.HANDLE(suspended.process)))
        if client_pid.value != suspended.pid or retained_pid != suspended.pid:
            raise RuntimeError("control-channel client identity was inconsistent") from None

    def owns(self, handle: int) -> bool:
        return handle in self._owned

    def assert_no_participant_message(self, pipe: int) -> None:
        available = wintypes.DWORD()
        if not cast(
            bool,
            self._peek_pipe(
                wintypes.HANDLE(pipe),
                None,
                0,
                None,
                ctypes.byref(available),
                None,
            ),
        ):
            raise self._failure("PeekNamedPipe")
        if available.value != 0:
            raise RuntimeError("participant advanced before the challenge") from None

    def _event(self) -> tuple[int, _Overlapped]:
        raw = cast(wintypes.HANDLE, self._create_event(None, True, False, None))
        event = self._own(_handle_value(raw, "CreateEventW"))
        overlapped = _Overlapped()
        overlapped.hEvent = wintypes.HANDLE(event)
        return event, overlapped

    def _complete_io(
        self,
        pipe: int,
        event: int,
        overlapped: _Overlapped,
        immediate: bool,
        operation: str,
        immediate_bytes: int,
    ) -> int:
        try:
            if immediate:
                return immediate_bytes
            code = self._get_last_error()
            if code != _ERROR_IO_PENDING:
                raise _NativeFailure(operation, code)
            outcome = cast(int, self._wait(wintypes.HANDLE(event), _TIMEOUT_MILLISECONDS))
            if outcome != _WAIT_OBJECT_0:
                wait_error = self._get_last_error() if outcome == _DWORD_FAILURE else None
                cancelled = cast(
                    bool,
                    self._cancel_io(wintypes.HANDLE(pipe), ctypes.byref(overlapped)),
                )
                if not cancelled and self._get_last_error() != _ERROR_NOT_FOUND:
                    raise self._failure("CancelIoEx")
                self._await_cancelled_io(pipe, event, overlapped)
                if wait_error is not None:
                    raise _NativeFailure("WaitForSingleObject", wait_error)
                raise RuntimeError(f"{operation} timed out") from None
            transferred = wintypes.DWORD()
            if not cast(
                bool,
                self._get_overlapped_result(
                    wintypes.HANDLE(pipe),
                    ctypes.byref(overlapped),
                    ctypes.byref(transferred),
                    False,
                ),
            ):
                raise self._failure("GetOverlappedResult")
            return transferred.value
        finally:
            self.close_handle(event)

    def write_document(self, pipe: int, document: Mapping[str, object]) -> None:
        self.write_bytes(pipe, _encode(document))

    def write_bytes(self, pipe: int, message: bytes) -> None:
        if not message or len(message) > _MAX_MESSAGE_BYTES:
            raise RuntimeError("control message size was invalid") from None
        buffer = ctypes.create_string_buffer(message)
        event, overlapped = self._event()
        written = wintypes.DWORD()
        immediate = cast(
            bool,
            self._write_file(
                wintypes.HANDLE(pipe),
                buffer,
                len(message),
                ctypes.byref(written),
                ctypes.byref(overlapped),
            ),
        )
        transferred = self._complete_io(
            pipe, event, overlapped, immediate, "WriteFile", written.value
        )
        if transferred != len(message):
            raise RuntimeError("control message write was incomplete") from None

    def read_document(self, pipe: int) -> dict[str, object]:
        buffer = ctypes.create_string_buffer(_MAX_MESSAGE_BYTES)
        event, overlapped = self._event()
        received = wintypes.DWORD()
        immediate = cast(
            bool,
            self._read_file(
                wintypes.HANDLE(pipe),
                buffer,
                len(buffer),
                ctypes.byref(received),
                ctypes.byref(overlapped),
            ),
        )
        transferred = self._complete_io(
            pipe, event, overlapped, immediate, "ReadFile", received.value
        )
        return _decode(bytes(buffer.raw[:transferred]))

    def wait_process(self, process: int) -> None:
        outcome = cast(
            int,
            self._wait(wintypes.HANDLE(process), _TIMEOUT_MILLISECONDS),
        )
        if outcome == _DWORD_FAILURE:
            raise self._failure("WaitForSingleObject")
        if outcome != _WAIT_OBJECT_0:
            raise RuntimeError("control participant did not settle before the deadline") from None

    def exit_code(self, process: int) -> int:
        result = wintypes.DWORD()
        if not cast(
            bool,
            self._get_exit_code(wintypes.HANDLE(process), ctypes.byref(result)),
        ):
            raise self._failure("GetExitCodeProcess")
        return result.value

    def settle(self, session: _Session, expected_exit: int) -> None:
        self.wait_process(session.process)
        if self.exit_code(session.process) != expected_exit:
            raise RuntimeError("control participant exit category was unexpected") from None
        self.close_handle(session.process)
        if self.accounting(session.job) != (1, 0):
            raise RuntimeError("control Job Object did not settle") from None
        if session.pipe in self._owned:
            self._disconnect_pipe(wintypes.HANDLE(session.pipe))
            self.close_handle(session.pipe)
        self.close_handle(session.job)


def _start_or_skip(probe: _WindowsControlProbe) -> _Session:
    job = probe.create_job()
    pipe, pipe_name = probe.create_control_pipe()
    probe.assert_first_instance_exclusive(pipe_name)
    try:
        suspended = probe.launch_suspended(job, pipe_name)
    except _NativeFailure as error:
        if error.operation == "AssignProcessToJobObject" and error.code == _ERROR_ACCESS_DENIED:
            pytest.skip("current host does not permit the required nested Job Object")
        raise
    pending = probe.begin_connect(pipe)
    try:
        probe.resume(suspended)
        probe.complete_connect(pipe, pending)
    except BaseException:
        if probe.owns(pending.event):
            probe.cancel_pending(pipe, pending)
            probe.close_handle(pending.event)
        raise
    probe.verify_client_identity(pipe, suspended)
    if probe.accounting(job) != (1, 1) or probe.process_ids(job) != (suspended.pid,):
        raise RuntimeError("control participant membership changed unexpectedly") from None
    if probe.exit_code(suspended.process) != _STILL_ACTIVE:
        raise RuntimeError("control participant exited before the challenge") from None
    probe.assert_no_participant_message(pipe)
    challenge = secrets.token_hex(32)
    return _Session(job, pipe, suspended.process, suspended.pid, challenge)


def _challenge(probe: _WindowsControlProbe, session: _Session) -> None:
    probe.write_document(
        session.pipe,
        _canonical_document("challenge", session.challenge, 0),
    )
    ready = probe.read_document(session.pipe)
    if ready != _canonical_document("ready", session.challenge, 1):
        raise RuntimeError("control participant readiness response was invalid") from None


def test_valid_challenge_releases_one_bound_participant() -> None:
    probe = _WindowsControlProbe()
    with probe:
        session = _start_or_skip(probe)
        _challenge(probe, session)
        probe.write_document(
            session.pipe,
            _canonical_document("release", session.challenge, 2),
        )
        released = probe.read_document(session.pipe)
        assert released == _canonical_document("released", session.challenge, 3)
        probe.settle(session, 0)
    assert probe.owned_count == 0


def test_replayed_challenge_is_rejected_before_release() -> None:
    probe = _WindowsControlProbe()
    with probe:
        session = _start_or_skip(probe)
        _challenge(probe, session)
        probe.write_document(
            session.pipe,
            _canonical_document("challenge", session.challenge, 0),
        )
        probe.settle(session, _EXIT_PROTOCOL)
    assert probe.owned_count == 0


def test_wrong_release_challenge_is_rejected() -> None:
    probe = _WindowsControlProbe()
    with probe:
        session = _start_or_skip(probe)
        _challenge(probe, session)
        probe.write_document(
            session.pipe,
            _canonical_document("release", secrets.token_hex(32), 2),
        )
        probe.settle(session, _EXIT_CHALLENGE)
    assert probe.owned_count == 0


def test_malformed_challenge_is_rejected() -> None:
    probe = _WindowsControlProbe()
    with probe:
        session = _start_or_skip(probe)
        probe.write_bytes(session.pipe, b'{"kind":"challenge"}')
        probe.settle(session, _EXIT_PROTOCOL)
    assert probe.owned_count == 0


def test_disconnect_is_rejected_without_release() -> None:
    probe = _WindowsControlProbe()
    with probe:
        session = _start_or_skip(probe)
        _challenge(probe, session)
        probe.close_handle(session.pipe)
        probe.settle(session, _EXIT_DISCONNECT)
    assert probe.owned_count == 0
