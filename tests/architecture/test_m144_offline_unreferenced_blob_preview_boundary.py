"""Protect M144 cache-free saved-fingerprint preview composition."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5",
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
    "src/ludoweave/assets/cache.py": (
        "bc0c253a46bd81735e15d5ba899d7e3b7cdcd7ecedde5b726f6c27dab410699f"
    ),
    "src/ludoweave/assets/inventory.py": (
        "5da1b6074bae2c09d2737a404ff10b0091b089a627615e2d0af755aed98017e8"
    ),
    "src/ludoweave/assets/fingerprint_verification.py": (
        "19f992d3a9ab6465e41808789453823d29cbb228ffc277b5e0e55c7cb8a27f8c"
    ),
    "src/ludoweave/assets/unreferenced_preview.py": (
        "697e0c7bfb33a0f2ed8dbb59bc46535dc2841bc55b535d1bc301639c3e6fd448"
    ),
    "scripts/release_artifacts.py": (
        "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca"
    ),
    "scripts/smoke_release.py": (
        "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be"
    ),
    "scripts/smoke_asset_cache_unreferenced_preview_wheel.py": (
        "b95bc2235d11669c25236656e0e75cd32b794bc35a3e43466566cab8771e40ca"
    ),
    "docs/rfcs/0126-add-path-free-unreferenced-blob-preview.md": (
        "fd48c7efb9e2160256f08217303812b07d7a11fcf9e9bc4ca03d3f609cded89a"
    ),
    "tests/architecture/test_m143_path_free_unreferenced_blob_preview_boundary.py": (
        "303bee0cb3bddaf97fe17b2ede3dd5b271909b0dc318d5287063083a6b64274e"
    ),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m144_retains_ci_dependencies_runtime_decoder_release_and_m143_evidence() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_record_preview_preflights_then_reads_one_bounded_record_offline() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-cache-fingerprint-record-preview"' in cli
    block = cli.split("def _run_asset_cache_fingerprint_record_preview(", 1)[1].split("\ndef ", 1)[
        0
    ]
    assert block.index("expected_lock.verify(current_lock)") < block.index(
        "expected_plan.verify(current_plan)"
    )
    assert block.index("expected_plan.verify(current_plan)") < block.index("project.read_relative(")
    assert block.count("project.read_relative(") == 1
    assert "max_bytes=ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES" in block
    assert block.count("decode_asset_cache_fingerprint(") == 1
    assert block.index("decode_asset_cache_fingerprint(") < block.index(
        "preview_asset_cache_unreferenced_blobs("
    )
    assert "return 0" in block
    for forbidden in (
        "fingerprint_asset_cache_observation",
        "inspect_asset_cache_inventory",
        "AssetCacheStore",
        '"cache"',
        "populate_asset_build_cache",
        ".publish(",
        "unlink(",
        "rmtree(",
        "remove(",
    ):
        assert forbidden not in block


def test_m144_reuses_m139_admission_and_m143_output_without_new_runtime_protocol() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    parser = cli.split("source_asset_cache_fingerprint_record_preview_parser =", 1)[1].split(
        "source_asset_cache_fingerprint_verify_parser =", 1
    )[0]
    assert '"asset-cache-fingerprint-record-preview"' in parser
    assert '"--fingerprint"' in parser
    assert '"--cache"' not in parser
    assert "ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES" in cli
    assert "decode_asset_cache_fingerprint" in cli
    assert "preview_asset_cache_unreferenced_blobs" in cli
    assert "ludoweave.asset-cache-unreferenced-preview/1" not in parser


def test_m144_has_offline_behavior_installed_and_documentation_evidence() -> None:
    for path in (
        "tests/integration/test_asset_cache_cli.py",
        "scripts/smoke_asset_cache_fingerprint_record_preview_wheel.py",
        "docs/rfcs/0127-add-offline-unreferenced-blob-preview.md",
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
            "docs/rfcs/0127-add-offline-unreferenced-blob-preview.md",
        )
    ).casefold()
    compact = " ".join(combined.split())
    assert "m144" in combined
    assert "asset-cache-fingerprint-record-preview" in combined
    assert "offline" in combined
    assert "no cache" in compact
    assert "no ci change" in compact
