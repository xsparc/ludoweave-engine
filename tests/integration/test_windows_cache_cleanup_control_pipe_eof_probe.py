"""Test-only Windows blocker control-pipe EOF probe for M157."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
from test_windows_cache_cleanup_child_owned_blocker_probe import (
    _CHILD,  # pyright: ignore[reportPrivateUsage]
    _MAX_LINE_BYTES,  # pyright: ignore[reportPrivateUsage]
    _TIMEOUT_SECONDS,  # pyright: ignore[reportPrivateUsage]
    _close_child,  # pyright: ignore[reportPrivateUsage]
    _read_ready,  # pyright: ignore[reportPrivateUsage]
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
    reason="M157 probes EOF on a Windows share-delete blocker's control pipe",
)

_CONTROL_EOF_EXIT_CODE = 4


def test_control_pipe_eof_closes_blocker_before_rename_retry(tmp_path: Path) -> None:
    live_path = tmp_path / "live"
    displaced_path = tmp_path / "displaced"
    candidate_path = live_path / "candidate.bin"
    displaced_candidate = displaced_path / "candidate.bin"
    live_path.mkdir()
    candidate_path.write_bytes(b"m157-control-pipe-eof")

    filesystem_probe = _ShareDeleteProbe()
    with filesystem_probe:
        root = filesystem_probe.open_root(tmp_path)
        filesystem_name, _ = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M157 control-pipe fixture requires an NTFS pytest volume")
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
        assert candidate_path.read_bytes() == b"m157-control-pipe-eof"

        stdin = blocker.stdin
        stdout = blocker.stdout
        stderr = blocker.stderr
        if stdin is None or stdout is None or stderr is None:
            raise RuntimeError("share-delete blocker pipes are unavailable") from None
        stdin.close()
        assert stdin.closed

        return_code = blocker.wait(timeout=_TIMEOUT_SECONDS)
        assert return_code == _CONTROL_EOF_EXIT_CODE
        assert stdout.read(_MAX_LINE_BYTES + 1) == b""
        assert stderr.read(_MAX_LINE_BYTES + 1) == b""

        assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
            succeeded=True,
            error_code=0,
        )
        assert not os.path.lexists(live_path)
        assert displaced_path.is_dir()
        assert not os.path.isjunction(displaced_path)
        assert displaced_candidate.read_bytes() == b"m157-control-pipe-eof"
    finally:
        _close_child(blocker)

    assert blocker.returncode == _CONTROL_EOF_EXIT_CODE
    assert displaced_candidate.read_bytes() == b"m157-control-pipe-eof"
