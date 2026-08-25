"""Protect bounded one-level M120 prefab fragment transaction planning."""

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
    "src/ludoweave/world/command_schema.py": "8f0e2f0d835a71e0e44a8fe2083c347c6a86b7f3dde4616b23d5ace8d0922317",
    "src/ludoweave/world/operations.py": "a979bf2e3e7d485b3e1b9dd1d1e71233e3adbf62de0729f12c71cd8bf7465ece",
    "src/ludoweave/world/transaction.py": "a8311704313101b53fd3bbbd77bdfba41dfc08aff9397fb4015a6d025c409cbc",
    "scripts/smoke_scene_wheel.py": "b5a01d5339d8f6830395b227c3f59d15a5623e933c1beb1cb049308521597d41",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m120_retains_protected_protocol_workflow_and_metadata_surfaces() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_prefab_is_an_exercised_scene_submodule() -> None:
    scene_root = _ROOT / "src/ludoweave/scene"
    assert {path.name for path in scene_root.glob("*.py")} == {
        "__init__.py",
        "document.py",
        "errors.py",
        "planning.py",
        "prefab.py",
    }
    assert (_ROOT / "tests/unit/test_prefab_documents.py").is_file()
    assert (_ROOT / "tests/integration/test_prefab_transactions.py").is_file()
    assert (_ROOT / "scripts/smoke_prefab_wheel.py").is_file()


def test_prefab_source_is_backend_neutral_and_has_no_ambient_loading() -> None:
    source = (_ROOT / "src/ludoweave/scene/prefab.py").read_text(encoding="utf-8")
    folded = source.casefold()
    for forbidden in (
        "ludoweave.render",
        "ludoweave.tools",
        "wgpu",
        "glfw",
        "numpy",
        "importlib",
        "pathlib",
        "subprocess",
        "open(",
        "eval(",
        "exec(",
    ):
        assert forbidden not in folded


def test_m120_docs_define_one_level_override_and_receipt_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/commands.md",
        _ROOT / "docs/rfcs/0103-add-one-level-prefab-fragment-planning.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    folded = combined.casefold()
    assert "M120" in combined
    assert "ludoweave.prefab/1" in combined
    assert "ludoweave.prefab-instance/1" in combined
    assert "schema-aware" in folded
    assert "ordinary entity.spawn commands" in folded
    assert "receipt aliases" in folded
    assert "one-level" in folded
    assert "no nested prefab inheritance" in folded
    assert "no live update" in folded
    assert "no file i/o" in folded
    assert "no new persistent operation" in folded
    assert "no workflow" in folded
    assert "https://datatracker.ietf.org/doc/html/rfc6902" in combined
    assert "https://datatracker.ietf.org/doc/html/rfc6901" in combined
