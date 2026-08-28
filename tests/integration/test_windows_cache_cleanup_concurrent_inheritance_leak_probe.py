"""Test-only controlled Windows concurrent handle-inheritance leak probe."""

from __future__ import annotations

import os
import queue
import subprocess
import sys
import threading
from collections.abc import Sequence
from pathlib import Path
from types import SimpleNamespace

import pytest
import test_windows_cache_cleanup_inherited_handle_probe as inherited_probe
from test_windows_cache_cleanup_child_owned_blocker_probe import (
    _close_child,  # pyright: ignore[reportPrivateUsage]
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
    reason="M166 probes a controlled concurrent Windows inheritance leak",
)

_CHILD = Path(__file__).parents[1] / "fixtures/windows_share_delete_inherited_blocker_child.py"
_RELEASE_TOKEN = b"!"
_MAX_LINE_BYTES = 128
_TIMEOUT_SECONDS = 15.0


def _release_inherited_blocker(process: subprocess.Popen[bytes]) -> None:
    stdin = process.stdin
    stdout = process.stdout
    stderr = process.stderr
    if stdin is None or stdout is None or stderr is None:
        raise RuntimeError("inherited blocker pipes are unavailable") from None
    stdin.write(_RELEASE_TOKEN)
    stdin.flush()
    stdin.close()
    assert inherited_probe._read_phase(process) == "closed"  # pyright: ignore[reportPrivateUsage]
    assert process.wait(timeout=_TIMEOUT_SECONDS) == 0
    assert stdout.read(_MAX_LINE_BYTES + 1) == b""
    assert stderr.read(_MAX_LINE_BYTES + 1) == b""


def test_concurrent_broad_launch_inherits_temporarily_inheritable_blocker(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    live_path = tmp_path / "live"
    displaced_path = tmp_path / "displaced"
    candidate_path = live_path / "candidate.bin"
    displaced_candidate = displaced_path / "candidate.bin"
    live_path.mkdir()
    candidate_path.write_bytes(b"m166-concurrent-inheritance-leak")

    filesystem_probe = _ShareDeleteProbe()
    with filesystem_probe:
        root = filesystem_probe.open_root(tmp_path)
        filesystem_name, _ = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M166 concurrent-inheritance fixture requires an NTFS pytest volume")
    assert filesystem_probe.owned_count == 0

    blocker_probe = _ShareDeleteProbe()
    with blocker_probe:
        blocker_handle = blocker_probe.open_directory_without_delete_sharing(live_path)
        original_popen = subprocess.Popen
        original_set_handle_inheritable = os.set_handle_inheritable
        explicit_launch_waiting = threading.Event()
        permit_explicit_launch = threading.Event()
        explicit_results: queue.Queue[subprocess.Popen[bytes] | BaseException] = queue.Queue(
            maxsize=1
        )
        parent_released = False
        explicit_process: subprocess.Popen[bytes] | None = None
        broad_process: subprocess.Popen[bytes] | None = None

        def pause_explicit_launch(
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
            assert close_fds is True
            assert cwd == tmp_path
            assert shell is False
            assert startupinfo.lpAttributeList == {"handle_list": [blocker_handle]}
            assert stdin == subprocess.PIPE
            assert stdout == subprocess.PIPE
            assert stderr == subprocess.PIPE
            explicit_launch_waiting.set()
            if not permit_explicit_launch.wait(timeout=_TIMEOUT_SECONDS):
                raise RuntimeError("explicit inherited launch was not released") from None
            return original_popen(
                arguments,
                close_fds=close_fds,
                cwd=cwd,
                shell=shell,
                startupinfo=startupinfo,
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
            )

        def spawn_explicit_child() -> None:
            try:
                explicit_results.put(
                    inherited_probe._spawn_inherited_blocker(  # pyright: ignore[reportPrivateUsage]
                        blocker_handle,
                        tmp_path,
                    )
                )
            except BaseException as error:
                explicit_results.put(error)

        monkeypatch.setattr(
            inherited_probe,
            "subprocess",
            SimpleNamespace(
                PIPE=subprocess.PIPE,
                Popen=pause_explicit_launch,
                STARTUPINFO=subprocess.STARTUPINFO,
            ),
        )
        explicit_thread = threading.Thread(target=spawn_explicit_child, daemon=True)
        explicit_thread.start()

        try:
            assert explicit_launch_waiting.wait(timeout=_TIMEOUT_SECONDS)
            assert explicit_thread.is_alive()
            assert os.get_handle_inheritable(blocker_handle) is True

            broad_process = original_popen(
                (sys.executable, "-I", "-B", str(_CHILD), str(blocker_handle)),
                close_fds=False,
                cwd=tmp_path,
                executable=sys.executable,
                shell=False,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            assert inherited_probe._read_phase(broad_process) == "ready"  # pyright: ignore[reportPrivateUsage]
            assert broad_process.poll() is None

            permit_explicit_launch.set()
            explicit_thread.join(timeout=_TIMEOUT_SECONDS)
            assert not explicit_thread.is_alive()
            explicit_result = explicit_results.get_nowait()
            if isinstance(explicit_result, BaseException):
                raise explicit_result
            explicit_process = explicit_result
            assert inherited_probe._read_phase(explicit_process) == "ready"  # pyright: ignore[reportPrivateUsage]
            assert explicit_process.poll() is None
            assert os.get_handle_inheritable(blocker_handle) is False
            assert blocker_probe.owned_count == 1

            assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
                succeeded=False,
                error_code=_ERROR_SHARING_VIOLATION,
            )
            blocker_probe.release(blocker_handle)
            parent_released = True
            assert blocker_probe.owned_count == 0
            assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
                succeeded=False,
                error_code=_ERROR_SHARING_VIOLATION,
            )

            _release_inherited_blocker(explicit_process)
            assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
                succeeded=False,
                error_code=_ERROR_SHARING_VIOLATION,
            )
            assert broad_process.poll() is None
            assert live_path.is_dir()
            assert not os.path.isjunction(live_path)
            assert not os.path.lexists(displaced_path)
            assert candidate_path.read_bytes() == b"m166-concurrent-inheritance-leak"

            _release_inherited_blocker(broad_process)
            assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
                succeeded=True,
                error_code=0,
            )
            assert not os.path.lexists(live_path)
            assert displaced_path.is_dir()
            assert not os.path.isjunction(displaced_path)
            assert displaced_candidate.read_bytes() == b"m166-concurrent-inheritance-leak"
        finally:
            permit_explicit_launch.set()
            explicit_thread.join(timeout=_TIMEOUT_SECONDS)
            if explicit_process is None:
                try:
                    pending_result = explicit_results.get_nowait()
                except queue.Empty:
                    pass
                else:
                    if not isinstance(pending_result, BaseException):
                        explicit_process = pending_result
            if not parent_released and os.get_handle_inheritable(blocker_handle):
                original_set_handle_inheritable(blocker_handle, False)
            for process in (explicit_process, broad_process):
                if process is not None:
                    _close_child(process)

    assert blocker_probe.owned_count == 0
    assert not explicit_thread.is_alive()
    for process in (explicit_process, broad_process):
        assert process is not None
        assert process.returncode == 0
        for stream in (process.stdin, process.stdout, process.stderr):
            assert stream is not None and stream.closed
    assert displaced_candidate.read_bytes() == b"m166-concurrent-inheritance-leak"
