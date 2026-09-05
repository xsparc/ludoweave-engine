"""Bind the ordered provider-certificate chain around the complete M227 boundary."""

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
    test_windows_contained_source_access_source_commit_git_signer_certificate_binding_probe as _m227_module,
)
from tests.integration.test_windows_contained_source_access_source_commit_git_file_retention_probe import (
    _RetainedGitExecutableFile,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_contained_source_access_source_commit_git_signer_certificate_binding_probe import (
    _CERT_CONTEXT,  # pyright: ignore[reportPrivateUsage]
    _CRYPT_PROVIDER_CERT,  # pyright: ignore[reportPrivateUsage]
    _CRYPT_PROVIDER_SGNR,  # pyright: ignore[reportPrivateUsage]
    _ERROR_SUCCESS,  # pyright: ignore[reportPrivateUsage]
    _MAX_CERTIFICATE_CHAIN_LENGTH,  # pyright: ignore[reportPrivateUsage]
    _MAX_CERTIFICATE_DER_BYTES,  # pyright: ignore[reportPrivateUsage]
    _TRUST_E_BAD_DIGEST,  # pyright: ignore[reportPrivateUsage]
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
    _FakeNativeFunction,  # pyright: ignore[reportPrivateUsage]
    _FakeWinTrust,  # pyright: ignore[reportPrivateUsage]
    _NativeFunction,  # pyright: ignore[reportPrivateUsage]
    _signed_status,  # pyright: ignore[reportPrivateUsage]
    _status_hex,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _verify_stable as _verify_image_stable,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M228 binds the ordered retained Git provider-certificate chain",
)

_MAX_PROVIDER_CHAIN_DER_BYTES = 4_194_304
_PROVIDER_CHAIN_DOMAIN = b"ludoweave.wintrust-provider-chain/1\0"


@dataclass(frozen=True, slots=True)
class _ProviderCertificateChainObservation:
    chain_length: int
    encoded_sizes: tuple[int, ...]
    certificate_sha256: tuple[str, ...]
    provider_chain_sha256: str
    verify_as_of_filetime: int


class _AuthenticodeProviderChainVerifier:
    """Own trust verification and detach its indexed provider certificates."""

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

    def observe(self, path: Path, handle: int) -> _ProviderCertificateChainObservation:
        if not path.is_absolute() or handle <= 0:
            raise RuntimeError("retained Git provider-chain input was invalid") from None

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
        observation: _ProviderCertificateChainObservation | None = None
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
                    observation = self._read_provider_chain(trust_data)
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
            raise RuntimeError("provider chain observation was unavailable") from None
        return observation

    def _read_provider_chain(
        self, trust_data: _WINTRUST_DATA
    ) -> _ProviderCertificateChainObservation:
        state_handle = trust_data.hWVTStateData
        if not state_handle:
            raise RuntimeError("provider chain data was unavailable") from None
        provider_data = cast(int | None, self._provider_data_from_state(state_handle))
        if not provider_data:
            raise RuntimeError("provider chain data was unavailable") from None

        signer = ctypes.cast(
            self._get_signer_from_chain(  # pyright: ignore[reportArgumentType]
                provider_data, 0, False, 0
            ),
            ctypes.POINTER(_CRYPT_PROVIDER_SGNR),
        )
        if not signer:
            raise RuntimeError("provider chain signer was unavailable") from None
        chain_length = int(signer.contents.csCertChain)
        if not 1 <= chain_length <= _MAX_CERTIFICATE_CHAIN_LENGTH:
            raise RuntimeError("provider certificate chain was invalid") from None

        chain_digest = hashlib.sha256(_PROVIDER_CHAIN_DOMAIN)
        chain_digest.update(chain_length.to_bytes(length=4, byteorder="big", signed=False))
        encoded_sizes: list[int] = []
        certificate_hashes: list[str] = []
        total_encoded_size = 0
        for certificate_index in range(chain_length):
            provider_certificate = ctypes.cast(
                self._get_certificate_from_chain(  # pyright: ignore[reportArgumentType]
                    signer, certificate_index
                ),
                ctypes.POINTER(_CRYPT_PROVIDER_CERT),
            )
            if not provider_certificate or not provider_certificate.contents.pCert:
                raise RuntimeError(
                    f"provider certificate was unavailable at index {certificate_index}"
                ) from None
            certificate = provider_certificate.contents.pCert.contents
            encoded_size = int(certificate.cbCertEncoded)
            if not 1 <= encoded_size <= _MAX_CERTIFICATE_DER_BYTES:
                raise RuntimeError(
                    f"provider certificate DER size was invalid at index {certificate_index}"
                ) from None
            if total_encoded_size > _MAX_PROVIDER_CHAIN_DER_BYTES - encoded_size:
                raise RuntimeError("provider chain DER total was invalid") from None
            if not certificate.pbCertEncoded:
                raise RuntimeError(
                    f"provider certificate DER was unavailable at index {certificate_index}"
                ) from None
            encoded = ctypes.string_at(certificate.pbCertEncoded, encoded_size)
            total_encoded_size += encoded_size
            encoded_sizes.append(encoded_size)
            certificate_hashes.append(hashlib.sha256(encoded).hexdigest())
            chain_digest.update(certificate_index.to_bytes(length=4, byteorder="big", signed=False))
            chain_digest.update(encoded_size.to_bytes(length=8, byteorder="big", signed=False))
            chain_digest.update(encoded)

        verify_time = signer.contents.sftVerifyAsOf
        verify_as_of_filetime = (int(verify_time.dwHighDateTime) << 32) | int(
            verify_time.dwLowDateTime
        )
        if verify_as_of_filetime <= 0:
            raise RuntimeError("provider chain verification time was invalid") from None
        return _ProviderCertificateChainObservation(
            chain_length=chain_length,
            encoded_sizes=tuple(encoded_sizes),
            certificate_sha256=tuple(certificate_hashes),
            provider_chain_sha256=chain_digest.hexdigest(),
            verify_as_of_filetime=verify_as_of_filetime,
        )


def test_git_provider_chain_matches_across_the_complete_m227_boundary() -> None:
    real_which = _commit_module.shutil.which
    with patch.object(
        _commit_module.shutil,
        "which",
        side_effect=real_which,
    ) as initial_lookup:
        git_executable = _commit_module._git_executable()  # pyright: ignore[reportPrivateUsage]
    assert initial_lookup.call_count == 1

    verifier = _AuthenticodeProviderChainVerifier()
    with _RetainedGitExecutableFile(git_executable) as retained:
        before_file = retained.snapshot()
        before_chain = verifier.observe(git_executable, retained.handle)
        with patch.object(
            _commit_module.shutil,
            "which",
            return_value=str(git_executable),
        ) as lookup:
            _m227_module.test_git_signer_certificate_matches_across_the_complete_m226_boundary()
        assert lookup.call_count == 1
        _verify_image_stable(before_file, retained.snapshot())
        after_chain = verifier.observe(git_executable, retained.handle)
        assert after_chain == before_chain


class _FakeProviderChainMaterial:
    def __init__(self, encoded_sizes: tuple[int, ...] = (4, 5, 6)) -> None:
        self.encoded_buffers: list[ctypes.Array[wintypes.BYTE]] = []
        self.certificates: list[_CERT_CONTEXT] = []
        self.encoded_bytes: list[bytes] = []
        self.provider_certificates = (_CRYPT_PROVIDER_CERT * len(encoded_sizes))()
        self.missing_certificate_index: int | None = None

        for index, encoded_size in enumerate(encoded_sizes):
            allocation_size = max(1, min(encoded_size, _MAX_CERTIFICATE_DER_BYTES))
            encoded_value = bytes((index + offset) % 256 for offset in range(allocation_size))
            encoded_buffer = (wintypes.BYTE * allocation_size).from_buffer_copy(encoded_value)
            certificate = _CERT_CONTEXT()
            certificate.pbCertEncoded = ctypes.cast(encoded_buffer, ctypes.POINTER(wintypes.BYTE))
            certificate.cbCertEncoded = encoded_size
            certificate.pCertInfo = None
            certificate.hCertStore = wintypes.HANDLE()
            self.encoded_buffers.append(encoded_buffer)
            self.certificates.append(certificate)
            self.encoded_bytes.append(encoded_value)

            provider_certificate = self.provider_certificates[index]
            provider_certificate.cbStruct = ctypes.sizeof(_CRYPT_PROVIDER_CERT)
            provider_certificate.pCert = ctypes.pointer(certificate)

        self.signer = _CRYPT_PROVIDER_SGNR()
        self.signer.cbStruct = ctypes.sizeof(_CRYPT_PROVIDER_SGNR)
        self.signer.sftVerifyAsOf = wintypes.FILETIME(1, 0)
        self.signer.csCertChain = len(encoded_sizes)
        self.signer.pasCertChain = ctypes.cast(
            self.provider_certificates, ctypes.POINTER(_CRYPT_PROVIDER_CERT)
        )

    def provider_data(self, *_arguments: object) -> int:
        return 1

    def get_signer(self, *_arguments: object) -> object:
        return ctypes.pointer(self.signer)

    def get_certificate(self, *_arguments: object) -> object:
        certificate_index = cast(int, _arguments[1])
        if certificate_index == self.missing_certificate_index:
            return None
        return ctypes.cast(
            ctypes.byref(
                self.provider_certificates,
                certificate_index * ctypes.sizeof(_CRYPT_PROVIDER_CERT),
            ),
            ctypes.POINTER(_CRYPT_PROVIDER_CERT),
        )


class _FakeWinTrustWithoutState:
    def __init__(self) -> None:
        self.calls: list[int] = []

    def __call__(self, *_arguments: object) -> int:
        data_pointer = ctypes.cast(
            _arguments[2],  # pyright: ignore[reportArgumentType]
            ctypes.POINTER(_WINTRUST_DATA),
        )
        self.calls.append(data_pointer.contents.dwStateAction)
        return _ERROR_SUCCESS


def _missing_native_value(*_arguments: object) -> None:
    return None


def _fake_verifier(
    wintrust: _FakeWinTrust | _FakeWinTrustWithoutState,
    *,
    provider_data: Callable[..., object],
    get_signer: Callable[..., object],
    get_certificate: Callable[..., object],
) -> _AuthenticodeProviderChainVerifier:
    verifier = object.__new__(_AuthenticodeProviderChainVerifier)
    vars(verifier)["_win_verify_trust"] = wintrust
    vars(verifier)["_provider_data_from_state"] = _FakeNativeFunction(provider_data)
    vars(verifier)["_get_signer_from_chain"] = _FakeNativeFunction(get_signer)
    vars(verifier)["_get_certificate_from_chain"] = _FakeNativeFunction(get_certificate)
    return verifier


def _expected_chain_digest(encoded_values: tuple[bytes, ...]) -> str:
    digest = hashlib.sha256(_PROVIDER_CHAIN_DOMAIN)
    digest.update(len(encoded_values).to_bytes(length=4, byteorder="big", signed=False))
    for certificate_index, encoded in enumerate(encoded_values):
        digest.update(certificate_index.to_bytes(length=4, byteorder="big", signed=False))
        digest.update(len(encoded).to_bytes(length=8, byteorder="big", signed=False))
        digest.update(encoded)
    return digest.hexdigest()


def test_provider_chain_digest_binds_certificate_boundaries_and_order() -> None:
    split = _expected_chain_digest((b"a", b"bc"))
    regrouped = _expected_chain_digest((b"ab", b"c"))
    reversed_chain = _expected_chain_digest((b"bc", b"a"))

    assert len({split, regrouped, reversed_chain}) == 3


def test_complete_provider_chain_is_detached_before_state_close() -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    material = _FakeProviderChainMaterial()
    observation = _fake_verifier(
        wintrust,
        provider_data=material.provider_data,
        get_signer=material.get_signer,
        get_certificate=material.get_certificate,
    ).observe(Path("c:/git.exe"), 1)

    encoded_values = tuple(material.encoded_bytes)
    assert observation == _ProviderCertificateChainObservation(
        chain_length=3,
        encoded_sizes=(4, 5, 6),
        certificate_sha256=tuple(hashlib.sha256(encoded).hexdigest() for encoded in encoded_values),
        provider_chain_sha256=_expected_chain_digest(encoded_values),
        verify_as_of_filetime=1,
    )
    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_missing_provider_state_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrustWithoutState()

    with pytest.raises(RuntimeError, match="provider chain data was unavailable"):
        _fake_verifier(
            wintrust,
            provider_data=_missing_native_value,
            get_signer=_missing_native_value,
            get_certificate=_missing_native_value,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_rejected_trust_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrust(_signed_status(_TRUST_E_BAD_DIGEST), _ERROR_SUCCESS)
    material = _FakeProviderChainMaterial()

    with pytest.raises(RuntimeError, match="0x80096010"):
        _fake_verifier(
            wintrust,
            provider_data=material.provider_data,
            get_signer=material.get_signer,
            get_certificate=material.get_certificate,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


@pytest.mark.parametrize(
    ("fault", "message"),
    [
        ("missing-data", "provider chain data was unavailable"),
        ("missing-signer", "provider chain signer was unavailable"),
        ("empty-chain", "provider certificate chain was invalid"),
        ("oversized-chain", "provider certificate chain was invalid"),
        ("missing-certificate", "provider certificate was unavailable at index 1"),
        ("empty-der", "provider certificate DER size was invalid at index 1"),
        ("oversized-der", "provider certificate DER size was invalid at index 1"),
        ("missing-der", "provider certificate DER was unavailable at index 1"),
        ("empty-time", "provider chain verification time was invalid"),
    ],
)
def test_invalid_provider_chain_still_closes_provider_state(fault: str, message: str) -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    material = _FakeProviderChainMaterial()
    provider_data: Callable[..., object] = material.provider_data
    get_signer: Callable[..., object] = material.get_signer
    if fault == "missing-data":
        provider_data = _missing_native_value
    elif fault == "missing-signer":
        get_signer = _missing_native_value
    elif fault == "empty-chain":
        material.signer.csCertChain = 0
    elif fault == "oversized-chain":
        material.signer.csCertChain = _MAX_CERTIFICATE_CHAIN_LENGTH + 1
    elif fault == "missing-certificate":
        material.missing_certificate_index = 1
    elif fault == "empty-der":
        material.certificates[1].cbCertEncoded = 0
    elif fault == "oversized-der":
        material.certificates[1].cbCertEncoded = _MAX_CERTIFICATE_DER_BYTES + 1
    elif fault == "missing-der":
        material.certificates[1].pbCertEncoded = ctypes.POINTER(wintypes.BYTE)()
    elif fault == "empty-time":
        material.signer.sftVerifyAsOf = wintypes.FILETIME()
    else:
        raise AssertionError(f"unexpected provider-chain fault: {fault}")

    with pytest.raises(RuntimeError, match=message):
        _fake_verifier(
            wintrust,
            provider_data=provider_data,
            get_signer=get_signer,
            get_certificate=material.get_certificate,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_provider_chain_total_der_limit_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    material = _FakeProviderChainMaterial((_MAX_CERTIFICATE_DER_BYTES,) * 5)

    with pytest.raises(RuntimeError, match="provider chain DER total was invalid"):
        _fake_verifier(
            wintrust,
            provider_data=material.provider_data,
            get_signer=material.get_signer,
            get_certificate=material.get_certificate,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_state_close_failure_after_provider_chain_observation_is_reported() -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _signed_status(_TRUST_E_BAD_DIGEST))
    material = _FakeProviderChainMaterial()

    with pytest.raises(RuntimeError, match="trust provider state close failed"):
        _fake_verifier(
            wintrust,
            provider_data=material.provider_data,
            get_signer=material.get_signer,
            get_certificate=material.get_certificate,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]
