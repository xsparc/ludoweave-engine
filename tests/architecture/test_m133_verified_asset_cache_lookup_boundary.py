"""Protect read-only current-plan-keyed M133 cache lookup."""

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
    "src/ludoweave/assets/execution.py": "251e48b1200e82e1fa9809b562f782ccb26ca6e30152e449b34cd1b25bfbf1ac",
    "src/ludoweave/assets/pipeline.py": "a5439fecef0e352c3e19bb6e73246f897ee12f9d2e53574a24da0874b7062e08",
    "src/ludoweave/assets/locks.py": "85c6acd3ce416e175e1af4acf84ffdab70a55d077073705e21498caa6a392154",
    "src/ludoweave/assets/plans.py": "a56c1b335228a5bfcef77792d5a0436960e356b12df3fbb274b0c3fc04623a16",
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
    "scripts/smoke_asset_cache_wheel.py": "52f72c1fa6747f0f0ba3f9c77fdedc0c8e26c9f6b4e4441a56247023b69a7a78",
    "docs/rfcs/0115-add-verified-local-asset-cache-publication.md": "5c5d2d985ef9c08669df9f72b8b4cdca498072a7d239c98f5c1ff02da936e162",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m133_retains_ci_metadata_execution_publication_and_m132_evidence() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_lookup_contract_is_bounded_strict_and_separate_from_write_authority() -> None:
    source = (_ROOT / "src/ludoweave/assets/cache.py").read_text(encoding="utf-8")
    for name in (
        "ASSET_CACHE_LOOKUP_PROTOCOL",
        "AssetCacheLookupEntry",
        "AssetCacheLookupSummary",
        "load_action",
        "inspect",
        "object_pairs_hook",
        "_METADATA_MAX_BYTES",
        "asset_cache.read_only",
    ):
        assert name in source
    inspect_block = source.split("    def inspect(", 1)[1].split("\n    def ", 1)[0]
    for forbidden in ("publish(", "os.replace", "mkdir", "unlink", "rmtree"):
        assert forbidden not in inspect_block


def test_cli_revalidates_current_plan_before_read_only_cache_inspection() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-cache-check"' in cli
    block = cli.split("def _run_asset_cache_check(", 1)[1].split("\ndef ", 1)[0]
    assert block.index("expected_lock.verify(current_lock)") < block.index(
        "expected_plan.verify(current_plan)"
    )
    assert block.index("expected_plan.verify(current_plan)") < block.index("AssetCacheStore")
    assert "writable=False" in block
    assert block.index("AssetCacheStore") < block.index("inspect(")
    for forbidden in ("_acquire_asset_build_inputs", "materialize", "publish("):
        assert forbidden not in block


def test_m133_has_behavior_installed_and_documentation_evidence() -> None:
    for path in (
        "tests/unit/test_asset_cache.py",
        "tests/integration/test_asset_cache_cli.py",
        "scripts/smoke_asset_cache_lookup_wheel.py",
        "docs/rfcs/0116-add-verified-read-only-asset-cache-lookup.md",
    ):
        assert (_ROOT / path).is_file()
    combined = "\n".join(
        (_ROOT / path).read_text(encoding="utf-8")
        for path in (
            "README.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "docs/architecture.md",
            "docs/rfcs/0116-add-verified-read-only-asset-cache-lookup.md",
        )
    ).casefold()
    assert "m133" in combined
    assert "ludoweave.asset-cache-lookup/1" in combined
    assert "read-only" in combined
    assert "no cache-assisted execution" in combined
    assert "no ci change" in combined
