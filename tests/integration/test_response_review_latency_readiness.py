"""M31 issue-response and pull-request-review latency admission evidence."""

import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from datetime import UTC, datetime, timedelta
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

import pytest

from ludoweave import __version__

_ROOT = Path(__file__).parents[2]
_EXAMPLE = _ROOT / "examples" / "response_review_latency_readiness.py"
_VALIDATOR = _ROOT / "scripts" / "response_review_latency_evidence.py"
_MANIFEST = _ROOT / "tests" / "fixtures" / "response_review_latency.json"
_BASE = datetime(2026, 8, 1, tzinfo=UTC)


class _Validate(Protocol):
    def __call__(self, document: dict[str, object], *, version: str) -> None: ...


class _Evaluate(Protocol):
    def __call__(self, manifest: Path) -> dict[str, object]: ...


class _ParseManifest(Protocol):
    def __call__(self, manifest: Path) -> tuple[bytes, tuple[object, ...]]: ...


def _load(path: Path, name: str) -> ModuleType:
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{name} could not be loaded")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validator() -> _Validate:
    module = _load(_VALIDATOR, "response_review_latency_validator")
    return cast(_Validate, module.validate_response_review_latency_evidence)


def _evaluator() -> tuple[ModuleType, _Evaluate]:
    module = _load(_EXAMPLE, "response_review_latency_example")
    return module, cast(_Evaluate, module.evaluate)


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def _timestamp(value: datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def _manifest() -> dict[str, object]:
    return cast(dict[str, object], json.loads(_MANIFEST.read_text(encoding="utf-8")))


def _measurement(
    kind: str,
    number: int,
    *,
    status: str = "observed",
    opened_minutes: int,
    latency_seconds: int = 300,
    source_character: str,
    review_character: str,
) -> dict[str, object]:
    opened_at = _BASE + timedelta(minutes=opened_minutes)
    segment = "issues" if kind == "issue-response" else "pull"
    resource_url = f"https://github.com/xsparc/ludoweave-engine/{segment}/{number}"
    if status == "observed":
        action_at = opened_at + timedelta(seconds=latency_seconds)
        anchor = "issuecomment" if kind == "issue-response" else "pullrequestreview"
        action_url: str | None = f"{resource_url}#{anchor}-{number + 1000}"
        action_at_text: str | None = _timestamp(action_at)
        outcome: str | None = "responded" if kind == "issue-response" else "commented"
        latency: int | None = latency_seconds
        maintainer_reviewed: bool | None = True
        distinct_reviewed: bool | None = True
    else:
        action_url = None
        action_at_text = None
        outcome = None
        latency = None
        maintainer_reviewed = None
        distinct_reviewed = None
    return {
        "kind": kind,
        "resource_url": resource_url,
        "opened_at": _timestamp(opened_at),
        "status": status,
        "action_url": action_url,
        "action_at": action_at_text,
        "action_outcome": outcome,
        "latency_seconds": latency,
        "source_snapshot_sha256": source_character * 64,
        "review_record_sha256": review_character * 64,
        "subject_external_human_reviewed": True,
        "maintainer_action_human_reviewed": maintainer_reviewed,
        "distinct_participants_reviewed": distinct_reviewed,
        "qualifying_action_state_reviewed": True,
        "provenance_reviewed": True,
        "validation_reviewed": True,
    }


def _window(measurements: list[dict[str, object]], *, index: int = 1) -> dict[str, object]:
    revision = str(index) * 40
    census_hash = "a" * 63 + f"{index:x}"
    review_hash = "b" * 63 + f"{index:x}"
    return {
        "window_id": f"window-{index:04d}",
        "opened_from": _timestamp(_BASE + timedelta(days=index - 1)),
        "opened_before": _timestamp(_BASE + timedelta(days=index)),
        "observed_through": _timestamp(_BASE + timedelta(days=index + 1)),
        "census_url": (
            "https://github.com/xsparc/ludoweave-engine/blob/"
            f"{revision}/evidence/response-review-latency/census-{census_hash}.json"
        ),
        "census_sha256": census_hash,
        "review_url": (
            "https://github.com/xsparc/ludoweave-engine/blob/"
            f"{revision}/evidence/response-review-latency/review-{review_hash}.json"
        ),
        "review_sha256": review_hash,
        "measurements": measurements,
        "public_census_complete_reviewed": True,
        "eligibility_reviewed": True,
        "provenance_reviewed": True,
        "validation_reviewed": True,
    }


def _ready_manifest() -> dict[str, object]:
    document = _manifest()
    measurements = [
        _measurement(
            "issue-response",
            101,
            opened_minutes=10,
            latency_seconds=60,
            source_character="c",
            review_character="d",
        ),
        _measurement(
            "issue-response",
            102,
            status="pending",
            opened_minutes=20,
            source_character="e",
            review_character="f",
        ),
        _measurement(
            "pull-request-review",
            201,
            opened_minutes=30,
            latency_seconds=120,
            source_character="1",
            review_character="2",
        ),
        _measurement(
            "pull-request-review",
            202,
            status="pending",
            opened_minutes=40,
            source_character="3",
            review_character="4",
        ),
    ]
    document["measurement_windows"] = [_window(measurements)]
    return document


def _write_manifest(tmp_path: Path, document: dict[str, object]) -> Path:
    path = tmp_path / "response_review_latency.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    return path


def _admit(
    module: ModuleType,
    evaluate: _Evaluate,
    path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> dict[str, object]:
    parse = cast(_ParseManifest, module._parse_manifest)
    raw, identities = parse(path)
    monkeypatch.setattr(module, "_REVIEWED_MANIFEST_SHA256", hashlib.sha256(raw).hexdigest())
    monkeypatch.setattr(module, "_MANDATORY_WINDOW_PREFIX", identities)
    return evaluate(path)


def _first_window(document: dict[str, object]) -> dict[str, object]:
    windows = cast(list[object], document["measurement_windows"])
    return cast(dict[str, object], windows[0])


def _measurements(document: dict[str, object]) -> list[dict[str, object]]:
    return cast(list[dict[str, object]], _first_window(document)["measurements"])


def _assert_rejected(document: dict[str, object], tmp_path: Path) -> None:
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError):
        evaluate(_write_manifest(tmp_path, document))


def test_default_report_is_repeatable_sanitized_and_not_ready() -> None:
    first = _run()
    second = _run("--manifest", str(_MANIFEST))

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["gate_satisfied"] is False
    assert document["latency_measurement_proven"] is False
    assert document["status"] == "not-ready"
    admission = cast(dict[str, object], document["admission"])
    assert admission["reason_codes"] == ["response-review-latency-evidence-absent"]
    for forbidden in (
        "resource_url",
        "action_url",
        "opened_at",
        "action_at",
        "census_url",
        "review_url",
        "source_snapshot_sha256",
        "review_record_sha256",
        "window_id",
        str(_ROOT),
    ):
        assert forbidden not in first.stdout


def test_missing_manifest_error_is_path_free(tmp_path: Path) -> None:
    missing = tmp_path / "private" / "missing.json"
    result = _run("--manifest", str(missing))

    assert result.returncode == 1
    assert result.stdout == ""
    assert "response-review manifest is unavailable" in result.stderr
    assert str(tmp_path) not in result.stderr


def test_validator_rejects_value_and_json_type_drift() -> None:
    document = cast(dict[str, object], json.loads(_run().stdout))
    validator = _validator()
    drifted = deepcopy(document)
    drifted["gate_satisfied"] = True
    with pytest.raises(RuntimeError, match="evidence drifted"):
        validator(drifted, version=__version__)
    typed = deepcopy(document)
    metrics = cast(dict[str, object], typed["metrics"])
    metrics["window_count"] = False
    with pytest.raises(RuntimeError, match="evidence drifted"):
        validator(typed, version=__version__)


def test_reviewed_complete_window_reports_counts_pending_and_latencies(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module, evaluate = _evaluator()
    path = _write_manifest(tmp_path, _ready_manifest())

    document = _admit(module, evaluate, path, monkeypatch)

    assert document["gate_satisfied"] is True
    assert document["latency_measurement_proven"] is True
    assert document["status"] == "ready"
    assert document["evidence_level"] == "reviewed-response-review-latency"
    metrics = cast(dict[str, object], document["metrics"])
    assert metrics["window_count"] == 1
    assert metrics["issue_response"] == {
        "eligible_count": 2,
        "median_seconds": 60.0,
        "observed_count": 1,
        "p95_seconds": 60,
        "pending_count": 1,
    }
    assert metrics["pull_request_review"] == {
        "eligible_count": 2,
        "median_seconds": 120.0,
        "observed_count": 1,
        "p95_seconds": 120,
        "pending_count": 1,
    }
    encoded = json.dumps(document, sort_keys=True)
    assert "issues/101" not in encoded
    assert "pull/201" not in encoded
    assert "2026-08" not in encoded


def test_even_median_and_nearest_rank_p95_are_deterministic(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _ready_manifest()
    measurements = _measurements(document)
    measurements[1] = _measurement(
        "issue-response",
        102,
        opened_minutes=20,
        latency_seconds=180,
        source_character="e",
        review_character="f",
    )
    module, evaluate = _evaluator()

    report = _admit(module, evaluate, _write_manifest(tmp_path, document), monkeypatch)

    metrics = cast(dict[str, object], report["metrics"])
    issue = cast(dict[str, object], metrics["issue_response"])
    assert issue["median_seconds"] == 120.0
    assert issue["p95_seconds"] == 180


def test_unreviewed_candidate_exposes_no_record_aggregates(tmp_path: Path) -> None:
    _, evaluate = _evaluator()

    report = evaluate(_write_manifest(tmp_path, _ready_manifest()))

    admission = cast(dict[str, object], report["admission"])
    assert "response-review-latency-manifest-identity-unreviewed" in cast(
        list[str], admission["reason_codes"]
    )
    metrics = cast(dict[str, object], report["metrics"])
    assert metrics["window_count"] == 0
    assert cast(dict[str, object], metrics["issue_response"])["eligible_count"] == 0
    assert cast(dict[str, object], metrics["pull_request_review"])["eligible_count"] == 0


def test_complete_window_without_pr_observation_remains_not_ready(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _ready_manifest()
    measurements = _measurements(document)
    measurements[2] = _measurement(
        "pull-request-review",
        201,
        status="pending",
        opened_minutes=30,
        source_character="1",
        review_character="2",
    )
    module, evaluate = _evaluator()

    report = _admit(module, evaluate, _write_manifest(tmp_path, document), monkeypatch)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["reason_codes"] == ("pull-request-review-measurement-absent",)


def test_mandatory_history_rejects_replacement_window(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = _ready_manifest()
    original_path = _write_manifest(tmp_path, original)
    module, evaluate = _evaluator()
    parse = cast(_ParseManifest, module._parse_manifest)
    _, original_identities = parse(original_path)
    replacement = deepcopy(original)
    _measurements(replacement)[0]["latency_seconds"] = 61
    _measurements(replacement)[0]["action_at"] = "2026-08-01T00:11:01Z"
    replacement_path = tmp_path / "replacement.json"
    replacement_path.write_text(json.dumps(replacement), encoding="utf-8")
    raw = replacement_path.read_bytes()
    monkeypatch.setattr(module, "_REVIEWED_MANIFEST_SHA256", hashlib.sha256(raw).hexdigest())
    monkeypatch.setattr(module, "_MANDATORY_WINDOW_PREFIX", original_identities)

    report = evaluate(replacement_path)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert "historical-measurement-window-missing" in cast(list[str], admission["reason_codes"])
    assert cast(dict[str, object], report["metrics"])["window_count"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schema", "ludoweave.community.response-review-latency/2"),
        ("source_project", "another-project"),
        ("measurement_policy", "fastest-action/1"),
        ("measurement_windows", {}),
    ],
)
def test_manifest_contract_rejects_incompatible_values(
    tmp_path: Path, field: str, value: object
) -> None:
    document = _manifest()
    document[field] = value
    _assert_rejected(document, tmp_path)


def test_manifest_rejects_unknown_and_duplicate_json_fields(tmp_path: Path) -> None:
    document = _manifest()
    document["unexpected"] = True
    _assert_rejected(document, tmp_path)
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text(
        '{"schema":"a","schema":"b","source_project":"ludoweave-engine",'
        '"measurement_policy":"first-public-human-maintainer-action/1",'
        '"measurement_windows":[]}',
        encoding="utf-8",
    )
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError, match="not valid JSON"):
        evaluate(duplicate)


def test_manifest_rejects_size_nesting_and_window_limits(tmp_path: Path) -> None:
    _, evaluate = _evaluator()
    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * 65_537)
    with pytest.raises(RuntimeError, match="byte limit"):
        evaluate(oversized)
    nested = tmp_path / "nested.json"
    nested.write_text("[" * 17 + "]" * 17, encoding="utf-8")
    with pytest.raises(RuntimeError, match="nesting limit"):
        evaluate(nested)
    document = _manifest()
    document["measurement_windows"] = [{}] * 13
    with pytest.raises(RuntimeError, match="window limit"):
        evaluate(_write_manifest(tmp_path, document))


def test_manifest_rejects_symlink_when_supported(tmp_path: Path) -> None:
    link = tmp_path / "manifest-link.json"
    try:
        link.symlink_to(_MANIFEST)
    except OSError:
        pytest.skip("symlink creation is unavailable")
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError, match="symbolic link"):
        evaluate(link)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("window_id", "window-2"),
        ("opened_before", "2026-08-01T00:00:00Z"),
        ("observed_through", "2026-08-01T12:00:00Z"),
        ("census_sha256", "A" * 64),
        ("review_sha256", "b" * 63),
        ("public_census_complete_reviewed", False),
        ("eligibility_reviewed", 1),
        ("provenance_reviewed", None),
        ("validation_reviewed", "true"),
    ],
)
def test_window_rejects_invalid_identity_time_hash_and_review(
    tmp_path: Path, field: str, value: object
) -> None:
    document = _ready_manifest()
    _first_window(document)[field] = value
    _assert_rejected(document, tmp_path)


def test_window_rejects_noncanonical_evidence_urls_and_revision_drift(tmp_path: Path) -> None:
    for field, value in (
        ("census_url", "https://example.com/census.json"),
        (
            "census_url",
            "https://github.com/xsparc/ludoweave-engine/blob/main/evidence/"
            + "response-review-latency/census-"
            + "a" * 63
            + "1.json",
        ),
        (
            "review_url",
            "https://github.com/xsparc/ludoweave-engine/blob/"
            + "2" * 40
            + "/evidence/response-review-latency/review-"
            + "b" * 63
            + "1.json",
        ),
    ):
        document = _ready_manifest()
        _first_window(document)[field] = value
        _assert_rejected(document, tmp_path)


def test_window_rejects_excess_duration_observation_lag_and_overlap(tmp_path: Path) -> None:
    document = _ready_manifest()
    _first_window(document)["opened_before"] = "2028-01-01T00:00:00Z"
    _first_window(document)["observed_through"] = "2028-01-02T00:00:00Z"
    _assert_rejected(document, tmp_path)

    document = _ready_manifest()
    _first_window(document)["observed_through"] = "2028-01-01T00:00:00Z"
    _assert_rejected(document, tmp_path)

    document = _ready_manifest()
    window = _first_window(document)
    window["observed_through"] = window["opened_before"]
    _assert_rejected(document, tmp_path)

    document = _ready_manifest()
    second = _window([], index=2)
    second["opened_from"] = "2026-08-01T12:00:00Z"
    document["measurement_windows"] = [_first_window(document), second]
    _assert_rejected(document, tmp_path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("kind", "issue-fastest-response"),
        ("resource_url", "https://example.com/issues/101"),
        ("resource_url", "https://github.com/xsparc/ludoweave-engine/issues/0101"),
        ("opened_at", "2026-08-02T00:00:00Z"),
        ("status", "complete"),
        ("latency_seconds", True),
        ("latency_seconds", 315_576_001),
        ("source_snapshot_sha256", "g" * 64),
        ("subject_external_human_reviewed", False),
        ("qualifying_action_state_reviewed", 1),
        ("provenance_reviewed", None),
        ("validation_reviewed", "true"),
    ],
)
def test_measurement_rejects_invalid_identity_types_bounds_and_reviews(
    tmp_path: Path, field: str, value: object
) -> None:
    document = _ready_manifest()
    _measurements(document)[0][field] = value
    _assert_rejected(document, tmp_path)


def test_observed_measurement_requires_exact_action_contract(tmp_path: Path) -> None:
    mutations: tuple[tuple[str, object], ...] = (
        ("action_url", None),
        (
            "action_url",
            "https://github.com/xsparc/ludoweave-engine/issues/101#issuecomment-0",
        ),
        (
            "action_url",
            "https://github.com/xsparc/ludoweave-engine/issues/102#issuecomment-1101",
        ),
        ("action_at", "2026-07-31T23:59:59Z"),
        ("action_at", "2026-08-04T00:00:00Z"),
        ("action_outcome", "approved"),
        ("latency_seconds", 59),
        ("maintainer_action_human_reviewed", False),
        ("distinct_participants_reviewed", None),
    )
    for field, value in mutations:
        document = _ready_manifest()
        _measurements(document)[0][field] = value
        _assert_rejected(document, tmp_path)


def test_pending_measurement_rejects_any_action_claim(tmp_path: Path) -> None:
    fields: tuple[tuple[str, object], ...] = (
        ("action_url", "https://github.com/xsparc/ludoweave-engine/issues/102#issuecomment-9"),
        ("action_at", "2026-08-01T00:30:00Z"),
        ("action_outcome", "responded"),
        ("latency_seconds", 1),
        ("maintainer_action_human_reviewed", True),
        ("distinct_participants_reviewed", True),
    )
    for field, value in fields:
        document = _ready_manifest()
        _measurements(document)[1][field] = value
        _assert_rejected(document, tmp_path)


def test_pr_review_outcomes_are_exact(tmp_path: Path) -> None:
    for outcome in ("approved", "changes-requested", "commented"):
        document = _ready_manifest()
        _measurements(document)[2]["action_outcome"] = outcome
        _, evaluate = _evaluator()
        evaluate(_write_manifest(tmp_path, document))
    document = _ready_manifest()
    _measurements(document)[2]["action_outcome"] = "dismissed"
    _assert_rejected(document, tmp_path)


def test_measurements_require_canonical_order(tmp_path: Path) -> None:
    document = _ready_manifest()
    measurements = _measurements(document)
    measurements[0], measurements[1] = measurements[1], measurements[0]
    _assert_rejected(document, tmp_path)
    document = _ready_manifest()
    measurements = _measurements(document)
    measurements[0], measurements[2] = measurements[2], measurements[0]
    _assert_rejected(document, tmp_path)


def test_duplicate_resource_action_or_evidence_identity_is_rejected(tmp_path: Path) -> None:
    for target, source in (
        ((1, "resource_url"), (0, "resource_url")),
        ((2, "action_url"), (0, "action_url")),
        ((1, "source_snapshot_sha256"), (0, "source_snapshot_sha256")),
        ((1, "review_record_sha256"), (0, "review_record_sha256")),
    ):
        document = _ready_manifest()
        measurements = _measurements(document)
        measurements[target[0]][target[1]] = measurements[source[0]][source[1]]
        _assert_rejected(document, tmp_path)


@pytest.mark.parametrize(
    "timestamp",
    [
        "2026-02-30T00:00:00Z",
        "2026-08-01T24:00:00Z",
        "2026-08-01T00:60:00Z",
        "2026-08-01T00:00:60Z",
        "2026-8-01T00:00:00Z",
        "\uff12\uff10\uff12\uff16-08-01T00:00:00Z",
    ],
)
def test_timestamp_validation_is_calendar_exact(tmp_path: Path, timestamp: str) -> None:
    document = _ready_manifest()
    _measurements(document)[0]["opened_at"] = timestamp
    _assert_rejected(document, tmp_path)


def test_measurement_record_limit_is_enforced(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _ready_manifest()
    _first_window(document)["measurements"] = [_measurements(document)[0]] * 257
    module, evaluate = _evaluator()
    monkeypatch.setattr(module, "_MAX_MANIFEST_BYTES", 1_000_000)
    with pytest.raises(RuntimeError, match="record limit"):
        evaluate(_write_manifest(tmp_path, document))
