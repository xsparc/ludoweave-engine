"""Protect M205's Windows cross-principal validation contract boundary."""

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
    "docs/rfcs/0187-adopt-windows-cleanup-durable-recovery-policy.md": (
        "2250e4f6e16095eb00094998d098255c16cc859e4e3b080e3e3ef5f5f245452a"
    ),
    "docs/security/windows-cache-cleanup-durable-recovery-policy.md": (
        "bacaf5d4119b73e1b8188cec71e2a5c8b4b91403c218cb43869d7e170c39f0c0"
    ),
    "pyproject.toml": "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1",
    "tests/architecture/test_m204_windows_cleanup_durable_recovery_policy.py": (
        "c2634282a787f7412bcf93087cfcab463d9d98ef021482349b528f62fc507dbf"
    ),
    "uv.lock": "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed",
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "a5165f5915dfb8d8eeeb4ee76c171d22d912300227f5eacd33c55435488cf6fb",
}
_DECISION = _ROOT / "docs/security/windows-cache-cleanup-cross-principal-validation-contract.md"
_RFC = _ROOT / "docs/rfcs/0188-adopt-windows-cross-principal-validation-contract.md"


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


def test_m205_changes_no_runtime_dependency_ci_or_m204_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m205_requires_a_genuinely_distinct_untrusted_principal() -> None:
    compact = _compact(_DECISION)
    for required in (
        "genuinely distinct untrusted local principal",
        "token_user sid must differ",
        "independently authenticated logon context",
        "token id, authentication id, and modified id",
        "primary token",
        "session id",
        "not the trusted-root owner",
        "not a member of administrators",
        "administrative bypass privileges",
    ):
        assert required in compact


def test_m205_rejects_same_principal_surrogates() -> None:
    compact = _compact(_DECISION)
    for required in (
        "restricted copy of the trusted token does not qualify",
        "integrity-level change does not qualify",
        "same-user appcontainer does not qualify",
        "same sid in another logon session does not qualify",
        "impersonation of the trusted sid does not qualify",
        "github-hosted administrator account does not qualify",
    ):
        assert required in compact


def test_m205_keeps_credentials_and_account_lifecycle_outside_the_repository() -> None:
    compact = _compact(_DECISION)
    for required in (
        "operator-provisioned",
        "private engine-owned launcher authority",
        "never accepts a username, password, credential, token value, or account secret",
        "must not create, delete, enable, disable, or modify an account",
        "must not change group membership, logon rights, or local security policy",
        "credentials never enter environment variables, files, command lines, logs, evidence, or ci secrets",
    ):
        assert required in compact


def test_m205_confines_every_lane_to_a_disposable_fixture() -> None:
    compact = _compact(_DECISION)
    for required in (
        "disposable fixture root",
        "outside the repository, workspace, user profile, and production cache",
        "ordinary non-reparse directory",
        "same local volume",
        "root sentinel",
        "exact cleanup confinement",
        "no network listener or network access",
    ):
        assert required in compact


def test_m205_requires_unrelated_process_and_session_topologies() -> None:
    compact = _compact(_DECISION)
    for required in (
        "trusted coordinator",
        "trusted engine process",
        "unrelated hostile process",
        "separate process tree",
        "separate authenticated logon context",
        "separate windows session lane",
        "parent-owned cooperation is not proof",
        "no inherited cleanup handle",
        "no arbitrary shell, script, or evaluation",
    ):
        assert required in compact


def test_m205_requires_explicit_handle_leakage_evidence() -> None:
    compact = _compact(_DECISION)
    for required in (
        "explicit handle inventory",
        "zero unlisted inheritable handles",
        "proc_thread_attribute_handle_list",
        "no root, candidate, quarantine, recovery-store, token, process, or job handle",
        "cross-session lane cannot rely on handle inheritance",
        "duplicatehandle attempts",
        "same object and access rights",
    ):
        assert required in compact


def test_m205_defines_the_complete_mandatory_lane_matrix() -> None:
    compact = _compact(_DECISION)
    for lane in (
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
    ):
        assert lane in compact


def test_m205_uses_deterministic_barriers_not_timing_luck() -> None:
    compact = _compact(_DECISION)
    for required in (
        "deterministic barrier schedule",
        "sleep, polling luck, and elapsed-time overlap are not proof",
        "before authority admission",
        "after authority admission but before intent",
        "after intent but before a pending record",
        "after quarantine_pending but before quarantine",
        "after quarantine but before quarantined",
        "after delete_pending but before deletion",
        "after deletion but before deleted",
        "during recovery reconciliation",
        "adversary-first and engine-first release orders",
        "bounded timeout and settlement",
    ):
        assert required in compact


def test_m205_requires_acl_and_actual_access_evidence() -> None:
    compact = _compact(_DECISION)
    for required in (
        "root, candidate, quarantine, recovery-store, and generation security",
        "owner, dacl, and security-descriptor control flags",
        "explicit, inherited, and protected dacl",
        "null dacl is forbidden",
        "delete, file_delete_child, write_dac, write_owner, file_write_attributes, file_add_file, and file_add_subdirectory",
        "actual allowed or denied operation result",
        "lane-specific delegated rights are not production authority",
        "revalidate after every acl transition",
    ):
        assert required in compact


def test_m205_requires_real_alias_reparse_and_identity_races() -> None:
    compact = _compact(_DECISION)
    for required in (
        "real same-volume hard link",
        "real reparse point",
        "path-string simulation is not evidence",
        "retained handles",
        "volume and file identity",
        "link count",
        "reparse tag",
        "root relationship",
        "unsupported creation capability keeps the lane unsupported",
    ):
        assert required in compact


def test_m205_defines_fail_closed_lane_outcomes() -> None:
    compact = _compact(_DECISION)
    for required in (
        "operating system denies the hostile action",
        "engine refuses before an unsafe effect",
        "recovery_required before another effect",
        "no out-of-root mutation",
        "no unauthorized deletion or restoration",
        "no canonical world-state change",
        "no leaked handle",
        "no participant or descendant remains alive",
        "passed, failed, unsupported, or not_run",
        "unsupported, not_run, or failed mandatory lane keeps criterion 6 unresolved",
    ):
        assert required in compact


def test_m205_evidence_is_bounded_canonical_and_sanitized() -> None:
    compact = _compact(_DECISION)
    for required in (
        "ludoweave.windows-cleanup-cross-principal-evidence/1",
        "maximum 32 lanes",
        "maximum 512 trials",
        "maximum 32,768 events",
        "maximum 4,194,304 bytes",
        "one complete canonical json object",
        "principal_sid_distinct",
        "authentication_context_distinct",
        "administrator_membership_absent",
        "bypass_privileges_absent",
        "no account name, domain, sid, token identifier, authentication identifier, session identifier, pid, path, handle, acl bytes, environment value, or platform error text",
        "canonical hashes are not authentication",
    ):
        assert required in compact


def test_m205_identity_is_observer_derived_not_self_asserted() -> None:
    compact = _compact(_DECISION)
    for required in (
        "participant self-report is not identity evidence",
        "coordinator-owned process and token handles",
        "query the effective token of each participant",
        "bind the exact executable digest",
        "bind the source commit",
        "authenticated local control channel",
        "exact principal-scoped dacl",
        "fresh unpredictable challenge",
        "does not prove public artifact authenticity",
    ):
        assert required in compact


def test_m205_teardown_preserves_operator_account_ownership() -> None:
    compact = _compact(_DECISION)
    for required in (
        "operator retains account and credential lifecycle ownership",
        "bounded participant and descendant settlement",
        "close every owned handle",
        "verify the exact root sentinel",
        "reparse-free teardown walk",
        "must not restore an external acl",
        "preserve the fixture on ambiguous teardown",
        "path-free failure evidence",
    ):
        assert required in compact


def test_m205_does_not_claim_criterion_6_evidence_or_windows_admission() -> None:
    compact = _compact(_DECISION)
    for required in (
        "criteria 1 through 5 are resolved as policy",
        "criteria 6 and 7 remain unresolved",
        "m205 does not resolve criterion 6",
        "no qualifying cross-principal run has occurred",
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


def test_m205_rfc_is_accepted_and_direction_preserving() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "no authority increase" in compact
    assert "no production adapter" in compact
    assert "no qualifying evidence" in compact
    assert "no new hosted allocation" in compact


def test_m205_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-cross-principal-validation-contract"
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
    assert "0188-adopt-windows-cross-principal-validation-contract.md" in rfc_index


def test_m205_adds_no_principal_launcher_or_cleanup_runtime_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "asset-cache-cleanup",
        "asset-cache-adversary",
        "cross-principal-validate",
        "principal-launcher",
    ):
        assert command not in cli

    names = {path.name for path in (_ROOT / "src/ludoweave/assets").glob("*.py")}
    assert {
        "cleanup.py",
        "cleanup_adversary.py",
        "cleanup_cross_principal.py",
        "cleanup_recovery.py",
        "credential_broker.py",
        "filesystem_adapter.py",
        "principal_launcher.py",
        "quarantine.py",
        "recovery.py",
        "windows_accounts.py",
    }.isdisjoint(names)
