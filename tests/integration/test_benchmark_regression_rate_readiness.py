"""M33 benchmark-regression-rate admission evidence."""

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
_EXAMPLE = _ROOT / "examples" / "benchmark_regression_rate_readiness.py"
_VALIDATOR = _ROOT / "scripts" / "benchmark_regression_rate_evidence.py"
_MANIFEST = _ROOT / "tests" / "fixtures" / "benchmark_regression_rate.json"
_BASE = datetime(2026, 8, 1, tzinfo=UTC)
_PROJECT = "https://github.com/xsparc/ludoweave-engine"


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
    module = _load(_VALIDATOR, "benchmark_regression_rate_validator")
    return cast(_Validate, module.validate_benchmark_regression_rate_evidence)


def _evaluator() -> tuple[ModuleType, _Evaluate]:
    module = _load(_EXAMPLE, "benchmark_regression_rate_example")
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


def _digest(role: str, index: int) -> str:
    return hashlib.sha256(f"{role}-{index}".encode()).hexdigest()


def _manifest() -> dict[str, object]:
    return cast(dict[str, object], json.loads(_MANIFEST.read_text(encoding="utf-8")))


def _evidence_url(revision: str, role: str, digest: str) -> str:
    return f"{_PROJECT}/blob/{revision}/evidence/benchmark-regression-rate/{role}-{digest}.json"


def _comparison(
    index: int,
    *,
    outcome: str = "stable",
    baseline_p95_ns: int = 1_000_000,
    candidate_p95_ns: int = 1_050_000,
    tolerance_bps: int = 500,
) -> dict[str, object]:
    run_number = 1000 + index
    job_number = 2000 + index
    base_sha = _digest("base", index)[:40]
    head_sha = _digest("head", index)[:40]
    evidence_revision = "1" * 40
    run_url = f"{_PROJECT}/actions/runs/{run_number}"
    result_hash = _digest("result", index)
    runner_hash = _digest("runner", index)
    baseline_hash: str | None = _digest("baseline", index)
    candidate_hash: str | None = _digest("candidate", index)
    baseline_url: str | None = _evidence_url(evidence_revision, "baseline", baseline_hash)
    candidate_url: str | None = _evidence_url(evidence_revision, "candidate", candidate_hash)
    baseline_value: int | None = baseline_p95_ns
    candidate_value: int | None = candidate_p95_ns
    if outcome == "stable":
        outcome_code = "benchmark-within-tolerance"
    elif outcome == "regressed":
        outcome_code = "benchmark-regressed"
    else:
        outcome_code = "job-failed-before-benchmark"
        baseline_value = candidate_value = None
        baseline_hash = candidate_hash = None
        baseline_url = candidate_url = None
    return {
        "comparison_id": f"comparison-{index:04d}",
        "run_url": run_url,
        "job_url": f"{run_url}/job/{job_number}",
        "base_sha": base_sha,
        "head_sha": head_sha,
        "workflow_url": f"{_PROJECT}/blob/{head_sha}/.github/workflows/ci.yml",
        "workflow_sha256": _digest("workflow", index),
        "benchmark_schema": "ludoweave.benchmark.m1/1",
        "benchmark_case": "simulation_tick_10000",
        "baseline_source_url": f"{_PROJECT}/blob/{base_sha}/benchmarks/benchmark_m1.py",
        "baseline_source_sha256": _digest("baseline-source", index),
        "candidate_source_url": f"{_PROJECT}/blob/{head_sha}/benchmarks/benchmark_m1.py",
        "candidate_source_sha256": _digest("candidate-source", index),
        "runner_profile_url": _evidence_url(evidence_revision, "runner", runner_hash),
        "runner_profile_sha256": runner_hash,
        "environment_profile": "github-ubuntu-cpython-3.12-gil-x86_64-v1",
        "metric": "p95_ns",
        "tolerance_bps": tolerance_bps,
        "started_at": _timestamp(_BASE + timedelta(minutes=10 * index)),
        "outcome": outcome,
        "baseline_p95_ns": baseline_value,
        "candidate_p95_ns": candidate_value,
        "outcome_code": outcome_code,
        "result_url": _evidence_url(evidence_revision, "result", result_hash),
        "result_sha256": result_hash,
        "baseline_artifact_url": baseline_url,
        "baseline_artifact_sha256": baseline_hash,
        "candidate_artifact_url": candidate_url,
        "candidate_artifact_sha256": candidate_hash,
        "eligible_comparison_reviewed": True,
        "comparability_reviewed": True,
        "threshold_predeclared_reviewed": True,
        "outcome_reviewed": True,
        "provenance_reviewed": True,
        "validation_reviewed": True,
    }


def _window(comparisons: list[dict[str, object]], *, index: int = 1) -> dict[str, object]:
    revision = str(index) * 40
    census_hash = _digest("census", index)
    review_hash = _digest("review", index)
    return {
        "window_id": f"window-{index:04d}",
        "started_from": _timestamp(_BASE + timedelta(days=index - 1)),
        "started_before": _timestamp(_BASE + timedelta(days=index)),
        "observed_through": _timestamp(_BASE + timedelta(days=index + 1)),
        "census_url": _evidence_url(revision, "census", census_hash),
        "census_sha256": census_hash,
        "review_url": _evidence_url(revision, "review", review_hash),
        "review_sha256": review_hash,
        "comparisons": comparisons,
        "controlled_runner_census_complete_reviewed": True,
        "eligibility_reviewed": True,
        "comparability_reviewed": True,
        "provenance_reviewed": True,
        "validation_reviewed": True,
    }


def _ready_manifest() -> dict[str, object]:
    document = _manifest()
    document["evaluation_windows"] = [
        _window(
            [
                _comparison(1),
                _comparison(
                    2,
                    outcome="regressed",
                    baseline_p95_ns=1_000_000,
                    candidate_p95_ns=1_050_001,
                ),
            ]
        )
    ]
    return document


def _write(tmp_path: Path, document: dict[str, object], name: str = "manifest.json") -> Path:
    path = tmp_path / name
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
    return cast(dict[str, object], cast(list[object], document["evaluation_windows"])[0])


def _comparisons(document: dict[str, object]) -> list[dict[str, object]]:
    return cast(list[dict[str, object]], _first_window(document)["comparisons"])


def _assert_rejected(document: dict[str, object], tmp_path: Path) -> None:
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError):
        evaluate(_write(tmp_path, document))


def test_default_report_is_repeatable_sanitized_and_not_ready() -> None:
    first = _run()
    second = _run("--manifest", str(_MANIFEST))

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["gate_satisfied"] is False
    assert document["benchmark_regression_rate_proven"] is False
    admission = cast(dict[str, object], document["admission"])
    assert admission["reason_codes"] == ["benchmark-regression-rate-evidence-absent"]
    for forbidden in (
        "run_url",
        "job_url",
        "base_sha",
        "head_sha",
        "environment_profile",
        "benchmark_case",
        "started_at",
        "artifact_url",
        str(_ROOT),
    ):
        assert forbidden not in first.stdout


def test_missing_manifest_error_is_path_free(tmp_path: Path) -> None:
    missing = tmp_path / "private" / "missing.json"
    result = _run("--manifest", str(missing))

    assert result.returncode == 1
    assert result.stdout == ""
    assert "benchmark-regression manifest is unavailable" in result.stderr
    assert str(tmp_path) not in result.stderr


def test_validator_rejects_value_and_json_type_drift() -> None:
    document = cast(dict[str, object], json.loads(_run().stdout))
    validator = _validator()
    drifted = deepcopy(document)
    drifted["gate_satisfied"] = True
    with pytest.raises(RuntimeError, match="evidence drifted"):
        validator(drifted, version=__version__)
    typed = deepcopy(document)
    cast(dict[str, object], typed["metrics"])["window_count"] = False
    with pytest.raises(RuntimeError, match="evidence drifted"):
        validator(typed, version=__version__)


def test_complete_reviewed_cohort_reports_exact_rational_rate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module, evaluate = _evaluator()
    report = _admit(module, evaluate, _write(tmp_path, _ready_manifest()), monkeypatch)

    assert report["gate_satisfied"] is True
    assert report["benchmark_regression_rate_proven"] is True
    assert report["evidence_level"] == "reviewed-controlled-benchmark-regression-rate"
    metrics = cast(dict[str, object], report["metrics"])
    assert metrics == {
        "comparison_count": 2,
        "manifest_sha256": metrics["manifest_sha256"],
        "measurement_policy": "complete-reviewed-controlled-benchmark-comparisons/1",
        "not_executed_count": 0,
        "records_verified": True,
        "regressed_count": 1,
        "regression_rate": {"denominator": 2, "numerator": 1},
        "stable_count": 1,
        "window_count": 1,
    }
    encoded = json.dumps(report, sort_keys=True)
    assert "actions/runs" not in encoded
    assert "simulation_tick" not in encoded
    assert "github-ubuntu" not in encoded


def test_exact_integer_threshold_treats_equality_as_stable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _manifest()
    document["evaluation_windows"] = [_window([_comparison(1)])]
    module, evaluate = _evaluator()

    report = _admit(module, evaluate, _write(tmp_path, document), monkeypatch)

    metrics = cast(dict[str, object], report["metrics"])
    assert metrics["stable_count"] == 1
    assert metrics["regressed_count"] == 0
    assert metrics["regression_rate"] == {"denominator": 1, "numerator": 0}


def test_one_nanosecond_above_threshold_must_be_regressed(tmp_path: Path) -> None:
    document = _manifest()
    document["evaluation_windows"] = [_window([_comparison(1, candidate_p95_ns=1_050_001)])]
    _assert_rejected(document, tmp_path)


def test_non_executed_comparison_is_preserved_and_blocks_rate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _ready_manifest()
    _comparisons(document)[1] = _comparison(2, outcome="not-executed")
    module, evaluate = _evaluator()

    report = _admit(module, evaluate, _write(tmp_path, document), monkeypatch)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["reason_codes"] == ("benchmark-comparison-cohort-incomplete",)
    metrics = cast(dict[str, object], report["metrics"])
    assert metrics["comparison_count"] == 2
    assert metrics["not_executed_count"] == 1
    assert metrics["regression_rate"] is None


def test_unreviewed_candidate_exposes_no_comparison_aggregates(tmp_path: Path) -> None:
    _, evaluate = _evaluator()

    report = evaluate(_write(tmp_path, _ready_manifest()))

    metrics = cast(dict[str, object], report["metrics"])
    assert metrics["comparison_count"] == 0
    assert metrics["regression_rate"] is None


def test_mandatory_history_rejects_replacement_window(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = _ready_manifest()
    original_path = _write(tmp_path, original, "original.json")
    module, evaluate = _evaluator()
    parse = cast(_ParseManifest, module._parse_manifest)
    _, original_identities = parse(original_path)
    replacement = deepcopy(original)
    _comparisons(replacement)[0]["candidate_p95_ns"] = 900_000
    replacement_path = _write(tmp_path, replacement, "replacement.json")
    monkeypatch.setattr(
        module,
        "_REVIEWED_MANIFEST_SHA256",
        hashlib.sha256(replacement_path.read_bytes()).hexdigest(),
    )
    monkeypatch.setattr(module, "_MANDATORY_WINDOW_PREFIX", original_identities)

    report = evaluate(replacement_path)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert "historical-evaluation-window-missing" in cast(list[str], admission["reason_codes"])


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schema", "ludoweave.performance.benchmark-regression-rate/2"),
        ("source_project", "another-project"),
        ("measurement_policy", "successful-comparisons-only/1"),
        ("evaluation_windows", {}),
    ],
)
def test_manifest_rejects_incompatible_values(tmp_path: Path, field: str, value: object) -> None:
    document = _manifest()
    document[field] = value
    _assert_rejected(document, tmp_path)


def test_manifest_rejects_unknown_duplicate_size_nesting_and_symlink(tmp_path: Path) -> None:
    document = _manifest()
    document["unexpected"] = True
    _assert_rejected(document, tmp_path)

    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text(
        '{"schema":"a","schema":"b","source_project":"ludoweave-engine",'
        '"measurement_policy":"complete-reviewed-controlled-benchmark-comparisons/1",'
        '"evaluation_windows":[]}',
        encoding="utf-8",
    )
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError, match="not valid JSON"):
        evaluate(duplicate)
    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * 131_073)
    with pytest.raises(RuntimeError, match="byte limit"):
        evaluate(oversized)
    nested = tmp_path / "nested.json"
    nested.write_text("[" * 17 + "]" * 17, encoding="utf-8")
    with pytest.raises(RuntimeError, match="nesting limit"):
        evaluate(nested)
    link = tmp_path / "manifest-link.json"
    try:
        link.symlink_to(_MANIFEST)
    except OSError:
        return
    with pytest.raises(RuntimeError, match="symbolic link"):
        evaluate(link)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("window_id", "window-1"),
        ("started_before", "2026-08-01T00:00:00Z"),
        ("observed_through", "2026-08-02T00:00:00Z"),
        ("census_sha256", "A" * 64),
        ("controlled_runner_census_complete_reviewed", False),
        ("eligibility_reviewed", 1),
        ("comparability_reviewed", None),
        ("provenance_reviewed", "true"),
        ("validation_reviewed", False),
    ],
)
def test_window_rejects_invalid_identity_time_hash_and_review(
    tmp_path: Path, field: str, value: object
) -> None:
    document = _ready_manifest()
    _first_window(document)[field] = value
    _assert_rejected(document, tmp_path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("comparison_id", "comparison-1"),
        ("run_url", f"{_PROJECT}/actions/runs/01001"),
        ("base_sha", "A" * 40),
        ("benchmark_schema", "ludoweave.profile.m7/1"),
        ("benchmark_case", "not_registered"),
        ("environment_profile", "Host Name"),
        ("metric", "mean_ns"),
        ("tolerance_bps", -1),
        ("tolerance_bps", 10_001),
        ("started_at", "2026-08-02T00:00:00Z"),
        ("eligible_comparison_reviewed", False),
        ("comparability_reviewed", 1),
        ("threshold_predeclared_reviewed", None),
        ("outcome_reviewed", "true"),
        ("provenance_reviewed", False),
        ("validation_reviewed", 0),
    ],
)
def test_comparison_rejects_invalid_identity_registration_metric_and_reviews(
    tmp_path: Path, field: str, value: object
) -> None:
    document = _ready_manifest()
    _comparisons(document)[0][field] = value
    _assert_rejected(document, tmp_path)


def test_comparison_rejects_noncanonical_sources_and_evidence(tmp_path: Path) -> None:
    mutations = (
        ("workflow_url", f"{_PROJECT}/blob/main/.github/workflows/ci.yml"),
        ("baseline_source_url", f"{_PROJECT}/blob/main/benchmarks/benchmark_m1.py"),
        ("candidate_source_url", f"{_PROJECT}/blob/main/benchmarks/benchmark_m1.py"),
        ("runner_profile_url", "https://example.com/runner.json"),
        ("result_url", "https://example.com/result.json"),
        ("baseline_artifact_url", "https://example.com/baseline.json"),
        ("candidate_artifact_url", "https://example.com/candidate.json"),
    )
    for field, value in mutations:
        document = _ready_manifest()
        _comparisons(document)[0][field] = value
        _assert_rejected(document, tmp_path)


def test_stable_regressed_and_nonexecution_outcome_evidence_is_exact(tmp_path: Path) -> None:
    for field, value in (
        ("baseline_p95_ns", 0),
        ("candidate_p95_ns", None),
        ("outcome_code", "passed"),
        ("baseline_artifact_sha256", None),
    ):
        document = _ready_manifest()
        _comparisons(document)[0][field] = value
        _assert_rejected(document, tmp_path)

    document = _ready_manifest()
    _comparisons(document)[1]["outcome"] = "stable"
    _comparisons(document)[1]["outcome_code"] = "benchmark-within-tolerance"
    _assert_rejected(document, tmp_path)

    for field, value in (
        ("baseline_p95_ns", 1),
        ("candidate_artifact_url", "x"),
        ("outcome_code", "benchmark-regressed"),
    ):
        document = _ready_manifest()
        _comparisons(document)[1] = _comparison(2, outcome="not-executed")
        _comparisons(document)[1][field] = value
        _assert_rejected(document, tmp_path)


def test_duplicate_comparison_and_evidence_identities_are_rejected(tmp_path: Path) -> None:
    document = _ready_manifest()
    duplicate = deepcopy(_comparisons(document)[0])
    duplicate["comparison_id"] = "comparison-0002"
    duplicate["started_at"] = _timestamp(_BASE + timedelta(minutes=20))
    _first_window(document)["comparisons"] = [_comparisons(document)[0], duplicate]
    _assert_rejected(document, tmp_path)

    document = _ready_manifest()
    _comparisons(document)[1]["result_sha256"] = _comparisons(document)[0]["result_sha256"]
    _comparisons(document)[1]["result_url"] = _comparisons(document)[0]["result_url"]
    _assert_rejected(document, tmp_path)


def test_shared_controlled_runner_profile_is_reusable_within_a_window(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _ready_manifest()
    first, second = _comparisons(document)
    second["runner_profile_url"] = first["runner_profile_url"]
    second["runner_profile_sha256"] = first["runner_profile_sha256"]
    second["environment_profile"] = first["environment_profile"]
    module, evaluate = _evaluator()

    report = _admit(module, evaluate, _write(tmp_path, document), monkeypatch)

    assert report["gate_satisfied"] is True
    assert cast(dict[str, object], report["metrics"])["comparison_count"] == 2


def test_all_registered_schema_case_pairs_parse(tmp_path: Path) -> None:
    module, _ = _evaluator()
    registrations = cast(dict[str, tuple[str, tuple[str, ...]]], module._REGISTERED_WORKLOADS)
    for schema, (source, cases) in registrations.items():
        for case in cases:
            document = _manifest()
            comparison = _comparison(1)
            comparison["benchmark_schema"] = schema
            comparison["benchmark_case"] = case
            base_sha = cast(str, comparison["base_sha"])
            head_sha = cast(str, comparison["head_sha"])
            comparison["baseline_source_url"] = f"{_PROJECT}/blob/{base_sha}/{source}"
            comparison["candidate_source_url"] = f"{_PROJECT}/blob/{head_sha}/{source}"
            document["evaluation_windows"] = [_window([comparison])]
            cast(_ParseManifest, module._parse_manifest)(_write(tmp_path, document, f"{case}.json"))


def test_cprofile_schema_is_not_a_registered_timing_comparison() -> None:
    module, _ = _evaluator()
    registrations = cast(dict[str, object], module._REGISTERED_WORKLOADS)

    assert "ludoweave.profile.m7/1" not in registrations
    assert set(registrations) == {
        "ludoweave.benchmark.m1/1",
        "ludoweave.benchmark.m2/1",
        "ludoweave.benchmark.m3/1",
        "ludoweave.benchmark.m4/1",
    }
