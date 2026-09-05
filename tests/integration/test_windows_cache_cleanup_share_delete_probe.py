"""Test-only Windows cross-process share-delete exclusion probe for M153.

The child command uses fixed relative components beneath pytest-owned temporary
storage. The blocking native handle remains private to the parent process.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest
from test_windows_cache_cleanup_capability_probe import (
    _FILE_FLAG_BACKUP_SEMANTICS,  # pyright: ignore[reportPrivateUsage]
    _FILE_FLAG_OPEN_REPARSE_POINT,  # pyright: ignore[reportPrivateUsage]
    _FILE_LIST_DIRECTORY,  # pyright: ignore[reportPrivateUsage]
    _FILE_READ_ATTRIBUTES,  # pyright: ignore[reportPrivateUsage]
    _FILE_SHARE_READ,  # pyright: ignore[reportPrivateUsage]
    _FILE_SHARE_WRITE,  # pyright: ignore[reportPrivateUsage]
    _INVALID_HANDLE_VALUE,  # pyright: ignore[reportPrivateUsage]
    _OPEN_EXISTING,  # pyright: ignore[reportPrivateUsage]
    _SYNCHRONIZE,  # pyright: ignore[reportPrivateUsage]
    _NativeFailure,  # pyright: ignore[reportPrivateUsage]
    _WindowsCapabilityProbe,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_junction_probe import (
    _filesystem_information,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M153 probes cross-process Windows share-delete exclusion",
)

_RENAME_COMMAND = ("cmd.exe", "/d", "/c", "ren live displaced")


class _ShareDeleteProbe(_WindowsCapabilityProbe):
    def open_directory_without_delete_sharing(self, path: Path) -> int:
        result = cast(
            int | None,
            self._create_file(
                str(path),
                _FILE_LIST_DIRECTORY | _FILE_READ_ATTRIBUTES | _SYNCHRONIZE,
                _FILE_SHARE_READ | _FILE_SHARE_WRITE,
                None,
                _OPEN_EXISTING,
                _FILE_FLAG_BACKUP_SEMANTICS | _FILE_FLAG_OPEN_REPARSE_POINT,
                None,
            ),
        )
        if result is None or result == _INVALID_HANDLE_VALUE:
            raise _NativeFailure(
                "CreateFileW(directory without delete sharing)",
                self._get_last_error(),
            )
        handle = self._adopt(result)
        try:
            self._reject_reparse(handle)
        except BaseException:
            self._close_owned(handle)
            raise
        return handle

    def release(self, handle: int) -> None:
        self._close_owned(handle)


def _attempt_child_rename(working_directory: Path) -> int:
    completed = subprocess.run(
        _RENAME_COMMAND,
        check=False,
        capture_output=True,
        close_fds=True,
        cwd=working_directory,
        shell=False,
        timeout=15.0,
    )
    return completed.returncode


def test_delete_share_omission_blocks_child_rename_until_close(tmp_path: Path) -> None:
    live_path = tmp_path / "live"
    displaced_path = tmp_path / "displaced"
    candidate_path = live_path / "candidate.bin"
    displaced_candidate = displaced_path / "candidate.bin"
    live_path.mkdir()
    candidate_path.write_bytes(b"m153-share-delete-exclusion")

    probe = _ShareDeleteProbe()
    with probe:
        root = probe.open_root(tmp_path)
        filesystem_name, _ = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M153 share-delete fixture requires an NTFS pytest volume")

        blocker = probe.open_directory_without_delete_sharing(live_path)
        try:
            blocked_return_code = _attempt_child_rename(tmp_path)

            assert blocked_return_code != 0
            assert live_path.is_dir()
            assert not os.path.isjunction(live_path)
            assert not os.path.lexists(displaced_path)
            assert candidate_path.read_bytes() == b"m153-share-delete-exclusion"
            assert probe.owned_count == 2
        finally:
            probe.release(blocker)

        assert probe.owned_count == 1
        assert _attempt_child_rename(tmp_path) == 0
        assert not os.path.lexists(live_path)
        assert displaced_path.is_dir()
        assert not os.path.isjunction(displaced_path)
        assert displaced_candidate.read_bytes() == b"m153-share-delete-exclusion"

    assert probe.owned_count == 0
    assert displaced_candidate.read_bytes() == b"m153-share-delete-exclusion"
