"""Bind each CMS signer hash algorithm to the complete M234 boundary."""

from __future__ import annotations

import ctypes
import hashlib
import re
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
    test_windows_contained_source_access_source_commit_git_cms_signer_info_certificate_id_binding_probe as _m234_module,
)
from tests.integration.test_windows_contained_source_access_source_commit_git_cms_signer_info_certificate_id_binding_probe import (
    _CMSG_SIGNER_INFO_V1,  # pyright: ignore[reportPrivateUsage]
    _MAX_CMS_SIGNER_INFO_BYTES,  # pyright: ignore[reportPrivateUsage]
    _AuthenticodeCmsSignerInfoCertificateIdVerifier,  # pyright: ignore[reportPrivateUsage]
    _CmsSignerInfoCertificateIdObservation,  # pyright: ignore[reportPrivateUsage]
    _FakeCmsSignerInfoCertificateIdMaterial,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_contained_source_access_source_commit_git_file_retention_probe import (
    _RetainedGitExecutableFile,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_contained_source_access_source_commit_git_message_signer_certificate_binding_probe import (
    _CRYPT_PROVIDER_DATA_PREFIX,  # pyright: ignore[reportPrivateUsage]
    _ERROR_SUCCESS,  # pyright: ignore[reportPrivateUsage]
    _MAX_MESSAGE_SIGNERS,  # pyright: ignore[reportPrivateUsage]
    _WINTRUST_DATA,  # pyright: ignore[reportPrivateUsage]
    _WTD_STATEACTION_CLOSE,  # pyright: ignore[reportPrivateUsage]
    _WTD_STATEACTION_VERIFY,  # pyright: ignore[reportPrivateUsage]
    _FakeNativeFunction,  # pyright: ignore[reportPrivateUsage]
    _FakeWinTrust,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_contained_source_access_source_commit_git_message_signer_certificate_id_binding_probe import (
    _CERT_ID,  # pyright: ignore[reportPrivateUsage]
    _status_hex,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_contained_source_access_source_commit_git_message_signer_certificate_identifier_binding_probe import (
    _CRYPT_DATA_BLOB,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _verify_stable as _verify_image_stable,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M235 binds each CMS signer hash algorithm",
)

_CMSG_SIGNER_HASH_ALGORITHM_PARAM = 8
_CMSG_CMS_SIGNER_INFO_PARAM = 39
_MAX_HASH_ALGORITHM_BYTES = 1_048_576
_MAX_ALGORITHM_OID_BYTES = 255
_MAX_ALGORITHM_PARAMETER_BYTES = 1_048_576
_HASH_ALGORITHM_SEQUENCE_DOMAIN = b"ludoweave.wintrust-hash-algorithm-sequence/1\0"
_HASH_ALGORITHM_VALUE_DOMAIN = b"ludoweave.wintrust-hash-algorithm/1\0"
_OID_PATTERN = re.compile(r"[0-9]+(?:\.[0-9]+)+")


class _CRYPT_ALGORITHM_IDENTIFIER(ctypes.Structure):
    _fields_ = [
        ("pszObjId", ctypes.c_void_p),
        ("Parameters", _CRYPT_DATA_BLOB),
    ]


class _CMSG_CMS_SIGNER_INFO_HASH_PREFIX(ctypes.Structure):
    _fields_ = [
        ("dwVersion", wintypes.DWORD),
        ("SignerId", _CERT_ID),
        ("HashAlgorithm", _CRYPT_ALGORITHM_IDENTIFIER),
    ]


@dataclass(frozen=True, slots=True)
class _HashAlgorithm:
    oid: str
    parameters: bytes


@dataclass(frozen=True, slots=True)
class _CmsSignerHashAlgorithmObservation(_CmsSignerInfoCertificateIdObservation):
    hash_algorithm_oids: tuple[str, ...]
    hash_algorithm_parameter_sizes: tuple[int, ...]
    cms_hash_algorithm_sha256: tuple[str, ...]
    dedicated_hash_algorithm_sha256: tuple[str, ...]
    hash_algorithm_sequence_sha256: str


def _hash_algorithm_sha256(algorithm: _HashAlgorithm) -> str:
    oid = algorithm.oid.encode("ascii")
    digest = hashlib.sha256(_HASH_ALGORITHM_VALUE_DOMAIN)
    digest.update(len(oid).to_bytes(8, "big", signed=False))
    digest.update(oid)
    digest.update(len(algorithm.parameters).to_bytes(8, "big", signed=False))
    digest.update(algorithm.parameters)
    return digest.hexdigest()


class _AuthenticodeCmsSignerHashAlgorithmVerifier(
    _AuthenticodeCmsSignerInfoCertificateIdVerifier,
):
    """Bind the two native hash-algorithm representations for every signer."""

    def observe(
        self,
        path: Path,
        handle: int,
    ) -> _CmsSignerHashAlgorithmObservation:
        return cast(
            _CmsSignerHashAlgorithmObservation,
            super().observe(path, handle),
        )

    def _read_identifier_sequence(
        self,
        trust_data: _WINTRUST_DATA,
    ) -> _CmsSignerHashAlgorithmObservation:
        base_observation = super()._read_identifier_sequence(trust_data)
        state_handle = trust_data.hWVTStateData
        if not state_handle:
            raise RuntimeError("CMS hash-algorithm provider data was unavailable") from None
        provider_address = cast(int | None, self._provider_data_from_state(state_handle))
        if not provider_address:
            raise RuntimeError("CMS hash-algorithm provider data was unavailable") from None
        provider = ctypes.cast(
            provider_address,
            ctypes.POINTER(_CRYPT_PROVIDER_DATA_PREFIX),
        ).contents
        if int(provider.cbStruct) < ctypes.sizeof(_CRYPT_PROVIDER_DATA_PREFIX):
            raise RuntimeError("CMS hash-algorithm provider structure was invalid") from None
        message_handle = provider.hMsg
        if not message_handle:
            raise RuntimeError("CMS hash-algorithm message handle was unavailable") from None
        signer_count = int(provider.csSigners)
        if signer_count != base_observation.signer_count or not (
            1 <= signer_count <= _MAX_MESSAGE_SIGNERS
        ):
            raise RuntimeError("CMS hash-algorithm signer count was invalid") from None

        digest = hashlib.sha256(_HASH_ALGORITHM_SEQUENCE_DOMAIN)
        digest.update(signer_count.to_bytes(4, "big", signed=False))
        hash_algorithm_oids: list[str] = []
        hash_algorithm_parameter_sizes: list[int] = []
        cms_hashes: list[str] = []
        dedicated_hashes: list[str] = []
        for signer_index in range(signer_count):
            cms_hash_algorithm = self._read_cms_signer_hash_algorithm(
                message_handle,
                signer_index,
            )
            dedicated_hash_algorithm = self._read_dedicated_signer_hash_algorithm(
                message_handle,
                signer_index,
            )
            if cms_hash_algorithm != dedicated_hash_algorithm:
                raise RuntimeError(
                    f"CMS and dedicated signer hash algorithms differed at index {signer_index}"
                ) from None
            hash_algorithm_oids.append(cms_hash_algorithm.oid)
            hash_algorithm_parameter_sizes.append(len(cms_hash_algorithm.parameters))
            cms_hash = _hash_algorithm_sha256(cms_hash_algorithm)
            dedicated_hash = _hash_algorithm_sha256(dedicated_hash_algorithm)
            cms_hashes.append(cms_hash)
            dedicated_hashes.append(dedicated_hash)
            digest.update(signer_index.to_bytes(4, "big", signed=False))
            digest.update(bytes.fromhex(cms_hash))

        return _CmsSignerHashAlgorithmObservation(
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
            certificate_id_sequence_sha256=base_observation.certificate_id_sequence_sha256,
            cms_signer_info_versions=base_observation.cms_signer_info_versions,
            cms_signer_info_certificate_id_choices=(
                base_observation.cms_signer_info_certificate_id_choices
            ),
            cms_signer_info_certificate_id_sizes=(
                base_observation.cms_signer_info_certificate_id_sizes
            ),
            cms_signer_info_certificate_id_sha256=(
                base_observation.cms_signer_info_certificate_id_sha256
            ),
            cms_signer_info_sequence_sha256=base_observation.cms_signer_info_sequence_sha256,
            hash_algorithm_oids=tuple(hash_algorithm_oids),
            hash_algorithm_parameter_sizes=tuple(hash_algorithm_parameter_sizes),
            cms_hash_algorithm_sha256=tuple(cms_hashes),
            dedicated_hash_algorithm_sha256=tuple(dedicated_hashes),
            hash_algorithm_sequence_sha256=digest.hexdigest(),
        )

    def _read_cms_signer_hash_algorithm(
        self,
        message_handle: wintypes.HANDLE,
        signer_index: int,
    ) -> _HashAlgorithm:
        queried_size = wintypes.DWORD()
        if not self._crypt_msg_get_param(
            message_handle,
            _CMSG_CMS_SIGNER_INFO_PARAM,
            signer_index,
            ctypes.c_void_p(),
            ctypes.byref(queried_size),
        ):
            raise RuntimeError(
                f"CMS signer hash-algorithm query failed at index {signer_index}: "
                f"{_status_hex(ctypes.get_last_error())}"
            ) from None
        cms_signer_info_size = int(queried_size.value)
        if not (
            ctypes.sizeof(_CMSG_CMS_SIGNER_INFO_HASH_PREFIX)
            <= cms_signer_info_size
            <= _MAX_CMS_SIGNER_INFO_BYTES
        ):
            raise RuntimeError(
                f"CMS signer hash-algorithm size was invalid at index {signer_index}"
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
                f"CMS signer hash-algorithm read failed at index {signer_index}: "
                f"{_status_hex(ctypes.get_last_error())}"
            ) from None
        actual_size = int(read_size.value)
        if not (
            ctypes.sizeof(_CMSG_CMS_SIGNER_INFO_HASH_PREFIX) <= actual_size <= cms_signer_info_size
        ):
            raise RuntimeError(
                f"CMS signer hash-algorithm size changed at index {signer_index}"
            ) from None
        prefix = ctypes.cast(
            cms_signer_info_buffer,
            ctypes.POINTER(_CMSG_CMS_SIGNER_INFO_HASH_PREFIX),
        ).contents
        if int(prefix.dwVersion) != _CMSG_SIGNER_INFO_V1:
            raise RuntimeError(
                f"unsupported CMS signer hash-algorithm version at index {signer_index}"
            ) from None
        return self._copy_algorithm_identifier(
            prefix.HashAlgorithm,
            cms_signer_info_buffer,
            actual_size,
            "CMS signer",
            signer_index,
        )

    def _read_dedicated_signer_hash_algorithm(
        self,
        message_handle: wintypes.HANDLE,
        signer_index: int,
    ) -> _HashAlgorithm:
        queried_size = wintypes.DWORD()
        if not self._crypt_msg_get_param(
            message_handle,
            _CMSG_SIGNER_HASH_ALGORITHM_PARAM,
            signer_index,
            ctypes.c_void_p(),
            ctypes.byref(queried_size),
        ):
            raise RuntimeError(
                f"dedicated signer hash-algorithm query failed at index {signer_index}: "
                f"{_status_hex(ctypes.get_last_error())}"
            ) from None
        hash_algorithm_size = int(queried_size.value)
        if not (
            ctypes.sizeof(_CRYPT_ALGORITHM_IDENTIFIER)
            <= hash_algorithm_size
            <= _MAX_HASH_ALGORITHM_BYTES
        ):
            raise RuntimeError(
                f"dedicated signer hash-algorithm size was invalid at index {signer_index}"
            ) from None

        hash_algorithm_buffer = ctypes.create_string_buffer(hash_algorithm_size)
        read_size = wintypes.DWORD(hash_algorithm_size)
        if not self._crypt_msg_get_param(
            message_handle,
            _CMSG_SIGNER_HASH_ALGORITHM_PARAM,
            signer_index,
            hash_algorithm_buffer,
            ctypes.byref(read_size),
        ):
            raise RuntimeError(
                f"dedicated signer hash-algorithm read failed at index {signer_index}: "
                f"{_status_hex(ctypes.get_last_error())}"
            ) from None
        actual_size = int(read_size.value)
        if not (ctypes.sizeof(_CRYPT_ALGORITHM_IDENTIFIER) <= actual_size <= hash_algorithm_size):
            raise RuntimeError(
                f"dedicated signer hash-algorithm size changed at index {signer_index}"
            ) from None
        algorithm = ctypes.cast(
            hash_algorithm_buffer,
            ctypes.POINTER(_CRYPT_ALGORITHM_IDENTIFIER),
        ).contents
        return self._copy_algorithm_identifier(
            algorithm,
            hash_algorithm_buffer,
            actual_size,
            "dedicated signer",
            signer_index,
        )

    @staticmethod
    def _copy_algorithm_identifier(
        algorithm: _CRYPT_ALGORITHM_IDENTIFIER,
        owner_buffer: ctypes.Array[ctypes.c_char],
        actual_size: int,
        role: str,
        signer_index: int,
    ) -> _HashAlgorithm:
        owner_start = ctypes.addressof(owner_buffer)
        owner_end = owner_start + actual_size
        oid_address = cast(int | None, algorithm.pszObjId)
        if not oid_address or not owner_start <= oid_address < owner_end:
            raise RuntimeError(
                f"{role} algorithm OID pointer escaped its owning buffer at index {signer_index}"
            ) from None
        oid_extent = min(_MAX_ALGORITHM_OID_BYTES + 1, owner_end - oid_address)
        oid_region = ctypes.string_at(oid_address, oid_extent)
        terminator = oid_region.find(b"\0")
        if terminator < 0:
            raise RuntimeError(
                f"{role} algorithm OID was not terminated inside its owning buffer at "
                f"index {signer_index}"
            ) from None
        oid_bytes = oid_region[:terminator]
        if not oid_bytes or len(oid_bytes) > _MAX_ALGORITHM_OID_BYTES:
            raise RuntimeError(
                f"{role} algorithm OID size was invalid at index {signer_index}"
            ) from None
        try:
            oid = oid_bytes.decode("ascii")
        except UnicodeDecodeError:
            raise RuntimeError(
                f"{role} algorithm OID was malformed at index {signer_index}"
            ) from None
        if _OID_PATTERN.fullmatch(oid) is None:
            raise RuntimeError(
                f"{role} algorithm OID was malformed at index {signer_index}"
            ) from None

        parameter_size = int(algorithm.Parameters.cbData)
        if not 0 <= parameter_size <= _MAX_ALGORITHM_PARAMETER_BYTES:
            raise RuntimeError(
                f"{role} algorithm parameter size was invalid at index {signer_index}"
            ) from None
        if parameter_size == 0:
            parameters = b""
        else:
            parameter_address = ctypes.cast(
                algorithm.Parameters.pbData,
                ctypes.c_void_p,
            ).value
            if (
                not parameter_address
                or parameter_address < owner_start
                or parameter_address > owner_end - parameter_size
            ):
                raise RuntimeError(
                    f"{role} algorithm parameters escaped their owning buffer at "
                    f"index {signer_index}"
                ) from None
            parameters = ctypes.string_at(parameter_address, parameter_size)
        return _HashAlgorithm(oid=oid, parameters=parameters)


def test_git_cms_signer_hash_algorithms_match_across_complete_m234_boundary() -> None:
    real_which = _commit_module.shutil.which
    with patch.object(
        _commit_module.shutil,
        "which",
        side_effect=real_which,
    ) as initial_lookup:
        git_executable = _commit_module._git_executable()  # pyright: ignore[reportPrivateUsage]
    assert initial_lookup.call_count == 1

    verifier = _AuthenticodeCmsSignerHashAlgorithmVerifier()
    with _RetainedGitExecutableFile(git_executable) as retained:
        before_file = retained.snapshot()
        before_hash_algorithm = verifier.observe(git_executable, retained.handle)
        with patch.object(
            _commit_module.shutil,
            "which",
            return_value=str(git_executable),
        ) as lookup:
            _m234_module.test_git_cms_signer_info_certificate_ids_match_across_the_complete_m233_boundary()
        assert lookup.call_count == 1
        _verify_image_stable(before_file, retained.snapshot())
        after_hash_algorithm = verifier.observe(git_executable, retained.handle)
        assert after_hash_algorithm == before_hash_algorithm


@dataclass(frozen=True, slots=True)
class _FakeHashAlgorithm:
    oid: bytes
    parameters: bytes = b""


class _FakeCmsSignerHashAlgorithmMaterial(_FakeCmsSignerInfoCertificateIdMaterial):
    def __init__(
        self,
        identifiers: tuple[tuple[bytes, bytes], ...] = (
            (b"issuer-a", b"serial-a"),
            (b"issuer-b", b"serial-b"),
        ),
        *,
        cms_algorithms: tuple[_FakeHashAlgorithm, ...] | None = None,
        dedicated_algorithms: tuple[_FakeHashAlgorithm, ...] | None = None,
    ) -> None:
        super().__init__(identifiers)
        defaults = (_FakeHashAlgorithm(b"2.16.840.1.101.3.4.2.1"),) * len(identifiers)
        self.cms_algorithms = defaults if cms_algorithms is None else cms_algorithms
        self.dedicated_algorithms = (
            self.cms_algorithms if dedicated_algorithms is None else dedicated_algorithms
        )
        if not (len(self.cms_algorithms) == len(self.dedicated_algorithms) == len(identifiers)):
            raise ValueError("fake signer hash-algorithm sequences must have equal counts")
        self.hash_calls: list[tuple[int, int, bool]] = []
        self.cms_extension_query_failure_index: int | None = None
        self.cms_extension_read_failure_index: int | None = None
        self.dedicated_query_failure_index: int | None = None
        self.dedicated_read_failure_index: int | None = None
        self.cms_extension_query_size_override: int | None = None
        self.cms_extension_read_size_override: int | None = None
        self.dedicated_query_size_override: int | None = None
        self.dedicated_read_size_override: int | None = None
        self.cms_oid_mode = "valid"
        self.cms_parameter_mode = "valid"

    def get_message_parameter(
        self,
        message_handle: object,
        parameter: int,
        index: int,
        output: object,
        size_pointer: object,
    ) -> bool:
        if parameter not in (
            _CMSG_CMS_SIGNER_INFO_PARAM,
            _CMSG_SIGNER_HASH_ALGORITHM_PARAM,
        ):
            return super().get_message_parameter(
                message_handle,
                parameter,
                index,
                output,
                size_pointer,
            )
        signer_index = int(index)
        is_read = bool(output)
        if not 0 <= signer_index < len(self.cms_algorithms):
            return False
        same_calls = sum(
            1
            for prior_parameter, prior_index, _ in self.hash_calls
            if prior_parameter == parameter and prior_index == signer_index
        )
        is_cms_extension = parameter == _CMSG_CMS_SIGNER_INFO_PARAM and same_calls >= 2
        self.hash_calls.append((parameter, signer_index, is_read))
        size = ctypes.cast(
            cast(int, size_pointer),
            ctypes.POINTER(wintypes.DWORD),
        ).contents
        if parameter == _CMSG_CMS_SIGNER_INFO_PARAM:
            algorithm = self.cms_algorithms[signer_index]
            structure_size = ctypes.sizeof(_CMSG_CMS_SIGNER_INFO_HASH_PREFIX)
            query_override = self.cms_extension_query_size_override if is_cms_extension else None
            read_override = self.cms_extension_read_size_override if is_cms_extension else None
            if (
                is_cms_extension
                and not is_read
                and signer_index == self.cms_extension_query_failure_index
            ):
                return False
            if (
                is_cms_extension
                and is_read
                and signer_index == self.cms_extension_read_failure_index
            ):
                return False
        else:
            algorithm = self.dedicated_algorithms[signer_index]
            structure_size = ctypes.sizeof(_CRYPT_ALGORITHM_IDENTIFIER)
            query_override = self.dedicated_query_size_override
            read_override = self.dedicated_read_size_override
            if not is_read and signer_index == self.dedicated_query_failure_index:
                return False
            if is_read and signer_index == self.dedicated_read_failure_index:
                return False
        required = structure_size + len(algorithm.oid) + 1 + len(algorithm.parameters)
        if not is_read:
            size.value = required if query_override is None else query_override
            return True
        size.value = required if read_override is None else read_override
        self._write_algorithm(
            output,
            parameter,
            signer_index,
            algorithm,
            required,
            is_cms_extension,
        )
        return True

    def _write_algorithm(
        self,
        output: object,
        parameter: int,
        signer_index: int,
        algorithm: _FakeHashAlgorithm,
        required: int,
        is_cms_extension: bool,
    ) -> None:
        output_value = cast(int, output)
        output_address = cast(int, ctypes.cast(output_value, ctypes.c_void_p).value)
        if parameter == _CMSG_CMS_SIGNER_INFO_PARAM:
            prefix = ctypes.cast(
                output_value,
                ctypes.POINTER(_CMSG_CMS_SIGNER_INFO_HASH_PREFIX),
            ).contents
            source = self.cms_signer_infos[signer_index].prefix
            prefix.dwVersion = source.dwVersion
            prefix.SignerId = source.SignerId
            target = prefix.HashAlgorithm
            structure_size = ctypes.sizeof(_CMSG_CMS_SIGNER_INFO_HASH_PREFIX)
        else:
            target = ctypes.cast(
                output_value,
                ctypes.POINTER(_CRYPT_ALGORITHM_IDENTIFIER),
            ).contents
            structure_size = ctypes.sizeof(_CRYPT_ALGORITHM_IDENTIFIER)
        oid_address = output_address + structure_size
        oid_payload = algorithm.oid + b"\0"
        if is_cms_extension and self.cms_oid_mode == "escaped":
            oid_address = output_address + required + 8
        elif is_cms_extension and self.cms_oid_mode == "unterminated":
            oid_payload = algorithm.oid + b"X"
        elif is_cms_extension and self.cms_oid_mode == "malformed":
            oid_payload = b"not-an-oid\0"
        target.pszObjId = oid_address
        if self.cms_oid_mode != "escaped" or not is_cms_extension:
            ctypes.memmove(oid_address, oid_payload, len(oid_payload))
        parameter_address = output_address + structure_size + len(algorithm.oid) + 1
        target.Parameters.cbData = len(algorithm.parameters)
        if is_cms_extension and self.cms_parameter_mode == "escaped":
            parameter_address = output_address + required + 8
        elif is_cms_extension and self.cms_parameter_mode == "oversized":
            target.Parameters.cbData = _MAX_ALGORITHM_PARAMETER_BYTES + 1
        target.Parameters.pbData = ctypes.cast(
            parameter_address,
            ctypes.POINTER(wintypes.BYTE),
        )
        if algorithm.parameters and not (is_cms_extension and self.cms_parameter_mode == "escaped"):
            ctypes.memmove(parameter_address, algorithm.parameters, len(algorithm.parameters))


def _fake_verifier(
    wintrust: Callable[..., object],
    material: _FakeCmsSignerHashAlgorithmMaterial,
) -> _AuthenticodeCmsSignerHashAlgorithmVerifier:
    verifier = object.__new__(_AuthenticodeCmsSignerHashAlgorithmVerifier)
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
    material: _FakeCmsSignerHashAlgorithmMaterial,
) -> _CmsSignerHashAlgorithmObservation:
    return _fake_verifier(
        _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS),
        material,
    ).observe(Path("c:/git.exe"), 1)


def test_fake_signer_hash_algorithms_bind_oid_parameters_and_index() -> None:
    algorithms = (
        _FakeHashAlgorithm(b"2.16.840.1.101.3.4.2.1", b"\x05\x00"),
        _FakeHashAlgorithm(b"1.3.14.3.2.26"),
    )
    material = _FakeCmsSignerHashAlgorithmMaterial(cms_algorithms=algorithms)

    observation = _observe_material(material)

    expected = tuple(
        _HashAlgorithm(algorithm.oid.decode("ascii"), algorithm.parameters)
        for algorithm in algorithms
    )
    assert observation.hash_algorithm_oids == tuple(value.oid for value in expected)
    assert observation.hash_algorithm_parameter_sizes == (2, 0)
    assert observation.cms_hash_algorithm_sha256 == tuple(
        _hash_algorithm_sha256(value) for value in expected
    )
    assert observation.dedicated_hash_algorithm_sha256 == (observation.cms_hash_algorithm_sha256)
    assert material.hash_calls == [
        (_CMSG_CMS_SIGNER_INFO_PARAM, 0, False),
        (_CMSG_CMS_SIGNER_INFO_PARAM, 0, True),
        (_CMSG_CMS_SIGNER_INFO_PARAM, 1, False),
        (_CMSG_CMS_SIGNER_INFO_PARAM, 1, True),
        (_CMSG_CMS_SIGNER_INFO_PARAM, 0, False),
        (_CMSG_CMS_SIGNER_INFO_PARAM, 0, True),
        (_CMSG_SIGNER_HASH_ALGORITHM_PARAM, 0, False),
        (_CMSG_SIGNER_HASH_ALGORITHM_PARAM, 0, True),
        (_CMSG_CMS_SIGNER_INFO_PARAM, 1, False),
        (_CMSG_CMS_SIGNER_INFO_PARAM, 1, True),
        (_CMSG_SIGNER_HASH_ALGORITHM_PARAM, 1, False),
        (_CMSG_SIGNER_HASH_ALGORITHM_PARAM, 1, True),
    ]


def test_signer_hash_algorithm_observation_is_detached() -> None:
    algorithm = _FakeHashAlgorithm(b"1.2.840.113549.2.5", b"\x05\x00")
    material = _FakeCmsSignerHashAlgorithmMaterial(
        ((b"issuer", b"serial"),),
        cms_algorithms=(algorithm,),
    )
    observation = _observe_material(material)

    assert observation.hash_algorithm_oids == ("1.2.840.113549.2.5",)
    assert observation.hash_algorithm_parameter_sizes == (2,)


def test_copied_hash_algorithm_survives_owner_buffer_mutation() -> None:
    oid = b"1.2.840.113549.2.5"
    parameters = b"\x05\x00"
    structure_size = ctypes.sizeof(_CRYPT_ALGORITHM_IDENTIFIER)
    buffer = ctypes.create_string_buffer(structure_size + len(oid) + 1 + len(parameters))
    buffer_address = ctypes.addressof(buffer)
    algorithm = ctypes.cast(
        buffer,
        ctypes.POINTER(_CRYPT_ALGORITHM_IDENTIFIER),
    ).contents
    oid_address = buffer_address + structure_size
    parameter_address = oid_address + len(oid) + 1
    ctypes.memmove(oid_address, oid + b"\0", len(oid) + 1)
    ctypes.memmove(parameter_address, parameters, len(parameters))
    algorithm.pszObjId = oid_address
    algorithm.Parameters.cbData = len(parameters)
    algorithm.Parameters.pbData = ctypes.cast(
        parameter_address,
        ctypes.POINTER(wintypes.BYTE),
    )

    detached = _AuthenticodeCmsSignerHashAlgorithmVerifier._copy_algorithm_identifier(  # pyright: ignore[reportPrivateUsage]
        algorithm,
        buffer,
        ctypes.sizeof(buffer),
        "test",
        0,
    )
    ctypes.memset(oid_address, ord("X"), len(oid))
    ctypes.memset(parameter_address, ord("Y"), len(parameters))

    assert detached == _HashAlgorithm("1.2.840.113549.2.5", b"\x05\x00")


def test_equal_concatenated_hash_algorithm_bytes_with_different_boundaries_differ() -> None:
    first = _hash_algorithm_sha256(_HashAlgorithm("1.23", b"4"))
    second = _hash_algorithm_sha256(_HashAlgorithm("1.2", b"34"))

    assert first != second


def test_reversed_hash_algorithm_order_hashes_differently() -> None:
    first_algorithms = (
        _FakeHashAlgorithm(b"1.2.3"),
        _FakeHashAlgorithm(b"1.2.4"),
    )
    second_algorithms = tuple(reversed(first_algorithms))

    first = _observe_material(_FakeCmsSignerHashAlgorithmMaterial(cms_algorithms=first_algorithms))
    second = _observe_material(
        _FakeCmsSignerHashAlgorithmMaterial(cms_algorithms=second_algorithms)
    )

    assert first.hash_algorithm_sequence_sha256 != second.hash_algorithm_sequence_sha256


def test_fake_hash_algorithm_material_rejects_mismatched_counts() -> None:
    with pytest.raises(ValueError, match="hash-algorithm sequences must have equal counts"):
        _FakeCmsSignerHashAlgorithmMaterial(
            ((b"issuer", b"serial"),),
            cms_algorithms=(),
        )


@pytest.mark.parametrize(
    ("fault", "message"),
    [
        ("cms-query-failure", "CMS signer hash-algorithm query failed"),
        ("cms-empty-size", "CMS signer hash-algorithm size was invalid"),
        ("cms-oversized-size", "CMS signer hash-algorithm size was invalid"),
        ("cms-read-failure", "CMS signer hash-algorithm read failed"),
        ("cms-changed-size", "CMS signer hash-algorithm size changed"),
        ("dedicated-query-failure", "dedicated signer hash-algorithm query failed"),
        ("dedicated-empty-size", "dedicated signer hash-algorithm size was invalid"),
        ("dedicated-oversized-size", "dedicated signer hash-algorithm size was invalid"),
        ("dedicated-read-failure", "dedicated signer hash-algorithm read failed"),
        ("dedicated-changed-size", "dedicated signer hash-algorithm size changed"),
        ("escaped-oid", "algorithm OID pointer escaped its owning buffer"),
        ("unterminated-oid", "algorithm OID was not terminated inside its owning buffer"),
        ("malformed-oid", "algorithm OID was malformed"),
        ("escaped-parameters", "algorithm parameters escaped their owning buffer"),
        ("oversized-parameters", "algorithm parameter size was invalid"),
        ("representation-mismatch", "CMS and dedicated signer hash algorithms differed"),
    ],
)
def test_signer_hash_algorithm_faults_are_rejected(fault: str, message: str) -> None:
    material = _FakeCmsSignerHashAlgorithmMaterial(((b"issuer", b"serial"),))
    if fault == "cms-query-failure":
        material.cms_extension_query_failure_index = 0
    elif fault == "cms-empty-size":
        material.cms_extension_query_size_override = 0
    elif fault == "cms-oversized-size":
        material.cms_extension_query_size_override = _MAX_CMS_SIGNER_INFO_BYTES + 1
    elif fault == "cms-read-failure":
        material.cms_extension_read_failure_index = 0
    elif fault == "cms-changed-size":
        material.cms_extension_read_size_override = 0
    elif fault == "dedicated-query-failure":
        material.dedicated_query_failure_index = 0
    elif fault == "dedicated-empty-size":
        material.dedicated_query_size_override = 0
    elif fault == "dedicated-oversized-size":
        material.dedicated_query_size_override = _MAX_HASH_ALGORITHM_BYTES + 1
    elif fault == "dedicated-read-failure":
        material.dedicated_read_failure_index = 0
    elif fault == "dedicated-changed-size":
        material.dedicated_read_size_override = 0
    elif fault == "escaped-oid":
        material.cms_oid_mode = "escaped"
    elif fault == "unterminated-oid":
        material.cms_oid_mode = "unterminated"
    elif fault == "malformed-oid":
        material.cms_oid_mode = "malformed"
    elif fault == "escaped-parameters":
        material.cms_algorithms = (_FakeHashAlgorithm(b"1.2.3", b"x"),)
        material.dedicated_algorithms = material.cms_algorithms
        material.cms_parameter_mode = "escaped"
    elif fault == "oversized-parameters":
        material.cms_parameter_mode = "oversized"
    elif fault == "representation-mismatch":
        material.dedicated_algorithms = (_FakeHashAlgorithm(b"1.2.4"),)

    with pytest.raises(RuntimeError, match=message):
        _observe_material(material)


def test_hash_algorithm_failures_still_close_wintrust_state() -> None:
    material = _FakeCmsSignerHashAlgorithmMaterial(((b"issuer", b"serial"),))
    material.cms_oid_mode = "malformed"
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    verifier = _fake_verifier(wintrust, material)

    with pytest.raises(RuntimeError, match="algorithm OID was malformed"):
        verifier.observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]
