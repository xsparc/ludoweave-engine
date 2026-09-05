"""Test-only Windows retained-source remote-debug exclusion probe."""

from __future__ import annotations

import ctypes
import sys
from unittest.mock import patch

import pytest

from tests.integration import (
    test_windows_retained_launch_source_binding_probe as _launch_source_module,
)
from tests.integration.test_windows_local_control_channel_probe import (
    _DIRECT_PYTHON,  # pyright: ignore[reportPrivateUsage]
    _PARTICIPANT,  # pyright: ignore[reportPrivateUsage]
    _PIPE_PREFIX,  # pyright: ignore[reportPrivateUsage]
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
from tests.integration.test_windows_retained_launch_source_access_refusal_probe import (
    _require_source_access_allowed,  # pyright: ignore[reportPrivateUsage]
    _require_source_access_refused,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_launch_source_binding_probe import (
    _InheritedLaunchSource,  # pyright: ignore[reportPrivateUsage]
    _InheritedNullHandle,  # pyright: ignore[reportPrivateUsage]
    _RetainedLaunchSourceControlProbe,  # pyright: ignore[reportPrivateUsage]
    _verify_source_stable,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _RetainedImageFile,  # pyright: ignore[reportPrivateUsage]
    _RetainedProcessImage,  # pyright: ignore[reportPrivateUsage]
    _verify_expected_image,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _verify_stable as _verify_image_stable,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M217 probes Windows retained-source remote-debug exclusion",
)
_M215_FIXED_COMMAND_LINE = (
    _launch_source_module._fixed_command_line  # pyright: ignore[reportPrivateUsage]
)


def _remote_debug_disabled_command_line(pipe_name: str) -> str:
    _M215_FIXED_COMMAND_LINE(pipe_name)
    return f'"{_DIRECT_PYTHON}" -I -B -X disable_remote_debug - {pipe_name}'


def test_remote_debug_exclusion_preserves_retained_source_boundary() -> None:
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
            with patch.object(
                _launch_source_module,
                "_fixed_command_line",
                _remote_debug_disabled_command_line,
            ):
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


def test_remote_debug_exclusion_command_line_is_exact() -> None:
    pipe_name = _PIPE_PREFIX + "0" * 32
    assert _remote_debug_disabled_command_line(pipe_name) == (
        f'"{_DIRECT_PYTHON}" -I -B -X disable_remote_debug - {pipe_name}'
    )
    assert str(_PARTICIPANT) not in _remote_debug_disabled_command_line(pipe_name)


@pytest.mark.parametrize(
    "pipe_name",
    [
        "",
        _PIPE_PREFIX,
        _PIPE_PREFIX + "0" * 31,
        _PIPE_PREFIX + "0" * 33,
        _PIPE_PREFIX + "g" * 32,
        _PIPE_PREFIX + "0" * 31 + " ",
    ],
)
def test_remote_debug_exclusion_reuses_pipe_validation(pipe_name: str) -> None:
    with pytest.raises(RuntimeError, match="pipe name"):
        _remote_debug_disabled_command_line(pipe_name)


def test_command_patch_restores_frozen_m215_composer() -> None:
    with patch.object(
        _launch_source_module,
        "_fixed_command_line",
        _remote_debug_disabled_command_line,
    ):
        assert (
            _launch_source_module._fixed_command_line  # pyright: ignore[reportPrivateUsage]
            is _remote_debug_disabled_command_line
        )
    assert (
        _launch_source_module._fixed_command_line  # pyright: ignore[reportPrivateUsage]
        is _M215_FIXED_COMMAND_LINE
    )
