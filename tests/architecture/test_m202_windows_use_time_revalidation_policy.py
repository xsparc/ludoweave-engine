"""Protect M202's Windows use-time revalidation policy boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0184-adopt-windows-cleanup-authority-admission-policy.md": (
        "03e9002da96d6088d23212e710743631bf0625c010c9046e821350f187f0b082"
    ),
    "docs/security/windows-cache-cleanup-authority-admission-policy.md": (
        "f2630ae26b73fba26b79e3d7789059a194db158411ca0980c4b27ccc02842026"
    ),
    "pyproject.toml": ("42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"),
    "tests/architecture/test_m201_windows_cleanup_authority_admission_policy.py": (
        "22e61e51d76e991bdf7c462b3f8cc0ea67c84e6959efa6602085d81839f007a3"
    ),
    "uv.lock": ("e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"),
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
}
_DECISION = _ROOT / "docs/security/windows-cache-cleanup-use-time-revalidation-policy.md"
_RFC = _ROOT / "docs/rfcs/0185-adopt-windows-use-time-revalidation-policy.md"


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


def _compact(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").casefold().split())


def test_m202_changes_no_runtime_dependency_ci_or_m201_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m202_requires_the_same_retained_objects_and_complete_admission_tuple() -> None:
    compact = _compact(_DECISION)
    for required in (
        "same retained handles",
        "effective-token tuple",
        "trusted-root tuple",
        "durable-generation tuple",
        "candidate tuple",
        "exactly equal to admission",
        "no close and reopen",
        "saved observation is not revalidation",
    ):
        assert required in compact


def test_m202_revalidates_effective_token_and_security_at_use() -> None:
    compact = _compact(_DECISION)
    for required in (
        "getcurrentthreadeffectivetoken",
        "token_user",
        "token_statistics",
        "token id",
        "authentication id",
        "modified id",
        "token type",
        "impersonation level",
        "getsecurityinfo",
        "owner sid",
        "non-null dacl",
        "security-descriptor digest",
        "accesscheck",
        "exact least-privilege rights",
        "maximum_allowed",
    ):
        assert required in compact


def test_m202_revalidates_identity_type_links_root_and_generation_at_use() -> None:
    compact = _compact(_DECISION)
    for required in (
        "file_id_info",
        "file_standard_info",
        "file_attribute_tag_info",
        "volume serial number",
        "128-bit file identifier",
        "exactly one link",
        "delete-pending",
        "ordinary non-reparse",
        "handle-relative",
        "no-follow acquisition chain",
        "root relationship",
        "generation-record object identity",
        "complete canonical generation-record sha-256",
        "pathname is not revalidation",
    ):
        assert required in compact


def test_m202_revalidates_immediately_before_every_mutation_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "immediately before every mutation boundary",
        "before the first quarantine or rename",
        "again after quarantine and before deletion",
        "same owning thread",
        "non-reentrant single-owner gate",
        "no callback",
        "no scheduling yield",
        "no blocking wait",
        "no pathname lookup",
        "same retained candidate handle",
        "one check cannot authorize a later mutation",
    ):
        assert required in compact


def test_m202_fails_closed_before_mutation_and_defers_partial_recovery() -> None:
    compact = _compact(_DECISION)
    for required in (
        "missing, changed, ambiguous, mismatched, untrusted, invalid, or unsupported",
        "refuse before the first mutation",
        "candidate remains untouched",
        "recovery-required",
        "must not guess rollback",
        "must not proceed to deletion",
        "criterion 5",
        "typed receipt remains criterion 4",
    ):
        assert required in compact


def test_m202_resolves_only_the_use_time_policy_criterion() -> None:
    compact = _compact(_DECISION)
    for required in (
        "criteria 1 and 2 remain resolved as policy",
        "criterion 3 is resolved as policy",
        "criteria 4 through 7 remain unresolved",
        "getsecurityinfo does not handle race conditions",
        "cross-principal adversarial proof remains criterion 6",
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


def test_m202_rfc_is_accepted_and_direction_preserving() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "no authority increase" in compact
    assert "no production adapter" in compact
    assert "no new hosted allocation" in compact


def test_m202_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-use-time-revalidation-policy"
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
    assert "0185-adopt-windows-use-time-revalidation-policy.md" in rfc_index


def test_m202_adds_no_cleanup_command_adapter_or_public_revalidation_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "asset-cache-cleanup",
        "asset-cache-capabilities",
        "asset-cache-prune",
        "asset-cache-delete",
        "asset-cache-revalidate",
    ):
        assert command not in cli

    names = {path.name for path in (_ROOT / "src/ludoweave/assets").glob("*.py")}
    assert {
        "cleanup.py",
        "cleanup_authority.py",
        "cleanup_capabilities.py",
        "cleanup_revalidation.py",
        "filesystem_adapter.py",
        "garbage_collection.py",
        "retention.py",
    }.isdisjoint(names)
