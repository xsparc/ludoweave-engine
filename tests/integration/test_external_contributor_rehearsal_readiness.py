"""M27 installed external-contributor rehearsal admission evidence."""

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
_EXAMPLE = _ROOT / "examples" / "external_contributor_rehearsal_readiness.py"
_VALIDATOR = _ROOT / "scripts" / "external_contributor_rehearsal_evidence.py"
_REHEARSALS = _ROOT / "tests" / "fixtures" / "external_contributor_rehearsal.json"


class _Validate(Protocol):
    def __call__(self, document: dict[str, object], *, version: str) -> None: ...


class _Evaluate(Protocol):
    def __call__(self, rehearsals: Path) -> dict[str, object]: ...


def _load(path: Path, name: str) -> ModuleType:
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{name} could not be loaded")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validator() -> _Validate:
    module = _load(_VALIDATOR, "external_contributor_rehearsal_validator")
    return cast(_Validate, module.validate_external_contributor_rehearsal_evidence)


def _evaluator() -> tuple[ModuleType, _Evaluate]:
    module = _load(_EXAMPLE, "external_contributor_rehearsal_example")
    return module, cast(_Evaluate, module.evaluate)


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def _document() -> dict[str, object]:
    result = _run("--rehearsals", str(_REHEARSALS))
    assert result.returncode == 0, result.stderr
    return cast(dict[str, object], json.loads(result.stdout))


def _manifest() -> dict[str, object]:
    return cast(dict[str, object], json.loads(_REHEARSALS.read_text(encoding="utf-8")))


def _record(
    *,
    contributor: str = "external-dev",
    issue: int = 101,
    pull_request: int = 102,
    base_character: str = "1",
    head_character: str = "2",
    merge_character: str = "3",
    patch_character: str = "4",
    feedback_character: str = "5",
) -> dict[str, object]:
    return {
        "contributor_login": contributor,
        "contributor_type": "human",
        "independence_reviewed": True,
        "issue_url": f"https://github.com/xsparc/ludoweave-engine/issues/{issue}",
        "pull_request_url": (f"https://github.com/xsparc/ludoweave-engine/pull/{pull_request}"),
        "base_commit": base_character * 40,
        "head_commit": head_character * 40,
        "merge_commit": merge_character * 40,
        "patch_sha256": patch_character * 64,
        "feedback_sha256": feedback_character * 64,
        "task_scope": "documentation",
        "validation_steps": ["clean-setup", "focused-check", "complete-gate"],
        "outcome": "merged",
        "dco_valid": True,
        "private_maintainer_knowledge_used": False,
        "public_api_changed": False,
        "persistent_format_changed": False,
        "dependency_changed": False,
        "workflow_changed": False,
    }


def _identity(record: dict[str, object]) -> tuple[object, ...]:
    return (
        record["contributor_login"],
        record["contributor_type"],
        record["independence_reviewed"],
        record["issue_url"],
        record["pull_request_url"],
        record["base_commit"],
        record["head_commit"],
        record["merge_commit"],
        record["patch_sha256"],
        record["feedback_sha256"],
        record["task_scope"],
        tuple(cast(list[str], record["validation_steps"])),
        record["outcome"],
        record["dco_valid"],
        record["private_maintainer_knowledge_used"],
        record["public_api_changed"],
        record["persistent_format_changed"],
        record["dependency_changed"],
        record["workflow_changed"],
    )


def _write_manifest(tmp_path: Path, document: dict[str, object]) -> Path:
    rehearsals = tmp_path / "external_contributor_rehearsal.json"
    rehearsals.write_text(json.dumps(document), encoding="utf-8")
    return rehearsals


def test_installed_rehearsal_report_is_repeatable_sanitized_and_not_ready() -> None:
    first = _run()
    second = _run("--rehearsals", str(_REHEARSALS))

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["gate_satisfied"] is False
    assert document["first_external_contribution_proven"] is False
    assert document["status"] == "not-ready"
    admission = cast(dict[str, object], document["admission"])
    assert admission == {
        "documentation_without_private_knowledge_proven": False,
        "historical_rehearsals_preserved": True,
        "independent_contributor_rehearsal_present": False,
        "manifest_identity_reviewed": True,
        "minimum_merged_rehearsals": 1,
        "reason_codes": ["external-contributor-rehearsal-absent"],
    }
    for forbidden in (
        "external-dev",
        "issue_url",
        "pull_request_url",
        "base_commit",
        "head_commit",
        "merge_commit",
        "patch_sha256",
        "feedback_sha256",
        "credential",
        "secret",
        "token",
    ):
        assert forbidden not in first.stdout.casefold()
    assert str(_ROOT).casefold() not in first.stdout.casefold()


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("root", "gate_satisfied", 0),
        ("root", "first_external_contribution_proven", True),
        ("admission", "documentation_without_private_knowledge_proven", True),
        ("admission", "historical_rehearsals_preserved", False),
        ("admission", "reason_codes", []),
        ("rehearsals", "record_count", 1),
        ("rehearsals", "records_verified", False),
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

    with pytest.raises(RuntimeError, match="contributor rehearsal evidence drifted"):
        _validator()(tampered, version=__version__)


def test_gate_becomes_true_only_for_reviewed_complete_rehearsal(tmp_path: Path) -> None:
    record = _record()
    document = _manifest()
    document["rehearsal_records"] = [record]
    rehearsals = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_REHEARSAL_SHA256"] = hashlib.sha256(
        rehearsals.read_bytes()
    ).hexdigest()
    module.__dict__["_MANDATORY_REHEARSAL_PREFIX"] = (_identity(record),)

    report = evaluate(rehearsals)

    assert report["gate_satisfied"] is True
    assert report["first_external_contribution_proven"] is True
    assert report["status"] == "ready"
    assert report["evidence_level"] == "reviewed-external-contributor-rehearsal"
    admission = cast(dict[str, object], report["admission"])
    assert admission["documentation_without_private_knowledge_proven"] is True
    assert admission["reason_codes"] == ()


def test_reviewed_manifest_requires_complete_mandatory_history(tmp_path: Path) -> None:
    document = _manifest()
    document["rehearsal_records"] = [_record()]
    rehearsals = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_REHEARSAL_SHA256"] = hashlib.sha256(
        rehearsals.read_bytes()
    ).hexdigest()

    report = evaluate(rehearsals)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["manifest_identity_reviewed"] is True
    assert admission["historical_rehearsals_preserved"] is False
    assert admission["independent_contributor_rehearsal_present"] is True
    assert admission["reason_codes"] == ("historical-contributor-rehearsal-missing",)


def test_unreviewed_synthetic_rehearsal_cannot_satisfy_gate(tmp_path: Path) -> None:
    document = _manifest()
    document["rehearsal_records"] = [_record()]
    rehearsals = _write_manifest(tmp_path, document)
    _, evaluate = _evaluator()

    report = evaluate(rehearsals)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["independent_contributor_rehearsal_present"] is True
    assert admission["historical_rehearsals_preserved"] is True
    assert admission["reason_codes"] == ("contributor-rehearsal-identity-unreviewed",)


def test_reviewed_manifest_cannot_drop_mandatory_rehearsal(tmp_path: Path) -> None:
    document = _manifest()
    document["rehearsal_records"] = [_record()]
    rehearsals = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_REHEARSAL_SHA256"] = hashlib.sha256(
        rehearsals.read_bytes()
    ).hexdigest()
    prior = _record(
        contributor="prior-contributor",
        issue=91,
        pull_request=92,
        base_character="6",
        head_character="7",
        merge_character="8",
        patch_character="9",
        feedback_character="a",
    )
    module.__dict__["_MANDATORY_REHEARSAL_PREFIX"] = (_identity(prior),)

    report = evaluate(rehearsals)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["historical_rehearsals_preserved"] is False
    assert admission["reason_codes"] == ("historical-contributor-rehearsal-missing",)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("contributor_login", "xsparc", "external GitHub user"),
        ("contributor_login", "-external", "external GitHub user"),
        ("contributor_type", "bot", "human contributor"),
        ("independence_reviewed", False, "independence must be explicitly true"),
        (
            "issue_url",
            "https://github.com/other/project/issues/101",
            "public project issues record",
        ),
        (
            "issue_url",
            "https://github.com/xsparc/ludoweave-engine/issues/0101",
            "public project issues record",
        ),
        (
            "pull_request_url",
            "https://github.com/xsparc/ludoweave-engine/pull/102?diff=split",
            "public project pull record",
        ),
        ("base_commit", "0" * 39, "Git object identity"),
        ("head_commit", "F" * 40, "Git object identity"),
        ("patch_sha256", "0" * 63, "lowercase SHA-256"),
        ("feedback_sha256", "F" * 64, "lowercase SHA-256"),
        ("task_scope", "public-api", "good-first compatible"),
        ("validation_steps", ["clean-setup"], "validation steps are incomplete"),
        ("outcome", "open", "must have merged"),
        ("dco_valid", False, "DCO validation must be explicitly true"),
        (
            "private_maintainer_knowledge_used",
            True,
            "private maintainer knowledge must be explicitly false",
        ),
        ("public_api_changed", True, "public API change must be explicitly false"),
        (
            "persistent_format_changed",
            True,
            "persistent format change must be explicitly false",
        ),
        ("dependency_changed", True, "dependency change must be explicitly false"),
        ("workflow_changed", True, "workflow change must be explicitly false"),
    ],
)
def test_rehearsal_records_fail_closed(
    tmp_path: Path, field: str, value: object, message: str
) -> None:
    record = _record()
    record[field] = value
    document = _manifest()
    document["rehearsal_records"] = [record]
    rehearsals = _write_manifest(tmp_path, document)
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match=message):
        evaluate(rehearsals)


def test_rehearsal_revisions_must_be_distinct(tmp_path: Path) -> None:
    record = _record()
    record["merge_commit"] = record["head_commit"]
    document = _manifest()
    document["rehearsal_records"] = [record]
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="revisions must be distinct"):
        evaluate(_write_manifest(tmp_path, document))


def test_rehearsal_artifacts_must_be_distinct(tmp_path: Path) -> None:
    record = _record()
    record["feedback_sha256"] = record["patch_sha256"]
    document = _manifest()
    document["rehearsal_records"] = [record]
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="artifact identities must be distinct"):
        evaluate(_write_manifest(tmp_path, document))


@pytest.mark.parametrize(
    ("field", "message"),
    [
        ("issue_url", "repeats a public record"),
        ("pull_request_url", "repeats a public record"),
        ("head_commit", "repeats a revision identity"),
        ("merge_commit", "repeats a revision identity"),
        ("patch_sha256", "repeats an artifact identity"),
        ("feedback_sha256", "repeats an artifact identity"),
    ],
)
def test_rehearsal_records_reject_reused_identity(tmp_path: Path, field: str, message: str) -> None:
    first = _record()
    second = _record(
        contributor="another-dev",
        issue=201,
        pull_request=202,
        base_character="6",
        head_character="7",
        merge_character="8",
        patch_character="9",
        feedback_character="a",
    )
    second[field] = first[field]
    document = _manifest()
    document["rehearsal_records"] = [first, second]
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match=message):
        evaluate(_write_manifest(tmp_path, document))


@pytest.mark.parametrize(
    ("target_field", "source_field", "message"),
    [
        ("head_commit", "merge_commit", "repeats a revision identity"),
        ("merge_commit", "head_commit", "repeats a revision identity"),
        ("patch_sha256", "feedback_sha256", "repeats an artifact identity"),
        ("feedback_sha256", "patch_sha256", "repeats an artifact identity"),
    ],
)
def test_rehearsal_records_reject_cross_role_identity_reuse(
    tmp_path: Path, target_field: str, source_field: str, message: str
) -> None:
    first = _record()
    second = _record(
        contributor="another-dev",
        issue=201,
        pull_request=202,
        base_character="6",
        head_character="7",
        merge_character="8",
        patch_character="9",
        feedback_character="a",
    )
    second[target_field] = first[source_field]
    document = _manifest()
    document["rehearsal_records"] = [first, second]
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match=message):
        evaluate(_write_manifest(tmp_path, document))


def test_rehearsal_manifest_rejects_duplicate_json_fields(tmp_path: Path) -> None:
    rehearsals = tmp_path / "duplicate.json"
    rehearsals.write_text(
        '{"schema":"ludoweave.community.external-contributor-rehearsal/1",'
        '"schema":"ludoweave.community.external-contributor-rehearsal/1"}',
        encoding="utf-8",
    )
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="not valid JSON"):
        evaluate(rehearsals)


def test_manifest_read_and_record_count_are_bounded(tmp_path: Path) -> None:
    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * 65_537)
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError, match="exceeds its byte limit"):
        evaluate(oversized)

    document = _manifest()
    document["rehearsal_records"] = [
        _record(
            contributor=f"external-{index}",
            issue=1000 + index,
            pull_request=2000 + index,
            base_character=f"{index % 10}",
            head_character=f"{(index + 1) % 10}",
            merge_character=f"{(index + 2) % 10}",
            patch_character=f"{index % 10}",
            feedback_character=f"{(index + 1) % 10}",
        )
        for index in range(65)
    ]
    with pytest.raises(RuntimeError, match="record limit"):
        evaluate(_write_manifest(tmp_path, document))


def test_rehearsal_readiness_rejects_unknown_arguments() -> None:
    result = _run("--contact-contributor")

    assert result.returncode == 2
    assert "unrecognized arguments" in result.stderr


def test_explicit_rehearsal_symlink_is_rejected(tmp_path: Path) -> None:
    linked = tmp_path / "linked-rehearsals.json"
    try:
        linked.symlink_to(_REHEARSALS)
    except OSError:
        pytest.skip("symbolic-link creation is unavailable")

    result = _run("--rehearsals", str(linked))

    assert result.returncode == 1
    assert "contributor-rehearsal manifest must not be a symbolic link" in result.stderr
