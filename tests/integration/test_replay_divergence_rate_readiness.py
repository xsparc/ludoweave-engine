"""M32 CI replay-divergence-rate admission evidence."""

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
_EXAMPLE = _ROOT / "examples" / "replay_divergence_rate_readiness.py"
_VALIDATOR = _ROOT / "scripts" / "replay_divergence_rate_evidence.py"
_MANIFEST = _ROOT / "tests" / "fixtures" / "replay_divergence_rate.json"
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
    module = _load(_VALIDATOR, "replay_divergence_rate_validator")
    return cast(_Validate, module.validate_replay_divergence_rate_evidence)


def _evaluator() -> tuple[ModuleType, _Evaluate]:
    module = _load(_EXAMPLE, "replay_divergence_rate_example")
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


def _execution(index: int, *, outcome: str = "verified") -> dict[str, object]:
    run_number = 1000 + index
    job_number = 2000 + index
    head_sha = _digest("head", index)[:40]
    expected_hash: str | None
    actual_hash: str | None
    first_tick: int | None
    if outcome == "verified":
        expected_hash = actual_hash = _digest("state", index)
        first_tick = None
        outcome_code = "replay-verified"
    elif outcome == "diverged":
        expected_hash = _digest("expected", index)
        actual_hash = _digest("actual", index)
        first_tick = 300 + index
        outcome_code = "world.replay.divergence"
    else:
        expected_hash = actual_hash = None
        first_tick = None
        outcome_code = "job-failed-before-replay"
    result_hash = _digest("result", index)
    evidence_revision = "1" * 40
    run_url = f"{_PROJECT}/actions/runs/{run_number}"
    return {
        "execution_id": f"execution-{index:04d}",
        "run_url": run_url,
        "job_url": f"{run_url}/job/{job_number}",
        "head_sha": head_sha,
        "workflow_url": f"{_PROJECT}/blob/{head_sha}/.github/workflows/ci.yml",
        "workflow_sha256": _digest("workflow", index),
        "case_id": f"clockwork-arena-{index}",
        "case_url": f"{_PROJECT}/blob/{head_sha}/tests/integration/test_clockwork_arena.py",
        "case_sha256": _digest("case", index),
        "started_at": _timestamp(_BASE + timedelta(minutes=10 * index)),
        "outcome": outcome,
        "expected_state_sha256": expected_hash,
        "actual_state_sha256": actual_hash,
        "first_divergent_tick": first_tick,
        "outcome_code": outcome_code,
        "result_url": (
            f"{_PROJECT}/blob/{evidence_revision}/evidence/replay-divergence-rate/"
            f"result-{result_hash}.json"
        ),
        "result_sha256": result_hash,
        "eligible_execution_reviewed": True,
        "outcome_reviewed": True,
        "provenance_reviewed": True,
        "validation_reviewed": True,
    }


def _window(executions: list[dict[str, object]], *, index: int = 1) -> dict[str, object]:
    revision = str(index) * 40
    census_hash = _digest("census", index)
    review_hash = _digest("review", index)
    return {
        "window_id": f"window-{index:04d}",
        "started_from": _timestamp(_BASE + timedelta(days=index - 1)),
        "started_before": _timestamp(_BASE + timedelta(days=index)),
        "observed_through": _timestamp(_BASE + timedelta(days=index + 1)),
        "census_url": (
            f"{_PROJECT}/blob/{revision}/evidence/replay-divergence-rate/census-{census_hash}.json"
        ),
        "census_sha256": census_hash,
        "review_url": (
            f"{_PROJECT}/blob/{revision}/evidence/replay-divergence-rate/review-{review_hash}.json"
        ),
        "review_sha256": review_hash,
        "executions": executions,
        "public_ci_census_complete_reviewed": True,
        "eligibility_reviewed": True,
        "provenance_reviewed": True,
        "validation_reviewed": True,
    }


def _ready_manifest() -> dict[str, object]:
    document = _manifest()
    document["evaluation_windows"] = [_window([_execution(1), _execution(2, outcome="diverged")])]
    return document


def _write_manifest(
    tmp_path: Path, document: dict[str, object], name: str = "manifest.json"
) -> Path:
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


def _executions(document: dict[str, object]) -> list[dict[str, object]]:
    return cast(list[dict[str, object]], _first_window(document)["executions"])


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
    assert document["divergence_rate_proven"] is False
    assert document["status"] == "not-ready"
    admission = cast(dict[str, object], document["admission"])
    assert admission["reason_codes"] == ["replay-divergence-rate-evidence-absent"]
    for forbidden in (
        "run_url",
        "job_url",
        "workflow_url",
        "case_url",
        "result_url",
        "started_at",
        "expected_state_sha256",
        "actual_state_sha256",
        "window_id",
        str(_ROOT),
    ):
        assert forbidden not in first.stdout


def test_missing_manifest_error_is_path_free(tmp_path: Path) -> None:
    missing = tmp_path / "private" / "missing.json"
    result = _run("--manifest", str(missing))

    assert result.returncode == 1
    assert result.stdout == ""
    assert "replay-divergence manifest is unavailable" in result.stderr
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


def test_reviewed_complete_cohort_reports_exact_rational_rate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module, evaluate = _evaluator()
    report = _admit(module, evaluate, _write_manifest(tmp_path, _ready_manifest()), monkeypatch)

    assert report["gate_satisfied"] is True
    assert report["divergence_rate_proven"] is True
    assert report["evidence_level"] == "reviewed-ci-replay-divergence-rate"
    metrics = cast(dict[str, object], report["metrics"])
    assert metrics == {
        "diverged_count": 1,
        "divergence_rate": {"denominator": 2, "numerator": 1},
        "execution_count": 2,
        "manifest_sha256": metrics["manifest_sha256"],
        "measurement_policy": "complete-reviewed-ci-replay-executions/1",
        "not_executed_count": 0,
        "records_verified": True,
        "verified_count": 1,
        "window_count": 1,
    }
    encoded = json.dumps(report, sort_keys=True)
    assert "actions/runs" not in encoded
    assert "clockwork-arena" not in encoded
    assert "2026-08" not in encoded


def test_non_executed_case_is_preserved_and_blocks_rate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _ready_manifest()
    _executions(document)[1] = _execution(2, outcome="not-executed")
    module, evaluate = _evaluator()

    report = _admit(module, evaluate, _write_manifest(tmp_path, document), monkeypatch)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["reason_codes"] == ("replay-execution-cohort-incomplete",)
    metrics = cast(dict[str, object], report["metrics"])
    assert metrics["execution_count"] == 2
    assert metrics["not_executed_count"] == 1
    assert metrics["divergence_rate"] is None


def test_unreviewed_candidate_exposes_no_execution_aggregates(tmp_path: Path) -> None:
    _, evaluate = _evaluator()

    report = evaluate(_write_manifest(tmp_path, _ready_manifest()))

    admission = cast(dict[str, object], report["admission"])
    assert "replay-divergence-manifest-identity-unreviewed" in cast(
        list[str], admission["reason_codes"]
    )
    metrics = cast(dict[str, object], report["metrics"])
    assert metrics["execution_count"] == 0
    assert metrics["divergence_rate"] is None


def test_mandatory_history_rejects_replacement_window(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = _ready_manifest()
    original_path = _write_manifest(tmp_path, original, "original.json")
    module, evaluate = _evaluator()
    parse = cast(_ParseManifest, module._parse_manifest)
    _, original_identities = parse(original_path)
    replacement = deepcopy(original)
    _executions(replacement)[0] = _execution(1, outcome="diverged")
    replacement_path = _write_manifest(tmp_path, replacement, "replacement.json")
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
    assert cast(dict[str, object], report["metrics"])["execution_count"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schema", "ludoweave.ci.replay-divergence-rate/2"),
        ("source_project", "another-project"),
        ("measurement_policy", "passing-replays-only/1"),
        ("evaluation_windows", {}),
    ],
)
def test_manifest_rejects_incompatible_values(tmp_path: Path, field: str, value: object) -> None:
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
        '"measurement_policy":"complete-reviewed-ci-replay-executions/1",'
        '"evaluation_windows":[]}',
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
    document["evaluation_windows"] = [{}] * 13
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
        ("started_before", "2026-08-01T00:00:00Z"),
        ("observed_through", "2026-08-01T12:00:00Z"),
        ("census_sha256", "A" * 64),
        ("review_sha256", "b" * 63),
        ("public_ci_census_complete_reviewed", False),
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
            f"{_PROJECT}/blob/main/evidence/replay-divergence-rate/"
            f"census-{_digest('census', 1)}.json",
        ),
        (
            "review_url",
            f"{_PROJECT}/blob/{'2' * 40}/evidence/replay-divergence-rate/"
            f"review-{_digest('review', 1)}.json",
        ),
    ):
        document = _ready_manifest()
        _first_window(document)[field] = value
        _assert_rejected(document, tmp_path)


def test_window_rejects_excess_duration_observation_lag_and_overlap(tmp_path: Path) -> None:
    document = _ready_manifest()
    _first_window(document)["started_before"] = "2028-01-01T00:00:00Z"
    _first_window(document)["observed_through"] = "2028-01-02T00:00:00Z"
    _assert_rejected(document, tmp_path)

    document = _ready_manifest()
    window = _first_window(document)
    window["observed_through"] = window["started_before"]
    _assert_rejected(document, tmp_path)

    document = _ready_manifest()
    second = _window([], index=2)
    second["started_from"] = "2026-08-01T12:00:00Z"
    document["evaluation_windows"] = [_first_window(document), second]
    _assert_rejected(document, tmp_path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("execution_id", "execution-1"),
        ("run_url", f"{_PROJECT}/actions/runs/01001"),
        ("job_url", f"{_PROJECT}/actions/runs/1001/job/0"),
        ("head_sha", "A" * 40),
        ("workflow_sha256", "g" * 64),
        ("case_id", "Clockwork"),
        ("case_sha256", "f" * 63),
        ("started_at", "2026-08-02T00:00:00Z"),
        ("outcome", "passed"),
        ("eligible_execution_reviewed", False),
        ("outcome_reviewed", 1),
        ("provenance_reviewed", None),
        ("validation_reviewed", "true"),
    ],
)
def test_execution_rejects_invalid_identity_type_bounds_and_reviews(
    tmp_path: Path, field: str, value: object
) -> None:
    document = _ready_manifest()
    _executions(document)[0][field] = value
    _assert_rejected(document, tmp_path)


def test_execution_rejects_noncanonical_workflow_case_and_result_urls(tmp_path: Path) -> None:
    mutations = (
        ("workflow_url", f"{_PROJECT}/blob/main/.github/workflows/ci.yml"),
        ("case_url", f"{_PROJECT}/blob/{_digest('head', 1)[:40]}/src/replay.py"),
        (
            "case_url",
            f"{_PROJECT}/blob/{_digest('head', 1)[:40]}/tests/test_replay.py#note.py",
        ),
        (
            "case_url",
            f"{_PROJECT}/blob/{_digest('head', 1)[:40]}/tests/test%2freplay.py",
        ),
        (
            "case_url",
            f"{_PROJECT}/blob/{_digest('head', 1)[:40]}/tests/test_replay.py?plain=.py",
        ),
        ("result_url", "https://example.com/result.json"),
        (
            "result_url",
            f"{_PROJECT}/blob/{'2' * 40}/evidence/replay-divergence-rate/"
            f"result-{_digest('result', 1)}.json",
        ),
    )
    for field, value in mutations:
        document = _ready_manifest()
        _executions(document)[0][field] = value
        _assert_rejected(document, tmp_path)


def test_verified_execution_requires_equal_hashes_and_exact_code(tmp_path: Path) -> None:
    for field, value in (
        ("expected_state_sha256", None),
        ("actual_state_sha256", _digest("other", 1)),
        ("first_divergent_tick", 0),
        ("outcome_code", "passed"),
    ):
        document = _ready_manifest()
        _executions(document)[0][field] = value
        _assert_rejected(document, tmp_path)


def test_diverged_execution_requires_distinct_hashes_tick_and_exact_code(tmp_path: Path) -> None:
    for field, value in (
        ("expected_state_sha256", None),
        ("actual_state_sha256", _digest("expected", 2)),
        ("first_divergent_tick", None),
        ("first_divergent_tick", -1),
        ("outcome_code", "replay-diverged"),
    ):
        document = _ready_manifest()
        _executions(document)[1][field] = value
        _assert_rejected(document, tmp_path)


def test_non_executed_case_rejects_any_replay_outcome_claim(tmp_path: Path) -> None:
    fields: tuple[tuple[str, object], ...] = (
        ("expected_state_sha256", _digest("expected", 2)),
        ("actual_state_sha256", _digest("actual", 2)),
        ("first_divergent_tick", 2),
        ("outcome_code", "replay-verified"),
    )
    for field, value in fields:
        document = _ready_manifest()
        _executions(document)[1] = _execution(2, outcome="not-executed")
        _executions(document)[1][field] = value
        _assert_rejected(document, tmp_path)


def test_non_execution_reason_codes_are_exact(tmp_path: Path) -> None:
    for code in (
        "job-cancelled",
        "job-failed-before-replay",
        "replay-case-skipped",
        "result-evidence-unavailable",
    ):
        document = _ready_manifest()
        _executions(document)[1] = _execution(2, outcome="not-executed")
        _executions(document)[1]["outcome_code"] = code
        _, evaluate = _evaluator()
        evaluate(_write_manifest(tmp_path, document))
    document = _ready_manifest()
    _executions(document)[1] = _execution(2, outcome="not-executed")
    _executions(document)[1]["outcome_code"] = "unknown"
    _assert_rejected(document, tmp_path)


def test_executions_require_canonical_order_and_unique_identity(tmp_path: Path) -> None:
    document = _ready_manifest()
    executions = _executions(document)
    executions[0], executions[1] = executions[1], executions[0]
    executions[0]["execution_id"] = "execution-0001"
    executions[1]["execution_id"] = "execution-0002"
    _assert_rejected(document, tmp_path)

    document = _ready_manifest()
    first, second = _executions(document)
    second["run_url"] = first["run_url"]
    second["job_url"] = first["job_url"]
    second["case_id"] = first["case_id"]
    _assert_rejected(document, tmp_path)


def test_duplicate_result_evidence_is_rejected(tmp_path: Path) -> None:
    for field in ("result_url", "result_sha256"):
        document = _ready_manifest()
        first, second = _executions(document)
        second[field] = first[field]
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
    _executions(document)[0]["started_at"] = timestamp
    _assert_rejected(document, tmp_path)


def test_execution_limit_is_enforced(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    document = _ready_manifest()
    _first_window(document)["executions"] = [_executions(document)[0]] * 513
    module, evaluate = _evaluator()
    monkeypatch.setattr(module, "_MAX_MANIFEST_BYTES", 1_000_000)
    with pytest.raises(RuntimeError, match="execution limit"):
        evaluate(_write_manifest(tmp_path, document))
