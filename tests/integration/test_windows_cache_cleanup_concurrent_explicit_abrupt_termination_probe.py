"""Test-only concurrent Windows explicit-list abrupt-termination isolation probe."""

from __future__ import annotations

import os
import queue
import subprocess
import sys
import threading
from collections.abc import Sequence
from pathlib import Path
from types import SimpleNamespace
from typing import cast

import pytest
import test_windows_cache_cleanup_inherited_handle_probe as inherited_probe
from test_windows_cache_cleanup_child_owned_blocker_probe import (
    _close_child,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_concurrent_inheritance_leak_probe import (
    _release_inherited_blocker,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_inherited_handle_probe import (
    _MAX_LINE_BYTES,  # pyright: ignore[reportPrivateUsage]
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
    reason="M170 probes concurrent explicit-list abrupt-termination isolation",
)

_LABELS = ("a", "b")
_TIMEOUT_SECONDS = 15.0


@pytest.mark.parametrize(
    ("abrupt_label", "survivor_label"),
    ((_LABELS[0], _LABELS[1]), (_LABELS[1], _LABELS[0])),
)
def test_abrupt_child_exit_isolates_surviving_explicit_blocker(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    abrupt_label: str,
    survivor_label: str,
) -> None:
    roots = {label: tmp_path / label for label in _LABELS}
    live_paths = {label: root / "live" for label, root in roots.items()}
    displaced_paths = {label: root / "displaced" for label, root in roots.items()}
    payloads = {label: f"m170-abrupt-isolation-{label}".encode() for label in _LABELS}
    for label in _LABELS:
        roots[label].mkdir()
        live_paths[label].mkdir()
        (live_paths[label] / "candidate.bin").write_bytes(payloads[label])

    filesystem_probe = _ShareDeleteProbe()
    with filesystem_probe:
        root = filesystem_probe.open_root(tmp_path)
        filesystem_name, _ = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M170 abrupt-termination fixture requires an NTFS pytest volume")
    assert filesystem_probe.owned_count == 0

    blocker_probe = _ShareDeleteProbe()
    with blocker_probe:
        handles = {
            label: blocker_probe.open_directory_without_delete_sharing(live_paths[label])
            for label in _LABELS
        }
        labels_by_handle = {handle: label for label, handle in handles.items()}
        expected_handles = set(handles.values())
        original_popen = subprocess.Popen
        original_get_handle_inheritable = os.get_handle_inheritable
        original_set_handle_inheritable = os.set_handle_inheritable
        coordination_lock = threading.Lock()
        marked_handles: set[int] = set()
        created_handles: set[int] = set()
        restoring_handles: set[int] = set()
        created_processes: dict[str, subprocess.Popen[bytes]] = {}
        both_marked = threading.Event()
        both_created = threading.Event()
        permit_launch_return = threading.Event()
        both_restoring = threading.Event()
        permit_restore = threading.Event()
        results: queue.Queue[tuple[str, subprocess.Popen[bytes] | BaseException]] = queue.Queue(
            maxsize=len(_LABELS)
        )
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

        def launch_explicit_child(
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
            label = labels_by_handle[handle]
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
            with coordination_lock:
                created_processes[label] = process
                created_handles.add(handle)
                if created_handles == expected_handles:
                    both_created.set()
            if not permit_launch_return.wait(timeout=_TIMEOUT_SECONDS):
                raise RuntimeError("explicit launch return was not released") from None
            return process

        def spawn_explicit_child(label: str) -> None:
            try:
                result: subprocess.Popen[bytes] | BaseException = (
                    inherited_probe._spawn_inherited_blocker(  # pyright: ignore[reportPrivateUsage]
                        handles[label],
                        roots[label],
                    )
                )
            except BaseException as error:
                result = error
            results.put((label, result))

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
                Popen=launch_explicit_child,
                STARTUPINFO=subprocess.STARTUPINFO,
            ),
        )
        threads = {
            label: threading.Thread(
                target=spawn_explicit_child,
                args=(label,),
                daemon=True,
            )
            for label in _LABELS
        }
        for thread in threads.values():
            thread.start()

        processes: dict[str, subprocess.Popen[bytes]] = {}
        try:
            assert both_marked.wait(timeout=_TIMEOUT_SECONDS)
            assert marked_handles == expected_handles
            assert all(thread.is_alive() for thread in threads.values())
            assert all(original_get_handle_inheritable(handle) for handle in expected_handles)

            assert both_created.wait(timeout=_TIMEOUT_SECONDS)
            assert created_handles == expected_handles
            assert set(created_processes) == set(_LABELS)
            assert all(thread.is_alive() for thread in threads.values())
            assert all(original_get_handle_inheritable(handle) for handle in expected_handles)
            permit_launch_return.set()

            assert both_restoring.wait(timeout=_TIMEOUT_SECONDS)
            assert restoring_handles == expected_handles
            assert all(thread.is_alive() for thread in threads.values())
            assert all(original_get_handle_inheritable(handle) for handle in expected_handles)
            permit_restore.set()

            for thread in threads.values():
                thread.join(timeout=_TIMEOUT_SECONDS)
            assert all(not thread.is_alive() for thread in threads.values())
            for _ in _LABELS:
                label, result = results.get(timeout=_TIMEOUT_SECONDS)
                if isinstance(result, BaseException):
                    raise result
                processes[label] = result
                assert result is created_processes[label]

            for label in _LABELS:
                process = processes[label]
                assert inherited_probe._read_phase(process) == "ready"  # pyright: ignore[reportPrivateUsage]
                assert process.poll() is None
                assert original_get_handle_inheritable(handles[label]) is False
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
            for label in _LABELS:
                assert _attempt_native_child_rename(roots[label]) == denied
                assert processes[label].poll() is None

            abrupt_process = processes[abrupt_label]
            survivor_process = processes[survivor_label]
            abrupt_process.kill()
            abrupt_return_code = abrupt_process.wait(timeout=_TIMEOUT_SECONDS)
            assert abrupt_return_code != 0
            abrupt_stdout = abrupt_process.stdout
            abrupt_stderr = abrupt_process.stderr
            if abrupt_stdout is None or abrupt_stderr is None:
                raise RuntimeError("abrupt blocker output pipes are unavailable") from None
            assert abrupt_stdout.read(_MAX_LINE_BYTES + 1) == b""
            assert abrupt_stderr.read(_MAX_LINE_BYTES + 1) == b""

            assert _attempt_native_child_rename(roots[abrupt_label]) == _NativeRenameResult(
                succeeded=True,
                error_code=0,
            )
            assert _attempt_native_child_rename(roots[survivor_label]) == denied
            assert survivor_process.poll() is None
            assert not os.path.lexists(live_paths[abrupt_label])
            assert displaced_paths[abrupt_label].is_dir()
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
            permit_launch_return.set()
            both_restoring.set()
            permit_restore.set()
            for thread in threads.values():
                thread.join(timeout=_TIMEOUT_SECONDS)
            for label, process in created_processes.items():
                processes.setdefault(label, process)
            for handle in handles.values():
                if handle not in parent_released and original_get_handle_inheritable(handle):
                    original_set_handle_inheritable(handle, False)
                if handle not in parent_released:
                    blocker_probe.release(handle)
                    parent_released.add(handle)
            for process in processes.values():
                _close_child(process)

    assert blocker_probe.owned_count == 0
    assert all(not thread.is_alive() for thread in threads.values())
    assert set(processes) == set(_LABELS)
    assert processes[abrupt_label].returncode is not None
    assert processes[abrupt_label].returncode != 0
    assert processes[survivor_label].returncode == 0
    for process in processes.values():
        for stream in (process.stdin, process.stdout, process.stderr):
            assert stream is not None and stream.closed
    for label in _LABELS:
        assert (displaced_paths[label] / "candidate.bin").read_bytes() == payloads[label]
