"""Protect the explicit, bounded, read-only M124 source-manifest boundary."""

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
    "scripts/smoke_prefab_file_wheel.py": "5548f6c5cd34f56b42523bcc2739938da375df816f3d9afff126a7e30d86be76",
    "scripts/smoke_source_check_wheel.py": "a5c0a76361e354e0b0a036ac311a25177839e2e1b07812972e11636c2548efa9",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m124_retains_workflows_metadata_root_and_prior_source_contracts() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_m124_narrows_only_the_obsolete_m123_headless_project_hash() -> None:
    source = (_ROOT / "tests/architecture/test_m123_read_only_source_check_boundary.py").read_text(
        encoding="utf-8"
    )
    assert '"src/ludoweave/tools/headless_project.py"' not in source
    assert '".github/workflows/ci.yml"' in source
    assert '"pyproject.toml"' in source
    assert '"src/ludoweave/scene/document.py"' in source
    assert "test_source_check_is_one_bounded_cli_composition_surface" in source
    assert "test_source_check_has_no_compile_mutation_discovery_or_write_capability" in source


def test_source_manifest_is_one_focused_immutable_scene_contract() -> None:
    scene_root = _ROOT / "src/ludoweave/scene"
    assert {path.name for path in scene_root.glob("*.py")} >= {
        "__init__.py",
        "document.py",
        "errors.py",
        "planning.py",
        "prefab.py",
        "sources.py",
    }
    path = _ROOT / "src/ludoweave/scene/sources.py"
    assert path.is_file()
    source = path.read_text(encoding="utf-8")
    assert 'SOURCE_MANIFEST_PROTOCOL = "ludoweave.source-manifest/1"' in source
    assert "class SourceManifestLimits:" in source
    assert "class SourceManifestEntry:" in source
    assert "class SourceManifest:" in source
    assert "@dataclass(frozen=True, slots=True)" in source


def test_headless_project_loads_one_confined_bounded_manifest() -> None:
    source = (_ROOT / "src/ludoweave/tools/headless_project.py").read_text(encoding="utf-8")
    assert "def load_source_manifest(" in source
    assert 'role="source_manifest"' in source
    assert "SourceManifest.from_json(" in source


def test_source_check_accepts_only_one_explicit_manifest_file() -> None:
    source = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    start = source.index("def _run_source_check(")
    end = source.index("def _run_apply(")
    implementation = source[start:end].casefold()
    assert 'source_mode.add_argument("--manifest"' in source
    assert "project.load_source_manifest(" in implementation
    assert "ludoweave.cli.source-manifest-check/1" in implementation
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


def test_source_manifest_has_behavior_and_installed_wheel_evidence() -> None:
    assert (_ROOT / "tests/unit/test_source_manifest.py").is_file()
    assert (_ROOT / "tests/integration/test_source_manifest_check_cli.py").is_file()
    assert (_ROOT / "scripts/smoke_source_manifest_check_wheel.py").is_file()


def test_m124_docs_define_explicit_read_only_manifest_checking() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/cli-workflows.md",
        _ROOT / "docs/rfcs/0107-add-explicit-source-manifest-checking.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    folded = combined.casefold()
    assert "M124" in combined
    assert "ludoweave.source-manifest/1" in combined
    assert "ludoweave.cli.source-manifest-check/1" in combined
    assert "explicit manifest" in folded
    assert "no directory discovery" in folded
    assert "no compile" in folded
    assert "no world mutation" in folded
    assert "no receipt" in folded
    assert "no workflow allocation" in folded
