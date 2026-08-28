"""Test-only concurrent Windows explicit-list restoration-failure isolation probe."""

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
from test_windows_cache_cleanup_concurrent_inheritance_leak_probe import (
    _release_inherited_blocker,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_inherited_restore_failure_probe import (
    _InjectedRestoreFailure,  # pyright: ignore[reportPrivateUsage]
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
    reason="M169 probes concurrent explicit-list restoration-failure isolation",
)

_LABELS = ("a", "b")
_TIMEOUT_SECONDS = 15.0


@dataclass(frozen=True, slots=True)
class _RestoreFailureOutcome:
    error: _InjectedRestoreFailure


@pytest.mark.parametrize(
    ("survivor_label", "failure_label"),
    ((_LABELS[0], _LABELS[1]), (_LABELS[1], _LABELS[0])),
)
def test_concurrent_restore_failure_isolates_surviving_explicit_child(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    survivor_label: str,
    failure_label: str,
) -> None:
    roots = {label: tmp_path / label for label in _LABELS}
    live_paths = {label: root / "live" for label, root in roots.items()}
    displaced_paths = {label: root / "displaced" for label, root in roots.items()}
    payloads = {label: f"m169-restore-failure-{label}".encode() for label in _LABELS}
    for label in _LABELS:
        roots[label].mkdir()
        live_paths[label].mkdir()
        (live_paths[label] / "candidate.bin").write_bytes(payloads[label])

    filesystem_probe = _ShareDeleteProbe()
    with filesystem_probe:
        root = filesystem_probe.open_root(tmp_path)
        filesystem_name, _ = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M169 restore-failure fixture requires an NTFS pytest volume")
    assert filesystem_probe.owned_count == 0

    blocker_probe = _ShareDeleteProbe()
    with blocker_probe:
        handles = {
            label: blocker_probe.open_directory_without_delete_sharing(live_paths[label])
            for label in _LABELS
        }
        survivor_handle = handles[survivor_label]
        failure_handle = handles[failure_label]
        expected_handles = set(handles.values())

        original_popen = subprocess.Popen
        original_get_handle_inheritable = os.get_handle_inheritable
        original_set_handle_inheritable = os.set_handle_inheritable
        original_close_child = inherited_probe._close_child  # pyright: ignore[reportPrivateUsage]
        injected = _InjectedRestoreFailure(
            errno.EIO,
            "injected concurrent handle restore failure",
        )
        coordination_lock = threading.Lock()
        marked_handles: set[int] = set()
        launching_handles: set[int] = set()
        outcome_handles: set[int] = set()
        restoring_handles: set[int] = set()
        created_processes: dict[int, subprocess.Popen[bytes]] = {}
        launch_errors: dict[int, BaseException] = {}
        helper_closed_processes: list[subprocess.Popen[bytes]] = []
        helper_preclose_returncodes: list[int | None] = []
        restore_failure_attempts = 0
        both_marked = threading.Event()
        both_launching = threading.Event()
        permit_launch = threading.Event()
        both_outcomes = threading.Event()
        permit_outcome_return = threading.Event()
        both_restoring = threading.Event()
        permit_restore = threading.Event()
        survivor_results: queue.Queue[subprocess.Popen[bytes] | BaseException] = queue.Queue(
            maxsize=1
        )
        failure_results: queue.Queue[_RestoreFailureOutcome | BaseException] = queue.Queue(
            maxsize=1
        )
        parent_released: set[int] = set()

        def coordinate_inheritability(handle: int, inheritable: bool) -> None:
            nonlocal restore_failure_attempts
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
            if handle == failure_handle:
                with coordination_lock:
                    restore_failure_attempts += 1
                    assert restore_failure_attempts == 1
                raise injected
            original_set_handle_inheritable(handle, False)

        def record_launch_boundary(handle: int) -> None:
            with coordination_lock:
                launching_handles.add(handle)
                if launching_handles == expected_handles:
                    both_launching.set()
            if not both_launching.wait(timeout=_TIMEOUT_SECONDS):
                raise RuntimeError("both explicit launches were not ready") from None
            if not permit_launch.wait(timeout=_TIMEOUT_SECONDS):
                raise RuntimeError("explicit launches were not released") from None

        def record_launch_outcome(handle: int) -> None:
            with coordination_lock:
                outcome_handles.add(handle)
                if outcome_handles == expected_handles:
                    both_outcomes.set()
            if not permit_outcome_return.wait(timeout=_TIMEOUT_SECONDS):
                raise RuntimeError("explicit launch outcomes were not released") from None

        def launch_explicit(
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
            assert set(handle_list) == {"handle_list"}
            listed_handles = handle_list["handle_list"]
            assert len(listed_handles) == 1
            handle = listed_handles[0]
            assert handle in expected_handles
            label = survivor_label if handle == survivor_handle else failure_label
            assert tuple(arguments) == (
                sys.executable,
                "-I",
                "-B",
                str(inherited_probe._CHILD),  # pyright: ignore[reportPrivateUsage]
                str(handle),
            )
            assert close_fds is True
            assert cwd == roots[label]
            assert shell is False
            assert stdin == subprocess.PIPE
            assert stdout == subprocess.PIPE
            assert stderr == subprocess.PIPE
            record_launch_boundary(handle)
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
            except BaseException as error:
                with coordination_lock:
                    launch_errors[handle] = error
                record_launch_outcome(handle)
                raise
            with coordination_lock:
                created_processes[handle] = process
            record_launch_outcome(handle)
            return process

        def capture_helper_close(process: subprocess.Popen[bytes]) -> None:
            with coordination_lock:
                helper_closed_processes.append(process)
                helper_preclose_returncodes.append(process.poll())
            original_close_child(process)

        def spawn_survivor() -> None:
            try:
                result: subprocess.Popen[bytes] | BaseException = (
                    inherited_probe._spawn_inherited_blocker(  # pyright: ignore[reportPrivateUsage]
                        survivor_handle,
                        roots[survivor_label],
                    )
                )
            except BaseException as error:
                result = error
            survivor_results.put(result)

        def spawn_restore_failure() -> None:
            try:
                process = inherited_probe._spawn_inherited_blocker(  # pyright: ignore[reportPrivateUsage]
                    failure_handle,
                    roots[failure_label],
                )
            except _InjectedRestoreFailure as error:
                result: _RestoreFailureOutcome | BaseException = _RestoreFailureOutcome(error)
            except BaseException as error:
                result = error
            else:
                result = AssertionError(
                    f"restore failure helper unexpectedly returned process {process.pid}"
                )
            failure_results.put(result)

        monkeypatch.setattr(
            inherited_probe,
            "os",
            SimpleNamespace(
                get_handle_inheritable=original_get_handle_inheritable,
                set_handle_inheritable=coordinate_inheritability,
            ),
        )
        monkeypatch.setattr(
            inherited_probe,
            "subprocess",
            SimpleNamespace(
                PIPE=subprocess.PIPE,
                Popen=launch_explicit,
                STARTUPINFO=subprocess.STARTUPINFO,
            ),
        )
        monkeypatch.setattr(inherited_probe, "_close_child", capture_helper_close)
        threads = {
            "survivor": threading.Thread(target=spawn_survivor, daemon=True),
            "failure": threading.Thread(target=spawn_restore_failure, daemon=True),
        }
        for thread in threads.values():
            thread.start()

        survivor_process: subprocess.Popen[bytes] | None = None
        try:
            assert both_marked.wait(timeout=_TIMEOUT_SECONDS)
            assert marked_handles == expected_handles
            assert all(thread.is_alive() for thread in threads.values())
            assert all(original_get_handle_inheritable(handle) for handle in expected_handles)

            assert both_launching.wait(timeout=_TIMEOUT_SECONDS)
            assert launching_handles == expected_handles
            permit_launch.set()

            assert both_outcomes.wait(timeout=_TIMEOUT_SECONDS)
            assert outcome_handles == expected_handles
            assert set(created_processes) == expected_handles
            assert launch_errors == {}
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

            survivor_result = survivor_results.get(timeout=_TIMEOUT_SECONDS)
            if isinstance(survivor_result, BaseException):
                raise survivor_result
            survivor_process = survivor_result
            assert survivor_process is created_processes[survivor_handle]

            failure_result = failure_results.get(timeout=_TIMEOUT_SECONDS)
            if isinstance(failure_result, BaseException):
                raise failure_result
            assert failure_result.error is injected
            assert restore_failure_attempts == 1

            failed_process = created_processes[failure_handle]
            assert helper_closed_processes == [failed_process]
            assert helper_preclose_returncodes == [None]
            assert failed_process.returncode is not None
            assert failed_process.poll() == failed_process.returncode
            for stream in (failed_process.stdin, failed_process.stdout, failed_process.stderr):
                assert stream is not None and stream.closed

            assert inherited_probe._read_phase(survivor_process) == "ready"  # pyright: ignore[reportPrivateUsage]
            assert survivor_process.poll() is None
            assert original_get_handle_inheritable(survivor_handle) is False
            assert original_get_handle_inheritable(failure_handle) is True
            assert blocker_probe.owned_count == len(_LABELS)

            denied = _NativeRenameResult(
                succeeded=False,
                error_code=_ERROR_SHARING_VIOLATION,
            )
            for label in _LABELS:
                assert _attempt_native_child_rename(roots[label]) == denied

            original_set_handle_inheritable(failure_handle, False)
            assert all(
                original_get_handle_inheritable(handle) is False for handle in expected_handles
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
            assert _attempt_native_child_rename(roots[survivor_label]) == denied
            assert survivor_process.poll() is None
            assert not os.path.lexists(live_paths[failure_label])
            assert displaced_paths[failure_label].is_dir()
            assert live_paths[survivor_label].is_dir()
            assert not os.path.lexists(displaced_paths[survivor_label])

            _release_inherited_blocker(survivor_process)
            assert _attempt_native_child_rename(roots[survivor_label]) == _NativeRenameResult(
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
            if survivor_process is None:
                survivor_process = created_processes.get(survivor_handle)
            for handle in handles.values():
                if handle not in parent_released and original_get_handle_inheritable(handle):
                    original_set_handle_inheritable(handle, False)
                if handle not in parent_released:
                    blocker_probe.release(handle)
                    parent_released.add(handle)
            for process in created_processes.values():
                original_close_child(process)

    assert blocker_probe.owned_count == 0
    assert all(not thread.is_alive() for thread in threads.values())
    assert set(created_processes) == expected_handles
    failed_process = created_processes[failure_handle]
    assert failed_process.returncode is not None
    assert survivor_process is not None and survivor_process.returncode == 0
    for process in created_processes.values():
        for stream in (process.stdin, process.stdout, process.stderr):
            assert stream is not None and stream.closed
    for label in _LABELS:
        assert (displaced_paths[label] / "candidate.bin").read_bytes() == payloads[label]
