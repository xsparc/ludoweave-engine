"""Protect M148's platform-capability decision and cleanup deferral."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946",
    ".github/workflows/release.yml": "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5",
    "docs/rfcs/0130-asset-cache-cleanup-threat-model.md": (
        "2a1f069cbeb9910c78b92933aea5242f784761077a80aee396b9541c484a2638"
    ),
    "docs/security/cache-cleanup-threat-model.md": (
        "30bf17e604d900525263aa9cd3fa83195175dd5625de07feeb4d201b181a7443"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
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


def test_m148_changes_no_runtime_script_dependency_ci_or_m147_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m148_adds_no_cleanup_adapter_probe_or_native_implementation() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "asset-cache-cleanup",
        "asset-cache-capabilities",
        "asset-cache-prune",
        "asset-cache-delete",
    ):
        assert command not in cli
    names = {path.name for path in (_ROOT / "src/ludoweave/assets").glob("*.py")}
    assert {
        "cleanup.py",
        "cleanup_capabilities.py",
        "filesystem_adapter.py",
        "garbage_collection.py",
        "retention.py",
    }.isdisjoint(names)


def test_m148_records_complete_platform_capability_decision() -> None:
    decision = (_ROOT / "docs/security/cache-cleanup-platform-capability-decision.md").read_text(
        encoding="utf-8"
    )
    compact = " ".join(decision.casefold().split())
    for required in (
        "no platform is admitted for cleanup",
        "standard library",
        "engine-owned, platform-specific filesystem capability",
        "no `dir_fd` support",
        "shutil.rmtree.avoids_symlink_attacks",
        "openat2",
        "o_nofollow_any",
        "file_flag_open_reparse_point",
        "setfileinformationbyhandle",
        "same-filesystem quarantine",
        "native objects must never enter the public api",
        "installed-wheel proof",
        "safe refusal",
    ):
        assert required in compact


def test_m148_rfc_and_public_decision_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0131-defer-portable-cache-cleanup-capability.md").read_text(
        encoding="utf-8"
    )
    assert "**Status:** Accepted" in rfc
    assert "cleanup remains unimplemented and unauthorized" in " ".join(rfc.casefold().split())
    for path in (
        "README.md",
        "CHANGELOG.md",
        "ROADMAP.md",
        "SECURITY.md",
        "docs/architecture.md",
        "docs/index.md",
        "mkdocs.yml",
    ):
        content = (_ROOT / path).read_text(encoding="utf-8")
        assert "cache-cleanup-platform-capability-decision" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0131-defer-portable-cache-cleanup-capability.md" in rfc_index


def test_m148_documents_explicit_non_goals_and_ci_restraint() -> None:
    paths = (
        "ROADMAP.md",
        "docs/architecture.md",
        "docs/rfcs/0131-defer-portable-cache-cleanup-capability.md",
        "docs/security/cache-cleanup-platform-capability-decision.md",
    )
    compact = " ".join(
        "\n".join((_ROOT / path).read_text(encoding="utf-8") for path in paths).casefold().split()
    )
    for required in (
        "no runtime api",
        "no public probe",
        "no cleanup authority",
        "no native code",
        "no dependency",
        "no workflow",
        "no ci change",
        "no remote cache",
    ):
        assert required in compact
