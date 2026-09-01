"""Validate one offline Windows independent-host collection plan."""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from hashlib import sha256
from os import fstat
from pathlib import Path
from stat import S_ISLNK, S_ISREG
from typing import NoReturn, cast

from ludoweave.world import JsonLimits, canonical_dumps, canonical_loads

_SCHEMA = "ludoweave.windows-cleanup-independent-host-collection-plan/1"
_RESULT_SCHEMA = "ludoweave.windows-cleanup-independent-host-collection-plan-validation/1"
_MAX_DOCUMENT_BYTES = 1_048_576
_MAX_HOSTS = 32
_LIMITS = JsonLimits(
    max_bytes=_MAX_DOCUMENT_BYTES,
    max_depth=8,
    max_nodes=2_048,
    max_collection_items=128,
    max_string_bytes=128,
)
_PROFILES = (
    "local_fixed_ntfs",
    "refs_refusal",
    "smb_refusal",
    "csvfs_refusal",
    "cross_volume_refusal",
    "unknown_filesystem_refusal",
    "missing_capability_refusal",
    "file_id_reuse_aba",
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
_INTERRUPTIONS = (
    "forced_process_termination",
    "vm_power_cut",
    "physical_host_power_loss",
)
_OPERATIONS = (
    "observe_revalidate",
    "launch_participant",
    "advance_barrier",
    "apply_interruption",
    "restart_reconcile",
    "collect_observations",
    "settle_teardown",
    "stage_artifact",
)
_REQUIREMENTS = (
    "atomic_same_volume_staging",
    "authority_nonserializable",
    "authority_single_run",
    "authority_single_use",
    "checkpoint_restore_forbidden",
    "cleanup_authority_separate",
    "clipboard_redirection_disabled",
    "custody_chronological",
    "digest_retained_separately",
    "fail_closed_teardown",
    "fixture_disposable_and_confined",
    "networking_disabled",
    "physical_interruption_operator_only",
    "process_identity_retained",
    "process_tree_contained",
    "public_runner_detached",
    "read_only_ingress_detached",
    "repository_credentials_absent",
    "sanitization_review_required",
    "stable_identifiers_excluded",
    "vm_power_control_external",
    "writable_live_sharing_disabled",
)
_WINDOWS_RELEASE_CLASSES = frozenset(
    (
        "windows_10",
        "windows_11",
        "windows_server_2022",
        "windows_server_2025",
        "other_supported",
    )
)
_ARCHITECTURE_CLASSES = frozenset(("x86_64", "arm64"))
_PERSISTENCE_CLASSES = frozenset(("persistent_vm", "physical"))


class CollectionPlanValidationError(ValueError):
    """A stable, path-free collection-plan validation failure."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True, slots=True)
class ValidationSummary:
    """Sanitized result of validating one collection plan."""

    collection_status: str
    plan_complete: bool
    plan_sha256: str
    host_count: int
    planned_binding_count: int
    authority_issued: bool = False
    criterion_6_satisfied: bool = False
    criterion_7_satisfied: bool = False
    windows_cleanup_admitted: bool = False

    def as_dict(self) -> dict[str, object]:
        """Return the canonical, path-free validation result."""

        return {
            "authority_issued": self.authority_issued,
            "collection_status": self.collection_status,
            "criterion_6_satisfied": self.criterion_6_satisfied,
            "criterion_7_satisfied": self.criterion_7_satisfied,
            "host_count": self.host_count,
            "plan_complete": self.plan_complete,
            "plan_sha256": self.plan_sha256,
            "planned_binding_count": self.planned_binding_count,
            "schema": _RESULT_SCHEMA,
            "status": "valid",
            "windows_cleanup_admitted": self.windows_cleanup_admitted,
        }


def validate_collection_plan_file(plan_file: Path) -> ValidationSummary:
    """Validate one stable canonical collection plan without granting authority."""

    encoded = _read_stable_regular_file(plan_file)
    try:
        decoded = canonical_loads(encoded, limits=_LIMITS)
        if canonical_dumps(decoded, limits=_LIMITS) + b"\n" != encoded:
            _invalid("plan.noncanonical", "collection plan must use one exact canonical JSON line")
    except CollectionPlanValidationError:
        raise
    except Exception as error:
        raise CollectionPlanValidationError(
            "plan.invalid_json",
            "collection plan is not bounded canonical JSON",
        ) from error

    document = _mapping(decoded, "document")
    collection_status, plan_complete, host_count, planned_binding_count = _validate_document(
        document
    )
    return ValidationSummary(
        collection_status=collection_status,
        plan_complete=plan_complete,
        plan_sha256=f"sha256:{sha256(encoded).hexdigest()}",
        host_count=host_count,
        planned_binding_count=planned_binding_count,
    )


def _read_stable_regular_file(plan_file: Path) -> bytes:
    try:
        before = plan_file.lstat()
    except OSError as error:
        raise CollectionPlanValidationError(
            "plan.read_failed", "collection plan could not be inspected"
        ) from error
    if S_ISLNK(before.st_mode) or not S_ISREG(before.st_mode):
        _invalid("plan.not_regular", "collection plan must be a regular non-symbolic-link file")
    if before.st_size > _MAX_DOCUMENT_BYTES:
        _invalid("plan.too_large", "collection plan exceeds the byte limit")

    try:
        with plan_file.open("rb") as stream:
            opened = fstat(stream.fileno())
            if (
                before.st_dev != opened.st_dev
                or before.st_ino != opened.st_ino
                or before.st_size != opened.st_size
                or not S_ISREG(opened.st_mode)
            ):
                _invalid("plan.changed", "collection plan changed while being opened")
            encoded = stream.read(_MAX_DOCUMENT_BYTES + 1)
            after_read = fstat(stream.fileno())
        after = plan_file.lstat()
    except CollectionPlanValidationError:
        raise
    except OSError as error:
        raise CollectionPlanValidationError(
            "plan.read_failed", "collection plan could not be read"
        ) from error

    if len(encoded) > _MAX_DOCUMENT_BYTES:
        _invalid("plan.too_large", "collection plan exceeds the byte limit")
    identity_before = (before.st_dev, before.st_ino, before.st_size)
    identity_after_read = (after_read.st_dev, after_read.st_ino, after_read.st_size)
    identity_after = (after.st_dev, after.st_ino, after.st_size)
    if (
        identity_before != identity_after_read
        or identity_before != identity_after
        or S_ISLNK(after.st_mode)
        or not S_ISREG(after.st_mode)
        or len(encoded) != before.st_size
    ):
        _invalid("plan.changed", "collection plan changed while being opened")
    return encoded


def _validate_document(document: Mapping[str, object]) -> tuple[str, bool, int, int]:
    _exact_fields(
        document,
        (
            "schema",
            "source_commit",
            "executable_sha256",
            "independent_host_contract_sha256",
            "collection_authority_policy_sha256",
            "cross_principal_evidence_sha256",
            "fixture_recipe_sha256",
            "capability_profile_sha256",
            "hosts",
            "profiles",
            "barriers",
            "interruptions",
            "operations",
            "requirements",
            "totals",
            "collection_status",
            "plan_complete",
            "authority_issued",
            "criterion_6_satisfied",
            "criterion_7_satisfied",
            "windows_cleanup_admitted",
        ),
        "document",
    )
    _equal(document["schema"], _SCHEMA, "schema")
    identities = (
        ("source_commit", "git-sha1:", 40),
        ("executable_sha256", "sha256:", 64),
        ("independent_host_contract_sha256", "sha256:", 64),
        ("collection_authority_policy_sha256", "sha256:", 64),
        ("cross_principal_evidence_sha256", "sha256:", 64),
        ("fixture_recipe_sha256", "sha256:", 64),
        ("capability_profile_sha256", "sha256:", 64),
    )
    identities_complete = True
    for field, prefix, length in identities:
        value = document[field]
        if value is None:
            identities_complete = False
        else:
            _validate_prefixed_hex(value, prefix, length, field)

    host_count = _validate_hosts(document["hosts"])
    _validate_ordered_records(document["profiles"], _PROFILES, "profile")
    _validate_ordered_text(document["barriers"], _BARRIERS, "barrier")
    _validate_ordered_text(document["interruptions"], _INTERRUPTIONS, "interruption")
    _validate_ordered_text(document["operations"], _OPERATIONS, "operation")
    requirements = _boolean_record(document["requirements"], _REQUIREMENTS, "requirements")
    planned_binding_count = host_count * len(_PROFILES) * len(_BARRIERS) * len(_INTERRUPTIONS)
    _validate_totals(document["totals"], host_count, planned_binding_count)

    collection_status = _text_member(
        document["collection_status"], frozenset(("not_run",)), "collection_status"
    )
    plan_complete = _boolean(document["plan_complete"], "plan_complete")
    derived_complete = identities_complete and host_count >= 2 and all(requirements.values())
    _equal(plan_complete, derived_complete, "plan_complete", code="claim.plan_complete")
    _equal(document["authority_issued"], False, "authority_issued", code="claim.authority")
    _equal(
        document["criterion_6_satisfied"],
        False,
        "criterion_6_satisfied",
        code="claim.criterion_6",
    )
    _equal(
        document["criterion_7_satisfied"],
        False,
        "criterion_7_satisfied",
        code="claim.criterion_7",
    )
    _equal(
        document["windows_cleanup_admitted"],
        False,
        "windows_cleanup_admitted",
        code="claim.windows_cleanup",
    )
    return collection_status, plan_complete, host_count, planned_binding_count


def _validate_hosts(value: object) -> int:
    hosts = _sequence(value, "hosts")
    if len(hosts) > _MAX_HOSTS:
        _invalid("limits.hosts", "collection plan exceeds the host limit")
    for index, host_value in enumerate(hosts, start=1):
        host = _mapping(host_value, "host")
        _exact_fields(
            host,
            (
                "ordinal",
                "windows_release_class",
                "architecture_class",
                "persistence_class",
                "status",
            ),
            "host",
        )
        _equal(host["ordinal"], index, "host.ordinal")
        _text_member(
            host["windows_release_class"], _WINDOWS_RELEASE_CLASSES, "host.windows_release_class"
        )
        _text_member(host["architecture_class"], _ARCHITECTURE_CLASSES, "host.architecture_class")
        _text_member(host["persistence_class"], _PERSISTENCE_CLASSES, "host.persistence_class")
        _equal(host["status"], "not_run", "host.status")
    return len(hosts)


def _validate_ordered_records(value: object, expected: tuple[str, ...], location: str) -> None:
    records = _sequence(value, f"{location}s")
    if len(records) != len(expected):
        _invalid("schema.matrix", f"collection plan must contain the exact {location} matrix")
    for record_value, expected_id in zip(records, expected, strict=True):
        record = _mapping(record_value, location)
        _exact_fields(record, ("id", "status"), location)
        _equal(record["id"], expected_id, f"{location}.id")
        _equal(record["status"], "not_run", f"{location}.status")


def _validate_ordered_text(value: object, expected: tuple[str, ...], location: str) -> None:
    items = _sequence(value, f"{location}s")
    if len(items) != len(expected):
        _invalid("schema.matrix", f"collection plan must contain the exact {location} sequence")
    for item, expected_item in zip(items, expected, strict=True):
        _equal(item, expected_item, location)


def _validate_totals(value: object, host_count: int, planned_binding_count: int) -> None:
    totals = _mapping(value, "totals")
    _exact_fields(
        totals,
        (
            "host_count",
            "profile_count",
            "barrier_count",
            "interruption_count",
            "operation_count",
            "planned_binding_count",
        ),
        "totals",
    )
    expected = {
        "host_count": host_count,
        "profile_count": len(_PROFILES),
        "barrier_count": len(_BARRIERS),
        "interruption_count": len(_INTERRUPTIONS),
        "operation_count": len(_OPERATIONS),
        "planned_binding_count": planned_binding_count,
    }
    for field, expected_value in expected.items():
        _equal(totals[field], expected_value, f"totals.{field}")


def _validate_prefixed_hex(value: object, prefix: str, length: int, field: str) -> None:
    if type(value) is not str:
        _invalid("identity.invalid", f"{field} must use the required digest identity")
    text = value
    payload = text.removeprefix(prefix)
    if (
        not text.startswith(prefix)
        or len(payload) != length
        or any(character not in "0123456789abcdef" for character in payload)
    ):
        _invalid("identity.invalid", f"{field} must use the required digest identity")


def _boolean_record(value: object, fields: tuple[str, ...], location: str) -> dict[str, bool]:
    record = _mapping(value, location)
    _exact_fields(record, fields, location)
    return {field: _boolean(record[field], f"{location}.{field}") for field in fields}


def _mapping(value: object, location: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        _invalid("schema.type", f"{location} must be an object")
    return cast(Mapping[str, object], value)


def _sequence(value: object, location: str) -> Sequence[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        _invalid("schema.type", f"{location} must be an array")
    return cast(Sequence[object], value)


def _exact_fields(value: Mapping[str, object], expected: tuple[str, ...], location: str) -> None:
    if set(value) != set(expected):
        _invalid("schema.fields", f"{location} contains missing or unknown fields")


def _boolean(value: object, field: str) -> bool:
    if type(value) is not bool:
        _invalid("schema.type", f"{field} must be a boolean")
    return value


def _text(value: object, field: str) -> str:
    if type(value) is not str:
        _invalid("schema.type", f"{field} must be text")
    return value


def _text_member(value: object, allowed: frozenset[str], field: str) -> str:
    text = _text(value, field)
    if text not in allowed:
        _invalid("schema.value", f"{field} contains an unsupported value")
    return text


def _equal(
    value: object,
    expected: object,
    field: str,
    *,
    code: str = "schema.value",
) -> None:
    if type(value) is not type(expected) or value != expected:
        _invalid(code, f"{field} contains an unexpected value")


def _invalid(code: str, message: str) -> NoReturn:
    raise CollectionPlanValidationError(code, message)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate one offline Windows independent-host collection plan."
    )
    parser.add_argument("plan_file", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Validate one plan and print one canonical path-free result."""

    arguments = _parser().parse_args(argv)
    try:
        summary = validate_collection_plan_file(arguments.plan_file)
        result = summary.as_dict()
        exit_code = 0
    except CollectionPlanValidationError as error:
        result = {
            "error": {"code": error.code, "message": error.message},
            "schema": _RESULT_SCHEMA,
            "status": "invalid",
        }
        exit_code = 1
    print(canonical_dumps(result).decode("utf-8"))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
