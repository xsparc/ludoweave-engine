"""Test-only Windows suspended-launch and Job Object containment probe."""

from __future__ import annotations

import ctypes
import json
import subprocess
import sys
import time
from collections.abc import Callable, Mapping
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Protocol, cast

import pytest

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M211 probes native Windows Job Object process-tree containment",
)

_ROOT = Path(__file__).parents[2]
_PARTICIPANT = _ROOT / "tests/fixtures/windows_independent_host_process_tree_participant.py"
_DIRECT_PYTHON = Path(sys.base_prefix) / "pythonw.exe"
_SCHEMA = "ludoweave.test.windows-independent-host-process-tree/1"
_MAX_OUTPUT_BYTES = 1_024
_TIMEOUT_SECONDS = 15.0

_CREATE_SUSPENDED = 0x00000004
_EXTENDED_STARTUPINFO_PRESENT = 0x00080000
_CREATE_NO_WINDOW = 0x08000000
_PROC_THREAD_ATTRIBUTE_HANDLE_LIST = 0x00020002

_HANDLE_FLAG_INHERIT = 0x00000001

_JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
_JOB_OBJECT_BASIC_ACCOUNTING_INFORMATION = 1
_JOB_OBJECT_BASIC_PROCESS_ID_LIST = 3
_JOB_OBJECT_EXTENDED_LIMIT_INFORMATION = 9

_PROCESS_QUERY_LIMITED_INFORMATION = 0x00001000
_SYNCHRONIZE = 0x00100000
_WAIT_OBJECT_0 = 0x00000000
_WAIT_TIMEOUT = 0x00000102
_WAIT_FAILED = 0xFFFFFFFF
_STILL_ACTIVE = 259
_ERROR_ACCESS_DENIED = 5
_TERMINATION_EXIT_CODE = 0x4C57


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


class _StartupInfoExW(ctypes.Structure):
    _fields_ = [
        ("StartupInfo", _StartupInfoW),
        ("lpAttributeList", ctypes.c_void_p),
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
        ("ProcessIdList", ctypes.c_size_t * 8),
    ]


class _NativeFailure(RuntimeError):
    def __init__(self, operation: str, code: int) -> None:
        self.operation = operation
        self.code = code
        super().__init__(f"{operation} failed with native code {code}")


@dataclass(frozen=True, slots=True)
class _ProcessTree:
    root_handle: int
    descendant_handle: int
    output_handle: int
    root_pid: int
    descendant_pid: int


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
    if value is None or value == 0:
        raise RuntimeError(f"{operation} returned an invalid handle") from None
    return value


class _WindowsJobProbe:
    def __init__(self) -> None:
        win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
        self._get_last_error = cast(Callable[[], int], vars(ctypes)["get_last_error"])
        kernel32 = win_dll("kernel32", use_last_error=True)
        self._create_job = _load_function(
            kernel32,
            "CreateJobObjectW",
            [ctypes.c_void_p, wintypes.LPCWSTR],
            wintypes.HANDLE,
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
        self._create_pipe = _load_function(
            kernel32,
            "CreatePipe",
            [
                ctypes.POINTER(wintypes.HANDLE),
                ctypes.POINTER(wintypes.HANDLE),
                ctypes.POINTER(_SecurityAttributes),
                wintypes.DWORD,
            ],
            wintypes.BOOL,
        )
        self._set_handle_information = _load_function(
            kernel32,
            "SetHandleInformation",
            [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD],
            wintypes.BOOL,
        )
        self._initialize_attribute_list = _load_function(
            kernel32,
            "InitializeProcThreadAttributeList",
            [ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.c_size_t)],
            wintypes.BOOL,
        )
        self._update_attribute = _load_function(
            kernel32,
            "UpdateProcThreadAttribute",
            [
                ctypes.c_void_p,
                wintypes.DWORD,
                ctypes.c_size_t,
                ctypes.c_void_p,
                ctypes.c_size_t,
                ctypes.c_void_p,
                ctypes.c_void_p,
            ],
            wintypes.BOOL,
        )
        self._delete_attribute_list = _load_function(
            kernel32,
            "DeleteProcThreadAttributeList",
            [ctypes.c_void_p],
            None,
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
                ctypes.c_void_p,
                ctypes.POINTER(_ProcessInformation),
            ],
            wintypes.BOOL,
        )
        self._resume_thread = _load_function(
            kernel32,
            "ResumeThread",
            [wintypes.HANDLE],
            wintypes.DWORD,
        )
        self._open_process = _load_function(
            kernel32,
            "OpenProcess",
            [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD],
            wintypes.HANDLE,
        )
        self._get_process_id = _load_function(
            kernel32,
            "GetProcessId",
            [wintypes.HANDLE],
            wintypes.DWORD,
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
        self._owned: set[int] = set()

    @property
    def owned_count(self) -> int:
        return len(self._owned)

    def __enter__(self) -> _WindowsJobProbe:
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

    def _create_output_pipe(self) -> tuple[int, int]:
        security = _SecurityAttributes(
            nLength=ctypes.sizeof(_SecurityAttributes),
            lpSecurityDescriptor=None,
            bInheritHandle=True,
        )
        read = wintypes.HANDLE()
        write = wintypes.HANDLE()
        if not cast(
            bool,
            self._create_pipe(ctypes.byref(read), ctypes.byref(write), ctypes.byref(security), 0),
        ):
            raise self._failure("CreatePipe")
        read_value = self._own(_handle_value(read, "CreatePipe"))
        write_value = self._own(_handle_value(write, "CreatePipe"))
        if not cast(
            bool,
            self._set_handle_information(
                wintypes.HANDLE(read_value),
                _HANDLE_FLAG_INHERIT,
                0,
            ),
        ):
            raise self._failure("SetHandleInformation")
        return read_value, write_value

    def _attribute_list(
        self, handles: tuple[int, ...]
    ) -> tuple[ctypes.Array[ctypes.c_char], ctypes.Array[wintypes.HANDLE]]:
        size = ctypes.c_size_t()
        self._initialize_attribute_list(None, 1, 0, ctypes.byref(size))
        if size.value == 0:
            raise self._failure("InitializeProcThreadAttributeList")
        buffer = ctypes.create_string_buffer(size.value)
        attribute_list = ctypes.cast(buffer, ctypes.c_void_p)
        if not cast(
            bool,
            self._initialize_attribute_list(attribute_list, 1, 0, ctypes.byref(size)),
        ):
            raise self._failure("InitializeProcThreadAttributeList")
        handle_array = (wintypes.HANDLE * len(handles))(
            *(wintypes.HANDLE(value) for value in handles)
        )
        if not cast(
            bool,
            self._update_attribute(
                attribute_list,
                0,
                _PROC_THREAD_ATTRIBUTE_HANDLE_LIST,
                ctypes.cast(handle_array, ctypes.c_void_p),
                ctypes.sizeof(handle_array),
                None,
                None,
            ),
        ):
            self._delete_attribute_list(attribute_list)
            raise self._failure("UpdateProcThreadAttribute")
        return buffer, handle_array

    def _query_accounting(self, job: int) -> _JobBasicAccountingInformation:
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
        assert returned.value == ctypes.sizeof(information)
        return information

    def accounting(self, job: int) -> tuple[int, int]:
        information = self._query_accounting(job)
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
                wintypes.HANDLE(process),
                wintypes.HANDLE(job),
                ctypes.byref(result),
            ),
        ):
            raise self._failure("IsProcessInJob")
        return bool(result.value)

    def _read_events(self, output: int) -> Mapping[str, Mapping[str, object]]:
        pending = bytearray()
        documents: dict[str, Mapping[str, object]] = {}
        deadline = time.monotonic() + _TIMEOUT_SECONDS
        while len(documents) < 2 and time.monotonic() < deadline:
            available = wintypes.DWORD()
            if not cast(
                bool,
                self._peek_pipe(
                    wintypes.HANDLE(output),
                    None,
                    0,
                    None,
                    ctypes.byref(available),
                    None,
                ),
            ):
                raise self._failure("PeekNamedPipe")
            if available.value == 0:
                time.sleep(0.01)
                continue
            chunk = ctypes.create_string_buffer(min(available.value, 256))
            received = wintypes.DWORD()
            if not cast(
                bool,
                self._read_file(
                    wintypes.HANDLE(output),
                    chunk,
                    len(chunk),
                    ctypes.byref(received),
                    None,
                ),
            ):
                raise self._failure("ReadFile")
            pending.extend(chunk.raw[: received.value])
            if len(pending) > _MAX_OUTPUT_BYTES:
                raise RuntimeError("participant output exceeded its bound") from None
            while b"\n" in pending:
                line, _, remainder = pending.partition(b"\n")
                pending = bytearray(remainder)
                try:
                    parsed: object = json.loads(line)
                except (UnicodeDecodeError, json.JSONDecodeError):
                    raise RuntimeError("participant output was not canonical JSON") from None
                if not isinstance(parsed, dict):
                    raise RuntimeError("participant output was not a JSON object") from None
                document = cast(dict[str, object], parsed)
                canonical = json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
                if canonical != bytes(line) or document.get("schema") != _SCHEMA:
                    raise RuntimeError("participant output was not canonical JSON") from None
                event = document.get("event")
                if event not in {"participant_ready", "descendant_ready"}:
                    raise RuntimeError("participant output had an unknown event") from None
                documents[cast(str, event)] = document
        if len(documents) != 2 or pending:
            raise RuntimeError("participant readiness handshake timed out") from None
        return documents

    def launch_tree(self, job: int) -> _ProcessTree:
        if not _DIRECT_PYTHON.is_file():
            raise RuntimeError("direct Windows Python executable is unavailable") from None
        output, output_write = self._create_output_pipe()
        attribute_buffer, handle_array = self._attribute_list((output_write,))
        startup = _StartupInfoExW()
        startup.StartupInfo.cb = ctypes.sizeof(startup)
        startup.lpAttributeList = ctypes.cast(attribute_buffer, ctypes.c_void_p)
        command_line = ctypes.create_unicode_buffer(
            subprocess.list2cmdline(
                (
                    str(_DIRECT_PYTHON),
                    "-I",
                    "-B",
                    str(_PARTICIPANT),
                    "participant",
                    str(output_write),
                )
            )
        )
        process_information = _ProcessInformation()
        try:
            created = cast(
                bool,
                self._create_process(
                    str(_DIRECT_PYTHON),
                    command_line,
                    None,
                    None,
                    True,
                    _CREATE_SUSPENDED | _CREATE_NO_WINDOW | _EXTENDED_STARTUPINFO_PRESENT,
                    None,
                    str(_ROOT),
                    ctypes.byref(startup),
                    ctypes.byref(process_information),
                ),
            )
        finally:
            self._delete_attribute_list(startup.lpAttributeList)
            del handle_array
        if not created:
            raise self._failure("CreateProcessW")
        root = self._own(_handle_value(process_information.hProcess, "CreateProcessW"))
        thread = self._own(_handle_value(process_information.hThread, "CreateProcessW"))
        self.close_handle(output_write)
        assigned = cast(
            bool,
            self._assign_process(wintypes.HANDLE(job), wintypes.HANDLE(root)),
        )
        if not assigned:
            code = self._get_last_error()
            self._terminate_process(wintypes.HANDLE(root), _TERMINATION_EXIT_CODE)
            self._wait(wintypes.HANDLE(root), 5_000)
            self.close_handle(thread)
            self.close_handle(root)
            raise _NativeFailure("AssignProcessToJobObject", code)
        assert self._process_is_in_job(root, job)
        assert self.accounting(job) == (1, 1)
        assert cast(int, self._wait(wintypes.HANDLE(root), 0)) == _WAIT_TIMEOUT
        available = wintypes.DWORD()
        assert cast(
            bool,
            self._peek_pipe(
                wintypes.HANDLE(output),
                None,
                0,
                None,
                ctypes.byref(available),
                None,
            ),
        )
        assert available.value == 0
        previous_suspend_count = cast(int, self._resume_thread(wintypes.HANDLE(thread)))
        if previous_suspend_count == _WAIT_FAILED:
            raise self._failure("ResumeThread")
        assert previous_suspend_count == 1
        self.close_handle(thread)

        events = self._read_events(output)
        root_event = events["participant_ready"]
        descendant_event = events["descendant_ready"]
        expected_root_fields = {"descendant_pid", "event", "pid", "schema"}
        if set(root_event) != expected_root_fields or set(descendant_event) != {
            "event",
            "pid",
            "schema",
        }:
            raise RuntimeError("participant output had an invalid shape") from None
        root_pid = root_event["pid"]
        descendant_pid = root_event["descendant_pid"]
        if type(root_pid) is not int or type(descendant_pid) is not int:
            raise RuntimeError("participant process identity had an invalid type") from None
        if root_pid != process_information.dwProcessId:
            raise RuntimeError("retained root process identity was inconsistent") from None
        if descendant_event["pid"] != descendant_pid:
            raise RuntimeError("descendant handshake identity was inconsistent") from None
        raw_descendant = cast(
            wintypes.HANDLE,
            self._open_process(
                _SYNCHRONIZE | _PROCESS_QUERY_LIMITED_INFORMATION,
                False,
                descendant_pid,
            ),
        )
        descendant = self._own(_handle_value(raw_descendant, "OpenProcess"))
        if cast(int, self._get_process_id(wintypes.HANDLE(descendant))) != descendant_pid:
            raise RuntimeError("retained descendant identity was inconsistent") from None
        if not self._process_is_in_job(descendant, job):
            raise RuntimeError("descendant escaped the private Job Object") from None
        if set(self.process_ids(job)) != {root_pid, descendant_pid}:
            raise RuntimeError("Job Object contained an unexpected process") from None
        assert self.accounting(job) == (2, 2)
        return _ProcessTree(
            root_handle=root,
            descendant_handle=descendant,
            output_handle=output,
            root_pid=root_pid,
            descendant_pid=descendant_pid,
        )

    def terminate_job(self, job: int) -> None:
        if not cast(
            bool,
            self._terminate_job(wintypes.HANDLE(job), _TERMINATION_EXIT_CODE),
        ):
            raise self._failure("TerminateJobObject")

    def wait_process(self, process: int) -> None:
        outcome = cast(int, self._wait(wintypes.HANDLE(process), 5_000))
        if outcome == _WAIT_FAILED:
            raise self._failure("WaitForSingleObject")
        if outcome != _WAIT_OBJECT_0:
            raise RuntimeError("contained process did not settle before the deadline") from None

    def exit_code(self, process: int) -> int:
        exit_code = wintypes.DWORD()
        if not cast(
            bool,
            self._get_exit_code(wintypes.HANDLE(process), ctypes.byref(exit_code)),
        ):
            raise self._failure("GetExitCodeProcess")
        return exit_code.value

    def wait_job_empty(self, job: int) -> tuple[int, int]:
        deadline = time.monotonic() + _TIMEOUT_SECONDS
        accounting = self.accounting(job)
        while accounting[1] != 0 and time.monotonic() < deadline:
            time.sleep(0.01)
            accounting = self.accounting(job)
        if accounting[1] != 0:
            raise RuntimeError("Job Object retained live process members") from None
        return accounting


def _launch_or_skip(probe: _WindowsJobProbe, job: int) -> _ProcessTree:
    try:
        return probe.launch_tree(job)
    except _NativeFailure as error:
        if error.operation == "AssignProcessToJobObject" and error.code == _ERROR_ACCESS_DENIED:
            pytest.skip("current host does not permit the required nested Job Object")
        raise


def test_job_scoped_termination_settles_exact_process_tree() -> None:
    probe = _WindowsJobProbe()
    with probe:
        job = probe.create_job()
        tree = _launch_or_skip(probe, job)
        assert tree.root_pid != tree.descendant_pid
        assert probe.exit_code(tree.root_handle) == _STILL_ACTIVE
        assert probe.exit_code(tree.descendant_handle) == _STILL_ACTIVE

        probe.terminate_job(job)
        probe.wait_process(tree.root_handle)
        probe.wait_process(tree.descendant_handle)
        assert probe.exit_code(tree.root_handle) == _TERMINATION_EXIT_CODE
        assert probe.exit_code(tree.descendant_handle) == _TERMINATION_EXIT_CODE

        probe.close_handle(tree.root_handle)
        probe.close_handle(tree.descendant_handle)
        assert probe.wait_job_empty(job) == (2, 0)
        probe.close_handle(tree.output_handle)
        probe.close_handle(job)
    assert probe.owned_count == 0


def test_last_job_handle_close_is_a_fail_safe_for_the_tree() -> None:
    probe = _WindowsJobProbe()
    with probe:
        job = probe.create_job()
        tree = _launch_or_skip(probe, job)
        assert probe.accounting(job) == (2, 2)

        probe.close_handle(job)
        probe.wait_process(tree.root_handle)
        probe.wait_process(tree.descendant_handle)
        assert probe.exit_code(tree.root_handle) != _STILL_ACTIVE
        assert probe.exit_code(tree.descendant_handle) != _STILL_ACTIVE

        probe.close_handle(tree.root_handle)
        probe.close_handle(tree.descendant_handle)
        probe.close_handle(tree.output_handle)
    assert probe.owned_count == 0
