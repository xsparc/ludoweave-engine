"""Evaluate reviewed agent-tool recovery evidence without inferring a success rate."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from ludoweave import __version__

type _CallIdentity = tuple[
    str,
    str,
    int,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    bool | None,
    str,
    str,
    str,
    str | None,
    str | None,
    str | None,
    str | None,
    bool,
    bool,
    bool,
    bool,
    bool,
    bool,
    bool,
]
type _WindowIdentity = tuple[
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    tuple[_CallIdentity, ...],
    bool,
    bool,
    bool,
    bool,
    bool,
    bool,
]

_SCHEMA = "ludoweave.evaluation.agent-tool-recovery-rate-readiness/1"
_MANIFEST_SCHEMA = "ludoweave.operations.agent-tool-recovery-rate/1"
_MEASUREMENT_POLICY = "complete-reviewed-task-directed-agent-tool-calls/1"
_REVIEWED_MANIFEST_SHA256 = "e952c045b039055e8439069cf88176b6ac1d2ad7de49a94d39b2737e5d06e1d5"
_MANDATORY_WINDOW_PREFIX: tuple[_WindowIdentity, ...] = ()
_MAX_MANIFEST_BYTES = 131_072
_MAX_JSON_NESTING = 16
_MAX_EVALUATION_WINDOWS = 12
_MAX_CALLS_PER_WINDOW = 2_048
_MAX_WINDOW_SECONDS = 31_622_400
_MAX_OBSERVATION_LAG_SECONDS = 31_622_400
_MAX_SESSION_CALL_INDEX = 2_147_483_647
_PROJECT_URL = "https://github.com/xsparc/ludoweave-engine"
_SERVICE_PROTOCOL = "ludoweave.agent.service/1"
_TOOL_NAMES = (
    "project_describe",
    "world_describe",
    "world_query",
    "entity_get",
    "transaction_validate",
    "transaction_apply",
    "world_tick",
    "world_snapshot",
    "world_diff",
    "render_capture",
    "telemetry_get",
    "test_run",
)
_NOT_COMPLETED_CODES = {
    "tool-call-cancelled",
    "tool-call-failed",
    "tool-call-rejected",
}
_UNOBSERVED_CODES = {
    "call-result-evidence-unavailable",
    "call-terminal-state-unobserved",
}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="explicit local reviewed agent-tool recovery manifest",
    )
    arguments = parser.parse_args(tuple(sys.argv[1:] if argv is None else argv))
    selected: object = getattr(arguments, "manifest", None)
    manifest = _default_manifest() if selected is None else _path(selected)
    print(json.dumps(evaluate(manifest), ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0


def evaluate(manifest: Path) -> dict[str, object]:
    """Return deterministic, path-free agent-tool recovery admission evidence."""

    raw_manifest, identities = _parse_manifest(manifest)
    manifest_hash = hashlib.sha256(raw_manifest).hexdigest()
    manifest_identity_reviewed = manifest_hash == _REVIEWED_MANIFEST_SHA256
    historical_windows_preserved = tuple(
        identities[: len(_MANDATORY_WINDOW_PREFIX)]
    ) == _MANDATORY_WINDOW_PREFIX and (
        not manifest_identity_reviewed or len(identities) == len(_MANDATORY_WINDOW_PREFIX)
    )
    admitted = identities if manifest_identity_reviewed and historical_windows_preserved else ()
    calls = tuple(call for window in admitted for call in window[8])
    completed_without_count = sum(call[10] == "completed-without-manual-recovery" for call in calls)
    completed_after_count = sum(call[10] == "completed-after-manual-recovery" for call in calls)
    not_completed_count = sum(call[10] == "not-completed" for call in calls)
    unobserved_count = sum(call[10] == "terminal-unobserved" for call in calls)
    manual_recovery_count = sum(call[11] is True for call in calls)
    complete_reviewed_windows = bool(admitted)
    tool_calls_present = bool(calls)
    terminal_call_cohort_complete = tool_calls_present and unobserved_count == 0
    gate_satisfied = (
        manifest_identity_reviewed
        and historical_windows_preserved
        and complete_reviewed_windows
        and tool_calls_present
        and terminal_call_cohort_complete
    )
    reasons: list[str]
    if manifest_identity_reviewed and historical_windows_preserved and not identities:
        reasons = ["agent-tool-recovery-rate-evidence-absent"]
    else:
        reasons = []
        if not manifest_identity_reviewed:
            reasons.append("agent-tool-recovery-manifest-identity-unreviewed")
        if not historical_windows_preserved:
            reasons.append("historical-evaluation-window-missing")
        if not complete_reviewed_windows:
            reasons.append("complete-reviewed-evaluation-window-absent")
        if not tool_calls_present:
            reasons.append("reviewed-agent-tool-call-absent")
        if tool_calls_present and not terminal_call_cohort_complete:
            reasons.append("agent-tool-terminal-cohort-incomplete")

    rate: dict[str, int] | None = None
    if gate_satisfied:
        rate = {"denominator": len(calls), "numerator": completed_without_count}
    return {
        "admission": {
            "complete_reviewed_windows": complete_reviewed_windows,
            "historical_windows_preserved": historical_windows_preserved,
            "manifest_identity_reviewed": manifest_identity_reviewed,
            "terminal_call_cohort_complete": terminal_call_cohort_complete,
            "tool_calls_present": tool_calls_present,
            "reason_codes": tuple(reasons),
        },
        "completion_without_manual_recovery_rate_proven": gate_satisfied,
        "evidence_level": (
            "reviewed-agent-tool-recovery-rate"
            if gate_satisfied
            else "agent-tool-recovery-rate-admission-readiness"
        ),
        "gate_satisfied": gate_satisfied,
        "ludoweave_version": __version__,
        "metrics": {
            "completed_after_manual_recovery_count": completed_after_count,
            "completed_without_manual_recovery_count": completed_without_count,
            "completion_without_manual_recovery_rate": rate,
            "manifest_sha256": manifest_hash,
            "manual_recovery_count": manual_recovery_count,
            "measurement_policy": _MEASUREMENT_POLICY,
            "not_completed_count": not_completed_count,
            "records_verified": True,
            "tool_call_count": len(calls),
            "unobserved_terminal_count": unobserved_count,
            "window_count": len(admitted),
        },
        "schema": _SCHEMA,
        "status": "ready" if gate_satisfied else "not-ready",
    }


def _parse_manifest(path: Path) -> tuple[bytes, tuple[_WindowIdentity, ...]]:
    raw_manifest = _read_bounded(path, _MAX_MANIFEST_BYTES, "agent-tool recovery manifest")
    document = _object(
        _loads(raw_manifest, "agent-tool recovery manifest"), "agent-tool recovery manifest"
    )
    _exact_fields(
        document,
        {"schema", "source_project", "measurement_policy", "evaluation_windows"},
        "agent-tool recovery manifest",
    )
    if document["schema"] != _MANIFEST_SCHEMA:
        raise RuntimeError("agent-tool recovery manifest schema is incompatible")
    if document["source_project"] != "ludoweave-engine":
        raise RuntimeError("agent-tool recovery project identity is invalid")
    if document["measurement_policy"] != _MEASUREMENT_POLICY:
        raise RuntimeError("agent-tool recovery measurement policy is incompatible")

    raw_windows = _list(document["evaluation_windows"], "evaluation windows")
    if len(raw_windows) > _MAX_EVALUATION_WINDOWS:
        raise RuntimeError("agent-tool recovery manifest exceeds its window limit")
    identities: list[_WindowIdentity] = []
    session_next_index: dict[str, int] = {}
    evidence_urls: set[str] = set()
    evidence_hashes: set[str] = set()
    previous_started_before: datetime | None = None
    for index, item in enumerate(raw_windows):
        identity, started_before = _window_identity(
            _object(item, "evaluation window"),
            index=index,
            previous_started_before=previous_started_before,
            session_next_index=session_next_index,
            evidence_urls=evidence_urls,
            evidence_hashes=evidence_hashes,
        )
        identities.append(identity)
        previous_started_before = started_before
    return raw_manifest, tuple(identities)


def _window_identity(
    window: dict[str, object],
    *,
    index: int,
    previous_started_before: datetime | None,
    session_next_index: dict[str, int],
    evidence_urls: set[str],
    evidence_hashes: set[str],
) -> tuple[_WindowIdentity, datetime]:
    _exact_fields(
        window,
        {
            "window_id",
            "started_from",
            "started_before",
            "observed_through",
            "census_url",
            "census_sha256",
            "review_url",
            "review_sha256",
            "calls",
            "task_directed_session_census_complete_reviewed",
            "eligibility_reviewed",
            "manual_recovery_definition_reviewed",
            "privacy_and_consent_reviewed",
            "provenance_reviewed",
            "validation_reviewed",
        },
        "evaluation window",
    )
    window_id = _bounded_ascii_text(window["window_id"], 16, "evaluation window ID")
    if window_id != f"window-{index + 1:04d}":
        raise RuntimeError("evaluation windows must use canonical sequential IDs")
    started_from, started_from_value = _utc_timestamp(
        window["started_from"], "evaluation window opening timestamp"
    )
    started_before, started_before_value = _utc_timestamp(
        window["started_before"], "evaluation window closing timestamp"
    )
    observed_through, observed_through_value = _utc_timestamp(
        window["observed_through"], "evaluation observation timestamp"
    )
    if started_from_value >= started_before_value:
        raise RuntimeError("evaluation window must have positive duration")
    if previous_started_before is not None and started_from_value < previous_started_before:
        raise RuntimeError("evaluation windows must be chronological and non-overlapping")
    if _seconds_between(started_from_value, started_before_value) > _MAX_WINDOW_SECONDS:
        raise RuntimeError("evaluation window exceeds its duration limit")
    if observed_through_value <= started_before_value:
        raise RuntimeError("evaluation observation must extend beyond the call window")
    if _seconds_between(started_before_value, observed_through_value) > (
        _MAX_OBSERVATION_LAG_SECONDS
    ):
        raise RuntimeError("evaluation observation exceeds its lag limit")

    census_hash = _sha256_text(window["census_sha256"], "evaluation census sha256")
    review_hash = _sha256_text(window["review_sha256"], "evaluation review sha256")
    if census_hash == review_hash:
        raise RuntimeError("evaluation census and review identities must be distinct")
    census_url, evidence_revision = _evidence_url(
        window["census_url"], role="census", digest=census_hash
    )
    review_url, review_revision = _evidence_url(
        window["review_url"], role="review", digest=review_hash
    )
    if evidence_revision != review_revision:
        raise RuntimeError("evaluation census and review revisions must match")
    for value, seen in (
        (census_url, evidence_urls),
        (review_url, evidence_urls),
        (census_hash, evidence_hashes),
        (review_hash, evidence_hashes),
    ):
        _claim_unique(value, seen, "evaluation evidence identity")

    raw_calls = _list(window["calls"], "window calls")
    if len(raw_calls) > _MAX_CALLS_PER_WINDOW:
        raise RuntimeError("evaluation window exceeds its call limit")
    calls: list[_CallIdentity] = []
    previous_key: tuple[datetime, str, int, str] | None = None
    for call_index, item in enumerate(raw_calls):
        call_identity, key = _call_identity(
            _object(item, "agent-tool call"),
            index=call_index,
            started_from_value=started_from_value,
            started_before_value=started_before_value,
            evidence_revision=evidence_revision,
            session_next_index=session_next_index,
            evidence_urls=evidence_urls,
            evidence_hashes=evidence_hashes,
        )
        if previous_key is not None and key <= previous_key:
            raise RuntimeError("agent-tool calls must follow canonical order")
        previous_key = key
        calls.append(call_identity)

    reviews = (
        _required_true(
            window["task_directed_session_census_complete_reviewed"],
            "task-directed session census completeness review",
        ),
        _required_true(window["eligibility_reviewed"], "evaluation eligibility review"),
        _required_true(
            window["manual_recovery_definition_reviewed"], "manual recovery definition review"
        ),
        _required_true(window["privacy_and_consent_reviewed"], "privacy and consent review"),
        _required_true(window["provenance_reviewed"], "evaluation provenance review"),
        _required_true(window["validation_reviewed"], "evaluation validation review"),
    )
    identity: _WindowIdentity = (
        window_id,
        started_from,
        started_before,
        observed_through,
        census_url,
        census_hash,
        review_url,
        review_hash,
        tuple(calls),
        *reviews,
    )
    return identity, started_before_value


def _call_identity(
    record: dict[str, object],
    *,
    index: int,
    started_from_value: datetime,
    started_before_value: datetime,
    evidence_revision: str,
    session_next_index: dict[str, int],
    evidence_urls: set[str],
    evidence_hashes: set[str],
) -> tuple[_CallIdentity, tuple[datetime, str, int, str]]:
    _exact_fields(
        record,
        {
            "call_id",
            "session_id",
            "session_call_index",
            "adapter_id",
            "tool_name",
            "service_protocol",
            "engine_sha",
            "service_contract_url",
            "service_contract_sha256",
            "started_at",
            "outcome",
            "manual_recovery_occurred",
            "outcome_code",
            "call_evidence_url",
            "call_evidence_sha256",
            "result_evidence_url",
            "result_evidence_sha256",
            "recovery_evidence_url",
            "recovery_evidence_sha256",
            "eligible_call_reviewed",
            "task_directed_context_reviewed",
            "manual_recovery_reviewed",
            "outcome_reviewed",
            "privacy_and_consent_reviewed",
            "provenance_reviewed",
            "validation_reviewed",
        },
        "agent-tool call",
    )
    call_id = _bounded_ascii_text(record["call_id"], 16, "call ID")
    if call_id != f"call-{index + 1:04d}":
        raise RuntimeError("agent-tool calls must use canonical sequential IDs")
    session_id = _slug(record["session_id"], 64, "session ID")
    session_call_index = _positive_int(
        record["session_call_index"], _MAX_SESSION_CALL_INDEX, "session call index"
    )
    expected_index = session_next_index.get(session_id, 1)
    if session_call_index != expected_index:
        raise RuntimeError("session call indices must be complete and sequential")
    session_next_index[session_id] = expected_index + 1
    adapter_id = _adapter_id(record["adapter_id"])
    tool_name = _bounded_ascii_text(record["tool_name"], 32, "agent tool name")
    if tool_name not in _TOOL_NAMES:
        raise RuntimeError("agent tool name is not registered")
    service_protocol = _bounded_ascii_text(record["service_protocol"], 40, "service protocol")
    if service_protocol != _SERVICE_PROTOCOL:
        raise RuntimeError("agent service protocol is incompatible")
    engine_sha = _git_sha(record["engine_sha"], "engine revision")
    service_contract_url = _source_url(record["service_contract_url"], engine_sha)
    service_contract_hash = _sha256_text(
        record["service_contract_sha256"], "service contract sha256"
    )
    started_at, started_at_value = _utc_timestamp(record["started_at"], "call timestamp")
    if not started_from_value <= started_at_value < started_before_value:
        raise RuntimeError("agent-tool call falls outside its evaluation window")

    outcome = _bounded_ascii_text(record["outcome"], 48, "call outcome")
    if outcome not in {
        "completed-without-manual-recovery",
        "completed-after-manual-recovery",
        "not-completed",
        "terminal-unobserved",
    }:
        raise RuntimeError("agent-tool call outcome is incompatible")
    recovery_occurred = _nullable_bool(
        record["manual_recovery_occurred"], "manual recovery occurrence"
    )
    outcome_code = _bounded_ascii_text(record["outcome_code"], 48, "call outcome code")
    call_hash = _sha256_text(record["call_evidence_sha256"], "call evidence sha256")
    call_url, call_revision = _evidence_url(
        record["call_evidence_url"], role="call", digest=call_hash
    )
    result_hash = _nullable_sha256_text(record["result_evidence_sha256"], "result evidence sha256")
    result_url, result_revision = _nullable_evidence_url(
        record["result_evidence_url"], role="result", digest=result_hash
    )
    recovery_hash = _nullable_sha256_text(
        record["recovery_evidence_sha256"], "recovery evidence sha256"
    )
    recovery_url, recovery_revision = _nullable_evidence_url(
        record["recovery_evidence_url"], role="recovery", digest=recovery_hash
    )
    revisions = {call_revision}
    if result_revision is not None:
        revisions.add(result_revision)
    if recovery_revision is not None:
        revisions.add(recovery_revision)
    if revisions != {evidence_revision}:
        raise RuntimeError("call evidence revision must match its evaluation evidence")
    _validate_outcome_evidence(
        outcome=outcome,
        recovery_occurred=recovery_occurred,
        outcome_code=outcome_code,
        result_url=result_url,
        result_hash=result_hash,
        recovery_url=recovery_url,
        recovery_hash=recovery_hash,
    )
    for value, seen in (
        (call_url, evidence_urls),
        (call_hash, evidence_hashes),
        (result_url, evidence_urls),
        (result_hash, evidence_hashes),
        (recovery_url, evidence_urls),
        (recovery_hash, evidence_hashes),
    ):
        if value is not None:
            _claim_unique(value, seen, "call evidence identity")

    reviews = (
        _required_true(record["eligible_call_reviewed"], "call eligibility review"),
        _required_true(record["task_directed_context_reviewed"], "task context review"),
        _required_true(record["manual_recovery_reviewed"], "manual recovery review"),
        _required_true(record["outcome_reviewed"], "call outcome review"),
        _required_true(record["privacy_and_consent_reviewed"], "privacy and consent review"),
        _required_true(record["provenance_reviewed"], "call provenance review"),
        _required_true(record["validation_reviewed"], "call validation review"),
    )
    identity: _CallIdentity = (
        call_id,
        session_id,
        session_call_index,
        adapter_id,
        tool_name,
        service_protocol,
        engine_sha,
        service_contract_url,
        service_contract_hash,
        started_at,
        outcome,
        recovery_occurred,
        outcome_code,
        call_url,
        call_hash,
        result_url,
        result_hash,
        recovery_url,
        recovery_hash,
        *reviews,
    )
    return identity, (started_at_value, session_id, session_call_index, tool_name)


def _validate_outcome_evidence(
    *,
    outcome: str,
    recovery_occurred: bool | None,
    outcome_code: str,
    result_url: str | None,
    result_hash: str | None,
    recovery_url: str | None,
    recovery_hash: str | None,
) -> None:
    result_present = result_url is not None and result_hash is not None
    recovery_present = recovery_url is not None and recovery_hash is not None
    if outcome == "completed-without-manual-recovery":
        if (
            recovery_occurred is not False
            or outcome_code != "tool-call-completed"
            or not result_present
            or recovery_present
        ):
            raise RuntimeError("recovery-free completion evidence is inconsistent")
    elif outcome == "completed-after-manual-recovery":
        if (
            recovery_occurred is not True
            or outcome_code != "tool-call-completed-after-manual-recovery"
            or not result_present
            or not recovery_present
        ):
            raise RuntimeError("manual-recovery completion evidence is inconsistent")
    elif outcome == "not-completed":
        if (
            type(recovery_occurred) is not bool
            or outcome_code not in _NOT_COMPLETED_CODES
            or not result_present
            or recovery_present is not recovery_occurred
        ):
            raise RuntimeError("non-completion evidence is inconsistent")
    elif (
        recovery_occurred is not None
        or outcome_code not in _UNOBSERVED_CODES
        or result_present
        or recovery_present
    ):
        raise RuntimeError("unobserved terminal evidence is inconsistent")


def _default_manifest() -> Path:
    bundled = Path(__file__).resolve().parent / "assets" / "agent_tool_recovery_rate.json"
    if bundled.is_file():
        return bundled
    return Path(__file__).resolve().parents[1] / "tests" / "fixtures" / bundled.name


def _path(value: object) -> Path:
    if not isinstance(value, Path):
        raise RuntimeError("agent-tool recovery manifest argument is invalid")
    return value


def _read_bounded(path: Path, limit: int, label: str) -> bytes:
    try:
        if path.is_symlink():
            raise RuntimeError(f"{label} must not be a symbolic link")
        with path.open("rb") as stream:
            payload = stream.read(limit + 1)
    except RuntimeError:
        raise
    except OSError as error:
        raise RuntimeError(f"{label} is unavailable") from error
    if len(payload) > limit:
        raise RuntimeError(f"{label} exceeds its byte limit")
    return payload


def _loads(payload: bytes, label: str) -> object:
    try:
        text = payload.decode("utf-8")
        value = json.loads(text, object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"{label} is not valid JSON") from error
    if _json_depth(value) > _MAX_JSON_NESTING:
        raise RuntimeError(f"{label} exceeds its nesting limit")
    return value


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    document: dict[str, object] = {}
    for key, value in pairs:
        if key in document:
            raise ValueError("duplicate JSON field")
        document[key] = value
    return document


def _json_depth(value: object) -> int:
    if isinstance(value, dict):
        mapping = cast(dict[object, object], value)
        return 1 + max((_json_depth(item) for item in mapping.values()), default=0)
    if isinstance(value, list):
        items = cast(list[object], value)
        return 1 + max((_json_depth(item) for item in items), default=0)
    return 0


def _object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _list(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise RuntimeError(f"{label} must be an array")
    return cast(list[object], value)


def _exact_fields(document: dict[str, object], expected: set[str], label: str) -> None:
    if set(document) != expected:
        raise RuntimeError(f"{label} fields are incompatible")


def _bounded_ascii_text(value: object, limit: int, label: str) -> str:
    if not isinstance(value, str) or not value or len(value) > limit or not value.isascii():
        raise RuntimeError(f"{label} is invalid")
    return value


def _slug(value: object, limit: int, label: str) -> str:
    text = _bounded_ascii_text(value, limit, label)
    if (
        text != text.lower()
        or text[0] not in "abcdefghijklmnopqrstuvwxyz0123456789"
        or text[-1] not in "abcdefghijklmnopqrstuvwxyz0123456789"
        or any(character not in "abcdefghijklmnopqrstuvwxyz0123456789-" for character in text)
    ):
        raise RuntimeError(f"{label} is invalid")
    return text


def _adapter_id(value: object) -> str:
    text = _bounded_ascii_text(value, 96, "adapter ID")
    parts = text.split(".")
    if len(parts) < 2 or any(_invalid_adapter_part(part) for part in parts):
        raise RuntimeError("adapter ID is invalid")
    return text


def _invalid_adapter_part(part: str) -> bool:
    return (
        not part
        or part != part.lower()
        or part[0] not in "abcdefghijklmnopqrstuvwxyz0123456789"
        or part[-1] not in "abcdefghijklmnopqrstuvwxyz0123456789"
        or any(character not in "abcdefghijklmnopqrstuvwxyz0123456789-" for character in part)
    )


def _positive_int(value: object, maximum: int, label: str) -> int:
    if type(value) is not int or not 1 <= value <= maximum:
        raise RuntimeError(f"{label} is invalid")
    return value


def _nullable_bool(value: object, label: str) -> bool | None:
    if value is not None and type(value) is not bool:
        raise RuntimeError(f"{label} is invalid")
    return value


def _required_true(value: object, label: str) -> bool:
    if value is not True:
        raise RuntimeError(f"{label} must be true")
    return True


def _git_sha(value: object, label: str) -> str:
    text = _bounded_ascii_text(value, 40, label)
    if len(text) != 40 or any(character not in "0123456789abcdef" for character in text):
        raise RuntimeError(f"{label} is invalid")
    return text


def _sha256_text(value: object, label: str) -> str:
    text = _bounded_ascii_text(value, 64, label)
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise RuntimeError(f"{label} is invalid")
    return text


def _nullable_sha256_text(value: object, label: str) -> str | None:
    return None if value is None else _sha256_text(value, label)


def _source_url(value: object, engine_sha: str) -> str:
    expected = f"{_PROJECT_URL}/blob/{engine_sha}/src/ludoweave/agent/tools.py"
    if value != expected:
        raise RuntimeError("service contract URL is invalid")
    return expected


def _evidence_url(value: object, *, role: str, digest: str) -> tuple[str, str]:
    text = _bounded_ascii_text(value, 256, f"{role} evidence URL")
    prefix = f"{_PROJECT_URL}/blob/"
    suffix = f"/evidence/agent-tool-recovery-rate/{role}-{digest}.json"
    if not text.startswith(prefix) or not text.endswith(suffix):
        raise RuntimeError(f"{role} evidence URL is invalid")
    revision = text[len(prefix) : -len(suffix)]
    if "/" in revision or _git_sha(revision, f"{role} evidence revision") != revision:
        raise RuntimeError(f"{role} evidence URL is invalid")
    return text, revision


def _nullable_evidence_url(
    value: object, *, role: str, digest: str | None
) -> tuple[str | None, str | None]:
    if value is None and digest is None:
        return None, None
    if value is None or digest is None:
        raise RuntimeError(f"{role} evidence URL and digest must appear together")
    return _evidence_url(value, role=role, digest=digest)


def _utc_timestamp(value: object, label: str) -> tuple[str, datetime]:
    text = _bounded_ascii_text(value, 20, label)
    try:
        parsed = datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except ValueError as error:
        raise RuntimeError(f"{label} is invalid") from error
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != text:
        raise RuntimeError(f"{label} is invalid")
    return text, parsed


def _seconds_between(start: datetime, end: datetime) -> int:
    return int((end - start).total_seconds())


def _claim_unique(value: str, seen: set[str], label: str) -> None:
    if value in seen:
        raise RuntimeError(f"{label} must be unique")
    seen.add(value)


if __name__ == "__main__":
    raise SystemExit(main())
