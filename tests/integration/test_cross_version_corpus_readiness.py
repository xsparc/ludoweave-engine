"""M24 installed cross-version receipt-corpus admission evidence."""

import hashlib
import json
import shutil
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
_EXAMPLE = _ROOT / "examples" / "cross_version_corpus_readiness.py"
_VALIDATOR = _ROOT / "scripts" / "cross_version_corpus_evidence.py"
_CORPUS = _ROOT / "tests" / "fixtures" / "cross_version_receipt_corpus.json"


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
    module = _load(_VALIDATOR, "cross_version_corpus_validator")
    return cast(_Validate, module.validate_cross_version_corpus_evidence)


def _evaluator() -> tuple[ModuleType, _Evaluate]:
    module = _load(_EXAMPLE, "cross_version_corpus_example")
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


def test_installed_corpus_readiness_is_repeatable_sanitized_and_not_ready() -> None:
    first = _run()
    second = _run("--corpus", str(_CORPUS))

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["gate_satisfied"] is False
    assert document["cross_version_proven"] is False
    assert document["status"] == "not-ready"
    admission = cast(dict[str, object], document["admission"])
    assert admission["corpus_identity_reviewed"] is True
    assert admission["cross_version_execution"] is False
    assert admission["historical_entries_preserved"] is True
    assert admission["supported_release_evidence_complete"] is False
    corpus = cast(dict[str, object], document["corpus"])
    assert corpus["fixture_count"] == 3
    assert corpus["canonical_round_trip"] is True
    for forbidden in (
        "credential",
        "environment",
        "expected_world_hash",
        "provider",
        "secret",
        "timing",
        "token",
    ):
        assert forbidden not in first.stdout.casefold()
    assert str(_ROOT).casefold() not in first.stdout.casefold()


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("root", "gate_satisfied", 0),
        ("root", "cross_version_proven", True),
        ("admission", "corpus_identity_reviewed", False),
        ("admission", "cross_version_execution", True),
        ("admission", "historical_entries_preserved", False),
        ("admission", "reason_codes", []),
        ("corpus", "canonical_round_trip", False),
        ("corpus", "fixture_count", 2),
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

    with pytest.raises(RuntimeError, match="installed readiness evidence drifted"):
        _validator()(tampered, version=__version__)


def test_admission_becomes_true_only_for_different_reader_and_release_evidence(
    tmp_path: Path,
) -> None:
    corpus = tmp_path / "cross_version_receipt_corpus.json"
    shutil.copytree(_CORPUS.parent / "receipt_v1", tmp_path / "receipt_v1")
    document = cast(dict[str, object], json.loads(_CORPUS.read_text(encoding="utf-8")))
    document["supported_releases"] = [
        {
            "version": version,
            "tag": f"v{version}",
            "commit": character * 40,
            "artifact_sha256": character * 64,
        }
        for version, character in (("0.1.0a1", "1"), ("0.1.0a2", "2"))
    ]
    corpus.write_text(json.dumps(document), encoding="utf-8")
    module, evaluate = _evaluator()
    module.__dict__["__version__"] = "0.1.0a2"
    module.__dict__["_REVIEWED_CORPUS_SHA256"] = hashlib.sha256(corpus.read_bytes()).hexdigest()

    report = evaluate(corpus)

    assert report["gate_satisfied"] is True
    assert report["cross_version_proven"] is True
    assert report["status"] == "ready"
    assert report["evidence_level"] == "cross-version-supported-release-evidence"
    admission = cast(dict[str, object], report["admission"])
    assert admission["reason_codes"] == ()
    assert admission["corpus_identity_reviewed"] is True
    assert admission["historical_entries_preserved"] is True
    assert admission["reader_differs_from_source"] is True
    assert admission["supported_release_evidence_complete"] is True


def test_unreviewed_future_manifest_cannot_satisfy_gate(tmp_path: Path) -> None:
    corpus = tmp_path / "cross_version_receipt_corpus.json"
    shutil.copytree(_CORPUS.parent / "receipt_v1", tmp_path / "receipt_v1")
    document = cast(dict[str, object], json.loads(_CORPUS.read_text(encoding="utf-8")))
    document["supported_releases"] = [
        {
            "version": version,
            "tag": f"v{version}",
            "commit": character * 40,
            "artifact_sha256": character * 64,
        }
        for version, character in (("0.1.0a1", "1"), ("0.1.0a2", "2"))
    ]
    corpus.write_text(json.dumps(document), encoding="utf-8")
    module, evaluate = _evaluator()
    module.__dict__["__version__"] = "0.1.0a2"

    report = evaluate(corpus)

    assert report["gate_satisfied"] is False
    assert report["cross_version_proven"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["corpus_identity_reviewed"] is False
    assert admission["cross_version_execution"] is True
    assert admission["supported_release_evidence_complete"] is True
    assert admission["reason_codes"] == ("corpus-identity-unreviewed",)


def test_reviewed_future_manifest_cannot_drop_m21_history(tmp_path: Path) -> None:
    corpus = tmp_path / "cross_version_receipt_corpus.json"
    shutil.copytree(_CORPUS.parent / "receipt_v1", tmp_path / "replacement_v1")
    document = cast(dict[str, object], json.loads(_CORPUS.read_text(encoding="utf-8")))
    sources = cast(list[dict[str, object]], document["source_manifests"])
    sources[0]["directory"] = "replacement_v1"
    document["supported_releases"] = [
        {
            "version": version,
            "tag": f"v{version}",
            "commit": character * 40,
            "artifact_sha256": character * 64,
        }
        for version, character in (("0.1.0a1", "1"), ("0.1.0a2", "2"))
    ]
    corpus.write_text(json.dumps(document), encoding="utf-8")
    module, evaluate = _evaluator()
    module.__dict__["__version__"] = "0.1.0a2"
    module.__dict__["_REVIEWED_CORPUS_SHA256"] = hashlib.sha256(corpus.read_bytes()).hexdigest()

    report = evaluate(corpus)

    assert report["gate_satisfied"] is False
    assert report["cross_version_proven"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["corpus_identity_reviewed"] is True
    assert admission["historical_entries_preserved"] is False
    assert admission["cross_version_execution"] is True
    assert admission["supported_release_evidence_complete"] is True
    assert admission["reason_codes"] == ("historical-corpus-entry-missing",)


def test_corpus_tamper_fails_before_receipt_decoding(tmp_path: Path) -> None:
    corpus = tmp_path / "cross_version_receipt_corpus.json"
    shutil.copytree(_CORPUS.parent / "receipt_v1", tmp_path / "receipt_v1")
    shutil.copyfile(_CORPUS, corpus)
    (tmp_path / "receipt_v1" / "committed.json").write_text("{}", encoding="utf-8")
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="fixture identity does not match"):
        evaluate(corpus)


def test_corpus_rejects_unsafe_source_directory(tmp_path: Path) -> None:
    document = cast(dict[str, object], json.loads(_CORPUS.read_text(encoding="utf-8")))
    sources = cast(list[dict[str, object]], document["source_manifests"])
    sources[0]["directory"] = "../receipt_v1"
    corpus = tmp_path / "cross_version_receipt_corpus.json"
    corpus.write_text(json.dumps(document), encoding="utf-8")
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="safe basename"):
        evaluate(corpus)


def test_corpus_manifest_read_is_bounded(tmp_path: Path) -> None:
    corpus = tmp_path / "cross_version_receipt_corpus.json"
    corpus.write_bytes(b" " * 65_537)
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="exceeds its byte limit"):
        evaluate(corpus)


def test_corpus_source_manifest_count_is_bounded(tmp_path: Path) -> None:
    document = cast(dict[str, object], json.loads(_CORPUS.read_text(encoding="utf-8")))
    sources = cast(list[dict[str, object]], document["source_manifests"])
    document["source_manifests"] = sources * 17
    corpus = tmp_path / "cross_version_receipt_corpus.json"
    corpus.write_text(json.dumps(document), encoding="utf-8")
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="source-manifest limit"):
        evaluate(corpus)


def test_corpus_supported_release_count_is_bounded(tmp_path: Path) -> None:
    shutil.copytree(_CORPUS.parent / "receipt_v1", tmp_path / "receipt_v1")
    document = cast(dict[str, object], json.loads(_CORPUS.read_text(encoding="utf-8")))
    document["supported_releases"] = [
        {
            "version": f"0.1.{index}a1",
            "tag": f"v0.1.{index}a1",
            "commit": "1" * 40,
            "artifact_sha256": "2" * 64,
        }
        for index in range(33)
    ]
    corpus = tmp_path / "cross_version_receipt_corpus.json"
    corpus.write_text(json.dumps(document), encoding="utf-8")
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="supported-release limit"):
        evaluate(corpus)


def test_corpus_readiness_rejects_unknown_arguments() -> None:
    result = _run("--reinterpret-v1")

    assert result.returncode == 2
    assert "unrecognized arguments" in result.stderr
