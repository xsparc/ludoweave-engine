"""Test-only child-owned Windows share-delete handshake for M155."""

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
    reason="M155 probes a child-owned Windows share-delete blocker",
)

_CHILD = Path(__file__).parents[1] / "fixtures/windows_share_delete_blocker_child.py"
_SCHEMA = "ludoweave.test.windows-share-delete-blocker/1"
_RELEASE_TOKEN = b"!"
_MAX_LINE_BYTES = 128
_TIMEOUT_SECONDS = 15.0


def _parse_phase(line: bytes) -> str:
    if not line.endswith(b"\n") or len(line) > _MAX_LINE_BYTES:
        raise RuntimeError("share-delete blocker returned invalid structured output") from None
    try:
        payload: object = json.loads(line)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RuntimeError("share-delete blocker returned invalid structured output") from None
    if not isinstance(payload, dict):
        raise RuntimeError("share-delete blocker returned invalid structured output") from None
    document = cast(dict[object, object], payload)
    if set(document) != {"phase", "schema"} or document["schema"] != _SCHEMA:
        raise RuntimeError("share-delete blocker returned invalid structured output") from None
    phase = document["phase"]
    if type(phase) is not str or phase not in {"ready", "closed"}:
        raise RuntimeError("share-delete blocker returned invalid structured output") from None
    return phase


def _read_ready(process: subprocess.Popen[bytes]) -> str:
    stdout = process.stdout
    if stdout is None:
        raise RuntimeError("share-delete blocker stdout is unavailable") from None
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
        raise RuntimeError("share-delete blocker readiness timed out") from None
    reader.join(timeout=_TIMEOUT_SECONDS)
    if reader.is_alive():
        raise RuntimeError("share-delete blocker readiness did not settle") from None
    if isinstance(result, BaseException):
        raise RuntimeError("share-delete blocker readiness failed") from result
    return _parse_phase(result)


def _release_and_read_closed(process: subprocess.Popen[bytes]) -> str:
    stdin = process.stdin
    stdout = process.stdout
    stderr = process.stderr
    if stdin is None or stdout is None or stderr is None:
        raise RuntimeError("share-delete blocker pipes are unavailable") from None
    stdin.write(_RELEASE_TOKEN)
    stdin.flush()
    stdin.close()
    try:
        return_code = process.wait(timeout=_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=_TIMEOUT_SECONDS)
        raise RuntimeError("share-delete blocker close timed out") from None
    closed_line = stdout.readline(_MAX_LINE_BYTES + 1)
    extra_stdout = stdout.read(_MAX_LINE_BYTES + 1)
    child_stderr = stderr.read(_MAX_LINE_BYTES + 1)
    if return_code != 0 or extra_stdout or child_stderr:
        raise RuntimeError("share-delete blocker returned invalid closure output") from None
    return _parse_phase(closed_line)


def _close_child(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is None:
        process.kill()
        process.wait(timeout=_TIMEOUT_SECONDS)
    for stream in (process.stdin, process.stdout, process.stderr):
        if stream is not None:
            stream.close()


def test_child_owned_blocker_denies_rename_until_acknowledged_close(tmp_path: Path) -> None:
    live_path = tmp_path / "live"
    displaced_path = tmp_path / "displaced"
    candidate_path = live_path / "candidate.bin"
    displaced_candidate = displaced_path / "candidate.bin"
    live_path.mkdir()
    candidate_path.write_bytes(b"m155-child-owned-share-delete")

    filesystem_probe = _ShareDeleteProbe()
    with filesystem_probe:
        root = filesystem_probe.open_root(tmp_path)
        filesystem_name, _ = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M155 child-owned fixture requires an NTFS pytest volume")
    assert filesystem_probe.owned_count == 0

    blocker = subprocess.Popen(
        (sys.executable, "-I", "-B", str(_CHILD)),
        close_fds=True,
        cwd=tmp_path,
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        assert _read_ready(blocker) == "ready"
        assert blocker.poll() is None

        assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
            succeeded=False,
            error_code=_ERROR_SHARING_VIOLATION,
        )
        assert blocker.poll() is None
        assert live_path.is_dir()
        assert not os.path.isjunction(live_path)
        assert not os.path.lexists(displaced_path)
        assert candidate_path.read_bytes() == b"m155-child-owned-share-delete"

        assert _release_and_read_closed(blocker) == "closed"
        assert blocker.returncode == 0
        assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
            succeeded=True,
            error_code=0,
        )
        assert not os.path.lexists(live_path)
        assert displaced_path.is_dir()
        assert not os.path.isjunction(displaced_path)
        assert displaced_candidate.read_bytes() == b"m155-child-owned-share-delete"
    finally:
        _close_child(blocker)

    assert blocker.returncode == 0
    assert displaced_candidate.read_bytes() == b"m155-child-owned-share-delete"
