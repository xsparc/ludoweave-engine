"""Protect M147's asset-cache cleanup threat model and runtime deferral."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "883674592dd8cfc7f2c292f379591f863c797fdb0cd65f2c0c83a47e232db686",
    ".github/workflows/release.yml": "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5",
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "uv.lock": "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18",
}
_PROTECTED_TREES = {
    "scripts": "9e410ddc56b56dd0485172e97fa371d6773f7b74b11f8fc1ff230faf33b3abd9",
    "src/ludoweave": "e6c951393b86b0673a25e0f6b1f4cf41224d3cb7807dd85c76aad482820cde36",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    for candidate in sorted(path.rglob("*")):
        if (
            candidate.is_file()
            and "__pycache__" not in candidate.parts
            and candidate.suffix != ".pyc"
        ):
            digest.update(candidate.relative_to(path).as_posix().encode())
            digest.update(b"\0")
            digest.update(candidate.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def test_m147_changes_no_runtime_script_dependency_or_ci_surface() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m147_adds_no_cleanup_command_or_implementation() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    assert "asset-cache-cleanup" not in cli
    assert "asset-cache-prune" not in cli
    assert "asset-cache-delete" not in cli
    names = {path.name for path in (_ROOT / "src/ludoweave/assets").glob("*.py")}
    assert {"cleanup.py", "garbage_collection.py", "retention.py"}.isdisjoint(names)


def test_m147_threat_model_covers_required_threats_and_invariants() -> None:
    threat_model = (_ROOT / "docs/security/cache-cleanup-threat-model.md").read_text(
        encoding="utf-8"
    )
    compact = " ".join(threat_model.casefold().split())
    for threat_id in range(1, 13):
        assert f"cct-{threat_id:02d}" in compact
    for required in (
        "time-of-check/time-of-use",
        "symlink",
        "junction",
        "reparse",
        "hard links",
        "concurrent reader",
        "stale, replayed, forged",
        "clock rollback",
        "disk-full",
        "same-filesystem quarantine",
        "idempotency",
        "path-free",
        "handle-relative, no-follow",
        "fails closed",
        "dry-run and mutation",
        "windows, macos, and linux",
        "cleanup remains unimplemented",
    ):
        assert required in compact


def test_m147_rfc_and_public_security_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0130-asset-cache-cleanup-threat-model.md").read_text(encoding="utf-8")
    assert "**Status:** Accepted" in rfc
    assert "cleanup remains unimplemented and unauthorized" in rfc.casefold()
    for path in (
        "docs/readme-history.md",
        "CHANGELOG.md",
        "ROADMAP.md",
        "SECURITY.md",
        "docs/architecture.md",
        "docs/index.md",
        "docs/rfcs/index.md",
        "mkdocs.yml",
    ):
        content = (_ROOT / path).read_text(encoding="utf-8")
        assert "cache-cleanup-threat-model" in content


def test_m147_documents_explicit_non_goals() -> None:
    paths = (
        "ROADMAP.md",
        "docs/architecture.md",
        "docs/rfcs/0130-asset-cache-cleanup-threat-model.md",
        "docs/security/cache-cleanup-threat-model.md",
    )
    compact = " ".join(
        "\n".join((_ROOT / path).read_text(encoding="utf-8") for path in paths).casefold().split()
    )
    for required in (
        "no runtime api",
        "no cleanup authority",
        "no candidate disclosure",
        "no dependency",
        "no workflow",
        "no ci change",
        "no remote cache",
    ):
        assert required in compact
