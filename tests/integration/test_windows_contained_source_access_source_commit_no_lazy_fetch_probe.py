"""Regress M222's dual exclusion of lazy Git object fetching."""

from __future__ import annotations

import os
import subprocess
import sys
from typing import cast
from unittest.mock import patch

import pytest

from tests.integration import (
    test_windows_contained_source_access_source_commit_binding_probe as _commit_module,
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M222 verifies the Windows source-commit reader's no-lazy-fetch boundary",
)


def test_no_lazy_fetch_exclusion_preserves_m221_boundary() -> None:
    _commit_module.test_committed_source_binding_preserves_m220_boundary()  # pyright: ignore[reportPrivateUsage]


def test_git_reader_passes_dual_no_lazy_fetch_exclusion() -> None:
    observed: dict[str, object] = {}

    def _fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[bytes]:
        observed["args"] = args
        observed["kwargs"] = kwargs
        command = cast(tuple[str, ...], args[0])
        return subprocess.CompletedProcess(command, 0, stdout=b"commit\n", stderr=b"")

    with patch.object(_commit_module.subprocess, "run", side_effect=_fake_run):
        result = _commit_module._run_git("cat-file", "-t", "fixed-object")  # pyright: ignore[reportPrivateUsage]

    assert result == b"commit\n"
    args = cast(tuple[object, ...], observed["args"])
    kwargs = cast(dict[str, object], observed["kwargs"])
    command = cast(tuple[str, ...], args[0])
    assert command.count("--no-lazy-fetch") == 1
    assert command.index("--no-replace-objects") < command.index("--no-lazy-fetch")
    assert command.index("--no-lazy-fetch") < command.index("-C")
    environment = cast(dict[str, str], kwargs["env"])
    assert environment["GIT_NO_LAZY_FETCH"] == "1"
    assert kwargs["stdin"] is subprocess.DEVNULL
    assert kwargs["stdout"] == subprocess.PIPE
    assert kwargs["stderr"] == subprocess.PIPE
    assert kwargs["shell"] is False
    assert kwargs["check"] is False
    assert kwargs["timeout"] == 10.0
    assert kwargs["creationflags"] == 0x08000000


def test_git_environment_rejects_ambient_lazy_fetch_override() -> None:
    ambient = {
        "GIT_NO_LAZY_FETCH": "0",
        "GIT_OBJECT_DIRECTORY": "ambient-object-directory",
        "LUDOWEAVE_M222_SENTINEL": "preserved",
    }
    with patch.dict(os.environ, ambient, clear=True):
        environment = _commit_module._git_environment()  # pyright: ignore[reportPrivateUsage]

    assert environment["GIT_NO_LAZY_FETCH"] == "1"
    assert "GIT_OBJECT_DIRECTORY" not in environment
    assert environment["LUDOWEAVE_M222_SENTINEL"] == "preserved"
