"""M34 agent-tool recovery-rate admission evidence."""

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
from ludoweave.agent import AGENT_TOOL_NAMES

_ROOT = Path(__file__).parents[2]
_EXAMPLE = _ROOT / "examples" / "agent_tool_recovery_rate_readiness.py"
_VALIDATOR = _ROOT / "scripts" / "agent_tool_recovery_rate_evidence.py"
_MANIFEST = _ROOT / "tests" / "fixtures" / "agent_tool_recovery_rate.json"
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
    module = _load(_VALIDATOR, "agent_tool_recovery_rate_validator")
    return cast(_Validate, module.validate_agent_tool_recovery_rate_evidence)


def _evaluator() -> tuple[ModuleType, _Evaluate]:
    module = _load(_EXAMPLE, "agent_tool_recovery_rate_example")
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


def _evidence_url(role: str, digest: str, *, revision: str = "1" * 40) -> str:
    return f"{_PROJECT}/blob/{revision}/evidence/agent-tool-recovery-rate/{role}-{digest}.json"


def _call(
    index: int,
    *,
    outcome: str = "completed-without-manual-recovery",
    session_id: str = "session-0001",
    session_call_index: int | None = None,
) -> dict[str, object]:
    engine_sha = _digest("engine", 1)[:40]
    call_hash = _digest("call", index)
    result_hash: str | None = _digest("result", index)
    recovery_hash: str | None = None
    recovery_occurred: bool | None
    if outcome == "completed-without-manual-recovery":
        recovery_occurred = False
        outcome_code = "tool-call-completed"
    elif outcome == "completed-after-manual-recovery":
        recovery_occurred = True
        outcome_code = "tool-call-completed-after-manual-recovery"
        recovery_hash = _digest("recovery", index)
    elif outcome == "not-completed":
        recovery_occurred = False
        outcome_code = "tool-call-failed"
    else:
        recovery_occurred = None
        outcome_code = "call-terminal-state-unobserved"
        result_hash = None
    return {
        "call_id": f"call-{index:04d}",
        "session_id": session_id,
        "session_call_index": index if session_call_index is None else session_call_index,
        "adapter_id": "org.example.adapter",
        "tool_name": AGENT_TOOL_NAMES[(index - 1) % len(AGENT_TOOL_NAMES)],
        "service_protocol": "ludoweave.agent.service/1",
        "engine_sha": engine_sha,
        "service_contract_url": (f"{_PROJECT}/blob/{engine_sha}/src/ludoweave/agent/tools.py"),
        "service_contract_sha256": _digest("service-contract", 1),
        "started_at": _timestamp(_BASE + timedelta(minutes=10 * index)),
        "outcome": outcome,
        "manual_recovery_occurred": recovery_occurred,
        "outcome_code": outcome_code,
        "call_evidence_url": _evidence_url("call", call_hash),
        "call_evidence_sha256": call_hash,
        "result_evidence_url": (
            None if result_hash is None else _evidence_url("result", result_hash)
        ),
        "result_evidence_sha256": result_hash,
        "recovery_evidence_url": (
            None if recovery_hash is None else _evidence_url("recovery", recovery_hash)
        ),
        "recovery_evidence_sha256": recovery_hash,
        "eligible_call_reviewed": True,
        "task_directed_context_reviewed": True,
        "manual_recovery_reviewed": True,
        "outcome_reviewed": True,
        "privacy_and_consent_reviewed": True,
        "provenance_reviewed": True,
        "validation_reviewed": True,
    }


def _window(calls: list[dict[str, object]], *, index: int = 1) -> dict[str, object]:
    revision = str(index) * 40
    census_hash = _digest("census", index)
    review_hash = _digest("review", index)
    return {
        "window_id": f"window-{index:04d}",
        "started_from": _timestamp(_BASE + timedelta(days=index - 1)),
        "started_before": _timestamp(_BASE + timedelta(days=index)),
        "observed_through": _timestamp(_BASE + timedelta(days=index + 1)),
        "census_url": _evidence_url("census", census_hash, revision=revision),
        "census_sha256": census_hash,
        "review_url": _evidence_url("review", review_hash, revision=revision),
        "review_sha256": review_hash,
        "calls": calls,
        "task_directed_session_census_complete_reviewed": True,
        "eligibility_reviewed": True,
        "manual_recovery_definition_reviewed": True,
        "privacy_and_consent_reviewed": True,
        "provenance_reviewed": True,
        "validation_reviewed": True,
    }


def _ready_manifest() -> dict[str, object]:
    document = _manifest()
    document["evaluation_windows"] = [
        _window(
            [
                _call(1),
                _call(2, outcome="completed-after-manual-recovery"),
                _call(3, outcome="not-completed"),
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


def _calls(document: dict[str, object]) -> list[dict[str, object]]:
    return cast(list[dict[str, object]], _first_window(document)["calls"])


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
    assert document["completion_without_manual_recovery_rate_proven"] is False
    assert document["status"] == "not-ready"
    assert cast(dict[str, object], document["admission"])["reason_codes"] == [
        "agent-tool-recovery-rate-evidence-absent"
    ]
    for forbidden in (
        "session_id",
        "adapter_id",
        "tool_name",
        "started_at",
        "call_evidence_url",
        "result_evidence_url",
        "recovery_evidence_url",
        "window_id",
        str(_ROOT),
    ):
        assert forbidden not in first.stdout


def test_missing_manifest_error_is_path_free(tmp_path: Path) -> None:
    missing = tmp_path / "private" / "missing.json"
    result = _run("--manifest", str(missing))

    assert result.returncode == 1
    assert result.stdout == ""
    assert "agent-tool recovery manifest is unavailable" in result.stderr
    assert str(tmp_path) not in result.stderr
    assert "Traceback" not in result.stderr


def test_validator_rejects_value_and_json_type_drift() -> None:
    document = cast(dict[str, object], json.loads(_run().stdout))
    validator = _validator()
    drifted = deepcopy(document)
    drifted["gate_satisfied"] = True
    with pytest.raises(RuntimeError, match="evidence drifted"):
        validator(drifted, version=__version__)
    typed = deepcopy(document)
    cast(dict[str, object], typed["metrics"])["tool_call_count"] = False
    with pytest.raises(RuntimeError, match="evidence drifted"):
        validator(typed, version=__version__)


def test_reviewed_terminal_cohort_reports_exact_rational_rate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module, evaluate = _evaluator()
    report = _admit(module, evaluate, _write(tmp_path, _ready_manifest()), monkeypatch)

    assert report["gate_satisfied"] is True
    assert report["completion_without_manual_recovery_rate_proven"] is True
    assert report["evidence_level"] == "reviewed-agent-tool-recovery-rate"
    metrics = cast(dict[str, object], report["metrics"])
    assert metrics == {
        "completed_after_manual_recovery_count": 1,
        "completed_without_manual_recovery_count": 1,
        "completion_without_manual_recovery_rate": {"denominator": 3, "numerator": 1},
        "manifest_sha256": metrics["manifest_sha256"],
        "manual_recovery_count": 1,
        "measurement_policy": "complete-reviewed-task-directed-agent-tool-calls/1",
        "not_completed_count": 1,
        "records_verified": True,
        "tool_call_count": 3,
        "unobserved_terminal_count": 0,
        "window_count": 1,
    }
    encoded = json.dumps(report, sort_keys=True)
    assert "org.example" not in encoded
    assert "project_describe" not in encoded
    assert "2026-08" not in encoded


def test_known_noncompletion_remains_in_rate_denominator(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _manifest()
    document["evaluation_windows"] = [_window([_call(1, outcome="not-completed")])]
    module, evaluate = _evaluator()

    report = _admit(module, evaluate, _write(tmp_path, document), monkeypatch)

    assert report["gate_satisfied"] is True
    assert cast(dict[str, object], report["metrics"])[
        "completion_without_manual_recovery_rate"
    ] == {"denominator": 1, "numerator": 0}


def test_unobserved_terminal_state_is_preserved_and_blocks_rate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _ready_manifest()
    _calls(document)[2] = _call(3, outcome="terminal-unobserved")
    module, evaluate = _evaluator()

    report = _admit(module, evaluate, _write(tmp_path, document), monkeypatch)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["reason_codes"] == ("agent-tool-terminal-cohort-incomplete",)
    metrics = cast(dict[str, object], report["metrics"])
    assert metrics["tool_call_count"] == 3
    assert metrics["unobserved_terminal_count"] == 1
    assert metrics["completion_without_manual_recovery_rate"] is None


def test_unreviewed_candidate_exposes_no_call_aggregates(tmp_path: Path) -> None:
    _, evaluate = _evaluator()

    report = evaluate(_write(tmp_path, _ready_manifest()))

    assert cast(dict[str, object], report["metrics"])["tool_call_count"] == 0
    assert (
        cast(dict[str, object], report["metrics"])["completion_without_manual_recovery_rate"]
        is None
    )


def test_mandatory_history_rejects_replacement_window(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = _ready_manifest()
    original_path = _write(tmp_path, original, "original.json")
    module, evaluate = _evaluator()
    parse = cast(_ParseManifest, module._parse_manifest)
    _, original_identities = parse(original_path)
    replacement = deepcopy(original)
    _calls(replacement)[0]["tool_name"] = "world_describe"
    replacement_path = _write(tmp_path, replacement, "replacement.json")
    monkeypatch.setattr(
        module,
        "_REVIEWED_MANIFEST_SHA256",
        hashlib.sha256(replacement_path.read_bytes()).hexdigest(),
    )
    monkeypatch.setattr(module, "_MANDATORY_WINDOW_PREFIX", original_identities)

    report = evaluate(replacement_path)

    assert report["gate_satisfied"] is False
    assert "historical-evaluation-window-missing" in cast(
        list[str], cast(dict[str, object], report["admission"])["reason_codes"]
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schema", "ludoweave.operations.agent-tool-recovery-rate/2"),
        ("source_project", "another-project"),
        ("measurement_policy", "successful-calls-only/1"),
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
        '"measurement_policy":"complete-reviewed-task-directed-agent-tool-calls/1",'
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


def test_manifest_rejects_parser_depth_exhaustion(tmp_path: Path) -> None:
    deeply_nested = tmp_path / "deeply-nested.json"
    deeply_nested.write_text("[" * 2_000 + "]" * 2_000, encoding="utf-8")
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="not valid JSON"):
        evaluate(deeply_nested)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("window_id", "window-1"),
        ("started_before", "2026-08-01T00:00:00Z"),
        ("observed_through", "2026-08-02T00:00:00Z"),
        ("census_sha256", "A" * 64),
        ("task_directed_session_census_complete_reviewed", False),
        ("eligibility_reviewed", 1),
        ("manual_recovery_definition_reviewed", None),
        ("privacy_and_consent_reviewed", False),
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


def test_window_rejects_noncanonical_evidence_urls_revision_drift_and_overlap(
    tmp_path: Path,
) -> None:
    for field, value in (
        ("census_url", "https://example.com/census.json"),
        (
            "review_url",
            _evidence_url("review", _digest("review", 1), revision="2" * 40),
        ),
    ):
        document = _ready_manifest()
        _first_window(document)[field] = value
        _assert_rejected(document, tmp_path)

    document = _ready_manifest()
    second = _window([], index=2)
    second["started_from"] = "2026-08-01T12:00:00Z"
    document["evaluation_windows"] = [_first_window(document), second]
    _assert_rejected(document, tmp_path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("call_id", "call-1"),
        ("session_id", "Session-1"),
        ("session_call_index", True),
        ("adapter_id", "adapter"),
        ("tool_name", "shell_execute"),
        ("service_protocol", "ludoweave.agent.service/2"),
        ("engine_sha", "A" * 40),
        ("service_contract_sha256", "g" * 64),
        ("started_at", "2026-08-02T00:00:00Z"),
        ("outcome", "passed"),
        ("eligible_call_reviewed", False),
        ("task_directed_context_reviewed", 1),
        ("manual_recovery_reviewed", None),
        ("outcome_reviewed", "true"),
        ("privacy_and_consent_reviewed", False),
        ("provenance_reviewed", False),
        ("validation_reviewed", 0),
    ],
)
def test_call_rejects_invalid_identity_registration_bounds_and_reviews(
    tmp_path: Path, field: str, value: object
) -> None:
    document = _ready_manifest()
    _calls(document)[0][field] = value
    _assert_rejected(document, tmp_path)


def test_call_rejects_noncanonical_contract_and_evidence_urls(tmp_path: Path) -> None:
    for field, value in (
        (
            "service_contract_url",
            f"{_PROJECT}/blob/main/src/ludoweave/agent/tools.py",
        ),
        ("call_evidence_url", "https://example.com/call.json"),
        (
            "result_evidence_url",
            _evidence_url("result", _digest("result", 1), revision="2" * 40),
        ),
    ):
        document = _ready_manifest()
        _calls(document)[0][field] = value
        _assert_rejected(document, tmp_path)


def test_outcome_evidence_shapes_are_exact(tmp_path: Path) -> None:
    mutations: tuple[tuple[int, str, object], ...] = (
        (0, "manual_recovery_occurred", True),
        (0, "outcome_code", "success"),
        (0, "result_evidence_url", None),
        (1, "manual_recovery_occurred", False),
        (1, "recovery_evidence_sha256", None),
        (2, "outcome_code", "unknown"),
        (2, "result_evidence_sha256", None),
    )
    for index, field, value in mutations:
        document = _ready_manifest()
        _calls(document)[index][field] = value
        _assert_rejected(document, tmp_path)


def test_failed_call_can_record_manual_recovery_without_becoming_completion(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _manifest()
    call = _call(1, outcome="not-completed")
    recovery_hash = _digest("recovery", 1)
    call["manual_recovery_occurred"] = True
    call["recovery_evidence_url"] = _evidence_url("recovery", recovery_hash)
    call["recovery_evidence_sha256"] = recovery_hash
    document["evaluation_windows"] = [_window([call])]
    module, evaluate = _evaluator()

    report = _admit(module, evaluate, _write(tmp_path, document), monkeypatch)

    metrics = cast(dict[str, object], report["metrics"])
    assert metrics["manual_recovery_count"] == 1
    assert metrics["not_completed_count"] == 1
    assert metrics["completed_after_manual_recovery_count"] == 0


def test_unobserved_reason_codes_are_exact(tmp_path: Path) -> None:
    for code in ("call-result-evidence-unavailable", "call-terminal-state-unobserved"):
        document = _manifest()
        call = _call(1, outcome="terminal-unobserved")
        call["outcome_code"] = code
        document["evaluation_windows"] = [_window([call])]
        _, evaluate = _evaluator()
        evaluate(_write(tmp_path, document))
    document = _manifest()
    call = _call(1, outcome="terminal-unobserved")
    call["outcome_code"] = "unknown"
    document["evaluation_windows"] = [_window([call])]
    _assert_rejected(document, tmp_path)


def test_session_call_indices_are_complete_and_sequential(tmp_path: Path) -> None:
    document = _ready_manifest()
    _calls(document)[1]["session_call_index"] = 3
    _assert_rejected(document, tmp_path)

    document = _manifest()
    document["evaluation_windows"] = [
        _window(
            [
                _call(1),
                _call(2, session_id="session-0002", session_call_index=1),
            ]
        )
    ]
    _, evaluate = _evaluator()
    evaluate(_write(tmp_path, document))


def test_calls_require_canonical_order_and_unique_evidence(tmp_path: Path) -> None:
    document = _ready_manifest()
    first, second = _calls(document)[:2]
    second["started_at"] = _timestamp(_BASE + timedelta(minutes=5))
    _assert_rejected(document, tmp_path)

    for field in ("call_evidence_url", "call_evidence_sha256"):
        document = _ready_manifest()
        first, second = _calls(document)[:2]
        second[field] = first[field]
        _assert_rejected(document, tmp_path)


def test_all_exact_product_tool_names_parse(tmp_path: Path) -> None:
    module, _ = _evaluator()
    assert tuple(cast(tuple[str, ...], module._TOOL_NAMES)) == AGENT_TOOL_NAMES
    for tool_name in AGENT_TOOL_NAMES:
        document = _manifest()
        call = _call(1)
        call["tool_name"] = tool_name
        document["evaluation_windows"] = [_window([call])]
        cast(_ParseManifest, module._parse_manifest)(
            _write(tmp_path, document, f"{tool_name}.json")
        )


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
    _calls(document)[0]["started_at"] = timestamp
    _assert_rejected(document, tmp_path)


def test_window_and_call_limits_are_enforced(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _manifest()
    document["evaluation_windows"] = [{}] * 13
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError, match="window limit"):
        evaluate(_write(tmp_path, document))

    document = _ready_manifest()
    _first_window(document)["calls"] = [_calls(document)[0]] * 2_049
    module, evaluate = _evaluator()
    monkeypatch.setattr(module, "_MAX_MANIFEST_BYTES", 10_000_000)
    with pytest.raises(RuntimeError, match="call limit"):
        evaluate(_write(tmp_path, document))
