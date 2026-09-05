"""Protect the bounded M121 project-confined scene-file loading boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5",
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
    "src/ludoweave/__init__.py": "dc8ac74a439a1e190a976a6a87713612fa27ce3b8218f1c11695f2c52c65970e",
    "src/ludoweave/scene/document.py": "ed18afa22514a39585b303c7cc4f78a912b4486a86f64a57c797f884d377d9c7",
    "src/ludoweave/scene/planning.py": "a47fbbd14f7583bf3bdb9284c3dc902d46e541fb8640dd569b60ff6e526b0716",
    "src/ludoweave/scene/prefab.py": "114d5884a31595d3e637393c18f1b864a8c1996becbd186624bd1e0b060ae0b0",
    "src/ludoweave/world/command_schema.py": "8f0e2f0d835a71e0e44a8fe2083c347c6a86b7f3dde4616b23d5ace8d0922317",
    "src/ludoweave/world/operations.py": "a979bf2e3e7d485b3e1b9dd1d1e71233e3adbf62de0729f12c71cd8bf7465ece",
    "src/ludoweave/world/transaction.py": "a8311704313101b53fd3bbbd77bdfba41dfc08aff9397fb4015a6d025c409cbc",
    "scripts/smoke_scene_wheel.py": "b5a01d5339d8f6830395b227c3f59d15a5623e933c1beb1cb049308521597d41",
    "scripts/smoke_prefab_wheel.py": "38c5743ddc418f68b4c085a86e0dd0159359197b86a3ab07d79ea891fd51dcde",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m121_retains_protocol_workflow_metadata_and_scene_planning_surfaces() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_scene_file_loading_extends_only_the_existing_tools_composition_root() -> None:
    source = (_ROOT / "src/ludoweave/tools/headless_project.py").read_text(encoding="utf-8")
    assert "def load_scene(" in source
    assert (_ROOT / "tests/unit/test_scene_file_loading.py").is_file()
    assert (_ROOT / "scripts/smoke_scene_file_wheel.py").is_file()


def test_scene_file_loading_has_no_ambient_or_mutating_capability() -> None:
    source = (_ROOT / "src/ludoweave/tools/headless_project.py").read_text(encoding="utf-8")
    folded = source.casefold()
    assert "from ludoweave.scene" in source
    for forbidden in (
        "ludoweave.render",
        "ludoweave.plugins",
        "wgpu",
        "glfw",
        "numpy",
        "importlib",
        "socket",
        "urllib",
        "requests",
        "watchdog",
        "eval(",
        "exec(",
    ):
        assert forbidden not in folded


def test_m121_docs_define_project_confinement_and_detached_loading() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/commands.md",
        _ROOT / "docs/rfcs/0104-add-project-confined-scene-file-loading.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    folded = combined.casefold()
    assert "M121" in combined
    assert "project-confined scene file" in folded
    assert "ludoweave.scene/1" in combined
    assert "detached immutable" in folded
    assert "no world mutation" in folded
    assert "no directory discovery" in folded
    assert "no prefab file" in folded
    assert "no file uri" in folded
    assert "no live update" in folded
    assert "no workflow" in folded
    assert "https://datatracker.ietf.org/doc/html/rfc8089" in combined
    assert "https://docs.python.org/3/library/pathlib.html" in combined
