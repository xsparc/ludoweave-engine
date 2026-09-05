"""Protect M142 strict saved-comparison admission and offline verification."""

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
    "src/ludoweave/assets/fingerprint_verification.py": "19f992d3a9ab6465e41808789453823d29cbb228ffc277b5e0e55c7cb8a27f8c",
    "src/ludoweave/assets/fingerprint_comparison.py": "22ad26eb008f7ffc77099bcadcb7dc5b81658ca44bbe1822faccba84376416a7",
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
    "scripts/smoke_asset_cache_fingerprint_record_comparison_wheel.py": "299cdf804c91c2224c6fb49702d526278b23853d604a72369e4956202cf24492",
    "docs/rfcs/0124-add-offline-cache-fingerprint-comparison.md": "727119631ef33af8ce66f7b1ce2549a3cdc46391d6889485014b319715113b72",
    "tests/architecture/test_m141_offline_cache_fingerprint_comparison_boundary.py": "9e3d7acd38361a4b4ce2b88eb0a2af13cac3364192fd4a9ba60b6a4eb716e3d9",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m142_retains_ci_dependencies_cache_release_and_m141_evidence() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_comparison_decoder_is_bounded_exact_and_canonical() -> None:
    source = (_ROOT / "src/ludoweave/assets/fingerprint_comparison_verification.py").read_text(
        encoding="utf-8"
    )
    block = source.split("def decode_asset_cache_fingerprint_comparison(", 1)[1].split("\ndef ", 1)[
        0
    ]
    assert "ASSET_CACHE_FINGERPRINT_COMPARISON_RECORD_MAX_BYTES = 4_096" in source
    assert "object_pairs_hook=_unique_object" in block
    assert "parse_constant=_reject_constant" in block
    assert "parse_int=_parse_integer" in block
    assert 'field="comparison"' in block
    assert 'field="deltas"' in block
    assert "raw != comparison.canonical_bytes()" in block
    assert "AssetCacheFingerprintComparison(" in block
    assert "AssetCacheInventoryDelta(" in block


def test_comparison_verifier_is_pure_and_recomputes_exact_evidence() -> None:
    source = (_ROOT / "src/ludoweave/assets/fingerprint_comparison_verification.py").read_text(
        encoding="utf-8"
    )
    block = source.split("def verify_asset_cache_fingerprint_comparison(", 1)[1].split("\ndef ", 1)[
        0
    ]
    assert "compare_asset_cache_fingerprint_records(plan, expected, current)" in block
    assert block.index("recomputed =") < block.index("comparison != recomputed")
    assert "sha256(comparison_bytes)" in block
    assert "AssetCacheFingerprintComparisonVerification(" in block
    for forbidden in (
        "fingerprint_asset_cache_observation",
        "AssetCacheStore",
        "Path(",
        "open(",
        "read_",
        "write_",
        "cache_root",
        "subprocess",
        "thread",
        "socket",
    ):
        assert forbidden not in block


def test_cli_preflights_current_inputs_before_three_bounded_records_without_cache() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-cache-fingerprint-comparison-verify"' in cli
    block = cli.split("def _run_asset_cache_fingerprint_comparison_verify(", 1)[1].split(
        "\ndef ", 1
    )[0]
    assert block.index("expected_lock.verify(current_lock)") < block.index(
        "expected_plan.verify(current_plan)"
    )
    assert block.index("expected_plan.verify(current_plan)") < block.index(
        'role="expected_asset_cache_fingerprint"'
    )
    assert block.index('role="expected_asset_cache_fingerprint"') < block.index(
        'role="current_asset_cache_fingerprint"'
    )
    assert block.index('role="current_asset_cache_fingerprint"') < block.index(
        'role="asset_cache_fingerprint_comparison"'
    )
    assert block.count("max_bytes=ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES") == 2
    assert block.count("max_bytes=ASSET_CACHE_FINGERPRINT_COMPARISON_RECORD_MAX_BYTES") == 1
    assert block.count("decode_asset_cache_fingerprint(") == 2
    assert block.count("decode_asset_cache_fingerprint_comparison(") == 1
    assert "verify_asset_cache_fingerprint_comparison(" in block
    assert "return 0" in block
    for forbidden in (
        '"cache"',
        "AssetCacheStore",
        "fingerprint_asset_cache_observation",
        "_acquire_asset_build_inputs",
        ".publish(",
    ):
        assert forbidden not in block


def test_m142_has_behavior_installed_and_documentation_evidence() -> None:
    for path in (
        "tests/unit/test_asset_cache_fingerprint_comparison_verification.py",
        "tests/integration/test_asset_cache_cli.py",
        "scripts/smoke_asset_cache_fingerprint_comparison_verification_wheel.py",
        "docs/rfcs/0125-verify-saved-cache-fingerprint-comparison.md",
    ):
        assert (_ROOT / path).is_file()
    combined = "\n".join(
        (_ROOT / path).read_text(encoding="utf-8")
        for path in (
            "README.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "docs/architecture.md",
            "docs/rfcs/0125-verify-saved-cache-fingerprint-comparison.md",
        )
    ).casefold()
    compact = " ".join(combined.split())
    assert "m142" in combined
    assert "asset-cache-fingerprint-comparison-verify" in combined
    assert "offline" in combined
    assert "not authenticity" in combined
    assert "no cache access" in combined
    assert "no ci change" in compact
