"""Protect M204's Windows cleanup durable recovery policy boundary."""

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
    "docs/rfcs/0186-adopt-windows-cleanup-protocol-receipt-policy.md": (
        "63283cb877425cabc23aef5ff8f00af7d51e39f0bf436e8da9cf11c6073793ca"
    ),
    "docs/security/windows-cache-cleanup-protocol-receipt-policy.md": (
        "53e40f10669ba9b2bd7062744f7aea7ab894a17af0cd99f864c44d2d40b6d905"
    ),
    "pyproject.toml": ("42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"),
    "tests/architecture/test_m203_windows_cleanup_protocol_receipt_policy.py": (
        "5524ae15a5aa6dad71e991a85221514748ed4c2e19b7bc25373e603a6fa1aa1d"
    ),
    "uv.lock": ("e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"),
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "a5165f5915dfb8d8eeeb4ee76c171d22d912300227f5eacd33c55435488cf6fb",
}
_DECISION = _ROOT / "docs/security/windows-cache-cleanup-durable-recovery-policy.md"
_RFC = _ROOT / "docs/rfcs/0187-adopt-windows-cleanup-durable-recovery-policy.md"


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


def test_m204_changes_no_runtime_dependency_ci_or_m203_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m204_uses_one_private_root_confined_recovery_store() -> None:
    compact = _compact(_DECISION)
    for required in (
        "one active cleanup operation per trusted root and generation",
        "private recovery store is root-confined",
        "ordinary non-reparse directory",
        "same volume",
        "not canonical world state",
        "cannot mint authority",
        "terminal history remains for the life of the generation",
    ):
        assert required in compact


def test_m204_records_are_bounded_immutable_and_hash_chained() -> None:
    compact = _compact(_DECISION)
    for required in (
        "ludoweave.windows-cleanup-recovery-record/1",
        "maximum 1,024 candidates",
        "maximum 4,098 committed records",
        "maximum 65,536 bytes per record",
        "maximum 67,108,864 committed bytes",
        "sequence starts at zero",
        "previous_record_sha256",
        "canonical sha-256",
        "no gap, duplicate, branch, rewrite, truncation, or replacement",
    ):
        assert required in compact


def test_m204_requires_a_verified_durable_publish_sequence() -> None:
    compact = _compact(_DECISION)
    for required in (
        "exclusive create of one unique staging record",
        "write the exact canonical bytes",
        "flush record contents and metadata",
        "no-replace same-directory publish",
        "settle the parent metadata",
        "reopen through the retained recovery-store handle",
        "only then is the phase durable",
        "replacefile is forbidden",
        "transactional ntfs is forbidden",
        "unsupported durability refuses before acknowledgement or mutation",
    ):
        assert required in compact


def test_m204_defines_write_ahead_phase_ordering() -> None:
    compact = _compact(_DECISION)
    for required in (
        "intent_durable",
        "quarantine_pending",
        "quarantined",
        "delete_pending",
        "restore_pending",
        "deleted",
        "restored",
        "completed",
        "quarantine_pending must be durable before quarantine",
        "delete_pending must be durable before deletion",
        "restore_pending must be durable before restoration",
        "completed is durable only after every candidate is terminal",
    ):
        assert required in compact


def test_m204_binds_acknowledgement_and_receipt_to_durable_state() -> None:
    compact = _compact(_DECISION)
    for required in (
        "accepted acknowledgement is forbidden before intent_durable",
        "durable replay lookup",
        "last durable phase",
        "none, intent_durable, quarantine_pending, quarantined, delete_pending, restore_pending, deleted, restored, or completed",
        "unchanged, quarantined, deleted, restored, or recovery_required",
        "completed receipt is forbidden before completed is durable",
        "no exactly-once claim",
    ):
        assert required in compact


def test_m204_quarantine_is_same_handle_same_volume_and_no_replace() -> None:
    compact = _compact(_DECISION)
    for required in (
        "same retained candidate handle",
        "retained quarantine-directory handle",
        "equal volume identity",
        "engine-generated private slot",
        "target slot must not exist",
        "no replace",
        "no copy/delete fallback",
        "movefile_copy_allowed is forbidden",
        "verify the same candidate identity after rename",
    ):
        assert required in compact


def test_m204_recovery_is_bounded_reconciled_and_idempotent() -> None:
    compact = _compact(_DECISION)
    for required in (
        "reconcile before applying an effect",
        "fresh private recovery authority",
        "same operation_id and request_sha256",
        "never repeat an already observed transition",
        "original exact and quarantine absent",
        "original absent and quarantine exact",
        "both present",
        "both absent",
        "recovery_required",
        "new cleanup requests refuse while recovery is unresolved",
    ):
        assert required in compact


def test_m204_restore_and_rollback_have_a_strict_commit_boundary() -> None:
    compact = _compact(_DECISION)
    for required in (
        "restore is permitted only before delete_pending",
        "original slot must be absent",
        "same retained quarantined object",
        "restore never overwrites",
        "after delete_pending, automatic rollback is forbidden",
        "must not guess rollback",
    ):
        assert required in compact


def test_m204_tamper_blocks_the_root_without_automatic_repair() -> None:
    compact = _compact(_DECISION)
    for required in (
        "invalid record chain",
        "unknown committed or staging entry",
        "owner, dacl, root, or generation mismatch",
        "identity, link, type, reparse, or delete-state mismatch",
        "block cleanup for the entire root and generation",
        "preserve records and quarantined objects",
        "no automatic journal repair, deletion, or restoration",
        "canonical hashes are not authentication",
    ):
        assert required in compact


def test_m204_defines_crash_and_power_loss_disposition() -> None:
    compact = _compact(_DECISION)
    for required in (
        "before intent_durable",
        "after intent_durable",
        "after quarantine_pending",
        "after quarantine but before quarantined",
        "after delete_pending but before deleted",
        "after deleted but before completed",
        "delivery remains unknown",
        "does not report completed from absence alone",
    ):
        assert required in compact


def test_m204_resolves_only_the_durable_recovery_policy_criterion() -> None:
    compact = _compact(_DECISION)
    for required in (
        "criteria 1 through 5 are resolved as policy",
        "criterion 5 is resolved as policy",
        "criteria 6 and 7 remain unresolved",
        "windows is not admitted",
        "cleanup remains unimplemented and unauthorized",
    ):
        assert required in compact
    for forbidden in ("windows is admitted", "cleanup is authorized", "production ready"):
        assert forbidden not in compact


def test_m204_rfc_is_accepted_and_direction_preserving() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "no authority increase" in compact
    assert "no production adapter" in compact
    assert "no new hosted allocation" in compact


def test_m204_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-durable-recovery-policy"
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
    assert "0187-adopt-windows-cleanup-durable-recovery-policy.md" in rfc_index


def test_m204_adds_no_cleanup_recovery_command_adapter_or_runtime_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "asset-cache-cleanup",
        "asset-cache-recover",
        "asset-cache-restore",
        "asset-cache-finalize",
        "asset-cache-reconcile",
    ):
        assert command not in cli

    names = {path.name for path in (_ROOT / "src/ludoweave/assets").glob("*.py")}
    assert {
        "cleanup.py",
        "cleanup_authority.py",
        "cleanup_journal.py",
        "cleanup_protocol.py",
        "cleanup_receipt.py",
        "cleanup_recovery.py",
        "cleanup_revalidation.py",
        "filesystem_adapter.py",
        "garbage_collection.py",
        "quarantine.py",
        "recovery.py",
        "retention.py",
    }.isdisjoint(names)
