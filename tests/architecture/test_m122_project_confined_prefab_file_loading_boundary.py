"""Protect the explicit M122 project-confined prefab-file loading boundary."""

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
    "src/ludoweave/scene/document.py": "28ff581ab61eb84116675526bd8f2dfedbcc990dec0d09de4b03774d1c9a8b81",
    "src/ludoweave/scene/planning.py": "a47fbbd14f7583bf3bdb9284c3dc902d46e541fb8640dd569b60ff6e526b0716",
    "src/ludoweave/scene/prefab.py": "19fff5db607e808be41d5453668c8976fb79de0a7ca0614f901f440bb7e294a3",
    "scripts/smoke_scene_file_wheel.py": "3f2abfcafb277c8b0432c9522c86e7efb5ccfb5fcf96c6bcb5dda0c4b5927b5d",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m122_retains_workflow_metadata_scene_and_scene_file_surfaces() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_prefab_file_loading_extends_only_the_existing_tools_composition_root() -> None:
    source = (_ROOT / "src/ludoweave/tools/headless_project.py").read_text(encoding="utf-8")
    assert "def load_prefab(" in source
    assert "def load_prefab_instance(" in source
    assert (_ROOT / "tests/unit/test_prefab_file_loading.py").is_file()
    assert (_ROOT / "scripts/smoke_prefab_file_wheel.py").is_file()


def test_prefab_file_loads_have_no_discovery_cache_or_mutation_capability() -> None:
    source = (_ROOT / "src/ludoweave/tools/headless_project.py").read_text(encoding="utf-8")
    start = source.index("    def load_prefab(")
    end = source.index("    def write_relative(")
    methods = source[start:end].casefold()
    for forbidden in (
        "iterdir",
        "glob",
        "walk",
        "importlib",
        "subprocess",
        "socket",
        "urllib",
        "requests",
        "watchdog",
        "write",
        "unlink",
        "replace",
        "eval(",
        "exec(",
    ):
        assert forbidden not in methods


def test_m122_docs_define_two_explicit_files_and_no_implicit_pairing() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/commands.md",
        _ROOT / "docs/rfcs/0105-add-project-confined-prefab-file-loading.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    folded = combined.casefold()
    assert "M122" in combined
    assert "project-confined prefab file" in folded
    assert "ludoweave.prefab/1" in combined
    assert "ludoweave.prefab-instance/1" in combined
    assert "two explicit files" in folded
    assert "no implicit pairing" in folded
    assert "no directory discovery" in folded
    assert "no cache" in folded
    assert "no live update" in folded
    assert "no world mutation" in folded
    assert "no workflow" in folded
    assert "https://docs.godotengine.org/en/stable/classes/class_resourceloader.html" in combined
