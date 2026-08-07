"""Evaluate reviewed issue-response and PR-review latency without making an SLA claim."""

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

type _MeasurementIdentity = tuple[
    str,
    str,
    str,
    str,
    str | None,
    str | None,
    str | None,
    int | None,
    str,
    str,
    bool,
    bool | None,
    bool | None,
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
    tuple[_MeasurementIdentity, ...],
    bool,
    bool,
    bool,
    bool,
]

_SCHEMA = "ludoweave.evaluation.response-review-latency-readiness/1"
_MANIFEST_SCHEMA = "ludoweave.community.response-review-latency/1"
_MEASUREMENT_POLICY = "first-public-human-maintainer-action/1"
_REVIEWED_MANIFEST_SHA256 = "bc40bbcc1636229fa2c78aed5f71854d1221fd3c0d33169edc1321dd07e69d4f"
_MANDATORY_WINDOW_PREFIX: tuple[_WindowIdentity, ...] = ()
_MAX_MANIFEST_BYTES = 65_536
_MAX_JSON_NESTING = 16
_MAX_MEASUREMENT_WINDOWS = 12
_MAX_MEASUREMENTS_PER_WINDOW = 256
_MAX_WINDOW_SECONDS = 31_622_400
_MAX_OBSERVATION_LAG_SECONDS = 31_622_400
_MAX_LATENCY_SECONDS = 315_576_000
_PROJECT_URL = "https://github.com/xsparc/ludoweave-engine"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="explicit local reviewed response/review-latency manifest",
    )
    arguments = parser.parse_args(tuple(sys.argv[1:] if argv is None else argv))
    selected: object = getattr(arguments, "manifest", None)
    manifest = _default_manifest() if selected is None else _path(selected)
    print(json.dumps(evaluate(manifest), ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0


def evaluate(manifest: Path) -> dict[str, object]:
    """Return deterministic, path-free response/review-latency admission evidence."""

    raw_manifest, identities = _parse_manifest(manifest)
    manifest_hash = hashlib.sha256(raw_manifest).hexdigest()
    manifest_identity_reviewed = manifest_hash == _REVIEWED_MANIFEST_SHA256
    historical_windows_preserved = tuple(
        identities[: len(_MANDATORY_WINDOW_PREFIX)]
    ) == _MANDATORY_WINDOW_PREFIX and (
        not manifest_identity_reviewed or len(identities) == len(_MANDATORY_WINDOW_PREFIX)
    )
    admitted = identities if manifest_identity_reviewed and historical_windows_preserved else ()
    admitted_measurements = tuple(measurement for window in admitted for measurement in window[8])
    issue_summary = _metric_summary(admitted_measurements, "issue-response")
    pull_request_summary = _metric_summary(admitted_measurements, "pull-request-review")
    complete_reviewed_windows = bool(admitted)
    issue_response_measurements_present = cast(int, issue_summary["observed_count"]) > 0
    pull_request_review_measurements_present = cast(int, pull_request_summary["observed_count"]) > 0
    gate_satisfied = (
        manifest_identity_reviewed
        and historical_windows_preserved
        and complete_reviewed_windows
        and issue_response_measurements_present
        and pull_request_review_measurements_present
    )
    reasons: list[str]
    if manifest_identity_reviewed and historical_windows_preserved and not identities:
        reasons = ["response-review-latency-evidence-absent"]
    else:
        reasons = []
        if not manifest_identity_reviewed:
            reasons.append("response-review-latency-manifest-identity-unreviewed")
        if not historical_windows_preserved:
            reasons.append("historical-measurement-window-missing")
        if not complete_reviewed_windows:
            reasons.append("complete-reviewed-measurement-window-absent")
        if not issue_response_measurements_present:
            reasons.append("issue-response-measurement-absent")
        if not pull_request_review_measurements_present:
            reasons.append("pull-request-review-measurement-absent")

    return {
        "admission": {
            "complete_reviewed_windows": complete_reviewed_windows,
            "historical_windows_preserved": historical_windows_preserved,
            "issue_response_measurements_present": issue_response_measurements_present,
            "manifest_identity_reviewed": manifest_identity_reviewed,
            "pull_request_review_measurements_present": (pull_request_review_measurements_present),
            "reason_codes": tuple(reasons),
        },
        "evidence_level": (
            "reviewed-response-review-latency"
            if gate_satisfied
            else "response-review-latency-admission-readiness"
        ),
        "gate_satisfied": gate_satisfied,
        "latency_measurement_proven": gate_satisfied,
        "ludoweave_version": __version__,
        "metrics": {
            "issue_response": issue_summary,
            "manifest_sha256": manifest_hash,
            "measurement_policy": _MEASUREMENT_POLICY,
            "pull_request_review": pull_request_summary,
            "records_verified": True,
            "window_count": len(admitted),
        },
        "schema": _SCHEMA,
        "status": "ready" if gate_satisfied else "not-ready",
    }


def _parse_manifest(path: Path) -> tuple[bytes, tuple[_WindowIdentity, ...]]:
    raw_manifest = _read_bounded(path, _MAX_MANIFEST_BYTES, "response-review manifest")
    document = _object(_loads(raw_manifest, "response-review manifest"), "response-review manifest")
    _exact_fields(
        document,
        {"schema", "source_project", "measurement_policy", "measurement_windows"},
        "response-review manifest",
    )
    if document["schema"] != _MANIFEST_SCHEMA:
        raise RuntimeError("response-review manifest schema is incompatible")
    if document["source_project"] != "ludoweave-engine":
        raise RuntimeError("response-review project identity is invalid")
    if document["measurement_policy"] != _MEASUREMENT_POLICY:
        raise RuntimeError("response-review measurement policy is incompatible")

    raw_windows = _list(document["measurement_windows"], "measurement windows")
    if len(raw_windows) > _MAX_MEASUREMENT_WINDOWS:
        raise RuntimeError("response-review manifest exceeds its window limit")
    identities: list[_WindowIdentity] = []
    resource_urls: set[str] = set()
    action_urls: set[str] = set()
    evidence_urls: set[str] = set()
    evidence_hashes: set[str] = set()
    previous_opened_before: datetime | None = None
    for index, item in enumerate(raw_windows):
        identity, opened_before = _window_identity(
            _object(item, "measurement window"),
            index=index,
            previous_opened_before=previous_opened_before,
            resource_urls=resource_urls,
            action_urls=action_urls,
            evidence_urls=evidence_urls,
            evidence_hashes=evidence_hashes,
        )
        identities.append(identity)
        previous_opened_before = opened_before
    return raw_manifest, tuple(identities)


def _window_identity(
    window: dict[str, object],
    *,
    index: int,
    previous_opened_before: datetime | None,
    resource_urls: set[str],
    action_urls: set[str],
    evidence_urls: set[str],
    evidence_hashes: set[str],
) -> tuple[_WindowIdentity, datetime]:
    _exact_fields(
        window,
        {
            "window_id",
            "opened_from",
            "opened_before",
            "observed_through",
            "census_url",
            "census_sha256",
            "review_url",
            "review_sha256",
            "measurements",
            "public_census_complete_reviewed",
            "eligibility_reviewed",
            "provenance_reviewed",
            "validation_reviewed",
        },
        "measurement window",
    )
    window_id = _bounded_ascii_text(window["window_id"], 16, "measurement window ID")
    if window_id != f"window-{index + 1:04d}":
        raise RuntimeError("measurement windows must use canonical sequential IDs")
    opened_from, opened_from_value = _utc_timestamp(
        window["opened_from"], "measurement window opening timestamp"
    )
    opened_before, opened_before_value = _utc_timestamp(
        window["opened_before"], "measurement window closing timestamp"
    )
    observed_through, observed_through_value = _utc_timestamp(
        window["observed_through"], "measurement observation timestamp"
    )
    if opened_from_value >= opened_before_value:
        raise RuntimeError("measurement window must have positive duration")
    if previous_opened_before is not None and opened_from_value < previous_opened_before:
        raise RuntimeError("measurement windows must be chronological and non-overlapping")
    if _seconds_between(opened_from_value, opened_before_value) > _MAX_WINDOW_SECONDS:
        raise RuntimeError("measurement window exceeds its duration limit")
    if observed_through_value < opened_before_value:
        raise RuntimeError("measurement observation must cover the opening window")
    if _seconds_between(opened_before_value, observed_through_value) > (
        _MAX_OBSERVATION_LAG_SECONDS
    ):
        raise RuntimeError("measurement observation exceeds its lag limit")

    census_hash = _sha256_text(window["census_sha256"], "measurement census sha256")
    review_hash = _sha256_text(window["review_sha256"], "measurement review sha256")
    if census_hash == review_hash:
        raise RuntimeError("measurement census and review identities must be distinct")
    census_url, census_revision = _evidence_url(
        window["census_url"], role="census", digest=census_hash
    )
    review_url, review_revision = _evidence_url(
        window["review_url"], role="review", digest=review_hash
    )
    if census_revision != review_revision:
        raise RuntimeError("measurement census and review revisions must match")
    for value, seen, role in (
        (census_url, evidence_urls, "measurement evidence URL"),
        (review_url, evidence_urls, "measurement evidence URL"),
        (census_hash, evidence_hashes, "measurement evidence sha256"),
        (review_hash, evidence_hashes, "measurement evidence sha256"),
    ):
        _claim_unique(value, seen, role)

    raw_measurements = _list(window["measurements"], "window measurements")
    if len(raw_measurements) > _MAX_MEASUREMENTS_PER_WINDOW:
        raise RuntimeError("measurement window exceeds its record limit")
    measurements: list[_MeasurementIdentity] = []
    previous_key: tuple[int, int] | None = None
    for item in raw_measurements:
        measurement_identity, key = _measurement_identity(
            _object(item, "latency measurement"),
            opened_from_value=opened_from_value,
            opened_before_value=opened_before_value,
            observed_through_value=observed_through_value,
            resource_urls=resource_urls,
            action_urls=action_urls,
            evidence_hashes=evidence_hashes,
        )
        if previous_key is not None and key <= previous_key:
            raise RuntimeError("latency measurements must follow canonical resource order")
        previous_key = key
        measurements.append(measurement_identity)

    public_census_complete_reviewed = _required_true(
        window["public_census_complete_reviewed"], "public census completeness review"
    )
    eligibility_reviewed = _required_true(
        window["eligibility_reviewed"], "measurement eligibility review"
    )
    provenance_reviewed = _required_true(
        window["provenance_reviewed"], "measurement provenance review"
    )
    validation_reviewed = _required_true(
        window["validation_reviewed"], "measurement validation review"
    )
    window_identity: _WindowIdentity = (
        window_id,
        opened_from,
        opened_before,
        observed_through,
        census_url,
        census_hash,
        review_url,
        review_hash,
        tuple(measurements),
        public_census_complete_reviewed,
        eligibility_reviewed,
        provenance_reviewed,
        validation_reviewed,
    )
    return window_identity, opened_before_value


def _measurement_identity(
    record: dict[str, object],
    *,
    opened_from_value: datetime,
    opened_before_value: datetime,
    observed_through_value: datetime,
    resource_urls: set[str],
    action_urls: set[str],
    evidence_hashes: set[str],
) -> tuple[_MeasurementIdentity, tuple[int, int]]:
    _exact_fields(
        record,
        {
            "kind",
            "resource_url",
            "opened_at",
            "status",
            "action_url",
            "action_at",
            "action_outcome",
            "latency_seconds",
            "source_snapshot_sha256",
            "review_record_sha256",
            "subject_external_human_reviewed",
            "maintainer_action_human_reviewed",
            "distinct_participants_reviewed",
            "qualifying_action_state_reviewed",
            "provenance_reviewed",
            "validation_reviewed",
        },
        "latency measurement",
    )
    kind = _bounded_ascii_text(record["kind"], 32, "measurement kind")
    if kind not in {"issue-response", "pull-request-review"}:
        raise RuntimeError("measurement kind is incompatible")
    resource_url, resource_number = _resource_url(record["resource_url"], kind)
    _claim_unique(resource_url, resource_urls, "measurement resource URL")
    opened_at, opened_at_value = _utc_timestamp(record["opened_at"], "resource opening timestamp")
    if not opened_from_value <= opened_at_value < opened_before_value:
        raise RuntimeError("measurement resource falls outside its opening window")
    status = _bounded_ascii_text(record["status"], 16, "measurement status")
    if status not in {"observed", "pending"}:
        raise RuntimeError("measurement status is incompatible")
    action_url = _nullable_ascii_text(record["action_url"], 256, "measurement action URL")
    action_at_raw = _nullable_ascii_text(record["action_at"], 20, "measurement action timestamp")
    action_outcome = _nullable_ascii_text(
        record["action_outcome"], 32, "measurement action outcome"
    )
    latency_seconds = _nullable_non_negative_int(
        record["latency_seconds"], _MAX_LATENCY_SECONDS, "measurement latency"
    )
    maintainer_action_human_reviewed = _nullable_true(
        record["maintainer_action_human_reviewed"], "maintainer action human review"
    )
    distinct_participants_reviewed = _nullable_true(
        record["distinct_participants_reviewed"], "distinct participant review"
    )
    if status == "pending":
        if any(
            value is not None
            for value in (
                action_url,
                action_at_raw,
                action_outcome,
                latency_seconds,
                maintainer_action_human_reviewed,
                distinct_participants_reviewed,
            )
        ):
            raise RuntimeError("pending measurement must not claim a qualifying action")
    else:
        if (
            action_url is None
            or action_at_raw is None
            or action_outcome is None
            or latency_seconds is None
            or maintainer_action_human_reviewed is not True
            or distinct_participants_reviewed is not True
        ):
            raise RuntimeError("observed measurement requires a reviewed qualifying action")
        _action_url(action_url, kind, resource_url)
        _claim_unique(action_url, action_urls, "measurement action URL")
        action_at, action_at_value = _utc_timestamp(action_at_raw, "measurement action timestamp")
        if action_at_value < opened_at_value or action_at_value > observed_through_value:
            raise RuntimeError("measurement action falls outside its observation interval")
        if latency_seconds != _seconds_between(opened_at_value, action_at_value):
            raise RuntimeError("measurement latency does not match its timestamps")
        if kind == "issue-response" and action_outcome != "responded":
            raise RuntimeError("issue response outcome is incompatible")
        if kind == "pull-request-review" and action_outcome not in {
            "approved",
            "changes-requested",
            "commented",
        }:
            raise RuntimeError("pull request review outcome is incompatible")
        action_at_raw = action_at

    source_snapshot_hash = _sha256_text(
        record["source_snapshot_sha256"], "measurement source snapshot sha256"
    )
    review_record_hash = _sha256_text(
        record["review_record_sha256"], "measurement review record sha256"
    )
    if source_snapshot_hash == review_record_hash:
        raise RuntimeError("measurement source and review identities must be distinct")
    _claim_unique(source_snapshot_hash, evidence_hashes, "measurement evidence sha256")
    _claim_unique(review_record_hash, evidence_hashes, "measurement evidence sha256")
    subject_external_human_reviewed = _required_true(
        record["subject_external_human_reviewed"], "external human subject review"
    )
    qualifying_action_state_reviewed = _required_true(
        record["qualifying_action_state_reviewed"], "qualifying action state review"
    )
    provenance_reviewed = _required_true(
        record["provenance_reviewed"], "measurement provenance review"
    )
    validation_reviewed = _required_true(
        record["validation_reviewed"], "measurement validation review"
    )
    identity: _MeasurementIdentity = (
        kind,
        resource_url,
        opened_at,
        status,
        action_url,
        action_at_raw,
        action_outcome,
        latency_seconds,
        source_snapshot_hash,
        review_record_hash,
        subject_external_human_reviewed,
        maintainer_action_human_reviewed,
        distinct_participants_reviewed,
        qualifying_action_state_reviewed,
        provenance_reviewed,
        validation_reviewed,
    )
    return identity, (0 if kind == "issue-response" else 1, resource_number)


def _metric_summary(measurements: tuple[_MeasurementIdentity, ...], kind: str) -> dict[str, object]:
    selected = tuple(measurement for measurement in measurements if measurement[0] == kind)
    latencies = sorted(
        cast(int, measurement[7]) for measurement in selected if measurement[3] == "observed"
    )
    pending_count = sum(measurement[3] == "pending" for measurement in selected)
    median_seconds: float | None = None
    p95_seconds: int | None = None
    if latencies:
        middle = len(latencies) // 2
        if len(latencies) % 2:
            median_seconds = float(latencies[middle])
        else:
            median_seconds = (latencies[middle - 1] + latencies[middle]) / 2
        p95_seconds = latencies[(95 * len(latencies) - 1) // 100]
    return {
        "eligible_count": len(selected),
        "median_seconds": median_seconds,
        "observed_count": len(latencies),
        "p95_seconds": p95_seconds,
        "pending_count": pending_count,
    }


def _default_manifest() -> Path:
    bundled = Path(__file__).resolve().parent / "assets" / "response_review_latency.json"
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


def _nullable_ascii_text(value: object, maximum: int, role: str) -> str | None:
    if value is None:
        return None
    return _bounded_ascii_text(value, maximum, role)


def _sha256_text(value: object, role: str) -> str:
    text = _bounded_ascii_text(value, 64, role)
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise RuntimeError(f"{role} is invalid")
    return text


def _utc_timestamp(value: object, role: str) -> tuple[str, datetime]:
    text = _bounded_ascii_text(value, 20, role)
    if (
        len(text) != 20
        or text[4] != "-"
        or text[7] != "-"
        or text[10] != "T"
        or text[13] != ":"
        or text[16] != ":"
        or text[19] != "Z"
        or any(
            not text[index].isascii() or not text[index].isdecimal()
            for index in (*range(4), 5, 6, 8, 9, 11, 12, 14, 15, 17, 18)
        )
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


def _resource_url(value: object, kind: str) -> tuple[str, int]:
    text = _bounded_ascii_text(value, 128, "measurement resource URL")
    segment = "issues" if kind == "issue-response" else "pull"
    prefix = f"{_PROJECT_URL}/{segment}/"
    if not text.startswith(prefix):
        raise RuntimeError("measurement resource URL is incompatible")
    number = text.removeprefix(prefix)
    if not _canonical_positive_decimal(number):
        raise RuntimeError("measurement resource URL is incompatible")
    return text, int(number)


def _action_url(value: str, kind: str, resource_url: str) -> None:
    anchor = "#issuecomment-" if kind == "issue-response" else "#pullrequestreview-"
    prefix = f"{resource_url}{anchor}"
    if not value.startswith(prefix) or not _canonical_positive_decimal(value.removeprefix(prefix)):
        raise RuntimeError("measurement action URL is incompatible")


def _evidence_url(value: object, *, role: str, digest: str) -> tuple[str, str]:
    text = _bounded_ascii_text(value, 384, f"measurement {role} URL")
    prefix = f"{_PROJECT_URL}/blob/"
    if not text.startswith(prefix):
        raise RuntimeError(f"measurement {role} URL is incompatible")
    parts = text.removeprefix(prefix).split("/")
    if len(parts) != 4:
        raise RuntimeError(f"measurement {role} URL is incompatible")
    revision, directory, subdirectory, filename = parts
    if (
        len(revision) != 40
        or any(character not in "0123456789abcdef" for character in revision)
        or directory != "evidence"
        or subdirectory != "response-review-latency"
        or filename != f"{role}-{digest}.json"
    ):
        raise RuntimeError(f"measurement {role} URL is incompatible")
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


def _nullable_true(value: object, role: str) -> bool | None:
    if value is None:
        return None
    return _required_true(value, role)


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
