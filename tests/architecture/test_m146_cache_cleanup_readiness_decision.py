"""Protect M146's evidence-based deferral of asset-cache cleanup."""

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
    "src/ludoweave/assets/unreferenced_preview.py": "697e0c7bfb33a0f2ed8dbb59bc46535dc2841bc55b535d1bc301639c3e6fd448",
    "src/ludoweave/assets/unreferenced_preview_verification.py": (
        "44f47ea976850a71add147cf7bc194ae342542b14d485a02320ea9e7f18b076f"
    ),
    "src/ludoweave/tools/cli.py": "0cf1f5153d0bf8c7ed55c835a99ec387f714e5b182e1d5d826fbd689e5dc65d9",
    "scripts/release_artifacts.py": "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca",
    "scripts/smoke_release.py": "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m146_changes_no_runtime_dependency_ci_or_release_surface() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED} == _PROTECTED


def test_m146_adds_no_cleanup_command_or_implementation() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert "asset-cache-cleanup" not in cli
    assert "asset-cache-prune" not in cli
    assert "asset-cache-delete" not in cli
    assets = _ROOT / "src/ludoweave/assets"
    names = {path.name for path in assets.glob("*.py")}
    assert "cleanup.py" not in names
    assert "garbage_collection.py" not in names
    assert "retention.py" not in names


def test_m146_records_complete_reconsideration_gates_and_non_goals() -> None:
    paths = (
        "README.md",
        "CHANGELOG.md",
        "ROADMAP.md",
        "docs/architecture.md",
        "docs/rfcs/0129-defer-asset-cache-cleanup.md",
    )
    combined = "\n".join((_ROOT / path).read_text(encoding="utf-8") for path in paths)
    compact = " ".join(combined.casefold().split())
    for required in (
        "m146",
        "identity-bearing",
        "retained roots",
        "quiescence",
        "trusted time",
        "mutation receipts",
        "concurrent-writer",
        "crash recovery",
        "reparse",
        "rollback",
        "no runtime",
        "no ci change",
    ):
        assert required in compact


def test_m146_rfc_is_accepted_and_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0129-defer-asset-cache-cleanup.md").read_text(encoding="utf-8")
    assert "**Status:** Accepted" in rfc
    assert "aggregate equality does not prove object identity" in rfc.casefold()
    index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    navigation = (_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert "0129-defer-asset-cache-cleanup.md" in index
    assert "0129-defer-asset-cache-cleanup.md" in navigation
