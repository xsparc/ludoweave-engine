"""Test-only Windows native sharing-violation probe for M154.

One fixed isolated child calls ``MoveFileExW`` beneath pytest-owned temporary
storage and returns only a bounded structured native result.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import pytest
from test_windows_cache_cleanup_junction_probe import (
    _filesystem_information,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_share_delete_probe import (
    _ShareDeleteProbe,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M154 probes a direct Windows native sharing-violation result",
)

_CHILD = Path(__file__).parents[1] / "fixtures/windows_share_delete_rename_child.py"
_SCHEMA = "ludoweave.test.windows-native-rename/1"
_ERROR_SHARING_VIOLATION = 32
_MAX_CHILD_OUTPUT_BYTES = 512


@dataclass(frozen=True, slots=True)
class _NativeRenameResult:
    succeeded: bool
    error_code: int


def _attempt_native_child_rename(working_directory: Path) -> _NativeRenameResult:
    completed = subprocess.run(
        (sys.executable, "-I", "-B", str(_CHILD)),
        check=False,
        capture_output=True,
        close_fds=True,
        cwd=working_directory,
        shell=False,
        stdin=subprocess.DEVNULL,
        timeout=15.0,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"native rename child exited with code {completed.returncode}") from None
    if completed.stderr or len(completed.stdout) > _MAX_CHILD_OUTPUT_BYTES:
        raise RuntimeError("native rename child returned invalid structured output") from None
    try:
        payload: object = json.loads(completed.stdout)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RuntimeError("native rename child returned invalid structured output") from None
    if not isinstance(payload, dict):
        raise RuntimeError("native rename child returned invalid structured output") from None
    document = cast(dict[object, object], payload)
    if set(document) != {"error_code", "schema", "succeeded"}:
        raise RuntimeError("native rename child returned invalid structured output") from None
    succeeded = document["succeeded"]
    error_code = document["error_code"]
    if (
        document["schema"] != _SCHEMA
        or type(succeeded) is not bool
        or type(error_code) is not int
        or error_code < 0
    ):
        raise RuntimeError("native rename child returned invalid structured output") from None
    return _NativeRenameResult(succeeded=succeeded, error_code=error_code)


def test_native_child_reports_sharing_violation_until_handle_close(tmp_path: Path) -> None:
    live_path = tmp_path / "live"
    displaced_path = tmp_path / "displaced"
    candidate_path = live_path / "candidate.bin"
    displaced_candidate = displaced_path / "candidate.bin"
    live_path.mkdir()
    candidate_path.write_bytes(b"m154-native-sharing-violation")

    probe = _ShareDeleteProbe()
    with probe:
        root = probe.open_root(tmp_path)
        filesystem_name, _ = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M154 native-error fixture requires an NTFS pytest volume")

        blocker = probe.open_directory_without_delete_sharing(live_path)
        try:
            denied = _attempt_native_child_rename(tmp_path)

            assert denied == _NativeRenameResult(
                succeeded=False,
                error_code=_ERROR_SHARING_VIOLATION,
            )
            assert live_path.is_dir()
            assert not os.path.isjunction(live_path)
            assert not os.path.lexists(displaced_path)
            assert candidate_path.read_bytes() == b"m154-native-sharing-violation"
            assert probe.owned_count == 2
        finally:
            probe.release(blocker)

        assert probe.owned_count == 1
        assert _attempt_native_child_rename(tmp_path) == _NativeRenameResult(
            succeeded=True,
            error_code=0,
        )
        assert not os.path.lexists(live_path)
        assert displaced_path.is_dir()
        assert not os.path.isjunction(displaced_path)
        assert displaced_candidate.read_bytes() == b"m154-native-sharing-violation"

    assert probe.owned_count == 0
    assert displaced_candidate.read_bytes() == b"m154-native-sharing-violation"
