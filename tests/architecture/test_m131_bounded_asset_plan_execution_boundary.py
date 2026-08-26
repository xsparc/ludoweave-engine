"""Protect bounded cache-free M131 asset build-plan execution."""

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
    "src/ludoweave/assets/plans.py": "a56c1b335228a5bfcef77792d5a0436960e356b12df3fbb274b0c3fc04623a16",
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
    "scripts/smoke_asset_build_plan_verify_wheel.py": "0686b0569db8277d215f8bdcd33cf184302e87f8872f0d0822feea2c0564e5da",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m131_retains_workflows_metadata_root_pipeline_locks_plans_and_m130_smoke() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_execution_contract_is_focused_bounded_and_cache_free() -> None:
    source = (_ROOT / "src/ludoweave/assets/execution.py").read_text(encoding="utf-8")
    package = (_ROOT / "src/ludoweave/assets/__init__.py").read_text(encoding="utf-8")
    for name in (
        "ASSET_BUILD_RESULT_PROTOCOL",
        "AssetBuildExecutionLimits",
        "AssetBuildInput",
        "AssetBuildResultEntry",
        "AssetBuildResult",
        "execute_asset_build_plan",
    ):
        assert name in source
        assert f'"{name}"' in package
    folded = source.casefold()
    assert "asset_build.limit_exceeded" in source
    assert "asset_build.input_mismatch" in source
    assert "asset_build.decode_failed" in source
    assert "assetpipeline" not in folded
    assert "cache_root" not in folded
    assert "mkdir(" not in source
    assert "write_bytes(" not in source
    assert "os.replace" not in source
    assert "subprocess" not in folded
    assert "thread" not in folded


def test_cli_executes_only_after_current_lock_and_saved_plan_verification() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-build"' in cli
    assert "def _run_asset_build_plan_execute(" in cli
    block = cli.split("def _run_asset_build_plan_execute(", 1)[1].split("\ndef ", 1)[0]
    assert "expected_lock.verify(current_lock)" in block
    assert "expected_plan.verify(current_plan)" in block
    assert "execute_asset_build_plan" in block
    assert "AssetPipeline" not in block
    assert ".build(" not in block
    assert "cache" not in block.casefold()


def test_asset_plan_execution_has_behavior_and_installed_evidence() -> None:
    assert (_ROOT / "tests/unit/test_asset_plan_execution.py").is_file()
    assert (_ROOT / "tests/integration/test_asset_plan_execution_cli.py").is_file()
    assert (_ROOT / "scripts/smoke_asset_plan_execution_wheel.py").is_file()


def test_m131_docs_define_in_memory_execution_only_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/api-status.md",
        _ROOT / "docs/rfcs/0114-add-bounded-in-memory-asset-plan-execution.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    folded = combined.casefold()
    assert "M131" in combined
    assert "ludoweave.asset-build-result/1" in combined
    assert "built-in decoder" in folded
    assert "no cache read" in folded
    assert "no cache write" in folded
    assert "no project write" in folded
    assert "no workflow allocation" in folded
