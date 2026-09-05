"""Protect M141 offline comparison of two saved cache fingerprints."""

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
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
    "scripts/smoke_asset_cache_fingerprint_comparison_wheel.py": "e40dd846d35ebfde36a6771778467b20ccced903aa702aefbbb2d76e90c6c4f1",
    "docs/rfcs/0123-add-path-free-cache-fingerprint-comparison.md": "d4a9450ec2df36239634acdb2b2218d88938b7dd9c05c5e63a59a98c5050d323",
    "tests/architecture/test_m140_path_free_cache_fingerprint_comparison_boundary.py": "2cfeba68e437955b5b1a627634534e06281060a6c5afc4178b25ddd71dc2cc14",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m141_retains_ci_dependencies_storage_release_and_m140_evidence() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_record_comparison_preflights_both_values_and_never_observes_cache() -> None:
    source = (_ROOT / "src/ludoweave/assets/fingerprint_comparison.py").read_text(encoding="utf-8")
    block = source.split("def compare_asset_cache_fingerprint_records(", 1)[1].split("\ndef ", 1)[0]
    assert block.count("_preflight(") == 2
    assert block.index('_preflight(plan, expected, record_role="expected")') < block.index(
        '_preflight(plan, current, record_role="current")'
    )
    assert block.index('_preflight(plan, current, record_role="current")') < block.index(
        "_compare_records(expected, current)"
    )
    for forbidden in (
        "fingerprint_asset_cache_observation",
        "AssetCacheStore",
        "Path(",
        "open(",
        "read_",
        "write_",
        "cache_root",
    ):
        assert forbidden not in block


def test_record_comparison_reuses_m140_report_without_new_protocol() -> None:
    source = (_ROOT / "src/ludoweave/assets/fingerprint_comparison.py").read_text(encoding="utf-8")
    block = source.split("def _compare_records(", 1)[1].split("\ndef ", 1)[0]
    assert "AssetCacheFingerprintComparison(" in block
    assert "AssetCacheInventoryDelta.between(expected.inventory, current.inventory)" in block
    assert "current.observation_sha256 == expected.observation_sha256" in block
    assert source.count("ASSET_CACHE_FINGERPRINT_COMPARISON_PROTOCOL =") == 1
    assert "asset-cache-fingerprint-record-comparison/" not in source


def test_cli_checks_current_inputs_before_two_bounded_records_and_no_cache() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-cache-fingerprint-record-compare"' in cli
    block = cli.split("def _run_asset_cache_fingerprint_record_compare(", 1)[1].split("\ndef ", 1)[
        0
    ]
    assert block.index("expected_lock.verify(current_lock)") < block.index(
        "expected_plan.verify(current_plan)"
    )
    assert block.index("expected_plan.verify(current_plan)") < block.index(
        "expected_document = project.read_relative("
    )
    assert block.index("expected_document = project.read_relative(") < block.index(
        "current_document = project.read_relative("
    )
    assert block.count("max_bytes=ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES") == 2
    assert block.count("decode_asset_cache_fingerprint(") == 2
    assert "compare_asset_cache_fingerprint_records(" in block
    assert "return 0 if comparison.equal else 1" in block
    for forbidden in (
        '"cache"',
        "AssetCacheStore",
        "fingerprint_asset_cache_observation",
        "_acquire_asset_build_inputs",
        ".publish(",
    ):
        assert forbidden not in block


def test_m141_has_behavior_installed_and_documentation_evidence() -> None:
    for path in (
        "tests/unit/test_asset_cache_fingerprint_record_comparison.py",
        "tests/integration/test_asset_cache_cli.py",
        "scripts/smoke_asset_cache_fingerprint_record_comparison_wheel.py",
        "docs/rfcs/0124-add-offline-cache-fingerprint-comparison.md",
    ):
        assert (_ROOT / path).is_file()
    combined = "\n".join(
        (_ROOT / path).read_text(encoding="utf-8")
        for path in (
            "README.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "docs/architecture.md",
            "docs/rfcs/0124-add-offline-cache-fingerprint-comparison.md",
        )
    ).casefold()
    compact = " ".join(combined.split())
    assert "m141" in combined
    assert "asset-cache-fingerprint-record-compare" in combined
    assert "offline" in combined
    assert "not authenticity" in combined
    assert "no cache access" in combined
    assert "no ci change" in compact
