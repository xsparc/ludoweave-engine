"""M26 installed supported-release-channel admission readiness evidence."""

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
_EXAMPLE = _ROOT / "examples" / "supported_release_channel_readiness.py"
_VALIDATOR = _ROOT / "scripts" / "supported_release_channel_evidence.py"
_CHANNEL = _ROOT / "tests" / "fixtures" / "supported_release_channel.json"


class _Validate(Protocol):
    def __call__(self, document: dict[str, object], *, version: str) -> None: ...


class _Evaluate(Protocol):
    def __call__(self, channel: Path) -> dict[str, object]: ...


def _load(path: Path, name: str) -> ModuleType:
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{name} could not be loaded")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validator() -> _Validate:
    module = _load(_VALIDATOR, "supported_release_channel_validator")
    return cast(_Validate, module.validate_supported_release_channel_evidence)


def _evaluator() -> tuple[ModuleType, _Evaluate]:
    module = _load(_EXAMPLE, "supported_release_channel_example")
    return module, cast(_Evaluate, module.evaluate)


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def _document() -> dict[str, object]:
    result = _run("--channel", str(_CHANNEL))
    assert result.returncode == 0, result.stderr
    return cast(dict[str, object], json.loads(result.stdout))


def _manifest() -> dict[str, object]:
    return cast(dict[str, object], json.loads(_CHANNEL.read_text(encoding="utf-8")))


def _record(
    version: str,
    *,
    character: str,
) -> dict[str, object]:
    return {
        "version": version,
        "tag": f"v{version}",
        "commit": character * 40,
        "release_url": (f"https://github.com/xsparc/ludoweave-engine/releases/tag/v{version}"),
        "artifact_sha256": character * 64,
        "release_notes_sha256": character * 64,
        "publication_channels": ["github-release"],
        "support_status": "supported",
        "yanked": False,
        "draft": False,
        "prerelease": False,
    }


def _write_manifest(tmp_path: Path, document: dict[str, object]) -> Path:
    channel = tmp_path / "supported_release_channel.json"
    channel.write_text(json.dumps(document), encoding="utf-8")
    return channel


def _two_feature_releases() -> list[dict[str, object]]:
    return [_record("1.0.0", character="1"), _record("1.1.0", character="2")]


def test_installed_release_channel_is_repeatable_sanitized_and_not_ready() -> None:
    first = _run()
    second = _run("--channel", str(_CHANNEL))

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = cast(dict[str, object], json.loads(first.stdout))
    _validator()(document, version=__version__)
    assert document["gate_satisfied"] is False
    assert document["supported_deprecation_release_channel_proven"] is False
    assert document["status"] == "not-ready"
    admission = cast(dict[str, object], document["admission"])
    assert admission == {
        "channel_identity_reviewed": True,
        "deprecation_window_feature_releases": 1,
        "historical_releases_preserved": True,
        "minimum_supported_feature_releases": 2,
        "reason_codes": ["supported-feature-release-channel-absent"],
        "supported_feature_release_channel": False,
    }
    for forbidden in (
        "artifact_sha256",
        "commit",
        "credential",
        "release_notes_sha256",
        "release_url",
        "secret",
        "token",
    ):
        assert forbidden not in first.stdout.casefold()
    assert str(_ROOT).casefold() not in first.stdout.casefold()


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("root", "gate_satisfied", 0),
        ("root", "supported_deprecation_release_channel_proven", True),
        ("admission", "channel_identity_reviewed", False),
        ("admission", "historical_releases_preserved", False),
        ("admission", "reason_codes", []),
        ("channel", "feature_release_count", 1),
        ("channel", "records_verified", False),
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

    with pytest.raises(RuntimeError, match="release channel readiness evidence drifted"):
        _validator()(tampered, version=__version__)


def test_gate_logic_becomes_true_only_for_reviewed_supported_feature_channel(
    tmp_path: Path,
) -> None:
    document = _manifest()
    document["release_records"] = _two_feature_releases()
    channel = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_RELEASE_CHANNEL_SHA256"] = hashlib.sha256(
        channel.read_bytes()
    ).hexdigest()

    report = evaluate(channel)

    assert report["gate_satisfied"] is True
    assert report["supported_deprecation_release_channel_proven"] is True
    assert report["status"] == "ready"
    assert report["evidence_level"] == "reviewed-supported-release-channel"
    admission = cast(dict[str, object], report["admission"])
    assert admission["reason_codes"] == ()
    channel_report = cast(dict[str, object], report["channel"])
    assert channel_report["distinct_feature_lines"] == 2
    assert channel_report["feature_release_count"] == 2
    assert channel_report["versions"] == ("1.0.0", "1.1.0")


def test_two_patch_releases_do_not_establish_two_feature_lines(tmp_path: Path) -> None:
    document = _manifest()
    document["release_records"] = [
        _record("1.0.0", character="1"),
        _record("1.0.1", character="2"),
    ]
    channel = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_RELEASE_CHANNEL_SHA256"] = hashlib.sha256(
        channel.read_bytes()
    ).hexdigest()

    report = evaluate(channel)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["channel_identity_reviewed"] is True
    assert admission["supported_feature_release_channel"] is False
    assert admission["reason_codes"] == ("supported-feature-release-channel-absent",)


def test_unreviewed_synthetic_releases_cannot_satisfy_gate(tmp_path: Path) -> None:
    document = _manifest()
    document["release_records"] = _two_feature_releases()
    channel = _write_manifest(tmp_path, document)
    _, evaluate = _evaluator()

    report = evaluate(channel)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["supported_feature_release_channel"] is True
    assert admission["reason_codes"] == ("release-channel-identity-unreviewed",)


def test_reviewed_manifest_cannot_drop_mandatory_release_history(tmp_path: Path) -> None:
    document = _manifest()
    document["release_records"] = _two_feature_releases()
    channel = _write_manifest(tmp_path, document)
    module, evaluate = _evaluator()
    module.__dict__["_REVIEWED_RELEASE_CHANNEL_SHA256"] = hashlib.sha256(
        channel.read_bytes()
    ).hexdigest()
    prior = _record("0.9.0", character="9")
    module.__dict__["_MANDATORY_RELEASE_PREFIX"] = (
        (
            prior["version"],
            prior["tag"],
            prior["commit"],
            prior["release_url"],
            prior["artifact_sha256"],
            prior["release_notes_sha256"],
            tuple(cast(list[str], prior["publication_channels"])),
            prior["support_status"],
            prior["yanked"],
            prior["draft"],
            prior["prerelease"],
        ),
    )

    report = evaluate(channel)

    assert report["gate_satisfied"] is False
    admission = cast(dict[str, object], report["admission"])
    assert admission["channel_identity_reviewed"] is True
    assert admission["historical_releases_preserved"] is False
    assert admission["supported_feature_release_channel"] is True
    assert admission["reason_codes"] == ("historical-release-record-missing",)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("version", "1.0.0a1", "final MAJOR.MINOR.PATCH"),
        ("tag", "v1.0.1", "exactly match"),
        ("commit", "0" * 39, "Git object identity"),
        ("release_url", "http://example.invalid/releases/v1.0.0", "HTTPS locator"),
        ("release_url", "https://127.0.0.1/releases/v1.0.0", "HTTPS locator"),
        ("release_url", "https://example.invalid", "HTTPS locator"),
        ("release_url", "https://example.invalid/releases//v1.0.0", "HTTPS locator"),
        (
            "release_url",
            "https://github.com/other/project/releases/tag/v1.0.0",
            "exactly identify the project tag",
        ),
        (
            "release_url",
            "https://user:secret@example.invalid/releases/v1.0.0",
            "HTTPS locator",
        ),
        ("artifact_sha256", "0" * 63, "lowercase SHA-256"),
        ("release_notes_sha256", "F" * 64, "lowercase SHA-256"),
        ("publication_channels", [], "publication channels are incomplete"),
        ("support_status", "unsupported", "must be supported"),
        ("yanked", True, "explicitly non-yanked"),
        ("draft", True, "explicitly non-draft"),
        ("prerelease", True, "explicitly final"),
    ],
)
def test_release_records_fail_closed(
    tmp_path: Path, field: str, value: object, message: str
) -> None:
    record = _record("1.0.0", character="1")
    record[field] = value
    document = _manifest()
    document["release_records"] = [record]
    channel = _write_manifest(tmp_path, document)
    _, evaluate = _evaluator()

    with pytest.raises(RuntimeError, match=message):
        evaluate(channel)


def test_release_records_are_unique_and_strictly_increasing(tmp_path: Path) -> None:
    _, evaluate = _evaluator()
    duplicate_document = _manifest()
    duplicate_document["release_records"] = [
        _record("1.0.0", character="1"),
        _record("1.0.0", character="2"),
    ]
    with pytest.raises(RuntimeError, match="repeats a version or tag"):
        evaluate(_write_manifest(tmp_path, duplicate_document))

    descending_document = _manifest()
    descending_document["release_records"] = [
        _record("1.1.0", character="1"),
        _record("1.0.0", character="2"),
    ]
    with pytest.raises(RuntimeError, match="strictly increasing"):
        evaluate(_write_manifest(tmp_path, descending_document))

    reused_identity_document = _manifest()
    second = _record("1.1.0", character="2")
    second["commit"] = "1" * 40
    reused_identity_document["release_records"] = [
        _record("1.0.0", character="1"),
        second,
    ]
    with pytest.raises(RuntimeError, match="repeats a publication identity"):
        evaluate(_write_manifest(tmp_path, reused_identity_document))


def test_release_channel_manifest_read_and_record_count_are_bounded(tmp_path: Path) -> None:
    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * 65_537)
    _, evaluate = _evaluator()
    with pytest.raises(RuntimeError, match="exceeds its byte limit"):
        evaluate(oversized)

    document = _manifest()
    document["release_records"] = [
        _record(f"1.{index}.0", character=f"{index % 10}") for index in range(65)
    ]
    channel = _write_manifest(tmp_path, document)
    with pytest.raises(RuntimeError, match="record limit"):
        evaluate(channel)


def test_release_channel_readiness_rejects_unknown_arguments() -> None:
    result = _run("--publish")

    assert result.returncode == 2
    assert "unrecognized arguments" in result.stderr


def test_explicit_release_channel_symlink_is_rejected(tmp_path: Path) -> None:
    linked = tmp_path / "linked-release-channel.json"
    try:
        linked.symlink_to(_CHANNEL)
    except OSError:
        pytest.skip("symbolic-link creation is unavailable")

    result = _run("--channel", str(linked))

    assert result.returncode == 1
    assert "release-channel manifest must not be a symbolic link" in result.stderr
