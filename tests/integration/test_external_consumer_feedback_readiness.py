"""M25 installed external-consumer-feedback admission readiness evidence."""

import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

import pytest

from ludoweave import __version__

_ROOT = Path(__file__).parents[2]
_EXAMPLE = _ROOT / "examples" / "external_consumer_feedback_readiness.py"
_VALIDATOR = _ROOT / "scripts" / "external_consumer_feedback_evidence.py"
_CORPUS = _ROOT / "tests" / "fixtures" / "external_consumer_feedback.json"
_PROTOCOLS = [
    "ludoweave.command/1",
    "ludoweave.transaction/1",
    "ludoweave.receipt/1",
]


class _Validate(Protocol):
    def __call__(self, document: dict[str, object], *, version: str) -> None: ...


class _Evaluate(Protocol):
    def __call__(self, corpus: Path) -> dict[str, object]: ...


def _load(path: Path, name: str) -> ModuleType:
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{name} could not be loaded")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validator() -> _Validate:
    module = _load(_VALIDATOR, "external_consumer_feedback_validator")
    return cast(_Validate, module.validate_external_consumer_feedback_evidence)


def _evaluator() -> tuple[ModuleType, _Evaluate]:
    module = _load(_EXAMPLE, "external_consumer_feedback_example")
    return module, cast(_Evaluate, module.evaluate)


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def _document() -> dict[str, object]:
    result = _run("--corpus", str(_CORPUS))
    assert result.returncode == 0, result.stderr
    return cast(dict[str, object], json.loads(result.stdout))


def _manifest() -> dict[str, object]:
    return cast(dict[str, object], json.loads(_CORPUS.read_text(encoding="utf-8")))


def _record(
    consumer_id: str = "external.consumer",
    *,
    character: str = "1",
) -> dict[str, object]:
    return {
        "consumer_id": consumer_id,
        "consumer_repository": f"https://example.invalid/{consumer_id}",
        "consumer_revision": character * 40,
        "relationship": "independent",
        "evidence_kind": "public-command-receipt-integration",
        "ludoweave_version": "0.1.0a1",
        "protocols": list(_PROTOCOLS),
        "outcome": "compatible",
        "integration_sha256": character * 64,
        "feedback_sha256": character * 64,
        "evidence_locator": f"https://example.invalid/{consumer_id}/commit/{character * 40}",
    }


def _write_manifest(tmp_path: Path, document: dict[str, object]) -> Path:
    corpus = tmp_path / "external_consumer_feedback.json"
    corpus.write_text(json.dumps(document), encoding="utf-8")
    return corpus


def test_installed_feedback_readiness_is_repeatable_sanitized_and_not_ready() -> None:
    first = _run()
    second = _run("--corpus", str(_CORPUS))

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["gate_satisfied"] is False
    assert document["external_feedback_proven"] is False
    assert document["status"] == "not-ready"
    admission = cast(dict[str, object], document["admission"])
    assert admission == {
        "corpus_identity_reviewed": True,
        "historical_records_preserved": True,
        "independent_consumer_feedback": False,
        "minimum_independent_consumers": 1,
        "reason_codes": ["external-consumer-feedback-absent"],
    }
    for forbidden in (
        "consumer_repository",
        "consumer_revision",
        "credential",
        "evidence_locator",
        "feedback_sha256",
        "integration_sha256",
        "secret",
        "token",
    ):
        assert forbidden not in first.stdout.casefold()
    assert str(_ROOT).casefold() not in first.stdout.casefold()


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("root", "gate_satisfied", 0),
        ("root", "external_feedback_proven", True),
        ("admission", "corpus_identity_reviewed", False),
        ("admission", "historical_records_preserved", False),
        ("admission", "reason_codes", []),
        ("corpus", "feedback_count", 1),
        ("corpus", "records_verified", False),
    ],
)
def test_exact_validator_rejects_admission_behavior_and_type_drift(
    section: str, key: str, value: object
) -> None:
    tampered = deepcopy(_document())
    if section == "root":
        tampered[key] = value
    else:
        cast(dict[str, object], tampered[section])[key] = value

    with pytest.raises(RuntimeError, match="feedback readiness evidence drifted"):
        _validator()(tampered, version=__version__)


def test_gate_logic_becomes_true_only_for_reviewed_independent_feedback(
    tmp_path: Path,
) -> None:
    document = _manifest()
    document["feedback_records"] = [_record()]
    corpus = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_FEEDBACK_CORPUS_SHA256"] = hashlib.sha256(
        corpus.read_bytes()
    ).hexdigest()

    report = evaluate(corpus)

    assert report["gate_satisfied"] is True
    assert report["external_feedback_proven"] is True
    assert report["status"] == "ready"
    assert report["evidence_level"] == "reviewed-external-consumer-feedback"
    admission = cast(dict[str, object], report["admission"])
    assert admission["reason_codes"] == ()
    corpus_report = cast(dict[str, object], report["corpus"])
    assert corpus_report["distinct_consumers"] == 1
    assert corpus_report["feedback_count"] == 1


def test_unreviewed_synthetic_feedback_cannot_satisfy_gate(tmp_path: Path) -> None:
    document = _manifest()
    document["feedback_records"] = [_record()]
    corpus = _write_manifest(tmp_path, document)
    _, evaluate = _evaluator()

    report = evaluate(corpus)

    assert report["gate_satisfied"] is False
    assert report["external_feedback_proven"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["independent_consumer_feedback"] is True
    assert admission["reason_codes"] == ("feedback-corpus-identity-unreviewed",)


def test_reviewed_manifest_cannot_drop_mandatory_feedback_history(tmp_path: Path) -> None:
    replacement = _record("replacement.consumer", character="2")
    document = _manifest()
    document["feedback_records"] = [replacement]
    corpus = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_FEEDBACK_CORPUS_SHA256"] = hashlib.sha256(
        corpus.read_bytes()
    ).hexdigest()
    module.__dict__["_MANDATORY_FEEDBACK_PREFIX"] = (
        (
            "prior.consumer",
            "https://example.invalid/prior.consumer",
            "1" * 40,
            "independent",
            "public-command-receipt-integration",
            "0.1.0a1",
            tuple(_PROTOCOLS),
            "compatible",
            "1" * 64,
            "1" * 64,
            f"https://example.invalid/prior.consumer/commit/{'1' * 40}",
        ),
    )

    report = evaluate(corpus)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["corpus_identity_reviewed"] is True
    assert admission["historical_records_preserved"] is False
    assert admission["independent_consumer_feedback"] is True
    assert admission["reason_codes"] == ("historical-feedback-record-missing",)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("relationship", "project-owned", "must be independent"),
        ("evidence_kind", "project-sample", "evidence kind is incompatible"),
        ("outcome", "unknown", "outcome is invalid"),
        ("consumer_repository", "http://example.invalid/repo", "HTTPS locator"),
        (
            "consumer_repository",
            "https://user:secret@example.invalid/repo",
            "HTTPS locator",
        ),
        ("consumer_repository", "https://localhost/repo", "HTTPS locator"),
        ("consumer_repository", "https://127.0.0.1/repo", "HTTPS locator"),
        (
            "evidence_locator",
            "https://169.254.169.254/evidence",
            "HTTPS locator",
        ),
        ("consumer_repository", "https://example.invalid\\repo", "HTTPS locator"),
        ("consumer_repository", "https://exämple.invalid/repo", "HTTPS locator"),
        ("evidence_locator", "https://example.invalid/evidence?mutable=1", "HTTPS locator"),
        ("integration_sha256", "0" * 63, "lowercase SHA-256"),
        ("protocols", _PROTOCOLS[:-1], "protocol coverage is incomplete"),
    ],
)
def test_feedback_records_fail_closed(
    tmp_path: Path, field: str, value: object, message: str
) -> None:
    record = _record()
    record[field] = value
    document = _manifest()
    document["feedback_records"] = [record]
    corpus = _write_manifest(tmp_path, document)
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match=message):
        evaluate(corpus)


def test_feedback_corpus_rejects_duplicate_consumers(tmp_path: Path) -> None:
    document = _manifest()
    document["feedback_records"] = [_record(), _record(character="2")]
    corpus = _write_manifest(tmp_path, document)
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="repeats a consumer"):
        evaluate(corpus)


def test_feedback_manifest_read_and_record_count_are_bounded(tmp_path: Path) -> None:
    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * 65_537)
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError, match="exceeds its byte limit"):
        evaluate(oversized)

    document = _manifest()
    document["feedback_records"] = [
        _record(f"consumer.{index}", character=f"{index % 10}") for index in range(65)
    ]
    corpus = _write_manifest(tmp_path, document)
    with pytest.raises(RuntimeError, match="record limit"):
        evaluate(corpus)


def test_feedback_readiness_rejects_unknown_arguments() -> None:
    result = _run("--claim-adoption")

    assert result.returncode == 2
    assert "unrecognized arguments" in result.stderr


def test_explicit_feedback_manifest_symlink_is_rejected(tmp_path: Path) -> None:
    linked = tmp_path / "linked-feedback.json"
    try:
        linked.symlink_to(_CORPUS)
    except OSError:
        pytest.skip("symbolic-link creation is unavailable")

    result = _run("--corpus", str(linked))

    assert result.returncode == 1
    assert "feedback manifest must not be a symbolic link" in result.stderr
