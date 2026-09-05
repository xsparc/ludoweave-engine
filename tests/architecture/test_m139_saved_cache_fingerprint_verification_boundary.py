"""Protect strict bounded M139 saved cache fingerprint verification."""

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
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
    "scripts/smoke_asset_cache_fingerprint_wheel.py": "afe0d9a3b55edf42ba4d187e5a59547f4767d26c2be587ad1d643a01ff0aa495",
    "docs/rfcs/0121-add-deterministic-cache-observation-fingerprint.md": "db537708a082e384ff8938b7e37382c79e37776c2dde5ed14f5bb6e201610689",
    "tests/architecture/test_m138_cache_observation_fingerprint_boundary.py": "81d72f3606265c70b9329631ae278f043060bd70735cf5510e78a48f38cf961d",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m139_retains_ci_dependencies_storage_release_and_m138_evidence() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_verifier_preflights_before_exactly_one_bounded_observation() -> None:
    source = (_ROOT / "src/ludoweave/assets/fingerprint_verification.py").read_text(
        encoding="utf-8"
    )
    block = source.split("def verify_asset_cache_fingerprint(", 1)[1].split("\ndef ", 1)[0]
    assert block.count("fingerprint_asset_cache_observation(") == 1
    assert block.index("_preflight_fingerprint(") < block.index(
        "fingerprint_asset_cache_observation("
    )
    assert block.index("current.inventory != fingerprint.inventory") < block.index(
        "current.observation_sha256 != fingerprint.observation_sha256"
    )
    assert "AssetCacheStore(" not in block


def test_record_decoder_is_bounded_exact_schema_and_ambiguity_rejecting() -> None:
    source = (_ROOT / "src/ludoweave/assets/fingerprint_verification.py").read_text(
        encoding="utf-8"
    )
    block = source.split("def decode_asset_cache_fingerprint(", 1)[1].split("\ndef ", 1)[0]
    assert "_document_bytes(document, maximum=checked_limits.max_bytes)" in block
    assert "object_pairs_hook=_unique_object" in block
    assert "parse_constant=_reject_constant" in block
    assert "_exact_fields(" in block
    assert "raw != fingerprint.canonical_bytes()" in block
    assert "open(" not in block


def test_verification_adds_no_mutation_remote_cleanup_or_backend_capability() -> None:
    source = (
        (_ROOT / "src/ludoweave/assets/fingerprint_verification.py")
        .read_text(encoding="utf-8")
        .casefold()
    )
    for forbidden in (
        "write_bytes",
        "write_text",
        "mkdir",
        "unlink",
        "rmdir",
        "rmtree",
        "remove(",
        "replace(",
        "tempfile",
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
        assert forbidden not in source


def test_cli_checks_current_plan_then_saved_record_then_current_cache() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-cache-fingerprint-verify"' in cli
    block = cli.split("def _run_asset_cache_fingerprint_verify(", 1)[1].split("\ndef ", 1)[0]
    assert block.index("expected_lock.verify(current_lock)") < block.index(
        "expected_plan.verify(current_plan)"
    )
    assert block.index("expected_plan.verify(current_plan)") < block.index("project.read_relative(")
    assert block.index("decode_asset_cache_fingerprint(") < block.index(
        "verify_asset_cache_fingerprint("
    )
    assert "_acquire_asset_build_inputs" not in block
    assert ".publish(" not in block


def test_m139_has_behavior_installed_and_documentation_evidence() -> None:
    for path in (
        "tests/unit/test_asset_cache_fingerprint_verification.py",
        "tests/integration/test_asset_cache_cli.py",
        "scripts/smoke_asset_cache_fingerprint_verification_wheel.py",
        "docs/rfcs/0122-add-saved-cache-fingerprint-verification.md",
    ):
        assert (_ROOT / path).is_file()
    combined = "\n".join(
        (_ROOT / path).read_text(encoding="utf-8")
        for path in (
            "README.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "docs/architecture.md",
            "docs/rfcs/0122-add-saved-cache-fingerprint-verification.md",
        )
    ).casefold()
    compact = " ".join(combined.split())
    assert "m139" in combined
    assert "ludoweave.asset-cache-fingerprint-verification/1" in combined
    assert "integrity equality" in combined
    assert "not authenticity" in combined
    assert "no ci change" in compact
