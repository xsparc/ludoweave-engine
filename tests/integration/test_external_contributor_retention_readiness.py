"""M29 installed external-contributor retention readiness evidence."""

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
_EXAMPLE = _ROOT / "examples" / "external_contributor_retention_readiness.py"
_VALIDATOR = _ROOT / "scripts" / "external_contributor_retention_evidence.py"
_RETENTION = _ROOT / "tests" / "fixtures" / "external_contributor_retention.json"
_VALIDATION_STEPS = ["clean-setup", "focused-check", "complete-gate"]


class _Validate(Protocol):
    def __call__(self, document: dict[str, object], *, version: str) -> None: ...


class _Evaluate(Protocol):
    def __call__(self, retention: Path) -> dict[str, object]: ...


def _load(path: Path, name: str) -> ModuleType:
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{name} could not be loaded")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validator() -> _Validate:
    module = _load(_VALIDATOR, "external_contributor_retention_validator")
    return cast(_Validate, module.validate_external_contributor_retention_evidence)


def _evaluator() -> tuple[ModuleType, _Evaluate]:
    module = _load(_EXAMPLE, "external_contributor_retention_example")
    return module, cast(_Evaluate, module.evaluate)


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def _document() -> dict[str, object]:
    result = _run("--retention", str(_RETENTION))
    assert result.returncode == 0, result.stderr
    return cast(dict[str, object], json.loads(result.stdout))


def _manifest() -> dict[str, object]:
    return cast(dict[str, object], json.loads(_RETENTION.read_text(encoding="utf-8")))


def _contribution(
    *,
    issue: int,
    pull_request: int,
    base_character: str,
    head_character: str,
    merge_character: str,
    patch_character: str,
    review_character: str,
    merged_at: str,
    task_scope: str,
) -> dict[str, object]:
    return {
        "issue_url": f"https://github.com/xsparc/ludoweave-engine/issues/{issue}",
        "pull_request_url": f"https://github.com/xsparc/ludoweave-engine/pull/{pull_request}",
        "base_commit": base_character * 40,
        "head_commit": head_character * 40,
        "merge_commit": merge_character * 40,
        "patch_sha256": patch_character * 64,
        "review_sha256": review_character * 64,
        "task_scope": task_scope,
        "validation_steps": list(_VALIDATION_STEPS),
        "outcome": "merged",
        "dco_valid": True,
        "merged_at": merged_at,
        "provenance_reviewed": True,
        "validation_reviewed": True,
    }


def _record(
    *,
    contributor: str = "external-developer",
    first_issue: int = 101,
    first_pull_request: int = 102,
    return_issue: int = 201,
    return_pull_request: int = 202,
    first_characters: tuple[str, str, str, str, str] = ("1", "2", "3", "4", "5"),
    return_characters: tuple[str, str, str, str, str] = ("3", "6", "7", "8", "9"),
) -> dict[str, object]:
    return {
        "contributor_login": contributor,
        "contributor_type": "human",
        "relationship": "independent-external",
        "identity_reviewed": True,
        "independence_reviewed": True,
        "same_contributor_reviewed": True,
        "chronology_reviewed": True,
        "retention_reviewed": True,
        "first_contribution": _contribution(
            issue=first_issue,
            pull_request=first_pull_request,
            base_character=first_characters[0],
            head_character=first_characters[1],
            merge_character=first_characters[2],
            patch_character=first_characters[3],
            review_character=first_characters[4],
            merged_at="2026-01-01T00:00:00Z",
            task_scope="documentation",
        ),
        "return_contribution": _contribution(
            issue=return_issue,
            pull_request=return_pull_request,
            base_character=return_characters[0],
            head_character=return_characters[1],
            merge_character=return_characters[2],
            patch_character=return_characters[3],
            review_character=return_characters[4],
            merged_at="2026-02-01T00:00:00Z",
            task_scope="tests",
        ),
    }


def _contribution_identity(contribution: dict[str, object]) -> tuple[object, ...]:
    return (
        contribution["issue_url"],
        contribution["pull_request_url"],
        contribution["base_commit"],
        contribution["head_commit"],
        contribution["merge_commit"],
        contribution["patch_sha256"],
        contribution["review_sha256"],
        contribution["task_scope"],
        tuple(cast(list[str], contribution["validation_steps"])),
        contribution["outcome"],
        contribution["dco_valid"],
        contribution["merged_at"],
        contribution["provenance_reviewed"],
        contribution["validation_reviewed"],
    )


def _identity(record: dict[str, object]) -> tuple[object, ...]:
    return (
        record["contributor_login"],
        record["contributor_type"],
        record["relationship"],
        record["identity_reviewed"],
        record["independence_reviewed"],
        record["same_contributor_reviewed"],
        record["chronology_reviewed"],
        record["retention_reviewed"],
        _contribution_identity(cast(dict[str, object], record["first_contribution"])),
        _contribution_identity(cast(dict[str, object], record["return_contribution"])),
    )


def _write_manifest(tmp_path: Path, document: dict[str, object]) -> Path:
    retention = tmp_path / "external_contributor_retention.json"
    retention.write_text(json.dumps(document), encoding="utf-8")
    return retention


def test_installed_retention_report_is_repeatable_sanitized_and_not_ready() -> None:
    first = _run()
    second = _run("--retention", str(_RETENTION))

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["gate_satisfied"] is False
    assert document["contributor_retention_proven"] is False
    assert document["status"] == "not-ready"
    admission = cast(dict[str, object], document["admission"])
    assert admission == {
        "historical_retention_preserved": True,
        "manifest_identity_reviewed": True,
        "minimum_retained_contributors": 1,
        "reason_codes": ["retained-external-contributor-absent"],
        "retained_external_contributor_present": False,
    }
    for forbidden in (
        "contributor_login",
        "issue_url",
        "pull_request_url",
        "base_commit",
        "head_commit",
        "merge_commit",
        "patch_sha256",
        "review_sha256",
        "merged_at",
        "credential",
        "secret",
        "token",
        "star_count",
    ):
        assert forbidden not in first.stdout.casefold()
    assert str(_ROOT).casefold() not in first.stdout.casefold()


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("root", "gate_satisfied", 0),
        ("root", "contributor_retention_proven", True),
        ("admission", "manifest_identity_reviewed", False),
        ("admission", "historical_retention_preserved", False),
        ("admission", "reason_codes", []),
        ("retention", "retained_contributor_count", 1),
        ("retention", "records_verified", False),
    ],
)
def test_exact_validator_rejects_gate_behavior_and_type_drift(
    section: str, key: str, value: object
) -> None:
    tampered = deepcopy(_document())
    if section == "root":
        tampered[key] = value
    else:
        cast(dict[str, object], tampered[section])[key] = value

    with pytest.raises(RuntimeError, match="contributor-retention readiness evidence drifted"):
        _validator()(tampered, version=__version__)


def test_gate_becomes_true_only_for_reviewed_complete_return(tmp_path: Path) -> None:
    record = _record()
    document = _manifest()
    document["retention_records"] = [record]
    retention = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_RETENTION_SHA256"] = hashlib.sha256(
        retention.read_bytes()
    ).hexdigest()
    module.__dict__["_MANDATORY_RETENTION_PREFIX"] = (_identity(record),)

    report = evaluate(retention)

    assert report["gate_satisfied"] is True
    assert report["contributor_retention_proven"] is True
    assert report["status"] == "ready"
    assert report["evidence_level"] == "reviewed-external-contributor-retention"
    admission = cast(dict[str, object], report["admission"])
    assert admission["reason_codes"] == ()
    retention_report = cast(dict[str, object], report["retention"])
    assert retention_report["retained_contributor_count"] == 1
    assert retention_report["return_contribution_count"] == 1
    assert retention_report["task_scopes"] == ("documentation", "tests")


def test_reviewed_manifest_requires_complete_mandatory_history(tmp_path: Path) -> None:
    document = _manifest()
    document["retention_records"] = [_record()]
    retention = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_RETENTION_SHA256"] = hashlib.sha256(
        retention.read_bytes()
    ).hexdigest()

    report = evaluate(retention)

    admission = cast(dict[str, object], report["admission"])
    assert admission["manifest_identity_reviewed"] is True
    assert admission["historical_retention_preserved"] is False
    assert admission["retained_external_contributor_present"] is False
    assert admission["reason_codes"] == (
        "historical-contributor-retention-record-missing",
        "retained-external-contributor-absent",
    )
    retention_report = cast(dict[str, object], report["retention"])
    assert retention_report["retained_contributor_count"] == 0
    assert retention_report["task_scopes"] == ()


def test_unreviewed_synthetic_return_exposes_no_aggregates(tmp_path: Path) -> None:
    document = _manifest()
    document["retention_records"] = [_record()]
    _, evaluate = _evaluator()

    report = evaluate(_write_manifest(tmp_path, document))

    admission = cast(dict[str, object], report["admission"])
    assert admission["retained_external_contributor_present"] is False
    assert admission["reason_codes"] == (
        "contributor-retention-manifest-identity-unreviewed",
        "retained-external-contributor-absent",
    )
    retention_report = cast(dict[str, object], report["retention"])
    assert retention_report["retained_contributor_count"] == 0
    assert retention_report["return_contribution_count"] == 0
    assert retention_report["task_scopes"] == ()


@pytest.mark.parametrize("location", ["manifest", "record"])
def test_popularity_fields_are_not_retention_evidence(tmp_path: Path, location: str) -> None:
    record = _record()
    document = _manifest()
    document["retention_records"] = [record]
    if location == "manifest":
        document["star_count"] = 100
    else:
        record["star_count"] = 100
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="fields are incompatible"):
        evaluate(_write_manifest(tmp_path, document))


def test_reviewed_manifest_cannot_replace_mandatory_contributor(tmp_path: Path) -> None:
    replacement = _record(
        contributor="another-developer",
        first_issue=301,
        first_pull_request=302,
        return_issue=401,
        return_pull_request=402,
        first_characters=("a", "b", "c", "d", "e"),
        return_characters=("c", "f", "0", "1", "2"),
    )
    document = _manifest()
    document["retention_records"] = [replacement]
    retention = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_RETENTION_SHA256"] = hashlib.sha256(
        retention.read_bytes()
    ).hexdigest()
    module.__dict__["_MANDATORY_RETENTION_PREFIX"] = (_identity(_record()),)

    report = evaluate(retention)

    admission = cast(dict[str, object], report["admission"])
    assert admission["historical_retention_preserved"] is False
    assert admission["retained_external_contributor_present"] is False


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("contributor_type", "agent", "human contributor"),
        ("relationship", "maintainer", "independent and external"),
        ("identity_reviewed", False, "identity must be explicitly true"),
        ("independence_reviewed", False, "independence must be explicitly true"),
        ("same_contributor_reviewed", False, "same-contributor review must be explicitly true"),
        ("chronology_reviewed", False, "chronology must be explicitly true"),
        ("retention_reviewed", False, "retention review must be explicitly true"),
    ],
)
def test_retention_records_fail_closed(
    tmp_path: Path, field: str, value: object, message: str
) -> None:
    record = _record()
    record[field] = value
    document = _manifest()
    document["retention_records"] = [record]
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match=message):
        evaluate(_write_manifest(tmp_path, document))


@pytest.mark.parametrize(
    ("which", "field", "value", "message"),
    [
        ("first_contribution", "issue_url", "https://example.invalid/issues/1", "project issues"),
        (
            "first_contribution",
            "pull_request_url",
            "https://example.invalid/pull/1",
            "project pull",
        ),
        ("first_contribution", "head_commit", "x" * 40, "Git object identity"),
        ("first_contribution", "patch_sha256", "0" * 63, "lowercase SHA-256"),
        ("first_contribution", "task_scope", "ownership", "scope is incompatible"),
        ("first_contribution", "validation_steps", _VALIDATION_STEPS[:-1], "steps are incomplete"),
        ("first_contribution", "outcome", "open", "must have merged"),
        ("first_contribution", "dco_valid", False, "DCO validation must be explicitly true"),
        ("first_contribution", "merged_at", "2026-02-30T00:00:00Z", "canonical UTC"),
        (
            "first_contribution",
            "merged_at",
            "\uff12\uff10\uff12\uff16-02-01T00:00:00Z",
            "canonical UTC",
        ),
        ("first_contribution", "provenance_reviewed", False, "provenance must be explicitly true"),
        ("return_contribution", "validation_reviewed", False, "validation must be explicitly true"),
        ("return_contribution", "merged_at", "2025-01-01T00:00:00Z", "merge after"),
    ],
)
def test_contributions_fail_closed(
    tmp_path: Path, which: str, field: str, value: object, message: str
) -> None:
    record = _record()
    cast(dict[str, object], record[which])[field] = value
    document = _manifest()
    document["retention_records"] = [record]
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match=message):
        evaluate(_write_manifest(tmp_path, document))


@pytest.mark.parametrize(
    ("target", "source", "message"),
    [
        (("root", "contributor_login"), ("root", "contributor_login"), "repeats a contributor"),
        (
            ("first_contribution", "issue_url"),
            ("first_contribution", "issue_url"),
            "repeats an issue",
        ),
        (
            ("return_contribution", "pull_request_url"),
            ("return_contribution", "pull_request_url"),
            "repeats a pull request",
        ),
        (
            ("first_contribution", "head_commit"),
            ("return_contribution", "merge_commit"),
            "repeats a revision identity",
        ),
        (
            ("return_contribution", "review_sha256"),
            ("first_contribution", "patch_sha256"),
            "repeats an artifact identity",
        ),
    ],
)
def test_retention_records_reject_reused_identity(
    tmp_path: Path,
    target: tuple[str, str],
    source: tuple[str, str],
    message: str,
) -> None:
    first = _record()
    second = _record(
        contributor="another-developer",
        first_issue=301,
        first_pull_request=302,
        return_issue=401,
        return_pull_request=402,
        first_characters=("a", "b", "c", "d", "e"),
        return_characters=("c", "f", "0", "1", "2"),
    )

    def value(record: dict[str, object], location: tuple[str, str]) -> object:
        section, field = location
        if section == "root":
            return record[field]
        return cast(dict[str, object], record[section])[field]

    section, field = target
    if section == "root":
        second[field] = value(first, source)
    else:
        cast(dict[str, object], second[section])[field] = value(first, source)
    document = _manifest()
    document["retention_records"] = [first, second]
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match=message):
        evaluate(_write_manifest(tmp_path, document))


def test_contributor_identity_is_case_insensitive(tmp_path: Path) -> None:
    first = _record(contributor="External-Developer")
    second = _record(
        contributor="external-developer",
        first_issue=301,
        first_pull_request=302,
        return_issue=401,
        return_pull_request=402,
        first_characters=("a", "b", "c", "d", "e"),
        return_characters=("c", "f", "0", "1", "2"),
    )
    document = _manifest()
    document["retention_records"] = [first, second]
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="repeats a contributor"):
        evaluate(_write_manifest(tmp_path, document))


def test_retention_manifest_rejects_duplicate_json_fields(tmp_path: Path) -> None:
    retention = tmp_path / "duplicate.json"
    retention.write_text(
        '{"schema":"ludoweave.community.external-contributor-retention/1",'
        '"schema":"ludoweave.community.external-contributor-retention/1"}',
        encoding="utf-8",
    )
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="not valid JSON"):
        evaluate(retention)


def test_retention_manifest_rejects_excessive_json_nesting(tmp_path: Path) -> None:
    retention = tmp_path / "nested.json"
    retention.write_text("[" * 17 + "]" * 17, encoding="utf-8")
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="exceeds its nesting limit"):
        evaluate(retention)


def test_retention_manifest_accepts_json_nesting_limit(tmp_path: Path) -> None:
    retention = tmp_path / "nested.json"
    retention.write_text("[" * 16 + "]" * 16, encoding="utf-8")
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="must be an object"):
        evaluate(retention)


def test_retention_nesting_guard_ignores_json_string_syntax(tmp_path: Path) -> None:
    document = _manifest()
    document["source_project"] = '["\\\\"]' * 20
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="project identity is invalid"):
        evaluate(_write_manifest(tmp_path, document))


def test_retention_manifest_read_and_record_count_are_bounded(tmp_path: Path) -> None:
    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * 65_537)
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError, match="exceeds its byte limit"):
        evaluate(oversized)

    document = _manifest()
    document["retention_records"] = [_record() for _ in range(33)]
    with pytest.raises(RuntimeError, match="record limit"):
        evaluate(_write_manifest(tmp_path, document))


def test_retention_readiness_rejects_unknown_arguments() -> None:
    result = _run("--count-stars")

    assert result.returncode == 2
    assert "unrecognized arguments" in result.stderr


def test_explicit_retention_manifest_symlink_is_rejected(tmp_path: Path) -> None:
    linked = tmp_path / "linked-retention.json"
    try:
        linked.symlink_to(_RETENTION)
    except OSError:
        pytest.skip("symbolic-link creation is unavailable")

    result = _run("--retention", str(linked))

    assert result.returncode == 1
    assert "contributor-retention manifest must not be a symbolic link" in result.stderr
