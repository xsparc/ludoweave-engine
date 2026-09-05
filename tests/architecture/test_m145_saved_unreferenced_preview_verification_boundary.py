"""Protect M145 bounded saved-preview admission and pure offline verification."""

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
        "f871de4856b3d4428c2a63c8c36797f38daf7beaef905c98c4b05dbdb27a18ad"
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
    "scripts/smoke_asset_cache_fingerprint_record_preview_wheel.py": (
        "089091bb66f31e54504bcaf7d10dafdcebbef306a2289d931f6a14eff359840b"
    ),
    "docs/rfcs/0127-add-offline-unreferenced-blob-preview.md": (
        "84bbf0039bd0c6edd50438e904a7406f6a6b54b0d8f8830bd2b1d5ddac9ee7d2"
    ),
    "tests/architecture/test_m144_offline_unreferenced_blob_preview_boundary.py": (
        "132eb18034455337fd056d1aa88e78f50c36837ea93d84eed709983fc14f036a"
    ),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m145_retains_ci_dependencies_cache_release_and_m144_evidence() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_saved_preview_admission_is_bounded_exact_and_canonical() -> None:
    source = (_ROOT / "src/ludoweave/assets/unreferenced_preview_verification.py").read_text(
        encoding="utf-8"
    )
    assert "ASSET_CACHE_UNREFERENCED_PREVIEW_RECORD_MAX_BYTES = 2_048" in source
    assert source.count("@dataclass(frozen=True, slots=True)") == 2
    decoder = source.split("def decode_asset_cache_unreferenced_preview(", 1)[1].split(
        "\ndef verify_asset_cache_unreferenced_preview(", 1
    )[0]
    for required in (
        "object_pairs_hook=_unique_object",
        "parse_constant=_reject_constant",
        "_exact_fields(",
        'root["status"]',
        "_bounded_integer(",
        "raw != preview.canonical_bytes()",
        "AssetCacheUnreferencedPreview(",
    ):
        assert required in decoder


def test_saved_preview_verification_is_pure_exact_and_path_free() -> None:
    source = (_ROOT / "src/ludoweave/assets/unreferenced_preview_verification.py").read_text(
        encoding="utf-8"
    )
    block = source.split("def verify_asset_cache_unreferenced_preview(", 1)[1].split("\ndef ", 1)[0]
    assert "type(value) is not expected_type" in block
    assert block.count("preview_asset_cache_unreferenced_blobs(") == 1
    assert "if preview != recomputed" in block
    assert "sha256(preview_bytes)" in block
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
        "unlink(",
        "remove(",
    ):
        assert forbidden not in block


def test_cli_preflights_then_reads_two_bounded_records_without_cache() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert 'source_command == "asset-cache-unreferenced-preview-verify"' in cli
    block = cli.split("def _run_asset_cache_unreferenced_preview_verify(", 1)[1].split("\ndef ", 1)[
        0
    ]
    assert block.index("expected_lock.verify(current_lock)") < block.index(
        "expected_plan.verify(current_plan)"
    )
    assert block.index("expected_plan.verify(current_plan)") < block.index("project.read_relative(")
    assert block.count("project.read_relative(") == 2
    assert "max_bytes=ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES" in block
    assert "max_bytes=ASSET_CACHE_UNREFERENCED_PREVIEW_RECORD_MAX_BYTES" in block
    assert block.index("decode_asset_cache_fingerprint(") < block.index(
        "decode_asset_cache_unreferenced_preview("
    )
    assert block.index("decode_asset_cache_unreferenced_preview(") < block.index(
        "verify_asset_cache_unreferenced_preview("
    )
    assert "return 0" in block
    for forbidden in (
        '"cache"',
        "fingerprint_asset_cache_observation",
        "inspect_asset_cache_inventory",
        "AssetCacheStore",
        ".publish(",
        "unlink(",
        "rmtree(",
        "remove(",
    ):
        assert forbidden not in block


def test_m145_exports_behavior_installed_and_documentation_evidence() -> None:
    exported = (_ROOT / "src/ludoweave/assets/__init__.py").read_text(encoding="utf-8")
    for name in (
        "ASSET_CACHE_UNREFERENCED_PREVIEW_RECORD_MAX_BYTES",
        "ASSET_CACHE_UNREFERENCED_PREVIEW_VERIFICATION_PROTOCOL",
        "AssetCacheUnreferencedPreviewRecordLimits",
        "AssetCacheUnreferencedPreviewVerification",
        "decode_asset_cache_unreferenced_preview",
        "verify_asset_cache_unreferenced_preview",
    ):
        assert f'"{name}"' in exported
    for path in (
        "tests/unit/test_asset_cache_unreferenced_preview_verification.py",
        "tests/integration/test_asset_cache_cli.py",
        "scripts/smoke_asset_cache_unreferenced_preview_verification_wheel.py",
        "docs/rfcs/0128-verify-saved-unreferenced-blob-preview.md",
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
            "docs/rfcs/0128-verify-saved-unreferenced-blob-preview.md",
        )
    ).casefold()
    compact = " ".join(combined.split())
    assert "m145" in combined
    assert "asset-cache-unreferenced-preview-verify" in combined
    assert "offline" in combined
    assert "no cache" in compact
    assert "no ci change" in compact
