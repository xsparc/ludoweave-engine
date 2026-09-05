"""Protect the bounded, read-only M125 source-lock verification boundary."""

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
    "src/ludoweave/scene/sources.py": "1a5075fc0711330d7407537ba5f85ca15d2fc5d6e9bab733f954416420b30303",
    "scripts/smoke_source_manifest_check_wheel.py": "420752c11dd8050a1d74d1c769f1003841b55b34c50cd1acafdf12b799e6672b",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m125_retains_workflows_metadata_root_and_m124_source_contract() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_source_lock_is_one_focused_immutable_scene_contract() -> None:
    scene_root = _ROOT / "src/ludoweave/scene"
    assert {path.name for path in scene_root.glob("*.py")} == {
        "__init__.py",
        "document.py",
        "errors.py",
        "locks.py",
        "planning.py",
        "prefab.py",
        "sources.py",
    }
    source = (_ROOT / "src/ludoweave/scene/locks.py").read_text(encoding="utf-8")
    assert 'SOURCE_LOCK_PROTOCOL = "ludoweave.source-lock/1"' in source
    assert "class SourceLockLimits:" in source
    assert "class SourceLockEntry:" in source
    assert "class SourceLock:" in source
    assert "def verify(" in source
    assert "@dataclass(frozen=True, slots=True)" in source


def test_headless_project_loads_one_confined_bounded_source_lock() -> None:
    source = (_ROOT / "src/ludoweave/tools/headless_project.py").read_text(encoding="utf-8")
    assert "def load_source_lock(" in source
    assert 'role="source_lock"' in source
    assert "SourceLock.from_json(" in source


def test_source_lock_cli_is_read_only_and_has_no_import_pipeline() -> None:
    source = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    start = source.index("def _run_source_lock(")
    end = source.index("def _run_apply(")
    implementation = source[start:end].casefold()
    assert '"lock"' in source
    assert '"verify"' in source
    assert "ludoweave.cli.source-lock-verify/1" in implementation
    for forbidden in (
        "compile_scene",
        "compile_prefab",
        "new_session",
        "transactionservice",
        "write_relative",
        "receipt",
        "iterdir",
        "glob",
        "walk",
        "importlib",
        "subprocess",
        "socket",
        "urllib",
        "requests",
        "watchdog",
        "eval(",
        "exec(",
    ):
        assert forbidden not in implementation


def test_source_lock_has_behavior_and_installed_wheel_evidence() -> None:
    assert (_ROOT / "tests/unit/test_source_lock.py").is_file()
    assert (_ROOT / "tests/integration/test_source_lock_cli.py").is_file()
    assert (_ROOT / "scripts/smoke_source_lock_wheel.py").is_file()


def test_m125_docs_define_integrity_not_import_or_snapshot_semantics() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/cli-workflows.md",
        _ROOT / "docs/rfcs/0108-add-source-integrity-lock-verification.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    folded = combined.casefold()
    assert "M125" in combined
    assert "ludoweave.source-lock/1" in combined
    assert "ludoweave.cli.source-lock-verify/1" in combined
    assert "content identity" in folded
    assert "not an atomic filesystem snapshot" in folded
    assert "no import" in folded
    assert "no cache" in folded
    assert "no world mutation" in folded
    assert "no workflow allocation" in folded
