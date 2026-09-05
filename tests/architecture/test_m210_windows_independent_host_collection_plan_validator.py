"""Protect M210's offline independent-host collection-plan boundary."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
from typing import cast

from ludoweave.world import canonical_dumps, canonical_loads

_ROOT = Path(__file__).parents[2]
_VALIDATOR = _ROOT / "tests/tools/validate_windows_independent_host_collection_plan.py"
_FIXTURE = _ROOT / "tests/fixtures/windows_cleanup_independent_host_collection_plan.json"
_DECISION = (
    _ROOT / "docs/security/windows-cache-cleanup-independent-host-collection-plan-validator.md"
)
_RFC = _ROOT / "docs/rfcs/0193-adopt-windows-independent-host-collection-plan-validator.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0192-adopt-windows-independent-host-collection-authority-policy.md": (
        "df48a04fa815de5c4b8d1d002a230e16e9cc9f69a64382ac06d16eeb1fce9899"
    ),
    "docs/security/windows-cache-cleanup-independent-host-collection-authority-policy.md": (
        "205ca4fa0d6f8f5bb69a80e123b349684b52bb7450a379b8ea47eaf06ae3dcc0"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m209_windows_independent_host_collection_authority_policy.py": (
        "d0c9b2b54e82df9008b5d2d4d104ec111c6f75c4187d7bef548cb6bbe4c292c3"
    ),
    "tests/fixtures/windows_cleanup_independent_host_evidence.json": (
        "ac326e940e5bc3250b44f5d26dbf1d7592b56edb53c563d374301c9bea3461f8"
    ),
    "tests/tools/validate_windows_independent_host_evidence.py": (
        "e320947eb6857f23f8c99a63311fae4458d55daf04facab2d2c92b3d956a27a2"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "a5165f5915dfb8d8eeeb4ee76c171d22d912300227f5eacd33c55435488cf6fb",
}


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


def test_m210_changes_no_runtime_dependency_ci_or_m209_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m210_source_only_validator_boundary_exists() -> None:
    assert _VALIDATOR.is_file()
    assert _FIXTURE.is_file()
    assert _DECISION.is_file()
    assert _RFC.is_file()


def test_m210_fixture_is_exact_canonical_incomplete_and_non_authorizing() -> None:
    encoded = _FIXTURE.read_bytes()
    document = cast(dict[str, object], canonical_loads(encoded))
    assert canonical_dumps(document) + b"\n" == encoded
    assert _sha256(_FIXTURE) == "c9c8e2f082583d4458d6a7a0b56d34c5d373149d15e3e9ca9528a5bdc915e8c6"
    assert document["hosts"] == []
    assert document["collection_status"] == "not_run"
    assert document["plan_complete"] is False
    assert document["authority_issued"] is False
    assert document["criterion_6_satisfied"] is False
    assert document["criterion_7_satisfied"] is False
    assert document["windows_cleanup_admitted"] is False


def test_m210_validator_has_exact_bounded_closed_matrix() -> None:
    source = _VALIDATOR.read_text(encoding="utf-8")
    for required in (
        '"ludoweave.windows-cleanup-independent-host-collection-plan/1"',
        "_MAX_DOCUMENT_BYTES = 1_048_576",
        "_MAX_HOSTS = 32",
        '"local_fixed_ntfs"',
        '"file_id_reuse_aba"',
        '"before_authority_admission"',
        '"during_recovery_reconciliation"',
        '"forced_process_termination"',
        '"vm_power_cut"',
        '"physical_host_power_loss"',
        '"other_supported"',
        '"observe_revalidate"',
        '"stage_artifact"',
    ):
        assert required in source


def test_m210_validator_derives_completeness_and_forces_false_claims() -> None:
    source = _VALIDATOR.read_text(encoding="utf-8")
    for required in (
        "derived_complete =",
        "host_count * len(_PROFILES) * len(_BARRIERS) * len(_INTERRUPTIONS)",
        'code="claim.plan_complete"',
        'code="claim.authority"',
        'code="claim.criterion_6"',
        'code="claim.criterion_7"',
        'code="claim.windows_cleanup"',
        "authority_issued: bool = False",
        "windows_cleanup_admitted: bool = False",
    ):
        assert required in source


def test_m210_source_tool_has_no_privileged_mutating_or_network_surface() -> None:
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
        {
            "ctypes",
            "http",
            "multiprocessing",
            "numpy",
            "socket",
            "subprocess",
            "urllib",
            "win32api",
            "win32job",
            "win32process",
            "win32security",
            "wgpu",
        }
    )
    assert calls.isdisjoint(
        {
            "chmod",
            "kill",
            "link",
            "mkdir",
            "remove",
            "rename",
            "replace",
            "rmdir",
            "symlink_to",
            "terminate",
            "unlink",
            "write_bytes",
            "write_text",
        }
    )


def test_m210_documentation_states_exact_false_authority_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "structural companion to the future private run manifest",
        "presence and syntax establish only structural completeness",
        "complete plan is still not executable authority",
        "stable identifiers are not schema fields",
        "`collection_status` is required to remain `not_run`",
        "source-only under `tests/tools`",
        "no qualifying run has occurred",
        "criteria 6 and 7 remain unresolved",
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


def test_m210_rfc_is_accepted_direction_preserving_and_non_authorizing() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "makes no executable authority increase" in compact
    assert "not an authority object" in compact
    assert "no qualifying evidence" in compact
    assert "zero github actions jobs or hosted allocation" in compact


def test_m210_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-independent-host-collection-plan-validator"
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
    assert "0193-adopt-windows-independent-host-collection-plan-validator.md" in rfc_index


def test_m210_adds_no_runtime_command_harness_or_cleanup_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "asset-cache-cleanup",
        "independent-host-collect",
        "collection-plan-validate",
        "windows-host-harness",
        "power-loss-fixture",
    ):
        assert command not in cli

    assert not (_ROOT / "scripts/validate_windows_independent_host_collection_plan.py").exists()
    names = {path.name for path in (_ROOT / "src/ludoweave/assets").glob("*.py")}
    assert {
        "cleanup.py",
        "collection_authority.py",
        "filesystem_adapter.py",
        "independent_host.py",
        "power_loss.py",
        "windows_host_harness.py",
    }.isdisjoint(names)
