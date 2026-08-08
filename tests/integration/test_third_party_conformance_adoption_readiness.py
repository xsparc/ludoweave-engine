"""M35 third-party conformance-adoption admission evidence."""

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
_EXAMPLE = _ROOT / "examples" / "third_party_conformance_adoption_readiness.py"
_VALIDATOR = _ROOT / "scripts" / "third_party_conformance_adoption_evidence.py"
_MANIFEST = _ROOT / "tests" / "fixtures" / "third_party_conformance_adoption.json"


class _Evaluate(Protocol):
    def __call__(self, manifest: Path) -> dict[str, object]: ...


class _Parse(Protocol):
    def __call__(self, manifest: Path) -> tuple[bytes, tuple[object, ...]]: ...


class _Validate(Protocol):
    def __call__(self, document: dict[str, object], *, version: str) -> None: ...


def _load(path: Path, name: str) -> ModuleType:
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{name} could not be loaded")
    module = module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(name, None)
    return module


def _evaluator() -> tuple[ModuleType, _Evaluate]:
    module = _load(_EXAMPLE, "third_party_conformance_example")
    return module, cast(_Evaluate, module.evaluate)


def _validator() -> _Validate:
    module = _load(_VALIDATOR, "third_party_conformance_validator")
    return cast(_Validate, module.validate_third_party_conformance_adoption_evidence)


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def _manifest() -> dict[str, object]:
    return cast(dict[str, object], json.loads(_MANIFEST.read_text(encoding="utf-8")))


def _record(
    *,
    sequence: int = 1,
    implementation: str = "org.example.renderer",
    kind: str = "render-device-adapter",
    outcome: str = "passed",
) -> dict[str, object]:
    profiles = {
        "agent-tool-adapter": (
            "ludoweave.agent-tool-conformance/1",
            "agent-tool-baseline/1",
            12,
        ),
        "render-device-adapter": (
            "ludoweave.render-device-conformance/1",
            "render-device-baseline/1",
            9,
        ),
        "render-device-plugin": (
            "ludoweave.render-device-conformance/1",
            "render-device-baseline/1",
            9,
        ),
        "world-store-adapter": (
            "ludoweave.world-store-conformance/1",
            "world-store-baseline/1",
            10,
        ),
    }
    protocol, profile, check_count = profiles[kind]
    revision = f"{sequence:x}"[-1] * 40
    repository = f"https://github.com/example/package-{sequence}"
    is_plugin = kind == "render-device-plugin"
    report_present = outcome != "not-executed"
    passed_check_count = check_count if outcome == "passed" else (check_count - 1)
    outcome_code = (
        "conformance-profile-passed" if outcome == "passed" else "conformance-profile-failed"
    )
    if outcome == "not-executed":
        passed_check_count = 0
        outcome_code = "conformance-run-not-started"
    return {
        "submission_id": f"submission-{sequence:04d}",
        "implementation_id": implementation,
        "implementation_kind": kind,
        "package_id": f"org.example.package-{sequence}",
        "package_version": "1.0.0",
        "repository_url": repository,
        "revision": revision,
        "relationship": "independent-external",
        "project_owned": False,
        "maintainer_authored": False,
        "license_spdx": "Apache-2.0",
        "installed_distribution": "public-wheel",
        "ludoweave_version": "0.1.0a1",
        "platform": "linux",
        "python_implementation": "CPython",
        "python_version": "3.12",
        "conformance_protocol": protocol,
        "conformance_profile": profile,
        "adapter_id": implementation,
        "check_count": check_count,
        "passed_check_count": passed_check_count,
        "outcome": outcome,
        "outcome_code": outcome_code,
        "package_artifact_url": (f"https://files.pythonhosted.org/packages/package-{sequence}.whl"),
        "package_sha256": f"{sequence + 1:x}"[-1] * 64,
        "ludoweave_wheel_url": "https://files.pythonhosted.org/ludoweave-0.1.0a1.whl",
        "ludoweave_wheel_sha256": "a" * 64,
        "conformance_report_url": (
            f"{repository}/blob/{revision}/evidence/conformance.json" if report_present else None
        ),
        "conformance_report_sha256": f"{sequence + 10:x}"[-1] * 64 if report_present else None,
        "plugin_manifest_url": (f"{repository}/blob/{revision}/plugin.json" if is_plugin else None),
        "plugin_manifest_sha256": "c" * 64 if is_plugin else None,
        "plugin_check_url": (
            f"{repository}/blob/{revision}/evidence/plugin-check.json" if is_plugin else None
        ),
        "plugin_check_sha256": "d" * 64 if is_plugin else None,
        "plugin_compatible": True if is_plugin else None,
        "review_url": (
            "https://github.com/xsparc/ludoweave-engine/commit/" + f"{sequence + 4:x}"[-1] * 40
        ),
        "review_sha256": f"{sequence + 5:x}"[-1] * 64,
        "authorship_reviewed": True,
        "independence_reviewed": True,
        "license_reviewed": True,
        "eligibility_reviewed": True,
        "outcome_reviewed": True,
        "provenance_reviewed": True,
        "validation_reviewed": True,
        "privacy_and_consent_reviewed": True,
    }


def _write(tmp_path: Path, document: dict[str, object]) -> Path:
    path = tmp_path / "third-party-conformance.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    return path


def _admit(
    module: ModuleType,
    evaluate: _Evaluate,
    path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> dict[str, object]:
    parse = cast(_Parse, module.__dict__["_parse_manifest"])
    _, identities = parse(path)
    monkeypatch.setitem(
        module.__dict__, "_REVIEWED_MANIFEST_SHA256", hashlib.sha256(path.read_bytes()).hexdigest()
    )
    monkeypatch.setitem(module.__dict__, "_MANDATORY_SUBMISSION_PREFIX", identities)
    return evaluate(path)


def _assert_rejected(document: dict[str, object], tmp_path: Path) -> None:
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError):
        evaluate(_write(tmp_path, document))


def test_empty_reviewed_manifest_is_exact_repeatable_sanitized_and_not_ready() -> None:
    first = _run()
    second = _run("--submissions", str(_MANIFEST))

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["gate_satisfied"] is False
    assert document["third_party_conformance_adoption_proven"] is False
    assert document["status"] == "not-ready"
    metrics = cast(dict[str, object], document["metrics"])
    assert metrics["passing_implementation_count"] == 0
    assert metrics["reviewed_submission_count"] == 0
    for forbidden in (
        "implementation_id",
        "package_id",
        "repository_url",
        "package_artifact_url",
        "review_url",
        "adapter_id",
        "credential",
        "secret",
        "token",
        str(_ROOT),
    ):
        assert forbidden.casefold() not in first.stdout.casefold()


def test_reviewed_passing_adapter_becomes_ready(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _manifest()
    document["submissions"] = [_record()]
    module, evaluate = _evaluator()

    report = _admit(module, evaluate, _write(tmp_path, document), monkeypatch)

    assert report["gate_satisfied"] is True
    assert report["third_party_conformance_adoption_proven"] is True
    metrics = cast(dict[str, object], report["metrics"])
    assert metrics["passing_implementation_count"] == 1
    assert metrics["passing_adapter_count"] == 1
    assert metrics["passing_plugin_adapter_count"] == 0
    assert metrics["passing_by_profile"] == {
        "agent-tool-baseline/1": 0,
        "render-device-baseline/1": 1,
        "world-store-baseline/1": 0,
    }


def test_reviewed_plugin_adapter_requires_both_conformance_and_manifest_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _manifest()
    document["submissions"] = [
        _record(kind="render-device-plugin", implementation="org.example.render-plugin")
    ]
    module, evaluate = _evaluator()

    report = _admit(module, evaluate, _write(tmp_path, document), monkeypatch)

    metrics = cast(dict[str, object], report["metrics"])
    assert report["gate_satisfied"] is True
    assert metrics["passing_adapter_count"] == 0
    assert metrics["passing_plugin_adapter_count"] == 1


def test_all_existing_profiles_are_counted_without_exposing_identities(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    records = [
        _record(
            sequence=1,
            kind="agent-tool-adapter",
            implementation="org.example.agent-adapter",
        ),
        _record(
            sequence=2,
            kind="render-device-adapter",
            implementation="org.example.render-adapter",
        ),
        _record(
            sequence=3,
            kind="world-store-adapter",
            implementation="org.example.world-adapter",
        ),
    ]
    document = _manifest()
    document["submissions"] = records
    module, evaluate = _evaluator()

    report = _admit(module, evaluate, _write(tmp_path, document), monkeypatch)

    metrics = cast(dict[str, object], report["metrics"])
    assert metrics["passing_implementation_count"] == 3
    assert metrics["passing_by_profile"] == {
        "agent-tool-baseline/1": 1,
        "render-device-baseline/1": 1,
        "world-store-baseline/1": 1,
    }
    encoded = json.dumps(report, sort_keys=True)
    for record in records:
        assert cast(str, record["implementation_id"]) not in encoded
        assert cast(str, record["repository_url"]) not in encoded


def test_failed_and_not_executed_submissions_are_preserved_but_not_counted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _manifest()
    document["submissions"] = [
        _record(sequence=1, outcome="failed"),
        _record(
            sequence=2,
            implementation="org.example.unexecuted",
            outcome="not-executed",
        ),
    ]
    module, evaluate = _evaluator()

    report = _admit(module, evaluate, _write(tmp_path, document), monkeypatch)

    assert report["gate_satisfied"] is False
    metrics = cast(dict[str, object], report["metrics"])
    assert metrics["reviewed_submission_count"] == 2
    assert metrics["passing_implementation_count"] == 0
    assert metrics["failed_submission_count"] == 1
    assert metrics["not_executed_submission_count"] == 1
    admission = cast(dict[str, object], report["admission"])
    assert admission["reason_codes"] == ("passing-third-party-implementation-absent",)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("relationship", "maintainer"),
        ("project_owned", True),
        ("maintainer_authored", True),
        ("installed_distribution", "source-checkout"),
        ("python_implementation", "PyPy"),
        ("python_version", "3.11"),
        ("platform", "android"),
        ("adapter_id", "org.example.someone-else"),
        ("check_count", 8),
        ("conformance_protocol", "ludoweave.render-device-conformance/2"),
        ("conformance_profile", "render-device-baseline/2"),
    ],
)
def test_ineligible_relationship_environment_and_profile_are_rejected(
    tmp_path: Path, field: str, value: object
) -> None:
    record = _record()
    record[field] = value
    document = _manifest()
    document["submissions"] = [record]

    _assert_rejected(document, tmp_path)


@pytest.mark.parametrize(
    "field",
    [
        "authorship_reviewed",
        "independence_reviewed",
        "license_reviewed",
        "eligibility_reviewed",
        "outcome_reviewed",
        "provenance_reviewed",
        "validation_reviewed",
        "privacy_and_consent_reviewed",
    ],
)
def test_every_manual_review_gate_is_mandatory(tmp_path: Path, field: str) -> None:
    record = _record()
    record[field] = False
    document = _manifest()
    document["submissions"] = [record]

    _assert_rejected(document, tmp_path)


@pytest.mark.parametrize(
    ("outcome", "field", "value"),
    [
        ("passed", "outcome_code", "conformance-profile-failed"),
        ("passed", "passed_check_count", 8),
        ("passed", "conformance_report_url", None),
        ("failed", "outcome_code", "conformance-profile-passed"),
        ("failed", "passed_check_count", 9),
        ("not-executed", "outcome_code", "conformance-profile-failed"),
        ("not-executed", "passed_check_count", 1),
    ],
)
def test_outcome_evidence_must_be_internally_consistent(
    tmp_path: Path, outcome: str, field: str, value: object
) -> None:
    record = _record(outcome=outcome)
    record[field] = value
    if field == "conformance_report_url" and value is None:
        record["conformance_report_sha256"] = None
    document = _manifest()
    document["submissions"] = [record]

    _assert_rejected(document, tmp_path)


def test_report_locator_and_hash_must_appear_together(tmp_path: Path) -> None:
    record = _record()
    record["conformance_report_sha256"] = None
    document = _manifest()
    document["submissions"] = [record]

    _assert_rejected(document, tmp_path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("plugin_manifest_url", "https://example.invalid/repo/commit/" + "1" * 40),
        ("plugin_manifest_sha256", "c" * 64),
        ("plugin_check_url", "https://example.invalid/repo/commit/" + "2" * 40),
        ("plugin_check_sha256", "d" * 64),
        ("plugin_compatible", True),
    ],
)
def test_adapter_only_record_cannot_claim_plugin_evidence(
    tmp_path: Path, field: str, value: object
) -> None:
    record = _record()
    record[field] = value
    document = _manifest()
    document["submissions"] = [record]

    _assert_rejected(document, tmp_path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("plugin_manifest_url", None),
        ("plugin_manifest_sha256", None),
        ("plugin_check_url", None),
        ("plugin_check_sha256", None),
        ("plugin_compatible", False),
    ],
)
def test_plugin_record_requires_complete_compatible_manifest_evidence(
    tmp_path: Path, field: str, value: object
) -> None:
    record = _record(kind="render-device-plugin")
    record[field] = value
    document = _manifest()
    document["submissions"] = [record]

    _assert_rejected(document, tmp_path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("repository_url", "http://example.invalid/org/package"),
        ("repository_url", "https://user@example.invalid/org/package"),
        ("repository_url", "https://127.0.0.1/org/package"),
        ("repository_url", "https://localhost/org/package"),
        ("repository_url", "https://packages.invalid/org/package"),
        ("repository_url", "https://example.com/org/package"),
        ("package_artifact_url", "https://example.invalid/pkg.whl?token=secret"),
        ("package_artifact_url", "https://files.pythonhosted.org/packages/pkg.tar.gz"),
        ("ludoweave_wheel_url", "https://files.pythonhosted.org/packages/pkg.zip"),
        ("ludoweave_wheel_url", "https://example.invalid:443/ludoweave.whl"),
        ("review_url", "https://github.com/xsparc/ludoweave-engine/pull/1"),
    ],
)
def test_public_immutable_locator_policy_is_enforced(
    tmp_path: Path, field: str, value: object
) -> None:
    record = _record()
    record[field] = value
    document = _manifest()
    document["submissions"] = [record]

    _assert_rejected(document, tmp_path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("submission_id", "submission-1"),
        ("implementation_id", "Not Safe"),
        ("implementation_kind", "audio-plugin"),
        ("package_id", "Package"),
        ("package_version", "1 version"),
        ("revision", "A" * 40),
        ("license_spdx", "NOASSERTION"),
        ("package_sha256", "A" * 64),
    ],
)
def test_identifiers_versions_license_and_hashes_are_strict(
    tmp_path: Path, field: str, value: object
) -> None:
    record = _record()
    record[field] = value
    document = _manifest()
    document["submissions"] = [record]

    _assert_rejected(document, tmp_path)


def test_duplicate_implementation_report_and_review_evidence_are_rejected(tmp_path: Path) -> None:
    first = _record(sequence=1, implementation="org.example.first")
    second = _record(sequence=2, implementation="org.example.second")
    document = _manifest()
    document["submissions"] = [first, second]

    document["submissions"] = [
        first,
        {
            **second,
            "implementation_id": first["implementation_id"],
            "adapter_id": first["adapter_id"],
        },
    ]
    _assert_rejected(document, tmp_path)
    document["submissions"] = [
        first,
        {**second, "conformance_report_url": first["conformance_report_url"]},
    ]
    _assert_rejected(document, tmp_path)
    document["submissions"] = [first, {**second, "review_sha256": first["review_sha256"]}]
    _assert_rejected(document, tmp_path)


def test_unknown_missing_and_noncanonical_order_records_are_rejected(tmp_path: Path) -> None:
    record = _record()
    record["unexpected"] = True
    document = _manifest()
    document["submissions"] = [record]
    _assert_rejected(document, tmp_path)

    record = _record()
    del record["license_reviewed"]
    document["submissions"] = [record]
    _assert_rejected(document, tmp_path)

    record = _record(sequence=2)
    document["submissions"] = [record]
    _assert_rejected(document, tmp_path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schema", "ludoweave.adoption.third-party-conformance/2"),
        ("source_project", "another-project"),
        ("measurement_policy", "successful-submissions-only/1"),
        ("submission_census_complete_reviewed", False),
        ("submissions", {}),
    ],
)
def test_manifest_contract_values_and_types_are_fixed(
    tmp_path: Path, field: str, value: object
) -> None:
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
        '"measurement_policy":"complete-reviewed-project-accepted-third-party-'
        'conformance-submissions/1","submission_census_complete_reviewed":true,'
        '"submissions":[]}',
        encoding="utf-8",
    )
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError, match="not valid JSON"):
        evaluate(duplicate)
    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * 262_145)
    with pytest.raises(RuntimeError, match="byte limit"):
        evaluate(oversized)
    nested = tmp_path / "nested.json"
    nested.write_text("[" * 17 + "]" * 17, encoding="utf-8")
    with pytest.raises(RuntimeError, match="nesting limit"):
        evaluate(nested)
    deeply_nested = tmp_path / "deeply-nested.json"
    deeply_nested.write_text("[" * 2_000 + "]" * 2_000, encoding="utf-8")
    with pytest.raises(RuntimeError, match="not valid JSON"):
        evaluate(deeply_nested)
    link = tmp_path / "manifest-link.json"
    try:
        link.symlink_to(_MANIFEST)
    except OSError:
        return
    with pytest.raises(RuntimeError, match="symbolic link"):
        evaluate(link)


def test_manifest_submission_limit_is_bounded(tmp_path: Path) -> None:
    document = _manifest()
    document["submissions"] = [{} for _ in range(65)]
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="submission limit"):
        evaluate(_write(tmp_path, document))


def test_unreviewed_or_history_replaced_manifest_suppresses_all_counts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = _manifest()
    record = _record()
    document["submissions"] = [record]
    path = _write(tmp_path, document)
    module, evaluate = _evaluator()

    unreviewed = evaluate(path)
    assert cast(dict[str, object], unreviewed["metrics"])["reviewed_submission_count"] == 0

    monkeypatch.setitem(
        module.__dict__, "_REVIEWED_MANIFEST_SHA256", hashlib.sha256(path.read_bytes()).hexdigest()
    )
    monkeypatch.setitem(module.__dict__, "_MANDATORY_SUBMISSION_PREFIX", (object(),))
    replaced = evaluate(path)
    assert replaced["gate_satisfied"] is False
    assert cast(dict[str, object], replaced["metrics"])["passing_implementation_count"] == 0
    assert (
        cast(dict[str, object], replaced["admission"])["historical_submissions_preserved"] is False
    )


def test_missing_manifest_error_is_path_free(tmp_path: Path) -> None:
    missing = tmp_path / "private" / "missing.json"
    result = _run("--submissions", str(missing))

    assert result.returncode == 1
    assert result.stdout == ""
    assert "conformance manifest is unavailable" in result.stderr
    assert str(tmp_path) not in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("root", "gate_satisfied", 0),
        ("root", "third_party_conformance_adoption_proven", True),
        ("admission", "manifest_identity_reviewed", False),
        ("admission", "reason_codes", []),
        ("metrics", "passing_implementation_count", 1),
        ("metrics", "records_verified", False),
    ],
)
def test_exact_validator_rejects_gate_behavior_and_json_type_drift(
    section: str, key: str, value: object
) -> None:
    document = cast(dict[str, object], json.loads(_run().stdout))
    tampered = deepcopy(document)
    if section == "root":
        tampered[key] = value
    else:
        cast(dict[str, object], tampered[section])[key] = value

    with pytest.raises(RuntimeError, match="evidence drifted"):
        _validator()(tampered, version=__version__)


def test_manifest_identity_is_exact_and_small() -> None:
    payload = _MANIFEST.read_bytes()

    assert len(payload) == 250
    assert hashlib.sha256(payload).hexdigest() == (
        "adee8c68b5d89923ee2682162eb24cd9542a4601b1ff6fb901709ebcc0066767"
    )
