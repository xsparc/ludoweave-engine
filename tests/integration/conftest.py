"""Explicit offline metadata store for the historical Windows Git probe family."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from tests.tools.git_source_fixture import materialize_m220_objects

# M159 already declares a Windows-only marker, but imports the Windows-only
# msvcrt module before pytest can evaluate that marker. Preserve the protected
# probe and its Windows execution; exclude only this file before import on
# unsupported hosts. This is unrelated to missing historical Git objects.
collect_ignore = (
    ["test_windows_cache_cleanup_broken_control_pipe_probe.py"] if sys.platform != "win32" else []
)


@pytest.fixture(scope="session")
def m220_git_object_store(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Own one pinned partial object database for this test session."""

    parent = tmp_path_factory.mktemp("m220-git-metadata")
    return materialize_m220_objects(parent / "objects.git")


@pytest.fixture(autouse=True)
def historical_git_probe_store(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Bind only M221-M235 Git reads; do not mock Git results or native checks."""

    if sys.platform != "win32" or not request.path.name.startswith(
        "test_windows_contained_source_access_source_commit"
    ):
        return
    from tests.integration import test_windows_contained_source_access_source_commit_binding_probe

    store: Path = request.getfixturevalue("m220_git_object_store")
    monkeypatch.setattr(
        test_windows_contained_source_access_source_commit_binding_probe, "_ROOT", store
    )
    # Pytest's default import mode also collects the M221 file under its bare
    # module name. Redirect that instance when selected directly, as well as
    # the package import used by later compositions.
    if request.path.name == "test_windows_contained_source_access_source_commit_binding_probe.py":
        module = sys.modules.get(request.path.stem)
        if module is not None:
            monkeypatch.setattr(module, "_ROOT", store)
