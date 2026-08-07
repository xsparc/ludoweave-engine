"""Evaluate reviewed benchmark-regression evidence without inferring a zero rate."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from ludoweave import __version__

type _ComparisonIdentity = tuple[
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
    str,
    str,
    str,
    str,
    str,
    str,
    int,
    str,
    str,
    int | None,
    int | None,
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
    tuple[_ComparisonIdentity, ...],
    bool,
    bool,
    bool,
    bool,
    bool,
]

_SCHEMA = "ludoweave.evaluation.benchmark-regression-rate-readiness/1"
_MANIFEST_SCHEMA = "ludoweave.performance.benchmark-regression-rate/1"
_MEASUREMENT_POLICY = "complete-reviewed-controlled-benchmark-comparisons/1"
_REVIEWED_MANIFEST_SHA256 = "720ae794e2a4ba76303196cd43d6ba0f3b21f81cffd4fa8584f526e2a0d48dca"
_MANDATORY_WINDOW_PREFIX: tuple[_WindowIdentity, ...] = ()
_MAX_MANIFEST_BYTES = 131_072
_MAX_JSON_NESTING = 16
_MAX_EVALUATION_WINDOWS = 12
_MAX_COMPARISONS_PER_WINDOW = 512
_MAX_WINDOW_SECONDS = 31_622_400
_MAX_OBSERVATION_LAG_SECONDS = 31_622_400
_MAX_P95_NS = 9_223_372_036_854_775_807
_MAX_TOLERANCE_BPS = 10_000
_PROJECT_URL = "https://github.com/xsparc/ludoweave-engine"
_NON_EXECUTION_CODES = {
    "benchmark-case-skipped",
    "comparison-evidence-unavailable",
    "job-cancelled",
    "job-failed-before-benchmark",
}
_REGISTERED_WORKLOADS: Mapping[str, tuple[str, tuple[str, ...]]] = {
    "ludoweave.benchmark.m1/1": (
        "benchmarks/benchmark_m1.py",
        (
            "entity_lifecycle",
            "read_query_10000",
            "write_query_10000",
            "scheduler_plan_generated_dag",
            "command_buffer_staged_flush",
            "fixed_step_3600_ticks",
            "simulation_tick_10000",
        ),
    ),
    "ludoweave.benchmark.m2/1": (
        "benchmarks/benchmark_m2.py",
        (
            "canonical_transaction_100",
            "atomic_transaction_apply_100",
            "snapshot_roundtrip_1000",
            "replay_verify_100_batches",
        ),
    ),
    "ludoweave.benchmark.m3/1": (
        "benchmarks/benchmark_m3.py",
        (
            "extract_pack_1000",
            "extract_pack_10000",
            "null_submit_1000",
            "null_submit_10000",
            "wgpu_submit_1000",
            "wgpu_submit_10000",
        ),
    ),
    "ludoweave.benchmark.m4/1": (
        "benchmarks/benchmark_m4.py",
        (
            "clockwork_arena_stress_1",
            "clockwork_arena_stress_4",
            "clockwork_arena_stress_8",
        ),
    ),
}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="explicit local reviewed benchmark-regression manifest",
    )
    arguments = parser.parse_args(tuple(sys.argv[1:] if argv is None else argv))
    selected: object = getattr(arguments, "manifest", None)
    manifest = _default_manifest() if selected is None else _path(selected)
    print(json.dumps(evaluate(manifest), ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0


def evaluate(manifest: Path) -> dict[str, object]:
    """Return deterministic, path-free benchmark-regression admission evidence."""

    raw_manifest, identities = _parse_manifest(manifest)
    manifest_hash = hashlib.sha256(raw_manifest).hexdigest()
    manifest_identity_reviewed = manifest_hash == _REVIEWED_MANIFEST_SHA256
    historical_windows_preserved = tuple(
        identities[: len(_MANDATORY_WINDOW_PREFIX)]
    ) == _MANDATORY_WINDOW_PREFIX and (
        not manifest_identity_reviewed or len(identities) == len(_MANDATORY_WINDOW_PREFIX)
    )
    admitted = identities if manifest_identity_reviewed and historical_windows_preserved else ()
    comparisons = tuple(comparison for window in admitted for comparison in window[8])
    stable_count = sum(comparison[19] == "stable" for comparison in comparisons)
    regressed_count = sum(comparison[19] == "regressed" for comparison in comparisons)
    not_executed_count = sum(comparison[19] == "not-executed" for comparison in comparisons)
    complete_reviewed_windows = bool(admitted)
    benchmark_comparisons_present = bool(comparisons)
    comparison_cohort_complete = benchmark_comparisons_present and not_executed_count == 0
    gate_satisfied = (
        manifest_identity_reviewed
        and historical_windows_preserved
        and complete_reviewed_windows
        and benchmark_comparisons_present
        and comparison_cohort_complete
    )
    reasons: list[str]
    if manifest_identity_reviewed and historical_windows_preserved and not identities:
        reasons = ["benchmark-regression-rate-evidence-absent"]
    else:
        reasons = []
        if not manifest_identity_reviewed:
            reasons.append("benchmark-regression-manifest-identity-unreviewed")
        if not historical_windows_preserved:
            reasons.append("historical-evaluation-window-missing")
        if not complete_reviewed_windows:
            reasons.append("complete-reviewed-evaluation-window-absent")
        if not benchmark_comparisons_present:
            reasons.append("reviewed-benchmark-comparison-absent")
        if benchmark_comparisons_present and not comparison_cohort_complete:
            reasons.append("benchmark-comparison-cohort-incomplete")

    regression_rate: dict[str, int] | None = None
    if gate_satisfied:
        regression_rate = {
            "denominator": stable_count + regressed_count,
            "numerator": regressed_count,
        }
    return {
        "admission": {
            "benchmark_comparisons_present": benchmark_comparisons_present,
            "comparison_cohort_complete": comparison_cohort_complete,
            "complete_reviewed_windows": complete_reviewed_windows,
            "historical_windows_preserved": historical_windows_preserved,
            "manifest_identity_reviewed": manifest_identity_reviewed,
            "reason_codes": tuple(reasons),
        },
        "benchmark_regression_rate_proven": gate_satisfied,
        "evidence_level": (
            "reviewed-controlled-benchmark-regression-rate"
            if gate_satisfied
            else "benchmark-regression-rate-admission-readiness"
        ),
        "gate_satisfied": gate_satisfied,
        "ludoweave_version": __version__,
        "metrics": {
            "comparison_count": len(comparisons),
            "manifest_sha256": manifest_hash,
            "measurement_policy": _MEASUREMENT_POLICY,
            "not_executed_count": not_executed_count,
            "records_verified": True,
            "regressed_count": regressed_count,
            "regression_rate": regression_rate,
            "stable_count": stable_count,
            "window_count": len(admitted),
        },
        "schema": _SCHEMA,
        "status": "ready" if gate_satisfied else "not-ready",
    }


def _parse_manifest(path: Path) -> tuple[bytes, tuple[_WindowIdentity, ...]]:
    raw_manifest = _read_bounded(path, _MAX_MANIFEST_BYTES, "benchmark-regression manifest")
    document = _object(
        _loads(raw_manifest, "benchmark-regression manifest"), "benchmark-regression manifest"
    )
    _exact_fields(
        document,
        {"schema", "source_project", "measurement_policy", "evaluation_windows"},
        "benchmark-regression manifest",
    )
    if document["schema"] != _MANIFEST_SCHEMA:
        raise RuntimeError("benchmark-regression manifest schema is incompatible")
    if document["source_project"] != "ludoweave-engine":
        raise RuntimeError("benchmark-regression project identity is invalid")
    if document["measurement_policy"] != _MEASUREMENT_POLICY:
        raise RuntimeError("benchmark-regression measurement policy is incompatible")

    raw_windows = _list(document["evaluation_windows"], "evaluation windows")
    if len(raw_windows) > _MAX_EVALUATION_WINDOWS:
        raise RuntimeError("benchmark-regression manifest exceeds its window limit")
    identities: list[_WindowIdentity] = []
    comparison_keys: set[str] = set()
    evidence_urls: set[str] = set()
    evidence_hashes: set[str] = set()
    previous_started_before: datetime | None = None
    for index, item in enumerate(raw_windows):
        identity, started_before = _window_identity(
            _object(item, "evaluation window"),
            index=index,
            previous_started_before=previous_started_before,
            comparison_keys=comparison_keys,
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
    comparison_keys: set[str],
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
            "comparisons",
            "controlled_runner_census_complete_reviewed",
            "eligibility_reviewed",
            "comparability_reviewed",
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
        raise RuntimeError("evaluation observation must extend beyond the comparison window")
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

    raw_comparisons = _list(window["comparisons"], "window comparisons")
    if len(raw_comparisons) > _MAX_COMPARISONS_PER_WINDOW:
        raise RuntimeError("evaluation window exceeds its comparison limit")
    comparisons: list[_ComparisonIdentity] = []
    previous_key: tuple[datetime, int, int, str, str] | None = None
    for comparison_index, item in enumerate(raw_comparisons):
        comparison_identity, key = _comparison_identity(
            _object(item, "benchmark comparison"),
            index=comparison_index,
            started_from_value=started_from_value,
            started_before_value=started_before_value,
            evidence_revision=evidence_revision,
            comparison_keys=comparison_keys,
            evidence_urls=evidence_urls,
            evidence_hashes=evidence_hashes,
        )
        if previous_key is not None and key <= previous_key:
            raise RuntimeError("benchmark comparisons must follow canonical order")
        previous_key = key
        comparisons.append(comparison_identity)

    reviews = (
        _required_true(
            window["controlled_runner_census_complete_reviewed"],
            "controlled runner census completeness review",
        ),
        _required_true(window["eligibility_reviewed"], "evaluation eligibility review"),
        _required_true(window["comparability_reviewed"], "evaluation comparability review"),
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
        tuple(comparisons),
        *reviews,
    )
    return identity, started_before_value


def _comparison_identity(
    record: dict[str, object],
    *,
    index: int,
    started_from_value: datetime,
    started_before_value: datetime,
    evidence_revision: str,
    comparison_keys: set[str],
    evidence_urls: set[str],
    evidence_hashes: set[str],
) -> tuple[_ComparisonIdentity, tuple[datetime, int, int, str, str]]:
    _exact_fields(
        record,
        {
            "comparison_id",
            "run_url",
            "job_url",
            "base_sha",
            "head_sha",
            "workflow_url",
            "workflow_sha256",
            "benchmark_schema",
            "benchmark_case",
            "baseline_source_url",
            "baseline_source_sha256",
            "candidate_source_url",
            "candidate_source_sha256",
            "runner_profile_url",
            "runner_profile_sha256",
            "environment_profile",
            "metric",
            "tolerance_bps",
            "started_at",
            "outcome",
            "baseline_p95_ns",
            "candidate_p95_ns",
            "outcome_code",
            "result_url",
            "result_sha256",
            "baseline_artifact_url",
            "baseline_artifact_sha256",
            "candidate_artifact_url",
            "candidate_artifact_sha256",
            "eligible_comparison_reviewed",
            "comparability_reviewed",
            "threshold_predeclared_reviewed",
            "outcome_reviewed",
            "provenance_reviewed",
            "validation_reviewed",
        },
        "benchmark comparison",
    )
    comparison_id = _bounded_ascii_text(record["comparison_id"], 24, "comparison ID")
    if comparison_id != f"comparison-{index + 1:04d}":
        raise RuntimeError("benchmark comparisons must use canonical sequential IDs")
    run_url, run_number = _run_url(record["run_url"])
    job_url, job_number = _job_url(record["job_url"], run_url)
    base_sha = _git_sha(record["base_sha"], "base revision")
    head_sha = _git_sha(record["head_sha"], "candidate revision")
    if base_sha == head_sha:
        raise RuntimeError("benchmark comparison revisions must be distinct")
    workflow_url = _workflow_url(record["workflow_url"], head_sha)
    workflow_hash = _sha256_text(record["workflow_sha256"], "workflow sha256")
    benchmark_schema = _bounded_ascii_text(record["benchmark_schema"], 40, "benchmark schema")
    registration = _REGISTERED_WORKLOADS.get(benchmark_schema)
    if registration is None:
        raise RuntimeError("benchmark schema is not registered for comparison")
    source_path, workload_names = registration
    benchmark_case = _bounded_ascii_text(record["benchmark_case"], 64, "benchmark case")
    if benchmark_case not in workload_names:
        raise RuntimeError("benchmark case is not registered for its schema")
    baseline_source_url = _benchmark_source_url(
        record["baseline_source_url"], base_sha, source_path, "baseline"
    )
    baseline_source_hash = _sha256_text(record["baseline_source_sha256"], "baseline source sha256")
    candidate_source_url = _benchmark_source_url(
        record["candidate_source_url"], head_sha, source_path, "candidate"
    )
    candidate_source_hash = _sha256_text(
        record["candidate_source_sha256"], "candidate source sha256"
    )
    runner_profile_hash = _sha256_text(record["runner_profile_sha256"], "runner profile sha256")
    runner_profile_url, runner_revision = _evidence_url(
        record["runner_profile_url"], role="runner", digest=runner_profile_hash
    )
    if runner_revision != evidence_revision:
        raise RuntimeError("runner profile revision must match its evaluation evidence")
    environment_profile = _slug(record["environment_profile"], 80, "environment profile")
    metric = _bounded_ascii_text(record["metric"], 16, "comparison metric")
    if metric != "p95_ns":
        raise RuntimeError("benchmark comparison metric is incompatible")
    tolerance_bps = _non_negative_int(
        record["tolerance_bps"], _MAX_TOLERANCE_BPS, "comparison tolerance"
    )
    started_at, started_at_value = _utc_timestamp(record["started_at"], "comparison timestamp")
    if not started_from_value <= started_at_value < started_before_value:
        raise RuntimeError("benchmark comparison falls outside its evaluation window")
    comparison_key = f"{run_number}:{job_number}:{benchmark_schema}:{benchmark_case}"
    _claim_unique(comparison_key, comparison_keys, "benchmark comparison identity")

    outcome = _bounded_ascii_text(record["outcome"], 16, "benchmark outcome")
    if outcome not in {"stable", "regressed", "not-executed"}:
        raise RuntimeError("benchmark outcome is incompatible")
    baseline_p95 = _nullable_positive_int(record["baseline_p95_ns"], _MAX_P95_NS, "baseline p95")
    candidate_p95 = _nullable_positive_int(record["candidate_p95_ns"], _MAX_P95_NS, "candidate p95")
    outcome_code = _bounded_ascii_text(record["outcome_code"], 48, "benchmark outcome code")
    baseline_artifact_hash = _nullable_sha256_text(
        record["baseline_artifact_sha256"], "baseline artifact sha256"
    )
    candidate_artifact_hash = _nullable_sha256_text(
        record["candidate_artifact_sha256"], "candidate artifact sha256"
    )
    baseline_artifact_url, candidate_artifact_url = _validate_outcome(
        record,
        outcome=outcome,
        outcome_code=outcome_code,
        baseline_p95=baseline_p95,
        candidate_p95=candidate_p95,
        tolerance_bps=tolerance_bps,
        baseline_artifact_hash=baseline_artifact_hash,
        candidate_artifact_hash=candidate_artifact_hash,
        evidence_revision=evidence_revision,
    )

    result_hash = _sha256_text(record["result_sha256"], "comparison result sha256")
    result_url, result_revision = _evidence_url(
        record["result_url"], role="result", digest=result_hash
    )
    if result_revision != evidence_revision:
        raise RuntimeError("comparison result revision must match its evaluation evidence")
    claimed_urls = [result_url]
    claimed_hashes = [result_hash]
    if baseline_artifact_url is not None and baseline_artifact_hash is not None:
        claimed_urls.append(baseline_artifact_url)
        claimed_hashes.append(baseline_artifact_hash)
    if candidate_artifact_url is not None and candidate_artifact_hash is not None:
        claimed_urls.append(candidate_artifact_url)
        claimed_hashes.append(candidate_artifact_hash)
    for value in claimed_urls:
        _claim_unique(value, evidence_urls, "benchmark evidence URL")
    for value in claimed_hashes:
        _claim_unique(value, evidence_hashes, "benchmark evidence sha256")

    reviews = (
        _required_true(record["eligible_comparison_reviewed"], "comparison eligibility review"),
        _required_true(record["comparability_reviewed"], "comparison comparability review"),
        _required_true(record["threshold_predeclared_reviewed"], "predeclared threshold review"),
        _required_true(record["outcome_reviewed"], "benchmark outcome review"),
        _required_true(record["provenance_reviewed"], "comparison provenance review"),
        _required_true(record["validation_reviewed"], "comparison validation review"),
    )
    identity: _ComparisonIdentity = (
        comparison_id,
        run_url,
        job_url,
        base_sha,
        head_sha,
        workflow_url,
        workflow_hash,
        benchmark_schema,
        benchmark_case,
        baseline_source_url,
        baseline_source_hash,
        candidate_source_url,
        candidate_source_hash,
        runner_profile_url,
        runner_profile_hash,
        environment_profile,
        metric,
        tolerance_bps,
        started_at,
        outcome,
        baseline_p95,
        candidate_p95,
        outcome_code,
        result_url,
        result_hash,
        baseline_artifact_url,
        baseline_artifact_hash,
        candidate_artifact_url,
        candidate_artifact_hash,
        *reviews,
    )
    return identity, (started_at_value, run_number, job_number, benchmark_schema, benchmark_case)


def _validate_outcome(
    record: dict[str, object],
    *,
    outcome: str,
    outcome_code: str,
    baseline_p95: int | None,
    candidate_p95: int | None,
    tolerance_bps: int,
    baseline_artifact_hash: str | None,
    candidate_artifact_hash: str | None,
    evidence_revision: str,
) -> tuple[str | None, str | None]:
    baseline_url_value = record["baseline_artifact_url"]
    candidate_url_value = record["candidate_artifact_url"]
    if outcome == "not-executed":
        if (
            baseline_p95 is not None
            or candidate_p95 is not None
            or baseline_artifact_hash is not None
            or candidate_artifact_hash is not None
            or baseline_url_value is not None
            or candidate_url_value is not None
            or outcome_code not in _NON_EXECUTION_CODES
        ):
            raise RuntimeError("non-executed benchmark must not claim comparison evidence")
        return None, None
    if (
        baseline_p95 is None
        or candidate_p95 is None
        or baseline_artifact_hash is None
        or candidate_artifact_hash is None
    ):
        raise RuntimeError("executed benchmark comparison requires complete timing evidence")
    baseline_url, baseline_revision = _evidence_url(
        baseline_url_value, role="baseline", digest=baseline_artifact_hash
    )
    candidate_url, candidate_revision = _evidence_url(
        candidate_url_value, role="candidate", digest=candidate_artifact_hash
    )
    if baseline_revision != evidence_revision or candidate_revision != evidence_revision:
        raise RuntimeError("benchmark artifact revisions must match evaluation evidence")
    regressed = candidate_p95 * 10_000 > baseline_p95 * (10_000 + tolerance_bps)
    if outcome == "stable" and (regressed or outcome_code != "benchmark-within-tolerance"):
        raise RuntimeError("stable benchmark outcome contradicts exact timing comparison")
    if outcome == "regressed" and (not regressed or outcome_code != "benchmark-regressed"):
        raise RuntimeError("regressed benchmark outcome contradicts exact timing comparison")
    return baseline_url, candidate_url


def _default_manifest() -> Path:
    bundled = Path(__file__).resolve().parent / "assets" / "benchmark_regression_rate.json"
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


def _slug(value: object, maximum: int, role: str) -> str:
    text = _bounded_ascii_text(value, maximum, role)
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789._-"
    if (
        text[0] not in "abcdefghijklmnopqrstuvwxyz0123456789"
        or text[-1] not in "abcdefghijklmnopqrstuvwxyz0123456789"
        or any(character not in allowed for character in text)
        or ".." in text
    ):
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


def _benchmark_source_url(value: object, revision: str, source: str, role: str) -> str:
    text = _bounded_ascii_text(value, 320, f"{role} benchmark source URL")
    expected = f"{_PROJECT_URL}/blob/{revision}/{source}"
    if text != expected:
        raise RuntimeError(f"{role} benchmark source URL is incompatible")
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
        or subdirectory != "benchmark-regression-rate"
        or filename != f"{role}-{digest}.json"
    ):
        raise RuntimeError(f"evaluation {role} URL is incompatible")
    return text, revision


def _canonical_positive_decimal(value: str) -> bool:
    return value.isascii() and value.isdecimal() and value != "0" and not value.startswith("0")


def _non_negative_int(value: object, maximum: int, role: str) -> int:
    if type(value) is not int or value < 0 or value > maximum:
        raise RuntimeError(f"{role} is invalid")
    return value


def _nullable_positive_int(value: object, maximum: int, role: str) -> int | None:
    if value is None:
        return None
    if type(value) is not int or value <= 0 or value > maximum:
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
