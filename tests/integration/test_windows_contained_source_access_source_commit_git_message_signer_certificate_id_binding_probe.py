"""Bind each explicit WinTrust message signer CERT_ID to M232."""

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
    test_windows_contained_source_access_source_commit_git_message_signer_certificate_identifier_binding_probe as _m232_module,
)
from tests.integration.test_windows_contained_source_access_source_commit_git_file_retention_probe import (
    _RetainedGitExecutableFile,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_contained_source_access_source_commit_git_message_signer_certificate_binding_probe import (
    _CRYPT_PROVIDER_DATA_PREFIX,  # pyright: ignore[reportPrivateUsage]
    _ERROR_SUCCESS,  # pyright: ignore[reportPrivateUsage]
    _MAX_MESSAGE_SIGNERS,  # pyright: ignore[reportPrivateUsage]
    _TRUST_E_BAD_DIGEST,  # pyright: ignore[reportPrivateUsage]
    _WINTRUST_DATA,  # pyright: ignore[reportPrivateUsage]
    _WTD_STATEACTION_CLOSE,  # pyright: ignore[reportPrivateUsage]
    _WTD_STATEACTION_VERIFY,  # pyright: ignore[reportPrivateUsage]
    _FakeNativeFunction,  # pyright: ignore[reportPrivateUsage]
    _FakeWinTrust,  # pyright: ignore[reportPrivateUsage]
    _signed_status,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_contained_source_access_source_commit_git_message_signer_certificate_identifier_binding_probe import (
    _MAX_CERTIFICATE_IDENTIFIER_COMPONENT_BYTES,  # pyright: ignore[reportPrivateUsage]
    _AuthenticodeMessageSignerCertificateIdentifierVerifier,  # pyright: ignore[reportPrivateUsage]
    _CertificateIdentifier,  # pyright: ignore[reportPrivateUsage]
    _FakeMessageSignerCertificateIdentifierMaterial,  # pyright: ignore[reportPrivateUsage]
    _MessageSignerCertificateIdentifierObservation,  # pyright: ignore[reportPrivateUsage]
    _status_hex,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _verify_stable as _verify_image_stable,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M233 binds each explicit WinTrust message signer CERT_ID",
)

_CMSG_SIGNER_CERT_ID_PARAM = 38
_CERT_ID_ISSUER_SERIAL_NUMBER = 1
_CERT_ID_KEY_IDENTIFIER = 2
_CERT_ID_SHA1_HASH = 3
_MAX_CERTIFICATE_ID_BYTES = 1_048_576
_CERTIFICATE_ID_SEQUENCE_DOMAIN = b"ludoweave.wintrust-message-signer-certificate-id/1\0"
_CERTIFICATE_ID_VALUE_DOMAIN = b"ludoweave.wintrust-certificate-id/1\0"


class _CRYPT_DATA_BLOB(ctypes.Structure):
    _fields_ = [
        ("cbData", wintypes.DWORD),
        ("pbData", ctypes.POINTER(wintypes.BYTE)),
    ]


class _CERT_ISSUER_SERIAL_NUMBER(ctypes.Structure):
    _fields_ = [
        ("Issuer", _CRYPT_DATA_BLOB),
        ("SerialNumber", _CRYPT_DATA_BLOB),
    ]


class _CERT_ID_VALUE(ctypes.Union):
    _fields_ = [  # noqa: RUF012 - ctypes requires this mutable class descriptor.
        ("IssuerSerialNumber", _CERT_ISSUER_SERIAL_NUMBER),
        ("KeyId", _CRYPT_DATA_BLOB),
        ("HashId", _CRYPT_DATA_BLOB),
    ]


class _CERT_ID(ctypes.Structure):
    _fields_ = [
        ("dwIdChoice", wintypes.DWORD),
        ("value", _CERT_ID_VALUE),
    ]


@dataclass(frozen=True, slots=True)
class _MessageCertificateId:
    choice: int
    identifier: _CertificateIdentifier


@dataclass(frozen=True, slots=True)
class _MessageSignerCertificateIdObservation(
    _MessageSignerCertificateIdentifierObservation,
):
    certificate_id_choices: tuple[int, ...]
    certificate_id_sizes: tuple[tuple[int, int], ...]
    certificate_id_sha256: tuple[str, ...]
    certificate_id_sequence_sha256: str


def _certificate_id_sha256(certificate_id: _MessageCertificateId) -> str:
    digest = hashlib.sha256(_CERTIFICATE_ID_VALUE_DOMAIN)
    digest.update(certificate_id.choice.to_bytes(4, "big", signed=False))
    identifier = certificate_id.identifier
    digest.update(len(identifier.issuer).to_bytes(8, "big", signed=False))
    digest.update(identifier.issuer)
    digest.update(len(identifier.serial_number).to_bytes(8, "big", signed=False))
    digest.update(identifier.serial_number)
    return digest.hexdigest()


class _AuthenticodeMessageSignerCertificateIdVerifier(
    _AuthenticodeMessageSignerCertificateIdentifierVerifier,
):
    """Own provider state and bind the explicit CERT_ID representation."""

    def observe(
        self,
        path: Path,
        handle: int,
    ) -> _MessageSignerCertificateIdObservation:
        return cast(
            _MessageSignerCertificateIdObservation,
            super().observe(path, handle),
        )

    def _read_identifier_sequence(
        self,
        trust_data: _WINTRUST_DATA,
    ) -> _MessageSignerCertificateIdObservation:
        base_observation = super()._read_identifier_sequence(trust_data)
        state_handle = trust_data.hWVTStateData
        if not state_handle:
            raise RuntimeError("certificate-ID provider data was unavailable") from None
        provider_address = cast(int | None, self._provider_data_from_state(state_handle))
        if not provider_address:
            raise RuntimeError("certificate-ID provider data was unavailable") from None
        provider = ctypes.cast(
            provider_address,
            ctypes.POINTER(_CRYPT_PROVIDER_DATA_PREFIX),
        ).contents
        if int(provider.cbStruct) < ctypes.sizeof(_CRYPT_PROVIDER_DATA_PREFIX):
            raise RuntimeError("certificate-ID provider structure was invalid") from None
        message_handle = provider.hMsg
        if not message_handle:
            raise RuntimeError("certificate-ID message handle was unavailable") from None
        signer_count = int(provider.csSigners)
        if signer_count != base_observation.signer_count or not (
            1 <= signer_count <= _MAX_MESSAGE_SIGNERS
        ):
            raise RuntimeError("certificate-ID signer count was invalid") from None

        digest = hashlib.sha256(_CERTIFICATE_ID_SEQUENCE_DOMAIN)
        digest.update(signer_count.to_bytes(4, "big", signed=False))
        certificate_id_choices: list[int] = []
        certificate_id_sizes: list[tuple[int, int]] = []
        certificate_id_hashes: list[str] = []
        for signer_index in range(signer_count):
            message_certificate_id = self._read_message_certificate_id(
                message_handle,
                signer_index,
            )
            legacy_identifier = self._read_message_certificate_info(
                message_handle,
                signer_index,
            )
            if message_certificate_id.identifier != legacy_identifier:
                raise RuntimeError(
                    "message certificate-ID and legacy certificate identifier differed at "
                    f"index {signer_index}"
                ) from None
            certificate_id_choices.append(message_certificate_id.choice)
            certificate_id_sizes.append(
                (
                    len(message_certificate_id.identifier.issuer),
                    len(message_certificate_id.identifier.serial_number),
                )
            )
            certificate_id_hashes.append(_certificate_id_sha256(message_certificate_id))
            digest.update(signer_index.to_bytes(4, "big", signed=False))
            digest.update(message_certificate_id.choice.to_bytes(4, "big", signed=False))
            for component in (
                message_certificate_id.identifier.issuer,
                message_certificate_id.identifier.serial_number,
            ):
                digest.update(len(component).to_bytes(8, "big", signed=False))
                digest.update(component)

        return _MessageSignerCertificateIdObservation(
            provider_store_count=base_observation.provider_store_count,
            signer_count=base_observation.signer_count,
            certificate_identifier_sizes=base_observation.certificate_identifier_sizes,
            message_certificate_identifier_sha256=(
                base_observation.message_certificate_identifier_sha256
            ),
            verified_certificate_identifier_sha256=(
                base_observation.verified_certificate_identifier_sha256
            ),
            provider_certificate_identifier_sha256=(
                base_observation.provider_certificate_identifier_sha256
            ),
            certificate_identifier_sequence_sha256=(
                base_observation.certificate_identifier_sequence_sha256
            ),
            certificate_id_choices=tuple(certificate_id_choices),
            certificate_id_sizes=tuple(certificate_id_sizes),
            certificate_id_sha256=tuple(certificate_id_hashes),
            certificate_id_sequence_sha256=digest.hexdigest(),
        )

    def _read_message_certificate_id(
        self,
        message_handle: wintypes.HANDLE,
        signer_index: int,
    ) -> _MessageCertificateId:
        queried_size = wintypes.DWORD()
        if not self._crypt_msg_get_param(
            message_handle,
            _CMSG_SIGNER_CERT_ID_PARAM,
            signer_index,
            ctypes.c_void_p(),
            ctypes.byref(queried_size),
        ):
            raise RuntimeError(
                f"message signer certificate-ID query failed at index {signer_index}: "
                f"{_status_hex(ctypes.get_last_error())}"
            ) from None
        certificate_id_size = int(queried_size.value)
        if not ctypes.sizeof(_CERT_ID) <= certificate_id_size <= _MAX_CERTIFICATE_ID_BYTES:
            raise RuntimeError(
                f"message signer certificate-ID size was invalid at index {signer_index}"
            ) from None

        certificate_id_buffer = ctypes.create_string_buffer(certificate_id_size)
        read_size = wintypes.DWORD(certificate_id_size)
        if not self._crypt_msg_get_param(
            message_handle,
            _CMSG_SIGNER_CERT_ID_PARAM,
            signer_index,
            certificate_id_buffer,
            ctypes.byref(read_size),
        ):
            raise RuntimeError(
                f"message signer certificate-ID read failed at index {signer_index}: "
                f"{_status_hex(ctypes.get_last_error())}"
            ) from None
        actual_size = int(read_size.value)
        if not ctypes.sizeof(_CERT_ID) <= actual_size <= certificate_id_size:
            raise RuntimeError(
                f"message signer certificate-ID size changed at index {signer_index}"
            ) from None
        certificate_id = ctypes.cast(
            certificate_id_buffer,
            ctypes.POINTER(_CERT_ID),
        ).contents
        choice = int(certificate_id.dwIdChoice)
        if choice != _CERT_ID_ISSUER_SERIAL_NUMBER:
            raise RuntimeError(
                "unsupported message signer certificate-ID choice at "
                f"index {signer_index}: {choice}"
            ) from None
        issuer_serial = certificate_id.value.IssuerSerialNumber
        identifier = _CertificateIdentifier(
            issuer=self._copy_component(
                issuer_serial.Issuer,
                "issuer",
                signer_index,
            ),
            serial_number=self._copy_component(
                issuer_serial.SerialNumber,
                "serial number",
                signer_index,
            ),
        )
        return _MessageCertificateId(choice=choice, identifier=identifier)

    @staticmethod
    def _copy_component(
        blob: _CRYPT_DATA_BLOB,
        component: str,
        signer_index: int,
    ) -> bytes:
        size = int(blob.cbData)
        if not 1 <= size <= _MAX_CERTIFICATE_IDENTIFIER_COMPONENT_BYTES:
            raise RuntimeError(
                f"message signer certificate-ID {component} size was invalid at "
                f"index {signer_index}"
            ) from None
        if not blob.pbData:
            raise RuntimeError(
                f"message signer certificate-ID {component} was unavailable at index {signer_index}"
            ) from None
        return ctypes.string_at(blob.pbData, size)


def test_git_message_signer_certificate_ids_match_across_the_complete_m232_boundary() -> None:
    real_which = _commit_module.shutil.which
    with patch.object(
        _commit_module.shutil,
        "which",
        side_effect=real_which,
    ) as initial_lookup:
        git_executable = _commit_module._git_executable()  # pyright: ignore[reportPrivateUsage]
    assert initial_lookup.call_count == 1

    verifier = _AuthenticodeMessageSignerCertificateIdVerifier()
    with _RetainedGitExecutableFile(git_executable) as retained:
        before_file = retained.snapshot()
        before_certificate_id = verifier.observe(git_executable, retained.handle)
        with patch.object(
            _commit_module.shutil,
            "which",
            return_value=str(git_executable),
        ) as lookup:
            _m232_module.test_git_message_signer_certificate_identifiers_match_across_the_complete_m231_boundary()
        assert lookup.call_count == 1
        _verify_image_stable(before_file, retained.snapshot())
        after_certificate_id = verifier.observe(git_executable, retained.handle)
        assert after_certificate_id == before_certificate_id


class _FakeCertificateId:
    def __init__(self, choice: int, issuer: bytes, serial_number: bytes) -> None:
        self.issuer_buffer = (wintypes.BYTE * len(issuer)).from_buffer_copy(issuer)
        self.serial_buffer = (wintypes.BYTE * len(serial_number)).from_buffer_copy(serial_number)
        self.certificate_id = _CERT_ID()
        self.certificate_id.dwIdChoice = choice
        issuer_serial = self.certificate_id.value.IssuerSerialNumber
        issuer_serial.Issuer.cbData = len(issuer)
        issuer_serial.Issuer.pbData = ctypes.cast(
            self.issuer_buffer,
            ctypes.POINTER(wintypes.BYTE),
        )
        issuer_serial.SerialNumber.cbData = len(serial_number)
        issuer_serial.SerialNumber.pbData = ctypes.cast(
            self.serial_buffer,
            ctypes.POINTER(wintypes.BYTE),
        )


class _FakeMessageSignerCertificateIdMaterial(
    _FakeMessageSignerCertificateIdentifierMaterial,
):
    def __init__(
        self,
        identifiers: tuple[tuple[bytes, bytes], ...] = (
            (b"issuer-a", b"serial-a"),
            (b"issuer-b", b"serial-b"),
        ),
        *,
        certificate_id_identifiers: tuple[tuple[bytes, bytes], ...] | None = None,
        choices: tuple[int, ...] | None = None,
    ) -> None:
        super().__init__(identifiers)
        selected_identifiers = (
            identifiers if certificate_id_identifiers is None else certificate_id_identifiers
        )
        selected_choices = (
            (_CERT_ID_ISSUER_SERIAL_NUMBER,) * len(identifiers) if choices is None else choices
        )
        if len(selected_identifiers) != len(identifiers) or len(selected_choices) != len(
            identifiers
        ):
            raise ValueError("fake certificate-ID sequences must have equal counts")
        self.certificate_ids = [
            _FakeCertificateId(choice, issuer, serial_number)
            for choice, (issuer, serial_number) in zip(
                selected_choices,
                selected_identifiers,
                strict=True,
            )
        ]
        self.certificate_id_query_failure_index: int | None = None
        self.certificate_id_read_failure_index: int | None = None
        self.certificate_id_query_size = ctypes.sizeof(_CERT_ID) + 64
        self.certificate_id_read_size = self.certificate_id_query_size
        self.certificate_id_calls: list[tuple[int, bool]] = []

    def get_message_parameter(
        self,
        message_handle: object,
        parameter: int,
        index: int,
        output: object,
        size_pointer: object,
    ) -> bool:
        if parameter != _CMSG_SIGNER_CERT_ID_PARAM:
            return super().get_message_parameter(
                message_handle,
                parameter,
                index,
                output,
                size_pointer,
            )
        signer_index = int(index)
        is_read = bool(output)
        self.certificate_id_calls.append((signer_index, is_read))
        if not 0 <= signer_index < len(self.certificate_ids):
            return False
        size = ctypes.cast(
            cast(int, size_pointer),
            ctypes.POINTER(wintypes.DWORD),
        ).contents
        if not is_read:
            size.value = self.certificate_id_query_size
            return signer_index != self.certificate_id_query_failure_index
        size.value = self.certificate_id_read_size
        if signer_index == self.certificate_id_read_failure_index:
            return False
        ctypes.memmove(
            cast(int, output),
            ctypes.byref(self.certificate_ids[signer_index].certificate_id),
            ctypes.sizeof(_CERT_ID),
        )
        return True


def _fake_verifier(
    wintrust: Callable[..., object],
    material: _FakeMessageSignerCertificateIdMaterial,
) -> _AuthenticodeMessageSignerCertificateIdVerifier:
    verifier = object.__new__(_AuthenticodeMessageSignerCertificateIdVerifier)
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
    material: _FakeMessageSignerCertificateIdMaterial,
    *,
    wintrust: Callable[..., object] | None = None,
) -> _MessageSignerCertificateIdObservation:
    selected_wintrust = wintrust or _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    return _fake_verifier(selected_wintrust, material).observe(Path("c:/git.exe"), 1)


def test_fake_certificate_ids_bind_choice_payload_and_index() -> None:
    identifiers = ((b"issuer-a", b"serial-a"), (b"issuer-b", b"serial-b"))
    material = _FakeMessageSignerCertificateIdMaterial(identifiers)

    observation = _observe_material(material)

    expected_ids = tuple(
        _MessageCertificateId(
            _CERT_ID_ISSUER_SERIAL_NUMBER,
            _CertificateIdentifier(issuer, serial_number),
        )
        for issuer, serial_number in identifiers
    )
    assert observation.certificate_id_choices == (
        _CERT_ID_ISSUER_SERIAL_NUMBER,
        _CERT_ID_ISSUER_SERIAL_NUMBER,
    )
    assert observation.certificate_id_sizes == tuple(
        (len(issuer), len(serial_number)) for issuer, serial_number in identifiers
    )
    assert observation.certificate_id_sha256 == tuple(
        _certificate_id_sha256(certificate_id) for certificate_id in expected_ids
    )
    assert material.certificate_id_calls == [
        (0, False),
        (0, True),
        (1, False),
        (1, True),
    ]


def test_certificate_id_observation_is_detached() -> None:
    material = _FakeMessageSignerCertificateIdMaterial(((b"issuer", b"serial"),))
    observation = _observe_material(material)

    material.certificate_ids[0].issuer_buffer[0] = ord("X")
    material.certificate_ids[0].serial_buffer[0] = ord("Y")

    expected = _certificate_id_sha256(
        _MessageCertificateId(
            _CERT_ID_ISSUER_SERIAL_NUMBER,
            _CertificateIdentifier(b"issuer", b"serial"),
        )
    )
    assert observation.certificate_id_sha256 == (expected,)


def test_equal_concatenated_certificate_id_bytes_with_different_boundaries_differ() -> None:
    first = _observe_material(_FakeMessageSignerCertificateIdMaterial(((b"ab", b"c"),)))
    second = _observe_material(_FakeMessageSignerCertificateIdMaterial(((b"a", b"bc"),)))

    assert first.certificate_id_sequence_sha256 != second.certificate_id_sequence_sha256


def test_reversed_certificate_id_order_hashes_differently() -> None:
    first = _observe_material(
        _FakeMessageSignerCertificateIdMaterial(
            ((b"issuer-a", b"serial-a"), (b"issuer-b", b"serial-b"))
        )
    )
    second = _observe_material(
        _FakeMessageSignerCertificateIdMaterial(
            ((b"issuer-b", b"serial-b"), (b"issuer-a", b"serial-a"))
        )
    )

    assert first.certificate_id_sequence_sha256 != second.certificate_id_sequence_sha256


def test_fake_certificate_id_material_rejects_mismatched_counts() -> None:
    with pytest.raises(ValueError, match="certificate-ID sequences must have equal counts"):
        _FakeMessageSignerCertificateIdMaterial(
            ((b"issuer", b"serial"),),
            choices=(),
        )


@pytest.mark.parametrize(
    ("fault", "message"),
    [
        ("query-failure", "certificate-ID query failed"),
        ("empty-size", "certificate-ID size was invalid"),
        ("oversized-size", "certificate-ID size was invalid"),
        ("read-failure", "certificate-ID read failed"),
        ("changed-size", "certificate-ID size changed"),
        ("short-read-size", "certificate-ID size changed"),
        ("key-id-choice", "unsupported message signer certificate-ID choice"),
        ("hash-id-choice", "unsupported message signer certificate-ID choice"),
        ("unknown-choice", "unsupported message signer certificate-ID choice"),
        ("empty-issuer", "certificate-ID issuer size was invalid"),
        ("oversized-issuer", "certificate-ID issuer size was invalid"),
        ("missing-issuer", "certificate-ID issuer was unavailable"),
        ("empty-serial", "certificate-ID serial number size was invalid"),
        ("oversized-serial", "certificate-ID serial number size was invalid"),
        ("missing-serial", "certificate-ID serial number was unavailable"),
        ("legacy-mismatch", "certificate-ID and legacy certificate identifier differed"),
    ],
)
def test_invalid_certificate_id_material_still_closes_provider_state(
    fault: str,
    message: str,
) -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    certificate_id_identifiers = (
        ((b"different", b"serial"),) if fault == "legacy-mismatch" else None
    )
    material = _FakeMessageSignerCertificateIdMaterial(
        ((b"issuer", b"serial"),),
        certificate_id_identifiers=certificate_id_identifiers,
    )
    if fault == "query-failure":
        material.certificate_id_query_failure_index = 0
    elif fault == "empty-size":
        material.certificate_id_query_size = 0
    elif fault == "oversized-size":
        material.certificate_id_query_size = _MAX_CERTIFICATE_ID_BYTES + 1
    elif fault == "read-failure":
        material.certificate_id_read_failure_index = 0
    elif fault == "changed-size":
        material.certificate_id_read_size = material.certificate_id_query_size + 1
    elif fault == "short-read-size":
        material.certificate_id_read_size = ctypes.sizeof(_CERT_ID) - 1
    elif fault == "key-id-choice":
        material.certificate_ids[0].certificate_id.dwIdChoice = _CERT_ID_KEY_IDENTIFIER
    elif fault == "hash-id-choice":
        material.certificate_ids[0].certificate_id.dwIdChoice = _CERT_ID_SHA1_HASH
    elif fault == "unknown-choice":
        material.certificate_ids[0].certificate_id.dwIdChoice = 99
    elif fault == "empty-issuer":
        material.certificate_ids[0].certificate_id.value.IssuerSerialNumber.Issuer.cbData = 0
    elif fault == "oversized-issuer":
        material.certificate_ids[0].certificate_id.value.IssuerSerialNumber.Issuer.cbData = (
            _MAX_CERTIFICATE_IDENTIFIER_COMPONENT_BYTES + 1
        )
    elif fault == "missing-issuer":
        material.certificate_ids[
            0
        ].certificate_id.value.IssuerSerialNumber.Issuer.pbData = ctypes.POINTER(wintypes.BYTE)()
    elif fault == "empty-serial":
        material.certificate_ids[0].certificate_id.value.IssuerSerialNumber.SerialNumber.cbData = 0
    elif fault == "oversized-serial":
        material.certificate_ids[0].certificate_id.value.IssuerSerialNumber.SerialNumber.cbData = (
            _MAX_CERTIFICATE_IDENTIFIER_COMPONENT_BYTES + 1
        )
    elif fault == "missing-serial":
        material.certificate_ids[
            0
        ].certificate_id.value.IssuerSerialNumber.SerialNumber.pbData = ctypes.POINTER(
            wintypes.BYTE
        )()
    elif fault != "legacy-mismatch":
        raise AssertionError(f"unexpected certificate-ID fault: {fault}")

    with pytest.raises(RuntimeError, match=message):
        _fake_verifier(wintrust, material).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]
    assert material.freed_indices == [0]


def test_equal_payload_with_different_choice_is_rejected() -> None:
    material = _FakeMessageSignerCertificateIdMaterial(
        ((b"issuer", b"serial"),),
        choices=(_CERT_ID_KEY_IDENTIFIER,),
    )

    with pytest.raises(
        RuntimeError,
        match="unsupported message signer certificate-ID choice",
    ):
        _observe_material(material)


def test_rejected_trust_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrust(_signed_status(_TRUST_E_BAD_DIGEST), _ERROR_SUCCESS)
    material = _FakeMessageSignerCertificateIdMaterial(((b"issuer", b"serial"),))

    with pytest.raises(RuntimeError, match="0x80096010"):
        _fake_verifier(wintrust, material).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]
