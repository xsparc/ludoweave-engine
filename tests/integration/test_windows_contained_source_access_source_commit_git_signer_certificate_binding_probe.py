"""Bind the primary signer certificate around the complete M226 boundary."""

from __future__ import annotations

import ctypes
import hashlib
import sys
from collections.abc import Callable
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from typing import cast
from unittest.mock import patch

import pytest

from tests.integration import (
    test_windows_contained_source_access_source_commit_binding_probe as _commit_module,
)
from tests.integration import (
    test_windows_contained_source_access_source_commit_git_authenticode_trust_probe as _m226_module,
)
from tests.integration.test_windows_contained_source_access_source_commit_git_authenticode_trust_probe import (
    _ERROR_SUCCESS,  # pyright: ignore[reportPrivateUsage]
    _WINTRUST_ACTION_GENERIC_VERIFY_V2,  # pyright: ignore[reportPrivateUsage]
    _WINTRUST_DATA,  # pyright: ignore[reportPrivateUsage]
    _WINTRUST_FILE_INFO,  # pyright: ignore[reportPrivateUsage]
    _WTD_CACHE_ONLY_URL_RETRIEVAL,  # pyright: ignore[reportPrivateUsage]
    _WTD_CHOICE_FILE,  # pyright: ignore[reportPrivateUsage]
    _WTD_REVOCATION_CHECK_NONE,  # pyright: ignore[reportPrivateUsage]
    _WTD_REVOKE_NONE,  # pyright: ignore[reportPrivateUsage]
    _WTD_STATEACTION_CLOSE,  # pyright: ignore[reportPrivateUsage]
    _WTD_STATEACTION_VERIFY,  # pyright: ignore[reportPrivateUsage]
    _WTD_UI_NONE,  # pyright: ignore[reportPrivateUsage]
    _NativeFunction,  # pyright: ignore[reportPrivateUsage]
    _signed_status,  # pyright: ignore[reportPrivateUsage]
    _status_hex,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_contained_source_access_source_commit_git_file_retention_probe import (
    _RetainedGitExecutableFile,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _verify_stable as _verify_image_stable,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M227 binds the retained Git Authenticode signer certificate",
)

_MAX_CERTIFICATE_DER_BYTES = 1_048_576
_MAX_CERTIFICATE_CHAIN_LENGTH = 32
_TRUST_E_BAD_DIGEST = 0x80096010


class _CERT_CONTEXT(ctypes.Structure):
    _fields_ = [
        ("dwCertEncodingType", wintypes.DWORD),
        ("pbCertEncoded", ctypes.POINTER(wintypes.BYTE)),
        ("cbCertEncoded", wintypes.DWORD),
        ("pCertInfo", ctypes.c_void_p),
        ("hCertStore", wintypes.HANDLE),
    ]


class _CRYPT_PROVIDER_CERT(ctypes.Structure):
    _fields_ = [
        ("cbStruct", wintypes.DWORD),
        ("pCert", ctypes.POINTER(_CERT_CONTEXT)),
    ]


class _CRYPT_PROVIDER_SGNR(ctypes.Structure):
    _fields_ = [
        ("cbStruct", wintypes.DWORD),
        ("sftVerifyAsOf", wintypes.FILETIME),
        ("csCertChain", wintypes.DWORD),
        ("pasCertChain", ctypes.POINTER(_CRYPT_PROVIDER_CERT)),
    ]


@dataclass(frozen=True, slots=True)
class _SignerCertificateObservation:
    encoded_size: int
    der_sha256: str
    verify_as_of_filetime: int


class _AuthenticodeSignerCertificateVerifier:
    """Own trust verification and copy its primary signer identity."""

    def __init__(self) -> None:
        win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
        wintrust = win_dll("wintrust", use_last_error=True)

        verify = cast(_NativeFunction, wintrust.WinVerifyTrust)
        verify.argtypes = [
            wintypes.HWND,
            ctypes.c_void_p,
            ctypes.POINTER(_WINTRUST_DATA),
        ]
        verify.restype = wintypes.LONG

        provider_data = cast(_NativeFunction, wintrust.WTHelperProvDataFromStateData)
        provider_data.argtypes = [wintypes.HANDLE]
        provider_data.restype = ctypes.c_void_p

        get_signer = cast(_NativeFunction, wintrust.WTHelperGetProvSignerFromChain)
        get_signer.argtypes = [ctypes.c_void_p, wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        get_signer.restype = ctypes.POINTER(_CRYPT_PROVIDER_SGNR)

        get_certificate = cast(_NativeFunction, wintrust.WTHelperGetProvCertFromChain)
        get_certificate.argtypes = [
            ctypes.POINTER(_CRYPT_PROVIDER_SGNR),
            wintypes.DWORD,
        ]
        get_certificate.restype = ctypes.POINTER(_CRYPT_PROVIDER_CERT)

        self._win_verify_trust = verify
        self._provider_data_from_state = provider_data
        self._get_signer_from_chain = get_signer
        self._get_certificate_from_chain = get_certificate

    def observe(self, path: Path, handle: int) -> _SignerCertificateObservation:
        if not path.is_absolute() or handle <= 0:
            raise RuntimeError("retained Git signer input was invalid") from None

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
        observation: _SignerCertificateObservation | None = None
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
            else:
                try:
                    observation = self._read_signer_certificate(trust_data)
                except RuntimeError as error:
                    failure = error
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
        if observation is None:
            raise RuntimeError("signer certificate observation was unavailable") from None
        return observation

    def _read_signer_certificate(self, trust_data: _WINTRUST_DATA) -> _SignerCertificateObservation:
        state_handle = trust_data.hWVTStateData
        if not state_handle:
            raise RuntimeError("signer provider data was unavailable") from None
        provider_data = cast(
            int | None,
            self._provider_data_from_state(state_handle),
        )
        if not provider_data:
            raise RuntimeError("signer provider data was unavailable") from None

        signer = ctypes.cast(
            self._get_signer_from_chain(  # pyright: ignore[reportArgumentType]
                provider_data, 0, False, 0
            ),
            ctypes.POINTER(_CRYPT_PROVIDER_SGNR),
        )
        if not signer:
            raise RuntimeError("primary signer was unavailable") from None
        chain_length = int(signer.contents.csCertChain)
        if not 1 <= chain_length <= _MAX_CERTIFICATE_CHAIN_LENGTH:
            raise RuntimeError("primary signer certificate chain was invalid") from None

        provider_certificate = ctypes.cast(
            self._get_certificate_from_chain(  # pyright: ignore[reportArgumentType]
                signer, 0
            ),
            ctypes.POINTER(_CRYPT_PROVIDER_CERT),
        )
        if not provider_certificate or not provider_certificate.contents.pCert:
            raise RuntimeError("signer certificate was unavailable") from None
        certificate = provider_certificate.contents.pCert.contents
        encoded_size = int(certificate.cbCertEncoded)
        if not 1 <= encoded_size <= _MAX_CERTIFICATE_DER_BYTES:
            raise RuntimeError("signer certificate DER size was invalid") from None
        if not certificate.pbCertEncoded:
            raise RuntimeError("signer certificate DER was unavailable") from None
        encoded = ctypes.string_at(certificate.pbCertEncoded, encoded_size)

        verify_time = signer.contents.sftVerifyAsOf
        verify_as_of_filetime = (int(verify_time.dwHighDateTime) << 32) | int(
            verify_time.dwLowDateTime
        )
        if verify_as_of_filetime <= 0:
            raise RuntimeError("signer verification time was invalid") from None
        return _SignerCertificateObservation(
            encoded_size=encoded_size,
            der_sha256=hashlib.sha256(encoded).hexdigest(),
            verify_as_of_filetime=verify_as_of_filetime,
        )


def test_git_signer_certificate_matches_across_the_complete_m226_boundary() -> None:
    real_which = _commit_module.shutil.which
    with patch.object(
        _commit_module.shutil,
        "which",
        side_effect=real_which,
    ) as initial_lookup:
        git_executable = _commit_module._git_executable()  # pyright: ignore[reportPrivateUsage]
    assert initial_lookup.call_count == 1

    verifier = _AuthenticodeSignerCertificateVerifier()
    with _RetainedGitExecutableFile(git_executable) as retained:
        before_file = retained.snapshot()
        before_signer = verifier.observe(git_executable, retained.handle)
        with patch.object(
            _commit_module.shutil,
            "which",
            return_value=str(git_executable),
        ) as lookup:
            _m226_module.test_retained_git_authenticode_trust_survives_the_m225_boundary()
        assert lookup.call_count == 1
        _verify_image_stable(before_file, retained.snapshot())
        after_signer = verifier.observe(git_executable, retained.handle)
        assert after_signer == before_signer


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
            data_pointer.contents.hWVTStateData = 1
            return self._verify_status
        if action == _WTD_STATEACTION_CLOSE:
            return self._close_status
        raise AssertionError(f"unexpected trust state action: {action}")


class _FakeNativeFunction:
    argtypes: list[object] | None = None
    restype: object = None

    def __init__(self, callback: Callable[..., object]) -> None:
        self._callback = callback

    def __call__(self, *arguments: object) -> object:
        return self._callback(*arguments)


class _FakeSignerMaterial:
    def __init__(self) -> None:
        self.encoded = (wintypes.BYTE * 4)(0x30, 0x02, 0x01, 0x00)
        self.certificate = _CERT_CONTEXT()
        self.certificate.pbCertEncoded = ctypes.cast(self.encoded, ctypes.POINTER(wintypes.BYTE))
        self.certificate.cbCertEncoded = len(self.encoded)
        self.certificate.pCertInfo = None
        self.certificate.hCertStore = wintypes.HANDLE()

        self.provider_certificate = _CRYPT_PROVIDER_CERT()
        self.provider_certificate.cbStruct = ctypes.sizeof(_CRYPT_PROVIDER_CERT)
        self.provider_certificate.pCert = ctypes.pointer(self.certificate)

        self.signer = _CRYPT_PROVIDER_SGNR()
        self.signer.cbStruct = ctypes.sizeof(_CRYPT_PROVIDER_SGNR)
        self.signer.sftVerifyAsOf = wintypes.FILETIME(1, 0)
        self.signer.csCertChain = 1
        self.signer.pasCertChain = ctypes.pointer(self.provider_certificate)

    def provider_data(self, *_arguments: object) -> int:
        return 1

    def get_signer(self, *_arguments: object) -> object:
        return ctypes.pointer(self.signer)

    def get_certificate(self, *_arguments: object) -> object:
        return ctypes.pointer(self.provider_certificate)


def _missing_native_value(*_arguments: object) -> None:
    return None


def _fake_verifier(
    wintrust: _FakeWinTrust,
    *,
    provider_data: Callable[..., object],
    get_signer: Callable[..., object],
    get_certificate: Callable[..., object],
) -> _AuthenticodeSignerCertificateVerifier:
    verifier = object.__new__(_AuthenticodeSignerCertificateVerifier)
    vars(verifier)["_win_verify_trust"] = wintrust
    vars(verifier)["_provider_data_from_state"] = _FakeNativeFunction(provider_data)
    vars(verifier)["_get_signer_from_chain"] = _FakeNativeFunction(get_signer)
    vars(verifier)["_get_certificate_from_chain"] = _FakeNativeFunction(get_certificate)
    return verifier


def test_missing_signer_provider_data_still_closes_provider_state() -> None:
    verifier = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)

    with pytest.raises(RuntimeError, match="signer provider data was unavailable"):
        _fake_verifier(
            verifier,
            provider_data=lambda *_: None,
            get_signer=lambda *_: None,
            get_certificate=lambda *_: None,
        ).observe(Path("c:/git.exe"), 1)

    assert verifier.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_rejected_trust_still_closes_provider_state() -> None:
    verifier = _FakeWinTrust(_signed_status(_TRUST_E_BAD_DIGEST), _ERROR_SUCCESS)

    with pytest.raises(RuntimeError, match="0x80096010"):
        _fake_verifier(
            verifier,
            provider_data=lambda *_: None,
            get_signer=lambda *_: None,
            get_certificate=lambda *_: None,
        ).observe(Path("c:/git.exe"), 1)

    assert verifier.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_missing_signer_certificate_still_closes_provider_state() -> None:
    verifier = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    material = _FakeSignerMaterial()

    with pytest.raises(RuntimeError, match="signer certificate was unavailable"):
        _fake_verifier(
            verifier,
            provider_data=material.provider_data,
            get_signer=material.get_signer,
            get_certificate=lambda *_: None,
        ).observe(Path("c:/git.exe"), 1)

    assert verifier.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


@pytest.mark.parametrize(
    ("fault", "message"),
    [
        ("missing-signer", "primary signer was unavailable"),
        ("empty-chain", "primary signer certificate chain was invalid"),
        ("empty-der", "signer certificate DER size was invalid"),
        ("missing-der", "signer certificate DER was unavailable"),
        ("empty-time", "signer verification time was invalid"),
    ],
)
def test_invalid_signer_material_still_closes_provider_state(fault: str, message: str) -> None:
    verifier = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    material = _FakeSignerMaterial()
    get_signer: Callable[..., object] = material.get_signer
    if fault == "missing-signer":
        get_signer = _missing_native_value
    elif fault == "empty-chain":
        material.signer.csCertChain = 0
    elif fault == "empty-der":
        material.certificate.cbCertEncoded = 0
    elif fault == "missing-der":
        material.certificate.pbCertEncoded = ctypes.POINTER(wintypes.BYTE)()
    elif fault == "empty-time":
        material.signer.sftVerifyAsOf = wintypes.FILETIME()
    else:
        raise AssertionError(f"unexpected signer fault: {fault}")

    with pytest.raises(RuntimeError, match=message):
        _fake_verifier(
            verifier,
            provider_data=material.provider_data,
            get_signer=get_signer,
            get_certificate=material.get_certificate,
        ).observe(Path("c:/git.exe"), 1)

    assert verifier.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_state_close_failure_after_signer_observation_is_reported() -> None:
    verifier = _FakeWinTrust(_ERROR_SUCCESS, _signed_status(_TRUST_E_BAD_DIGEST))
    material = _FakeSignerMaterial()

    with pytest.raises(RuntimeError, match="trust provider state close failed"):
        _fake_verifier(
            verifier,
            provider_data=material.provider_data,
            get_signer=material.get_signer,
            get_certificate=material.get_certificate,
        ).observe(Path("c:/git.exe"), 1)

    assert verifier.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]
