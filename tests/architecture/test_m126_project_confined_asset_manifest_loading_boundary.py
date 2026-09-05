"""Protect bounded M126 project-confined asset-manifest loading."""

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
    "src/ludoweave/scene/document.py": "ed18afa22514a39585b303c7cc4f78a912b4486a86f64a57c797f884d377d9c7",
    "src/ludoweave/scene/planning.py": "a47fbbd14f7583bf3bdb9284c3dc902d46e541fb8640dd569b60ff6e526b0716",
    "src/ludoweave/scene/prefab.py": "114d5884a31595d3e637393c18f1b864a8c1996becbd186624bd1e0b060ae0b0",
    "src/ludoweave/scene/sources.py": "1a5075fc0711330d7407537ba5f85ca15d2fc5d6e9bab733f954416420b30303",
    "src/ludoweave/scene/locks.py": "ff003999ab34bdc06721b5784df9046cda6b54db4b0e28776ccdf2e6d86e0799",
    "scripts/smoke_source_lock_wheel.py": "3e249de70132f143c3b3ac0b2c655cde820541d162095411fc72a39b1eb8c611",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m126_retains_workflows_metadata_root_and_m125_source_contract() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_asset_manifest_contract_is_bounded_and_focused() -> None:
    source = (_ROOT / "src/ludoweave/assets/pipeline.py").read_text(encoding="utf-8")
    exports = (_ROOT / "src/ludoweave/assets/__init__.py").read_text(encoding="utf-8")
    assert 'ASSET_MANIFEST_PROTOCOL = "ludoweave.assets/1"' in source
    assert "class AssetManifestLimits:" in source
    assert "def from_json(" in source
    assert "def canonical_bytes(" in source
    assert '"ASSET_MANIFEST_PROTOCOL"' in exports
    assert '"AssetManifestLimits"' in exports


def test_headless_project_loads_one_confined_bounded_asset_manifest() -> None:
    source = (_ROOT / "src/ludoweave/tools/headless_project.py").read_text(encoding="utf-8")
    assert "def load_asset_manifest(" in source
    assert 'role="asset_manifest"' in source
    assert "AssetManifest.from_json(" in source


def test_asset_manifest_file_loader_has_installed_evidence() -> None:
    assert (_ROOT / "tests/unit/test_asset_manifest_file_loading.py").is_file()
    assert (_ROOT / "scripts/smoke_asset_manifest_file_wheel.py").is_file()


def test_m126_docs_define_loader_only_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "ROADMAP.md",
        _ROOT / "docs/architecture.md",
        _ROOT / "docs/api-status.md",
        _ROOT / "docs/rfcs/0109-add-project-confined-asset-manifest-loading.md",
    )
    assert all(path.is_file() for path in paths)
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    folded = combined.casefold()
    assert "M126" in combined
    assert "ludoweave.assets/1" in combined
    assert "project-confined asset manifest" in folded
    assert "no asset source read" in folded
    assert "no asset build" in folded
    assert "no cache" in folded
    assert "no directory discovery" in folded
    assert "no world mutation" in folded
    assert "no workflow allocation" in folded
