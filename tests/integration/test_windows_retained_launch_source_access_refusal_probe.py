"""Test-only Windows retained launch-source access-refusal probe."""

from __future__ import annotations

import ctypes
import sys
from collections.abc import Callable
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import pytest

from tests.integration.test_windows_local_control_channel_probe import (
    _DIRECT_PYTHON,  # pyright: ignore[reportPrivateUsage]
    _PARTICIPANT,  # pyright: ignore[reportPrivateUsage]
    _canonical_document,  # pyright: ignore[reportPrivateUsage]
    _challenge,  # pyright: ignore[reportPrivateUsage]
    _start_or_skip,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_local_control_token_binding_probe import (
    _NativeSessionBinding,  # pyright: ignore[reportPrivateUsage]
    _RetainedTokenBinding,  # pyright: ignore[reportPrivateUsage]
    _verify_same_logon,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_local_control_token_binding_probe import (
    _verify_stable as _verify_token_stable,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_launch_source_binding_probe import (
    _GENERIC_WRITE,  # pyright: ignore[reportPrivateUsage]
    _InheritedLaunchSource,  # pyright: ignore[reportPrivateUsage]
    _InheritedNullHandle,  # pyright: ignore[reportPrivateUsage]
    _RetainedLaunchSourceControlProbe,  # pyright: ignore[reportPrivateUsage]
    _verify_source_stable,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _FILE_ATTRIBUTE_NORMAL,  # pyright: ignore[reportPrivateUsage]
    _FILE_SHARE_DELETE,  # pyright: ignore[reportPrivateUsage]
    _FILE_SHARE_READ,  # pyright: ignore[reportPrivateUsage]
    _FILE_SHARE_WRITE,  # pyright: ignore[reportPrivateUsage]
    _INVALID_HANDLE_VALUE,  # pyright: ignore[reportPrivateUsage]
    _OPEN_EXISTING,  # pyright: ignore[reportPrivateUsage]
    _ImageApi,  # pyright: ignore[reportPrivateUsage]
    _RetainedImageFile,  # pyright: ignore[reportPrivateUsage]
    _RetainedProcessImage,  # pyright: ignore[reportPrivateUsage]
    _verify_expected_image,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _verify_stable as _verify_image_stable,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M216 probes native Windows retained launch-source access refusal",
)

_DELETE = 0x00010000
_ERROR_SHARING_VIOLATION = 32
_COMPETING_SHARE_MODE = _FILE_SHARE_READ | _FILE_SHARE_WRITE | _FILE_SHARE_DELETE


@dataclass(frozen=True, slots=True)
class _OpenResult:
    handle: int | None
    error_code: int


class _SourceAccessApi:
    """Issue access-only CreateFileW requests and close successful handles."""

    def __init__(self) -> None:
        self._api = _ImageApi()
        self._set_last_error = cast(Callable[[int], None], vars(ctypes)["set_last_error"])

    def open(self, path: str | Path, desired_access: int) -> _OpenResult:
        self._set_last_error(0)
        raw = cast(
            wintypes.HANDLE,
            self._api.create_file(
                str(path),
                desired_access,
                _COMPETING_SHARE_MODE,
                None,
                _OPEN_EXISTING,
                _FILE_ATTRIBUTE_NORMAL,
                wintypes.HANDLE(),
            ),
        )
        value = raw if isinstance(raw, int) else raw.value
        error_code = self._api.get_last_error()
        if value is None or value == 0 or value == _INVALID_HANDLE_VALUE:
            return _OpenResult(None, error_code)
        return _OpenResult(value, error_code)

    def close(self, handle: int) -> None:
        if not cast(bool, self._api.close_handle(wintypes.HANDLE(handle))):
            raise self._api.fail("CloseHandle") from None


def _require_refused_result(
    result: _OpenResult,
    *,
    access_name: str,
    phase: str,
    close_handle: Callable[[int], None],
) -> None:
    handle = result.handle
    if handle is not None:
        close_handle(handle)
        raise RuntimeError(
            f"{access_name} competing source access unexpectedly succeeded during {phase}"
        ) from None
    if result.error_code != _ERROR_SHARING_VIOLATION:
        raise RuntimeError(
            f"{access_name} competing source access returned an unexpected native category"
        ) from None


def _require_allowed_result(
    result: _OpenResult,
    *,
    access_name: str,
    close_handle: Callable[[int], None],
) -> None:
    handle = result.handle
    if handle is None:
        raise RuntimeError(f"{access_name} competing source access did not settle") from None
    close_handle(handle)


def _require_source_access_refused(path: str | Path, *, phase: str) -> None:
    api = _SourceAccessApi()
    for access_name, desired_access in (("write", _GENERIC_WRITE), ("delete", _DELETE)):
        _require_refused_result(
            api.open(path, desired_access),
            access_name=access_name,
            phase=phase,
            close_handle=api.close,
        )


def _require_source_access_allowed(path: str | Path) -> None:
    api = _SourceAccessApi()
    for access_name, desired_access in (("write", _GENERIC_WRITE), ("delete", _DELETE)):
        _require_allowed_result(
            api.open(path, desired_access),
            access_name=access_name,
            close_handle=api.close,
        )


def test_retained_launch_source_refuses_competing_access() -> None:
    with (
        _InheritedLaunchSource(_PARTICIPANT) as source_file,
        _InheritedNullHandle() as output_handle,
        _InheritedNullHandle() as error_handle,
    ):
        probe = _RetainedLaunchSourceControlProbe(source_file, output_handle, error_handle)
        with probe, _RetainedImageFile(_DIRECT_PYTHON) as expected_image_file:
            source_before = source_file.snapshot()
            expected_image = expected_image_file.snapshot()
            _require_source_access_refused(_PARTICIPANT, phase="before_launch")
            session = _start_or_skip(probe)
            _require_source_access_refused(_PARTICIPANT, phase="after_connection")
            output_handle.close()
            error_handle.close()
            with (
                _RetainedTokenBinding(0) as controller_binding,
                _RetainedTokenBinding(session.process) as participant_binding,
                _RetainedProcessImage(session.process) as observed_image,
            ):
                controller = controller_binding.snapshot()
                participant = participant_binding.snapshot()
                _verify_same_logon(controller, participant)
                _NativeSessionBinding().verify(session.pipe, session.pid, participant)
                participant_logon_sid = ctypes.create_string_buffer(participant.logon_sid)
                probe._verify_pipe_dacl(  # pyright: ignore[reportPrivateUsage]
                    session.pipe, ctypes.addressof(participant_logon_sid)
                )
                image_before = observed_image.snapshot()
                _verify_expected_image(expected_image, image_before)
                _challenge(probe, session)
                _require_source_access_refused(_PARTICIPANT, phase="after_ready")
                _verify_token_stable(participant, participant_binding.snapshot())
                _verify_image_stable(expected_image, expected_image_file.snapshot())
                _verify_image_stable(image_before, observed_image.snapshot())
                _verify_source_stable(source_before, source_file.snapshot())
                probe.write_document(
                    session.pipe,
                    _canonical_document("release", session.challenge, 2),
                )
                released = probe.read_document(session.pipe)
                assert released == _canonical_document("released", session.challenge, 3)
            probe.settle(session, 0)
        assert probe.owned_count == 0
    _require_source_access_allowed(_PARTICIPANT)
    with _RetainedImageFile(_PARTICIPANT) as post_file:
        _verify_source_stable(source_before, post_file.snapshot())


def test_unexpected_competing_access_success_closes_before_failure() -> None:
    closed: list[int] = []
    with pytest.raises(RuntimeError, match="unexpectedly succeeded"):
        _require_refused_result(
            _OpenResult(7, 0),
            access_name="write",
            phase="synthetic",
            close_handle=closed.append,
        )
    assert closed == [7]


@pytest.mark.parametrize("error_code", [0, 1, 5, 33, 87])
def test_nonsharing_native_error_fails_closed(error_code: int) -> None:
    with pytest.raises(RuntimeError, match="unexpected native category"):
        _require_refused_result(
            _OpenResult(None, error_code),
            access_name="delete",
            phase="synthetic",
            close_handle=lambda _handle: None,
        )


def test_exact_sharing_violation_is_accepted() -> None:
    _require_refused_result(
        _OpenResult(None, _ERROR_SHARING_VIOLATION),
        access_name="write",
        phase="synthetic",
        close_handle=lambda _handle: None,
    )


def test_allowed_access_closes_each_handle() -> None:
    closed: list[int] = []
    _require_allowed_result(_OpenResult(11, 0), access_name="delete", close_handle=closed.append)
    assert closed == [11]


@pytest.mark.parametrize("error_code", [0, 5, _ERROR_SHARING_VIOLATION])
def test_missing_post_settlement_access_fails_closed(error_code: int) -> None:
    with pytest.raises(RuntimeError, match="did not settle"):
        _require_allowed_result(
            _OpenResult(None, error_code),
            access_name="write",
            close_handle=lambda _handle: None,
        )
