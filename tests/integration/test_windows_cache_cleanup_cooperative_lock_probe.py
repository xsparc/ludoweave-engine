"""Test-only Windows cooperative shared/exclusive lock probe for M173."""

from __future__ import annotations

import ctypes
import json
import os
import queue
import subprocess
import sys
import threading
from collections.abc import Callable
from ctypes import wintypes
from pathlib import Path
from typing import cast

import pytest
from test_windows_cache_cleanup_capability_probe import (
    _FILE_SHARE_DELETE,  # pyright: ignore[reportPrivateUsage]
    _FILE_SHARE_READ,  # pyright: ignore[reportPrivateUsage]
    _FILE_SHARE_WRITE,  # pyright: ignore[reportPrivateUsage]
    _INVALID_HANDLE_VALUE,  # pyright: ignore[reportPrivateUsage]
    _OPEN_EXISTING,  # pyright: ignore[reportPrivateUsage]
    _load_function,  # pyright: ignore[reportPrivateUsage]
    _NativeFailure,  # pyright: ignore[reportPrivateUsage]
    _WindowsCapabilityProbe,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_exclusive_root_acquisition_probe import (
    _require_ntfs,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M173 probes Windows cooperative shared/exclusive coordination",
)

_CHILD = Path(__file__).parents[1] / "fixtures/windows_coordination_lock_participant_child.py"
_SCHEMA = "ludoweave.test.windows-coordination-lock-participant/1"
_RELEASE_TOKEN = b"!"
_GENERIC_READ = 0x80000000
_FILE_ATTRIBUTE_NORMAL = 0x00000080
_LOCKFILE_FAIL_IMMEDIATELY = 0x00000001
_LOCKFILE_EXCLUSIVE_LOCK = 0x00000002
_ERROR_LOCK_VIOLATION = 33
_MAX_LINE_BYTES = 192
_TIMEOUT_SECONDS = 15.0


class _Overlapped(ctypes.Structure):
    _fields_ = [
        ("Internal", ctypes.c_size_t),
        ("InternalHigh", ctypes.c_size_t),
        ("Offset", wintypes.DWORD),
        ("OffsetHigh", wintypes.DWORD),
        ("hEvent", wintypes.HANDLE),
    ]


class _CoordinationLockProbe(_WindowsCapabilityProbe):
    def __init__(self) -> None:
        super().__init__()
        win_dll = cast(Callable[..., ctypes.CDLL], vars(ctypes)["WinDLL"])
        kernel32 = win_dll("kernel32", use_last_error=True)
        self._lock_file_ex = _load_function(
            kernel32,
            "LockFileEx",
            [
                wintypes.HANDLE,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.DWORD,
                ctypes.POINTER(_Overlapped),
            ],
            wintypes.BOOL,
        )
        self._unlock_file_ex = _load_function(
            kernel32,
            "UnlockFileEx",
            [
                wintypes.HANDLE,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.DWORD,
                ctypes.POINTER(_Overlapped),
            ],
            wintypes.BOOL,
        )
        self._exclusive: dict[int, _Overlapped] = {}

    def acquire_exclusive(self, path: Path) -> int:
        raw_handle = cast(
            int | None,
            self._create_file(
                str(path),
                _GENERIC_READ,
                _FILE_SHARE_READ | _FILE_SHARE_WRITE | _FILE_SHARE_DELETE,
                None,
                _OPEN_EXISTING,
                _FILE_ATTRIBUTE_NORMAL,
                None,
            ),
        )
        if raw_handle is None or raw_handle == _INVALID_HANDLE_VALUE:
            raise _NativeFailure("CreateFileW(coordination)", self._get_last_error())
        handle = self._adopt(raw_handle)
        try:
            self._reject_reparse(handle)
            overlapped = _Overlapped()
            if not cast(
                bool,
                self._lock_file_ex(
                    wintypes.HANDLE(handle),
                    _LOCKFILE_FAIL_IMMEDIATELY | _LOCKFILE_EXCLUSIVE_LOCK,
                    0,
                    1,
                    0,
                    ctypes.byref(overlapped),
                ),
            ):
                raise _NativeFailure("LockFileEx(exclusive)", self._get_last_error())
            self._exclusive[handle] = overlapped
        except BaseException:
            self._close_owned(handle)
            raise
        return handle

    def release_exclusive(self, handle: int) -> None:
        overlapped = self._exclusive[handle]
        self._require_win32(
            "UnlockFileEx(exclusive)",
            self._unlock_file_ex(
                wintypes.HANDLE(handle),
                0,
                1,
                0,
                ctypes.byref(overlapped),
            ),
        )
        del self._exclusive[handle]
        self._close_owned(handle)

    def close(self) -> None:
        while self._exclusive:
            self.release_exclusive(next(reversed(self._exclusive)))
        super().close()


def _parse_event(line: bytes) -> tuple[str, int]:
    if not line.endswith(b"\n") or len(line) > _MAX_LINE_BYTES:
        raise RuntimeError("coordination participant returned invalid structured output") from None
    try:
        payload: object = json.loads(line)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RuntimeError("coordination participant returned invalid structured output") from None
    if not isinstance(payload, dict):
        raise RuntimeError("coordination participant returned invalid structured output") from None
    document = cast(dict[object, object], payload)
    if set(document) != {"error_code", "phase", "schema"} or document["schema"] != _SCHEMA:
        raise RuntimeError("coordination participant returned invalid structured output") from None
    phase = document["phase"]
    error_code = document["error_code"]
    if (
        type(phase) is not str
        or phase not in {"ready", "closed", "refused"}
        or type(error_code) is not int
        or error_code < 0
        or (phase == "refused") != (error_code > 0)
    ):
        raise RuntimeError("coordination participant returned invalid structured output") from None
    return phase, error_code


def _start_participant(working_directory: Path) -> subprocess.Popen[bytes]:
    return subprocess.Popen(
        (sys.executable, "-I", "-B", str(_CHILD)),
        close_fds=True,
        cwd=working_directory,
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _read_event(process: subprocess.Popen[bytes]) -> tuple[str, int]:
    stdout = process.stdout
    if stdout is None:
        raise RuntimeError("coordination participant stdout is unavailable") from None
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
        raise RuntimeError("coordination participant event timed out") from None
    reader.join(timeout=_TIMEOUT_SECONDS)
    if reader.is_alive():
        raise RuntimeError("coordination participant event did not settle") from None
    if isinstance(result, BaseException):
        raise RuntimeError("coordination participant event failed") from result
    return _parse_event(result)


def _release_and_read_closed(process: subprocess.Popen[bytes]) -> tuple[str, int]:
    stdin = process.stdin
    stdout = process.stdout
    stderr = process.stderr
    if stdin is None or stdout is None or stderr is None:
        raise RuntimeError("coordination participant pipes are unavailable") from None
    stdin.write(_RELEASE_TOKEN)
    stdin.flush()
    stdin.close()
    try:
        return_code = process.wait(timeout=_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=_TIMEOUT_SECONDS)
        raise RuntimeError("coordination participant close timed out") from None
    closed = _parse_event(stdout.readline(_MAX_LINE_BYTES + 1))
    if return_code != 0 or stdout.read(_MAX_LINE_BYTES + 1) or stderr.read(_MAX_LINE_BYTES + 1):
        raise RuntimeError("coordination participant returned invalid closure output") from None
    return closed


def _read_refused(process: subprocess.Popen[bytes]) -> tuple[str, int]:
    refused = _read_event(process)
    try:
        return_code = process.wait(timeout=_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=_TIMEOUT_SECONDS)
        raise RuntimeError("coordination participant refusal timed out") from None
    stdout = process.stdout
    stderr = process.stderr
    if (
        stdout is None
        or stderr is None
        or return_code != 0
        or stdout.read(_MAX_LINE_BYTES + 1)
        or stderr.read(_MAX_LINE_BYTES + 1)
    ):
        raise RuntimeError("coordination participant returned invalid refusal output") from None
    return refused


def _close_participant(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is None:
        process.kill()
        process.wait(timeout=_TIMEOUT_SECONDS)
    for stream in (process.stdin, process.stdout, process.stderr):
        if stream is not None:
            stream.close()


def _create_fixture(tmp_path: Path) -> tuple[Path, bytes]:
    live_path = tmp_path / "live"
    live_path.mkdir()
    coordination_path = live_path / "coordination.lock"
    payload = b"ludoweave-m173-coordination-v1\n"
    coordination_path.write_bytes(payload)
    _require_ntfs(tmp_path)
    return coordination_path, payload


def test_shared_participants_collectively_refuse_exclusive_until_last_close(
    tmp_path: Path,
) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    first = _start_participant(tmp_path)
    second = _start_participant(tmp_path)
    try:
        assert _read_event(first) == ("ready", 0)
        assert _read_event(second) == ("ready", 0)
        assert first.poll() is None
        assert second.poll() is None

        probe = _CoordinationLockProbe()
        with probe:
            with pytest.raises(
                _NativeFailure,
                match=r"LockFileEx\(exclusive\) failed with native code 33",
            ) as both_active:
                probe.acquire_exclusive(coordination_path)
            assert both_active.value.code == _ERROR_LOCK_VIOLATION
            assert probe.owned_count == 0

            assert _release_and_read_closed(first) == ("closed", 0)
            assert first.returncode == 0
            assert second.poll() is None
            with pytest.raises(_NativeFailure) as one_active:
                probe.acquire_exclusive(coordination_path)
            assert one_active.value.code == _ERROR_LOCK_VIOLATION
            assert probe.owned_count == 0

            assert _release_and_read_closed(second) == ("closed", 0)
            assert second.returncode == 0
            exclusive = probe.acquire_exclusive(coordination_path)
            assert os.get_handle_inheritable(exclusive) is False
            assert probe.owned_count == 1
            probe.release_exclusive(exclusive)
            assert probe.owned_count == 0
    finally:
        _close_participant(first)
        _close_participant(second)

    assert coordination_path.read_bytes() == payload


def test_exclusive_refuses_late_participant_until_release(tmp_path: Path) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    denied: subprocess.Popen[bytes] | None = None
    admitted: subprocess.Popen[bytes] | None = None

    probe = _CoordinationLockProbe()
    with probe:
        exclusive = probe.acquire_exclusive(coordination_path)
        assert os.get_handle_inheritable(exclusive) is False
        assert probe.owned_count == 1
        denied = _start_participant(tmp_path)
        try:
            assert _read_refused(denied) == ("refused", _ERROR_LOCK_VIOLATION)
            assert denied.returncode == 0
            assert probe.owned_count == 1
        finally:
            _close_participant(denied)

        probe.release_exclusive(exclusive)
        assert probe.owned_count == 0
        admitted = _start_participant(tmp_path)
        try:
            assert _read_event(admitted) == ("ready", 0)
            assert admitted.poll() is None
            assert _release_and_read_closed(admitted) == ("closed", 0)
            assert admitted.returncode == 0
        finally:
            _close_participant(admitted)

    assert denied.returncode == 0
    assert admitted.returncode == 0
    assert coordination_path.read_bytes() == payload
