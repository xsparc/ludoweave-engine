"""Protect the verified local-only M132 asset cache boundary."""

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
    "scripts/smoke_asset_plan_execution_wheel.py": "ce466577f618a20aebc3cf129ca19abc644f85e2317df5d3310b00a945843731",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m132_retains_workflows_metadata_root_legacy_pipeline_and_m131_smoke() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_cache_contract_is_atomic_verified_local_and_backend_free() -> None:
    source = (_ROOT / "src/ludoweave/assets/cache.py").read_text(encoding="utf-8")
    for name in (
        "ASSET_CACHE_ENTRY_PROTOCOL",
        "ASSET_CACHE_PUBLISH_PROTOCOL",
        "AssetCacheStore",
        "AssetCachePublishSummary",
    ):
        assert name in source
    assert "os.replace" in source
    assert "tempfile.mkdtemp" in source
    assert "fsync" in source
    assert "asset_cache.corrupt_entry" in source
    assert "asset_cache.publish_failed" in source
    folded = source.casefold()
    for banned in (
        "requests",
        "urllib",
        "socket",
        "subprocess",
        "thread",
        "asyncio",
        "multiprocessing",
        "wgpu",
        "glfw",
        "numpy",
    ):
        assert banned not in folded


def test_cli_verifies_and_materializes_before_explicit_cache_publication() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-cache"' in cli
    block = cli.split("def _run_asset_cache_publish(", 1)[1].split("\ndef ", 1)[0]
    assert block.index("expected_lock.verify(current_lock)") < block.index(
        "expected_plan.verify(current_plan)"
    )
    assert block.index("expected_plan.verify(current_plan)") < block.index(
        "materialize_asset_build_plan"
    )
    assert block.index("materialize_asset_build_plan") < block.index("AssetCacheStore")
    assert block.index("AssetCacheStore") < block.index("publish(")


def test_m132_has_behavior_installed_and_documentation_evidence() -> None:
    for path in (
        "tests/unit/test_asset_cache.py",
        "tests/integration/test_asset_cache_cli.py",
        "scripts/smoke_asset_cache_wheel.py",
        "docs/rfcs/0115-add-verified-local-asset-cache-publication.md",
    ):
        assert (_ROOT / path).is_file()
    combined = "\n".join(
        (_ROOT / path).read_text(encoding="utf-8")
        for path in (
            "README.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "docs/architecture.md",
            "docs/rfcs/0115-add-verified-local-asset-cache-publication.md",
        )
    ).casefold()
    assert "m132" in combined
    assert "ludoweave.asset-cache-entry/1" in combined
    assert "atomic per-entry" in combined
    assert "no remote cache" in combined
    assert "no ci change" in combined
