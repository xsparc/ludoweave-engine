"""Bind M222 fixed Git reads to one executable selection per observation."""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import cast
from unittest.mock import patch

import pytest

from tests.integration import (
    test_windows_contained_source_access_source_commit_binding_probe as _commit_module,
)
from tests.integration import (
    test_windows_contained_source_access_source_commit_no_lazy_fetch_probe as _no_lazy_fetch_module,
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M223 binds one Git executable selection across the Windows M222 boundary",
)

_EXPECTED_GIT_READS = 48


def _require_git_selection_bound_m222_boundary() -> None:
    git_executable = _commit_module._git_executable()  # pyright: ignore[reportPrivateUsage]
    if not git_executable.is_absolute() or not git_executable.is_file():
        raise RuntimeError("selected Git executable was not an absolute file") from None

    original_run = cast(
        Callable[..., subprocess.CompletedProcess[bytes]],
        subprocess.run,
    )
    commands: list[tuple[str, ...]] = []

    def _record_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[bytes]:
        command = cast(tuple[str, ...], args[0])
        commands.append(command)
        return original_run(*args, **kwargs)

    with (
        patch.object(
            _commit_module,
            "_git_executable",
            return_value=git_executable,
        ) as selection,
        patch.object(
            _commit_module.subprocess,
            "run",
            side_effect=_record_run,
        ),
    ):
        _no_lazy_fetch_module.test_no_lazy_fetch_exclusion_preserves_m221_boundary()

    assert selection.call_count == _EXPECTED_GIT_READS
    assert len(commands) == _EXPECTED_GIT_READS
    assert all(Path(command[0]) == git_executable for command in commands)


def test_git_selection_binding_preserves_m222_boundary() -> None:
    real_which = _commit_module.shutil.which

    with patch.object(
        _commit_module.shutil,
        "which",
        side_effect=real_which,
    ) as lookup:
        _require_git_selection_bound_m222_boundary()

    assert lookup.call_count == 1
