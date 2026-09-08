"""Protect M207's Windows independent-host validation contract boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "67fc471f84d7dde8b239bd9e92235a34f780cc3d3370b0dbf451e6a922a027f1"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0189-adopt-windows-cross-principal-evidence-validator.md": (
        "52daaccab653cb6c9c80cb43ca547573994af5476e6e7340993f6f050104270d"
    ),
    "docs/security/windows-cache-cleanup-cross-principal-evidence-validator.md": (
        "77d6de16d50c1c773a9536f0a1838dc8442e1cb4b2edef82a48d92f119ac462e"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m206_windows_cross_principal_evidence_validator.py": (
        "71796835eb0376b89546d9f35169b0ca36f774150afec6c1e1cf92699a173ccb"
    ),
    "tests/fixtures/windows_cleanup_cross_principal_evidence.json": (
        "b1e20ff9518c52dab5e8251597e5c8344bbca18f81b4ad008c4ac7f5b41cbc9b"
    ),
    "tests/tools/validate_windows_cross_principal_evidence.py": (
        "80586de48d48c4fa1beb0bfa4fc0ba7930fc41ea5048c4e66750de611adf6ca6"
    ),
    "uv.lock": "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18",
}
_PROTECTED_TREES = {
    "examples": "8e8d3a618b8bb14c439d4c0809db345fe471dc7c07f1765b03c4bb507f8fc98a",
    "scripts": "8833e1120f60e74f4b5024ef6a6049821a72afef44c0143bab3f7bbd9298e247",
    "src/ludoweave": "1e7f21b3d5bb0a8021f47f9bf1089873a59cb3e798b02933569d3eee3c9a35c1",
}
_DECISION = _ROOT / "docs/security/windows-cache-cleanup-independent-host-validation-contract.md"
_RFC = _ROOT / "docs/rfcs/0190-adopt-windows-independent-host-validation-contract.md"


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


def test_m207_changes_no_runtime_dependency_ci_or_m206_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m207_requires_genuinely_independent_hosts() -> None:
    compact = _compact(_DECISION)
    for required in (
        "at least two independently provisioned windows hosts",
        "distinct operating-system installation",
        "distinct boot instance",
        "distinct storage instance",
        "two processes on one host do not qualify",
        "two sessions on one host do not qualify",
        "a container does not qualify",
        "a reboot of one host does not qualify",
        "clones resumed from one vm snapshot do not qualify",
        "observer-attested independence",
    ):
        assert required in compact


def test_m207_requires_observed_capability_profiles() -> None:
    compact = _compact(_DECISION)
    for required in (
        "windows release class",
        "filesystem family",
        "filesystem version class",
        "volume capability flags",
        "local or remote classification",
        "same-volume relationship",
        "file-id scope",
        "persistence class",
        "capabilities are observed, not inferred",
        "getvolumeinformationw",
        "file_supports_hard_links",
        "file_supports_reparse_points",
        "file_supports_open_by_file_id",
    ):
        assert required in compact


def test_m207_defines_the_complete_host_and_refusal_matrix() -> None:
    compact = _compact(_DECISION)
    for lane in (
        "local_fixed_ntfs",
        "refs_refusal",
        "smb_refusal",
        "csvfs_refusal",
        "cross_volume_refusal",
        "unknown_filesystem_refusal",
        "missing_capability_refusal",
        "file_id_reuse_aba",
    ):
        assert lane in compact
    for required in (
        "copy/delete fallback is forbidden",
        "safe refusal must be observed",
        "unsupported is not a passing refusal",
        "no substitute profile",
        "allocation pressure without observed reuse is unsupported evidence",
    ):
        assert required in compact


def test_m207_separates_interruption_and_durability_classes() -> None:
    compact = _compact(_DECISION)
    for required in (
        "forced_process_termination",
        "vm_power_cut",
        "physical_host_power_loss",
        "graceful close is not interruption evidence",
        "a vm power cut is not physical-host power-loss evidence",
        "a successful flush call is not sufficient proof",
        "restart and recovery reconciliation",
        "no unsafe external mutation",
    ):
        assert required in compact


def test_m207_evidence_is_bounded_identity_bound_and_sanitized() -> None:
    compact = _compact(_DECISION)
    for required in (
        "ludoweave.windows-cleanup-independent-host-evidence/1",
        "one bounded canonical json object",
        "maximum 32 host results",
        "maximum 128 profile results",
        "maximum 65,536 observations",
        "maximum 8,388,608 bytes",
        "source commit",
        "executable digest",
        "contract digest",
        "cross-principal evidence digest",
        "no hostname, machine identifier, volume serial number, file identifier, account name, sid, path, environment value, credential, or platform error text",
        "canonical hashes are not authentication",
    ):
        assert required in compact


def test_m207_keeps_admission_fail_closed_and_unresolved() -> None:
    compact = _compact(_DECISION)
    for required in (
        "passed, failed, unsupported, or not_run",
        "failed, unsupported, or not_run keeps criterion 7 unresolved",
        "criterion 6 must already be satisfied",
        "criterion 7 remains unresolved",
        "m207 does not resolve criterion 7",
        "windows_cleanup_admitted is false",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
    ):
        assert required in compact
    for forbidden in (
        "criterion 7 is resolved",
        "windows is admitted",
        "cleanup is authorized",
        "production ready",
    ):
        assert forbidden not in compact


def test_m207_keeps_evidence_collection_offline_and_operator_controlled() -> None:
    compact = _compact(_DECISION)
    for required in (
        "operator-controlled hosts",
        "offline evidence collection",
        "must not be attached to a public-repository workflow",
        "no credential or account secret enters the repository",
        "no network listener or network access",
        "public evidence contains only sanitized classifications",
    ):
        assert required in compact


def test_m207_rfc_is_accepted_and_direction_preserving() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "no authority increase" in compact
    assert "no implementation or validator" in compact
    assert "no qualifying evidence" in compact
    assert "no new hosted allocation" in compact


def test_m207_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-independent-host-validation-contract"
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
    assert "0190-adopt-windows-independent-host-validation-contract.md" in rfc_index


def test_m207_adds_no_host_harness_validator_or_cleanup_runtime_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "asset-cache-cleanup",
        "independent-host-validate",
        "windows-host-harness",
        "power-loss-fixture",
    ):
        assert command not in cli

    assert not (_ROOT / "scripts/validate_windows_independent_host_evidence.py").exists()
    names = {path.name for path in (_ROOT / "src/ludoweave/assets").glob("*.py")}
    assert {
        "cleanup.py",
        "cleanup_recovery.py",
        "filesystem_adapter.py",
        "independent_host.py",
        "power_loss.py",
        "windows_host_harness.py",
    }.isdisjoint(names)
