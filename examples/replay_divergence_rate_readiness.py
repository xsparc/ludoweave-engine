"""Evaluate reviewed CI replay-divergence evidence without inferring a zero rate."""

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

type _ExecutionIdentity = tuple[
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str | None,
    str | None,
    int | None,
    str,
    str,
    str,
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
    tuple[_ExecutionIdentity, ...],
    bool,
    bool,
    bool,
    bool,
]

_SCHEMA = "ludoweave.evaluation.replay-divergence-rate-readiness/1"
_MANIFEST_SCHEMA = "ludoweave.ci.replay-divergence-rate/1"
_MEASUREMENT_POLICY = "complete-reviewed-ci-replay-executions/1"
_REVIEWED_MANIFEST_SHA256 = "cff8a32428ac8dcd18029be4f70e9d359b4c9d70fd411ffe2f36d35704d68aa7"
_MANDATORY_WINDOW_PREFIX: tuple[_WindowIdentity, ...] = ()
_MAX_MANIFEST_BYTES = 65_536
_MAX_JSON_NESTING = 16
_MAX_EVALUATION_WINDOWS = 12
_MAX_EXECUTIONS_PER_WINDOW = 512
_MAX_WINDOW_SECONDS = 31_622_400
_MAX_OBSERVATION_LAG_SECONDS = 31_622_400
_MAX_DIVERGENT_TICK = 9_223_372_036_854_775_807
_PROJECT_URL = "https://github.com/xsparc/ludoweave-engine"
_NON_EXECUTION_CODES = {
    "job-cancelled",
    "job-failed-before-replay",
    "replay-case-skipped",
    "result-evidence-unavailable",
}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="explicit local reviewed CI replay-divergence manifest",
    )
    arguments = parser.parse_args(tuple(sys.argv[1:] if argv is None else argv))
    selected: object = getattr(arguments, "manifest", None)
    manifest = _default_manifest() if selected is None else _path(selected)
    print(json.dumps(evaluate(manifest), ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0


def evaluate(manifest: Path) -> dict[str, object]:
    """Return deterministic, path-free CI replay-divergence admission evidence."""

    raw_manifest, identities = _parse_manifest(manifest)
    manifest_hash = hashlib.sha256(raw_manifest).hexdigest()
    manifest_identity_reviewed = manifest_hash == _REVIEWED_MANIFEST_SHA256
    historical_windows_preserved = tuple(
        identities[: len(_MANDATORY_WINDOW_PREFIX)]
    ) == _MANDATORY_WINDOW_PREFIX and (
        not manifest_identity_reviewed or len(identities) == len(_MANDATORY_WINDOW_PREFIX)
    )
    admitted = identities if manifest_identity_reviewed and historical_windows_preserved else ()
    executions = tuple(execution for window in admitted for execution in window[8])
    verified_count = sum(execution[10] == "verified" for execution in executions)
    diverged_count = sum(execution[10] == "diverged" for execution in executions)
    not_executed_count = sum(execution[10] == "not-executed" for execution in executions)
    complete_reviewed_windows = bool(admitted)
    replay_executions_present = bool(executions)
    replay_execution_cohort_complete = replay_executions_present and not_executed_count == 0
    gate_satisfied = (
        manifest_identity_reviewed
        and historical_windows_preserved
        and complete_reviewed_windows
        and replay_executions_present
        and replay_execution_cohort_complete
    )
    reasons: list[str]
    if manifest_identity_reviewed and historical_windows_preserved and not identities:
        reasons = ["replay-divergence-rate-evidence-absent"]
    else:
        reasons = []
        if not manifest_identity_reviewed:
            reasons.append("replay-divergence-manifest-identity-unreviewed")
        if not historical_windows_preserved:
            reasons.append("historical-evaluation-window-missing")
        if not complete_reviewed_windows:
            reasons.append("complete-reviewed-evaluation-window-absent")
        if not replay_executions_present:
            reasons.append("reviewed-replay-execution-absent")
        if replay_executions_present and not replay_execution_cohort_complete:
            reasons.append("replay-execution-cohort-incomplete")

    divergence_rate: dict[str, int] | None = None
    if gate_satisfied:
        divergence_rate = {"denominator": len(executions), "numerator": diverged_count}
    return {
        "admission": {
            "complete_reviewed_windows": complete_reviewed_windows,
            "historical_windows_preserved": historical_windows_preserved,
            "manifest_identity_reviewed": manifest_identity_reviewed,
            "replay_execution_cohort_complete": replay_execution_cohort_complete,
            "replay_executions_present": replay_executions_present,
            "reason_codes": tuple(reasons),
        },
        "divergence_rate_proven": gate_satisfied,
        "evidence_level": (
            "reviewed-ci-replay-divergence-rate"
            if gate_satisfied
            else "ci-replay-divergence-rate-admission-readiness"
        ),
        "gate_satisfied": gate_satisfied,
        "ludoweave_version": __version__,
        "metrics": {
            "diverged_count": diverged_count,
            "divergence_rate": divergence_rate,
            "execution_count": len(executions),
            "manifest_sha256": manifest_hash,
            "measurement_policy": _MEASUREMENT_POLICY,
            "not_executed_count": not_executed_count,
            "records_verified": True,
            "verified_count": verified_count,
            "window_count": len(admitted),
        },
        "schema": _SCHEMA,
        "status": "ready" if gate_satisfied else "not-ready",
    }


def _parse_manifest(path: Path) -> tuple[bytes, tuple[_WindowIdentity, ...]]:
    raw_manifest = _read_bounded(path, _MAX_MANIFEST_BYTES, "replay-divergence manifest")
    document = _object(
        _loads(raw_manifest, "replay-divergence manifest"), "replay-divergence manifest"
    )
    _exact_fields(
        document,
        {"schema", "source_project", "measurement_policy", "evaluation_windows"},
        "replay-divergence manifest",
    )
    if document["schema"] != _MANIFEST_SCHEMA:
        raise RuntimeError("replay-divergence manifest schema is incompatible")
    if document["source_project"] != "ludoweave-engine":
        raise RuntimeError("replay-divergence project identity is invalid")
    if document["measurement_policy"] != _MEASUREMENT_POLICY:
        raise RuntimeError("replay-divergence measurement policy is incompatible")

    raw_windows = _list(document["evaluation_windows"], "evaluation windows")
    if len(raw_windows) > _MAX_EVALUATION_WINDOWS:
        raise RuntimeError("replay-divergence manifest exceeds its window limit")
    identities: list[_WindowIdentity] = []
    execution_keys: set[str] = set()
    evidence_urls: set[str] = set()
    evidence_hashes: set[str] = set()
    previous_started_before: datetime | None = None
    for index, item in enumerate(raw_windows):
        identity, started_before = _window_identity(
            _object(item, "evaluation window"),
            index=index,
            previous_started_before=previous_started_before,
            execution_keys=execution_keys,
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
    execution_keys: set[str],
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
            "executions",
            "public_ci_census_complete_reviewed",
            "eligibility_reviewed",
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
        raise RuntimeError("evaluation observation must extend beyond the execution window")
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
    for value, seen, role in (
        (census_url, evidence_urls, "evaluation evidence URL"),
        (review_url, evidence_urls, "evaluation evidence URL"),
        (census_hash, evidence_hashes, "evaluation evidence sha256"),
        (review_hash, evidence_hashes, "evaluation evidence sha256"),
    ):
        _claim_unique(value, seen, role)

    raw_executions = _list(window["executions"], "window executions")
    if len(raw_executions) > _MAX_EXECUTIONS_PER_WINDOW:
        raise RuntimeError("evaluation window exceeds its execution limit")
    executions: list[_ExecutionIdentity] = []
    previous_key: tuple[datetime, int, int, str] | None = None
    for execution_index, item in enumerate(raw_executions):
        execution_identity, key = _execution_identity(
            _object(item, "replay execution"),
            index=execution_index,
            started_from_value=started_from_value,
            started_before_value=started_before_value,
            evidence_revision=evidence_revision,
            execution_keys=execution_keys,
            evidence_urls=evidence_urls,
            evidence_hashes=evidence_hashes,
        )
        if previous_key is not None and key <= previous_key:
            raise RuntimeError("replay executions must follow canonical order")
        previous_key = key
        executions.append(execution_identity)

    public_ci_census_complete_reviewed = _required_true(
        window["public_ci_census_complete_reviewed"], "public CI census completeness review"
    )
    eligibility_reviewed = _required_true(
        window["eligibility_reviewed"], "evaluation eligibility review"
    )
    provenance_reviewed = _required_true(
        window["provenance_reviewed"], "evaluation provenance review"
    )
    validation_reviewed = _required_true(
        window["validation_reviewed"], "evaluation validation review"
    )
    window_identity: _WindowIdentity = (
        window_id,
        started_from,
        started_before,
        observed_through,
        census_url,
        census_hash,
        review_url,
        review_hash,
        tuple(executions),
        public_ci_census_complete_reviewed,
        eligibility_reviewed,
        provenance_reviewed,
        validation_reviewed,
    )
    return window_identity, started_before_value


def _execution_identity(
    record: dict[str, object],
    *,
    index: int,
    started_from_value: datetime,
    started_before_value: datetime,
    evidence_revision: str,
    execution_keys: set[str],
    evidence_urls: set[str],
    evidence_hashes: set[str],
) -> tuple[_ExecutionIdentity, tuple[datetime, int, int, str]]:
    _exact_fields(
        record,
        {
            "execution_id",
            "run_url",
            "job_url",
            "head_sha",
            "workflow_url",
            "workflow_sha256",
            "case_id",
            "case_url",
            "case_sha256",
            "started_at",
            "outcome",
            "expected_state_sha256",
            "actual_state_sha256",
            "first_divergent_tick",
            "outcome_code",
            "result_url",
            "result_sha256",
            "eligible_execution_reviewed",
            "outcome_reviewed",
            "provenance_reviewed",
            "validation_reviewed",
        },
        "replay execution",
    )
    execution_id = _bounded_ascii_text(record["execution_id"], 20, "execution ID")
    if execution_id != f"execution-{index + 1:04d}":
        raise RuntimeError("replay executions must use canonical sequential IDs")
    run_url, run_number = _run_url(record["run_url"])
    job_url, job_number = _job_url(record["job_url"], run_url)
    head_sha = _git_sha(record["head_sha"], "execution head sha")
    workflow_url = _workflow_url(record["workflow_url"], head_sha)
    workflow_hash = _sha256_text(record["workflow_sha256"], "workflow sha256")
    case_id = _case_id(record["case_id"])
    case_url = _case_url(record["case_url"], head_sha)
    case_hash = _sha256_text(record["case_sha256"], "replay case sha256")
    started_at, started_at_value = _utc_timestamp(record["started_at"], "execution timestamp")
    if not started_from_value <= started_at_value < started_before_value:
        raise RuntimeError("replay execution falls outside its evaluation window")
    execution_key = f"{run_number}:{job_number}:{case_id}"
    _claim_unique(execution_key, execution_keys, "replay execution identity")

    outcome = _bounded_ascii_text(record["outcome"], 16, "replay outcome")
    if outcome not in {"verified", "diverged", "not-executed"}:
        raise RuntimeError("replay outcome is incompatible")
    expected_hash = _nullable_sha256_text(record["expected_state_sha256"], "expected state sha256")
    actual_hash = _nullable_sha256_text(record["actual_state_sha256"], "actual state sha256")
    first_divergent_tick = _nullable_non_negative_int(
        record["first_divergent_tick"], _MAX_DIVERGENT_TICK, "first divergent tick"
    )
    outcome_code = _bounded_ascii_text(record["outcome_code"], 40, "replay outcome code")
    if outcome == "verified":
        if (
            expected_hash is None
            or actual_hash is None
            or expected_hash != actual_hash
            or first_divergent_tick is not None
            or outcome_code != "replay-verified"
        ):
            raise RuntimeError("verified replay execution has incompatible outcome evidence")
    elif outcome == "diverged":
        if (
            expected_hash is None
            or actual_hash is None
            or expected_hash == actual_hash
            or first_divergent_tick is None
            or outcome_code != "world.replay.diverged"
        ):
            raise RuntimeError("diverged replay execution has incompatible outcome evidence")
    elif (
        expected_hash is not None
        or actual_hash is not None
        or first_divergent_tick is not None
        or outcome_code not in _NON_EXECUTION_CODES
    ):
        raise RuntimeError("non-executed replay case must not claim replay outcome evidence")

    result_hash = _sha256_text(record["result_sha256"], "execution result sha256")
    result_url, result_revision = _evidence_url(
        record["result_url"], role="result", digest=result_hash
    )
    if result_revision != evidence_revision:
        raise RuntimeError("execution result revision must match its evaluation evidence")
    _claim_unique(result_url, evidence_urls, "execution result URL")
    _claim_unique(result_hash, evidence_hashes, "execution result sha256")
    eligible_execution_reviewed = _required_true(
        record["eligible_execution_reviewed"], "eligible replay execution review"
    )
    outcome_reviewed = _required_true(record["outcome_reviewed"], "replay outcome review")
    provenance_reviewed = _required_true(
        record["provenance_reviewed"], "execution provenance review"
    )
    validation_reviewed = _required_true(
        record["validation_reviewed"], "execution validation review"
    )
    identity: _ExecutionIdentity = (
        execution_id,
        run_url,
        job_url,
        head_sha,
        workflow_url,
        workflow_hash,
        case_id,
        case_url,
        case_hash,
        started_at,
        outcome,
        expected_hash,
        actual_hash,
        first_divergent_tick,
        outcome_code,
        result_url,
        result_hash,
        eligible_execution_reviewed,
        outcome_reviewed,
        provenance_reviewed,
        validation_reviewed,
    )
    return identity, (started_at_value, run_number, job_number, case_id)


def _default_manifest() -> Path:
    bundled = Path(__file__).resolve().parent / "assets" / "replay_divergence_rate.json"
    if bundled.is_file():
        return bundled
    return Path(__file__).resolve().parents[1] / "tests" / "fixtures" / bundled.name


def _read_bounded(path: Path, maximum: int, role: str) -> bytes:
    try:
        if path.is_symlink():
            raise RuntimeError(f"{role} must not be a symbolic link")
        with path.open("rb") as stream:
            value = stream.read(maximum + 1)
    except OSError as error:
        raise RuntimeError(f"{role} is unavailable") from error
    if len(value) > maximum:
        raise RuntimeError(f"{role} exceeds its byte limit")
    return value


def _loads(value: bytes, role: str) -> object:
    _reject_excessive_nesting(value, role)
    try:
        return json.loads(value, object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError, ValueError) as error:
        raise RuntimeError(f"{role} is not valid JSON") from error


def _reject_excessive_nesting(value: bytes, role: str) -> None:
    depth = 0
    in_string = False
    escaped = False
    for character in value:
        if in_string:
            if escaped:
                escaped = False
            elif character == ord("\\"):
                escaped = True
            elif character == ord('"'):
                in_string = False
            continue
        if character == ord('"'):
            in_string = True
        elif character in (ord("{"), ord("[")):
            depth += 1
            if depth > _MAX_JSON_NESTING:
                raise RuntimeError(f"{role} exceeds its nesting limit")
        elif character in (ord("}"), ord("]")) and depth > 0:
            depth -= 1


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def _exact_fields(value: dict[str, object], expected: set[str], role: str) -> None:
    if set(value) != expected:
        raise RuntimeError(f"{role} fields are incompatible")


def _path(value: object) -> Path:
    if not isinstance(value, Path):
        raise TypeError("manifest must be a path")
    return value


def _object(value: object, role: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise RuntimeError(f"{role} must be an object")
    return cast(dict[str, object], value)


def _list(value: object, role: str) -> list[object]:
    if not isinstance(value, list):
        raise RuntimeError(f"{role} must be a list")
    return cast(list[object], value)


def _bounded_ascii_text(value: object, maximum: int, role: str) -> str:
    if type(value) is not str or not value or len(value) > maximum:
        raise RuntimeError(f"{role} is invalid")
    text = value
    if not text.isascii() or text != text.strip():
        raise RuntimeError(f"{role} is invalid")
    return text


def _sha256_text(value: object, role: str) -> str:
    text = _bounded_ascii_text(value, 64, role)
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise RuntimeError(f"{role} is invalid")
    return text


def _nullable_sha256_text(value: object, role: str) -> str | None:
    if value is None:
        return None
    return _sha256_text(value, role)


def _git_sha(value: object, role: str) -> str:
    text = _bounded_ascii_text(value, 40, role)
    if len(text) != 40 or any(character not in "0123456789abcdef" for character in text):
        raise RuntimeError(f"{role} is invalid")
    return text


def _utc_timestamp(value: object, role: str) -> tuple[str, datetime]:
    text = _bounded_ascii_text(value, 20, role)
    digit_indexes = (*range(4), 5, 6, 8, 9, 11, 12, 14, 15, 17, 18)
    if (
        len(text) != 20
        or text[4] != "-"
        or text[7] != "-"
        or text[10] != "T"
        or text[13] != ":"
        or text[16] != ":"
        or text[19] != "Z"
        or any(not text[index].isascii() or not text[index].isdecimal() for index in digit_indexes)
    ):
        raise RuntimeError(f"{role} is invalid")
    try:
        parsed = datetime(
            int(text[:4]),
            int(text[5:7]),
            int(text[8:10]),
            int(text[11:13]),
            int(text[14:16]),
            int(text[17:19]),
            tzinfo=UTC,
        )
    except ValueError as error:
        raise RuntimeError(f"{role} is invalid") from error
    return text, parsed


def _seconds_between(earlier: datetime, later: datetime) -> int:
    return int((later - earlier).total_seconds())


def _run_url(value: object) -> tuple[str, int]:
    text = _bounded_ascii_text(value, 128, "workflow run URL")
    prefix = f"{_PROJECT_URL}/actions/runs/"
    number = text.removeprefix(prefix) if text.startswith(prefix) else ""
    if not _canonical_positive_decimal(number):
        raise RuntimeError("workflow run URL is incompatible")
    return text, int(number)


def _job_url(value: object, run_url: str) -> tuple[str, int]:
    text = _bounded_ascii_text(value, 160, "workflow job URL")
    prefix = f"{run_url}/job/"
    number = text.removeprefix(prefix) if text.startswith(prefix) else ""
    if not _canonical_positive_decimal(number):
        raise RuntimeError("workflow job URL is incompatible")
    return text, int(number)


def _workflow_url(value: object, head_sha: str) -> str:
    text = _bounded_ascii_text(value, 256, "workflow source URL")
    expected = f"{_PROJECT_URL}/blob/{head_sha}/.github/workflows/ci.yml"
    if text != expected:
        raise RuntimeError("workflow source URL is incompatible")
    return text


def _case_id(value: object) -> str:
    text = _bounded_ascii_text(value, 64, "replay case ID")
    if (
        not text[0].islower()
        or not text[0].isascii()
        or any(character not in "abcdefghijklmnopqrstuvwxyz0123456789.-" for character in text)
        or text.endswith((".", "-"))
        or ".." in text
    ):
        raise RuntimeError("replay case ID is incompatible")
    return text


def _case_url(value: object, head_sha: str) -> str:
    text = _bounded_ascii_text(value, 384, "replay case source URL")
    prefix = f"{_PROJECT_URL}/blob/{head_sha}/"
    relative = text.removeprefix(prefix) if text.startswith(prefix) else ""
    parts = relative.split("/")
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
    if (
        len(parts) < 2
        or parts[0] != "tests"
        or not parts[-1].endswith(".py")
        or any(
            not part or part in {".", ".."} or any(character not in allowed for character in part)
            for part in parts
        )
    ):
        raise RuntimeError("replay case source URL is incompatible")
    return text


def _evidence_url(value: object, *, role: str, digest: str) -> tuple[str, str]:
    text = _bounded_ascii_text(value, 384, f"evaluation {role} URL")
    prefix = f"{_PROJECT_URL}/blob/"
    if not text.startswith(prefix):
        raise RuntimeError(f"evaluation {role} URL is incompatible")
    parts = text.removeprefix(prefix).split("/")
    if len(parts) != 4:
        raise RuntimeError(f"evaluation {role} URL is incompatible")
    revision, directory, subdirectory, filename = parts
    if (
        len(revision) != 40
        or any(character not in "0123456789abcdef" for character in revision)
        or directory != "evidence"
        or subdirectory != "replay-divergence-rate"
        or filename != f"{role}-{digest}.json"
    ):
        raise RuntimeError(f"evaluation {role} URL is incompatible")
    return text, revision


def _canonical_positive_decimal(value: str) -> bool:
    return value.isascii() and value.isdecimal() and value != "0" and not value.startswith("0")


def _nullable_non_negative_int(value: object, maximum: int, role: str) -> int | None:
    if value is None:
        return None
    if type(value) is not int or value < 0 or value > maximum:
        raise RuntimeError(f"{role} is invalid")
    return value


def _required_true(value: object, role: str) -> bool:
    if type(value) is not bool or value is not True:
        raise RuntimeError(f"{role} must be true")
    return True


def _claim_unique(value: str, seen: set[str], role: str) -> None:
    if value in seen:
        raise RuntimeError(f"{role} is repeated")
    seen.add(value)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from error
