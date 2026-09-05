"""Protect pure deterministic M129 asset build planning."""

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
    "src/ludoweave/assets/locks.py": "85c6acd3ce416e175e1af4acf84ffdab70a55d077073705e21498caa6a392154",
    "src/ludoweave/scene/locks.py": "ff003999ab34bdc06721b5784df9046cda6b54db4b0e28776ccdf2e6d86e0799",
    "src/ludoweave/scene/sources.py": "1a5075fc0711330d7407537ba5f85ca15d2fc5d6e9bab733f954416420b30303",
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
    "scripts/smoke_asset_source_lock_wheel.py": "0586b64c8676aacbd8ec516fbcef7d3feface8a238116d0f0a6604f179988ae7",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m129_retains_workflows_metadata_root_locks_source_and_m128_boundaries() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_assets_expose_bounded_pure_asset_build_plan_contract() -> None:
    plan = (_ROOT / "src/ludoweave/assets/plans.py").read_text(encoding="utf-8")
    pipeline = (_ROOT / "src/ludoweave/assets/pipeline.py").read_text(encoding="utf-8")
    exports = (_ROOT / "src/ludoweave/assets/__init__.py").read_text(encoding="utf-8")
    assert 'ASSET_BUILD_PLAN_PROTOCOL = "ludoweave.asset-build-plan/1"' in plan
    assert "class AssetBuildPlanLimits:" in plan
    assert "class AssetBuildPlanEntry:" in plan
    assert "class AssetBuildPlan:" in plan
    assert "def from_inputs(" in plan
    assert 'ASSET_LOADER_PROTOCOL = "ludoweave.assets/1"' in pipeline
    assert "AssetBuildPlan" in exports


def test_cli_composes_verified_asset_plan_without_build_or_cache() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-plan"' in cli
    assert "def _run_asset_build_plan(" in cli
    assert "expected.verify(current)" in cli
    block = cli.split("def _run_asset_build_plan(", 1)[1].split("\ndef ", 1)[0]
    assert "AssetPipeline" not in block
    assert ".build(" not in block


def test_asset_build_plan_has_behavior_and_installed_evidence() -> None:
    assert (_ROOT / "tests/unit/test_asset_build_plan.py").is_file()
    assert (_ROOT / "tests/integration/test_asset_build_plan_cli.py").is_file()
    assert (_ROOT / "scripts/smoke_asset_build_plan_wheel.py").is_file()


def test_m129_docs_define_plan_only_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/api-status.md",
        _ROOT / "docs/rfcs/0112-add-deterministic-asset-build-planning.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    folded = combined.casefold()
    assert "M129" in combined
    assert "ludoweave.asset-build-plan/1" in combined
    assert "dependency-first" in folded
    assert "no asset build" in folded
    assert "no cache read" in folded
    assert "no cache write" in folded
    assert "no workflow allocation" in folded
