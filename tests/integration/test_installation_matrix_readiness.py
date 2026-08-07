"""M30 installed clean-install matrix readiness evidence."""

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
_EXAMPLE = _ROOT / "examples" / "installation_matrix_readiness.py"
_VALIDATOR = _ROOT / "scripts" / "installation_matrix_evidence.py"
_MATRIX = _ROOT / "tests" / "fixtures" / "installation_matrix.json"
_ENVIRONMENTS = (
    "ubuntu-cpython-3.12",
    "ubuntu-cpython-3.13",
    "ubuntu-cpython-3.14",
    "macos-cpython-3.12",
    "macos-cpython-3.14",
    "windows-cpython-3.12",
    "windows-cpython-3.14",
)
_CONTRACTS = {
    "ubuntu-cpython-3.12": ("linux", "3.12.1"),
    "ubuntu-cpython-3.13": ("linux", "3.13.1"),
    "ubuntu-cpython-3.14": ("linux", "3.14.1"),
    "macos-cpython-3.12": ("macos", "3.12.1"),
    "macos-cpython-3.14": ("macos", "3.14.1"),
    "windows-cpython-3.12": ("windows", "3.12.1"),
    "windows-cpython-3.14": ("windows", "3.14.1"),
}
_CHECKS = ["version", "doctor", "hello-headless", "clockwork-arena-headless"]


class _Validate(Protocol):
    def __call__(self, document: dict[str, object], *, version: str) -> None: ...


class _Evaluate(Protocol):
    def __call__(self, matrix: Path) -> dict[str, object]: ...


def _load(path: Path, name: str) -> ModuleType:
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{name} could not be loaded")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validator() -> _Validate:
    module = _load(_VALIDATOR, "installation_matrix_validator")
    return cast(_Validate, module.validate_installation_matrix_evidence)


def _evaluator() -> tuple[ModuleType, _Evaluate]:
    module = _load(_EXAMPLE, "installation_matrix_example")
    return module, cast(_Evaluate, module.evaluate)


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def _manifest() -> dict[str, object]:
    return cast(dict[str, object], json.loads(_MATRIX.read_text(encoding="utf-8")))


def _record(environment: str, log_character: str) -> dict[str, object]:
    platform, python_version = _CONTRACTS[environment]
    release_tag = f"v{__version__}"
    release_url = f"https://github.com/xsparc/ludoweave-engine/releases/tag/{release_tag}"
    wheel_name = f"ludoweave-{__version__}-py3-none-any.whl"
    environment_number = _ENVIRONMENTS.index(environment) + 1
    return {
        "environment_id": environment,
        "python_version": python_version,
        "platform_system": platform,
        "release_version": __version__,
        "release_tag": release_tag,
        "release_url": release_url,
        "wheel_url": (
            "https://github.com/xsparc/ludoweave-engine/releases/download/"
            f"{release_tag}/{wheel_name}"
        ),
        "wheel_sha256": "a" * 64,
        "validation_url": (
            "https://github.com/xsparc/ludoweave-engine/actions/runs/"
            f"{1000 + environment_number}/job/{2000 + environment_number}"
        ),
        "installation_log_sha256": log_character * 64,
        "validated_at": "2026-08-07T10:00:00Z",
        "outcome": "passed",
        "isolated_environment": True,
        "installed_from_release_wheel": True,
        "dependencies_absent": True,
        "native_compiler_absent": True,
        "checks_passed": list(_CHECKS),
        "provenance_reviewed": True,
        "validation_reviewed": True,
    }


def _records() -> list[dict[str, object]]:
    return [
        _record(environment, character)
        for environment, character in zip(
            _ENVIRONMENTS, ("b", "c", "d", "e", "f", "0", "1"), strict=True
        )
    ]


def _identity(record: dict[str, object]) -> tuple[object, ...]:
    return (
        record["environment_id"],
        record["python_version"],
        record["platform_system"],
        record["release_version"],
        record["release_tag"],
        record["release_url"],
        record["wheel_url"],
        record["wheel_sha256"],
        record["validation_url"],
        record["installation_log_sha256"],
        record["validated_at"],
        record["outcome"],
        record["isolated_environment"],
        record["installed_from_release_wheel"],
        record["dependencies_absent"],
        record["native_compiler_absent"],
        tuple(cast(list[str], record["checks_passed"])),
        record["provenance_reviewed"],
        record["validation_reviewed"],
    )


def _write_manifest(tmp_path: Path, document: dict[str, object]) -> Path:
    matrix = tmp_path / "installation_matrix.json"
    matrix.write_text(json.dumps(document), encoding="utf-8")
    return matrix


def _document() -> dict[str, object]:
    result = _run("--matrix", str(_MATRIX))
    assert result.returncode == 0, result.stderr
    return cast(dict[str, object], json.loads(result.stdout))


def test_installed_matrix_report_is_repeatable_sanitized_and_not_ready() -> None:
    first = _run()
    second = _run("--matrix", str(_MATRIX))

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["gate_satisfied"] is False
    assert document["installation_matrix_proven"] is False
    assert document["status"] == "not-ready"
    admission = cast(dict[str, object], document["admission"])
    assert admission["reason_codes"] == ["installation-matrix-evidence-absent"]
    for forbidden in (
        "release_url",
        "wheel_url",
        "validation_url",
        "python_version",
        "platform_system",
        "installation_log_sha256",
        "validated_at",
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
        ("root", "installation_matrix_proven", True),
        ("admission", "manifest_identity_reviewed", False),
        ("admission", "reason_codes", []),
        ("installation", "successful_environment_count", 1),
        ("installation", "records_verified", False),
    ],
)
def test_exact_validator_rejects_behavior_and_type_drift(
    section: str, key: str, value: object
) -> None:
    tampered = deepcopy(_document())
    if section == "root":
        tampered[key] = value
    else:
        cast(dict[str, object], tampered[section])[key] = value

    with pytest.raises(RuntimeError, match="installation-matrix readiness evidence drifted"):
        _validator()(tampered, version=__version__)


def test_gate_becomes_true_only_for_reviewed_complete_matrix(tmp_path: Path) -> None:
    records = _records()
    document = _manifest()
    document["installation_records"] = records
    matrix = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_MATRIX_SHA256"] = hashlib.sha256(matrix.read_bytes()).hexdigest()
    module.__dict__["_MANDATORY_INSTALLATION_PREFIX"] = tuple(map(_identity, records))

    report = evaluate(matrix)

    assert report["gate_satisfied"] is True
    assert report["installation_matrix_proven"] is True
    assert report["status"] == "ready"
    assert report["evidence_level"] == "reviewed-installation-matrix"
    admission = cast(dict[str, object], report["admission"])
    assert admission["reason_codes"] == ()
    installation = cast(dict[str, object], report["installation"])
    assert installation["environments"] == _ENVIRONMENTS
    assert installation["successful_environment_count"] == 7
    assert installation["release_versions"] == (__version__,)


def test_reviewed_partial_matrix_remains_not_ready(tmp_path: Path) -> None:
    records = _records()[:-1]
    document = _manifest()
    document["installation_records"] = records
    matrix = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_MATRIX_SHA256"] = hashlib.sha256(matrix.read_bytes()).hexdigest()
    module.__dict__["_MANDATORY_INSTALLATION_PREFIX"] = tuple(map(_identity, records))

    report = evaluate(matrix)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["complete_environment_matrix"] is False
    assert admission["reason_codes"] == ("installation-matrix-incomplete",)
    installation = cast(dict[str, object], report["installation"])
    assert installation["successful_environment_count"] == 6


def test_unreviewed_synthetic_matrix_exposes_no_record_aggregates(tmp_path: Path) -> None:
    document = _manifest()
    document["installation_records"] = _records()
    _, evaluate = _evaluator()

    report = evaluate(_write_manifest(tmp_path, document))

    admission = cast(dict[str, object], report["admission"])
    assert admission["manifest_identity_reviewed"] is False
    assert admission["complete_environment_matrix"] is False
    assert "installation-matrix-manifest-identity-unreviewed" in cast(
        tuple[str, ...], admission["reason_codes"]
    )
    installation = cast(dict[str, object], report["installation"])
    assert installation["environments"] == ()
    assert installation["release_versions"] == ()
    assert installation["successful_environment_count"] == 0


def test_reviewed_manifest_requires_complete_mandatory_history(tmp_path: Path) -> None:
    records = _records()
    document = _manifest()
    document["installation_records"] = records
    matrix = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_MATRIX_SHA256"] = hashlib.sha256(matrix.read_bytes()).hexdigest()

    report = evaluate(matrix)

    admission = cast(dict[str, object], report["admission"])
    assert admission["manifest_identity_reviewed"] is True
    assert admission["historical_matrix_preserved"] is False
    assert "historical-installation-matrix-record-missing" in cast(
        tuple[str, ...], admission["reason_codes"]
    )
    installation = cast(dict[str, object], report["installation"])
    assert installation["successful_environment_count"] == 0


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("environment_id", "freebsd-cpython-3.12", "environment is unsupported"),
        ("platform_system", "windows", "platform does not match"),
        ("python_version", "3.13.1", "Python version does not match"),
        ("python_version", "3.12.01", "Python version is invalid"),
        ("release_version", "9.9.9", "release version does not match"),
        ("release_tag", "latest", "release tag is incompatible"),
        ("release_url", "https://example.com/release", "release URL is incompatible"),
        ("wheel_url", "https://example.com/wheel", "wheel URL is incompatible"),
        ("wheel_sha256", "A" * 64, "wheel sha256 is invalid"),
        ("validation_url", "https://example.com/run", "validation URL is incompatible"),
        ("installation_log_sha256", "b" * 63, "installation log sha256 is invalid"),
        ("validated_at", "2026-08-07", "validation timestamp is invalid"),
        ("validated_at", "2026-13-07T10:00:00Z", "validation timestamp is invalid"),
        ("validated_at", "2026-02-31T10:00:00Z", "validation timestamp is invalid"),
        ("outcome", "failed", "outcome must be passed"),
        ("isolated_environment", False, "isolated environment review must be true"),
        ("installed_from_release_wheel", False, "release-wheel installation review must be true"),
        ("dependencies_absent", False, "dependency-free installation review must be true"),
        ("native_compiler_absent", False, "native-compiler absence review must be true"),
        ("checks_passed", _CHECKS[:-1], "checks are incomplete"),
        ("provenance_reviewed", False, "provenance review must be true"),
        ("validation_reviewed", False, "validation review must be true"),
    ],
)
def test_installation_record_rejects_invalid_fields(
    tmp_path: Path, field: str, value: object, message: str
) -> None:
    document = _manifest()
    record = _record(_ENVIRONMENTS[0], "b")
    record[field] = value
    document["installation_records"] = [record]
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match=message):
        evaluate(_write_manifest(tmp_path, document))


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("schema", "ludoweave.community.installation-matrix/2", "schema is incompatible"),
        ("source_project", "other", "project identity is invalid"),
        ("required_environments", list(reversed(_ENVIRONMENTS)), "environments are incompatible"),
        ("required_checks", list(reversed(_CHECKS)), "checks are incompatible"),
    ],
)
def test_manifest_rejects_incompatible_contract_fields(
    tmp_path: Path, field: str, value: object, message: str
) -> None:
    document = _manifest()
    document[field] = value
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match=message):
        evaluate(_write_manifest(tmp_path, document))


def test_manifest_rejects_unknown_root_and_record_fields(tmp_path: Path) -> None:
    document = _manifest()
    document["star_count"] = 1
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError, match="manifest fields are incompatible"):
        evaluate(_write_manifest(tmp_path, document))

    document = _manifest()
    record = _record(_ENVIRONMENTS[0], "b")
    record["runner_path"] = "C:/runner"
    document["installation_records"] = [record]
    with pytest.raises(RuntimeError, match="record fields are incompatible"):
        evaluate(_write_manifest(tmp_path, document))


def test_manifest_rejects_duplicate_environment_log_and_artifact_drift(tmp_path: Path) -> None:
    _, evaluate = _evaluator()
    document = _manifest()
    document["installation_records"] = [
        _record(_ENVIRONMENTS[0], "b"),
        _record(_ENVIRONMENTS[0], "c"),
    ]
    with pytest.raises(RuntimeError, match="repeats an environment"):
        evaluate(_write_manifest(tmp_path, document))

    first = _record(_ENVIRONMENTS[0], "b")
    second = _record(_ENVIRONMENTS[1], "c")
    second["validation_url"] = first["validation_url"]
    document["installation_records"] = [first, second]
    with pytest.raises(RuntimeError, match="repeats a validation URL"):
        evaluate(_write_manifest(tmp_path, document))

    document["installation_records"] = [
        _record(_ENVIRONMENTS[0], "b"),
        _record(_ENVIRONMENTS[1], "b"),
    ]
    with pytest.raises(RuntimeError, match="repeats an installation log"):
        evaluate(_write_manifest(tmp_path, document))

    second = _record(_ENVIRONMENTS[1], "c")
    second["wheel_sha256"] = "f" * 64
    document["installation_records"] = [_record(_ENVIRONMENTS[0], "b"), second]
    with pytest.raises(RuntimeError, match="share one release wheel"):
        evaluate(_write_manifest(tmp_path, document))


def test_manifest_requires_canonical_environment_order(tmp_path: Path) -> None:
    document = _manifest()
    document["installation_records"] = [
        _record(_ENVIRONMENTS[1], "b"),
        _record(_ENVIRONMENTS[0], "c"),
    ]
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="required environment order"):
        evaluate(_write_manifest(tmp_path, document))


def test_manifest_rejects_duplicate_json_fields(tmp_path: Path) -> None:
    matrix = tmp_path / "duplicate.json"
    matrix.write_text(
        '{"schema":"ludoweave.community.installation-matrix/1",'
        '"schema":"ludoweave.community.installation-matrix/1"}',
        encoding="utf-8",
    )
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match="not valid JSON"):
        evaluate(matrix)


def test_manifest_enforces_nesting_limit_and_ignores_string_syntax(tmp_path: Path) -> None:
    matrix = tmp_path / "nested.json"
    matrix.write_text("[" * 17 + "]" * 17, encoding="utf-8")
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError, match="exceeds its nesting limit"):
        evaluate(matrix)

    matrix.write_text("[" * 16 + "]" * 16, encoding="utf-8")
    with pytest.raises(RuntimeError, match="must be an object"):
        evaluate(matrix)

    document = _manifest()
    document["source_project"] = '["\\\\"]' * 20
    with pytest.raises(RuntimeError, match="project identity is invalid"):
        evaluate(_write_manifest(tmp_path, document))


def test_manifest_read_and_record_count_are_bounded(tmp_path: Path) -> None:
    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * 65_537)
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError, match="exceeds its byte limit"):
        evaluate(oversized)

    document = _manifest()
    document["installation_records"] = [_record(_ENVIRONMENTS[0], "b") for _ in range(17)]
    with pytest.raises(RuntimeError, match="record limit"):
        evaluate(_write_manifest(tmp_path, document))


def test_readiness_rejects_unknown_arguments() -> None:
    result = _run("--download-latest")

    assert result.returncode == 2
    assert "unrecognized arguments" in result.stderr


def test_explicit_matrix_symlink_is_rejected(tmp_path: Path) -> None:
    linked = tmp_path / "linked-matrix.json"
    try:
        linked.symlink_to(_MATRIX)
    except OSError:
        pytest.skip("symbolic-link creation is unavailable")

    result = _run("--matrix", str(linked))

    assert result.returncode == 1
    assert "installation-matrix manifest must not be a symbolic link" in result.stderr
