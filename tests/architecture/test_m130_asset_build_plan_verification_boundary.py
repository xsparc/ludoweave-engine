"""Protect read-only confined M130 asset build-plan verification."""

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
    "src/ludoweave/assets/pipeline.py": "a5439fecef0e352c3e19bb6e73246f897ee12f9d2e53574a24da0874b7062e08",
    "src/ludoweave/assets/locks.py": "85c6acd3ce416e175e1af4acf84ffdab70a55d077073705e21498caa6a392154",
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
    "scripts/smoke_asset_build_plan_wheel.py": "e5cf5c5bbf818ff744ac06bb4fc6804975063434e0cdb14a6fdd9a75a32dfc67",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m130_retains_workflows_metadata_root_pipeline_lock_and_m129_smoke() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_plan_contract_supports_content_silent_exact_verification() -> None:
    source = (_ROOT / "src/ludoweave/assets/plans.py").read_text(encoding="utf-8")
    assert "def verify(" in source
    assert 'code="asset_build_plan.mismatch"' in source
    assert 'code="asset_build_plan.invalid_verify"' in source


def test_project_loader_and_cli_verify_current_saved_plan_without_execution() -> None:
    project = (_ROOT / "src/ludoweave/tools/headless_project.py").read_text(encoding="utf-8")
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert "def load_asset_build_plan(" in project
    assert 'source_command == "asset-plan-verify"' in cli
    assert "def _run_asset_build_plan_verify(" in cli
    block = cli.split("def _run_asset_build_plan_verify(", 1)[1].split("\ndef ", 1)[0]
    assert "AssetPipeline" not in block
    assert ".build(" not in block


def test_asset_plan_verification_has_behavior_and_installed_evidence() -> None:
    assert (_ROOT / "tests/unit/test_asset_build_plan_verification.py").is_file()
    assert (_ROOT / "tests/integration/test_asset_build_plan_verification_cli.py").is_file()
    assert (_ROOT / "scripts/smoke_asset_build_plan_verify_wheel.py").is_file()


def test_m130_docs_define_verification_only_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/api-status.md",
        _ROOT / "docs/rfcs/0113-add-confined-asset-build-plan-verification.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    folded = combined.casefold()
    assert "M130" in combined
    assert "ludoweave.cli.asset-build-plan-verify/1" in combined
    assert "content-silent" in folded
    assert "no asset build" in folded
    assert "no cache read" in folded
    assert "no cache write" in folded
    assert "no workflow allocation" in folded
