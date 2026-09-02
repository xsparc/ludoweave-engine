"""Bind every M224 Git child image before its primary thread can run."""

from __future__ import annotations

import ctypes
import subprocess
import sys
from collections.abc import Callable
from ctypes import wintypes
from types import ModuleType
from typing import cast
from unittest.mock import patch

import pytest

from tests.integration import (
    test_windows_contained_source_access_source_commit_binding_probe as _commit_module,
)
from tests.integration import (
    test_windows_contained_source_access_source_commit_git_selection_binding_probe as _selection_module,
)
from tests.integration.test_windows_contained_source_access_source_commit_git_file_retention_probe import (
    _RetainedGitExecutableFile,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _ImageSnapshot,  # pyright: ignore[reportPrivateUsage]
    _load_function,  # pyright: ignore[reportPrivateUsage]
    _RetainedImageFile,  # pyright: ignore[reportPrivateUsage]
    _RetainedProcessImage,  # pyright: ignore[reportPrivateUsage]
    _verify_expected_image,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _verify_stable as _verify_image_stable,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M225 binds each Windows Git child image before its primary thread runs",
)

_CREATE_SUSPENDED = 0x00000004
_EXPECTED_GIT_READS = 48
_RESUME_FAILED = 0xFFFFFFFF
_WAIT_OBJECT_0 = 0x00000000
_WAIT_TIMEOUT = 0x00000102
_SETTLEMENT_TIMEOUT_MS = 5_000
_TERMINATION_EXIT_CODE = 113


class _ChildProcessApi:
    """Own native pre-return failure cleanup for one suspended child."""

    def __init__(self) -> None:
        win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
        self._get_last_error = cast(Callable[[], int], vars(ctypes)["get_last_error"])
        kernel32 = win_dll("kernel32", use_last_error=True)
        self._resume_thread = _load_function(
            kernel32,
            "ResumeThread",
            [wintypes.HANDLE],
            wintypes.DWORD,
        )
        self._terminate_process = _load_function(
            kernel32,
            "TerminateProcess",
            [wintypes.HANDLE, wintypes.UINT],
            wintypes.BOOL,
        )
        self._wait_for_single_object = _load_function(
            kernel32,
            "WaitForSingleObject",
            [wintypes.HANDLE, wintypes.DWORD],
            wintypes.DWORD,
        )
        self._close_handle = _load_function(
            kernel32,
            "CloseHandle",
            [wintypes.HANDLE],
            wintypes.BOOL,
        )

    def _fail(self, operation: str) -> RuntimeError:
        return RuntimeError(f"{operation} failed with native code {self._get_last_error()}")

    def resume_thread(self, thread_handle: int) -> int:
        result = cast(int, self._resume_thread(wintypes.HANDLE(thread_handle)))
        if result == _RESUME_FAILED:
            raise self._fail("ResumeThread") from None
        return result

    def _close(self, handle: int) -> None:
        if not cast(bool, self._close_handle(wintypes.HANDLE(handle))):
            raise self._fail("CloseHandle") from None

    def terminate_wait_and_close(self, process_handle: int, thread_handle: int) -> None:
        failure: BaseException | None = None
        try:
            if not cast(
                bool,
                self._terminate_process(
                    wintypes.HANDLE(process_handle),
                    _TERMINATION_EXIT_CODE,
                ),
            ):
                raise self._fail("TerminateProcess") from None
            result = cast(
                int,
                self._wait_for_single_object(
                    wintypes.HANDLE(process_handle),
                    _SETTLEMENT_TIMEOUT_MS,
                ),
            )
            if result != _WAIT_OBJECT_0:
                raise RuntimeError(
                    f"WaitForSingleObject did not settle the child: {result}"
                ) from None
        except BaseException as error:
            failure = error
        for handle in (thread_handle, process_handle):
            try:
                self._close(handle)
            except BaseException as error:
                if failure is None:
                    failure = error
        if failure is not None:
            raise failure


def _snapshot_retained_image(observed: _RetainedProcessImage) -> _ImageSnapshot:
    retained = cast(_RetainedImageFile, vars(observed)["_image"])
    return retained.snapshot()


def _winapi_module() -> ModuleType:
    return cast(ModuleType, vars(subprocess)["_winapi"])


def _close_observations(
    observations: list[tuple[_RetainedProcessImage, _ImageSnapshot]],
) -> None:
    failure: BaseException | None = None
    for retained, snapshot in reversed(observations):
        try:
            _verify_image_stable(snapshot, _snapshot_retained_image(retained))
        except BaseException as error:
            if failure is None:
                failure = error
        try:
            retained.close()
        except BaseException as error:
            if failure is None:
                failure = error
    if failure is not None:
        raise failure


def test_git_child_images_match_the_retained_m224_executable() -> None:
    real_which = _commit_module.shutil.which
    with patch.object(
        _commit_module.shutil,
        "which",
        side_effect=real_which,
    ) as lookup:
        git_executable = _commit_module._git_executable()  # pyright: ignore[reportPrivateUsage]
    assert lookup.call_count == 1

    winapi = _winapi_module()
    real_create_process = cast(
        Callable[..., tuple[int, int, int, int]],
        vars(winapi)["CreateProcess"],
    )
    api = _ChildProcessApi()
    observations: list[tuple[_RetainedProcessImage, _ImageSnapshot]] = []

    with _RetainedGitExecutableFile(git_executable) as expected_file:
        expected = expected_file.snapshot()

        def _create_bound_process(*arguments: object) -> tuple[int, int, int, int]:
            if len(arguments) != 9 or not isinstance(arguments[5], int):
                raise RuntimeError("unexpected CPython CreateProcess boundary") from None
            bound_arguments = list(arguments)
            creation_flags = arguments[5]
            bound_arguments[5] = creation_flags | _CREATE_SUSPENDED
            process_handle, thread_handle, process_id, thread_id = real_create_process(
                *bound_arguments
            )
            retained: _RetainedProcessImage | None = None
            try:
                retained = _RetainedProcessImage(process_handle)
                observed_snapshot = _snapshot_retained_image(retained)
                _verify_expected_image(expected, observed_snapshot)
                previous_suspend_count = api.resume_thread(thread_handle)
                if previous_suspend_count != 1:
                    raise RuntimeError(
                        "Git child did not have exactly one creation suspension"
                    ) from None
                observations.append((retained, observed_snapshot))
            except BaseException:
                try:
                    api.terminate_wait_and_close(process_handle, thread_handle)
                finally:
                    if retained is not None:
                        retained.close()
                raise
            return process_handle, thread_handle, process_id, thread_id

        try:
            with (
                patch.object(
                    _commit_module,
                    "_git_executable",
                    return_value=git_executable,
                ) as selection,
                patch.object(
                    winapi,
                    "CreateProcess",
                    side_effect=_create_bound_process,
                ) as creation,
            ):
                _selection_module._require_git_selection_bound_m222_boundary()  # pyright: ignore[reportPrivateUsage]

            assert selection.call_count == 1
            assert creation.call_count == _EXPECTED_GIT_READS
            assert len(observations) == _EXPECTED_GIT_READS
            _verify_image_stable(expected, expected_file.snapshot())
            for retained, snapshot in observations:
                _verify_image_stable(snapshot, _snapshot_retained_image(retained))
        finally:
            _close_observations(observations)

    with _RetainedImageFile(git_executable) as settled:
        _verify_image_stable(expected, settled.snapshot())


class _FakeImage:
    def __init__(self, snapshot: _ImageSnapshot) -> None:
        self._snapshot = snapshot

    def snapshot(self) -> _ImageSnapshot:
        return self._snapshot


class _FakeRetainedProcessImage:
    def __init__(self, snapshot: _ImageSnapshot) -> None:
        self._image = _FakeImage(snapshot)
        self.closed = False

    def close(self) -> None:
        self.closed = True


def _sample_snapshot(name: str) -> _ImageSnapshot:
    return _ImageSnapshot(name, 1, b"file-id", 2, b"digest")


def test_observation_cleanup_closes_every_retained_image_after_drift() -> None:
    expected = _sample_snapshot("c:\\git.exe")
    first = _FakeRetainedProcessImage(_sample_snapshot("c:\\other.exe"))
    second = _FakeRetainedProcessImage(expected)
    observations = cast(
        list[tuple[_RetainedProcessImage, _ImageSnapshot]],
        [(first, expected), (second, expected)],
    )

    with pytest.raises(RuntimeError, match="changed before release"):
        _close_observations(observations)

    assert first.closed
    assert second.closed


def test_failed_suspended_settlement_closes_both_native_handles() -> None:
    api = object.__new__(_ChildProcessApi)
    closed: list[int] = []
    terminated: list[tuple[int, int]] = []

    def _terminate_process(process: wintypes.HANDLE, exit_code: int) -> bool:
        terminated.append((cast(int, process.value), exit_code))
        return True

    def _wait_for_single_object(_process: object, _timeout: object) -> int:
        return _WAIT_TIMEOUT

    def _close_handle(handle: wintypes.HANDLE) -> bool:
        closed.append(cast(int, handle.value))
        return True

    vars(api)["_get_last_error"] = lambda: 5
    vars(api)["_terminate_process"] = _terminate_process
    vars(api)["_wait_for_single_object"] = _wait_for_single_object
    vars(api)["_close_handle"] = _close_handle

    with pytest.raises(RuntimeError, match="did not settle"):
        api.terminate_wait_and_close(101, 202)

    assert terminated == [(101, _TERMINATION_EXIT_CODE)]
    assert closed == [202, 101]
