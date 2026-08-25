"""Protect the bounded data-only M119 scene transaction-planning boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github/workflows/ci.yml"
_RELEASE = _ROOT / ".github/workflows/release.yml"
_PYPROJECT = _ROOT / "pyproject.toml"
_LOCK = _ROOT / "uv.lock"
_PACKAGE_ROOT = _ROOT / "src/ludoweave/__init__.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_RELEASE_SHA256 = "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"
_PACKAGE_ROOT_SHA256 = "dc8ac74a439a1e190a976a6a87713612fa27ce3b8218f1c11695f2c52c65970e"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m119_retains_workflow_metadata_lock_and_small_root_api() -> None:
    assert _sha256(_CI) == _CI_SHA256
    assert _sha256(_RELEASE) == _RELEASE_SHA256
    assert _sha256(_PYPROJECT) == _PYPROJECT_SHA256
    assert _sha256(_LOCK) == _LOCK_SHA256
    assert _sha256(_PACKAGE_ROOT) == _PACKAGE_ROOT_SHA256


def test_scene_contract_is_an_exercised_focused_subpackage() -> None:
    expected = {
        "__init__.py",
        "document.py",
        "errors.py",
        "planning.py",
    }
    scene_root = _ROOT / "src/ludoweave/scene"

    assert scene_root.is_dir()
    assert {path.name for path in scene_root.glob("*.py")} == expected
    assert (_ROOT / "tests/unit/test_scene_documents.py").is_file()
    assert (_ROOT / "tests/integration/test_scene_transactions.py").is_file()
    assert (_ROOT / "scripts/smoke_scene_wheel.py").is_file()


def test_scene_dependency_direction_is_explicit_and_backend_neutral() -> None:
    rules = (_ROOT / "tests/architecture/import_rules.py").read_text(encoding="utf-8")
    scene_sources = tuple((_ROOT / "src/ludoweave/scene").glob("*.py"))

    assert '"ludoweave.scene"' in rules
    assert all("ludoweave.render" not in path.read_text(encoding="utf-8") for path in scene_sources)
    assert all("ludoweave.tools" not in path.read_text(encoding="utf-8") for path in scene_sources)
    assert all("wgpu" not in path.read_text(encoding="utf-8").casefold() for path in scene_sources)


def test_m119_docs_bound_scene_transaction_planning() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/commands.md",
        _ROOT / "docs/rfcs/0102-add-data-only-scene-transaction-planning.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    folded = combined.casefold()
    assert "M119" in combined
    assert "versioned data-only scene document" in folded
    assert "ordinary entity.spawn commands" in folded
    assert "receipt aliases" in folded
    assert "canonical runtime state remains in the world store" in folded
    assert "no prefab inheritance" in folded
    assert "no file i/o" in folded
    assert "no workflow" in folded
    assert "https://datatracker.ietf.org/doc/rfc8259/" in combined
    assert "https://json-schema.org/draft/2020-12/json-schema-core" in combined
    assert "https://datatracker.ietf.org/doc/rfc3986/" in combined
