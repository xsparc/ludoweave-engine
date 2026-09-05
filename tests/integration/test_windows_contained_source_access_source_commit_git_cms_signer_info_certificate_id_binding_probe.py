"""Bind each CMS SignerInfo certificate ID to the complete M233 boundary."""

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
    test_windows_contained_source_access_source_commit_git_message_signer_certificate_id_binding_probe as _m233_module,
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
from tests.integration.test_windows_contained_source_access_source_commit_git_message_signer_certificate_id_binding_probe import (
    _CERT_ID,  # pyright: ignore[reportPrivateUsage]
    _CERT_ID_ISSUER_SERIAL_NUMBER,  # pyright: ignore[reportPrivateUsage]
    _CERT_ID_KEY_IDENTIFIER,  # pyright: ignore[reportPrivateUsage]
    _CERT_ID_SHA1_HASH,  # pyright: ignore[reportPrivateUsage]
    _MAX_CERTIFICATE_IDENTIFIER_COMPONENT_BYTES,  # pyright: ignore[reportPrivateUsage]
    _AuthenticodeMessageSignerCertificateIdVerifier,  # pyright: ignore[reportPrivateUsage]
    _certificate_id_sha256,  # pyright: ignore[reportPrivateUsage]
    _CertificateIdentifier,  # pyright: ignore[reportPrivateUsage]
    _FakeCertificateId,  # pyright: ignore[reportPrivateUsage]
    _FakeMessageSignerCertificateIdMaterial,  # pyright: ignore[reportPrivateUsage]
    _MessageCertificateId,  # pyright: ignore[reportPrivateUsage]
    _MessageSignerCertificateIdObservation,  # pyright: ignore[reportPrivateUsage]
    _status_hex,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _verify_stable as _verify_image_stable,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M234 binds each CMS SignerInfo certificate ID",
)

_CMSG_CMS_SIGNER_INFO_PARAM = 39
_CMSG_SIGNER_INFO_V1 = 1
_CMSG_SIGNER_INFO_V3 = 3
_MAX_CMS_SIGNER_INFO_BYTES = 1_048_576
_CMS_SIGNER_INFO_SEQUENCE_DOMAIN = b"ludoweave.wintrust-cms-signer-info-sequence/1\0"
_CMS_SIGNER_INFO_VALUE_DOMAIN = b"ludoweave.wintrust-cms-signer-info/1\0"


class _CMSG_CMS_SIGNER_INFO_PREFIX(ctypes.Structure):
    _fields_ = [
        ("dwVersion", wintypes.DWORD),
        ("SignerId", _CERT_ID),
    ]


@dataclass(frozen=True, slots=True)
class _CmsSignerInfoCertificateId:
    version: int
    certificate_id: _MessageCertificateId


@dataclass(frozen=True, slots=True)
class _CmsSignerInfoCertificateIdObservation(_MessageSignerCertificateIdObservation):
    cms_signer_info_versions: tuple[int, ...]
    cms_signer_info_certificate_id_choices: tuple[int, ...]
    cms_signer_info_certificate_id_sizes: tuple[tuple[int, int], ...]
    cms_signer_info_certificate_id_sha256: tuple[str, ...]
    cms_signer_info_sequence_sha256: str


def _cms_signer_info_sha256(signer_info: _CmsSignerInfoCertificateId) -> str:
    digest = hashlib.sha256(_CMS_SIGNER_INFO_VALUE_DOMAIN)
    digest.update(signer_info.version.to_bytes(4, "big", signed=False))
    certificate_id = signer_info.certificate_id
    digest.update(certificate_id.choice.to_bytes(4, "big", signed=False))
    for component in (
        certificate_id.identifier.issuer,
        certificate_id.identifier.serial_number,
    ):
        digest.update(len(component).to_bytes(8, "big", signed=False))
        digest.update(component)
    return digest.hexdigest()


class _AuthenticodeCmsSignerInfoCertificateIdVerifier(
    _AuthenticodeMessageSignerCertificateIdVerifier,
):
    """Own provider state and bind the CMS SignerInfo SignerId representation."""

    def observe(
        self,
        path: Path,
        handle: int,
    ) -> _CmsSignerInfoCertificateIdObservation:
        return cast(
            _CmsSignerInfoCertificateIdObservation,
            super().observe(path, handle),
        )

    def _read_identifier_sequence(
        self,
        trust_data: _WINTRUST_DATA,
    ) -> _CmsSignerInfoCertificateIdObservation:
        base_observation = super()._read_identifier_sequence(trust_data)
        state_handle = trust_data.hWVTStateData
        if not state_handle:
            raise RuntimeError("CMS signer-info provider data was unavailable") from None
        provider_address = cast(int | None, self._provider_data_from_state(state_handle))
        if not provider_address:
            raise RuntimeError("CMS signer-info provider data was unavailable") from None
        provider = ctypes.cast(
            provider_address,
            ctypes.POINTER(_CRYPT_PROVIDER_DATA_PREFIX),
        ).contents
        if int(provider.cbStruct) < ctypes.sizeof(_CRYPT_PROVIDER_DATA_PREFIX):
            raise RuntimeError("CMS signer-info provider structure was invalid") from None
        message_handle = provider.hMsg
        if not message_handle:
            raise RuntimeError("CMS signer-info message handle was unavailable") from None
        signer_count = int(provider.csSigners)
        if signer_count != base_observation.signer_count or not (
            1 <= signer_count <= _MAX_MESSAGE_SIGNERS
        ):
            raise RuntimeError("CMS signer-info signer count was invalid") from None

        digest = hashlib.sha256(_CMS_SIGNER_INFO_SEQUENCE_DOMAIN)
        digest.update(signer_count.to_bytes(4, "big", signed=False))
        cms_signer_info_versions: list[int] = []
        cms_certificate_id_choices: list[int] = []
        cms_certificate_id_sizes: list[tuple[int, int]] = []
        cms_signer_info_hashes: list[str] = []
        for signer_index in range(signer_count):
            cms_signer_info = self._read_cms_signer_info(
                message_handle,
                signer_index,
            )
            dedicated_certificate_id = self._read_message_certificate_id(
                message_handle,
                signer_index,
            )
            if cms_signer_info.certificate_id != dedicated_certificate_id:
                raise RuntimeError(
                    f"CMS signer-info and dedicated certificate-ID differed at index {signer_index}"
                ) from None
            certificate_id = cms_signer_info.certificate_id
            sizes = (
                len(certificate_id.identifier.issuer),
                len(certificate_id.identifier.serial_number),
            )
            if (
                cms_signer_info.version != _CMSG_SIGNER_INFO_V1
                or certificate_id.choice != base_observation.certificate_id_choices[signer_index]
                or sizes != base_observation.certificate_id_sizes[signer_index]
                or _certificate_id_sha256(certificate_id)
                != base_observation.certificate_id_sha256[signer_index]
            ):
                raise RuntimeError(
                    "CMS signer-info certificate-ID and M233 observation differed at "
                    f"index {signer_index}"
                ) from None
            cms_signer_info_versions.append(cms_signer_info.version)
            cms_certificate_id_choices.append(certificate_id.choice)
            cms_certificate_id_sizes.append(sizes)
            cms_signer_info_hashes.append(_cms_signer_info_sha256(cms_signer_info))
            digest.update(signer_index.to_bytes(4, "big", signed=False))
            digest.update(cms_signer_info.version.to_bytes(4, "big", signed=False))
            digest.update(certificate_id.choice.to_bytes(4, "big", signed=False))
            for component in (
                certificate_id.identifier.issuer,
                certificate_id.identifier.serial_number,
            ):
                digest.update(len(component).to_bytes(8, "big", signed=False))
                digest.update(component)

        return _CmsSignerInfoCertificateIdObservation(
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
            certificate_id_choices=base_observation.certificate_id_choices,
            certificate_id_sizes=base_observation.certificate_id_sizes,
            certificate_id_sha256=base_observation.certificate_id_sha256,
            certificate_id_sequence_sha256=(base_observation.certificate_id_sequence_sha256),
            cms_signer_info_versions=tuple(cms_signer_info_versions),
            cms_signer_info_certificate_id_choices=tuple(cms_certificate_id_choices),
            cms_signer_info_certificate_id_sizes=tuple(cms_certificate_id_sizes),
            cms_signer_info_certificate_id_sha256=tuple(cms_signer_info_hashes),
            cms_signer_info_sequence_sha256=digest.hexdigest(),
        )

    def _read_cms_signer_info(
        self,
        message_handle: wintypes.HANDLE,
        signer_index: int,
    ) -> _CmsSignerInfoCertificateId:
        queried_size = wintypes.DWORD()
        if not self._crypt_msg_get_param(
            message_handle,
            _CMSG_CMS_SIGNER_INFO_PARAM,
            signer_index,
            ctypes.c_void_p(),
            ctypes.byref(queried_size),
        ):
            raise RuntimeError(
                f"CMS signer-info query failed at index {signer_index}: "
                f"{_status_hex(ctypes.get_last_error())}"
            ) from None
        cms_signer_info_size = int(queried_size.value)
        if not (
            ctypes.sizeof(_CMSG_CMS_SIGNER_INFO_PREFIX)
            <= cms_signer_info_size
            <= _MAX_CMS_SIGNER_INFO_BYTES
        ):
            raise RuntimeError(
                f"CMS signer-info size was invalid at index {signer_index}"
            ) from None

        cms_signer_info_buffer = ctypes.create_string_buffer(cms_signer_info_size)
        read_size = wintypes.DWORD(cms_signer_info_size)
        if not self._crypt_msg_get_param(
            message_handle,
            _CMSG_CMS_SIGNER_INFO_PARAM,
            signer_index,
            cms_signer_info_buffer,
            ctypes.byref(read_size),
        ):
            raise RuntimeError(
                f"CMS signer-info read failed at index {signer_index}: "
                f"{_status_hex(ctypes.get_last_error())}"
            ) from None
        actual_size = int(read_size.value)
        if not (ctypes.sizeof(_CMSG_CMS_SIGNER_INFO_PREFIX) <= actual_size <= cms_signer_info_size):
            raise RuntimeError(f"CMS signer-info size changed at index {signer_index}") from None
        prefix = ctypes.cast(
            cms_signer_info_buffer,
            ctypes.POINTER(_CMSG_CMS_SIGNER_INFO_PREFIX),
        ).contents
        version = int(prefix.dwVersion)
        if version != _CMSG_SIGNER_INFO_V1:
            raise RuntimeError(
                f"unsupported CMS signer-info version at index {signer_index}: {version}"
            ) from None
        choice = int(prefix.SignerId.dwIdChoice)
        if choice != _CERT_ID_ISSUER_SERIAL_NUMBER:
            raise RuntimeError(
                "unsupported CMS signer-info certificate-ID choice at "
                f"index {signer_index}: {choice}"
            ) from None
        issuer_serial = prefix.SignerId.value.IssuerSerialNumber
        certificate_id = _MessageCertificateId(
            choice=choice,
            identifier=_CertificateIdentifier(
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
            ),
        )
        return _CmsSignerInfoCertificateId(
            version=version,
            certificate_id=certificate_id,
        )


def test_git_cms_signer_info_certificate_ids_match_across_the_complete_m233_boundary() -> None:
    real_which = _commit_module.shutil.which
    with patch.object(
        _commit_module.shutil,
        "which",
        side_effect=real_which,
    ) as initial_lookup:
        git_executable = _commit_module._git_executable()  # pyright: ignore[reportPrivateUsage]
    assert initial_lookup.call_count == 1

    verifier = _AuthenticodeCmsSignerInfoCertificateIdVerifier()
    with _RetainedGitExecutableFile(git_executable) as retained:
        before_file = retained.snapshot()
        before_cms_signer_info = verifier.observe(git_executable, retained.handle)
        with patch.object(
            _commit_module.shutil,
            "which",
            return_value=str(git_executable),
        ) as lookup:
            _m233_module.test_git_message_signer_certificate_ids_match_across_the_complete_m232_boundary()
        assert lookup.call_count == 1
        _verify_image_stable(before_file, retained.snapshot())
        after_cms_signer_info = verifier.observe(git_executable, retained.handle)
        assert after_cms_signer_info == before_cms_signer_info


class _FakeCmsSignerInfo:
    def __init__(self, version: int, choice: int, issuer: bytes, serial_number: bytes) -> None:
        self.certificate_id_material = _FakeCertificateId(
            choice,
            issuer,
            serial_number,
        )
        self.prefix = _CMSG_CMS_SIGNER_INFO_PREFIX()
        self.prefix.dwVersion = version
        self.prefix.SignerId = self.certificate_id_material.certificate_id


class _FakeCmsSignerInfoCertificateIdMaterial(_FakeMessageSignerCertificateIdMaterial):
    def __init__(
        self,
        identifiers: tuple[tuple[bytes, bytes], ...] = (
            (b"issuer-a", b"serial-a"),
            (b"issuer-b", b"serial-b"),
        ),
        *,
        cms_identifiers: tuple[tuple[bytes, bytes], ...] | None = None,
        cms_choices: tuple[int, ...] | None = None,
        versions: tuple[int, ...] | None = None,
    ) -> None:
        super().__init__(identifiers)
        selected_identifiers = identifiers if cms_identifiers is None else cms_identifiers
        selected_choices = (
            (_CERT_ID_ISSUER_SERIAL_NUMBER,) * len(identifiers)
            if cms_choices is None
            else cms_choices
        )
        selected_versions = (
            (_CMSG_SIGNER_INFO_V1,) * len(identifiers) if versions is None else versions
        )
        if not (
            len(selected_identifiers)
            == len(selected_choices)
            == len(selected_versions)
            == len(identifiers)
        ):
            raise ValueError("fake CMS signer-info sequences must have equal counts")
        self.cms_signer_infos = [
            _FakeCmsSignerInfo(version, choice, issuer, serial_number)
            for version, choice, (issuer, serial_number) in zip(
                selected_versions,
                selected_choices,
                selected_identifiers,
                strict=True,
            )
        ]
        self.cms_query_failure_index: int | None = None
        self.cms_read_failure_index: int | None = None
        self.cms_query_size = ctypes.sizeof(_CMSG_CMS_SIGNER_INFO_PREFIX) + 64
        self.cms_read_size = self.cms_query_size
        self.cms_calls: list[tuple[int, bool]] = []

    def get_message_parameter(
        self,
        message_handle: object,
        parameter: int,
        index: int,
        output: object,
        size_pointer: object,
    ) -> bool:
        if parameter != _CMSG_CMS_SIGNER_INFO_PARAM:
            return super().get_message_parameter(
                message_handle,
                parameter,
                index,
                output,
                size_pointer,
            )
        signer_index = int(index)
        is_read = bool(output)
        self.cms_calls.append((signer_index, is_read))
        if not 0 <= signer_index < len(self.cms_signer_infos):
            return False
        size = ctypes.cast(
            cast(int, size_pointer),
            ctypes.POINTER(wintypes.DWORD),
        ).contents
        if not is_read:
            size.value = self.cms_query_size
            return signer_index != self.cms_query_failure_index
        size.value = self.cms_read_size
        if signer_index == self.cms_read_failure_index:
            return False
        ctypes.memmove(
            cast(int, output),
            ctypes.byref(self.cms_signer_infos[signer_index].prefix),
            ctypes.sizeof(_CMSG_CMS_SIGNER_INFO_PREFIX),
        )
        return True


def _fake_verifier(
    wintrust: Callable[..., object],
    material: _FakeCmsSignerInfoCertificateIdMaterial,
) -> _AuthenticodeCmsSignerInfoCertificateIdVerifier:
    verifier = object.__new__(_AuthenticodeCmsSignerInfoCertificateIdVerifier)
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
    material: _FakeCmsSignerInfoCertificateIdMaterial,
    *,
    wintrust: Callable[..., object] | None = None,
) -> _CmsSignerInfoCertificateIdObservation:
    selected_wintrust = wintrust or _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    return _fake_verifier(selected_wintrust, material).observe(Path("c:/git.exe"), 1)


def test_fake_cms_signer_info_binds_version_choice_payload_and_index() -> None:
    identifiers = ((b"issuer-a", b"serial-a"), (b"issuer-b", b"serial-b"))
    material = _FakeCmsSignerInfoCertificateIdMaterial(identifiers)

    observation = _observe_material(material)

    expected = tuple(
        _CmsSignerInfoCertificateId(
            _CMSG_SIGNER_INFO_V1,
            _MessageCertificateId(
                _CERT_ID_ISSUER_SERIAL_NUMBER,
                _CertificateIdentifier(issuer, serial_number),
            ),
        )
        for issuer, serial_number in identifiers
    )
    assert observation.cms_signer_info_versions == (
        _CMSG_SIGNER_INFO_V1,
        _CMSG_SIGNER_INFO_V1,
    )
    assert observation.cms_signer_info_certificate_id_choices == (
        _CERT_ID_ISSUER_SERIAL_NUMBER,
        _CERT_ID_ISSUER_SERIAL_NUMBER,
    )
    assert observation.cms_signer_info_certificate_id_sizes == tuple(
        (len(issuer), len(serial_number)) for issuer, serial_number in identifiers
    )
    assert observation.cms_signer_info_certificate_id_sha256 == tuple(
        _cms_signer_info_sha256(signer_info) for signer_info in expected
    )
    assert material.cms_calls == [(0, False), (0, True), (1, False), (1, True)]


def test_cms_signer_info_observation_is_detached() -> None:
    material = _FakeCmsSignerInfoCertificateIdMaterial(((b"issuer", b"serial"),))
    observation = _observe_material(material)

    info = material.cms_signer_infos[0].certificate_id_material
    info.issuer_buffer[0] = ord("X")
    info.serial_buffer[0] = ord("Y")

    expected = _cms_signer_info_sha256(
        _CmsSignerInfoCertificateId(
            _CMSG_SIGNER_INFO_V1,
            _MessageCertificateId(
                _CERT_ID_ISSUER_SERIAL_NUMBER,
                _CertificateIdentifier(b"issuer", b"serial"),
            ),
        )
    )
    assert observation.cms_signer_info_certificate_id_sha256 == (expected,)


def test_cms_signer_info_hash_binds_version() -> None:
    certificate_id = _MessageCertificateId(
        _CERT_ID_ISSUER_SERIAL_NUMBER,
        _CertificateIdentifier(b"issuer", b"serial"),
    )

    assert _cms_signer_info_sha256(
        _CmsSignerInfoCertificateId(_CMSG_SIGNER_INFO_V1, certificate_id)
    ) != _cms_signer_info_sha256(_CmsSignerInfoCertificateId(_CMSG_SIGNER_INFO_V3, certificate_id))


def test_equal_concatenated_cms_identifier_bytes_with_different_boundaries_differ() -> None:
    first = _observe_material(_FakeCmsSignerInfoCertificateIdMaterial(((b"ab", b"c"),)))
    second = _observe_material(_FakeCmsSignerInfoCertificateIdMaterial(((b"a", b"bc"),)))

    assert first.cms_signer_info_sequence_sha256 != second.cms_signer_info_sequence_sha256


def test_reversed_cms_signer_info_order_hashes_differently() -> None:
    first = _observe_material(
        _FakeCmsSignerInfoCertificateIdMaterial(
            ((b"issuer-a", b"serial-a"), (b"issuer-b", b"serial-b"))
        )
    )
    second = _observe_material(
        _FakeCmsSignerInfoCertificateIdMaterial(
            ((b"issuer-b", b"serial-b"), (b"issuer-a", b"serial-a"))
        )
    )

    assert first.cms_signer_info_sequence_sha256 != second.cms_signer_info_sequence_sha256


def test_fake_cms_signer_info_material_rejects_mismatched_counts() -> None:
    with pytest.raises(ValueError, match="CMS signer-info sequences must have equal counts"):
        _FakeCmsSignerInfoCertificateIdMaterial(
            ((b"issuer", b"serial"),),
            versions=(),
        )


@pytest.mark.parametrize(
    ("fault", "message"),
    [
        ("query-failure", "CMS signer-info query failed"),
        ("empty-size", "CMS signer-info size was invalid"),
        ("oversized-size", "CMS signer-info size was invalid"),
        ("read-failure", "CMS signer-info read failed"),
        ("changed-size", "CMS signer-info size changed"),
        ("short-read-size", "CMS signer-info size changed"),
        ("zero-version", "unsupported CMS signer-info version"),
        ("v3-version", "unsupported CMS signer-info version"),
        ("key-id-choice", "unsupported CMS signer-info certificate-ID choice"),
        ("hash-id-choice", "unsupported CMS signer-info certificate-ID choice"),
        ("unknown-choice", "unsupported CMS signer-info certificate-ID choice"),
        ("empty-issuer", "certificate-ID issuer size was invalid"),
        ("oversized-issuer", "certificate-ID issuer size was invalid"),
        ("missing-issuer", "certificate-ID issuer was unavailable"),
        ("empty-serial", "certificate-ID serial number size was invalid"),
        ("oversized-serial", "certificate-ID serial number size was invalid"),
        ("missing-serial", "certificate-ID serial number was unavailable"),
        ("dedicated-mismatch", "CMS signer-info and dedicated certificate-ID differed"),
    ],
)
def test_invalid_cms_signer_info_material_still_closes_provider_state(
    fault: str,
    message: str,
) -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    cms_identifiers = ((b"different", b"serial"),) if fault == "dedicated-mismatch" else None
    material = _FakeCmsSignerInfoCertificateIdMaterial(
        ((b"issuer", b"serial"),),
        cms_identifiers=cms_identifiers,
    )
    if fault == "query-failure":
        material.cms_query_failure_index = 0
    elif fault == "empty-size":
        material.cms_query_size = 0
    elif fault == "oversized-size":
        material.cms_query_size = _MAX_CMS_SIGNER_INFO_BYTES + 1
    elif fault == "read-failure":
        material.cms_read_failure_index = 0
    elif fault == "changed-size":
        material.cms_read_size = material.cms_query_size + 1
    elif fault == "short-read-size":
        material.cms_read_size = ctypes.sizeof(_CMSG_CMS_SIGNER_INFO_PREFIX) - 1
    elif fault == "zero-version":
        material.cms_signer_infos[0].prefix.dwVersion = 0
    elif fault == "v3-version":
        material.cms_signer_infos[0].prefix.dwVersion = _CMSG_SIGNER_INFO_V3
    elif fault == "key-id-choice":
        material.cms_signer_infos[0].prefix.SignerId.dwIdChoice = _CERT_ID_KEY_IDENTIFIER
    elif fault == "hash-id-choice":
        material.cms_signer_infos[0].prefix.SignerId.dwIdChoice = _CERT_ID_SHA1_HASH
    elif fault == "unknown-choice":
        material.cms_signer_infos[0].prefix.SignerId.dwIdChoice = 99
    elif fault == "empty-issuer":
        material.cms_signer_infos[0].prefix.SignerId.value.IssuerSerialNumber.Issuer.cbData = 0
    elif fault == "oversized-issuer":
        material.cms_signer_infos[0].prefix.SignerId.value.IssuerSerialNumber.Issuer.cbData = (
            _MAX_CERTIFICATE_IDENTIFIER_COMPONENT_BYTES + 1
        )
    elif fault == "missing-issuer":
        material.cms_signer_infos[
            0
        ].prefix.SignerId.value.IssuerSerialNumber.Issuer.pbData = ctypes.POINTER(wintypes.BYTE)()
    elif fault == "empty-serial":
        material.cms_signer_infos[
            0
        ].prefix.SignerId.value.IssuerSerialNumber.SerialNumber.cbData = 0
    elif fault == "oversized-serial":
        material.cms_signer_infos[
            0
        ].prefix.SignerId.value.IssuerSerialNumber.SerialNumber.cbData = (
            _MAX_CERTIFICATE_IDENTIFIER_COMPONENT_BYTES + 1
        )
    elif fault == "missing-serial":
        material.cms_signer_infos[
            0
        ].prefix.SignerId.value.IssuerSerialNumber.SerialNumber.pbData = ctypes.POINTER(
            wintypes.BYTE
        )()
    elif fault != "dedicated-mismatch":
        raise AssertionError(f"unexpected CMS signer-info fault: {fault}")

    with pytest.raises(RuntimeError, match=message):
        _fake_verifier(wintrust, material).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]
    assert material.freed_indices == [0]


def test_rejected_trust_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrust(_signed_status(_TRUST_E_BAD_DIGEST), _ERROR_SUCCESS)
    material = _FakeCmsSignerInfoCertificateIdMaterial(((b"issuer", b"serial"),))

    with pytest.raises(RuntimeError, match="0x80096010"):
        _fake_verifier(wintrust, material).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]
