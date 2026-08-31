"""Validate one offline Windows cleanup cross-principal evidence artifact."""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from hashlib import sha256
from os import fstat
from pathlib import Path
from stat import S_ISLNK, S_ISREG
from typing import cast

from ludoweave.world import JsonLimits, canonical_dumps, canonical_loads

_SCHEMA = "ludoweave.windows-cleanup-cross-principal-evidence/1"
_RESULT_SCHEMA = "ludoweave.windows-cleanup-cross-principal-evidence-validation/1"
_MAX_DOCUMENT_BYTES = 4_194_304
_MAX_LANES = 32
_MAX_TRIALS = 512
_MAX_EVENTS = 32_768
_LIMITS = JsonLimits(
    max_bytes=_MAX_DOCUMENT_BYTES,
    max_depth=8,
    max_nodes=2_048,
    max_collection_items=256,
    max_string_bytes=256,
)
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
_QUALIFICATION_FIELDS = (
    "principal_sid_distinct",
    "authentication_context_distinct",
    "administrator_membership_absent",
    "bypass_privileges_absent",
)
_CONTROL_FIELDS = (
    "observer_derived",
    "control_channel_authenticated",
    "fixture_confined",
    "teardown_settled",
)
_OUTCOME_FIELDS = (
    "no_out_of_root_mutation",
    "no_unauthorized_deletion_or_restoration",
    "no_canonical_world_state_change",
    "no_leaked_handle",
    "no_live_participant_or_descendant",
)
_LANE_STATUSES = frozenset(("passed", "failed", "unsupported", "not_run"))
_ORDER_STATUSES = frozenset(("passed", "failed", "unsupported", "not_run", "not_applicable"))


class EvidenceValidationError(ValueError):
    """A stable, path-free evidence validation failure."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True, slots=True)
class ValidationSummary:
    """Sanitized result of validating one evidence artifact."""

    criterion_6_satisfied: bool
    evidence_sha256: str
    lane_status_counts: Mapping[str, int]
    windows_cleanup_admitted: bool = False

    def as_dict(self) -> dict[str, object]:
        """Return the canonical, path-free CLI result."""

        return {
            "criterion_6_satisfied": self.criterion_6_satisfied,
            "evidence_sha256": self.evidence_sha256,
            "lane_status_counts": dict(self.lane_status_counts),
            "schema": _RESULT_SCHEMA,
            "status": "valid",
            "windows_cleanup_admitted": self.windows_cleanup_admitted,
        }


def validate_evidence_file(evidence_file: Path) -> ValidationSummary:
    """Read and validate one regular, stable, canonical evidence file."""

    encoded = _read_stable_regular_file(evidence_file)
    try:
        decoded = canonical_loads(encoded, limits=_LIMITS)
        if canonical_dumps(decoded, limits=_LIMITS) != encoded:
            raise EvidenceValidationError(
                "evidence.noncanonical",
                "evidence artifact must use exact canonical bytes",
            )
    except EvidenceValidationError:
        raise
    except Exception as error:
        raise EvidenceValidationError(
            "evidence.invalid_json",
            "evidence artifact is not bounded canonical JSON",
        ) from error

    document = _mapping(decoded, "document")
    criterion, counts = _validate_document(document)
    return ValidationSummary(
        criterion_6_satisfied=criterion,
        evidence_sha256=f"sha256:{sha256(encoded).hexdigest()}",
        lane_status_counts=counts,
    )


def _read_stable_regular_file(evidence_file: Path) -> bytes:
    try:
        before = evidence_file.lstat()
    except OSError as error:
        raise EvidenceValidationError(
            "evidence.read_failed", "evidence artifact could not be inspected"
        ) from error
    if S_ISLNK(before.st_mode) or not S_ISREG(before.st_mode):
        raise EvidenceValidationError(
            "evidence.not_regular", "evidence artifact must be a regular non-symbolic-link file"
        )
    if before.st_size > _MAX_DOCUMENT_BYTES:
        raise EvidenceValidationError(
            "evidence.too_large", "evidence artifact exceeds the byte limit"
        )

    try:
        with evidence_file.open("rb") as stream:
            opened = fstat(stream.fileno())
            if (
                before.st_dev != opened.st_dev
                or before.st_ino != opened.st_ino
                or before.st_size != opened.st_size
                or not S_ISREG(opened.st_mode)
            ):
                raise EvidenceValidationError(
                    "evidence.changed", "evidence artifact changed while being opened"
                )
            encoded = stream.read(_MAX_DOCUMENT_BYTES + 1)
            after_read = fstat(stream.fileno())
        after = evidence_file.lstat()
    except EvidenceValidationError:
        raise
    except OSError as error:
        raise EvidenceValidationError(
            "evidence.read_failed", "evidence artifact could not be read"
        ) from error

    if len(encoded) > _MAX_DOCUMENT_BYTES:
        raise EvidenceValidationError(
            "evidence.too_large", "evidence artifact exceeds the byte limit"
        )
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
        raise EvidenceValidationError(
            "evidence.changed", "evidence artifact changed while being opened"
        )
    return encoded


def _validate_document(document: Mapping[str, object]) -> tuple[bool, dict[str, int]]:
    _exact_fields(
        document,
        (
            "schema",
            "source_commit",
            "executable_sha256",
            "qualification",
            "controls",
            "lanes",
            "totals",
            "criterion_6_satisfied",
            "windows_cleanup_admitted",
        ),
        "document",
    )
    _equal(document["schema"], _SCHEMA, "schema")
    qualification = _boolean_record(
        document["qualification"], _QUALIFICATION_FIELDS, "qualification"
    )
    controls = _boolean_record(document["controls"], _CONTROL_FIELDS, "controls")
    lanes = _sequence(document["lanes"], "lanes")
    if len(lanes) > _MAX_LANES or len(lanes) != len(_LANES):
        _invalid("schema.lanes", "evidence must contain exactly 13 mandatory lanes")

    counts = {status: 0 for status in sorted(_LANE_STATUSES)}
    total_trials = 0
    total_events = 0
    all_passed = True
    for index, lane_value in enumerate(lanes):
        lane = _mapping(lane_value, "lane")
        status, trial_count, event_count = _validate_lane(lane, _LANES[index])
        counts[status] += 1
        total_trials += trial_count
        total_events += event_count
        all_passed = all_passed and status == "passed"

    if total_trials > _MAX_TRIALS:
        _invalid("limits.trials", "evidence exceeds the trial limit")
    if total_events > _MAX_EVENTS:
        _invalid("limits.events", "evidence exceeds the event limit")
    _validate_totals(document["totals"], total_trials, total_events)

    all_not_run = counts["not_run"] == len(_LANES)
    source_commit = document["source_commit"]
    executable_sha256 = document["executable_sha256"]
    if all_not_run:
        if source_commit is not None or executable_sha256 is not None:
            _invalid("identity.unattempted", "unattempted evidence must omit identities")
    else:
        _validate_prefixed_hex(source_commit, "git-sha1:", 40, "source_commit")
        _validate_prefixed_hex(executable_sha256, "sha256:", 64, "executable_sha256")

    expected_criterion = all(qualification.values()) and all(controls.values()) and all_passed
    criterion = _boolean(document["criterion_6_satisfied"], "criterion_6_satisfied")
    if criterion != expected_criterion:
        _invalid(
            "claim.criterion_6",
            "criterion_6_satisfied does not match the complete evidence",
        )
    admitted = _boolean(document["windows_cleanup_admitted"], "windows_cleanup_admitted")
    if admitted:
        _invalid(
            "claim.windows_cleanup",
            "windows_cleanup_admitted must remain false until criterion 7 is satisfied",
        )
    return criterion, counts


def _validate_lane(lane: Mapping[str, object], expected_id: str) -> tuple[str, int, int]:
    _exact_fields(
        lane,
        ("id", "status", "trial_count", "event_count", "barriers", "outcomes"),
        "lane",
    )
    _equal(lane["id"], expected_id, "lane.id")
    status = _text_member(lane["status"], _LANE_STATUSES, "lane.status")
    trial_count = _nonnegative_integer(lane["trial_count"], "lane.trial_count")
    event_count = _nonnegative_integer(lane["event_count"], "lane.event_count")
    barriers = _sequence(lane["barriers"], "lane.barriers")
    outcomes = _boolean_record(lane["outcomes"], _OUTCOME_FIELDS, "lane.outcomes")

    if status == "not_run":
        if trial_count != 0 or event_count != 0 or barriers or any(outcomes.values()):
            _invalid("lane.not_run", "not_run lanes must contain no observations")
        return status, trial_count, event_count

    if len(barriers) > len(_BARRIERS):
        _invalid("lane.barriers", "lane contains too many barriers")
    applicable_count = 0
    for index, barrier_value in enumerate(barriers):
        barrier = _mapping(barrier_value, "barrier")
        expected_barrier = _BARRIERS[index]
        applicable_count += _validate_barrier(
            barrier, expected_barrier, lane_passed=status == "passed"
        )
    if status == "passed":
        if (
            tuple(_text(_mapping(item, "barrier")["id"], "barrier.id") for item in barriers)
            != _BARRIERS
        ):
            _invalid("lane.barriers", "passed lane must contain every barrier in canonical order")
        if applicable_count == 0:
            _invalid("lane.barriers", "passed lane must exercise an applicable barrier")
        if trial_count == 0 or event_count == 0 or not all(outcomes.values()):
            _invalid("lane.passed", "passed lane must contain successful observations")
    return status, trial_count, event_count


def _validate_barrier(barrier: Mapping[str, object], expected_id: str, *, lane_passed: bool) -> int:
    _exact_fields(barrier, ("id", "applicable", "release_orders"), "barrier")
    _equal(barrier["id"], expected_id, "barrier.id")
    applicable = _boolean(barrier["applicable"], "barrier.applicable")
    orders = _mapping(barrier["release_orders"], "barrier.release_orders")
    _exact_fields(orders, ("authority_first", "mutation_first"), "barrier.release_orders")
    authority_first = _text_member(
        orders["authority_first"], _ORDER_STATUSES, "barrier.authority_first"
    )
    mutation_first = _text_member(
        orders["mutation_first"], _ORDER_STATUSES, "barrier.mutation_first"
    )
    if applicable:
        if "not_applicable" in (authority_first, mutation_first):
            _invalid(
                "barrier.release_order",
                "applicable release orders cannot be not_applicable",
            )
        if lane_passed and (authority_first != "passed" or mutation_first != "passed"):
            _invalid("barrier.release_order", "applicable release orders must pass")
        return 1
    if authority_first != "not_applicable" or mutation_first != "not_applicable":
        _invalid("barrier.not_applicable", "inapplicable release orders must be not_applicable")
    return 0


def _validate_totals(value: object, trial_count: int, event_count: int) -> None:
    totals = _mapping(value, "totals")
    _exact_fields(totals, ("lane_count", "trial_count", "event_count"), "totals")
    _equal(totals["lane_count"], len(_LANES), "totals.lane_count")
    _equal(totals["trial_count"], trial_count, "totals.trial_count")
    _equal(totals["event_count"], event_count, "totals.event_count")


def _validate_prefixed_hex(value: object, prefix: str, length: int, field: str) -> None:
    if type(value) is not str:
        _invalid("identity.invalid", f"{field} must use the required digest identity")
    text = cast(str, value)
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
    return cast(bool, value)


def _text(value: object, field: str) -> str:
    if type(value) is not str:
        _invalid("schema.type", f"{field} must be text")
    return cast(str, value)


def _text_member(value: object, allowed: frozenset[str], field: str) -> str:
    text = _text(value, field)
    if text not in allowed:
        _invalid("schema.value", f"{field} contains an unsupported value")
    return text


def _nonnegative_integer(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        _invalid("schema.type", f"{field} must be a non-negative integer")
    return cast(int, value)


def _equal(value: object, expected: object, field: str) -> None:
    if type(value) is not type(expected) or value != expected:
        _invalid("schema.value", f"{field} contains an unexpected value")


def _invalid(code: str, message: str) -> None:
    raise EvidenceValidationError(code, message)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate one offline Windows cross-principal evidence artifact."
    )
    parser.add_argument("evidence_file", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Validate an artifact and print one canonical, path-free result."""

    arguments = _parser().parse_args(argv)
    try:
        summary = validate_evidence_file(arguments.evidence_file)
        result = summary.as_dict()
        exit_code = 0
    except EvidenceValidationError as error:
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
