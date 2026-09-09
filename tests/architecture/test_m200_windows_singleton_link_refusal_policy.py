"""Protect M200's Windows singleton-link refusal policy boundary."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "883674592dd8cfc7f2c292f379591f863c797fdb0cd65f2c0c83a47e232db686"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0182-refresh-windows-cache-cleanup-readiness.md": (
        "2d45861c8af75c06a8ba52fb7bbed9c2b937a8ff701f14201c4992af27310769"
    ),
    "docs/security/cache-cleanup-windows-readiness-refresh.md": (
        "3f0301010c45a68d357bacdef027fe22ad8156d66b4d668dbe56822a4fd7b90a"
    ),
    "pyproject.toml": ("f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d"),
    "tests/architecture/test_m199_windows_cache_cleanup_readiness_refresh.py": (
        "8a6a3fa32f046c6bd8eb845eff932d03fa715123120355dfbbe619c40d635925"
    ),
    "uv.lock": ("55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18"),
}
_PROTECTED_TREES = {
    "examples": "f1774c37b8002dcd420b6aafe885c8289e2be44300e3d03f88cbcb03a43bc7a0",
    "scripts": "a21166a0d275e9583c39d280c8ca77c016da2048e510970c2601f5250ddefdbf",
    "src/ludoweave": "e6c951393b86b0673a25e0f6b1f4cf41224d3cb7807dd85c76aad482820cde36",
}
_DECISION = _ROOT / "docs/security/windows-cache-cleanup-singleton-link-refusal-policy.md"
_RFC = _ROOT / "docs/rfcs/0183-adopt-windows-singleton-link-refusal-policy.md"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    for candidate in sorted(
        path.rglob("*"),
        key=lambda item: (tuple(part.casefold() for part in item.parts), item.parts),
    ):
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


def _compact(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").casefold().split())


def test_m200_changes_no_runtime_dependency_ci_or_m199_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m200_retains_the_complete_m199_probe_evidence_boundary() -> None:
    architecture_numbers = {
        int(match.group(1))
        for path in (_ROOT / "tests/architecture").glob("test_m*.py")
        if (match := re.match(r"test_m(\d+)_", path.name)) is not None
        and 149 <= int(match.group(1)) <= 198
    }
    integration = sorted((_ROOT / "tests/integration").glob("test_windows_cache_cleanup*.py"))
    security = [
        path
        for path in (_ROOT / "docs/security").glob("cache-cleanup-windows*.md")
        if path.name != "cache-cleanup-windows-readiness-refresh.md"
    ]
    assert architecture_numbers == set(range(149, 199))
    assert len(integration) == 50
    assert len(security) == 50


def test_m200_requires_exact_singleton_link_observations() -> None:
    compact = _compact(_DECISION)
    for required in (
        "retained opened object",
        "handle-derived link count",
        "exactly one link",
        "at admission",
        "immediately before mutation",
        "zero",
        "greater than one",
        "changed",
        "unavailable",
        "invalid",
        "unsupported",
        "refuse before mutation",
    ):
        assert required in compact


def test_m200_rejects_name_enumeration_as_authority() -> None:
    compact = _compact(_DECISION)
    for required in (
        "findfirstfilenamew",
        "pathname-based observation",
        "not authority",
        "do not enumerate hard-link names",
        "necessary but not sufficient",
    ):
        assert required in compact


def test_m200_resolves_only_the_hard_link_policy_criterion() -> None:
    compact = _compact(_DECISION)
    for required in (
        "criterion 2 is resolved as policy",
        "criterion 1 remains unresolved",
        "criteria 3 through 7 remain unresolved",
        "use-time enforcement remains unimplemented",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
    ):
        assert required in compact

    for forbidden in (
        "windows is admitted",
        "cleanup is authorized",
        "production ready",
    ):
        assert forbidden not in compact


def test_m200_rfc_is_accepted_and_direction_preserving() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "no authority increase" in compact
    assert "no production adapter" in compact
    assert "no new hosted allocation" in compact


def test_m200_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-singleton-link-refusal-policy"
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
        assert slug in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0183-adopt-windows-singleton-link-refusal-policy.md" in rfc_index


def test_m200_adds_no_cleanup_command_adapter_or_public_probe() -> None:
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
