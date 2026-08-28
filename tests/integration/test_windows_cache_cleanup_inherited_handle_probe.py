"""Test-only inherited-handle retention probe for M163."""

from __future__ import annotations

import json
import os
import queue
import subprocess
import sys
import threading
from pathlib import Path
from typing import cast

import pytest
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
    reason="M163 probes explicit Windows inherited blocker-handle retention",
)

_CHILD = Path(__file__).parents[1] / "fixtures/windows_share_delete_inherited_blocker_child.py"
_SCHEMA = "ludoweave.test.windows-inherited-share-delete-blocker/1"
_RELEASE_TOKEN = b"!"
_MAX_LINE_BYTES = 128
_TIMEOUT_SECONDS = 15.0


def _parse_phase(line: bytes) -> str:
    if not line.endswith(b"\n") or len(line) > _MAX_LINE_BYTES:
        raise RuntimeError("inherited-handle blocker returned invalid output") from None
    try:
        payload: object = json.loads(line)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RuntimeError("inherited-handle blocker returned invalid output") from None
    if not isinstance(payload, dict):
        raise RuntimeError("inherited-handle blocker returned invalid output") from None
    document = cast(dict[object, object], payload)
    if set(document) != {"phase", "schema"} or document["schema"] != _SCHEMA:
        raise RuntimeError("inherited-handle blocker returned invalid output") from None
    phase = document["phase"]
    if type(phase) is not str or phase not in {"ready", "closed"}:
        raise RuntimeError("inherited-handle blocker returned invalid output") from None
    return phase


def _read_phase(process: subprocess.Popen[bytes]) -> str:
    stdout = process.stdout
    if stdout is None:
        raise RuntimeError("inherited-handle blocker stdout is unavailable") from None
    results: queue.Queue[bytes | BaseException] = queue.Queue(maxsize=1)

    def read_one_line() -> None:
        try:
            results.put(stdout.readline(_MAX_LINE_BYTES + 1))
        except BaseException as error:  # pragma: no cover - defensive pipe failure
            results.put(error)

    reader = threading.Thread(target=read_one_line, daemon=True)
    reader.start()
    try:
        result = results.get(timeout=_TIMEOUT_SECONDS)
    except queue.Empty:
        process.kill()
        process.wait(timeout=_TIMEOUT_SECONDS)
        reader.join(timeout=_TIMEOUT_SECONDS)
        raise RuntimeError("inherited-handle blocker phase timed out") from None
    reader.join(timeout=_TIMEOUT_SECONDS)
    if reader.is_alive():
        raise RuntimeError("inherited-handle blocker phase did not settle") from None
    if isinstance(result, BaseException):
        raise RuntimeError("inherited-handle blocker phase failed") from result
    return _parse_phase(result)


def _spawn_inherited_blocker(handle: int, working_directory: Path) -> subprocess.Popen[bytes]:
    startup_info = subprocess.STARTUPINFO()
    startup_info.lpAttributeList = {"handle_list": [handle]}
    if os.get_handle_inheritable(handle):
        raise RuntimeError("blocker handle was unexpectedly inheritable") from None
    process: subprocess.Popen[bytes] | None = None
    os.set_handle_inheritable(handle, True)
    try:
        process = subprocess.Popen(
            (sys.executable, "-I", "-B", str(_CHILD), str(handle)),
            close_fds=True,
            cwd=working_directory,
            shell=False,
            startupinfo=startup_info,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    finally:
        try:
            os.set_handle_inheritable(handle, False)
        except BaseException:
            if process is not None:
                _close_child(process)
            raise
    if process is None:  # pragma: no cover - Popen either returns or raises
        raise RuntimeError("inherited-handle blocker did not start") from None
    return process


def test_inherited_handle_retains_blocker_after_parent_closes(tmp_path: Path) -> None:
    live_path = tmp_path / "live"
    displaced_path = tmp_path / "displaced"
    candidate_path = live_path / "candidate.bin"
    displaced_candidate = displaced_path / "candidate.bin"
    live_path.mkdir()
    candidate_path.write_bytes(b"m163-inherited-handle-retention")

    filesystem_probe = _ShareDeleteProbe()
    with filesystem_probe:
        root = filesystem_probe.open_root(tmp_path)
        filesystem_name, _ = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M163 inherited-handle fixture requires an NTFS pytest volume")
    assert filesystem_probe.owned_count == 0

    blocker_probe = _ShareDeleteProbe()
    with blocker_probe:
        blocker_handle = blocker_probe.open_directory_without_delete_sharing(live_path)
        blocker = _spawn_inherited_blocker(blocker_handle, tmp_path)
        try:
            assert os.get_handle_inheritable(blocker_handle) is False
            assert _read_phase(blocker) == "ready"
            assert blocker.poll() is None
            assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
                succeeded=False,
                error_code=_ERROR_SHARING_VIOLATION,
            )
            assert live_path.is_dir()
            assert not os.path.isjunction(live_path)
            assert not os.path.lexists(displaced_path)
            assert candidate_path.read_bytes() == b"m163-inherited-handle-retention"
            assert blocker_probe.owned_count == 1

            blocker_probe.release(blocker_handle)
            assert blocker_probe.owned_count == 0
            assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
                succeeded=False,
                error_code=_ERROR_SHARING_VIOLATION,
            )
            assert blocker.poll() is None
            assert live_path.is_dir()
            assert not os.path.isjunction(live_path)
            assert not os.path.lexists(displaced_path)
            assert candidate_path.read_bytes() == b"m163-inherited-handle-retention"

            stdin = blocker.stdin
            stdout = blocker.stdout
            stderr = blocker.stderr
            assert stdin is not None and stdout is not None and stderr is not None
            stdin.write(_RELEASE_TOKEN)
            stdin.flush()
            stdin.close()
            assert _read_phase(blocker) == "closed"
            assert blocker.wait(timeout=_TIMEOUT_SECONDS) == 0
            assert stdout.read(_MAX_LINE_BYTES + 1) == b""
            assert stderr.read(_MAX_LINE_BYTES + 1) == b""

            assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
                succeeded=True,
                error_code=0,
            )
            assert not os.path.lexists(live_path)
            assert displaced_path.is_dir()
            assert not os.path.isjunction(displaced_path)
            assert displaced_candidate.read_bytes() == b"m163-inherited-handle-retention"
        finally:
            _close_child(blocker)

    assert blocker.returncode == 0
    assert displaced_candidate.read_bytes() == b"m163-inherited-handle-retention"
