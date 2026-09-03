"""Correlate WinTrust message and provider signer certificates around M230."""

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
    test_windows_contained_source_access_source_commit_git_signed_message_signer_info_binding_probe as _m230_module,
)
from tests.integration.test_windows_contained_source_access_source_commit_git_file_retention_probe import (
    _RetainedGitExecutableFile,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_contained_source_access_source_commit_git_signed_message_signer_info_binding_probe import (
    _CRYPT_PROVIDER_DATA_PREFIX,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_contained_source_access_source_commit_git_signer_certificate_binding_probe import (
    _CERT_CONTEXT,  # pyright: ignore[reportPrivateUsage]
    _CRYPT_PROVIDER_CERT,  # pyright: ignore[reportPrivateUsage]
    _CRYPT_PROVIDER_SGNR,  # pyright: ignore[reportPrivateUsage]
    _ERROR_SUCCESS,  # pyright: ignore[reportPrivateUsage]
    _MAX_CERTIFICATE_CHAIN_LENGTH,  # pyright: ignore[reportPrivateUsage]
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
    reason="M231 correlates WinTrust message and provider signer certificates",
)

_CMSG_SIGNER_COUNT_PARAM = 5
_CMSG_USE_SIGNER_INDEX_FLAG = 0x4
_MAX_MESSAGE_SIGNERS = 16
_MAX_PROVIDER_STORES = 32
_MAX_CERTIFICATE_DER_BYTES = 1_048_576
_MAX_MESSAGE_SIGNER_CERTIFICATE_BYTES = 4_194_304
_MESSAGE_SIGNER_CERTIFICATE_SEQUENCE_DOMAIN = b"ludoweave.wintrust-message-signer-certificate/1\0"


@dataclass(frozen=True, slots=True)
class _MessageSignerCertificateObservation:
    provider_store_count: int
    signer_count: int
    certificate_sizes: tuple[int, ...]
    message_certificate_sha256: tuple[str, ...]
    provider_certificate_sha256: tuple[str, ...]
    message_signer_certificate_sequence_sha256: str


class _AuthenticodeMessageSignerCertificateVerifier:
    """Own WinTrust state and correlate every verified message signer."""

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

        get_and_verify_message_signer = cast(_NativeFunction, crypt32.CryptMsgGetAndVerifySigner)
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

    def observe(self, path: Path, handle: int) -> _MessageSignerCertificateObservation:
        if not path.is_absolute() or handle <= 0:
            raise RuntimeError("retained Git message-signer input was invalid") from None

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
        observation: _MessageSignerCertificateObservation | None = None
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
                    observation = self._read_certificate_sequence(trust_data)
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
            raise RuntimeError("message-signer observation was unavailable") from None
        return observation

    def _read_certificate_sequence(
        self, trust_data: _WINTRUST_DATA
    ) -> _MessageSignerCertificateObservation:
        state_handle = trust_data.hWVTStateData
        if not state_handle:
            raise RuntimeError("message-signer provider data was unavailable") from None
        provider_address = cast(int | None, self._provider_data_from_state(state_handle))
        if not provider_address:
            raise RuntimeError("message-signer provider data was unavailable") from None
        provider = ctypes.cast(
            provider_address,
            ctypes.POINTER(_CRYPT_PROVIDER_DATA_PREFIX),
        ).contents
        if int(provider.cbStruct) < ctypes.sizeof(_CRYPT_PROVIDER_DATA_PREFIX):
            raise RuntimeError("message-signer provider structure was invalid") from None

        message_handle = provider.hMsg
        if not message_handle:
            raise RuntimeError("message-signer message handle was unavailable") from None
        signer_count = int(provider.csSigners)
        if not 1 <= signer_count <= _MAX_MESSAGE_SIGNERS:
            raise RuntimeError("message-signer provider count was invalid") from None

        message_signer_count = wintypes.DWORD()
        count_size = wintypes.DWORD(ctypes.sizeof(message_signer_count))
        if not self._crypt_msg_get_param(
            message_handle,
            _CMSG_SIGNER_COUNT_PARAM,
            0,
            ctypes.byref(message_signer_count),
            ctypes.byref(count_size),
        ):
            raise RuntimeError("message-signer count query failed") from None
        if int(count_size.value) != ctypes.sizeof(message_signer_count):
            raise RuntimeError("message-signer count size was invalid") from None
        if int(message_signer_count.value) != signer_count:
            raise RuntimeError("message and provider signer counts differed") from None

        provider_store_count = int(provider.chStores)
        if not 0 <= provider_store_count <= _MAX_PROVIDER_STORES:
            raise RuntimeError("message-signer provider-store count was invalid") from None
        provider_stores: object | None = None
        if provider_store_count:
            if not provider.pahStores:
                raise RuntimeError("message-signer provider stores were unavailable") from None
            provider_stores = ctypes.cast(
                provider.pahStores,
                ctypes.POINTER(wintypes.HANDLE),
            )

        digest = hashlib.sha256(_MESSAGE_SIGNER_CERTIFICATE_SEQUENCE_DOMAIN)
        digest.update(provider_store_count.to_bytes(4, "big", signed=False))
        digest.update(signer_count.to_bytes(4, "big", signed=False))
        certificate_sizes: list[int] = []
        message_certificate_hashes: list[str] = []
        provider_certificate_hashes: list[str] = []
        total_encoded_size = 0
        for signer_index in range(signer_count):
            message_der = self._verified_message_certificate_der(
                message_handle,
                provider_store_count,
                provider_stores,
                signer_index,
            )
            if total_encoded_size > (_MAX_MESSAGE_SIGNER_CERTIFICATE_BYTES - len(message_der)):
                raise RuntimeError("message-signer certificate total was invalid") from None
            provider_der = self._provider_certificate_der(
                provider_address,
                signer_index,
            )
            if provider_der != message_der:
                raise RuntimeError("message and provider signer certificates differed") from None
            total_encoded_size += len(message_der)
            certificate_sizes.append(len(message_der))
            message_certificate_hashes.append(hashlib.sha256(message_der).hexdigest())
            provider_certificate_hashes.append(hashlib.sha256(provider_der).hexdigest())
            digest.update(signer_index.to_bytes(4, "big", signed=False))
            digest.update(len(message_der).to_bytes(8, "big", signed=False))
            digest.update(message_der)
            digest.update(provider_der)

        return _MessageSignerCertificateObservation(
            provider_store_count=provider_store_count,
            signer_count=signer_count,
            certificate_sizes=tuple(certificate_sizes),
            message_certificate_sha256=tuple(message_certificate_hashes),
            provider_certificate_sha256=tuple(provider_certificate_hashes),
            message_signer_certificate_sequence_sha256=digest.hexdigest(),
        )

    def _verified_message_certificate_der(
        self,
        message_handle: wintypes.HANDLE,
        provider_store_count: int,
        provider_stores: object | None,
        signer_index: int,
    ) -> bytes:
        message_certificate = ctypes.POINTER(_CERT_CONTEXT)()
        requested_index = wintypes.DWORD(signer_index)
        failure: RuntimeError | None = None
        message_der: bytes | None = None
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
                encoded_size = int(message_certificate.contents.cbCertEncoded)
                if not 1 <= encoded_size <= _MAX_CERTIFICATE_DER_BYTES:
                    failure = RuntimeError(
                        f"message signer certificate size was invalid at index {signer_index}"
                    )
                elif not message_certificate.contents.pbCertEncoded:
                    failure = RuntimeError(
                        f"message signer certificate DER was unavailable at index {signer_index}"
                    )
                else:
                    message_der = ctypes.string_at(
                        message_certificate.contents.pbCertEncoded,
                        encoded_size,
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
        if message_der is None:
            raise RuntimeError("message signer certificate was unavailable") from None
        return message_der

    def _provider_certificate_der(
        self,
        provider_address: int,
        signer_index: int,
    ) -> bytes:
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
        certificate = provider_certificate.contents.pCert.contents
        encoded_size = int(certificate.cbCertEncoded)
        if not 1 <= encoded_size <= _MAX_CERTIFICATE_DER_BYTES:
            raise RuntimeError(
                f"provider signer certificate size was invalid at index {signer_index}"
            ) from None
        if not certificate.pbCertEncoded:
            raise RuntimeError(
                f"provider signer certificate DER was unavailable at index {signer_index}"
            ) from None
        return ctypes.string_at(certificate.pbCertEncoded, encoded_size)


def test_git_message_signer_certificates_match_across_the_complete_m230_boundary() -> None:
    real_which = _commit_module.shutil.which
    with patch.object(
        _commit_module.shutil,
        "which",
        side_effect=real_which,
    ) as initial_lookup:
        git_executable = _commit_module._git_executable()  # pyright: ignore[reportPrivateUsage]
    assert initial_lookup.call_count == 1

    verifier = _AuthenticodeMessageSignerCertificateVerifier()
    with _RetainedGitExecutableFile(git_executable) as retained:
        before_file = retained.snapshot()
        before_certificate = verifier.observe(git_executable, retained.handle)
        with patch.object(
            _commit_module.shutil,
            "which",
            return_value=str(git_executable),
        ) as lookup:
            _m230_module.test_git_signed_message_signer_info_matches_across_the_complete_m229_boundary()
        assert lookup.call_count == 1
        _verify_image_stable(before_file, retained.snapshot())
        after_certificate = verifier.observe(git_executable, retained.handle)
        assert after_certificate == before_certificate


class _FakeMessageSignerCertificateMaterial:
    def __init__(
        self,
        message_values: tuple[bytes, ...] = (b"certificate-a", b"certificate-b"),
        *,
        provider_values: tuple[bytes, ...] | None = None,
    ) -> None:
        selected_provider_values = message_values if provider_values is None else provider_values
        if len(selected_provider_values) != len(message_values):
            raise ValueError("fake signer sequences must have equal counts")
        self.message_values = message_values
        self.provider_values = selected_provider_values
        self.provider = _CRYPT_PROVIDER_DATA_PREFIX()
        self.provider.cbStruct = ctypes.sizeof(_CRYPT_PROVIDER_DATA_PREFIX)
        self.provider.hMsg = wintypes.HANDLE(1)
        self.provider.csSigners = len(message_values)
        self.store_handles = (wintypes.HANDLE * 2)(wintypes.HANDLE(11), wintypes.HANDLE(12))
        self.provider.chStores = len(self.store_handles)
        self.provider.pahStores = ctypes.cast(self.store_handles, ctypes.c_void_p)
        self.message_signer_count = len(message_values)
        self.count_size = ctypes.sizeof(wintypes.DWORD())
        self.count_query_succeeds = True

        self.message_buffers = [
            (wintypes.BYTE * len(value)).from_buffer_copy(value) for value in message_values
        ]
        self.provider_buffers = [
            (wintypes.BYTE * len(value)).from_buffer_copy(value)
            for value in selected_provider_values
        ]
        self.message_contexts = [
            self._certificate_context(buffer, len(value))
            for buffer, value in zip(self.message_buffers, message_values, strict=True)
        ]
        self.provider_contexts = [
            self._certificate_context(buffer, len(value))
            for buffer, value in zip(
                self.provider_buffers,
                selected_provider_values,
                strict=True,
            )
        ]
        self.provider_certificates: list[_CRYPT_PROVIDER_CERT] = []
        self.provider_signers: list[_CRYPT_PROVIDER_SGNR] = []
        for context in self.provider_contexts:
            provider_certificate = _CRYPT_PROVIDER_CERT()
            provider_certificate.cbStruct = ctypes.sizeof(_CRYPT_PROVIDER_CERT)
            provider_certificate.pCert = ctypes.pointer(context)
            self.provider_certificates.append(provider_certificate)
            provider_signer = _CRYPT_PROVIDER_SGNR()
            provider_signer.cbStruct = ctypes.sizeof(_CRYPT_PROVIDER_SGNR)
            provider_signer.csCertChain = 1
            provider_signer.pasCertChain = ctypes.pointer(provider_certificate)
            self.provider_signers.append(provider_signer)

        self.verify_failure_index: int | None = None
        self.verify_failure_with_context = False
        self.returned_index: dict[int, int] = {}
        self.missing_message_context_index: int | None = None
        self.missing_provider_signer_index: int | None = None
        self.missing_provider_certificate_index: int | None = None
        self.free_failure_index: int | None = None
        self.message_calls: list[tuple[int, int, int]] = []
        self.provider_signer_calls: list[int] = []
        self.provider_certificate_calls: list[tuple[int, int]] = []
        self.freed_indices: list[int] = []

    @staticmethod
    def _certificate_context(
        buffer: ctypes.Array[wintypes.BYTE],
        size: int,
    ) -> _CERT_CONTEXT:
        context = _CERT_CONTEXT()
        context.pbCertEncoded = ctypes.cast(buffer, ctypes.POINTER(wintypes.BYTE))
        context.cbCertEncoded = size
        return context

    def provider_data(self, *_arguments: object) -> int:
        return ctypes.addressof(self.provider)

    def get_message_parameter(
        self,
        _message_handle: object,
        parameter: int,
        _index: int,
        output: object,
        size_pointer: object,
    ) -> bool:
        if parameter != _CMSG_SIGNER_COUNT_PARAM or not self.count_query_succeeds:
            return False
        ctypes.cast(
            cast(int, output), ctypes.POINTER(wintypes.DWORD)
        ).contents.value = self.message_signer_count
        ctypes.cast(
            cast(int, size_pointer), ctypes.POINTER(wintypes.DWORD)
        ).contents.value = self.count_size
        return True

    def get_and_verify_message_signer(
        self,
        _message_handle: object,
        store_count: int,
        _stores: object,
        flags: int,
        certificate_output: object,
        index_pointer: object,
    ) -> bool:
        index = ctypes.cast(cast(int, index_pointer), ctypes.POINTER(wintypes.DWORD)).contents
        requested = int(index.value)
        self.message_calls.append((requested, int(store_count), int(flags)))
        if requested == self.verify_failure_index:
            if self.verify_failure_with_context:
                ctypes.cast(
                    cast(int, certificate_output),
                    ctypes.POINTER(ctypes.POINTER(_CERT_CONTEXT)),
                )[0] = ctypes.pointer(self.message_contexts[requested])
            return False
        index.value = self.returned_index.get(requested, requested)
        if requested == self.missing_message_context_index:
            return True
        ctypes.cast(
            cast(int, certificate_output),
            ctypes.POINTER(ctypes.POINTER(_CERT_CONTEXT)),
        )[0] = ctypes.pointer(self.message_contexts[requested])
        return True

    def free_certificate(self, context: object) -> bool:
        certificate = ctypes.cast(cast(int, context), ctypes.POINTER(_CERT_CONTEXT))
        address = ctypes.addressof(certificate.contents)
        index = next(
            index
            for index, candidate in enumerate(self.message_contexts)
            if ctypes.addressof(candidate) == address
        )
        self.freed_indices.append(index)
        return index != self.free_failure_index

    def get_provider_signer(
        self,
        _provider_address: object,
        index: int,
        _counter_signer: object,
        _counter_index: object,
    ) -> object | None:
        self.provider_signer_calls.append(int(index))
        if int(index) == self.missing_provider_signer_index:
            return None
        return ctypes.pointer(self.provider_signers[int(index)])

    def get_provider_certificate(
        self,
        signer: object,
        certificate_index: int,
    ) -> object | None:
        signer_pointer = ctypes.cast(cast(int, signer), ctypes.POINTER(_CRYPT_PROVIDER_SGNR))
        signer_address = ctypes.addressof(signer_pointer.contents)
        signer_index = next(
            index
            for index, candidate in enumerate(self.provider_signers)
            if ctypes.addressof(candidate) == signer_address
        )
        self.provider_certificate_calls.append((signer_index, int(certificate_index)))
        if signer_index == self.missing_provider_certificate_index:
            return None
        return ctypes.pointer(self.provider_certificates[signer_index])


class _FakeWinTrustWithoutState:
    def __init__(self) -> None:
        self.calls: list[int] = []

    def __call__(self, *_arguments: object) -> int:
        data_pointer = ctypes.cast(
            _arguments[2],  # pyright: ignore[reportArgumentType]
            ctypes.POINTER(_WINTRUST_DATA),
        )
        action = int(data_pointer.contents.dwStateAction)
        self.calls.append(action)
        if action in (_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE):
            return _ERROR_SUCCESS
        raise AssertionError(f"unexpected trust state action: {action}")


def _fake_verifier(
    wintrust: Callable[..., object],
    material: _FakeMessageSignerCertificateMaterial,
) -> _AuthenticodeMessageSignerCertificateVerifier:
    verifier = object.__new__(_AuthenticodeMessageSignerCertificateVerifier)
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
    material: _FakeMessageSignerCertificateMaterial,
    *,
    wintrust: Callable[..., object] | None = None,
) -> _MessageSignerCertificateObservation:
    selected_wintrust = wintrust or _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    return _fake_verifier(selected_wintrust, material).observe(Path("c:/git.exe"), 1)


def _expected_sequence_hash(values: tuple[bytes, ...], store_count: int = 2) -> str:
    digest = hashlib.sha256(_MESSAGE_SIGNER_CERTIFICATE_SEQUENCE_DOMAIN)
    digest.update(store_count.to_bytes(4, "big", signed=False))
    digest.update(len(values).to_bytes(4, "big", signed=False))
    for index, value in enumerate(values):
        digest.update(index.to_bytes(4, "big", signed=False))
        digest.update(len(value).to_bytes(8, "big", signed=False))
        digest.update(value)
        digest.update(value)
    return digest.hexdigest()


def test_fake_message_signer_certificates_bind_the_complete_sequence() -> None:
    values = (b"certificate-a", b"certificate-b")
    material = _FakeMessageSignerCertificateMaterial(values)

    observation = _observe_material(material)

    hashes = tuple(hashlib.sha256(value).hexdigest() for value in values)
    assert observation == _MessageSignerCertificateObservation(
        provider_store_count=2,
        signer_count=2,
        certificate_sizes=tuple(len(value) for value in values),
        message_certificate_sha256=hashes,
        provider_certificate_sha256=hashes,
        message_signer_certificate_sequence_sha256=_expected_sequence_hash(values),
    )
    assert material.message_calls == [
        (0, 2, _CMSG_USE_SIGNER_INDEX_FLAG),
        (1, 2, _CMSG_USE_SIGNER_INDEX_FLAG),
    ]
    assert material.provider_signer_calls == [0, 1]
    assert material.provider_certificate_calls == [(0, 0), (1, 0)]
    assert material.freed_indices == [0, 1]


def test_fake_message_signer_certificate_material_rejects_mismatched_counts() -> None:
    with pytest.raises(ValueError, match="equal counts"):
        _FakeMessageSignerCertificateMaterial(
            (b"certificate",),
            provider_values=(),
        )


def test_equal_concatenated_certificate_bytes_with_different_boundaries_differ() -> None:
    first = _observe_material(_FakeMessageSignerCertificateMaterial((b"ab", b"c")))
    second = _observe_material(_FakeMessageSignerCertificateMaterial((b"a", b"bc")))

    assert first.message_signer_certificate_sequence_sha256 != (
        second.message_signer_certificate_sequence_sha256
    )


def test_reversed_message_signer_certificate_order_hashes_differently() -> None:
    first = _observe_material(_FakeMessageSignerCertificateMaterial((b"first", b"second")))
    second = _observe_material(_FakeMessageSignerCertificateMaterial((b"second", b"first")))

    assert first.message_signer_certificate_sequence_sha256 != (
        second.message_signer_certificate_sequence_sha256
    )


def test_message_signer_certificate_observation_is_detached() -> None:
    material = _FakeMessageSignerCertificateMaterial((b"certificate",))
    observation = _observe_material(material)

    material.message_buffers[0][0] = ord("X")
    material.provider_buffers[0][0] = ord("Y")

    expected = hashlib.sha256(b"certificate").hexdigest()
    assert observation.message_certificate_sha256 == (expected,)
    assert observation.provider_certificate_sha256 == (expected,)


@pytest.mark.parametrize(
    ("path", "handle"),
    [(Path("git.exe"), 1), (Path("c:/git.exe"), 0), (Path("c:/git.exe"), -1)],
)
def test_invalid_message_signer_inputs_are_rejected(path: Path, handle: int) -> None:
    material = _FakeMessageSignerCertificateMaterial((b"certificate",))
    verifier = _fake_verifier(_FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS), material)

    with pytest.raises(RuntimeError, match="message-signer input was invalid"):
        verifier.observe(path, handle)


def test_missing_provider_state_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrustWithoutState()
    material = _FakeMessageSignerCertificateMaterial((b"certificate",))

    with pytest.raises(RuntimeError, match="provider data was unavailable"):
        _fake_verifier(wintrust, material).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


@pytest.mark.parametrize(
    ("fault", "message"),
    [
        ("short-provider", "provider structure was invalid"),
        ("missing-message", "message handle was unavailable"),
        ("empty-provider-count", "provider count was invalid"),
        ("oversized-provider-count", "provider count was invalid"),
        ("count-query-failure", "count query failed"),
        ("count-size", "count size was invalid"),
        ("count-mismatch", "signer counts differed"),
        ("oversized-store-count", "provider-store count was invalid"),
        ("missing-stores", "provider stores were unavailable"),
        ("verify-failure", "certificate verification failed"),
        ("changed-index", "signer index changed"),
        ("missing-message-certificate", "certificate was unavailable"),
        ("empty-message-certificate", "certificate size was invalid"),
        ("oversized-message-certificate", "certificate size was invalid"),
        ("missing-message-der", "certificate DER was unavailable"),
        ("missing-provider-signer", "provider signer was unavailable"),
        ("empty-provider-chain", "provider signer chain was invalid"),
        ("oversized-provider-chain", "provider signer chain was invalid"),
        ("missing-provider-certificate", "provider signer certificate was unavailable"),
        ("empty-provider-certificate", "provider signer certificate size was invalid"),
        ("oversized-provider-certificate", "provider signer certificate size was invalid"),
        ("missing-provider-der", "provider signer certificate DER was unavailable"),
        ("certificate-mismatch", "signer certificates differed"),
    ],
)
def test_invalid_message_signer_material_still_closes_and_frees(
    fault: str,
    message: str,
) -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    provider_values = (b"different",) if fault == "certificate-mismatch" else None
    material = _FakeMessageSignerCertificateMaterial(
        (b"certificate",),
        provider_values=provider_values,
    )
    if fault == "short-provider":
        material.provider.cbStruct = ctypes.sizeof(_CRYPT_PROVIDER_DATA_PREFIX) - 1
    elif fault == "missing-message":
        material.provider.hMsg = wintypes.HANDLE()
    elif fault == "empty-provider-count":
        material.provider.csSigners = 0
    elif fault == "oversized-provider-count":
        material.provider.csSigners = _MAX_MESSAGE_SIGNERS + 1
    elif fault == "count-query-failure":
        material.count_query_succeeds = False
    elif fault == "count-size":
        material.count_size = 0
    elif fault == "count-mismatch":
        material.message_signer_count = 2
    elif fault == "oversized-store-count":
        material.provider.chStores = _MAX_PROVIDER_STORES + 1
    elif fault == "missing-stores":
        material.provider.pahStores = None
    elif fault == "verify-failure":
        material.verify_failure_index = 0
    elif fault == "changed-index":
        material.returned_index[0] = 1
    elif fault == "missing-message-certificate":
        material.missing_message_context_index = 0
    elif fault == "empty-message-certificate":
        material.message_contexts[0].cbCertEncoded = 0
    elif fault == "oversized-message-certificate":
        material.message_contexts[0].cbCertEncoded = _MAX_CERTIFICATE_DER_BYTES + 1
    elif fault == "missing-message-der":
        material.message_contexts[0].pbCertEncoded = ctypes.POINTER(wintypes.BYTE)()
    elif fault == "missing-provider-signer":
        material.missing_provider_signer_index = 0
    elif fault == "empty-provider-chain":
        material.provider_signers[0].csCertChain = 0
    elif fault == "oversized-provider-chain":
        material.provider_signers[0].csCertChain = _MAX_CERTIFICATE_CHAIN_LENGTH + 1
    elif fault == "missing-provider-certificate":
        material.missing_provider_certificate_index = 0
    elif fault == "empty-provider-certificate":
        material.provider_contexts[0].cbCertEncoded = 0
    elif fault == "oversized-provider-certificate":
        material.provider_contexts[0].cbCertEncoded = _MAX_CERTIFICATE_DER_BYTES + 1
    elif fault == "missing-provider-der":
        material.provider_contexts[0].pbCertEncoded = ctypes.POINTER(wintypes.BYTE)()
    elif fault != "certificate-mismatch":
        raise AssertionError(f"unexpected message-signer fault: {fault}")

    with pytest.raises(RuntimeError, match=message):
        _fake_verifier(wintrust, material).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]
    if fault in {
        "verify-failure",
        "short-provider",
        "missing-message",
        "empty-provider-count",
        "oversized-provider-count",
        "count-query-failure",
        "count-size",
        "count-mismatch",
        "oversized-store-count",
        "missing-stores",
        "missing-message-certificate",
    }:
        assert material.freed_indices == []
    else:
        assert material.freed_indices == [0]


def test_failed_message_verification_frees_a_returned_context() -> None:
    material = _FakeMessageSignerCertificateMaterial((b"certificate",))
    material.verify_failure_index = 0
    material.verify_failure_with_context = True

    with pytest.raises(RuntimeError, match="certificate verification failed"):
        _observe_material(material)

    assert material.freed_indices == [0]


def test_message_signer_certificate_total_is_bounded() -> None:
    value = b"x" * _MAX_CERTIFICATE_DER_BYTES
    material = _FakeMessageSignerCertificateMaterial((value,) * 5)

    with pytest.raises(RuntimeError, match="certificate total was invalid"):
        _observe_material(material)

    assert material.freed_indices == [0, 1, 2, 3, 4]


def test_message_signer_certificate_free_failure_is_reported() -> None:
    material = _FakeMessageSignerCertificateMaterial((b"certificate",))
    material.free_failure_index = 0

    with pytest.raises(RuntimeError, match="certificate free failed"):
        _observe_material(material)

    assert material.freed_indices == [0]


def test_primary_message_failure_precedes_certificate_free_failure() -> None:
    material = _FakeMessageSignerCertificateMaterial((b"certificate",))
    material.message_contexts[0].cbCertEncoded = 0
    material.free_failure_index = 0

    with pytest.raises(RuntimeError, match="certificate size was invalid"):
        _observe_material(material)

    assert material.freed_indices == [0]


def test_rejected_trust_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrust(_signed_status(_TRUST_E_BAD_DIGEST), _ERROR_SUCCESS)
    material = _FakeMessageSignerCertificateMaterial((b"certificate",))

    with pytest.raises(RuntimeError, match="0x80096010"):
        _fake_verifier(wintrust, material).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_state_close_failure_after_certificate_observation_is_reported() -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _signed_status(_TRUST_E_BAD_DIGEST))
    material = _FakeMessageSignerCertificateMaterial((b"certificate",))

    with pytest.raises(RuntimeError, match="trust provider state close failed"):
        _fake_verifier(wintrust, material).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]
