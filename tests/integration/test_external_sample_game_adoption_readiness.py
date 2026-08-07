"""M28 installed external sample-game adoption readiness evidence."""

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
_EXAMPLE = _ROOT / "examples" / "external_sample_game_adoption_readiness.py"
_VALIDATOR = _ROOT / "scripts" / "external_sample_game_adoption_evidence.py"
_SAMPLES = _ROOT / "tests" / "fixtures" / "external_sample_game_adoption.json"
_CAPABILITIES = [
    "headless-fixed-tick",
    "typed-command-receipt",
    "verified-replay",
]


class _Validate(Protocol):
    def __call__(self, document: dict[str, object], *, version: str) -> None: ...


class _Evaluate(Protocol):
    def __call__(self, samples: Path) -> dict[str, object]: ...


def _load(path: Path, name: str) -> ModuleType:
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{name} could not be loaded")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validator() -> _Validate:
    module = _load(_VALIDATOR, "external_sample_game_adoption_validator")
    return cast(_Validate, module.validate_external_sample_game_adoption_evidence)


def _evaluator() -> tuple[ModuleType, _Evaluate]:
    module = _load(_EXAMPLE, "external_sample_game_adoption_example")
    return module, cast(_Evaluate, module.evaluate)


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def _document() -> dict[str, object]:
    result = _run("--samples", str(_SAMPLES))
    assert result.returncode == 0, result.stderr
    return cast(dict[str, object], json.loads(result.stdout))


def _manifest() -> dict[str, object]:
    return cast(dict[str, object], json.loads(_SAMPLES.read_text(encoding="utf-8")))


def _record(
    *,
    author: str = "external-developer",
    slug: str = "orbit-garden",
    repository: str = "https://example.invalid/orbit-garden",
    revision_character: str = "1",
    source_character: str = "2",
    execution_character: str = "3",
    review_character: str = "4",
) -> dict[str, object]:
    revision = revision_character * 40
    return {
        "external_author_id": author,
        "authorship_reviewed": True,
        "relationship": "independent-external",
        "game_slug": slug,
        "repository_url": repository,
        "revision": revision,
        "sample_scope": "2d-game",
        "engine_distribution": "installed-wheel",
        "ludoweave_version": "0.1.0a1",
        "capabilities": list(_CAPABILITIES),
        "outcome": "validated",
        "source_sha256": source_character * 64,
        "execution_sha256": execution_character * 64,
        "review_sha256": review_character * 64,
        "evidence_locator": f"{repository}/commit/{revision}",
        "license_spdx": "Apache-2.0",
        "license_reviewed": True,
        "project_owned": False,
        "maintainer_authored": False,
        "independence_reviewed": True,
        "provenance_reviewed": True,
        "outcome_reviewed": True,
    }


def _identity(record: dict[str, object]) -> tuple[object, ...]:
    return (
        record["external_author_id"],
        record["authorship_reviewed"],
        record["relationship"],
        record["game_slug"],
        record["repository_url"],
        record["revision"],
        record["sample_scope"],
        record["engine_distribution"],
        record["ludoweave_version"],
        tuple(cast(list[str], record["capabilities"])),
        record["outcome"],
        record["source_sha256"],
        record["execution_sha256"],
        record["review_sha256"],
        record["evidence_locator"],
        record["license_spdx"],
        record["license_reviewed"],
        record["project_owned"],
        record["maintainer_authored"],
        record["independence_reviewed"],
        record["provenance_reviewed"],
        record["outcome_reviewed"],
    )


def _write_manifest(tmp_path: Path, document: dict[str, object]) -> Path:
    samples = tmp_path / "external_sample_game_adoption.json"
    samples.write_text(json.dumps(document), encoding="utf-8")
    return samples


def test_installed_sample_game_report_is_repeatable_sanitized_and_not_ready() -> None:
    first = _run()
    second = _run("--samples", str(_SAMPLES))

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["gate_satisfied"] is False
    assert document["external_sample_game_adoption_proven"] is False
    assert document["status"] == "not-ready"
    admission = cast(dict[str, object], document["admission"])
    assert admission == {
        "external_sample_game_present": False,
        "historical_sample_games_preserved": True,
        "manifest_identity_reviewed": True,
        "minimum_external_sample_games": 1,
        "reason_codes": ["external-sample-game-absent"],
    }
    for forbidden in (
        "external_author_id",
        "repository_url",
        "revision",
        "source_sha256",
        "execution_sha256",
        "review_sha256",
        "evidence_locator",
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
        ("root", "external_sample_game_adoption_proven", True),
        ("admission", "manifest_identity_reviewed", False),
        ("admission", "historical_sample_games_preserved", False),
        ("admission", "reason_codes", []),
        ("sample_games", "game_count", 1),
        ("sample_games", "records_verified", False),
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

    with pytest.raises(RuntimeError, match="sample-game adoption readiness evidence drifted"):
        _validator()(tampered, version=__version__)


def test_gate_becomes_true_only_for_reviewed_complete_external_game(tmp_path: Path) -> None:
    record = _record()
    document = _manifest()
    document["sample_game_records"] = [record]
    samples = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_SAMPLE_GAME_SHA256"] = hashlib.sha256(
        samples.read_bytes()
    ).hexdigest()
    module.__dict__["_MANDATORY_SAMPLE_GAME_PREFIX"] = (_identity(record),)

    report = evaluate(samples)

    assert report["gate_satisfied"] is True
    assert report["external_sample_game_adoption_proven"] is True
    assert report["status"] == "ready"
    assert report["evidence_level"] == "reviewed-external-sample-game-adoption"
    admission = cast(dict[str, object], report["admission"])
    assert admission["reason_codes"] == ()
    games = cast(dict[str, object], report["sample_games"])
    assert games["game_count"] == 1
    assert games["distinct_authors"] == 1


def test_reviewed_manifest_requires_complete_mandatory_history(tmp_path: Path) -> None:
    document = _manifest()
    document["sample_game_records"] = [_record()]
    samples = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_SAMPLE_GAME_SHA256"] = hashlib.sha256(
        samples.read_bytes()
    ).hexdigest()

    report = evaluate(samples)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["manifest_identity_reviewed"] is True
    assert admission["historical_sample_games_preserved"] is False
    assert admission["external_sample_game_present"] is True
    assert admission["reason_codes"] == ("historical-sample-game-record-missing",)


def test_unreviewed_synthetic_game_cannot_satisfy_gate(tmp_path: Path) -> None:
    document = _manifest()
    document["sample_game_records"] = [_record()]
    samples = _write_manifest(tmp_path, document)
    _, evaluate = _evaluator()

    report = evaluate(samples)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["external_sample_game_present"] is True
    assert admission["historical_sample_games_preserved"] is True
    assert admission["reason_codes"] == ("sample-game-manifest-identity-unreviewed",)


def test_reviewed_manifest_cannot_drop_mandatory_game(tmp_path: Path) -> None:
    replacement = _record(
        author="another-developer",
        slug="another-game",
        repository="https://example.invalid/another-game",
        revision_character="5",
        source_character="6",
        execution_character="7",
        review_character="8",
    )
    document = _manifest()
    document["sample_game_records"] = [replacement]
    samples = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_SAMPLE_GAME_SHA256"] = hashlib.sha256(
        samples.read_bytes()
    ).hexdigest()
    module.__dict__["_MANDATORY_SAMPLE_GAME_PREFIX"] = (_identity(_record()),)

    report = evaluate(samples)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["historical_sample_games_preserved"] is False
    assert admission["reason_codes"] == ("historical-sample-game-record-missing",)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("authorship_reviewed", False, "authorship must be explicitly reviewed"),
        ("relationship", "project-owned", "independent and external"),
        ("repository_url", "http://example.invalid/game", "HTTPS locator"),
        ("repository_url", "https://user:secret@example.invalid/game", "HTTPS locator"),
        ("repository_url", "https://localhost/game", "HTTPS locator"),
        ("repository_url", "https://127.0.0.1/game", "HTTPS locator"),
        ("evidence_locator", "https://169.254.169.254/game", "HTTPS locator"),
        ("repository_url", "https://example.invalid\\game", "HTTPS locator"),
        ("repository_url", "https://exÃ¤mple.invalid/game", "HTTPS locator"),
        ("evidence_locator", "https://example.invalid/game?mutable=1", "HTTPS locator"),
        ("sample_scope", "3d-game", "scope is incompatible"),
        ("engine_distribution", "source-tree", "installed wheel"),
        ("capabilities", _CAPABILITIES[:-1], "capability coverage is incomplete"),
        ("outcome", "unverified", "outcome must be validated"),
        ("source_sha256", "0" * 63, "lowercase SHA-256"),
        ("execution_sha256", "2" * 64, "artifact identities must be distinct"),
        ("license_spdx", "NOASSERTION", "SPDX license is invalid"),
        ("license_reviewed", False, "license must be explicitly reviewed"),
        ("project_owned", True, "not external sample games"),
        ("maintainer_authored", True, "not external sample games"),
        ("independence_reviewed", False, "independence must be explicitly reviewed"),
        ("provenance_reviewed", False, "provenance must be explicitly reviewed"),
        ("outcome_reviewed", False, "outcome must be explicitly reviewed"),
    ],
)
def test_sample_game_records_fail_closed(
    tmp_path: Path, field: str, value: object, message: str
) -> None:
    record = _record()
    record[field] = value
    document = _manifest()
    document["sample_game_records"] = [record]
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match=message):
        evaluate(_write_manifest(tmp_path, document))


@pytest.mark.parametrize(
    ("field", "message"),
    [
        ("game_slug", "repeats a game slug"),
        ("repository_url", "repeats a repository"),
        ("revision", "repeats a revision identity"),
        ("source_sha256", "repeats an artifact identity"),
        ("evidence_locator", "repeats an evidence locator"),
    ],
)
def test_sample_games_reject_reused_identity(tmp_path: Path, field: str, message: str) -> None:
    first = _record()
    second = _record(
        author="another-developer",
        slug="another-game",
        repository="https://example.invalid/another-game",
        revision_character="5",
        source_character="6",
        execution_character="7",
        review_character="8",
    )
    second[field] = first[field]
    document = _manifest()
    document["sample_game_records"] = [first, second]
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match=message):
        evaluate(_write_manifest(tmp_path, document))


def test_sample_games_reject_cross_role_artifact_reuse(tmp_path: Path) -> None:
    first = _record()
    second = _record(
        author="another-developer",
        slug="another-game",
        repository="https://example.invalid/another-game",
        revision_character="5",
        source_character="6",
        execution_character="7",
        review_character="8",
    )
    second["review_sha256"] = first["execution_sha256"]
    document = _manifest()
    document["sample_game_records"] = [first, second]
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="repeats an artifact identity"):
        evaluate(_write_manifest(tmp_path, document))


def test_sample_game_manifest_rejects_duplicate_json_fields(tmp_path: Path) -> None:
    samples = tmp_path / "duplicate.json"
    samples.write_text(
        '{"schema":"ludoweave.adoption.external-sample-games/1",'
        '"schema":"ludoweave.adoption.external-sample-games/1"}',
        encoding="utf-8",
    )
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="not valid JSON"):
        evaluate(samples)


def test_sample_game_manifest_read_and_record_count_are_bounded(tmp_path: Path) -> None:
    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * 65_537)
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError, match="exceeds its byte limit"):
        evaluate(oversized)

    document = _manifest()
    document["sample_game_records"] = [
        _record(
            author=f"external-{index}",
            slug=f"game-{index}",
            repository=f"https://example.invalid/game-{index}",
            revision_character=f"{index % 10}",
            source_character=f"{index % 10}",
            execution_character=f"{(index + 1) % 10}",
            review_character=f"{(index + 2) % 10}",
        )
        for index in range(33)
    ]
    with pytest.raises(RuntimeError, match="record limit"):
        evaluate(_write_manifest(tmp_path, document))


def test_sample_game_readiness_rejects_unknown_arguments() -> None:
    result = _run("--claim-adoption")

    assert result.returncode == 2
    assert "unrecognized arguments" in result.stderr


def test_explicit_sample_game_manifest_symlink_is_rejected(tmp_path: Path) -> None:
    linked = tmp_path / "linked-samples.json"
    try:
        linked.symlink_to(_SAMPLES)
    except OSError:
        pytest.skip("symbolic-link creation is unavailable")

    result = _run("--samples", str(linked))

    assert result.returncode == 1
    assert "sample-game manifest must not be a symbolic link" in result.stderr
