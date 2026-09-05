"""The import-time exclusion covers exactly one already Windows-only probe."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("platform", ["linux", "darwin", "win32"])
def test_platform_collection_excludes_only_unimportable_windows_probe(
    monkeypatch: pytest.MonkeyPatch, platform: str
) -> None:
    configuration = Path(__file__).parents[1] / "integration/conftest.py"
    with monkeypatch.context() as patch:
        patch.setattr(sys, "platform", platform)
        namespace = runpy.run_path(str(configuration))
    assert namespace["collect_ignore"] == (
        [] if platform == "win32" else ["test_windows_cache_cleanup_broken_control_pipe_probe.py"]
    )
