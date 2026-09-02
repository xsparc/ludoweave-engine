"""Bind encoded WinTrust message SignerInfo values around complete M229."""

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
    test_windows_contained_source_access_source_commit_git_countersigner_chain_binding_probe as _m229_module,
)
from tests.integration.test_windows_contained_source_access_source_commit_git_file_retention_probe import (
    _RetainedGitExecutableFile,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_contained_source_access_source_commit_git_signer_certificate_binding_probe import (
    _ERROR_SUCCESS,  # pyright: ignore[reportPrivateUsage]
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
    reason="M230 binds retained Git WinTrust encoded SignerInfo values",
)

_CMSG_SIGNER_COUNT_PARAM = 5
_CMSG_ENCODED_SIGNER = 28
_MAX_SIGNED_MESSAGE_SIGNERS = 16
_MAX_ENCODED_SIGNER_INFO_BYTES = 1_048_576
_MAX_SIGNED_MESSAGE_SIGNER_INFO_BYTES = 4_194_304
_SIGNED_MESSAGE_SIGNER_SEQUENCE_DOMAIN = b"ludoweave.wintrust-signed-message-signer-info/1\0"


class _CRYPT_PROVIDER_DATA_PREFIX(ctypes.Structure):
    _fields_ = [
        ("cbStruct", wintypes.DWORD),
        ("pWintrustData", ctypes.c_void_p),
        ("fOpenedFile", wintypes.BOOL),
        ("hWndParent", wintypes.HWND),
        ("pgActionID", ctypes.c_void_p),
        ("hProv", wintypes.HANDLE),
        ("dwError", wintypes.DWORD),
        ("dwRegSecuritySettings", wintypes.DWORD),
        ("dwRegPolicySettings", wintypes.DWORD),
        ("psPfns", ctypes.c_void_p),
        ("cdwTrustStepErrors", wintypes.DWORD),
        ("padwTrustStepErrors", ctypes.POINTER(wintypes.DWORD)),
        ("chStores", wintypes.DWORD),
        ("pahStores", ctypes.c_void_p),
        ("dwEncoding", wintypes.DWORD),
        ("hMsg", wintypes.HANDLE),
        ("csSigners", wintypes.DWORD),
    ]


@dataclass(frozen=True, slots=True)
class _SignedMessageSignerSequenceObservation:
    encoding_type: int
    provider_signer_count: int
    message_signer_count: int
    encoded_sizes: tuple[int, ...]
    signer_info_sha256: tuple[str, ...]
    signed_message_signer_sequence_sha256: str


class _AuthenticodeSignedMessageSignerInfoVerifier:
    """Own WinTrust state and detach each bounded encoded SignerInfo."""

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

        get_message_parameter = cast(_NativeFunction, crypt32.CryptMsgGetParam)
        get_message_parameter.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.DWORD,
            ctypes.c_void_p,
            ctypes.POINTER(wintypes.DWORD),
        ]
        get_message_parameter.restype = wintypes.BOOL

        self._win_verify_trust = verify
        self._provider_data_from_state = provider_data
        self._crypt_msg_get_param = get_message_parameter

    def observe(self, path: Path, handle: int) -> _SignedMessageSignerSequenceObservation:
        if not path.is_absolute() or handle <= 0:
            raise RuntimeError("retained Git signed-message input was invalid") from None

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
        observation: _SignedMessageSignerSequenceObservation | None = None
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
                    observation = self._read_signed_message(trust_data)
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
            raise RuntimeError("signed-message observation was unavailable") from None
        return observation

    def _read_signed_message(
        self, trust_data: _WINTRUST_DATA
    ) -> _SignedMessageSignerSequenceObservation:
        state_handle = trust_data.hWVTStateData
        if not state_handle:
            raise RuntimeError("signed-message provider data was unavailable") from None
        provider_address = cast(int | None, self._provider_data_from_state(state_handle))
        if not provider_address:
            raise RuntimeError("signed-message provider data was unavailable") from None

        provider = ctypes.cast(
            provider_address,
            ctypes.POINTER(_CRYPT_PROVIDER_DATA_PREFIX),
        ).contents
        if int(provider.cbStruct) < ctypes.sizeof(_CRYPT_PROVIDER_DATA_PREFIX):
            raise RuntimeError("signed-message provider structure was invalid") from None
        encoding_type = int(provider.dwEncoding)
        if encoding_type <= 0:
            raise RuntimeError("signed-message encoding was invalid") from None
        message_handle = provider.hMsg
        if not message_handle:
            raise RuntimeError("signed-message handle was unavailable") from None
        provider_signer_count = int(provider.csSigners)
        if not 1 <= provider_signer_count <= _MAX_SIGNED_MESSAGE_SIGNERS:
            raise RuntimeError("provider signer count was invalid") from None

        count = wintypes.DWORD()
        count_size = wintypes.DWORD(ctypes.sizeof(count))
        if not self._crypt_msg_get_param(
            message_handle,
            _CMSG_SIGNER_COUNT_PARAM,
            0,
            ctypes.byref(count),
            ctypes.byref(count_size),
        ):
            raise RuntimeError("signed-message signer count query failed") from None
        if int(count_size.value) != ctypes.sizeof(count):
            raise RuntimeError("signed-message signer count size was invalid") from None
        message_signer_count = int(count.value)
        if not 1 <= message_signer_count <= _MAX_SIGNED_MESSAGE_SIGNERS:
            raise RuntimeError("signed-message signer count was invalid") from None
        if message_signer_count != provider_signer_count:
            raise RuntimeError("provider and message signer counts differed") from None

        sequence_digest = hashlib.sha256(_SIGNED_MESSAGE_SIGNER_SEQUENCE_DOMAIN)
        sequence_digest.update(encoding_type.to_bytes(length=4, byteorder="big", signed=False))
        sequence_digest.update(
            provider_signer_count.to_bytes(length=4, byteorder="big", signed=False)
        )
        sequence_digest.update(
            message_signer_count.to_bytes(length=4, byteorder="big", signed=False)
        )
        encoded_sizes: list[int] = []
        signer_hashes: list[str] = []
        total_encoded_size = 0
        for signer_index in range(message_signer_count):
            requested_size = wintypes.DWORD()
            if not self._crypt_msg_get_param(
                message_handle,
                _CMSG_ENCODED_SIGNER,
                signer_index,
                None,
                ctypes.byref(requested_size),
            ):
                raise RuntimeError(
                    f"encoded SignerInfo size query failed at index {signer_index}"
                ) from None
            encoded_size = int(requested_size.value)
            if not 1 <= encoded_size <= _MAX_ENCODED_SIGNER_INFO_BYTES:
                raise RuntimeError(
                    f"encoded SignerInfo size was invalid at index {signer_index}"
                ) from None
            if total_encoded_size > _MAX_SIGNED_MESSAGE_SIGNER_INFO_BYTES - encoded_size:
                raise RuntimeError("encoded SignerInfo total was invalid") from None

            buffer = (wintypes.BYTE * encoded_size)()
            actual_size = wintypes.DWORD(requested_size.value)
            if not self._crypt_msg_get_param(
                message_handle,
                _CMSG_ENCODED_SIGNER,
                signer_index,
                buffer,
                ctypes.byref(actual_size),
            ):
                raise RuntimeError(
                    f"encoded SignerInfo read failed at index {signer_index}"
                ) from None
            if int(actual_size.value) != encoded_size:
                raise RuntimeError(
                    f"encoded SignerInfo size changed at index {signer_index}"
                ) from None
            encoded = ctypes.string_at(buffer, encoded_size)
            total_encoded_size += encoded_size
            encoded_sizes.append(encoded_size)
            signer_hashes.append(hashlib.sha256(encoded).hexdigest())
            sequence_digest.update(signer_index.to_bytes(length=4, byteorder="big", signed=False))
            sequence_digest.update(encoded_size.to_bytes(length=8, byteorder="big", signed=False))
            sequence_digest.update(encoded)

        return _SignedMessageSignerSequenceObservation(
            encoding_type=encoding_type,
            provider_signer_count=provider_signer_count,
            message_signer_count=message_signer_count,
            encoded_sizes=tuple(encoded_sizes),
            signer_info_sha256=tuple(signer_hashes),
            signed_message_signer_sequence_sha256=sequence_digest.hexdigest(),
        )


def test_git_signed_message_signer_info_matches_across_the_complete_m229_boundary() -> None:
    real_which = _commit_module.shutil.which
    with patch.object(
        _commit_module.shutil,
        "which",
        side_effect=real_which,
    ) as initial_lookup:
        git_executable = _commit_module._git_executable()  # pyright: ignore[reportPrivateUsage]
    assert initial_lookup.call_count == 1

    verifier = _AuthenticodeSignedMessageSignerInfoVerifier()
    with _RetainedGitExecutableFile(git_executable) as retained:
        before_file = retained.snapshot()
        before_signers = verifier.observe(git_executable, retained.handle)
        with patch.object(
            _commit_module.shutil,
            "which",
            return_value=str(git_executable),
        ) as lookup:
            _m229_module.test_git_countersigner_chains_match_across_the_complete_m228_boundary()
        assert lookup.call_count == 1
        _verify_image_stable(before_file, retained.snapshot())
        after_signers = verifier.observe(git_executable, retained.handle)
        assert after_signers == before_signers


class _FakeSignedMessageMaterial:
    def __init__(self, encoded_signers: tuple[bytes, ...] = (b"abc", b"defg")) -> None:
        self.encoded_signers = [bytearray(value) for value in encoded_signers]
        self.provider = _CRYPT_PROVIDER_DATA_PREFIX()
        self.provider.cbStruct = ctypes.sizeof(_CRYPT_PROVIDER_DATA_PREFIX)
        self.provider.dwEncoding = 0x00010001
        self.provider.hMsg = wintypes.HANDLE(1)
        self.provider.csSigners = len(encoded_signers)
        self.message_signer_count = len(encoded_signers)
        self.count_size = ctypes.sizeof(wintypes.DWORD())
        self.count_query_succeeds = True
        self.size_query_failure_index: int | None = None
        self.read_failure_index: int | None = None
        self.reported_sizes: dict[int, int] = {}
        self.returned_sizes: dict[int, int] = {}
        self.calls: list[tuple[int, int, bool]] = []

    def provider_data(self, *_arguments: object) -> int:
        return ctypes.addressof(self.provider)

    def get_message_parameter(
        self,
        _message_handle: object,
        parameter: int,
        index: int,
        output: object,
        size_pointer: object,
    ) -> bool:
        size = ctypes.cast(cast(int, size_pointer), ctypes.POINTER(wintypes.DWORD))
        is_size_query = output is None
        self.calls.append((parameter, index, is_size_query))
        if parameter == _CMSG_SIGNER_COUNT_PARAM:
            if not self.count_query_succeeds:
                return False
            ctypes.cast(
                cast(int, output), ctypes.POINTER(wintypes.DWORD)
            ).contents.value = self.message_signer_count
            size.contents.value = self.count_size
            return True
        if parameter != _CMSG_ENCODED_SIGNER or not 0 <= index < len(self.encoded_signers):
            return False

        encoded = self.encoded_signers[index]
        reported_size = self.reported_sizes.get(index, len(encoded))
        if is_size_query:
            if self.size_query_failure_index == index:
                return False
            size.contents.value = reported_size
            return True
        if self.read_failure_index == index:
            return False
        copy_size = min(len(encoded), reported_size)
        ctypes.memmove(output, bytes(encoded), copy_size)  # pyright: ignore[reportArgumentType]
        size.contents.value = self.returned_sizes.get(index, reported_size)
        return True


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


def _missing_native_value(*_arguments: object) -> None:
    return None


def _fake_verifier(
    wintrust: Callable[..., object],
    *,
    provider_data: Callable[..., object],
    get_message_parameter: Callable[..., object],
) -> _AuthenticodeSignedMessageSignerInfoVerifier:
    verifier = object.__new__(_AuthenticodeSignedMessageSignerInfoVerifier)
    vars(verifier)["_win_verify_trust"] = _FakeNativeFunction(wintrust)
    vars(verifier)["_provider_data_from_state"] = _FakeNativeFunction(provider_data)
    vars(verifier)["_crypt_msg_get_param"] = _FakeNativeFunction(get_message_parameter)
    return verifier


def _expected_sequence_hash(encoding_type: int, values: tuple[bytes, ...]) -> str:
    digest = hashlib.sha256(_SIGNED_MESSAGE_SIGNER_SEQUENCE_DOMAIN)
    digest.update(encoding_type.to_bytes(length=4, byteorder="big", signed=False))
    digest.update(len(values).to_bytes(length=4, byteorder="big", signed=False))
    digest.update(len(values).to_bytes(length=4, byteorder="big", signed=False))
    for index, value in enumerate(values):
        digest.update(index.to_bytes(length=4, byteorder="big", signed=False))
        digest.update(len(value).to_bytes(length=8, byteorder="big", signed=False))
        digest.update(value)
    return digest.hexdigest()


def _observe_material(
    material: _FakeSignedMessageMaterial,
    *,
    wintrust: Callable[..., object] | None = None,
) -> _SignedMessageSignerSequenceObservation:
    selected_wintrust = wintrust or _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    return _fake_verifier(
        selected_wintrust,
        provider_data=material.provider_data,
        get_message_parameter=material.get_message_parameter,
    ).observe(Path("c:/git.exe"), 1)


def test_fake_signed_message_observation_binds_exact_sequence() -> None:
    values = (b"abc", b"defg")
    material = _FakeSignedMessageMaterial(values)

    observation = _observe_material(material)

    assert observation == _SignedMessageSignerSequenceObservation(
        encoding_type=0x00010001,
        provider_signer_count=2,
        message_signer_count=2,
        encoded_sizes=(3, 4),
        signer_info_sha256=tuple(hashlib.sha256(value).hexdigest() for value in values),
        signed_message_signer_sequence_sha256=_expected_sequence_hash(0x00010001, values),
    )
    assert material.calls == [
        (_CMSG_SIGNER_COUNT_PARAM, 0, False),
        (_CMSG_ENCODED_SIGNER, 0, True),
        (_CMSG_ENCODED_SIGNER, 0, False),
        (_CMSG_ENCODED_SIGNER, 1, True),
        (_CMSG_ENCODED_SIGNER, 1, False),
    ]


def test_equal_concatenated_signer_bytes_with_different_boundaries_hash_differently() -> None:
    first = _observe_material(_FakeSignedMessageMaterial((b"ab", b"c")))
    second = _observe_material(_FakeSignedMessageMaterial((b"a", b"bc")))

    assert b"ab" + b"c" == b"a" + b"bc"
    assert first.signed_message_signer_sequence_sha256 != (
        second.signed_message_signer_sequence_sha256
    )


def test_reversed_signer_order_hashes_differently() -> None:
    first = _observe_material(_FakeSignedMessageMaterial((b"first", b"second")))
    second = _observe_material(_FakeSignedMessageMaterial((b"second", b"first")))

    assert first.signed_message_signer_sequence_sha256 != (
        second.signed_message_signer_sequence_sha256
    )


def test_observation_is_detached_from_native_buffers() -> None:
    material = _FakeSignedMessageMaterial((b"abc",))
    observation = _observe_material(material)

    material.encoded_signers[0][:] = b"xyz"

    assert observation.encoded_sizes == (3,)
    assert observation.signer_info_sha256 == (hashlib.sha256(b"abc").hexdigest(),)


@pytest.mark.parametrize(
    ("path", "handle"),
    [(Path("git.exe"), 1), (Path("c:/git.exe"), 0), (Path("c:/git.exe"), -1)],
)
def test_invalid_signed_message_inputs_are_rejected(path: Path, handle: int) -> None:
    material = _FakeSignedMessageMaterial((b"abc",))
    verifier = _fake_verifier(
        _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS),
        provider_data=material.provider_data,
        get_message_parameter=material.get_message_parameter,
    )

    with pytest.raises(RuntimeError, match="signed-message input was invalid"):
        verifier.observe(path, handle)


def test_missing_provider_state_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrustWithoutState()
    material = _FakeSignedMessageMaterial((b"abc",))

    with pytest.raises(RuntimeError, match="signed-message provider data was unavailable"):
        _fake_verifier(
            wintrust,
            provider_data=material.provider_data,
            get_message_parameter=material.get_message_parameter,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_missing_provider_data_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)

    with pytest.raises(RuntimeError, match="signed-message provider data was unavailable"):
        _fake_verifier(
            wintrust,
            provider_data=_missing_native_value,
            get_message_parameter=_missing_native_value,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


@pytest.mark.parametrize(
    ("fault", "message"),
    [
        ("short-provider", "signed-message provider structure was invalid"),
        ("empty-encoding", "signed-message encoding was invalid"),
        ("missing-message", "signed-message handle was unavailable"),
        ("empty-provider-count", "provider signer count was invalid"),
        ("oversized-provider-count", "provider signer count was invalid"),
        ("count-query-failure", "signed-message signer count query failed"),
        ("count-size", "signed-message signer count size was invalid"),
        ("empty-message-count", "signed-message signer count was invalid"),
        ("oversized-message-count", "signed-message signer count was invalid"),
        ("count-mismatch", "provider and message signer counts differed"),
        ("size-query-failure", "encoded SignerInfo size query failed"),
        ("empty-signer", "encoded SignerInfo size was invalid"),
        ("oversized-signer", "encoded SignerInfo size was invalid"),
        ("read-failure", "encoded SignerInfo read failed"),
        ("changed-size", "encoded SignerInfo size changed"),
    ],
)
def test_invalid_signed_message_material_still_closes_provider_state(
    fault: str, message: str
) -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)
    material = _FakeSignedMessageMaterial((b"abc",))
    if fault == "short-provider":
        material.provider.cbStruct = ctypes.sizeof(_CRYPT_PROVIDER_DATA_PREFIX) - 1
    elif fault == "empty-encoding":
        material.provider.dwEncoding = 0
    elif fault == "missing-message":
        material.provider.hMsg = wintypes.HANDLE()
    elif fault == "empty-provider-count":
        material.provider.csSigners = 0
    elif fault == "oversized-provider-count":
        material.provider.csSigners = _MAX_SIGNED_MESSAGE_SIGNERS + 1
    elif fault == "count-query-failure":
        material.count_query_succeeds = False
    elif fault == "count-size":
        material.count_size = 0
    elif fault == "empty-message-count":
        material.message_signer_count = 0
    elif fault == "oversized-message-count":
        material.message_signer_count = _MAX_SIGNED_MESSAGE_SIGNERS + 1
    elif fault == "count-mismatch":
        material.provider.csSigners = 2
    elif fault == "size-query-failure":
        material.size_query_failure_index = 0
    elif fault == "empty-signer":
        material.reported_sizes[0] = 0
    elif fault == "oversized-signer":
        material.reported_sizes[0] = _MAX_ENCODED_SIGNER_INFO_BYTES + 1
    elif fault == "read-failure":
        material.read_failure_index = 0
    elif fault == "changed-size":
        material.returned_sizes[0] = 2
    else:
        raise AssertionError(f"unexpected signed-message fault: {fault}")

    with pytest.raises(RuntimeError, match=message):
        _fake_verifier(
            wintrust,
            provider_data=material.provider_data,
            get_message_parameter=material.get_message_parameter,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_complete_signer_info_sequence_total_is_bounded() -> None:
    value = b"x" * _MAX_ENCODED_SIGNER_INFO_BYTES
    material = _FakeSignedMessageMaterial((value, value, value, value, value))
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _ERROR_SUCCESS)

    with pytest.raises(RuntimeError, match="encoded SignerInfo total was invalid"):
        _fake_verifier(
            wintrust,
            provider_data=material.provider_data,
            get_message_parameter=material.get_message_parameter,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_rejected_trust_still_closes_provider_state() -> None:
    wintrust = _FakeWinTrust(_signed_status(_TRUST_E_BAD_DIGEST), _ERROR_SUCCESS)

    with pytest.raises(RuntimeError, match="0x80096010"):
        _fake_verifier(
            wintrust,
            provider_data=_missing_native_value,
            get_message_parameter=_missing_native_value,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]


def test_state_close_failure_after_signer_info_observation_is_reported() -> None:
    wintrust = _FakeWinTrust(_ERROR_SUCCESS, _signed_status(_TRUST_E_BAD_DIGEST))
    material = _FakeSignedMessageMaterial((b"abc",))

    with pytest.raises(RuntimeError, match="trust provider state close failed"):
        _fake_verifier(
            wintrust,
            provider_data=material.provider_data,
            get_message_parameter=material.get_message_parameter,
        ).observe(Path("c:/git.exe"), 1)

    assert wintrust.calls == [_WTD_STATEACTION_VERIFY, _WTD_STATEACTION_CLOSE]
