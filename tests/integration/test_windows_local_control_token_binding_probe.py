"""Test-only Windows retained client-token and session-binding probe."""

from __future__ import annotations

import ctypes
import sys
from collections.abc import Callable
from ctypes import wintypes
from dataclasses import dataclass, replace
from types import TracebackType
from typing import Protocol, cast

import pytest

from tests.integration.test_windows_local_control_channel_probe import (
    _canonical_document,  # pyright: ignore[reportPrivateUsage]
    _challenge,  # pyright: ignore[reportPrivateUsage]
    _start_or_skip,  # pyright: ignore[reportPrivateUsage]
    _WindowsControlProbe,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M213 probes native Windows retained-token and session binding",
)

_TOKEN_QUERY = 0x0008
_TOKEN_USER = 1
_TOKEN_STATISTICS = 10
_TOKEN_SESSION_ID = 12
_TOKEN_LOGON_SID = 28
_TOKEN_PRIMARY = 1
_ERROR_INSUFFICIENT_BUFFER = 122


class _NativeFunction(Protocol):
    argtypes: list[object] | None
    restype: object

    def __call__(self, *arguments: object) -> object: ...


class _Luid(ctypes.Structure):
    _fields_ = [("LowPart", wintypes.DWORD), ("HighPart", wintypes.LONG)]


class _SidAndAttributes(ctypes.Structure):
    _fields_ = [("Sid", ctypes.c_void_p), ("Attributes", wintypes.DWORD)]


class _TokenUser(ctypes.Structure):
    _fields_ = [("User", _SidAndAttributes)]


class _TokenGroupsOne(ctypes.Structure):
    _fields_ = [("GroupCount", wintypes.DWORD), ("Groups", _SidAndAttributes * 1)]


class _TokenStatistics(ctypes.Structure):
    _fields_ = [
        ("TokenId", _Luid),
        ("AuthenticationId", _Luid),
        ("ExpirationTime", ctypes.c_longlong),
        ("TokenType", ctypes.c_int),
        ("ImpersonationLevel", ctypes.c_int),
        ("DynamicCharged", wintypes.DWORD),
        ("DynamicAvailable", wintypes.DWORD),
        ("GroupCount", wintypes.DWORD),
        ("PrivilegeCount", wintypes.DWORD),
        ("ModifiedId", _Luid),
    ]


@dataclass(frozen=True, slots=True)
class _TokenSnapshot:
    user_sid: bytes
    logon_sid: bytes
    token_id: tuple[int, int]
    authentication_id: tuple[int, int]
    modified_id: tuple[int, int]
    session_id: int
    token_type: int


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


def _luid(value: _Luid) -> tuple[int, int]:
    return value.LowPart, value.HighPart


class _RetainedTokenBinding:
    """Own one query-only process token and produce private copied snapshots."""

    def __init__(self, process: int) -> None:
        win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
        self._get_last_error = cast(Callable[[], int], vars(ctypes)["get_last_error"])
        kernel32 = win_dll("kernel32", use_last_error=True)
        advapi32 = win_dll("advapi32", use_last_error=True)
        self._close_handle = _load_function(
            kernel32, "CloseHandle", [wintypes.HANDLE], wintypes.BOOL
        )
        self._get_current_process = _load_function(
            kernel32, "GetCurrentProcess", [], wintypes.HANDLE
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
        self._get_length_sid = _load_function(
            advapi32, "GetLengthSid", [ctypes.c_void_p], wintypes.DWORD
        )
        source = (
            cast(wintypes.HANDLE, self._get_current_process())
            if process == 0
            else wintypes.HANDLE(process)
        )
        token = wintypes.HANDLE()
        if not cast(
            bool,
            self._open_process_token(source, _TOKEN_QUERY, ctypes.byref(token)),
        ):
            self._fail("OpenProcessToken")
        if token.value is None or token.value == 0:
            raise RuntimeError("retained process token was unavailable") from None
        self.token = int(token.value)

    def __enter__(self) -> _RetainedTokenBinding:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def _fail(self, operation: str) -> None:
        code = self._get_last_error()
        raise RuntimeError(f"{operation} failed with native code {code}") from None

    def close(self) -> None:
        token = self.token
        if token == 0:
            return
        if not cast(bool, self._close_handle(wintypes.HANDLE(token))):
            self._fail("CloseHandle")
        self.token = 0

    def _query(self, information_class: int) -> ctypes.Array[ctypes.c_char]:
        required = wintypes.DWORD()
        self._get_token_information(
            wintypes.HANDLE(self.token),
            information_class,
            None,
            0,
            ctypes.byref(required),
        )
        if self._get_last_error() != _ERROR_INSUFFICIENT_BUFFER or required.value == 0:
            self._fail("GetTokenInformation")
        buffer = ctypes.create_string_buffer(required.value)
        returned = wintypes.DWORD()
        if not cast(
            bool,
            self._get_token_information(
                wintypes.HANDLE(self.token),
                information_class,
                buffer,
                len(buffer),
                ctypes.byref(returned),
            ),
        ):
            self._fail("GetTokenInformation")
        if returned.value != required.value:
            raise RuntimeError("token information size changed during query") from None
        return buffer

    def _copy_sid(self, pointer: int | None) -> bytes:
        if pointer is None or pointer == 0:
            raise RuntimeError("token SID was unavailable") from None
        length = cast(int, self._get_length_sid(ctypes.c_void_p(pointer)))
        if length == 0:
            self._fail("GetLengthSid")
        return ctypes.string_at(pointer, length)

    def snapshot(self) -> _TokenSnapshot:
        user_buffer = self._query(_TOKEN_USER)
        user = ctypes.cast(user_buffer, ctypes.POINTER(_TokenUser)).contents

        logon_buffer = self._query(_TOKEN_LOGON_SID)
        logon = ctypes.cast(logon_buffer, ctypes.POINTER(_TokenGroupsOne)).contents
        if logon.GroupCount != 1:
            raise RuntimeError("token did not contain one logon identity") from None

        statistics_buffer = self._query(_TOKEN_STATISTICS)
        statistics = ctypes.cast(statistics_buffer, ctypes.POINTER(_TokenStatistics)).contents

        session_buffer = self._query(_TOKEN_SESSION_ID)
        session_id = ctypes.cast(session_buffer, ctypes.POINTER(wintypes.DWORD)).contents

        return _TokenSnapshot(
            user_sid=self._copy_sid(user.User.Sid),
            logon_sid=self._copy_sid(logon.Groups[0].Sid),
            token_id=_luid(statistics.TokenId),
            authentication_id=_luid(statistics.AuthenticationId),
            modified_id=_luid(statistics.ModifiedId),
            session_id=session_id.value,
            token_type=statistics.TokenType,
        )


class _NativeSessionBinding:
    def __init__(self) -> None:
        win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
        self._get_last_error = cast(Callable[[], int], vars(ctypes)["get_last_error"])
        kernel32 = win_dll("kernel32", use_last_error=True)
        self._get_pipe_client_session = _load_function(
            kernel32,
            "GetNamedPipeClientSessionId",
            [wintypes.HANDLE, ctypes.POINTER(wintypes.ULONG)],
            wintypes.BOOL,
        )
        self._process_id_to_session = _load_function(
            kernel32,
            "ProcessIdToSessionId",
            [wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)],
            wintypes.BOOL,
        )

    def verify(self, pipe: int, pid: int, participant: _TokenSnapshot) -> None:
        pipe_session = wintypes.ULONG()
        if not cast(
            bool,
            self._get_pipe_client_session(wintypes.HANDLE(pipe), ctypes.byref(pipe_session)),
        ):
            self._fail("GetNamedPipeClientSessionId")
        process_session = wintypes.DWORD()
        if not cast(
            bool,
            self._process_id_to_session(wintypes.DWORD(pid), ctypes.byref(process_session)),
        ):
            self._fail("ProcessIdToSessionId")
        if not (pipe_session.value == process_session.value == participant.session_id):
            raise RuntimeError("native client session binding was inconsistent") from None

    def _fail(self, operation: str) -> None:
        code = self._get_last_error()
        raise RuntimeError(f"{operation} failed with native code {code}") from None


def _verify_same_logon(controller: _TokenSnapshot, participant: _TokenSnapshot) -> None:
    if participant.token_type != _TOKEN_PRIMARY:
        raise RuntimeError("participant token was not primary") from None
    if participant.user_sid != controller.user_sid:
        raise RuntimeError("participant user identity did not match the controller") from None
    if participant.logon_sid != controller.logon_sid:
        raise RuntimeError("participant logon identity did not match the controller") from None
    if participant.authentication_id != controller.authentication_id:
        raise RuntimeError(
            "participant authentication identity did not match the controller"
        ) from None
    if participant.session_id != controller.session_id:
        raise RuntimeError("participant session did not match the controller") from None


def _verify_stable(before: _TokenSnapshot, after: _TokenSnapshot) -> None:
    if after != before:
        raise RuntimeError("participant token identity changed before release") from None


def test_retained_client_token_binding_is_stable() -> None:
    probe = _WindowsControlProbe()
    with probe:
        session = _start_or_skip(probe)
        with (
            _RetainedTokenBinding(0) as controller_binding,
            _RetainedTokenBinding(session.process) as binding,
        ):
            controller = controller_binding.snapshot()
            participant = binding.snapshot()
            _verify_same_logon(controller, participant)
            _NativeSessionBinding().verify(session.pipe, session.pid, participant)
            participant_logon_sid = ctypes.create_string_buffer(participant.logon_sid)
            probe._verify_pipe_dacl(  # pyright: ignore[reportPrivateUsage]
                session.pipe, ctypes.addressof(participant_logon_sid)
            )
            _challenge(probe, session)
            _verify_stable(participant, binding.snapshot())
            probe.write_document(
                session.pipe,
                _canonical_document("release", session.challenge, 2),
            )
            released = probe.read_document(session.pipe)
            assert released == _canonical_document("released", session.challenge, 3)
        probe.settle(session, 0)
    assert probe.owned_count == 0


def _sample_snapshot() -> _TokenSnapshot:
    return _TokenSnapshot(b"user", b"logon", (1, 2), (3, 4), (5, 6), 7, _TOKEN_PRIMARY)


@pytest.mark.parametrize(
    ("changed", "message"),
    [
        ({"user_sid": b"other"}, "user identity"),
        ({"logon_sid": b"other"}, "logon identity"),
        ({"authentication_id": (8, 9)}, "authentication identity"),
        ({"session_id": 8}, "session"),
        ({"token_type": 2}, "not primary"),
    ],
)
def test_same_logon_binding_fails_closed(changed: dict[str, object], message: str) -> None:
    controller = _sample_snapshot()
    participant = replace(controller, **changed)
    with pytest.raises(RuntimeError, match=message):
        _verify_same_logon(controller, participant)


@pytest.mark.parametrize(
    "changed",
    [
        {"user_sid": b"other"},
        {"logon_sid": b"other"},
        {"token_id": (8, 9)},
        {"authentication_id": (8, 9)},
        {"modified_id": (8, 9)},
        {"session_id": 8},
        {"token_type": 2},
    ],
)
def test_retained_token_drift_fails_closed(changed: dict[str, object]) -> None:
    before = _sample_snapshot()
    with pytest.raises(RuntimeError, match="changed before release"):
        _verify_stable(before, replace(before, **changed))


def test_identical_retained_token_snapshot_is_accepted() -> None:
    snapshot = _sample_snapshot()
    _verify_same_logon(snapshot, snapshot)
    _verify_stable(snapshot, snapshot)
