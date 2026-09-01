"""Protect M208's offline independent-host evidence-validation boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
from typing import cast

from ludoweave.world import canonical_dumps, canonical_loads

_ROOT = Path(__file__).parents[2]
_VALIDATOR = _ROOT / "tests/tools/validate_windows_independent_host_evidence.py"
_FIXTURE = _ROOT / "tests/fixtures/windows_cleanup_independent_host_evidence.json"
_DECISION = _ROOT / "docs/security/windows-cache-cleanup-independent-host-evidence-validator.md"
_RFC = _ROOT / "docs/rfcs/0191-adopt-windows-independent-host-evidence-validator.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0190-adopt-windows-independent-host-validation-contract.md": (
        "999b84bced5490448cf509bca334eb54b344d39781c7266d240741a490a535c3"
    ),
    "docs/security/windows-cache-cleanup-independent-host-validation-contract.md": (
        "369e68496da25379eca1f3f7a25179b77ee5ce4c547be9bde3bbd11808de0f57"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m207_windows_independent_host_validation_contract.py": (
        "6c43c4f155f945a222d5ceea739a57a6c97926ce03ca75724847fbfe1dbd6b04"
    ),
    "tests/fixtures/windows_cleanup_cross_principal_evidence.json": (
        "b1e20ff9518c52dab5e8251597e5c8344bbca18f81b4ad008c4ac7f5b41cbc9b"
    ),
    "tests/tools/validate_windows_cross_principal_evidence.py": (
        "80586de48d48c4fa1beb0bfa4fc0ba7930fc41ea5048c4e66750de611adf6ca6"
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


def test_m208_changes_no_runtime_dependency_ci_or_prior_evidence_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m208_validator_and_reviewed_fixture_exist() -> None:
    assert _VALIDATOR.is_file()
    assert _FIXTURE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m208_fixture_is_exact_canonical_incomplete_and_digest_bound() -> None:
    encoded = _FIXTURE.read_bytes()
    assert encoded[-1:] != b"\n"
    assert _sha256(_FIXTURE) == "ac326e940e5bc3250b44f5d26dbf1d7592b56edb53c563d374301c9bea3461f8"
    document = cast(dict[str, object], canonical_loads(encoded))
    profiles = cast(list[dict[str, object]], document["profiles"])
    assert canonical_dumps(document) == encoded
    assert document["hosts"] == []
    assert [profile["status"] for profile in profiles] == ["not_run"] * 8
    assert document["cross_principal_evidence_sha256"] == (
        "sha256:b1e20ff9518c52dab5e8251597e5c8344bbca18f81b4ad008c4ac7f5b41cbc9b"
    )
    assert document["criterion_7_satisfied"] is False
    assert document["windows_cleanup_admitted"] is False


def test_m208_validator_has_exact_bounded_schema_and_matrix() -> None:
    source = _VALIDATOR.read_text(encoding="utf-8")
    for required in (
        '"ludoweave.windows-cleanup-independent-host-evidence/1"',
        "_MAX_DOCUMENT_BYTES = 8_388_608",
        "_MAX_HOSTS = 32",
        "_MAX_PROFILE_RESULTS = 128",
        "_MAX_TRIALS = 4_096",
        "_MAX_OBSERVATIONS = 65_536",
        '"local_fixed_ntfs"',
        '"refs_refusal"',
        '"smb_refusal"',
        '"csvfs_refusal"',
        '"cross_volume_refusal"',
        '"unknown_filesystem_refusal"',
        '"missing_capability_refusal"',
        '"file_id_reuse_aba"',
        '"forced_process_termination"',
        '"vm_power_cut"',
        '"physical_host_power_loss"',
    ):
        assert required in source


def test_m208_validator_derives_companion_binding_and_never_admits_windows() -> None:
    source = _VALIDATOR.read_text(encoding="utf-8")
    for required in (
        "validate_cross_principal_evidence_file",
        "cross_summary.evidence_sha256",
        "cross_summary.criterion_6_satisfied",
        '"binding.cross_principal"',
        '"claim.criterion_7"',
        '"claim.windows_cleanup"',
        "windows_cleanup_admitted: bool = False",
    ):
        assert required in source


def test_m208_source_tool_has_no_privileged_or_mutating_import_surface() -> None:
    tree = ast.parse(_VALIDATOR.read_text(encoding="utf-8"))
    imports: set[str] = set()
    calls: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.add(node.func.attr)

    assert imports.isdisjoint(
        {"ctypes", "numpy", "socket", "subprocess", "win32api", "win32security", "wgpu"}
    )
    assert calls.isdisjoint(
        {
            "chmod",
            "link",
            "mkdir",
            "remove",
            "rename",
            "replace",
            "rmdir",
            "symlink_to",
            "unlink",
            "write_bytes",
            "write_text",
        }
    )


def test_m208_documentation_states_exact_false_authority_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "two-file input boundary",
        "separately validated m206 cross-principal document",
        "criterion 6 is derived",
        "all eight profile lanes pass",
        "windows_cleanup_admitted",
        "source-only test tooling",
        "no host coordinator",
        "no qualifying host execution",
        "criterion 6 and criterion 7 remain unresolved",
    ):
        assert required in compact
    for forbidden in (
        "criterion 7 is resolved",
        "windows is admitted",
        "cleanup is authorized",
        "production ready",
    ):
        assert forbidden not in compact


def test_m208_rfc_is_accepted_direction_preserving_and_non_authorizing() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "makes no authority increase" in compact
    assert "no qualifying run" in compact
    assert "no hosted allocation" in compact
    assert "criteria 6 and 7 remain unresolved" in compact


def test_m208_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-independent-host-evidence-validator"
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
    assert "0191-adopt-windows-independent-host-evidence-validator.md" in rfc_index


def test_m208_adds_no_runtime_command_harness_or_cleanup_surface() -> None:
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
