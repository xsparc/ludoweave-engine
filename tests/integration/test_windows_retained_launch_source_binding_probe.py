"""Test-only Windows retained launch-source binding probe."""

from __future__ import annotations

import ctypes
import sys
from collections.abc import Callable
from ctypes import wintypes
from dataclasses import replace
from pathlib import Path
from types import TracebackType
from typing import cast

import pytest

from tests.integration.test_windows_local_control_channel_probe import (
    _CREATE_NO_WINDOW,  # pyright: ignore[reportPrivateUsage]
    _CREATE_SUSPENDED,  # pyright: ignore[reportPrivateUsage]
    _DIRECT_PYTHON,  # pyright: ignore[reportPrivateUsage]
    _PARTICIPANT,  # pyright: ignore[reportPrivateUsage]
    _PIPE_PREFIX,  # pyright: ignore[reportPrivateUsage]
    _ROOT,  # pyright: ignore[reportPrivateUsage]
    _TERMINATION_EXIT_CODE,  # pyright: ignore[reportPrivateUsage]
    _TIMEOUT_MILLISECONDS,  # pyright: ignore[reportPrivateUsage]
    _WAIT_TIMEOUT,  # pyright: ignore[reportPrivateUsage]
    _canonical_document,  # pyright: ignore[reportPrivateUsage]
    _challenge,  # pyright: ignore[reportPrivateUsage]
    _handle_value,  # pyright: ignore[reportPrivateUsage]
    _NativeFailure,  # pyright: ignore[reportPrivateUsage]
    _ProcessInformation,  # pyright: ignore[reportPrivateUsage]
    _SecurityAttributes,  # pyright: ignore[reportPrivateUsage]
    _start_or_skip,  # pyright: ignore[reportPrivateUsage]
    _StartupInfoW,  # pyright: ignore[reportPrivateUsage]
    _SuspendedProcess,  # pyright: ignore[reportPrivateUsage]
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
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _FILE_ATTRIBUTE_NORMAL,  # pyright: ignore[reportPrivateUsage]
    _FILE_SHARE_READ,  # pyright: ignore[reportPrivateUsage]
    _FILE_SHARE_WRITE,  # pyright: ignore[reportPrivateUsage]
    _GENERIC_READ,  # pyright: ignore[reportPrivateUsage]
    _MAX_IMAGE_BYTES,  # pyright: ignore[reportPrivateUsage]
    _OPEN_EXISTING,  # pyright: ignore[reportPrivateUsage]
    _READ_CHUNK_BYTES,  # pyright: ignore[reportPrivateUsage]
    _ImageApi,  # pyright: ignore[reportPrivateUsage]
    _ImageSnapshot,  # pyright: ignore[reportPrivateUsage]
    _load_function,  # pyright: ignore[reportPrivateUsage]
    _normalized_name,  # pyright: ignore[reportPrivateUsage]
    _RetainedImageFile,  # pyright: ignore[reportPrivateUsage]
    _RetainedProcessImage,  # pyright: ignore[reportPrivateUsage]
    _verify_expected_image,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _verify_stable as _verify_image_stable,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M215 probes native Windows retained launch-source binding",
)

_EXTENDED_STARTUPINFO_PRESENT = 0x00080000
_PROC_THREAD_ATTRIBUTE_HANDLE_LIST = 0x00020002
_STARTF_USESTDHANDLES = 0x00000100
_HANDLE_FLAG_INHERIT = 0x00000001
_GENERIC_WRITE = 0x40000000
_MAX_LAUNCH_SOURCE_BYTES = _MAX_IMAGE_BYTES
_LAUNCH_SOURCE_READ_CHUNK_BYTES = _READ_CHUNK_BYTES


class _StartupInfoExW(ctypes.Structure):
    _fields_ = [
        ("StartupInfo", _StartupInfoW),
        ("lpAttributeList", ctypes.c_void_p),
    ]


def _fixed_command_line(pipe_name: str) -> str:
    suffix = pipe_name[len(_PIPE_PREFIX) :] if pipe_name.startswith(_PIPE_PREFIX) else ""
    if len(suffix) != 32 or any(character not in "0123456789abcdef" for character in suffix):
        raise RuntimeError("control pipe name was invalid") from None
    arguments = (str(_DIRECT_PYTHON), "-I", "-B", "-", pipe_name)
    return f'"{arguments[0]}" {arguments[1]} {arguments[2]} {arguments[3]} {arguments[4]}'


def _require_exact_standard_handles(handles: tuple[int, ...]) -> None:
    if len(handles) != 3 or len(set(handles)) != 3 or any(handle <= 0 for handle in handles):
        raise RuntimeError("inherited standard handles were not exact") from None


class _InheritedLaunchSource(_RetainedImageFile):
    """Own one inheritable, read-only source handle used as participant stdin."""

    def __init__(self, path: str | Path) -> None:
        if _MAX_LAUNCH_SOURCE_BYTES <= 0 or _LAUNCH_SOURCE_READ_CHUNK_BYTES <= 0:
            raise RuntimeError("launch-source read bounds were invalid") from None
        self._api = _ImageApi()
        self._close_handle = self._api.close_handle
        self._name = _normalized_name(path)
        security = _SecurityAttributes(
            nLength=ctypes.sizeof(_SecurityAttributes),
            lpSecurityDescriptor=None,
            bInheritHandle=True,
        )
        raw = cast(
            wintypes.HANDLE,
            self._api.create_file(
                self._name,
                _GENERIC_READ,
                _FILE_SHARE_READ,
                ctypes.byref(security),
                _OPEN_EXISTING,
                _FILE_ATTRIBUTE_NORMAL,
                wintypes.HANDLE(),
            ),
        )
        self.handle = _handle_value(raw, "CreateFileW")

    def __enter__(self) -> _InheritedLaunchSource:
        return self

    def rewind(self) -> None:
        position = ctypes.c_longlong()
        if not cast(
            bool,
            self._api.set_file_pointer(
                wintypes.HANDLE(self.handle),
                ctypes.c_longlong(0),
                ctypes.byref(position),
                0,
            ),
        ):
            raise self._api.fail("SetFilePointerEx") from None
        if position.value != 0:
            raise RuntimeError("launch source did not rewind to offset zero") from None


class _InheritedNullHandle:
    """Own one inheritable write-only NUL handle for a fixed standard stream."""

    def __init__(self) -> None:
        self._api = _ImageApi()
        self._close_handle = self._api.close_handle
        security = _SecurityAttributes(
            nLength=ctypes.sizeof(_SecurityAttributes),
            lpSecurityDescriptor=None,
            bInheritHandle=True,
        )
        raw = cast(
            wintypes.HANDLE,
            self._api.create_file(
                "NUL",
                _GENERIC_WRITE,
                _FILE_SHARE_READ | _FILE_SHARE_WRITE,
                ctypes.byref(security),
                _OPEN_EXISTING,
                _FILE_ATTRIBUTE_NORMAL,
                wintypes.HANDLE(),
            ),
        )
        self.handle = _handle_value(raw, "CreateFileW")

    def __enter__(self) -> _InheritedNullHandle:
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


class _RetainedLaunchSourceControlProbe(_WindowsControlProbe):
    def __init__(
        self,
        source: _InheritedLaunchSource,
        output: _InheritedNullHandle,
        error: _InheritedNullHandle,
    ) -> None:
        super().__init__()
        self._source = source
        self._output = output
        self._error = error
        win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
        kernel32 = win_dll("kernel32", use_last_error=True)
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
        self._get_handle_information = _load_function(
            kernel32,
            "GetHandleInformation",
            [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)],
            wintypes.BOOL,
        )

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

    def _require_inheritable(self, handle: int) -> None:
        flags = wintypes.DWORD()
        if not cast(
            bool,
            self._get_handle_information(wintypes.HANDLE(handle), ctypes.byref(flags)),
        ):
            raise self._failure("GetHandleInformation")
        if flags.value != _HANDLE_FLAG_INHERIT:
            raise RuntimeError("standard handle was not solely inheritable") from None

    def launch_suspended(self, job: int, pipe_name: str) -> _SuspendedProcess:
        if not _DIRECT_PYTHON.is_file():
            raise RuntimeError("direct Windows Python executable is unavailable") from None
        standard_handles = (self._source.handle, self._output.handle, self._error.handle)
        _require_exact_standard_handles(standard_handles)
        for handle in standard_handles:
            self._require_inheritable(handle)
        attribute_buffer, handle_array = self._attribute_list(standard_handles)
        startup = _StartupInfoExW()
        startup.StartupInfo.cb = ctypes.sizeof(startup)
        startup.StartupInfo.dwFlags = _STARTF_USESTDHANDLES
        startup.StartupInfo.hStdInput = wintypes.HANDLE(self._source.handle)
        startup.StartupInfo.hStdOutput = wintypes.HANDLE(self._output.handle)
        startup.StartupInfo.hStdError = wintypes.HANDLE(self._error.handle)
        startup.lpAttributeList = ctypes.cast(attribute_buffer, ctypes.c_void_p)
        self._source.rewind()
        command_line = ctypes.create_unicode_buffer(_fixed_command_line(pipe_name))
        information = _ProcessInformation()
        try:
            created = cast(
                bool,
                self._create_process(  # pyright: ignore[reportPrivateUsage]
                    str(_DIRECT_PYTHON),
                    command_line,
                    None,
                    None,
                    True,
                    _CREATE_SUSPENDED | _CREATE_NO_WINDOW | _EXTENDED_STARTUPINFO_PRESENT,
                    None,
                    str(_ROOT),
                    ctypes.cast(ctypes.byref(startup), ctypes.POINTER(_StartupInfoW)),
                    ctypes.byref(information),
                ),
            )
        finally:
            self._delete_attribute_list(startup.lpAttributeList)
            del handle_array
        if not created:
            raise self._failure("CreateProcessW")  # pyright: ignore[reportPrivateUsage]
        process = self._own(  # pyright: ignore[reportPrivateUsage]
            _handle_value(information.hProcess, "CreateProcessW")
        )
        thread = self._own(  # pyright: ignore[reportPrivateUsage]
            _handle_value(information.hThread, "CreateProcessW")
        )
        assigned = cast(
            bool,
            self._assign_process(  # pyright: ignore[reportPrivateUsage]
                wintypes.HANDLE(job), wintypes.HANDLE(process)
            ),
        )
        if not assigned:
            code = self._get_last_error()  # pyright: ignore[reportPrivateUsage]
            self._terminate_process(  # pyright: ignore[reportPrivateUsage]
                wintypes.HANDLE(process), _TERMINATION_EXIT_CODE
            )
            self._wait(  # pyright: ignore[reportPrivateUsage]
                wintypes.HANDLE(process), _TIMEOUT_MILLISECONDS
            )
            self.close_handle(thread)
            self.close_handle(process)
            raise _NativeFailure("AssignProcessToJobObject", code)
        if not self._process_is_in_job(  # pyright: ignore[reportPrivateUsage]
            process, job
        ):
            raise RuntimeError("control participant escaped the private Job Object") from None
        if self.accounting(job) != (1, 1) or self.process_ids(job) != (information.dwProcessId,):
            raise RuntimeError("control Job Object membership was not exact") from None
        if (
            cast(
                int,
                self._wait(wintypes.HANDLE(process), 0),  # pyright: ignore[reportPrivateUsage]
            )
            != _WAIT_TIMEOUT
        ):
            raise RuntimeError("suspended control participant was not live") from None
        return _SuspendedProcess(process, thread, information.dwProcessId)


def _verify_source_stable(before: _ImageSnapshot, after: _ImageSnapshot) -> None:
    if after != before:
        raise RuntimeError("retained launch source changed before release") from None


def test_retained_launch_source_is_stable() -> None:
    with (
        _InheritedLaunchSource(_PARTICIPANT) as source_file,
        _InheritedNullHandle() as output_handle,
        _InheritedNullHandle() as error_handle,
    ):
        probe = _RetainedLaunchSourceControlProbe(source_file, output_handle, error_handle)
        with probe, _RetainedImageFile(_DIRECT_PYTHON) as expected_image_file:
            source_before = source_file.snapshot()
            expected_image = expected_image_file.snapshot()
            session = _start_or_skip(probe)
            output_handle.close()
            error_handle.close()
            with (
                _RetainedTokenBinding(0) as controller_binding,
                _RetainedTokenBinding(session.process) as participant_binding,
                _RetainedProcessImage(session.process) as observed_image,
            ):
                controller = controller_binding.snapshot()
                participant = participant_binding.snapshot()
                _verify_same_logon(controller, participant)
                _NativeSessionBinding().verify(session.pipe, session.pid, participant)
                participant_logon_sid = ctypes.create_string_buffer(participant.logon_sid)
                probe._verify_pipe_dacl(  # pyright: ignore[reportPrivateUsage]
                    session.pipe, ctypes.addressof(participant_logon_sid)
                )
                image_before = observed_image.snapshot()
                _verify_expected_image(expected_image, image_before)
                _challenge(probe, session)
                _verify_token_stable(participant, participant_binding.snapshot())
                _verify_image_stable(expected_image, expected_image_file.snapshot())
                _verify_image_stable(image_before, observed_image.snapshot())
                _verify_source_stable(source_before, source_file.snapshot())
                probe.write_document(
                    session.pipe,
                    _canonical_document("release", session.challenge, 2),
                )
                released = probe.read_document(session.pipe)
                assert released == _canonical_document("released", session.challenge, 3)
            probe.settle(session, 0)
        assert probe.owned_count == 0


@pytest.mark.parametrize(
    "handles",
    [
        (),
        (1,),
        (1, 2),
        (1, 2, 3, 4),
        (1, 1, 2),
        (0, 1, 2),
        (-1, 1, 2),
    ],
)
def test_non_exact_standard_handle_sets_fail_closed(handles: tuple[int, ...]) -> None:
    with pytest.raises(RuntimeError, match="not exact"):
        _require_exact_standard_handles(handles)


@pytest.mark.parametrize(
    "pipe_name",
    [
        "",
        _PIPE_PREFIX,
        _PIPE_PREFIX + "0" * 31,
        _PIPE_PREFIX + "0" * 33,
        _PIPE_PREFIX + "g" * 32,
        _PIPE_PREFIX + "0" * 31 + " ",
    ],
)
def test_noncanonical_pipe_names_fail_closed(pipe_name: str) -> None:
    with pytest.raises(RuntimeError, match="pipe name"):
        _fixed_command_line(pipe_name)


def test_fixed_command_line_uses_isolated_standard_input() -> None:
    pipe_name = _PIPE_PREFIX + "0" * 32
    command_line = _fixed_command_line(pipe_name)
    assert command_line == f'"{_DIRECT_PYTHON}" -I -B - {pipe_name}'
    assert str(_PARTICIPANT) not in command_line


@pytest.mark.parametrize(
    "changed",
    [
        {"normalized_name": "c:\\other.py"},
        {"volume_serial": 2},
        {"file_id": b"other"},
        {"size": 3},
        {"sha256": b"other"},
    ],
)
def test_retained_launch_source_drift_fails_closed(changed: dict[str, object]) -> None:
    before = _ImageSnapshot("c:\\participant.py", 1, b"file-id", 2, b"digest")
    with pytest.raises(RuntimeError, match="changed before release"):
        _verify_source_stable(before, replace(before, **changed))


def test_identical_launch_source_snapshot_is_accepted() -> None:
    snapshot = _ImageSnapshot("c:\\participant.py", 1, b"file-id", 2, b"digest")
    _verify_source_stable(snapshot, snapshot)
