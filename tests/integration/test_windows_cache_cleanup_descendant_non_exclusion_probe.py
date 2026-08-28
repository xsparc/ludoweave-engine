"""Test-only Windows root/descendant non-exclusion probe for M172."""

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
from test_windows_cache_cleanup_exclusive_root_acquisition_probe import (
    _ExclusiveDirectoryProbe,  # pyright: ignore[reportPrivateUsage]
    _require_ntfs,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M172 probes Windows directory/descendant non-exclusion",
)

_CHILD = Path(__file__).parents[1] / "fixtures/windows_descendant_file_holder_child.py"
_SCHEMA = "ludoweave.test.windows-descendant-file-holder/1"
_RELEASE_TOKEN = b"!"
_MAX_LINE_BYTES = 128
_TIMEOUT_SECONDS = 15.0


def _parse_phase(line: bytes) -> str:
    if not line.endswith(b"\n") or len(line) > _MAX_LINE_BYTES:
        raise RuntimeError("descendant holder returned invalid structured output") from None
    try:
        payload: object = json.loads(line)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RuntimeError("descendant holder returned invalid structured output") from None
    if not isinstance(payload, dict):
        raise RuntimeError("descendant holder returned invalid structured output") from None
    document = cast(dict[object, object], payload)
    if set(document) != {"phase", "schema"} or document["schema"] != _SCHEMA:
        raise RuntimeError("descendant holder returned invalid structured output") from None
    phase = document["phase"]
    if type(phase) is not str or phase not in {"ready", "closed"}:
        raise RuntimeError("descendant holder returned invalid structured output") from None
    return phase


def _start_holder(working_directory: Path) -> subprocess.Popen[bytes]:
    return subprocess.Popen(
        (sys.executable, "-I", "-B", str(_CHILD)),
        close_fds=True,
        cwd=working_directory,
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _read_ready(process: subprocess.Popen[bytes]) -> str:
    stdout = process.stdout
    if stdout is None:
        raise RuntimeError("descendant holder stdout is unavailable") from None
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
        raise RuntimeError("descendant holder readiness timed out") from None
    reader.join(timeout=_TIMEOUT_SECONDS)
    if reader.is_alive():
        raise RuntimeError("descendant holder readiness did not settle") from None
    if isinstance(result, BaseException):
        raise RuntimeError("descendant holder readiness failed") from result
    return _parse_phase(result)


def _release_and_read_closed(process: subprocess.Popen[bytes]) -> str:
    stdin = process.stdin
    stdout = process.stdout
    stderr = process.stderr
    if stdin is None or stdout is None or stderr is None:
        raise RuntimeError("descendant holder pipes are unavailable") from None
    stdin.write(_RELEASE_TOKEN)
    stdin.flush()
    stdin.close()
    try:
        return_code = process.wait(timeout=_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=_TIMEOUT_SECONDS)
        raise RuntimeError("descendant holder close timed out") from None
    closed_line = stdout.readline(_MAX_LINE_BYTES + 1)
    extra_stdout = stdout.read(_MAX_LINE_BYTES + 1)
    child_stderr = stderr.read(_MAX_LINE_BYTES + 1)
    if return_code != 0 or extra_stdout or child_stderr:
        raise RuntimeError("descendant holder returned invalid closure output") from None
    return _parse_phase(closed_line)


def _close_holder(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is None:
        process.kill()
        process.wait(timeout=_TIMEOUT_SECONDS)
    for stream in (process.stdin, process.stdout, process.stderr):
        if stream is not None:
            stream.close()


def _create_fixture(tmp_path: Path, payload: bytes) -> tuple[Path, Path]:
    live_path = tmp_path / "live"
    candidate_path = live_path / "candidate.bin"
    live_path.mkdir()
    candidate_path.write_bytes(payload)
    _require_ntfs(tmp_path)
    return live_path, candidate_path


def test_exclusive_root_does_not_refuse_late_descendant_holder(tmp_path: Path) -> None:
    payload = b"m172-root-first-descendant"
    live_path, candidate_path = _create_fixture(tmp_path, payload)

    probe = _ExclusiveDirectoryProbe()
    holder: subprocess.Popen[bytes] | None = None
    with probe:
        exclusive = probe.open_directory_exclusive(live_path)
        assert os.get_handle_inheritable(exclusive) is False
        assert probe.owned_count == 1
        holder = _start_holder(tmp_path)
        try:
            assert _read_ready(holder) == "ready"
            assert holder.poll() is None
            assert probe.owned_count == 1
            assert candidate_path.read_bytes() == payload
            assert _release_and_read_closed(holder) == "closed"
            assert holder.returncode == 0
            assert probe.owned_count == 1
        finally:
            _close_holder(holder)
        probe.release(exclusive)
        assert probe.owned_count == 0

    assert holder.returncode == 0
    assert probe.owned_count == 0
    assert candidate_path.read_bytes() == payload


def test_existing_descendant_holder_does_not_refuse_exclusive_root(tmp_path: Path) -> None:
    payload = b"m172-descendant-first-root"
    live_path, candidate_path = _create_fixture(tmp_path, payload)

    holder = _start_holder(tmp_path)
    try:
        assert _read_ready(holder) == "ready"
        assert holder.poll() is None

        probe = _ExclusiveDirectoryProbe()
        with probe:
            exclusive = probe.open_directory_exclusive(live_path)
            assert os.get_handle_inheritable(exclusive) is False
            assert probe.owned_count == 1
            assert holder.poll() is None
            assert candidate_path.read_bytes() == payload
            probe.release(exclusive)
            assert probe.owned_count == 0
            assert holder.poll() is None

        assert _release_and_read_closed(holder) == "closed"
        assert holder.returncode == 0
    finally:
        _close_holder(holder)

    assert holder.returncode == 0
    assert candidate_path.read_bytes() == payload
