"""Protect bounded M128 asset-source lock generation and verification."""

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
    "src/ludoweave/scene/locks.py": "ff003999ab34bdc06721b5784df9046cda6b54db4b0e28776ccdf2e6d86e0799",
    "src/ludoweave/scene/sources.py": "1a5075fc0711330d7407537ba5f85ca15d2fc5d6e9bab733f954416420b30303",
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
    "scripts/smoke_source_asset_dependency_wheel.py": "6d5afd0369ff885519386c873222b1705a859396c72d4a3fe54052a737f2f769",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m128_retains_workflows_metadata_root_pipeline_scene_and_m127_boundaries() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_assets_expose_bounded_immutable_asset_source_lock_contract() -> None:
    source = (_ROOT / "src/ludoweave/assets/locks.py").read_text(encoding="utf-8")
    exports = (_ROOT / "src/ludoweave/assets/__init__.py").read_text(encoding="utf-8")
    assert 'ASSET_SOURCE_LOCK_PROTOCOL = "ludoweave.asset-source-lock/1"' in source
    assert "class AssetSourceLockLimits:" in source
    assert "class AssetSourceLockEntry:" in source
    assert "class AssetSourceLock:" in source
    assert "def verify(" in source
    assert "AssetSourceLock" in exports


def test_project_loader_and_cli_compose_lock_generation_and_verification() -> None:
    project = (_ROOT / "src/ludoweave/tools/headless_project.py").read_text(encoding="utf-8")
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert "def load_asset_source_lock(" in project
    assert "def hash_relative(" in project
    assert "def _hash_bounded(" in project
    assert 'source_command == "asset-lock"' in cli
    assert 'source_command == "asset-verify"' in cli
    assert "def _current_asset_source_lock(" in cli
    assert '"ludoweave.cli.asset-source-lock-verify/1"' in cli


def test_asset_source_lock_has_behavior_and_installed_evidence() -> None:
    assert (_ROOT / "tests/unit/test_asset_source_lock.py").is_file()
    assert (_ROOT / "tests/integration/test_asset_source_lock_cli.py").is_file()
    assert (_ROOT / "scripts/smoke_asset_source_lock_wheel.py").is_file()


def test_m128_docs_define_input_identity_only_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/api-status.md",
        _ROOT / "docs/rfcs/0111-add-asset-source-lock-verification.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    folded = combined.casefold()
    assert "M128" in combined
    assert "ludoweave.asset-source-lock/1" in combined
    assert "256 mib" in folded
    assert "1 gib" in folded
    assert "no asset decode" in folded
    assert "no asset build" in folded
    assert "no cache write" in folded
    assert "no workflow allocation" in folded
