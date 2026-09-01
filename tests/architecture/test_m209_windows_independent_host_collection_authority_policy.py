"""Protect M209's independent-host collection-authority policy boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_DECISION = (
    _ROOT / "docs/security/windows-cache-cleanup-independent-host-collection-authority-policy.md"
)
_RFC = _ROOT / "docs/rfcs/0192-adopt-windows-independent-host-collection-authority-policy.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0191-adopt-windows-independent-host-evidence-validator.md": (
        "8f3a05621c0d0c2beb08bc9339cee8e297f4ff7c0feee5d3c91cf2216a637c88"
    ),
    "docs/security/windows-cache-cleanup-independent-host-evidence-validator.md": (
        "ee37286cee8b80bf45053e97e0ff11c661eae90e8d68c7f008d05341c1973453"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m208_windows_independent_host_evidence_validator.py": (
        "217db36e9d4d82deab21b5a11583384225f6ea94bff0c188e6bc7c44689573e0"
    ),
    "tests/fixtures/windows_cleanup_independent_host_evidence.json": (
        "ac326e940e5bc3250b44f5d26dbf1d7592b56edb53c563d374301c9bea3461f8"
    ),
    "tests/integration/test_windows_independent_host_evidence.py": (
        "ea59666b6916e15ad2ededdb0b380ec3f255626ee9d3da337d364c13f4ec6e01"
    ),
    "tests/tools/validate_windows_independent_host_evidence.py": (
        "e320947eb6857f23f8c99a63311fae4458d55daf04facab2d2c92b3d956a27a2"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
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


def _compact(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").casefold().split())


def test_m209_policy_exists() -> None:
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m209_changes_no_runtime_dependency_ci_or_m208_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m209_binds_private_single_run_collection_authority() -> None:
    compact = _compact(_DECISION)
    for required in (
        "trusted offline coordinator",
        "operator-controlled",
        "private",
        "non-serializable",
        "single-run",
        "single-use",
        "host ordinal",
        "profile lane",
        "trial ordinal",
        "barrier ordinal",
        "interruption class",
        "source commit",
        "executable digest",
        "contract digest",
        "cross-principal evidence digest",
        "fixture-recipe digest",
        "capability-profile digest",
        "cannot mint or widen collection authority",
    ):
        assert required in compact


def test_m209_separates_collection_from_cleanup_and_product_authority() -> None:
    compact = _compact(_DECISION)
    for required in (
        "collection authority is not cleanup authority",
        "cannot mint m201 cleanup authority",
        "cannot authorize production cache access",
        "cannot set windows_cleanup_admitted",
        "no canonical world-state mutation",
        "no public runtime api",
        "no cli or mcp command",
    ):
        assert required in compact


def test_m209_denies_live_channels_and_public_runner_attachment() -> None:
    compact = _compact(_DECISION)
    for required in (
        "networking disabled",
        "clipboard redirection disabled",
        "no writable mapped folder",
        "no network listener or network access",
        "must not be attached to a public-repository workflow",
        "self-hosted runner",
        "no github token",
        "ingress completes before the run begins",
        "egress begins only after settlement",
    ):
        assert required in compact


def test_m209_constrains_process_vm_and_physical_interruption_authority() -> None:
    compact = _compact(_DECISION)
    for required in (
        "forced_process_termination",
        "vm_power_cut",
        "physical_host_power_loss",
        "exact spawned participant",
        "must not target an unbound process",
        "equivalent to disconnecting power",
        "no guest shutdown",
        "no checkpoint restore",
        "must not be automated by repository code",
        "physical action remains operator-only",
    ):
        assert required in compact


def test_m209_requires_private_custody_atomic_staging_and_sanitization() -> None:
    compact = _compact(_DECISION)
    for required in (
        "private run manifest",
        "atomic same-volume replacement",
        "sha-256 digest retained separately",
        "chronological custody record",
        "source, creation, transfer, reviewer, and disposition",
        "separate sanitization review",
        "canonical hashes are not authentication",
        "public evidence contains only sanitized classifications",
        "m208 validator",
    ):
        assert required in compact


def test_m209_fails_closed_and_requires_bounded_teardown() -> None:
    compact = _compact(_DECISION)
    for required in (
        "invalidate the affected trial",
        "must not normalize",
        "no live fixture participant or descendant",
        "no open fixture handle",
        "quarantined for operator review",
        "authority expires before export",
        "teardown ambiguity",
        "failed, unsupported, or not_run",
    ):
        assert required in compact


def test_m209_keeps_criteria_and_admission_unresolved() -> None:
    compact = _compact(_DECISION)
    for required in (
        "criteria 6 and 7 remain unresolved",
        "no qualifying run has occurred",
        "windows_cleanup_admitted is false",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
        "m209 does not authorize the privileged harness",
    ):
        assert required in compact
    for forbidden in (
        "criterion 6 is resolved",
        "criterion 7 is resolved",
        "windows is admitted",
        "cleanup is authorized",
        "production ready",
    ):
        assert forbidden not in compact


def test_m209_rfc_is_accepted_and_direction_preserving() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "no executable authority increase" in compact
    assert "no privileged harness" in compact
    assert "no qualifying evidence" in compact
    assert "no new hosted allocation" in compact


def test_m209_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-independent-host-collection-authority-policy"
    for path in (
        "README.md",
        "CHANGELOG.md",
        "ROADMAP.md",
        "SECURITY.md",
        "docs/architecture.md",
        "docs/index.md",
        "mkdocs.yml",
    ):
        assert slug in (_ROOT / path).read_text(encoding="utf-8")
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0192-adopt-windows-independent-host-collection-authority-policy.md" in rfc_index


def test_m209_adds_no_harness_command_native_or_cleanup_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "asset-cache-cleanup",
        "independent-host-collect",
        "windows-host-harness",
        "power-loss-fixture",
    ):
        assert command not in cli

    assert not (_ROOT / "scripts/collect_windows_independent_host_evidence.py").exists()
    names = {path.name for path in (_ROOT / "src/ludoweave/assets").glob("*.py")}
    assert {
        "cleanup.py",
        "cleanup_authority.py",
        "filesystem_adapter.py",
        "independent_host.py",
        "power_loss.py",
        "windows_host_harness.py",
    }.isdisjoint(names)
