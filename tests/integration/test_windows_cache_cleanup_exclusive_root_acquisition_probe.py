"""Test-only Windows exclusive-root acquisition and refusal probe for M171."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import pytest
from test_windows_cache_cleanup_capability_probe import (
    _FILE_FLAG_BACKUP_SEMANTICS,  # pyright: ignore[reportPrivateUsage]
    _FILE_FLAG_OPEN_REPARSE_POINT,  # pyright: ignore[reportPrivateUsage]
    _FILE_LIST_DIRECTORY,  # pyright: ignore[reportPrivateUsage]
    _FILE_READ_ATTRIBUTES,  # pyright: ignore[reportPrivateUsage]
    _INVALID_HANDLE_VALUE,  # pyright: ignore[reportPrivateUsage]
    _OPEN_EXISTING,  # pyright: ignore[reportPrivateUsage]
    _SYNCHRONIZE,  # pyright: ignore[reportPrivateUsage]
    _NativeFailure,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_child_owned_blocker_probe import (
    _CHILD as _BLOCKER_CHILD,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_child_owned_blocker_probe import (
    _close_child,  # pyright: ignore[reportPrivateUsage]
    _read_ready,  # pyright: ignore[reportPrivateUsage]
    _release_and_read_closed,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_junction_probe import (
    _filesystem_information,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_native_error_probe import (
    _ERROR_SHARING_VIOLATION,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_share_delete_probe import (
    _ShareDeleteProbe,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M171 probes Windows exclusive-root acquisition and refusal",
)

_OPEN_CHILD = Path(__file__).parents[1] / "fixtures/windows_exclusive_directory_open_child.py"
_SCHEMA = "ludoweave.test.windows-directory-open/1"
_MAX_CHILD_OUTPUT_BYTES = 512
_TIMEOUT_SECONDS = 15.0


@dataclass(frozen=True, slots=True)
class _DirectoryOpenResult:
    succeeded: bool
    error_code: int


class _ExclusiveDirectoryProbe(_ShareDeleteProbe):
    def open_directory_exclusive(self, path: Path) -> int:
        result = cast(
            int | None,
            self._create_file(
                str(path),
                _FILE_LIST_DIRECTORY | _FILE_READ_ATTRIBUTES | _SYNCHRONIZE,
                0,
                None,
                _OPEN_EXISTING,
                _FILE_FLAG_BACKUP_SEMANTICS | _FILE_FLAG_OPEN_REPARSE_POINT,
                None,
            ),
        )
        if result is None or result == _INVALID_HANDLE_VALUE:
            raise _NativeFailure(
                "CreateFileW(exclusive directory)",
                self._get_last_error(),
            )
        handle = self._adopt(result)
        try:
            self._reject_reparse(handle)
        except BaseException:
            self._close_owned(handle)
            raise
        return handle


def _require_ntfs(path: Path) -> None:
    probe = _ShareDeleteProbe()
    with probe:
        root = probe.open_root(path)
        filesystem_name, _ = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M171 exclusive-root fixture requires an NTFS pytest volume")
    assert probe.owned_count == 0


def _attempt_child_open(working_directory: Path) -> _DirectoryOpenResult:
    completed = subprocess.run(
        (sys.executable, "-I", "-B", str(_OPEN_CHILD)),
        check=False,
        capture_output=True,
        close_fds=True,
        cwd=working_directory,
        shell=False,
        stdin=subprocess.DEVNULL,
        timeout=_TIMEOUT_SECONDS,
    )
    if (
        completed.returncode != 0
        or completed.stderr
        or len(completed.stdout) > _MAX_CHILD_OUTPUT_BYTES
    ):
        raise RuntimeError("exclusive directory child returned invalid structured output") from None
    try:
        payload: object = json.loads(completed.stdout)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RuntimeError("exclusive directory child returned invalid structured output") from None
    if not isinstance(payload, dict):
        raise RuntimeError("exclusive directory child returned invalid structured output") from None
    document = cast(dict[object, object], payload)
    if set(document) != {"error_code", "schema", "succeeded"}:
        raise RuntimeError("exclusive directory child returned invalid structured output") from None
    succeeded = document["succeeded"]
    error_code = document["error_code"]
    if (
        document["schema"] != _SCHEMA
        or type(succeeded) is not bool
        or type(error_code) is not int
        or error_code < 0
        or (succeeded and error_code != 0)
    ):
        raise RuntimeError("exclusive directory child returned invalid structured output") from None
    return _DirectoryOpenResult(succeeded=succeeded, error_code=error_code)


def _start_existing_participant(working_directory: Path) -> subprocess.Popen[bytes]:
    return subprocess.Popen(
        (sys.executable, "-I", "-B", str(_BLOCKER_CHILD)),
        close_fds=True,
        cwd=working_directory,
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_exclusive_owner_denies_late_child_until_close(tmp_path: Path) -> None:
    live_path = tmp_path / "live"
    candidate_path = live_path / "candidate.bin"
    live_path.mkdir()
    candidate_path.write_bytes(b"m171-exclusive-owner")
    _require_ntfs(tmp_path)

    probe = _ExclusiveDirectoryProbe()
    with probe:
        exclusive = probe.open_directory_exclusive(live_path)
        assert os.get_handle_inheritable(exclusive) is False
        assert probe.owned_count == 1

        assert _attempt_child_open(tmp_path) == _DirectoryOpenResult(
            succeeded=False,
            error_code=_ERROR_SHARING_VIOLATION,
        )
        assert candidate_path.read_bytes() == b"m171-exclusive-owner"
        assert probe.owned_count == 1

        probe.release(exclusive)
        assert probe.owned_count == 0
        assert _attempt_child_open(tmp_path) == _DirectoryOpenResult(
            succeeded=True,
            error_code=0,
        )

    assert probe.owned_count == 0
    assert candidate_path.read_bytes() == b"m171-exclusive-owner"


def test_existing_child_causes_exclusive_acquisition_to_fail_closed(tmp_path: Path) -> None:
    live_path = tmp_path / "live"
    candidate_path = live_path / "candidate.bin"
    live_path.mkdir()
    candidate_path.write_bytes(b"m171-existing-participant")
    _require_ntfs(tmp_path)

    participant = _start_existing_participant(tmp_path)
    try:
        assert _read_ready(participant) == "ready"
        assert participant.poll() is None

        denied_probe = _ExclusiveDirectoryProbe()
        with denied_probe:
            with pytest.raises(
                _NativeFailure,
                match=r"CreateFileW\(exclusive directory\) failed with native code 32",
            ) as raised:
                denied_probe.open_directory_exclusive(live_path)
            assert raised.value.code == _ERROR_SHARING_VIOLATION
            assert denied_probe.owned_count == 0
            assert participant.poll() is None
            assert candidate_path.read_bytes() == b"m171-existing-participant"

        assert _release_and_read_closed(participant) == "closed"
        assert participant.returncode == 0

        acquired_probe = _ExclusiveDirectoryProbe()
        with acquired_probe:
            exclusive = acquired_probe.open_directory_exclusive(live_path)
            assert os.get_handle_inheritable(exclusive) is False
            assert acquired_probe.owned_count == 1
            acquired_probe.release(exclusive)
            assert acquired_probe.owned_count == 0
    finally:
        _close_child(participant)

    assert participant.returncode == 0
    assert candidate_path.read_bytes() == b"m171-existing-participant"
