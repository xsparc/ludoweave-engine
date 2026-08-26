"""Protect additive, read-only M134 cache-assisted asset realization."""

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
    "src/ludoweave/assets/cache.py": "bc0c253a46bd81735e15d5ba899d7e3b7cdcd7ecedde5b726f6c27dab410699f",
    "src/ludoweave/assets/execution.py": "251e48b1200e82e1fa9809b562f782ccb26ca6e30152e449b34cd1b25bfbf1ac",
    "src/ludoweave/assets/pipeline.py": "a5439fecef0e352c3e19bb6e73246f897ee12f9d2e53574a24da0874b7062e08",
    "src/ludoweave/assets/locks.py": "85c6acd3ce416e175e1af4acf84ffdab70a55d077073705e21498caa6a392154",
    "src/ludoweave/assets/plans.py": "a56c1b335228a5bfcef77792d5a0436960e356b12df3fbb274b0c3fc04623a16",
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
    "scripts/smoke_asset_cache_lookup_wheel.py": "72b68b8236cb8ed92c1a9f61f2341267c1afc19e40dca1b6428b1d283a711eaf",
    "docs/rfcs/0116-add-verified-read-only-asset-cache-lookup.md": "b91ba54ce358b0c89ee87444fae5d345b60fc581e3e6bc98ab9d89e9a7a450ea",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m134_retains_ci_dependencies_prior_cache_contracts_and_execution() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_realization_preflights_then_reads_all_candidates_before_decoding() -> None:
    source = (_ROOT / "src/ludoweave/assets/realization.py").read_text(encoding="utf-8")
    block = source.split("def realize_asset_build_plan(", 1)[1].split("\ndef ", 1)[0]
    assert block.index("_preflight_inputs") < block.index("cache.load_action")
    assert block.index("cache.load_action") < block.index("_decode_artifact")
    assert "writable" not in block
    for forbidden in (
        ".publish(",
        "write_bytes",
        "write_text",
        "mkdir",
        "unlink",
        "rmtree",
        "os.replace",
        "subprocess",
        "requests",
        "urllib",
        "socket",
        "thread",
        "asyncio",
        "multiprocessing",
        "wgpu",
        "glfw",
        "numpy",
    ):
        assert forbidden not in source.casefold()


def test_cli_verifies_and_acquires_before_read_only_realization() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-realize"' in cli
    block = cli.split("def _run_asset_realize(", 1)[1].split("\ndef ", 1)[0]
    assert block.index("expected_lock.verify(current_lock)") < block.index(
        "expected_plan.verify(current_plan)"
    )
    assert block.index("expected_plan.verify(current_plan)") < block.index(
        "_acquire_asset_build_inputs"
    )
    assert block.index("_acquire_asset_build_inputs") < block.index("AssetCacheStore")
    assert block.index("AssetCacheStore") < block.index("realize_asset_build_plan")
    assert "writable=False" in block
    assert "publish(" not in block


def test_m134_has_behavior_installed_and_documentation_evidence() -> None:
    for path in (
        "tests/unit/test_asset_realization.py",
        "tests/integration/test_asset_cache_cli.py",
        "scripts/smoke_asset_realization_wheel.py",
        "docs/rfcs/0117-add-read-only-cache-assisted-asset-realization.md",
    ):
        assert (_ROOT / path).is_file()
    combined = "\n".join(
        (_ROOT / path).read_text(encoding="utf-8")
        for path in (
            "README.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "docs/architecture.md",
            "docs/rfcs/0117-add-read-only-cache-assisted-asset-realization.md",
        )
    ).casefold()
    assert "m134" in combined
    assert "ludoweave.asset-build-realization/1" in combined
    assert "read-only" in combined
    assert "no automatic cache publication" in combined
    assert "no ci change" in combined
