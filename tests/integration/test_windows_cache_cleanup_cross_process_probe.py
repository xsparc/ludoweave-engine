"""Test-only Windows cross-process namespace-substitution probe for M152.

The child command uses fixed relative components beneath pytest-owned temporary
storage. Native handles remain private to the retained M149 parent process.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
from test_windows_cache_cleanup_capability_probe import (
    _UnsafeComponent,  # pyright: ignore[reportPrivateUsage]
    _WindowsCapabilityProbe,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_junction_probe import (
    _FILE_SUPPORTS_REPARSE_POINTS,  # pyright: ignore[reportPrivateUsage]
    _filesystem_information,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M152 probes cross-process Windows directory-handle behavior",
)

_SUBSTITUTION_COMMAND = (
    "cmd.exe",
    "/d",
    "/c",
    "ren live displaced && mklink /j live target",
)


def _substitute_live_name_from_child(working_directory: Path) -> None:
    completed = subprocess.run(
        _SUBSTITUTION_COMMAND,
        check=False,
        capture_output=True,
        close_fds=True,
        cwd=working_directory,
        shell=False,
        timeout=15.0,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"cross-process substitution failed with exit code {completed.returncode}"
        ) from None


def test_retained_parent_survives_cross_process_name_substitution(tmp_path: Path) -> None:
    live_path = tmp_path / "live"
    displaced_path = tmp_path / "displaced"
    target_path = tmp_path / "target"
    junction_path = tmp_path / "live"
    displaced_candidate = displaced_path / "candidate.bin"
    target_candidate = target_path / "candidate.bin"
    live_path.mkdir()
    target_path.mkdir()
    (live_path / "candidate.bin").write_bytes(b"m152-retained-parent")
    target_candidate.write_bytes(b"m152-cross-process-target")

    with _WindowsCapabilityProbe() as probe:
        root = probe.open_root(tmp_path)
        filesystem_name, filesystem_flags = _filesystem_information(root)
        if filesystem_name.casefold() != "ntfs":
            pytest.skip("M152 cross-process fixture requires an NTFS pytest volume")
        assert filesystem_flags & _FILE_SUPPORTS_REPARSE_POINTS

        retained_parent = probe.open_directory(root, "live")
        retained_parent_identity = probe.identity(retained_parent)

        try:
            _substitute_live_name_from_child(tmp_path)
            assert displaced_path.is_dir()
            assert not os.path.isjunction(displaced_path)
            assert os.path.isjunction(junction_path)
            assert probe.identity(retained_parent) == retained_parent_identity

            with pytest.raises(_UnsafeComponent, match="reparse component refused"):
                probe.open_directory(root, "live")

            through_retained_parent = probe.open_file(
                retained_parent,
                "candidate.bin",
                delete_access=False,
            )
            displaced_parent = probe.open_directory(root, "displaced")
            through_displaced_name = probe.open_file(
                displaced_parent,
                "candidate.bin",
                delete_access=False,
            )
            target_parent = probe.open_directory(root, "target")
            through_target = probe.open_file(
                target_parent,
                "candidate.bin",
                delete_access=False,
            )

            assert probe.identity(through_retained_parent) == probe.identity(through_displaced_name)
            assert probe.identity(through_retained_parent) != probe.identity(through_target)
            assert probe.owned_count == 7
            assert displaced_candidate.read_bytes() == b"m152-retained-parent"
            assert target_candidate.read_bytes() == b"m152-cross-process-target"
        finally:
            if os.path.isjunction(junction_path):
                os.rmdir(junction_path)

    assert displaced_candidate.read_bytes() == b"m152-retained-parent"
    assert target_candidate.read_bytes() == b"m152-cross-process-target"
    assert not os.path.lexists(junction_path)
    assert probe.owned_count == 0
