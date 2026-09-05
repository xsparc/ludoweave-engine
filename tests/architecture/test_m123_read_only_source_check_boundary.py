"""Protect the bounded read-only M123 source-check CLI boundary."""

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
    "scripts/smoke_prefab_file_wheel.py": "5548f6c5cd34f56b42523bcc2739938da375df816f3d9afff126a7e30d86be76",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m123_retains_workflow_metadata_and_scene_prefab_contracts() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_m123_narrows_only_the_obsolete_m118_whole_cli_hash() -> None:
    source = (
        _ROOT / "tests/architecture/test_m118_python315_prerelease_compatibility.py"
    ).read_text(encoding="utf-8")
    assert "_CLI_SHA256" not in source
    assert "test_python315_remains_outside_supported_metadata" in source
    assert "test_doctor_retains_the_exact_supported_cpython_boundary" in source
    assert "_PYPROJECT_SHA256" in source
    assert "_DOCTOR_SHA256" in source


def test_source_check_is_one_bounded_cli_composition_surface() -> None:
    source = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'subparsers.add_parser("source"' in source
    assert "source_subparsers.add_parser(" in source
    assert '        "check",' in source
    assert "def _run_source_check(" in source
    assert (_ROOT / "tests/integration/test_source_check_cli.py").is_file()
    assert (_ROOT / "scripts/smoke_source_check_wheel.py").is_file()


def test_source_check_has_no_compile_mutation_discovery_or_write_capability() -> None:
    source = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    start = source.index("def _run_source_check(")
    end = source.index("def _run_apply(")
    implementation = source[start:end].casefold()
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


def test_m123_docs_define_structured_read_only_source_preflight() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/cli-workflows.md",
        _ROOT / "docs/rfcs/0106-add-read-only-source-check-cli.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    folded = combined.casefold()
    assert "M123" in combined
    assert "ludoweave source check" in folded
    assert "ludoweave.cli.source-check/1" in combined
    assert "two explicit files" in folded
    assert "no world mutation" in folded
    assert "no receipt" in folded
    assert "no compile" in folded
    assert "no directory discovery" in folded
    assert "no cache" in folded
    assert "no workflow allocation" in folded
    assert (
        "https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html"
        in combined
    )
