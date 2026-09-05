"""Verify retained Git Authenticode trust around the complete M225 boundary."""

from __future__ import annotations

import ctypes
import sys
from collections.abc import Callable
from ctypes import wintypes
from pathlib import Path
from typing import Protocol, cast
from unittest.mock import patch

import pytest

from tests.integration import (
    test_windows_contained_source_access_source_commit_binding_probe as _commit_module,
)
from tests.integration import (
    test_windows_contained_source_access_source_commit_git_child_image_binding_probe as _m225_module,
)
from tests.integration.test_windows_contained_source_access_source_commit_git_file_retention_probe import (
    _RetainedGitExecutableFile,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _verify_stable as _verify_image_stable,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M226 verifies Windows Authenticode trust for the retained Git image",
)

_ERROR_SUCCESS = 0
_WTD_UI_NONE = 2
_WTD_REVOKE_NONE = 0
_WTD_CHOICE_FILE = 1
_WTD_STATEACTION_VERIFY = 0x00000001
_WTD_STATEACTION_CLOSE = 0x00000002
_WTD_REVOCATION_CHECK_NONE = 0x00000010
_WTD_CACHE_ONLY_URL_RETRIEVAL = 0x00001000
_TRUST_E_NOSIGNATURE = 0x800B0100
_TRUST_E_BAD_DIGEST = 0x80096010


class _NativeFunction(Protocol):
    argtypes: list[object] | None
    restype: object

    def __call__(self, *arguments: object) -> object: ...


class _GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", wintypes.BYTE * 8),
    ]


_WINTRUST_ACTION_GENERIC_VERIFY_V2 = _GUID(
    0x00AAC56B,
    0xCD44,
    0x11D0,
    (wintypes.BYTE * 8)(0x8C, 0xC2, 0x00, 0xC0, 0x4F, 0xC2, 0x95, 0xEE),
)


class _WINTRUST_FILE_INFO(ctypes.Structure):
    _fields_ = [
        ("cbStruct", wintypes.DWORD),
        ("pcwszFilePath", wintypes.LPCWSTR),
        ("hFile", wintypes.HANDLE),
        ("pgKnownSubject", ctypes.POINTER(_GUID)),
    ]


class _WINTRUST_DATA(ctypes.Structure):
    _fields_ = [
        ("cbStruct", wintypes.DWORD),
        ("pPolicyCallbackData", ctypes.c_void_p),
        ("pSIPClientData", ctypes.c_void_p),
        ("dwUIChoice", wintypes.DWORD),
        ("fdwRevocationChecks", wintypes.DWORD),
        ("dwUnionChoice", wintypes.DWORD),
        ("pFile", ctypes.POINTER(_WINTRUST_FILE_INFO)),
        ("dwStateAction", wintypes.DWORD),
        ("hWVTStateData", wintypes.HANDLE),
        ("pwszURLReference", wintypes.LPCWSTR),
        ("dwProvFlags", wintypes.DWORD),
        ("dwUIContext", wintypes.DWORD),
        ("pSignatureSettings", ctypes.c_void_p),
    ]


def _signed_status(value: int) -> int:
    return ctypes.c_long(value).value


def _status_hex(status: int) -> str:
    return f"0x{status & 0xFFFFFFFF:08x}"


class _AuthenticodeVerifier:
    """Own one noninteractive WinVerifyTrust verification lifecycle."""

    def __init__(self) -> None:
        win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
        wintrust = win_dll("wintrust", use_last_error=True)
        function = cast(_NativeFunction, wintrust.WinVerifyTrust)
        function.argtypes = [
            wintypes.HWND,
            ctypes.POINTER(_GUID),
            ctypes.POINTER(_WINTRUST_DATA),
        ]
        function.restype = wintypes.LONG
        self._win_verify_trust = function

    def verify(self, path: Path, handle: int) -> None:
        if not path.is_absolute() or handle <= 0:
            raise RuntimeError("retained Git trust input was invalid") from None

        file_info = _WINTRUST_FILE_INFO()
        file_info.cbStruct = ctypes.sizeof(file_info)
        file_info.pcwszFilePath = str(path)
        file_info.hFile = wintypes.HANDLE(handle)
        file_info.pgKnownSubject = None

        trust_data = _WINTRUST_DATA()
        trust_data.cbStruct = ctypes.sizeof(trust_data)
        trust_data.pPolicyCallbackData = None
        trust_data.pSIPClientData = None
        trust_data.dwUIChoice = _WTD_UI_NONE
        trust_data.fdwRevocationChecks = _WTD_REVOKE_NONE
        trust_data.dwUnionChoice = _WTD_CHOICE_FILE
        trust_data.pFile = ctypes.pointer(file_info)
        trust_data.dwStateAction = _WTD_STATEACTION_VERIFY
        trust_data.hWVTStateData = wintypes.HANDLE()
        trust_data.pwszURLReference = None
        trust_data.dwProvFlags = _WTD_CACHE_ONLY_URL_RETRIEVAL | _WTD_REVOCATION_CHECK_NONE
        trust_data.dwUIContext = 0
        trust_data.pSignatureSettings = None

        failure: RuntimeError | None = None
        try:
            status = cast(
                int,
                self._win_verify_trust(
                    wintypes.HWND(),
                    ctypes.byref(_WINTRUST_ACTION_GENERIC_VERIFY_V2),
                    ctypes.byref(trust_data),
                ),
            )
            if status != _ERROR_SUCCESS:
                failure = RuntimeError(
                    f"WinVerifyTrust rejected retained Git: {_status_hex(status)}"
                )
        finally:
            trust_data.dwStateAction = _WTD_STATEACTION_CLOSE
            close_status = cast(
                int,
                self._win_verify_trust(
                    wintypes.HWND(),
                    ctypes.byref(_WINTRUST_ACTION_GENERIC_VERIFY_V2),
                    ctypes.byref(trust_data),
                ),
            )
            if close_status != _ERROR_SUCCESS and failure is None:
                failure = RuntimeError(
                    f"trust provider state close failed: {_status_hex(close_status)}"
                )
        if failure is not None:
            raise failure from None


def test_retained_git_authenticode_trust_survives_the_m225_boundary() -> None:
    real_which = _commit_module.shutil.which
    with patch.object(
        _commit_module.shutil,
        "which",
        side_effect=real_which,
    ) as initial_lookup:
        git_executable = _commit_module._git_executable()  # pyright: ignore[reportPrivateUsage]
    assert initial_lookup.call_count == 1

    verifier = _AuthenticodeVerifier()
    with _RetainedGitExecutableFile(git_executable) as retained:
        before = retained.snapshot()
        if Path(before.normalized_name) != git_executable:
            raise RuntimeError("retained Git trust path was not canonical") from None
        verifier.verify(git_executable, retained.handle)
        with patch.object(
            _commit_module.shutil,
            "which",
            return_value=str(git_executable),
        ) as lookup:
            _m225_module.test_git_child_images_match_the_retained_m224_executable()
        assert lookup.call_count == 1
        _verify_image_stable(before, retained.snapshot())
        verifier.verify(git_executable, retained.handle)


class _FakeWinTrust:
    def __init__(self, verify_status: int, close_status: int) -> None:
        self._verify_status = verify_status
        self._close_status = close_status
        self.calls: list[int] = []

    def __call__(self, *_arguments: object) -> int:
        data_pointer = ctypes.cast(
            _arguments[2],  # pyright: ignore[reportArgumentType]
            ctypes.POINTER(_WINTRUST_DATA),
        )
        action = data_pointer.contents.dwStateAction
        self.calls.append(action)
        if action == _WTD_STATEACTION_VERIFY:
            return self._verify_status
        if action == _WTD_STATEACTION_CLOSE:
            return self._close_status
        raise AssertionError(f"unexpected trust state action: {action}")


def _fake_verifier(fake: _FakeWinTrust) -> _AuthenticodeVerifier:
    verifier = object.__new__(_AuthenticodeVerifier)
    vars(verifier)["_win_verify_trust"] = fake
    return verifier


def test_rejected_trust_still_closes_provider_state() -> None:
    verifier = _FakeWinTrust(_signed_status(_TRUST_E_NOSIGNATURE), _ERROR_SUCCESS)

    with pytest.raises(RuntimeError, match="0x800b0100"):
        _fake_verifier(verifier).verify(Path("c:/git.exe"), 1)

    assert verifier.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_trust_provider_state_close_failure_is_reported() -> None:
    verifier = _FakeWinTrust(_ERROR_SUCCESS, _signed_status(_TRUST_E_BAD_DIGEST))

    with pytest.raises(RuntimeError, match="trust provider state close failed"):
        _fake_verifier(verifier).verify(Path("c:/git.exe"), 1)

    assert verifier.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]
