"""Protect M143 path-free read-only unreferenced-blob preview evidence."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5",
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
    "src/ludoweave/assets/cache.py": "bc0c253a46bd81735e15d5ba899d7e3b7cdcd7ecedde5b726f6c27dab410699f",
    "src/ludoweave/assets/inventory.py": "5da1b6074bae2c09d2737a404ff10b0091b089a627615e2d0af755aed98017e8",
    "src/ludoweave/assets/fingerprint_verification.py": "f871de4856b3d4428c2a63c8c36797f38daf7beaef905c98c4b05dbdb27a18ad",
    "src/ludoweave/assets/fingerprint_comparison.py": "22ad26eb008f7ffc77099bcadcb7dc5b81658ca44bbe1822faccba84376416a7",
    "src/ludoweave/assets/fingerprint_comparison_verification.py": (
        "8c81ffbd941b3e6ed9bb24defd3497323d6eb1a73ee24a1a458009480e4ff8d1"
    ),
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
    "scripts/smoke_asset_cache_fingerprint_comparison_verification_wheel.py": (
        "cfa1380cbfb7619eef487732af9552242cbc5375a62dd91e97ba27c04d9bcfc2"
    ),
    "docs/rfcs/0125-verify-saved-cache-fingerprint-comparison.md": (
        "4c6c751c28d6dd30c9fa2ea0b2a82d0dd633e89192d648b1b26bce7590d8d83a"
    ),
    "tests/architecture/test_m142_saved_cache_fingerprint_comparison_verification_boundary.py": (
        "1a0b9a00d8894c1494db16beb287446437f027f0edbad32875b7cce3abcf20ef"
    ),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m143_retains_ci_dependencies_cache_release_and_m142_evidence() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_preview_value_is_fixed_path_free_and_aggregate_only() -> None:
    source = (_ROOT / "src/ludoweave/assets/unreferenced_preview.py").read_text(encoding="utf-8")
    value = source.split("class AssetCacheUnreferencedPreview:", 1)[1].split(
        "\ndef preview_asset_cache_unreferenced_blobs(", 1
    )[0]
    assert '"ludoweave.asset-cache-unreferenced-preview/1"' in source
    assert "@dataclass(frozen=True, slots=True)" in source
    for field in (
        '"status": "observed"',
        '"fingerprint_protocol"',
        '"inventory_protocol"',
        '"plan_sha256"',
        '"observation_sha256"',
        '"unreferenced_blobs"',
        '"unreferenced_blob_bytes"',
    ):
        assert field in value
    for forbidden in (
        '"candidates"',
        '"cache_key"',
        '"uri"',
        '"path"',
        '"filename"',
        '"timestamp"',
        '"age"',
        '"deletable"',
    ):
        assert forbidden not in value


def test_preview_function_is_pure_exact_and_plan_bound() -> None:
    source = (_ROOT / "src/ludoweave/assets/unreferenced_preview.py").read_text(encoding="utf-8")
    block = source.split("def preview_asset_cache_unreferenced_blobs(", 1)[1].split("\ndef ", 1)[0]
    assert "type(plan) is not AssetBuildPlan" in block
    assert "type(fingerprint) is not AssetCacheFingerprint" in block
    assert "sha256(plan.canonical_bytes())" in block
    assert "inventory.plan_sha256 != plan_sha256" in block
    assert "inventory.unreferenced_blobs" in block
    assert "inventory.unreferenced_blob_bytes" in block
    for forbidden in (
        "fingerprint_asset_cache_observation",
        "inspect_asset_cache_inventory",
        "AssetCacheStore",
        "Path(",
        "open(",
        "read_",
        "write_",
        "cache_root",
        "subprocess",
        "thread",
        "socket",
        "time.",
        "os.",
    ):
        assert forbidden not in block


def test_cli_preflights_inputs_then_observes_once_without_mutation() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-cache-unreferenced-preview"' in cli
    block = cli.split("def _run_asset_cache_unreferenced_preview(", 1)[1].split("\ndef ", 1)[0]
    assert block.index("expected_lock.verify(current_lock)") < block.index(
        "expected_plan.verify(current_plan)"
    )
    assert block.index("expected_plan.verify(current_plan)") < block.index(
        "fingerprint_asset_cache_observation("
    )
    assert block.count("fingerprint_asset_cache_observation(") == 1
    assert block.index("fingerprint_asset_cache_observation(") < block.index(
        "preview_asset_cache_unreferenced_blobs("
    )
    assert "return 0" in block
    for forbidden in (
        "AssetCacheStore",
        "inspect_asset_cache_inventory",
        "populate_asset_build_cache",
        ".publish(",
        "unlink(",
        "rmtree(",
        "remove(",
    ):
        assert forbidden not in block


def test_m143_has_behavior_installed_and_documentation_evidence() -> None:
    for path in (
        "tests/unit/test_asset_cache_unreferenced_preview.py",
        "tests/integration/test_asset_cache_cli.py",
        "scripts/smoke_asset_cache_unreferenced_preview_wheel.py",
        "docs/rfcs/0126-add-path-free-unreferenced-blob-preview.md",
    ):
        assert (_ROOT / path).is_file()
    combined = "\n".join(
        (_ROOT / path).read_text(encoding="utf-8")
        for path in (
            "README.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "docs/architecture.md",
            "docs/cli-workflows.md",
            "docs/rfcs/0126-add-path-free-unreferenced-blob-preview.md",
        )
    ).casefold()
    compact = " ".join(combined.split())
    assert "m143" in combined
    assert "asset-cache-unreferenced-preview" in combined
    assert "path-free" in combined
    assert "not a" in combined and "deletion" in combined
    assert "no ci change" in compact
