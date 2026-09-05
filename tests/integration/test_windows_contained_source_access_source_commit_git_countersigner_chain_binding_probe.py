"""Exercise a bounded WinTrust countersigner-chain observation around M228."""

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
    test_windows_contained_source_access_source_commit_git_provider_chain_binding_probe as _m228_module,
)
from tests.integration.test_windows_contained_source_access_source_commit_git_file_retention_probe import (
    _RetainedGitExecutableFile,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_contained_source_access_source_commit_git_provider_chain_binding_probe import (
    _MAX_PROVIDER_CHAIN_DER_BYTES,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_contained_source_access_source_commit_git_signer_certificate_binding_probe import (
    _CERT_CONTEXT,  # pyright: ignore[reportPrivateUsage]
    _CRYPT_PROVIDER_CERT,  # pyright: ignore[reportPrivateUsage]
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
    reason="M229 binds the retained Git WinTrust countersigner chains",
)

_MAX_COUNTER_SIGNERS = 16
_MAX_COUNTER_SIGNER_DER_BYTES = 8_388_608
_COUNTER_SIGNER_CHAIN_DOMAIN = b"ludoweave.wintrust-countersigner-chain/1\0"
_COUNTER_SIGNER_SEQUENCE_DOMAIN = b"ludoweave.wintrust-countersigner-sequence/1\0"


class _CRYPT_PROVIDER_SGNR_COMPLETE(ctypes.Structure):
    pass


_CRYPT_PROVIDER_SGNR_COMPLETE._fields_ = [  # pyright: ignore[reportAttributeAccessIssue]
    ("cbStruct", wintypes.DWORD),
    ("sftVerifyAsOf", wintypes.FILETIME),
    ("csCertChain", wintypes.DWORD),
    ("pasCertChain", ctypes.POINTER(_CRYPT_PROVIDER_CERT)),
    ("dwSignerType", wintypes.DWORD),
    ("psSigner", ctypes.c_void_p),
    ("dwError", wintypes.DWORD),
    ("csCounterSigners", wintypes.DWORD),
    ("pasCounterSigners", ctypes.POINTER(_CRYPT_PROVIDER_SGNR_COMPLETE)),
    ("pChainContext", ctypes.c_void_p),
]


@dataclass(frozen=True, slots=True)
class _CounterSignerChainObservation:
    signer_type: int
    provider_error: int
    verify_as_of_filetime: int
    chain_length: int
    encoded_sizes: tuple[int, ...]
    certificate_sha256: tuple[str, ...]
    provider_chain_sha256: str


@dataclass(frozen=True, slots=True)
class _ProviderCounterSignerSequenceObservation:
    counter_signer_count: int
    counter_signers: tuple[_CounterSignerChainObservation, ...]
    counter_signer_sequence_sha256: str


class _AuthenticodeCounterSignerChainVerifier:
    """Own trust verification and detach every indexed countersigner chain."""

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
        get_signer.restype = ctypes.POINTER(_CRYPT_PROVIDER_SGNR_COMPLETE)

        get_certificate = cast(_NativeFunction, wintrust.WTHelperGetProvCertFromChain)
        get_certificate.argtypes = [
            ctypes.POINTER(_CRYPT_PROVIDER_SGNR_COMPLETE),
            wintypes.DWORD,
        ]
        get_certificate.restype = ctypes.POINTER(_CRYPT_PROVIDER_CERT)

        self._win_verify_trust = verify
        self._provider_data_from_state = provider_data
        self._get_signer_from_chain = get_signer
        self._get_certificate_from_chain = get_certificate

    def observe(self, path: Path, handle: int) -> _ProviderCounterSignerSequenceObservation:
        if not path.is_absolute() or handle <= 0:
            raise RuntimeError("retained Git countersigner input was invalid") from None

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
        observation: _ProviderCounterSignerSequenceObservation | None = None
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
                    observation = self._read_counter_signers(trust_data)
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
            raise RuntimeError("countersigner observation was unavailable") from None
        return observation

    def _read_counter_signers(
        self, trust_data: _WINTRUST_DATA
    ) -> _ProviderCounterSignerSequenceObservation:
        state_handle = trust_data.hWVTStateData
        if not state_handle:
            raise RuntimeError("countersigner data was unavailable") from None
        provider_data = cast(int | None, self._provider_data_from_state(state_handle))
        if not provider_data:
            raise RuntimeError("countersigner data was unavailable") from None

        primary_signer = ctypes.cast(
            self._get_signer_from_chain(  # pyright: ignore[reportArgumentType]
                provider_data, 0, False, 0
            ),
            ctypes.POINTER(_CRYPT_PROVIDER_SGNR_COMPLETE),
        )
        if not primary_signer:
            raise RuntimeError("primary signer was unavailable") from None
        counter_signer_count = int(primary_signer.contents.csCounterSigners)
        if not 1 <= counter_signer_count <= _MAX_COUNTER_SIGNERS:
            raise RuntimeError("provider countersigner count was invalid") from None

        sequence_digest = hashlib.sha256(_COUNTER_SIGNER_SEQUENCE_DOMAIN)
        sequence_digest.update(
            counter_signer_count.to_bytes(length=4, byteorder="big", signed=False)
        )
        counter_signers: list[_CounterSignerChainObservation] = []
        total_encoded_size = 0
        for counter_signer_index in range(counter_signer_count):
            counter_signer = ctypes.cast(
                self._get_signer_from_chain(  # pyright: ignore[reportArgumentType]
                    provider_data, 0, True, counter_signer_index
                ),
                ctypes.POINTER(_CRYPT_PROVIDER_SGNR_COMPLETE),
            )
            if not counter_signer:
                raise RuntimeError(
                    f"provider countersigner was unavailable at index {counter_signer_index}"
                ) from None
            signer = counter_signer.contents
            signer_type = int(signer.dwSignerType)
            provider_error = int(signer.dwError)
            if provider_error != _ERROR_SUCCESS:
                raise RuntimeError(
                    f"provider countersigner error was nonzero at index {counter_signer_index}"
                ) from None
            verify_time = signer.sftVerifyAsOf
            verify_as_of_filetime = (int(verify_time.dwHighDateTime) << 32) | int(
                verify_time.dwLowDateTime
            )
            if verify_as_of_filetime <= 0:
                raise RuntimeError(
                    f"countersigner verification time was invalid at index {counter_signer_index}"
                ) from None
            chain_length = int(signer.csCertChain)
            if not 1 <= chain_length <= _MAX_CERTIFICATE_CHAIN_LENGTH:
                raise RuntimeError(
                    f"countersigner certificate chain was invalid at index {counter_signer_index}"
                ) from None

            chain_digest = hashlib.sha256(_COUNTER_SIGNER_CHAIN_DOMAIN)
            chain_digest.update(
                counter_signer_index.to_bytes(length=4, byteorder="big", signed=False)
            )
            chain_digest.update(chain_length.to_bytes(length=4, byteorder="big", signed=False))
            sequence_digest.update(
                counter_signer_index.to_bytes(length=4, byteorder="big", signed=False)
            )
            sequence_digest.update(signer_type.to_bytes(length=4, byteorder="big", signed=False))
            sequence_digest.update(provider_error.to_bytes(length=4, byteorder="big", signed=False))
            sequence_digest.update(
                verify_as_of_filetime.to_bytes(length=8, byteorder="big", signed=False)
            )
            sequence_digest.update(chain_length.to_bytes(length=4, byteorder="big", signed=False))

            encoded_sizes: list[int] = []
            certificate_hashes: list[str] = []
            chain_encoded_size = 0
            for certificate_index in range(chain_length):
                provider_certificate = ctypes.cast(
                    self._get_certificate_from_chain(  # pyright: ignore[reportArgumentType]
                        counter_signer, certificate_index
                    ),
                    ctypes.POINTER(_CRYPT_PROVIDER_CERT),
                )
                if not provider_certificate or not provider_certificate.contents.pCert:
                    raise RuntimeError(
                        "countersigner certificate was unavailable at indexes "
                        f"{counter_signer_index}/{certificate_index}"
                    ) from None
                certificate = provider_certificate.contents.pCert.contents
                encoded_size = int(certificate.cbCertEncoded)
                if not 1 <= encoded_size <= _MAX_CERTIFICATE_DER_BYTES:
                    raise RuntimeError(
                        "countersigner certificate DER size was invalid at indexes "
                        f"{counter_signer_index}/{certificate_index}"
                    ) from None
                if chain_encoded_size > _MAX_PROVIDER_CHAIN_DER_BYTES - encoded_size:
                    raise RuntimeError(
                        f"countersigner chain DER total was invalid at index {counter_signer_index}"
                    ) from None
                if total_encoded_size > _MAX_COUNTER_SIGNER_DER_BYTES - encoded_size:
                    raise RuntimeError("countersigner DER total was invalid") from None
                if not certificate.pbCertEncoded:
                    raise RuntimeError(
                        "countersigner certificate DER was unavailable at indexes "
                        f"{counter_signer_index}/{certificate_index}"
                    ) from None
                encoded = ctypes.string_at(certificate.pbCertEncoded, encoded_size)
                chain_encoded_size += encoded_size
                total_encoded_size += encoded_size
                encoded_sizes.append(encoded_size)
                certificate_hashes.append(hashlib.sha256(encoded).hexdigest())
                for digest in (chain_digest, sequence_digest):
                    digest.update(
                        certificate_index.to_bytes(length=4, byteorder="big", signed=False)
                    )
                    digest.update(encoded_size.to_bytes(length=8, byteorder="big", signed=False))
                    digest.update(encoded)

            counter_signers.append(
                _CounterSignerChainObservation(
                    signer_type=signer_type,
                    provider_error=provider_error,
                    verify_as_of_filetime=verify_as_of_filetime,
                    chain_length=chain_length,
                    encoded_sizes=tuple(encoded_sizes),
                    certificate_sha256=tuple(certificate_hashes),
                    provider_chain_sha256=chain_digest.hexdigest(),
                )
            )

        return _ProviderCounterSignerSequenceObservation(
            counter_signer_count=counter_signer_count,
            counter_signers=tuple(counter_signers),
            counter_signer_sequence_sha256=sequence_digest.hexdigest(),
        )


def test_git_countersigner_chains_match_across_the_complete_m228_boundary() -> None:
    real_which = _commit_module.shutil.which
    with patch.object(
        _commit_module.shutil,
        "which",
        side_effect=real_which,
    ) as initial_lookup:
        git_executable = _commit_module._git_executable()  # pyright: ignore[reportPrivateUsage]
    assert initial_lookup.call_count == 1

    verifier = _AuthenticodeCounterSignerChainVerifier()
    with _RetainedGitExecutableFile(git_executable) as retained:
        before_file = retained.snapshot()
        before_counter_signers = verifier.observe(git_executable, retained.handle)
        with patch.object(
            _commit_module.shutil,
            "which",
            return_value=str(git_executable),
        ) as lookup:
            _m228_module.test_git_provider_chain_matches_across_the_complete_m227_boundary()
        assert lookup.call_count == 1
        _verify_image_stable(before_file, retained.snapshot())
        after_counter_signers = verifier.observe(git_executable, retained.handle)
        assert after_counter_signers == before_counter_signers


class _FakeCounterSignerMaterial:
    def __init__(
        self,
        chains: tuple[tuple[int, ...], ...] = ((4, 5), (3,)),
    ) -> None:
        self.encoded_buffers: list[ctypes.Array[wintypes.BYTE]] = []
        self.certificates: list[list[_CERT_CONTEXT]] = []
        self.encoded_bytes: list[tuple[bytes, ...]] = []
        self.provider_certificates: list[ctypes.Array[_CRYPT_PROVIDER_CERT]] = []
        self.signers = (_CRYPT_PROVIDER_SGNR_COMPLETE * len(chains))()
        self.missing_counter_signer_index: int | None = None
        self.missing_certificate_indexes: tuple[int, int] | None = None
        self._certificates_by_signer: dict[int, ctypes.Array[_CRYPT_PROVIDER_CERT]] = {}

        for counter_index, encoded_sizes in enumerate(chains):
            chain_certificates: list[_CERT_CONTEXT] = []
            chain_bytes: list[bytes] = []
            providers = (_CRYPT_PROVIDER_CERT * len(encoded_sizes))()
            for certificate_index, encoded_size in enumerate(encoded_sizes):
                allocation_size = max(1, min(encoded_size, _MAX_CERTIFICATE_DER_BYTES))
                encoded = bytes(
                    (counter_index * 31 + certificate_index + offset) % 256
                    for offset in range(allocation_size)
                )
                encoded_buffer = (wintypes.BYTE * allocation_size).from_buffer_copy(encoded)
                certificate = _CERT_CONTEXT()
                certificate.pbCertEncoded = ctypes.cast(
                    encoded_buffer, ctypes.POINTER(wintypes.BYTE)
                )
                certificate.cbCertEncoded = encoded_size
                certificate.pCertInfo = None
                certificate.hCertStore = wintypes.HANDLE()
                provider_certificate = providers[certificate_index]
                provider_certificate.cbStruct = ctypes.sizeof(_CRYPT_PROVIDER_CERT)
                provider_certificate.pCert = ctypes.pointer(certificate)
                self.encoded_buffers.append(encoded_buffer)
                chain_certificates.append(certificate)
                chain_bytes.append(encoded)

            signer = self.signers[counter_index]
            signer.cbStruct = ctypes.sizeof(_CRYPT_PROVIDER_SGNR_COMPLETE)
            signer.sftVerifyAsOf = wintypes.FILETIME(counter_index + 1, 0)
            signer.csCertChain = len(encoded_sizes)
            signer.pasCertChain = ctypes.cast(providers, ctypes.POINTER(_CRYPT_PROVIDER_CERT))
            signer.dwSignerType = 0x10
            signer.psSigner = None
            signer.dwError = _ERROR_SUCCESS
            signer.csCounterSigners = 0
            signer.pasCounterSigners = ctypes.POINTER(_CRYPT_PROVIDER_SGNR_COMPLETE)()
            signer.pChainContext = None
            self.provider_certificates.append(providers)
            self.certificates.append(chain_certificates)
            self.encoded_bytes.append(tuple(chain_bytes))
            self._certificates_by_signer[ctypes.addressof(signer)] = providers

        self.primary_signer = _CRYPT_PROVIDER_SGNR_COMPLETE()
        self.primary_signer.cbStruct = ctypes.sizeof(_CRYPT_PROVIDER_SGNR_COMPLETE)
        self.primary_signer.sftVerifyAsOf = wintypes.FILETIME(1, 0)
        self.primary_signer.csCertChain = 1
        self.primary_signer.pasCertChain = ctypes.POINTER(_CRYPT_PROVIDER_CERT)()
        self.primary_signer.dwSignerType = 0
        self.primary_signer.psSigner = None
        self.primary_signer.dwError = _ERROR_SUCCESS
        self.primary_signer.csCounterSigners = len(chains)
        self.primary_signer.pasCounterSigners = ctypes.cast(
            self.signers, ctypes.POINTER(_CRYPT_PROVIDER_SGNR_COMPLETE)
        )
        self.primary_signer.pChainContext = None

    def provider_data(self, *_arguments: object) -> int:
        return 1

    def get_signer(self, *_arguments: object) -> object:
        is_counter_signer = bool(_arguments[2])
        if not is_counter_signer:
            return ctypes.pointer(self.primary_signer)
        counter_index = cast(int, _arguments[3])
        if counter_index == self.missing_counter_signer_index:
            return None
        return ctypes.cast(
            ctypes.byref(
                self.signers,
                counter_index * ctypes.sizeof(_CRYPT_PROVIDER_SGNR_COMPLETE),
            ),
            ctypes.POINTER(_CRYPT_PROVIDER_SGNR_COMPLETE),
        )

    def get_certificate(self, *_arguments: object) -> object:
        signer_pointer = ctypes.cast(
            _arguments[0],  # pyright: ignore[reportArgumentType]
            ctypes.POINTER(_CRYPT_PROVIDER_SGNR_COMPLETE),
        )
        certificate_index = cast(int, _arguments[1])
        signer_address = ctypes.addressof(signer_pointer.contents)
        counter_index = next(
            index
            for index, signer in enumerate(self.signers)
            if ctypes.addressof(signer) == signer_address
        )
        if (counter_index, certificate_index) == self.missing_certificate_indexes:
            return None
        providers = self._certificates_by_signer[signer_address]
        return ctypes.cast(
            ctypes.byref(
                providers,
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
) -> _AuthenticodeCounterSignerChainVerifier:
    verifier = object.__new__(_AuthenticodeCounterSignerChainVerifier)
    vars(verifier)["_win_verify_trust"] = wintrust
    vars(verifier)["_provider_data_from_state"] = _FakeNativeFunction(provider_data)
    vars(verifier)["_get_signer_from_chain"] = _FakeNativeFunction(get_signer)
    vars(verifier)["_get_certificate_from_chain"] = _FakeNativeFunction(get_certificate)
    return verifier


def _expected_sequence_digest(encoded_chains: tuple[tuple[bytes, ...], ...]) -> str:
    digest = hashlib.sha256(_COUNTER_SIGNER_SEQUENCE_DOMAIN)
    digest.update(len(encoded_chains).to_bytes(4, "big"))
    for counter_index, encoded_values in enumerate(encoded_chains):
        digest.update(counter_index.to_bytes(4, "big"))
        digest.update((0x10).to_bytes(4, "big"))
        digest.update((0).to_bytes(4, "big"))
        digest.update((counter_index + 1).to_bytes(8, "big"))
        digest.update(len(encoded_values).to_bytes(4, "big"))
        for certificate_index, encoded in enumerate(encoded_values):
            digest.update(certificate_index.to_bytes(4, "big"))
            digest.update(len(encoded).to_bytes(8, "big"))
            digest.update(encoded)
    return digest.hexdigest()


def _expected_observation(
    material: _FakeCounterSignerMaterial,
) -> _ProviderCounterSignerSequenceObservation:
    sequence_digest = hashlib.sha256(_COUNTER_SIGNER_SEQUENCE_DOMAIN)
    sequence_digest.update(len(material.signers).to_bytes(4, "big"))
    observations: list[_CounterSignerChainObservation] = []
    for counter_index, encoded_values in enumerate(material.encoded_bytes):
        signer = material.signers[counter_index]
        verify_time = counter_index + 1
        chain_digest = hashlib.sha256(_COUNTER_SIGNER_CHAIN_DOMAIN)
        chain_digest.update(counter_index.to_bytes(4, "big"))
        chain_digest.update(len(encoded_values).to_bytes(4, "big"))
        sequence_digest.update(counter_index.to_bytes(4, "big"))
        sequence_digest.update(int(signer.dwSignerType).to_bytes(4, "big"))
        sequence_digest.update(int(signer.dwError).to_bytes(4, "big"))
        sequence_digest.update(verify_time.to_bytes(8, "big"))
        sequence_digest.update(len(encoded_values).to_bytes(4, "big"))
        for certificate_index, encoded in enumerate(encoded_values):
            for digest in (chain_digest, sequence_digest):
                digest.update(certificate_index.to_bytes(4, "big"))
                digest.update(len(encoded).to_bytes(8, "big"))
                digest.update(encoded)
        observations.append(
            _CounterSignerChainObservation(
                signer_type=int(signer.dwSignerType),
                provider_error=int(signer.dwError),
                verify_as_of_filetime=verify_time,
                chain_length=len(encoded_values),
                encoded_sizes=tuple(len(encoded) for encoded in encoded_values),
                certificate_sha256=tuple(
                    hashlib.sha256(encoded).hexdigest() for encoded in encoded_values
                ),
                provider_chain_sha256=chain_digest.hexdigest(),
            )
        )
    return _ProviderCounterSignerSequenceObservation(
        counter_signer_count=len(observations),
        counter_signers=tuple(observations),
        counter_signer_sequence_sha256=sequence_digest.hexdigest(),
    )


def test_countersigner_digest_binds_boundaries_and_order() -> None:
    split = _expected_sequence_digest(((b"a", b"bc"),))
    regrouped = _expected_sequence_digest(((b"ab", b"c"),))
    ordered = _expected_sequence_digest(((b"first",), (b"second",)))
    reversed_sequence = _expected_sequence_digest(((b"second",), (b"first",)))

    assert split != regrouped
    assert ordered != reversed_sequence


def test_complete_countersigner_sequence_is_detached_before_state_close() -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    material = _FakeCounterSignerMaterial()
    observation = _fake_verifier(
        wintrust,
        provider_data=material.provider_data,
        get_signer=material.get_signer,
        get_certificate=material.get_certificate,
    ).observe(Path("c:/git.exe"), 1)

    assert observation == _expected_observation(material)
    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_missing_provider_state_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrustWithoutState()

    with pytest.raises(RuntimeError, match="countersigner data was unavailable"):
        _fake_verifier(
            wintrust,
            provider_data=_missing_native_value,
            get_signer=_missing_native_value,
            get_certificate=_missing_native_value,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_rejected_trust_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrust(_signed_status(_TRUST_E_BAD_DIGEST), _ERROR_SUCCESS)
    material = _FakeCounterSignerMaterial()

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
        ("missing-data", "countersigner data was unavailable"),
        ("missing-primary", "primary signer was unavailable"),
        ("empty-count", "provider countersigner count was invalid"),
        ("oversized-count", "provider countersigner count was invalid"),
        ("missing-counter", "provider countersigner was unavailable at index 1"),
        ("provider-error", "provider countersigner error was nonzero at index 1"),
        ("empty-time", "countersigner verification time was invalid at index 1"),
        ("empty-chain", "countersigner certificate chain was invalid at index 1"),
        ("oversized-chain", "countersigner certificate chain was invalid at index 1"),
        ("missing-certificate", "countersigner certificate was unavailable at indexes 1/0"),
        ("missing-cert-context", "countersigner certificate was unavailable at indexes 1/0"),
        ("empty-der", "countersigner certificate DER size was invalid at indexes 1/0"),
        ("oversized-der", "countersigner certificate DER size was invalid at indexes 1/0"),
        ("missing-der", "countersigner certificate DER was unavailable at indexes 1/0"),
    ],
)
def test_invalid_countersigner_sequence_still_closes_provider_state(
    fault: str, message: str
) -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    material = _FakeCounterSignerMaterial()
    provider_data: Callable[..., object] = material.provider_data
    get_signer: Callable[..., object] = material.get_signer
    if fault == "missing-data":
        provider_data = _missing_native_value
    elif fault == "missing-primary":
        get_signer = _missing_native_value
    elif fault == "empty-count":
        material.primary_signer.csCounterSigners = 0
    elif fault == "oversized-count":
        material.primary_signer.csCounterSigners = _MAX_COUNTER_SIGNERS + 1
    elif fault == "missing-counter":
        material.missing_counter_signer_index = 1
    elif fault == "provider-error":
        material.signers[1].dwError = 1
    elif fault == "empty-time":
        material.signers[1].sftVerifyAsOf = wintypes.FILETIME()
    elif fault == "empty-chain":
        material.signers[1].csCertChain = 0
    elif fault == "oversized-chain":
        material.signers[1].csCertChain = _MAX_CERTIFICATE_CHAIN_LENGTH + 1
    elif fault == "missing-certificate":
        material.missing_certificate_indexes = (1, 0)
    elif fault == "missing-cert-context":
        material.provider_certificates[1][0].pCert = ctypes.POINTER(_CERT_CONTEXT)()
    elif fault == "empty-der":
        material.certificates[1][0].cbCertEncoded = 0
    elif fault == "oversized-der":
        material.certificates[1][0].cbCertEncoded = _MAX_CERTIFICATE_DER_BYTES + 1
    elif fault == "missing-der":
        material.certificates[1][0].pbCertEncoded = ctypes.POINTER(wintypes.BYTE)()
    else:
        raise AssertionError(f"unexpected countersigner fault: {fault}")

    with pytest.raises(RuntimeError, match=message):
        _fake_verifier(
            wintrust,
            provider_data=provider_data,
            get_signer=get_signer,
            get_certificate=material.get_certificate,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_countersigner_total_der_limit_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    material = _FakeCounterSignerMaterial(
        (
            (_MAX_CERTIFICATE_DER_BYTES,) * 4,
            (_MAX_CERTIFICATE_DER_BYTES,) * 4,
            (_MAX_CERTIFICATE_DER_BYTES,),
        )
    )

    with pytest.raises(RuntimeError, match="countersigner DER total was invalid"):
        _fake_verifier(
            wintrust,
            provider_data=material.provider_data,
            get_signer=material.get_signer,
            get_certificate=material.get_certificate,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_one_countersigner_chain_der_limit_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    material = _FakeCounterSignerMaterial(((_MAX_CERTIFICATE_DER_BYTES,) * 5,))

    with pytest.raises(RuntimeError, match="countersigner chain DER total was invalid"):
        _fake_verifier(
            wintrust,
            provider_data=material.provider_data,
            get_signer=material.get_signer,
            get_certificate=material.get_certificate,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_state_close_failure_after_countersigner_observation_is_reported() -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _signed_status(_TRUST_E_BAD_DIGEST))
    material = _FakeCounterSignerMaterial()

    with pytest.raises(RuntimeError, match="trust provider state close failed"):
        _fake_verifier(
            wintrust,
            provider_data=material.provider_data,
            get_signer=material.get_signer,
            get_certificate=material.get_certificate,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]
