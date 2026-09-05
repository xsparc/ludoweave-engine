"""Test-only Windows contained source-access image-binding probe."""

from __future__ import annotations

import ctypes
import sys
from ctypes import wintypes
from pathlib import Path
from typing import cast
from unittest.mock import patch

import pytest

from tests.integration import (
    test_windows_retained_launch_source_binding_probe as _launch_source_module,
)
from tests.integration.test_windows_contained_source_access_refusal_probe import (
    _contender_command_line,  # pyright: ignore[reportPrivateUsage]
    _require_contender_exit,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_independent_host_process_containment_probe import (
    _CREATE_NO_WINDOW,  # pyright: ignore[reportPrivateUsage]
    _CREATE_SUSPENDED,  # pyright: ignore[reportPrivateUsage]
    _ERROR_ACCESS_DENIED,  # pyright: ignore[reportPrivateUsage]
    _STILL_ACTIVE,  # pyright: ignore[reportPrivateUsage]
    _TERMINATION_EXIT_CODE,  # pyright: ignore[reportPrivateUsage]
    _WAIT_FAILED,  # pyright: ignore[reportPrivateUsage]
    _handle_value,  # pyright: ignore[reportPrivateUsage]
    _NativeFailure,  # pyright: ignore[reportPrivateUsage]
    _ProcessInformation,  # pyright: ignore[reportPrivateUsage]
    _StartupInfoW,  # pyright: ignore[reportPrivateUsage]
    _WindowsJobProbe,  # pyright: ignore[reportPrivateUsage]
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
from tests.integration.test_windows_remote_debug_exclusion_probe import (
    _remote_debug_disabled_command_line,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_launch_source_access_refusal_probe import (
    _require_source_access_allowed,  # pyright: ignore[reportPrivateUsage]
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
    reason="M219 probes contained Windows source-access image binding",
)

_ROOT = Path(__file__).parents[2]


class _ContainedSourceAccessImageProbe(_WindowsJobProbe):
    """Bind one fixed contained access contender to its retained image."""

    def run_image_bound_contender(self, *, phase: str) -> None:
        with _RetainedImageFile(_DIRECT_PYTHON) as expected_image_file:
            expected_image = expected_image_file.snapshot()
            job = self.create_job()
            startup = _StartupInfoW()
            startup.cb = ctypes.sizeof(startup)
            command_line = ctypes.create_unicode_buffer(_contender_command_line())
            process_information = _ProcessInformation()
            created = cast(
                bool,
                self._create_process(  # pyright: ignore[reportPrivateUsage]
                    str(_DIRECT_PYTHON),
                    command_line,
                    None,
                    None,
                    False,
                    _CREATE_SUSPENDED | _CREATE_NO_WINDOW,
                    None,
                    str(_ROOT),
                    ctypes.byref(startup),
                    ctypes.byref(process_information),
                ),
            )
            if not created:
                raise self._failure(  # pyright: ignore[reportPrivateUsage]
                    "CreateProcessW"
                )
            process = self._own(  # pyright: ignore[reportPrivateUsage]
                _handle_value(process_information.hProcess, "CreateProcessW")
            )
            thread = self._own(  # pyright: ignore[reportPrivateUsage]
                _handle_value(process_information.hThread, "CreateProcessW")
            )
            process_id = int(process_information.dwProcessId)

            assigned = cast(
                bool,
                self._assign_process(  # pyright: ignore[reportPrivateUsage]
                    wintypes.HANDLE(job), wintypes.HANDLE(process)
                ),
            )
            if not assigned:
                code = self._get_last_error()  # pyright: ignore[reportPrivateUsage]
                self._terminate_process(  # pyright: ignore[reportPrivateUsage]
                    wintypes.HANDLE(process), _TERMINATION_EXIT_CODE
                )
                self.wait_process(process)
                raise _NativeFailure("AssignProcessToJobObject", code)
            assert self._process_is_in_job(  # pyright: ignore[reportPrivateUsage]
                process, job
            )
            assert self.accounting(job) == (1, 1)
            assert self.process_ids(job) == (process_id,)
            assert self.exit_code(process) == _STILL_ACTIVE

            with (
                _RetainedTokenBinding(0) as controller_binding,
                _RetainedTokenBinding(process) as contender_binding,
                _RetainedProcessImage(process) as observed_image,
            ):
                controller = controller_binding.snapshot()
                contender = contender_binding.snapshot()
                _verify_same_logon(controller, contender)
                image_before = observed_image.snapshot()
                _verify_expected_image(expected_image, image_before)

                previous_suspend_count = cast(
                    int,
                    self._resume_thread(  # pyright: ignore[reportPrivateUsage]
                        wintypes.HANDLE(thread)
                    ),
                )
                if previous_suspend_count == _WAIT_FAILED:
                    raise self._failure(  # pyright: ignore[reportPrivateUsage]
                        "ResumeThread"
                    )
                if previous_suspend_count != 1:
                    raise RuntimeError(
                        "image-bound contender had an invalid suspend count"
                    ) from None
                self.close_handle(thread)

                self.wait_process(process)
                exit_code = self.exit_code(process)
                _require_contender_exit(exit_code, phase=phase)
                assert self.exit_code(process) == 0
                _verify_image_stable(expected_image, expected_image_file.snapshot())
                _verify_image_stable(
                    image_before,
                    observed_image._image.snapshot(  # pyright: ignore[reportPrivateUsage]
                        normalized_name=image_before.normalized_name
                    ),
                )

            self.close_handle(process)
            assert self.wait_job_empty(job) == (1, 0)
            self.close_handle(job)
            assert self.owned_count == 0


def _require_image_bound_source_access_refused(*, phase: str) -> None:
    image_probe = _ContainedSourceAccessImageProbe()
    try:
        with image_probe:
            image_probe.run_image_bound_contender(phase=phase)
    except _NativeFailure as error:
        if error.operation == "AssignProcessToJobObject" and error.code == _ERROR_ACCESS_DENIED:
            pytest.skip("current host does not permit the required nested Job Object")
        raise
    assert image_probe.owned_count == 0


def test_contained_source_access_image_binding_preserves_boundary() -> None:
    with (
        _InheritedLaunchSource(_PARTICIPANT) as source_file,
        _InheritedNullHandle() as output_handle,
        _InheritedNullHandle() as error_handle,
    ):
        probe = _RetainedLaunchSourceControlProbe(source_file, output_handle, error_handle)
        with probe, _RetainedImageFile(_DIRECT_PYTHON) as expected_image_file:
            source_before = source_file.snapshot()
            expected_image = expected_image_file.snapshot()
            _require_image_bound_source_access_refused(phase="before_launch")
            with patch.object(
                _launch_source_module,
                "_fixed_command_line",
                _remote_debug_disabled_command_line,
            ):
                session = _start_or_skip(probe)
            _require_image_bound_source_access_refused(phase="after_connection")
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
                _require_image_bound_source_access_refused(phase="after_ready")
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


def test_image_bound_contender_reuses_exact_fixed_command() -> None:
    command_line = _contender_command_line()
    assert command_line.startswith(f'"{_DIRECT_PYTHON}" -I -B ')
    assert str(_PARTICIPANT) not in command_line


def test_image_bound_participant_reuses_remote_debug_exclusion() -> None:
    pipe_name = _PIPE_PREFIX + "0" * 32
    command_line = _remote_debug_disabled_command_line(pipe_name)
    assert "-X disable_remote_debug" in command_line
    assert str(_PARTICIPANT) not in command_line
