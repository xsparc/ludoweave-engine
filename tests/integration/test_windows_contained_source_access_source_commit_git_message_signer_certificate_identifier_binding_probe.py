"""Bind WinTrust message signer identifiers to exact verified certificates."""

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
    test_windows_contained_source_access_source_commit_git_message_signer_certificate_binding_probe as _m231_module,
)
from tests.integration.test_windows_contained_source_access_source_commit_git_file_retention_probe import (
    _RetainedGitExecutableFile,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_contained_source_access_source_commit_git_message_signer_certificate_binding_probe import (
    _CERT_CONTEXT,  # pyright: ignore[reportPrivateUsage]
    _CMSG_SIGNER_COUNT_PARAM,  # pyright: ignore[reportPrivateUsage]
    _CMSG_USE_SIGNER_INDEX_FLAG,  # pyright: ignore[reportPrivateUsage]
    _CRYPT_PROVIDER_CERT,  # pyright: ignore[reportPrivateUsage]
    _CRYPT_PROVIDER_DATA_PREFIX,  # pyright: ignore[reportPrivateUsage]
    _CRYPT_PROVIDER_SGNR,  # pyright: ignore[reportPrivateUsage]
    _ERROR_SUCCESS,  # pyright: ignore[reportPrivateUsage]
    _MAX_CERTIFICATE_CHAIN_LENGTH,  # pyright: ignore[reportPrivateUsage]
    _MAX_CERTIFICATE_DER_BYTES,  # pyright: ignore[reportPrivateUsage]
    _MAX_MESSAGE_SIGNERS,  # pyright: ignore[reportPrivateUsage]
    _MAX_PROVIDER_STORES,  # pyright: ignore[reportPrivateUsage]
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
    _FakeMessageSignerCertificateMaterial,  # pyright: ignore[reportPrivateUsage]
    _FakeNativeFunction,  # pyright: ignore[reportPrivateUsage]
    _FakeWinTrust,  # pyright: ignore[reportPrivateUsage]
    _FakeWinTrustWithoutState,  # pyright: ignore[reportPrivateUsage]
    _NativeFunction,  # pyright: ignore[reportPrivateUsage]
    _signed_status,  # pyright: ignore[reportPrivateUsage]
    _status_hex,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _verify_stable as _verify_image_stable,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M232 binds WinTrust message signer certificate identifiers",
)

_CMSG_SIGNER_CERT_INFO_PARAM = 7
_MAX_CERTIFICATE_INFO_BYTES = 1_048_576
_MAX_CERTIFICATE_IDENTIFIER_COMPONENT_BYTES = 65_536
_MAX_CERTIFICATE_IDENTIFIER_BYTES = 1_048_576
_CERTIFICATE_IDENTIFIER_SEQUENCE_DOMAIN = (
    b"ludoweave.wintrust-message-signer-certificate-identifier/1\0"
)
_CERTIFICATE_IDENTIFIER_VALUE_DOMAIN = b"ludoweave.wintrust-certificate-identifier/1\0"


class _CRYPT_DATA_BLOB(ctypes.Structure):
    _fields_ = [
        ("cbData", wintypes.DWORD),
        ("pbData", ctypes.POINTER(wintypes.BYTE)),
    ]


class _CRYPT_ALGORITHM_IDENTIFIER(ctypes.Structure):
    _fields_ = [
        ("pszObjId", ctypes.c_char_p),
        ("Parameters", _CRYPT_DATA_BLOB),
    ]


class _CERT_INFO_PREFIX(ctypes.Structure):
    _fields_ = [
        ("dwVersion", wintypes.DWORD),
        ("SerialNumber", _CRYPT_DATA_BLOB),
        ("SignatureAlgorithm", _CRYPT_ALGORITHM_IDENTIFIER),
        ("Issuer", _CRYPT_DATA_BLOB),
    ]


@dataclass(frozen=True, slots=True)
class _CertificateIdentifier:
    issuer: bytes
    serial_number: bytes


@dataclass(frozen=True, slots=True)
class _MessageSignerCertificateIdentifierObservation:
    provider_store_count: int
    signer_count: int
    certificate_identifier_sizes: tuple[tuple[int, int], ...]
    message_certificate_identifier_sha256: tuple[str, ...]
    verified_certificate_identifier_sha256: tuple[str, ...]
    provider_certificate_identifier_sha256: tuple[str, ...]
    certificate_identifier_sequence_sha256: str


def _identifier_sha256(identifier: _CertificateIdentifier) -> str:
    digest = hashlib.sha256(_CERTIFICATE_IDENTIFIER_VALUE_DOMAIN)
    digest.update(len(identifier.issuer).to_bytes(8, "big", signed=False))
    digest.update(identifier.issuer)
    digest.update(len(identifier.serial_number).to_bytes(8, "big", signed=False))
    digest.update(identifier.serial_number)
    return digest.hexdigest()


class _AuthenticodeMessageSignerCertificateIdentifierVerifier:
    """Own WinTrust state and correlate every exact signer identifier."""

    def __init__(self) -> None:
        win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
        wintrust = win_dll("wintrust", use_last_error=True)
        crypt32 = win_dll("crypt32", use_last_error=True)

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

        get_provider_signer = cast(_NativeFunction, wintrust.WTHelperGetProvSignerFromChain)
        get_provider_signer.argtypes = [
            ctypes.c_void_p,
            wintypes.DWORD,
            wintypes.BOOL,
            wintypes.DWORD,
        ]
        get_provider_signer.restype = ctypes.POINTER(_CRYPT_PROVIDER_SGNR)

        get_provider_certificate = cast(_NativeFunction, wintrust.WTHelperGetProvCertFromChain)
        get_provider_certificate.argtypes = [
            ctypes.POINTER(_CRYPT_PROVIDER_SGNR),
            wintypes.DWORD,
        ]
        get_provider_certificate.restype = ctypes.POINTER(_CRYPT_PROVIDER_CERT)

        get_message_parameter = cast(_NativeFunction, crypt32.CryptMsgGetParam)
        get_message_parameter.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.DWORD,
            ctypes.c_void_p,
            ctypes.POINTER(wintypes.DWORD),
        ]
        get_message_parameter.restype = wintypes.BOOL

        get_and_verify_message_signer = cast(
            _NativeFunction,
            crypt32.CryptMsgGetAndVerifySigner,
        )
        get_and_verify_message_signer.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.HANDLE),
            wintypes.DWORD,
            ctypes.POINTER(ctypes.POINTER(_CERT_CONTEXT)),
            ctypes.POINTER(wintypes.DWORD),
        ]
        get_and_verify_message_signer.restype = wintypes.BOOL

        free_certificate = cast(_NativeFunction, crypt32.CertFreeCertificateContext)
        free_certificate.argtypes = [ctypes.POINTER(_CERT_CONTEXT)]
        free_certificate.restype = wintypes.BOOL

        self._win_verify_trust = verify
        self._provider_data_from_state = provider_data
        self._get_provider_signer = get_provider_signer
        self._get_provider_certificate = get_provider_certificate
        self._crypt_msg_get_param = get_message_parameter
        self._crypt_msg_get_and_verify_signer = get_and_verify_message_signer
        self._free_certificate_context = free_certificate

    def observe(
        self,
        path: Path,
        handle: int,
    ) -> _MessageSignerCertificateIdentifierObservation:
        if not path.is_absolute() or handle <= 0:
            raise RuntimeError("retained Git certificate-identifier input was invalid") from None

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
        observation: _MessageSignerCertificateIdentifierObservation | None = None
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
                    observation = self._read_identifier_sequence(trust_data)
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
            raise RuntimeError("certificate-identifier observation was unavailable") from None
        return observation

    def _read_identifier_sequence(
        self,
        trust_data: _WINTRUST_DATA,
    ) -> _MessageSignerCertificateIdentifierObservation:
        state_handle = trust_data.hWVTStateData
        if not state_handle:
            raise RuntimeError("certificate-identifier provider data was unavailable") from None
        provider_address = cast(int | None, self._provider_data_from_state(state_handle))
        if not provider_address:
            raise RuntimeError("certificate-identifier provider data was unavailable") from None
        provider = ctypes.cast(
            provider_address,
            ctypes.POINTER(_CRYPT_PROVIDER_DATA_PREFIX),
        ).contents
        if int(provider.cbStruct) < ctypes.sizeof(_CRYPT_PROVIDER_DATA_PREFIX):
            raise RuntimeError("certificate-identifier provider structure was invalid") from None

        message_handle = provider.hMsg
        if not message_handle:
            raise RuntimeError("certificate-identifier message handle was unavailable") from None
        signer_count = int(provider.csSigners)
        if not 1 <= signer_count <= _MAX_MESSAGE_SIGNERS:
            raise RuntimeError("certificate-identifier provider count was invalid") from None

        message_signer_count = wintypes.DWORD()
        count_size = wintypes.DWORD(ctypes.sizeof(message_signer_count))
        if not self._crypt_msg_get_param(
            message_handle,
            _CMSG_SIGNER_COUNT_PARAM,
            0,
            ctypes.byref(message_signer_count),
            ctypes.byref(count_size),
        ):
            raise RuntimeError("certificate-identifier signer-count query failed") from None
        if int(count_size.value) != ctypes.sizeof(message_signer_count):
            raise RuntimeError("certificate-identifier signer-count size was invalid") from None
        if int(message_signer_count.value) != signer_count:
            raise RuntimeError("message and provider signer counts differed") from None

        provider_store_count = int(provider.chStores)
        if not 0 <= provider_store_count <= _MAX_PROVIDER_STORES:
            raise RuntimeError("certificate-identifier provider-store count was invalid") from None
        provider_stores: object | None = None
        if provider_store_count:
            if not provider.pahStores:
                raise RuntimeError(
                    "certificate-identifier provider stores were unavailable"
                ) from None
            provider_stores = ctypes.cast(
                provider.pahStores,
                ctypes.POINTER(wintypes.HANDLE),
            )

        digest = hashlib.sha256(_CERTIFICATE_IDENTIFIER_SEQUENCE_DOMAIN)
        digest.update(provider_store_count.to_bytes(4, "big", signed=False))
        digest.update(signer_count.to_bytes(4, "big", signed=False))
        certificate_identifier_sizes: list[tuple[int, int]] = []
        message_hashes: list[str] = []
        verified_hashes: list[str] = []
        provider_hashes: list[str] = []
        total_identifier_size = 0
        for signer_index in range(signer_count):
            message_identifier = self._read_message_certificate_info(
                message_handle,
                signer_index,
            )
            verified_der, verified_identifier = self._verified_certificate(
                message_handle,
                provider_store_count,
                provider_stores,
                signer_index,
            )
            provider_der, provider_identifier = self._provider_certificate(
                provider_address,
                signer_index,
            )
            if provider_der != verified_der:
                raise RuntimeError(
                    f"verified and provider certificate bytes differed at index {signer_index}"
                ) from None
            if message_identifier != verified_identifier:
                raise RuntimeError(
                    f"message and verified certificate identifiers differed at index {signer_index}"
                ) from None
            if verified_identifier != provider_identifier:
                raise RuntimeError(
                    "verified and provider certificate identifiers differed at "
                    f"index {signer_index}"
                ) from None

            identifier_size = len(message_identifier.issuer) + len(message_identifier.serial_number)
            if total_identifier_size > (_MAX_CERTIFICATE_IDENTIFIER_BYTES - identifier_size):
                raise RuntimeError("certificate-identifier total was invalid") from None
            total_identifier_size += identifier_size
            certificate_identifier_sizes.append(
                (len(message_identifier.issuer), len(message_identifier.serial_number))
            )
            message_hashes.append(_identifier_sha256(message_identifier))
            verified_hashes.append(_identifier_sha256(verified_identifier))
            provider_hashes.append(_identifier_sha256(provider_identifier))
            digest.update(signer_index.to_bytes(4, "big", signed=False))
            for identifier in (
                message_identifier,
                verified_identifier,
                provider_identifier,
            ):
                digest.update(len(identifier.issuer).to_bytes(8, "big", signed=False))
                digest.update(identifier.issuer)
                digest.update(len(identifier.serial_number).to_bytes(8, "big", signed=False))
                digest.update(identifier.serial_number)

        return _MessageSignerCertificateIdentifierObservation(
            provider_store_count=provider_store_count,
            signer_count=signer_count,
            certificate_identifier_sizes=tuple(certificate_identifier_sizes),
            message_certificate_identifier_sha256=tuple(message_hashes),
            verified_certificate_identifier_sha256=tuple(verified_hashes),
            provider_certificate_identifier_sha256=tuple(provider_hashes),
            certificate_identifier_sequence_sha256=digest.hexdigest(),
        )

    def _read_message_certificate_info(
        self,
        message_handle: wintypes.HANDLE,
        signer_index: int,
    ) -> _CertificateIdentifier:
        queried_size = wintypes.DWORD()
        if not self._crypt_msg_get_param(
            message_handle,
            _CMSG_SIGNER_CERT_INFO_PARAM,
            signer_index,
            ctypes.c_void_p(),
            ctypes.byref(queried_size),
        ):
            raise RuntimeError(
                f"message signer certificate-info query failed at index {signer_index}: "
                f"{_status_hex(ctypes.get_last_error())}"
            ) from None
        info_size = int(queried_size.value)
        if not ctypes.sizeof(_CERT_INFO_PREFIX) <= info_size <= _MAX_CERTIFICATE_INFO_BYTES:
            raise RuntimeError(
                f"message signer certificate-info size was invalid at index {signer_index}"
            ) from None

        info_buffer = ctypes.create_string_buffer(info_size)
        read_size = wintypes.DWORD(info_size)
        if not self._crypt_msg_get_param(
            message_handle,
            _CMSG_SIGNER_CERT_INFO_PARAM,
            signer_index,
            info_buffer,
            ctypes.byref(read_size),
        ):
            raise RuntimeError(
                f"message signer certificate-info read failed at index {signer_index}: "
                f"{_status_hex(ctypes.get_last_error())}"
            ) from None
        actual_size = int(read_size.value)
        if not ctypes.sizeof(_CERT_INFO_PREFIX) <= actual_size <= info_size:
            raise RuntimeError(
                f"message signer certificate-info size changed at index {signer_index}"
            ) from None
        info = ctypes.cast(info_buffer, ctypes.POINTER(_CERT_INFO_PREFIX)).contents
        return self._certificate_identifier(info, "message", signer_index)

    def _verified_certificate(
        self,
        message_handle: wintypes.HANDLE,
        provider_store_count: int,
        provider_stores: object | None,
        signer_index: int,
    ) -> tuple[bytes, _CertificateIdentifier]:
        message_certificate = ctypes.POINTER(_CERT_CONTEXT)()
        requested_index = wintypes.DWORD(signer_index)
        failure: RuntimeError | None = None
        result: tuple[bytes, _CertificateIdentifier] | None = None
        try:
            if not self._crypt_msg_get_and_verify_signer(
                message_handle,
                provider_store_count,
                provider_stores,
                _CMSG_USE_SIGNER_INDEX_FLAG,
                ctypes.byref(message_certificate),
                ctypes.byref(requested_index),
            ):
                failure = RuntimeError(
                    "message signer certificate verification failed at "
                    f"index {signer_index}: {_status_hex(ctypes.get_last_error())}"
                )
            elif int(requested_index.value) != signer_index:
                failure = RuntimeError(f"message signer index changed at index {signer_index}")
            elif not message_certificate:
                failure = RuntimeError(
                    f"message signer certificate was unavailable at index {signer_index}"
                )
            else:
                context = message_certificate.contents
                encoded_size = int(context.cbCertEncoded)
                if not 1 <= encoded_size <= _MAX_CERTIFICATE_DER_BYTES:
                    failure = RuntimeError(
                        f"verified certificate size was invalid at index {signer_index}"
                    )
                elif not context.pbCertEncoded:
                    failure = RuntimeError(
                        f"verified certificate DER was unavailable at index {signer_index}"
                    )
                else:
                    result = (
                        ctypes.string_at(context.pbCertEncoded, encoded_size),
                        self._certificate_context_identifier(
                            context,
                            "verified",
                            signer_index,
                        ),
                    )
        finally:
            if (
                message_certificate
                and not self._free_certificate_context(message_certificate)
                and failure is None
            ):
                failure = RuntimeError(
                    f"message signer certificate free failed at index {signer_index}"
                )

        if failure is not None:
            raise failure from None
        if result is None:
            raise RuntimeError("verified certificate was unavailable") from None
        return result

    def _provider_certificate(
        self,
        provider_address: int,
        signer_index: int,
    ) -> tuple[bytes, _CertificateIdentifier]:
        signer = ctypes.cast(
            cast(
                int,
                self._get_provider_signer(
                    provider_address,
                    signer_index,
                    False,
                    0,
                ),
            ),
            ctypes.POINTER(_CRYPT_PROVIDER_SGNR),
        )
        if not signer:
            raise RuntimeError(f"provider signer was unavailable at index {signer_index}") from None
        chain_length = int(signer.contents.csCertChain)
        if not 1 <= chain_length <= _MAX_CERTIFICATE_CHAIN_LENGTH:
            raise RuntimeError(
                f"provider signer chain was invalid at index {signer_index}"
            ) from None
        provider_certificate = ctypes.cast(
            cast(int, self._get_provider_certificate(signer, 0)),
            ctypes.POINTER(_CRYPT_PROVIDER_CERT),
        )
        if not provider_certificate or not provider_certificate.contents.pCert:
            raise RuntimeError(
                f"provider signer certificate was unavailable at index {signer_index}"
            ) from None
        context = provider_certificate.contents.pCert.contents
        encoded_size = int(context.cbCertEncoded)
        if not 1 <= encoded_size <= _MAX_CERTIFICATE_DER_BYTES:
            raise RuntimeError(
                f"provider certificate size was invalid at index {signer_index}"
            ) from None
        if not context.pbCertEncoded:
            raise RuntimeError(
                f"provider certificate DER was unavailable at index {signer_index}"
            ) from None
        return (
            ctypes.string_at(context.pbCertEncoded, encoded_size),
            self._certificate_context_identifier(context, "provider", signer_index),
        )

    def _certificate_context_identifier(
        self,
        context: _CERT_CONTEXT,
        source: str,
        signer_index: int,
    ) -> _CertificateIdentifier:
        if not context.pCertInfo:
            raise RuntimeError(
                f"{source} certificate info was unavailable at index {signer_index}"
            ) from None
        info = ctypes.cast(
            context.pCertInfo,
            ctypes.POINTER(_CERT_INFO_PREFIX),
        ).contents
        return self._certificate_identifier(info, source, signer_index)

    @staticmethod
    def _certificate_identifier(
        info: _CERT_INFO_PREFIX,
        source: str,
        signer_index: int,
    ) -> _CertificateIdentifier:
        serial_number = info.SerialNumber
        serial_size = int(serial_number.cbData)
        if not 1 <= serial_size <= _MAX_CERTIFICATE_IDENTIFIER_COMPONENT_BYTES:
            raise RuntimeError(
                f"{source} certificate serial-number size was invalid at index {signer_index}"
            ) from None
        if not serial_number.pbData:
            raise RuntimeError(
                f"{source} certificate serial number was unavailable at index {signer_index}"
            ) from None
        issuer = info.Issuer
        issuer_size = int(issuer.cbData)
        if not 1 <= issuer_size <= _MAX_CERTIFICATE_IDENTIFIER_COMPONENT_BYTES:
            raise RuntimeError(
                f"{source} certificate issuer size was invalid at index {signer_index}"
            ) from None
        if not issuer.pbData:
            raise RuntimeError(
                f"{source} certificate issuer was unavailable at index {signer_index}"
            ) from None
        return _CertificateIdentifier(
            issuer=ctypes.string_at(issuer.pbData, issuer_size),
            serial_number=ctypes.string_at(serial_number.pbData, serial_size),
        )


def test_git_message_signer_certificate_identifiers_match_across_the_complete_m231_boundary() -> (
    None
):
    real_which = _commit_module.shutil.which
    with patch.object(
        _commit_module.shutil,
        "which",
        side_effect=real_which,
    ) as initial_lookup:
        git_executable = _commit_module._git_executable()  # pyright: ignore[reportPrivateUsage]
    assert initial_lookup.call_count == 1

    verifier = _AuthenticodeMessageSignerCertificateIdentifierVerifier()
    with _RetainedGitExecutableFile(git_executable) as retained:
        before_file = retained.snapshot()
        before_identifier = verifier.observe(git_executable, retained.handle)
        with patch.object(
            _commit_module.shutil,
            "which",
            return_value=str(git_executable),
        ) as lookup:
            _m231_module.test_git_message_signer_certificates_match_across_the_complete_m230_boundary()
        assert lookup.call_count == 1
        _verify_image_stable(before_file, retained.snapshot())
        after_identifier = verifier.observe(git_executable, retained.handle)
        assert after_identifier == before_identifier


class _FakeCertificateInfo:
    def __init__(self, identifier: tuple[bytes, bytes]) -> None:
        issuer, serial_number = identifier
        self.issuer_buffer = (wintypes.BYTE * len(issuer)).from_buffer_copy(issuer)
        self.serial_buffer = (wintypes.BYTE * len(serial_number)).from_buffer_copy(serial_number)
        self.info = _CERT_INFO_PREFIX()
        self.info.Issuer.cbData = len(issuer)
        self.info.Issuer.pbData = ctypes.cast(
            self.issuer_buffer,
            ctypes.POINTER(wintypes.BYTE),
        )
        self.info.SerialNumber.cbData = len(serial_number)
        self.info.SerialNumber.pbData = ctypes.cast(
            self.serial_buffer,
            ctypes.POINTER(wintypes.BYTE),
        )


class _FakeMessageSignerCertificateIdentifierMaterial(_FakeMessageSignerCertificateMaterial):
    def __init__(
        self,
        identifiers: tuple[tuple[bytes, bytes], ...] = (
            (b"issuer-a", b"serial-a"),
            (b"issuer-b", b"serial-b"),
        ),
        *,
        verified_identifiers: tuple[tuple[bytes, bytes], ...] | None = None,
        provider_identifiers: tuple[tuple[bytes, bytes], ...] | None = None,
        certificate_values: tuple[bytes, ...] | None = None,
        provider_values: tuple[bytes, ...] | None = None,
    ) -> None:
        selected_values = (
            tuple(f"certificate-{index}".encode() for index in range(len(identifiers)))
            if certificate_values is None
            else certificate_values
        )
        if len(selected_values) != len(identifiers):
            raise ValueError("fake certificate and identifier counts must match")
        selected_verified = identifiers if verified_identifiers is None else verified_identifiers
        selected_provider = identifiers if provider_identifiers is None else provider_identifiers
        if len(selected_verified) != len(identifiers) or len(selected_provider) != len(identifiers):
            raise ValueError("fake identifier sequences must have equal counts")
        super().__init__(selected_values, provider_values=provider_values)

        self.message_infos = [_FakeCertificateInfo(value) for value in identifiers]
        self.verified_infos = [_FakeCertificateInfo(value) for value in selected_verified]
        self.provider_infos = [_FakeCertificateInfo(value) for value in selected_provider]
        for context, info in zip(
            self.message_contexts,
            self.verified_infos,
            strict=True,
        ):
            context.pCertInfo = ctypes.addressof(info.info)
        for context, info in zip(
            self.provider_contexts,
            self.provider_infos,
            strict=True,
        ):
            context.pCertInfo = ctypes.addressof(info.info)

        self.info_query_failure_index: int | None = None
        self.info_read_failure_index: int | None = None
        self.info_query_size = ctypes.sizeof(_CERT_INFO_PREFIX) + 64
        self.info_read_size = self.info_query_size
        self.info_calls: list[tuple[int, bool]] = []

    def get_message_parameter(
        self,
        message_handle: object,
        parameter: int,
        index: int,
        output: object,
        size_pointer: object,
    ) -> bool:
        if parameter == _CMSG_SIGNER_COUNT_PARAM:
            return super().get_message_parameter(
                message_handle,
                parameter,
                index,
                output,
                size_pointer,
            )
        if parameter != _CMSG_SIGNER_CERT_INFO_PARAM:
            return False
        signer_index = int(index)
        is_read = bool(output)
        self.info_calls.append((signer_index, is_read))
        if not 0 <= signer_index < len(self.message_infos):
            return False
        size = ctypes.cast(
            cast(int, size_pointer),
            ctypes.POINTER(wintypes.DWORD),
        ).contents
        if not is_read:
            size.value = self.info_query_size
            return signer_index != self.info_query_failure_index
        size.value = self.info_read_size
        if signer_index == self.info_read_failure_index:
            return False
        ctypes.memmove(
            cast(int, output),
            ctypes.byref(self.message_infos[signer_index].info),
            ctypes.sizeof(_CERT_INFO_PREFIX),
        )
        return True


def _fake_verifier(
    wintrust: Callable[..., object],
    material: _FakeMessageSignerCertificateIdentifierMaterial,
) -> _AuthenticodeMessageSignerCertificateIdentifierVerifier:
    verifier = object.__new__(_AuthenticodeMessageSignerCertificateIdentifierVerifier)
    vars(verifier)["_win_verify_trust"] = _FakeNativeFunction(wintrust)
    vars(verifier)["_provider_data_from_state"] = _FakeNativeFunction(material.provider_data)
    vars(verifier)["_get_provider_signer"] = _FakeNativeFunction(material.get_provider_signer)
    vars(verifier)["_get_provider_certificate"] = _FakeNativeFunction(
        material.get_provider_certificate
    )
    vars(verifier)["_crypt_msg_get_param"] = _FakeNativeFunction(material.get_message_parameter)
    vars(verifier)["_crypt_msg_get_and_verify_signer"] = _FakeNativeFunction(
        material.get_and_verify_message_signer
    )
    vars(verifier)["_free_certificate_context"] = _FakeNativeFunction(material.free_certificate)
    return verifier


def _observe_material(
    material: _FakeMessageSignerCertificateIdentifierMaterial,
    *,
    wintrust: Callable[..., object] | None = None,
) -> _MessageSignerCertificateIdentifierObservation:
    selected_wintrust = wintrust or _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    return _fake_verifier(selected_wintrust, material).observe(Path("c:/git.exe"), 1)


def _expected_sequence_hash(identifiers: tuple[tuple[bytes, bytes], ...]) -> str:
    digest = hashlib.sha256(_CERTIFICATE_IDENTIFIER_SEQUENCE_DOMAIN)
    digest.update((2).to_bytes(4, "big", signed=False))
    digest.update(len(identifiers).to_bytes(4, "big", signed=False))
    for index, (issuer, serial_number) in enumerate(identifiers):
        digest.update(index.to_bytes(4, "big", signed=False))
        for _source in range(3):
            digest.update(len(issuer).to_bytes(8, "big", signed=False))
            digest.update(issuer)
            digest.update(len(serial_number).to_bytes(8, "big", signed=False))
            digest.update(serial_number)
    return digest.hexdigest()


def test_fake_certificate_identifiers_bind_every_source_and_index() -> None:
    identifiers = ((b"issuer-a", b"serial-a"), (b"issuer-b", b"serial-b"))
    material = _FakeMessageSignerCertificateIdentifierMaterial(identifiers)

    observation = _observe_material(material)

    hashes = tuple(
        _identifier_sha256(_CertificateIdentifier(issuer, serial_number))
        for issuer, serial_number in identifiers
    )
    assert observation == _MessageSignerCertificateIdentifierObservation(
        provider_store_count=2,
        signer_count=2,
        certificate_identifier_sizes=tuple(
            (len(issuer), len(serial_number)) for issuer, serial_number in identifiers
        ),
        message_certificate_identifier_sha256=hashes,
        verified_certificate_identifier_sha256=hashes,
        provider_certificate_identifier_sha256=hashes,
        certificate_identifier_sequence_sha256=_expected_sequence_hash(identifiers),
    )
    assert material.info_calls == [(0, False), (0, True), (1, False), (1, True)]
    assert material.message_calls == [
        (0, 2, _CMSG_USE_SIGNER_INDEX_FLAG),
        (1, 2, _CMSG_USE_SIGNER_INDEX_FLAG),
    ]
    assert material.provider_signer_calls == [0, 1]
    assert material.provider_certificate_calls == [(0, 0), (1, 0)]
    assert material.freed_indices == [0, 1]


def test_fake_certificate_identifier_material_rejects_mismatched_counts() -> None:
    with pytest.raises(ValueError, match="certificate and identifier counts must match"):
        _FakeMessageSignerCertificateIdentifierMaterial(
            ((b"issuer", b"serial"),),
            certificate_values=(),
        )


def test_equal_concatenated_identifier_bytes_with_different_boundaries_differ() -> None:
    first = _observe_material(_FakeMessageSignerCertificateIdentifierMaterial(((b"ab", b"c"),)))
    second = _observe_material(_FakeMessageSignerCertificateIdentifierMaterial(((b"a", b"bc"),)))

    assert first.certificate_identifier_sequence_sha256 != (
        second.certificate_identifier_sequence_sha256
    )


def test_reversed_certificate_identifier_order_hashes_differently() -> None:
    first = _observe_material(
        _FakeMessageSignerCertificateIdentifierMaterial(
            ((b"issuer-a", b"serial-a"), (b"issuer-b", b"serial-b"))
        )
    )
    second = _observe_material(
        _FakeMessageSignerCertificateIdentifierMaterial(
            ((b"issuer-b", b"serial-b"), (b"issuer-a", b"serial-a"))
        )
    )

    assert first.certificate_identifier_sequence_sha256 != (
        second.certificate_identifier_sequence_sha256
    )


def test_certificate_identifier_observation_is_detached() -> None:
    material = _FakeMessageSignerCertificateIdentifierMaterial(((b"issuer", b"serial"),))
    observation = _observe_material(material)

    material.message_infos[0].issuer_buffer[0] = ord("X")
    material.verified_infos[0].issuer_buffer[0] = ord("Y")
    material.provider_infos[0].issuer_buffer[0] = ord("Z")

    expected = _identifier_sha256(_CertificateIdentifier(b"issuer", b"serial"))
    assert observation.message_certificate_identifier_sha256 == (expected,)
    assert observation.verified_certificate_identifier_sha256 == (expected,)
    assert observation.provider_certificate_identifier_sha256 == (expected,)


@pytest.mark.parametrize(
    ("path", "handle"),
    [(Path("git.exe"), 1), (Path("c:/git.exe"), 0), (Path("c:/git.exe"), -1)],
)
def test_invalid_certificate_identifier_inputs_are_rejected(path: Path, handle: int) -> None:
    material = _FakeMessageSignerCertificateIdentifierMaterial(((b"issuer", b"serial"),))
    verifier = _fake_verifier(_FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS), material)

    with pytest.raises(RuntimeError, match="certificate-identifier input was invalid"):
        verifier.observe(path, handle)


def test_missing_provider_state_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrustWithoutState()
    material = _FakeMessageSignerCertificateIdentifierMaterial(((b"issuer", b"serial"),))

    with pytest.raises(RuntimeError, match="provider data was unavailable"):
        _fake_verifier(wintrust, material).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


@pytest.mark.parametrize(
    ("fault", "message"),
    [
        ("short-provider", "provider structure was invalid"),
        ("count-query-failure", "signer-count query failed"),
        ("count-mismatch", "signer counts differed"),
        ("missing-stores", "provider stores were unavailable"),
        ("info-query-failure", "certificate-info query failed"),
        ("empty-info-size", "certificate-info size was invalid"),
        ("oversized-info-size", "certificate-info size was invalid"),
        ("info-read-failure", "certificate-info read failed"),
        ("changed-info-size", "certificate-info size changed"),
        ("empty-message-serial", "message certificate serial-number size was invalid"),
        ("oversized-message-serial", "message certificate serial-number size was invalid"),
        ("missing-message-serial", "message certificate serial number was unavailable"),
        ("empty-message-issuer", "message certificate issuer size was invalid"),
        ("oversized-message-issuer", "message certificate issuer size was invalid"),
        ("missing-message-issuer", "message certificate issuer was unavailable"),
        ("verify-failure", "certificate verification failed"),
        ("changed-index", "signer index changed"),
        ("missing-message-certificate", "certificate was unavailable"),
        ("missing-verified-info", "verified certificate info was unavailable"),
        ("empty-verified-serial", "verified certificate serial-number size was invalid"),
        ("missing-verified-issuer", "verified certificate issuer was unavailable"),
        ("missing-provider-signer", "provider signer was unavailable"),
        ("missing-provider-certificate", "provider signer certificate was unavailable"),
        ("missing-provider-info", "provider certificate info was unavailable"),
        ("empty-provider-serial", "provider certificate serial-number size was invalid"),
        ("missing-provider-issuer", "provider certificate issuer was unavailable"),
        ("message-verified-mismatch", "message and verified certificate identifiers differed"),
        ("verified-provider-mismatch", "verified and provider certificate identifiers differed"),
        ("certificate-byte-mismatch", "verified and provider certificate bytes differed"),
    ],
)
def test_invalid_certificate_identifier_material_still_closes_and_frees(
    fault: str,
    message: str,
) -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    verified = ((b"different", b"serial"),) if fault == "message-verified-mismatch" else None
    provider = ((b"different", b"serial"),) if fault == "verified-provider-mismatch" else None
    provider_values = (b"different-certificate",) if fault == "certificate-byte-mismatch" else None
    material = _FakeMessageSignerCertificateIdentifierMaterial(
        ((b"issuer", b"serial"),),
        verified_identifiers=verified,
        provider_identifiers=provider,
        provider_values=provider_values,
    )
    if fault == "short-provider":
        material.provider.cbStruct = ctypes.sizeof(_CRYPT_PROVIDER_DATA_PREFIX) - 1
    elif fault == "count-query-failure":
        material.count_query_succeeds = False
    elif fault == "count-mismatch":
        material.message_signer_count = 2
    elif fault == "missing-stores":
        material.provider.pahStores = None
    elif fault == "info-query-failure":
        material.info_query_failure_index = 0
    elif fault == "empty-info-size":
        material.info_query_size = 0
    elif fault == "oversized-info-size":
        material.info_query_size = _MAX_CERTIFICATE_INFO_BYTES + 1
    elif fault == "info-read-failure":
        material.info_read_failure_index = 0
    elif fault == "changed-info-size":
        material.info_read_size = material.info_query_size + 1
    elif fault == "empty-message-serial":
        material.message_infos[0].info.SerialNumber.cbData = 0
    elif fault == "oversized-message-serial":
        material.message_infos[0].info.SerialNumber.cbData = (
            _MAX_CERTIFICATE_IDENTIFIER_COMPONENT_BYTES + 1
        )
    elif fault == "missing-message-serial":
        material.message_infos[0].info.SerialNumber.pbData = ctypes.POINTER(wintypes.BYTE)()
    elif fault == "empty-message-issuer":
        material.message_infos[0].info.Issuer.cbData = 0
    elif fault == "oversized-message-issuer":
        material.message_infos[0].info.Issuer.cbData = (
            _MAX_CERTIFICATE_IDENTIFIER_COMPONENT_BYTES + 1
        )
    elif fault == "missing-message-issuer":
        material.message_infos[0].info.Issuer.pbData = ctypes.POINTER(wintypes.BYTE)()
    elif fault == "verify-failure":
        material.verify_failure_index = 0
    elif fault == "changed-index":
        material.returned_index[0] = 1
    elif fault == "missing-message-certificate":
        material.missing_message_context_index = 0
    elif fault == "missing-verified-info":
        material.message_contexts[0].pCertInfo = None
    elif fault == "empty-verified-serial":
        material.verified_infos[0].info.SerialNumber.cbData = 0
    elif fault == "missing-verified-issuer":
        material.verified_infos[0].info.Issuer.pbData = ctypes.POINTER(wintypes.BYTE)()
    elif fault == "missing-provider-signer":
        material.missing_provider_signer_index = 0
    elif fault == "missing-provider-certificate":
        material.missing_provider_certificate_index = 0
    elif fault == "missing-provider-info":
        material.provider_contexts[0].pCertInfo = None
    elif fault == "empty-provider-serial":
        material.provider_infos[0].info.SerialNumber.cbData = 0
    elif fault == "missing-provider-issuer":
        material.provider_infos[0].info.Issuer.pbData = ctypes.POINTER(wintypes.BYTE)()
    elif fault not in {
        "message-verified-mismatch",
        "verified-provider-mismatch",
        "certificate-byte-mismatch",
    }:
        raise AssertionError(f"unexpected certificate-identifier fault: {fault}")

    with pytest.raises(RuntimeError, match=message):
        _fake_verifier(wintrust, material).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]
    no_free_faults = {
        "short-provider",
        "count-query-failure",
        "count-mismatch",
        "missing-stores",
        "info-query-failure",
        "empty-info-size",
        "oversized-info-size",
        "info-read-failure",
        "changed-info-size",
        "empty-message-serial",
        "oversized-message-serial",
        "missing-message-serial",
        "empty-message-issuer",
        "oversized-message-issuer",
        "missing-message-issuer",
        "verify-failure",
        "missing-message-certificate",
    }
    if fault in no_free_faults:
        assert material.freed_indices == []
    else:
        assert material.freed_indices == [0]


def test_certificate_identifier_total_is_bounded() -> None:
    component = b"x" * _MAX_CERTIFICATE_IDENTIFIER_COMPONENT_BYTES
    identifiers = tuple((component, component) for _index in range(9))
    material = _FakeMessageSignerCertificateIdentifierMaterial(identifiers)

    with pytest.raises(RuntimeError, match="certificate-identifier total was invalid"):
        _observe_material(material)

    assert material.freed_indices == list(range(9))


def test_message_signer_certificate_free_failure_is_reported() -> None:
    material = _FakeMessageSignerCertificateIdentifierMaterial(((b"issuer", b"serial"),))
    material.free_failure_index = 0

    with pytest.raises(RuntimeError, match="certificate free failed"):
        _observe_material(material)

    assert material.freed_indices == [0]


def test_primary_identifier_failure_precedes_certificate_free_failure() -> None:
    material = _FakeMessageSignerCertificateIdentifierMaterial(((b"issuer", b"serial"),))
    material.message_contexts[0].pCertInfo = None
    material.free_failure_index = 0

    with pytest.raises(RuntimeError, match="verified certificate info was unavailable"):
        _observe_material(material)

    assert material.freed_indices == [0]


def test_rejected_trust_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrust(_signed_status(_TRUST_E_BAD_DIGEST), _ERROR_SUCCESS)
    material = _FakeMessageSignerCertificateIdentifierMaterial(((b"issuer", b"serial"),))

    with pytest.raises(RuntimeError, match="0x80096010"):
        _fake_verifier(wintrust, material).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_state_close_failure_after_identifier_observation_is_reported() -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _signed_status(_TRUST_E_BAD_DIGEST))
    material = _FakeMessageSignerCertificateIdentifierMaterial(((b"issuer", b"serial"),))

    with pytest.raises(RuntimeError, match="trust provider state close failed"):
        _fake_verifier(wintrust, material).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]
