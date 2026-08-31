"""Protect M203's Windows cleanup protocol and receipt policy boundary."""

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
    "docs/rfcs/0185-adopt-windows-use-time-revalidation-policy.md": (
        "e659ea692cde436d16386d4290cde759b8cd54bcbd261007d87f8fcb93999bf7"
    ),
    "docs/security/windows-cache-cleanup-use-time-revalidation-policy.md": (
        "05ec78b85022321438ba22c0342ee9bafee9f64a8ebc59c61c00967cd35d2c84"
    ),
    "pyproject.toml": ("42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"),
    "tests/architecture/test_m202_windows_use_time_revalidation_policy.py": (
        "c5952f86de27703fad5de346a8c01ae2eb91e0ea505dd2d2953c55bdcc694071"
    ),
    "uv.lock": ("e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"),
}
_PROTECTED_TREES = {
    "examples": "af497a33b643d066314f3de8497aeaeeb028379cf0764ce769a8df15c15f8d30",
    "scripts": "1473e489e474a863c379d66f5cb35930c2ffabed872deee4c6bad635d4befaa6",
    "src/ludoweave": "6434a67931fabd685a34fc8b4130091d06b4de04fdf21517c35b638b78efd66c",
}
_DECISION = _ROOT / "docs/security/windows-cache-cleanup-protocol-receipt-policy.md"
_RFC = _ROOT / "docs/rfcs/0186-adopt-windows-cleanup-protocol-receipt-policy.md"


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


def test_m203_changes_no_runtime_dependency_ci_or_m202_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m203_uses_a_distinct_versioned_cleanup_protocol_family() -> None:
    compact = _compact(_DECISION)
    for required in (
        "ludoweave.asset-cache-cleanup.request/1",
        "ludoweave.asset-cache-cleanup.acknowledgement/1",
        "ludoweave.asset-cache-cleanup.receipt/1",
        "distinct from ludoweave.command/1",
        "distinct from ludoweave.transaction/1",
        "distinct from ludoweave.receipt/1",
        "world transaction receipt cannot represent cleanup",
    ):
        assert required in compact


def test_m203_requires_one_bounded_complete_canonical_document() -> None:
    compact = _compact(_DECISION)
    for required in (
        "one complete canonical json object",
        "utf-8 byte slice",
        "declared byte length",
        "request: 16,384 bytes",
        "acknowledgement: 8,192 bytes",
        "receipt: 1,048,576 bytes",
        "maximum depth 32",
        "maximum 100,000 nodes",
        "maximum 262,144 utf-8 string bytes",
        "maximum 1,024 outcomes",
        "maximum 64 diagnostics",
        "byte order mark",
        "trailing bytes",
        "duplicate keys",
        "unknown fields",
        "json text sequence",
        "batch",
        "notification",
        "partial parse",
    ):
        assert required in compact


def test_m203_request_is_attribution_only_and_cannot_select_targets() -> None:
    compact = _compact(_DECISION)
    for required in (
        "exact request fields are protocol, request_id, operation_id, actor, intent, and dry_run",
        "intent is exactly asset_cache_cleanup",
        "actor attribution is not authentication",
        "request contains no path",
        "no candidate identifier",
        "request cannot mint authority",
        "trusted composition root",
        "dry_run cannot authorize mutation",
    ):
        assert required in compact


def test_m203_acknowledgement_has_exact_non_success_semantics() -> None:
    compact = _compact(_DECISION)
    for required in (
        "exact acknowledgement fields are protocol, request_id, operation_id, request_sha256, status, receipt_id, and diagnostic",
        "exactly one acknowledgement",
        "accepted or refused",
        "accepted acknowledges only bounded admission",
        "does not mean mutation started",
        "does not mean mutation succeeded",
        "refused guarantees no mutation",
        "acknowledgement is not a receipt",
    ):
        assert required in compact


def test_m203_receipt_has_exact_typed_outcomes_without_recovery_invention() -> None:
    compact = _compact(_DECISION)
    for required in (
        "exact receipt fields are protocol, request_id, operation_id, request_sha256, acknowledgement_sha256, receipt_id, status, phase, outcomes, and diagnostics",
        "refused, completed, or recovery_required",
        "candidate_ordinal, status, and code",
        "deterministic candidate order",
        "completed is forbidden before durable terminal completion",
        "recovery_required after any completed mutation phase without terminal completion",
        "receipt is evidence, not authority",
        "criterion 5 defines the durable phase transitions",
    ):
        assert required in compact


def test_m203_correlates_retries_without_claiming_exactly_once() -> None:
    compact = _compact(_DECISION)
    for required in (
        "sha-256 over canonical request bytes",
        "sha-256 over canonical acknowledgement bytes",
        "same operation_id and same request_sha256",
        "same operation_id with a different request_sha256 is a conflict",
        "must not repeat mutation",
        "no exactly-once claim",
        "criterion 5 must define durable replay lookup",
        "delivery failure leaves the outcome unknown",
    ):
        assert required in compact


def test_m203_receipts_are_bounded_path_free_non_authenticating_evidence() -> None:
    compact = _compact(_DECISION)
    for required in (
        "operation-local ordinal",
        "path-free",
        "native handles",
        "token identifiers",
        "security descriptors",
        "generation nonces",
        "file identifiers",
        "content identities",
        "platform error text",
        "diagnostic codes are semantic",
        "messages are metadata",
        "no authenticity, signature, or non-repudiation claim",
    ):
        assert required in compact


def test_m203_resolves_only_the_protocol_policy_criterion() -> None:
    compact = _compact(_DECISION)
    for required in (
        "criteria 1 through 4 are resolved as policy",
        "criterion 4 is resolved as policy",
        "criteria 5 through 7 remain unresolved",
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


def test_m203_rfc_is_accepted_and_direction_preserving() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    compact = " ".join(rfc.casefold().split())
    assert "**Status:** Accepted" in rfc
    assert "direction-preserving" in compact
    assert "no authority increase" in compact
    assert "no production adapter" in compact
    assert "no new hosted allocation" in compact


def test_m203_public_boundary_is_registered_without_ci_expansion() -> None:
    slug = "windows-cache-cleanup-protocol-receipt-policy"
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
    assert "0186-adopt-windows-cleanup-protocol-receipt-policy.md" in rfc_index


def test_m203_adds_no_cleanup_command_adapter_or_public_protocol_surface() -> None:
    cli = (_ROOT / "src/ludoweave/tools/cli.py").read_text(encoding="utf-8")
    for command in (
        "asset-cache-cleanup",
        "asset-cache-capabilities",
        "asset-cache-prune",
        "asset-cache-delete",
        "asset-cache-revalidate",
        "asset-cache-recover",
    ):
        assert command not in cli

    names = {path.name for path in (_ROOT / "src/ludoweave/assets").glob("*.py")}
    assert {
        "cleanup.py",
        "cleanup_authority.py",
        "cleanup_capabilities.py",
        "cleanup_protocol.py",
        "cleanup_receipt.py",
        "cleanup_revalidation.py",
        "filesystem_adapter.py",
        "garbage_collection.py",
        "recovery.py",
        "retention.py",
    }.isdisjoint(names)
