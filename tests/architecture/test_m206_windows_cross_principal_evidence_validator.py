"""Protect M206's offline Windows cross-principal evidence validator."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import cast

from ludoweave.world import canonical_dumps, canonical_loads

_ROOT = Path(__file__).parents[2]
_VALIDATOR = _ROOT / "tests/tools/validate_windows_cross_principal_evidence.py"
_FIXTURE = _ROOT / "tests/fixtures/windows_cleanup_cross_principal_evidence.json"
_DECISION = _ROOT / "docs/security/windows-cache-cleanup-cross-principal-evidence-validator.md"
_RFC = _ROOT / "docs/rfcs/0189-adopt-windows-cross-principal-evidence-validator.md"
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": (
        "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
    ),
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0188-adopt-windows-cross-principal-validation-contract.md": (
        "35d05528cec153d43547851fe3b9e2305fe714fc2e568b3e1e0213b1bb103604"
    ),
    "docs/security/windows-cache-cleanup-cross-principal-validation-contract.md": (
        "5169f2d7680a4dfb0db48faea006262d8a4049ec48ddcaa093f7edfb76e1e8b6"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "scripts/release_artifacts.py": (
        "d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca"
    ),
    "scripts/smoke_release.py": (
        "9f5a2c1d94255d24f6c5a63621c9bf2e08eea8b6117f0e691832322455f7c6be"
    ),
    "scripts/smoke_wheel.py": ("2727640d8696c9ff67c3f2a7a23af06b89a98d9edc40400696e4a9ed34ce464c"),
    "tests/architecture/test_m205_windows_cross_principal_validation_contract.py": (
        "1a722e1d31c552053606aea14d1462cb7d4c1d0fd88921a6e2ae179baf42af3b"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "src/ludoweave": "a5165f5915dfb8d8eeeb4ee76c171d22d912300227f5eacd33c55435488cf6fb",
}
_LANES = (
    "baseline_denial",
    "acl_flip",
    "owner_dacl_takeover_denial",
    "hard_link_alias",
    "reparse_substitution",
    "rename_substitution",
    "delete_recreate",
    "inherited_handle",
    "duplicate_handle",
    "unrelated_open",
    "cross_session",
    "recovery_tamper",
    "control_channel_failure",
)
_BARRIERS = (
    "before_authority_admission",
    "after_authority_before_intent",
    "after_intent_before_pending",
    "after_quarantine_pending_before_quarantine",
    "after_quarantine_before_quarantined",
    "after_delete_pending_before_deletion",
    "after_deletion_before_deleted",
    "during_recovery_reconciliation",
)


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


def test_m206_preserves_runtime_dependency_ci_release_and_m205_boundaries() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m206_validator_is_offline_read_only_and_canonical() -> None:
    source = _VALIDATOR.read_text(encoding="utf-8")
    for required in (
        "ludoweave.windows-cleanup-cross-principal-evidence/1",
        "canonical_loads",
        "canonical_dumps",
        "JsonLimits",
        "lstat",
        "fstat",
        "S_ISLNK",
        "S_ISREG",
        "st_dev",
        "st_ino",
        "evidence artifact changed while being opened",
        "evidence artifact must use exact canonical bytes",
    ):
        assert required in source


def test_m206_validator_defines_exact_lanes_barriers_and_bounds() -> None:
    source = _VALIDATOR.read_text(encoding="utf-8")
    for item in (*_LANES, *_BARRIERS):
        assert f'"{item}"' in source
    for required in (
        "_MAX_DOCUMENT_BYTES = 4_194_304",
        "_MAX_LANES = 32",
        "_MAX_TRIALS = 512",
        "_MAX_EVENTS = 32_768",
        "max_depth=8",
        "max_nodes=2_048",
        "max_collection_items=256",
        "max_string_bytes=256",
    ):
        assert required in source


def test_m206_validator_enforces_exact_claim_relationships() -> None:
    source = _VALIDATOR.read_text(encoding="utf-8")
    for required in (
        "principal_sid_distinct",
        "authentication_context_distinct",
        "administrator_membership_absent",
        "bypass_privileges_absent",
        "observer_derived",
        "control_channel_authenticated",
        "fixture_confined",
        "teardown_settled",
        "no_out_of_root_mutation",
        "no_unauthorized_deletion_or_restoration",
        "no_canonical_world_state_change",
        "no_leaked_handle",
        "no_live_participant_or_descendant",
        "criterion_6_satisfied",
        "windows_cleanup_admitted",
        "git-sha1:",
        "sha256:",
    ):
        assert required in source


def test_m206_validator_has_a_narrow_import_and_execution_boundary() -> None:
    source = _VALIDATOR.read_text(encoding="utf-8")
    tree = ast.parse(source)
    direct_imports: set[str] = set()
    from_imports: set[str] = set()
    banned_names = {
        "__import__",
        "compile",
        "eval",
        "exec",
        "getattr",
        "globals",
        "input",
        "locals",
        "setattr",
        "vars",
    }
    used_banned_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            direct_imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            from_imports.update(f"{node.module}:{alias.name}" for alias in node.names)
        elif isinstance(node, ast.Name) and node.id in banned_names:
            used_banned_names.add(node.id)

    assert direct_imports == {"argparse"}
    assert from_imports == {
        "__future__:annotations",
        "collections.abc:Mapping",
        "collections.abc:Sequence",
        "dataclasses:dataclass",
        "hashlib:sha256",
        "os:fstat",
        "pathlib:Path",
        "stat:S_ISLNK",
        "stat:S_ISREG",
        "typing:cast",
        "ludoweave.world:JsonLimits",
        "ludoweave.world:canonical_dumps",
        "ludoweave.world:canonical_loads",
    }
    assert used_banned_names == set()
    for forbidden in (
        "ctypes",
        "subprocess",
        "socket",
        "winreg",
        "CreateProcess",
        "LogonUser",
        "DuplicateHandle",
        "Remove-Item",
        "unlink(",
        "write_bytes(",
        "write_text(",
    ):
        assert forbidden not in source


def test_m206_reviewed_fixture_is_canonical_incomplete_and_sanitized() -> None:
    encoded = _FIXTURE.read_bytes()
    decoded = canonical_loads(encoded)
    assert canonical_dumps(decoded) == encoded
    document = cast(dict[str, object], decoded)
    assert document["schema"] == "ludoweave.windows-cleanup-cross-principal-evidence/1"
    assert document["criterion_6_satisfied"] is False
    assert document["windows_cleanup_admitted"] is False
    assert document["source_commit"] is None
    assert document["executable_sha256"] is None
    lanes = cast(list[dict[str, object]], document["lanes"])
    assert tuple(lane["id"] for lane in lanes) == _LANES
    assert all(lane["status"] == "not_run" for lane in lanes)
    assert all(lane["trial_count"] == lane["event_count"] == 0 for lane in lanes)
    assert b"\n" not in encoded
    for forbidden in (
        b"account_name",
        b"domain",
        b'"principal_sid":',
        b"token_id",
        b"authentication_id",
        b"session_id",
        b"pid",
        b"path",
        b"handle_value",
        b"acl_bytes",
        b"environment",
        b"platform_error",
        b"credential",
        b"password",
        b"secret",
    ):
        assert forbidden not in encoded.lower()


def test_m206_decision_defines_validity_without_admission() -> None:
    compact = _compact(_DECISION)
    for required in (
        "structurally valid does not mean criterion 6 satisfied",
        "one exact canonical json object",
        "duplicate fields, unknown fields, noncanonical bytes, and non-finite numbers are rejected",
        "regular non-symbolic-link file",
        "before and after open identity and size",
        "all 13 mandatory lanes in canonical order",
        "all eight barrier identities",
        "passed, failed, unsupported, not_run, and not_applicable",
        "only an all-passed complete document can set criterion_6_satisfied true",
        "windows_cleanup_admitted must remain false",
        "reviewed fixture is intentionally all not_run",
        "m206 does not resolve criterion 6",
        "no qualifying cross-principal run has occurred",
        "no credential or account lifecycle",
        "no new hosted allocation",
    ):
        assert required in compact


def test_m206_rfc_is_accepted_direction_preserving_and_source_only() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "**Milestone:** M206" in rfc
    assert "direction-preserving" in compact
    assert "source-only" in compact
    assert "no authority increase" in compact
    assert "no qualifying evidence" in compact
    assert "no new hosted allocation" in compact


def test_m206_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-cross-principal-evidence-validator"
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
    assert "0189-adopt-windows-cross-principal-evidence-validator.md" in (
        _ROOT / "docs/rfcs/index.md"
    ).read_text(encoding="utf-8")


def test_m206_adds_no_runtime_command_launcher_or_cleanup_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "cross-principal-evidence",
        "cross-principal-validate",
        "principal-launcher",
        "asset-cache-cleanup",
    ):
        assert command not in cli
    assert not (_ROOT / "src/ludoweave/assets/cleanup.py").exists()
    assert not (_ROOT / "src/ludoweave/assets/principal_launcher.py").exists()


def test_m206_keeps_criterion_6_and_windows_admission_unresolved() -> None:
    for path in (_DECISION, _RFC):
        compact = _compact(path)
        for required in (
            "criterion 6 remains unresolved",
            "windows is not admitted",
            "cleanup remains unimplemented and unauthorized",
        ):
            assert required in compact
        for forbidden in (
            "criterion 6 is resolved",
            "windows is admitted",
            "cleanup is authorized",
            "production ready",
        ):
            assert forbidden not in compact


def test_m206_fixture_is_strict_json_without_duplicate_keys() -> None:
    def reject_duplicate(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate field")
            result[key] = value
        return result

    decoded = json.loads(
        _FIXTURE.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
    )
    assert isinstance(decoded, dict)
