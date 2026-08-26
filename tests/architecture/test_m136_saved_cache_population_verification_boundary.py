"""Protect bounded read-only M136 saved population verification."""

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
    "src/ludoweave/assets/realization.py": "f0cfbb20d14326361bae0299f73377562de79f794cee2b1ec9060ade744631ad",
    "src/ludoweave/assets/population.py": "85605a634dcc63faa0ced102426ef81ea988678298330ae648478a030be11db5",
    "src/ludoweave/assets/pipeline.py": "a5439fecef0e352c3e19bb6e73246f897ee12f9d2e53574a24da0874b7062e08",
    "src/ludoweave/assets/locks.py": "85c6acd3ce416e175e1af4acf84ffdab70a55d077073705e21498caa6a392154",
    "src/ludoweave/assets/plans.py": "a56c1b335228a5bfcef77792d5a0436960e356b12df3fbb274b0c3fc04623a16",
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
    "scripts/smoke_asset_cache_population_wheel.py": "c83ab1758321a63ec0e811b9bf17b12f2aa34dbae407b11a78283515514a4490",
    "docs/rfcs/0118-add-post-realization-cache-population.md": "47ef00c97d47ebfcb7e5b30cab0f5da89e87e6b634e81d039478d3b5fa4f9be8",
    "tests/architecture/test_m135_post_realization_cache_population_boundary.py": "0f955e47c1843a1cd46bc4a1777c1349277ab7b95e074049b8a9381a3221885f",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m136_retains_ci_dependencies_and_prior_asset_contracts() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_population_reader_is_bounded_strict_and_duplicate_rejecting() -> None:
    source = (_ROOT / "src/ludoweave/assets/population_verification.py").read_text(encoding="utf-8")
    decoder = source.split("def from_json(", 1)[1].split("\n    def ", 1)[0]
    assert decoder.index("_document_bytes") < decoder.index("json.loads")
    assert "object_pairs_hook=_unique_object" in decoder
    assert "parse_constant=_reject_constant" in decoder
    assert "_exact_fields" in decoder
    assert "max_entries" in decoder
    for count in ("hits", "decoded", "published", "reused"):
        assert f'("{count}", record.{count})' in decoder


def test_population_verification_preflights_then_reads_without_write_authority() -> None:
    source = (_ROOT / "src/ludoweave/assets/population_verification.py").read_text(encoding="utf-8")
    block = source.split("def verify_asset_cache_population(", 1)[1].split("\ndef ", 1)[0]
    assert block.index("_preflight_population") < block.index("AssetCacheStore")
    assert block.index("AssetCacheStore") < block.index("cache.load_action")
    assert "writable=False" in block
    for forbidden in (
        ".publish(",
        "write_bytes",
        "write_text",
        "mkdir",
        "unlink",
        "rmtree",
        "os.replace",
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
        "importlib",
        "eval(",
        "exec(",
    ):
        assert forbidden not in source.casefold()


def test_cli_verifies_current_plan_before_saved_report_and_cache() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-cache-population-verify"' in cli
    block = cli.split("def _run_asset_cache_population_verify(", 1)[1].split("\ndef ", 1)[0]
    assert block.index("expected_lock.verify(current_lock)") < block.index(
        "expected_plan.verify(current_plan)"
    )
    assert block.index("expected_plan.verify(current_plan)") < block.index("read_relative")
    assert block.index("read_relative") < block.index("AssetCachePopulationRecord.from_json")
    assert block.index("AssetCachePopulationRecord.from_json") < block.index(
        "verify_asset_cache_population"
    )
    assert "_acquire_asset_build_inputs" not in block
    assert "AssetCacheStore" not in block
    assert ".publish(" not in block


def test_m136_has_behavior_installed_and_documentation_evidence() -> None:
    for path in (
        "tests/unit/test_asset_cache_population_verification.py",
        "tests/integration/test_asset_cache_cli.py",
        "scripts/smoke_asset_cache_population_verification_wheel.py",
        "docs/rfcs/0119-add-saved-cache-population-verification.md",
    ):
        assert (_ROOT / path).is_file()
    combined = "\n".join(
        (_ROOT / path).read_text(encoding="utf-8")
        for path in (
            "README.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "docs/architecture.md",
            "docs/rfcs/0119-add-saved-cache-population-verification.md",
        )
    ).casefold()
    assert "m136" in combined
    assert "ludoweave.asset-cache-population-verification/1" in combined
    assert "read-only" in combined
    assert "not provenance" in combined
    assert "no ci change" in combined
