"""Test-only concurrent Windows explicit-list launch-failure isolation probe."""

from __future__ import annotations

import errno
import os
import queue
import subprocess
import sys
import threading
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import cast

import pytest
import test_windows_cache_cleanup_inherited_handle_probe as inherited_probe
import test_windows_cache_cleanup_inherited_launch_failure_probe as failure_probe
from test_windows_cache_cleanup_child_owned_blocker_probe import (
    _close_child,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_concurrent_inheritance_leak_probe import (
    _release_inherited_blocker,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_junction_probe import (
    _filesystem_information,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_native_error_probe import (
    _ERROR_SHARING_VIOLATION,  # pyright: ignore[reportPrivateUsage]
    _attempt_native_child_rename,  # pyright: ignore[reportPrivateUsage]
    _NativeRenameResult,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_share_delete_probe import (
    _ShareDeleteProbe,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M168 probes concurrent explicit-list launch-failure isolation",
)

_LABELS = ("a", "b")
_TIMEOUT_SECONDS = 15.0


@dataclass(frozen=True, slots=True)
class _FailureOutcome:
    error: FileNotFoundError


@pytest.mark.parametrize(
    ("success_label", "failure_label"),
    ((_LABELS[0], _LABELS[1]), (_LABELS[1], _LABELS[0])),
)
def test_concurrent_failed_explicit_launch_isolates_successful_child(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    success_label: str,
    failure_label: str,
) -> None:
    roots = {label: tmp_path / label for label in _LABELS}
    live_paths = {label: root / "live" for label, root in roots.items()}
    displaced_paths = {label: root / "displaced" for label, root in roots.items()}
    payloads = {label: f"m168-launch-failure-{label}".encode() for label in _LABELS}
    for label in _LABELS:
        roots[label].mkdir()
        live_paths[label].mkdir()
        (live_paths[label] / "candidate.bin").write_bytes(payloads[label])

    filesystem_probe = _ShareDeleteProbe()
    with filesystem_probe:
        root = filesystem_probe.open_root(tmp_path)
        filesystem_name, _ = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M168 launch-failure fixture requires an NTFS pytest volume")
    assert filesystem_probe.owned_count == 0

    blocker_probe = _ShareDeleteProbe()
    with blocker_probe:
        handles = {
            label: blocker_probe.open_directory_without_delete_sharing(live_paths[label])
            for label in _LABELS
        }
        success_handle = handles[success_label]
        failure_handle = handles[failure_label]
        expected_handles = set(handles.values())
        missing_executable = (
            roots[failure_label] / failure_probe._MISSING_EXECUTABLE_NAME  # pyright: ignore[reportPrivateUsage]
        )
        assert not os.path.lexists(missing_executable)

        original_popen = subprocess.Popen
        original_get_handle_inheritable = os.get_handle_inheritable
        original_set_handle_inheritable = os.set_handle_inheritable
        coordination_lock = threading.Lock()
        marked_handles: set[int] = set()
        launching_roles: set[str] = set()
        outcome_roles: set[str] = set()
        restoring_handles: set[int] = set()
        both_marked = threading.Event()
        both_launching = threading.Event()
        permit_launch = threading.Event()
        both_outcomes = threading.Event()
        permit_outcome_return = threading.Event()
        both_restoring = threading.Event()
        permit_restore = threading.Event()
        created_processes: dict[str, subprocess.Popen[bytes]] = {}
        observed_failure: FileNotFoundError | None = None
        success_results: queue.Queue[subprocess.Popen[bytes] | BaseException] = queue.Queue(
            maxsize=1
        )
        failure_results: queue.Queue[_FailureOutcome | BaseException] = queue.Queue(maxsize=1)
        parent_released: set[int] = set()

        def coordinate_inheritability(handle: int, inheritable: bool) -> None:
            assert handle in expected_handles
            if inheritable:
                original_set_handle_inheritable(handle, True)
                with coordination_lock:
                    marked_handles.add(handle)
                    if marked_handles == expected_handles:
                        both_marked.set()
                if not both_marked.wait(timeout=_TIMEOUT_SECONDS):
                    raise RuntimeError("both explicit handles were not marked") from None
                return

            with coordination_lock:
                restoring_handles.add(handle)
                if restoring_handles == expected_handles:
                    both_restoring.set()
            if not both_restoring.wait(timeout=_TIMEOUT_SECONDS):
                raise RuntimeError("both explicit handles did not reach restoration") from None
            if not permit_restore.wait(timeout=_TIMEOUT_SECONDS):
                raise RuntimeError("explicit handle restoration was not released") from None
            original_set_handle_inheritable(handle, False)

        def wait_for_launch(role: str) -> None:
            with coordination_lock:
                launching_roles.add(role)
                if launching_roles == {"success", "failure"}:
                    both_launching.set()
            if not both_launching.wait(timeout=_TIMEOUT_SECONDS):
                raise RuntimeError("both explicit launches were not ready") from None
            if not permit_launch.wait(timeout=_TIMEOUT_SECONDS):
                raise RuntimeError("explicit launches were not released") from None

        def record_outcome(role: str) -> None:
            with coordination_lock:
                outcome_roles.add(role)
                if outcome_roles == {"success", "failure"}:
                    both_outcomes.set()
            if not permit_outcome_return.wait(timeout=_TIMEOUT_SECONDS):
                raise RuntimeError("explicit launch outcomes were not released") from None

        def launch_success(
            arguments: Sequence[str],
            *,
            close_fds: bool,
            cwd: Path,
            shell: bool,
            startupinfo: subprocess.STARTUPINFO,
            stdin: int,
            stdout: int,
            stderr: int,
        ) -> subprocess.Popen[bytes]:
            handle_list = cast(dict[str, list[int]], startupinfo.lpAttributeList)
            assert handle_list == {"handle_list": [success_handle]}
            assert close_fds is True
            assert cwd == roots[success_label]
            assert shell is False
            assert stdin == subprocess.PIPE
            assert stdout == subprocess.PIPE
            assert stderr == subprocess.PIPE
            wait_for_launch("success")
            try:
                process = original_popen(
                    arguments,
                    close_fds=close_fds,
                    cwd=cwd,
                    shell=shell,
                    startupinfo=startupinfo,
                    stdin=stdin,
                    stdout=stdout,
                    stderr=stderr,
                )
            except BaseException:
                record_outcome("success")
                raise
            with coordination_lock:
                created_processes["success"] = process
            record_outcome("success")
            return process

        def launch_failure(
            arguments: Sequence[str],
            *,
            close_fds: bool,
            cwd: Path,
            executable: str,
            shell: bool,
            startupinfo: subprocess.STARTUPINFO,
            stdin: int,
            stdout: int,
            stderr: int,
        ) -> subprocess.Popen[bytes]:
            nonlocal observed_failure
            handle_list = cast(dict[str, list[int]], startupinfo.lpAttributeList)
            assert handle_list == {"handle_list": [failure_handle]}
            assert tuple(arguments) == (str(missing_executable),)
            assert executable == str(missing_executable)
            assert close_fds is True
            assert cwd == roots[failure_label]
            assert shell is False
            assert stdin == subprocess.DEVNULL
            assert stdout == subprocess.DEVNULL
            assert stderr == subprocess.DEVNULL
            wait_for_launch("failure")
            try:
                process = original_popen(
                    arguments,
                    close_fds=close_fds,
                    cwd=cwd,
                    executable=executable,
                    shell=shell,
                    startupinfo=startupinfo,
                    stdin=stdin,
                    stdout=stdout,
                    stderr=stderr,
                )
            except FileNotFoundError as error:
                observed_failure = error
                record_outcome("failure")
                raise
            with coordination_lock:
                created_processes["failure"] = process
            record_outcome("failure")
            return process

        def spawn_success() -> None:
            try:
                result: subprocess.Popen[bytes] | BaseException = (
                    inherited_probe._spawn_inherited_blocker(  # pyright: ignore[reportPrivateUsage]
                        success_handle,
                        roots[success_label],
                    )
                )
            except BaseException as error:
                result = error
            success_results.put(result)

        def attempt_failure() -> None:
            try:
                result: _FailureOutcome | BaseException = _FailureOutcome(
                    failure_probe._attempt_missing_executable_launch(  # pyright: ignore[reportPrivateUsage]
                        failure_handle,
                        roots[failure_label],
                    )
                )
            except BaseException as error:
                result = error
            failure_results.put(result)

        shared_os = SimpleNamespace(
            get_handle_inheritable=original_get_handle_inheritable,
            set_handle_inheritable=coordinate_inheritability,
        )
        monkeypatch.setattr(inherited_probe, "os", shared_os)
        monkeypatch.setattr(
            failure_probe,
            "os",
            SimpleNamespace(
                path=os.path,
                get_handle_inheritable=original_get_handle_inheritable,
                set_handle_inheritable=coordinate_inheritability,
            ),
        )
        monkeypatch.setattr(
            inherited_probe,
            "subprocess",
            SimpleNamespace(
                PIPE=subprocess.PIPE,
                Popen=launch_success,
                STARTUPINFO=subprocess.STARTUPINFO,
            ),
        )
        monkeypatch.setattr(
            failure_probe,
            "subprocess",
            SimpleNamespace(
                DEVNULL=subprocess.DEVNULL,
                Popen=launch_failure,
                STARTUPINFO=subprocess.STARTUPINFO,
            ),
        )
        threads = {
            "success": threading.Thread(target=spawn_success, daemon=True),
            "failure": threading.Thread(target=attempt_failure, daemon=True),
        }
        for thread in threads.values():
            thread.start()

        success_process: subprocess.Popen[bytes] | None = None
        try:
            assert both_marked.wait(timeout=_TIMEOUT_SECONDS)
            assert marked_handles == expected_handles
            assert all(thread.is_alive() for thread in threads.values())
            assert all(original_get_handle_inheritable(handle) for handle in expected_handles)

            assert both_launching.wait(timeout=_TIMEOUT_SECONDS)
            assert launching_roles == {"success", "failure"}
            permit_launch.set()

            assert both_outcomes.wait(timeout=_TIMEOUT_SECONDS)
            assert outcome_roles == {"success", "failure"}
            assert set(created_processes) == {"success"}
            assert observed_failure is not None
            assert type(observed_failure) is FileNotFoundError
            assert observed_failure.errno == errno.ENOENT
            assert observed_failure.winerror == failure_probe._ERROR_FILE_NOT_FOUND  # pyright: ignore[reportPrivateUsage]
            assert all(thread.is_alive() for thread in threads.values())
            assert all(original_get_handle_inheritable(handle) for handle in expected_handles)
            permit_outcome_return.set()

            assert both_restoring.wait(timeout=_TIMEOUT_SECONDS)
            assert restoring_handles == expected_handles
            assert all(thread.is_alive() for thread in threads.values())
            assert all(original_get_handle_inheritable(handle) for handle in expected_handles)
            permit_restore.set()

            for thread in threads.values():
                thread.join(timeout=_TIMEOUT_SECONDS)
            assert all(not thread.is_alive() for thread in threads.values())

            success_result = success_results.get(timeout=_TIMEOUT_SECONDS)
            if isinstance(success_result, BaseException):
                raise success_result
            success_process = success_result
            assert success_process is created_processes["success"]

            failure_result = failure_results.get(timeout=_TIMEOUT_SECONDS)
            if isinstance(failure_result, BaseException):
                raise failure_result
            assert failure_result.error is observed_failure
            assert not os.path.lexists(missing_executable)

            assert inherited_probe._read_phase(success_process) == "ready"  # pyright: ignore[reportPrivateUsage]
            assert success_process.poll() is None
            assert all(
                original_get_handle_inheritable(handle) is False for handle in expected_handles
            )
            assert blocker_probe.owned_count == len(_LABELS)

            denied = _NativeRenameResult(
                succeeded=False,
                error_code=_ERROR_SHARING_VIOLATION,
            )
            for label in _LABELS:
                assert _attempt_native_child_rename(roots[label]) == denied
            for handle in handles.values():
                blocker_probe.release(handle)
                parent_released.add(handle)
            assert blocker_probe.owned_count == 0

            assert _attempt_native_child_rename(roots[failure_label]) == _NativeRenameResult(
                succeeded=True,
                error_code=0,
            )
            assert _attempt_native_child_rename(roots[success_label]) == denied
            assert success_process.poll() is None
            assert not os.path.lexists(live_paths[failure_label])
            assert displaced_paths[failure_label].is_dir()
            assert live_paths[success_label].is_dir()
            assert not os.path.lexists(displaced_paths[success_label])

            _release_inherited_blocker(success_process)
            assert _attempt_native_child_rename(roots[success_label]) == _NativeRenameResult(
                succeeded=True,
                error_code=0,
            )
            for label in _LABELS:
                assert not os.path.lexists(live_paths[label])
                assert displaced_paths[label].is_dir()
                assert not os.path.isjunction(displaced_paths[label])
                assert (displaced_paths[label] / "candidate.bin").read_bytes() == payloads[label]
        finally:
            both_marked.set()
            both_launching.set()
            permit_launch.set()
            both_outcomes.set()
            permit_outcome_return.set()
            both_restoring.set()
            permit_restore.set()
            for thread in threads.values():
                thread.join(timeout=_TIMEOUT_SECONDS)
            if success_process is None:
                success_process = created_processes.get("success")
            for handle in handles.values():
                if handle not in parent_released and original_get_handle_inheritable(handle):
                    original_set_handle_inheritable(handle, False)
                if handle not in parent_released:
                    blocker_probe.release(handle)
                    parent_released.add(handle)
            for process in created_processes.values():
                _close_child(process)

    assert blocker_probe.owned_count == 0
    assert all(not thread.is_alive() for thread in threads.values())
    assert set(created_processes) == {"success"}
    assert success_process is not None and success_process.returncode == 0
    for stream in (success_process.stdin, success_process.stdout, success_process.stderr):
        assert stream is not None and stream.closed
    assert not os.path.lexists(missing_executable)
    for label in _LABELS:
        assert (displaced_paths[label] / "candidate.bin").read_bytes() == payloads[label]
