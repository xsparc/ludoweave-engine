"""Evaluate reviewed third-party conformance adoption without discovering packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from ipaddress import ip_address
from pathlib import Path
from typing import cast
from urllib.parse import urlsplit

from ludoweave import __version__

_SCHEMA = "ludoweave.evaluation.third-party-conformance-adoption-readiness/1"
_MANIFEST_SCHEMA = "ludoweave.adoption.third-party-conformance/1"
_MEASUREMENT_POLICY = "complete-reviewed-project-accepted-third-party-conformance-submissions/1"
_REVIEWED_MANIFEST_SHA256 = "adee8c68b5d89923ee2682162eb24cd9542a4601b1ff6fb901709ebcc0066767"
_MAX_MANIFEST_BYTES = 262_144
_MAX_JSON_NESTING = 16
_MAX_SUBMISSIONS = 64
_SAFE_ID = re.compile(r"[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*\Z")
_VERSION = re.compile(r"[0-9][0-9A-Za-z]*(?:[.+-][0-9A-Za-z]+)*\Z")
_GIT_SHA = re.compile(r"[0-9a-f]{40}\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_SPDX = re.compile(r"[A-Za-z0-9][A-Za-z0-9.+-]{0,63}\Z")
_IMMUTABLE_PATH = re.compile(r"/(?:blob|commit)/[0-9a-f]{40}(?:/|\Z)")


@dataclass(frozen=True, slots=True)
class _ProfileRule:
    protocol: str
    profile: str
    check_count: int
    category: str
    plugin_backed: bool


_PROFILE_RULES = {
    "agent-tool-adapter": _ProfileRule(
        "ludoweave.agent-tool-conformance/1",
        "agent-tool-baseline/1",
        12,
        "adapter",
        False,
    ),
    "render-device-adapter": _ProfileRule(
        "ludoweave.render-device-conformance/1",
        "render-device-baseline/1",
        9,
        "adapter",
        False,
    ),
    "render-device-plugin": _ProfileRule(
        "ludoweave.render-device-conformance/1",
        "render-device-baseline/1",
        9,
        "plugin-adapter",
        True,
    ),
    "world-store-adapter": _ProfileRule(
        "ludoweave.world-store-conformance/1",
        "world-store-baseline/1",
        10,
        "adapter",
        False,
    ),
}
_PROFILE_KEYS = (
    "agent-tool-baseline/1",
    "render-device-baseline/1",
    "world-store-baseline/1",
)
_NOT_EXECUTED_CODES = {
    "conformance-run-cancelled",
    "conformance-run-not-started",
    "conformance-run-unavailable",
    "submission-withdrawn-before-run",
}


@dataclass(frozen=True, slots=True)
class _SubmissionIdentity:
    submission_id: str
    implementation_id: str
    implementation_kind: str
    category: str
    package_id: str
    package_version: str
    repository_url: str
    revision: str
    license_spdx: str
    ludoweave_version: str
    platform: str
    python_version: str
    conformance_protocol: str
    conformance_profile: str
    check_count: int
    passed_check_count: int
    outcome: str
    outcome_code: str
    package_artifact_url: str
    package_sha256: str
    ludoweave_wheel_url: str
    ludoweave_wheel_sha256: str
    conformance_report_url: str | None
    conformance_report_sha256: str | None
    plugin_manifest_url: str | None
    plugin_manifest_sha256: str | None
    plugin_check_url: str | None
    plugin_check_sha256: str | None
    plugin_compatible: bool | None
    review_url: str
    review_sha256: str


_MANDATORY_SUBMISSION_PREFIX: tuple[_SubmissionIdentity, ...] = ()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--submissions",
        type=Path,
        default=None,
        help="explicit local reviewed third-party conformance manifest",
    )
    arguments = parser.parse_args(tuple(sys.argv[1:] if argv is None else argv))
    selected: object = getattr(arguments, "submissions", None)
    submissions = _default_manifest() if selected is None else _path(selected)
    try:
        report = evaluate(submissions)
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0


def evaluate(manifest: Path) -> dict[str, object]:
    """Return deterministic aggregate third-party conformance evidence."""

    raw_manifest, identities = _parse_manifest(manifest)
    manifest_hash = hashlib.sha256(raw_manifest).hexdigest()
    manifest_identity_reviewed = manifest_hash == _REVIEWED_MANIFEST_SHA256
    historical_submissions_preserved = tuple(
        identities[: len(_MANDATORY_SUBMISSION_PREFIX)]
    ) == _MANDATORY_SUBMISSION_PREFIX and (
        not manifest_identity_reviewed or len(identities) == len(_MANDATORY_SUBMISSION_PREFIX)
    )
    admitted = identities if manifest_identity_reviewed and historical_submissions_preserved else ()
    passed = tuple(item for item in admitted if item.outcome == "passed")
    failed_count = sum(item.outcome == "failed" for item in admitted)
    not_executed_count = sum(item.outcome == "not-executed" for item in admitted)
    passing_profiles = {
        profile: sum(item.conformance_profile == profile for item in passed)
        for profile in _PROFILE_KEYS
    }
    passing_adapter_count = sum(item.category == "adapter" for item in passed)
    passing_plugin_count = sum(item.category == "plugin-adapter" for item in passed)
    reviewed_submission_present = bool(admitted)
    passing_implementation_present = bool(passed)
    gate_satisfied = (
        manifest_identity_reviewed
        and historical_submissions_preserved
        and passing_implementation_present
    )
    reasons: list[str]
    if manifest_identity_reviewed and historical_submissions_preserved and not identities:
        reasons = ["third-party-conformance-evidence-absent"]
    else:
        reasons = []
        if not manifest_identity_reviewed:
            reasons.append("third-party-conformance-manifest-identity-unreviewed")
        if not historical_submissions_preserved:
            reasons.append("historical-conformance-submission-missing")
        if not passing_implementation_present:
            reasons.append("passing-third-party-implementation-absent")

    return {
        "admission": {
            "accepted_profile_count": len(_PROFILE_KEYS),
            "historical_submissions_preserved": historical_submissions_preserved,
            "manifest_identity_reviewed": manifest_identity_reviewed,
            "passing_third_party_implementation_present": passing_implementation_present,
            "reviewed_submission_present": reviewed_submission_present,
            "reason_codes": tuple(reasons),
            "submission_census_complete_reviewed": True,
        },
        "evidence_level": (
            "reviewed-third-party-conformance-adoption"
            if gate_satisfied
            else "third-party-conformance-adoption-readiness"
        ),
        "gate_satisfied": gate_satisfied,
        "ludoweave_version": __version__,
        "metrics": {
            "failed_submission_count": failed_count,
            "manifest_sha256": manifest_hash,
            "measurement_policy": _MEASUREMENT_POLICY,
            "not_executed_submission_count": not_executed_count,
            "passing_adapter_count": passing_adapter_count,
            "passing_by_profile": passing_profiles,
            "passing_implementation_count": len(passed),
            "passing_plugin_adapter_count": passing_plugin_count,
            "records_verified": True,
            "reviewed_submission_count": len(admitted),
        },
        "schema": _SCHEMA,
        "status": "ready" if gate_satisfied else "not-ready",
        "third_party_conformance_adoption_proven": gate_satisfied,
    }


def _parse_manifest(path: Path) -> tuple[bytes, tuple[_SubmissionIdentity, ...]]:
    raw_manifest = _read_bounded(path, _MAX_MANIFEST_BYTES, "conformance manifest")
    document = _object(_loads(raw_manifest, "conformance manifest"), "conformance manifest")
    _exact_fields(
        document,
        {
            "schema",
            "source_project",
            "measurement_policy",
            "submission_census_complete_reviewed",
            "submissions",
        },
        "conformance manifest",
    )
    if document["schema"] != _MANIFEST_SCHEMA:
        raise RuntimeError("conformance manifest schema is incompatible")
    if document["source_project"] != "ludoweave-engine":
        raise RuntimeError("conformance manifest project identity is invalid")
    if document["measurement_policy"] != _MEASUREMENT_POLICY:
        raise RuntimeError("conformance manifest measurement policy is incompatible")
    if document["submission_census_complete_reviewed"] is not True:
        raise RuntimeError("conformance submission census is not completely reviewed")
    raw_submissions = _list(document["submissions"], "conformance submissions")
    if len(raw_submissions) > _MAX_SUBMISSIONS:
        raise RuntimeError("conformance manifest exceeds its submission limit")

    identities: list[_SubmissionIdentity] = []
    implementations: set[str] = set()
    report_urls: set[str] = set()
    report_hashes: set[str] = set()
    review_urls: set[str] = set()
    review_hashes: set[str] = set()
    for index, item in enumerate(raw_submissions):
        identity = _submission_identity(_object(item, "conformance submission"), index)
        _claim_unique(identity.implementation_id, implementations, "implementation identity")
        _claim_optional_unique(
            identity.conformance_report_url, report_urls, "conformance report locator"
        )
        _claim_optional_unique(
            identity.conformance_report_sha256, report_hashes, "conformance report identity"
        )
        _claim_unique(identity.review_url, review_urls, "submission review locator")
        _claim_unique(identity.review_sha256, review_hashes, "submission review identity")
        identities.append(identity)
    return raw_manifest, tuple(identities)


def _submission_identity(record: dict[str, object], index: int) -> _SubmissionIdentity:
    _exact_fields(
        record,
        {
            "submission_id",
            "implementation_id",
            "implementation_kind",
            "package_id",
            "package_version",
            "repository_url",
            "revision",
            "relationship",
            "project_owned",
            "maintainer_authored",
            "license_spdx",
            "installed_distribution",
            "ludoweave_version",
            "platform",
            "python_implementation",
            "python_version",
            "conformance_protocol",
            "conformance_profile",
            "adapter_id",
            "check_count",
            "passed_check_count",
            "outcome",
            "outcome_code",
            "package_artifact_url",
            "package_sha256",
            "ludoweave_wheel_url",
            "ludoweave_wheel_sha256",
            "conformance_report_url",
            "conformance_report_sha256",
            "plugin_manifest_url",
            "plugin_manifest_sha256",
            "plugin_check_url",
            "plugin_check_sha256",
            "plugin_compatible",
            "review_url",
            "review_sha256",
            "authorship_reviewed",
            "independence_reviewed",
            "license_reviewed",
            "eligibility_reviewed",
            "outcome_reviewed",
            "provenance_reviewed",
            "validation_reviewed",
            "privacy_and_consent_reviewed",
        },
        "conformance submission",
    )
    submission_id = _bounded_ascii(record["submission_id"], 20, "submission ID")
    if submission_id != f"submission-{index + 1:04d}":
        raise RuntimeError("conformance submissions must use canonical sequential IDs")
    implementation_id = _safe_id(record["implementation_id"], "implementation ID")
    implementation_kind = _bounded_ascii(record["implementation_kind"], 32, "implementation kind")
    rule = _PROFILE_RULES.get(implementation_kind)
    if rule is None:
        raise RuntimeError("implementation kind is not admitted")
    package_id = _safe_id(record["package_id"], "package ID")
    package_version = _version(record["package_version"], "package version")
    repository_url = _repository_url(record["repository_url"])
    revision = _git_sha(record["revision"], "implementation revision")
    if record["relationship"] != "independent-external":
        raise RuntimeError("implementation relationship must be independent and external")
    if _bool(record["project_owned"], "project-owned status"):
        raise RuntimeError("project-owned implementations are not third-party evidence")
    if _bool(record["maintainer_authored"], "maintainer authorship status"):
        raise RuntimeError("maintainer-authored implementations are not third-party evidence")
    for field, label in (
        ("authorship_reviewed", "authorship review"),
        ("independence_reviewed", "independence review"),
        ("license_reviewed", "license review"),
        ("eligibility_reviewed", "eligibility review"),
        ("outcome_reviewed", "outcome review"),
        ("provenance_reviewed", "provenance review"),
        ("validation_reviewed", "validation review"),
        ("privacy_and_consent_reviewed", "privacy and consent review"),
    ):
        if not _bool(record[field], label):
            raise RuntimeError(f"{label} must be explicitly complete")

    license_spdx = _spdx(record["license_spdx"])
    if record["installed_distribution"] != "public-wheel":
        raise RuntimeError("conformance must exercise a public installed wheel")
    ludoweave_version = _version(record["ludoweave_version"], "LudoWeave version")
    platform = _bounded_ascii(record["platform"], 16, "platform")
    if platform not in {"linux", "macos", "windows"}:
        raise RuntimeError("conformance platform is unsupported")
    if record["python_implementation"] != "CPython":
        raise RuntimeError("conformance Python implementation must be CPython")
    python_version = _bounded_ascii(record["python_version"], 8, "Python version")
    if python_version not in {"3.12", "3.13", "3.14"}:
        raise RuntimeError("conformance Python version is unsupported")
    protocol = _bounded_ascii(record["conformance_protocol"], 64, "conformance protocol")
    profile = _bounded_ascii(record["conformance_profile"], 48, "conformance profile")
    if (protocol, profile) != (rule.protocol, rule.profile):
        raise RuntimeError("implementation kind and conformance profile do not match")
    adapter_id = _safe_id(record["adapter_id"], "adapter ID")
    if adapter_id != implementation_id:
        raise RuntimeError("adapter and implementation identities must match")
    check_count = _positive_int(record["check_count"], 64, "conformance check count")
    if check_count != rule.check_count:
        raise RuntimeError("conformance check count does not match its profile")
    passed_check_count = _non_negative_int(
        record["passed_check_count"], check_count, "passed check count"
    )

    outcome = _bounded_ascii(record["outcome"], 24, "conformance outcome")
    outcome_code = _bounded_ascii(record["outcome_code"], 48, "conformance outcome code")
    report_url = _nullable_immutable_url(
        record["conformance_report_url"], "conformance report locator"
    )
    report_hash = _nullable_sha256(record["conformance_report_sha256"], "conformance report sha256")
    if (report_url is None) is not (report_hash is None):
        raise RuntimeError("conformance report locator and identity must appear together")
    _validate_outcome(
        outcome=outcome,
        outcome_code=outcome_code,
        check_count=check_count,
        passed_check_count=passed_check_count,
        report_present=report_url is not None,
    )

    package_artifact_url = _wheel_url(record["package_artifact_url"], "package artifact")
    package_hash = _sha256(record["package_sha256"], "package artifact sha256")
    wheel_url = _wheel_url(record["ludoweave_wheel_url"], "LudoWeave wheel")
    wheel_hash = _sha256(record["ludoweave_wheel_sha256"], "LudoWeave wheel sha256")
    plugin_manifest_url = _nullable_immutable_url(
        record["plugin_manifest_url"], "plugin manifest locator"
    )
    plugin_manifest_hash = _nullable_sha256(
        record["plugin_manifest_sha256"], "plugin manifest sha256"
    )
    plugin_check_url = _nullable_immutable_url(record["plugin_check_url"], "plugin check locator")
    plugin_check_hash = _nullable_sha256(record["plugin_check_sha256"], "plugin check sha256")
    plugin_compatible = _nullable_bool(record["plugin_compatible"], "plugin compatibility")
    plugin_values = (
        plugin_manifest_url,
        plugin_manifest_hash,
        plugin_check_url,
        plugin_check_hash,
    )
    if rule.plugin_backed:
        if any(value is None for value in plugin_values) or plugin_compatible is not True:
            raise RuntimeError("plugin-backed conformance requires compatible manifest evidence")
    elif any(value is not None for value in plugin_values) or plugin_compatible is not None:
        raise RuntimeError("adapter-only conformance must not claim plugin evidence")

    review_url = _immutable_url(record["review_url"], "submission review locator")
    review_hash = _sha256(record["review_sha256"], "submission review sha256")
    hashes = {
        package_hash,
        wheel_hash,
        review_hash,
        *(value for value in (report_hash, plugin_manifest_hash, plugin_check_hash) if value),
    }
    expected_hash_count = 3 + int(report_hash is not None) + int(rule.plugin_backed) * 2
    if len(hashes) != expected_hash_count:
        raise RuntimeError("submission evidence identities must be distinct")

    return _SubmissionIdentity(
        submission_id=submission_id,
        implementation_id=implementation_id,
        implementation_kind=implementation_kind,
        category=rule.category,
        package_id=package_id,
        package_version=package_version,
        repository_url=repository_url,
        revision=revision,
        license_spdx=license_spdx,
        ludoweave_version=ludoweave_version,
        platform=platform,
        python_version=python_version,
        conformance_protocol=protocol,
        conformance_profile=profile,
        check_count=check_count,
        passed_check_count=passed_check_count,
        outcome=outcome,
        outcome_code=outcome_code,
        package_artifact_url=package_artifact_url,
        package_sha256=package_hash,
        ludoweave_wheel_url=wheel_url,
        ludoweave_wheel_sha256=wheel_hash,
        conformance_report_url=report_url,
        conformance_report_sha256=report_hash,
        plugin_manifest_url=plugin_manifest_url,
        plugin_manifest_sha256=plugin_manifest_hash,
        plugin_check_url=plugin_check_url,
        plugin_check_sha256=plugin_check_hash,
        plugin_compatible=plugin_compatible,
        review_url=review_url,
        review_sha256=review_hash,
    )


def _validate_outcome(
    *,
    outcome: str,
    outcome_code: str,
    check_count: int,
    passed_check_count: int,
    report_present: bool,
) -> None:
    if outcome == "passed":
        if (
            outcome_code != "conformance-profile-passed"
            or passed_check_count != check_count
            or not report_present
        ):
            raise RuntimeError("passing conformance evidence is inconsistent")
    elif outcome == "failed":
        if (
            outcome_code != "conformance-profile-failed"
            or passed_check_count >= check_count
            or not report_present
        ):
            raise RuntimeError("failed conformance evidence is inconsistent")
    elif outcome == "not-executed":
        if outcome_code not in _NOT_EXECUTED_CODES or passed_check_count != 0 or report_present:
            raise RuntimeError("non-executed conformance evidence is inconsistent")
    else:
        raise RuntimeError("conformance outcome is incompatible")


def _default_manifest() -> Path:
    bundled = Path(__file__).resolve().parent / "assets" / "third_party_conformance_adoption.json"
    if bundled.is_file():
        return bundled
    return Path(__file__).resolve().parents[1] / "tests" / "fixtures" / bundled.name


def _path(value: object) -> Path:
    if not isinstance(value, Path):
        raise RuntimeError("conformance manifest argument is invalid")
    return value


def _read_bounded(path: Path, limit: int, label: str) -> bytes:
    try:
        if path.is_symlink():
            raise RuntimeError(f"{label} must not be a symbolic link")
        with path.open("rb") as stream:
            payload = stream.read(limit + 1)
    except RuntimeError:
        raise
    except OSError as error:
        raise RuntimeError(f"{label} is unavailable") from error
    if len(payload) > limit:
        raise RuntimeError(f"{label} exceeds its byte limit")
    return payload


def _loads(payload: bytes, label: str) -> object:
    try:
        text = payload.decode("utf-8")
        value = json.loads(text, object_pairs_hook=_unique_object)
        if _json_depth(value) > _MAX_JSON_NESTING:
            raise RuntimeError(f"{label} exceeds its nesting limit")
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError, ValueError) as error:
        raise RuntimeError(f"{label} is not valid JSON") from error
    return value


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    document: dict[str, object] = {}
    for key, value in pairs:
        if key in document:
            raise ValueError("duplicate JSON field")
        document[key] = value
    return document


def _json_depth(value: object) -> int:
    if isinstance(value, dict):
        mapping = cast(dict[object, object], value)
        return 1 + max((_json_depth(item) for item in mapping.values()), default=0)
    if isinstance(value, list):
        items = cast(list[object], value)
        return 1 + max((_json_depth(item) for item in items), default=0)
    return 0


def _object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _list(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise RuntimeError(f"{label} must be an array")
    return cast(list[object], value)


def _exact_fields(value: dict[str, object], expected: set[str], label: str) -> None:
    if set(value) != expected:
        raise RuntimeError(f"{label} fields are incompatible")


def _bool(value: object, label: str) -> bool:
    if type(value) is not bool:
        raise RuntimeError(f"{label} must be boolean")
    return value


def _nullable_bool(value: object, label: str) -> bool | None:
    if value is None:
        return None
    return _bool(value, label)


def _bounded_ascii(value: object, limit: int, label: str) -> str:
    if not isinstance(value, str) or not value or len(value) > limit or not value.isascii():
        raise RuntimeError(f"{label} is invalid")
    return value


def _safe_id(value: object, label: str) -> str:
    text = _bounded_ascii(value, 96, label)
    if _SAFE_ID.fullmatch(text) is None:
        raise RuntimeError(f"{label} is invalid")
    return text


def _version(value: object, label: str) -> str:
    text = _bounded_ascii(value, 32, label)
    if _VERSION.fullmatch(text) is None:
        raise RuntimeError(f"{label} is invalid")
    return text


def _git_sha(value: object, label: str) -> str:
    text = _bounded_ascii(value, 40, label)
    if _GIT_SHA.fullmatch(text) is None:
        raise RuntimeError(f"{label} is invalid")
    return text


def _sha256(value: object, label: str) -> str:
    text = _bounded_ascii(value, 64, label)
    if _SHA256.fullmatch(text) is None:
        raise RuntimeError(f"{label} is invalid")
    return text


def _nullable_sha256(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _sha256(value, label)


def _spdx(value: object) -> str:
    text = _bounded_ascii(value, 64, "license SPDX identity")
    if _SPDX.fullmatch(text) is None or text in {"NONE", "NOASSERTION"}:
        raise RuntimeError("license SPDX identity is invalid")
    return text


def _positive_int(value: object, maximum: int, label: str) -> int:
    if type(value) is not int or value < 1 or value > maximum:
        raise RuntimeError(f"{label} is invalid")
    return value


def _non_negative_int(value: object, maximum: int, label: str) -> int:
    if type(value) is not int or value < 0 or value > maximum:
        raise RuntimeError(f"{label} is invalid")
    return value


def _repository_url(value: object) -> str:
    url = _https_url(value, "implementation repository")
    path = urlsplit(url).path.rstrip("/")
    if not path or path.count("/") < 2:
        raise RuntimeError("implementation repository locator is invalid")
    return url.rstrip("/")


def _https_url(value: object, label: str) -> str:
    text = _bounded_ascii(value, 512, f"{label} locator")
    try:
        parsed = urlsplit(text)
        port = parsed.port
    except ValueError as error:
        raise RuntimeError(f"{label} locator is invalid") from error
    host = parsed.hostname
    if (
        parsed.scheme != "https"
        or host is None
        or parsed.username is not None
        or parsed.password is not None
        or port is not None
        or parsed.query
        or parsed.fragment
        or not parsed.path.startswith("/")
    ):
        raise RuntimeError(f"{label} locator is invalid")
    normalized_host = host.casefold().rstrip(".")
    if (
        "." not in normalized_host
        or normalized_host == "localhost"
        or normalized_host in {"example.com", "example.net", "example.org"}
        or normalized_host.endswith(
            (".localhost", ".local", ".internal", ".invalid", ".example", ".test")
        )
    ):
        raise RuntimeError(f"{label} locator host is not public")
    try:
        ip_address(normalized_host)
    except ValueError:
        pass
    else:
        raise RuntimeError(f"{label} locator must not use an IP authority")
    return text


def _wheel_url(value: object, label: str) -> str:
    text = _https_url(value, label)
    if not urlsplit(text).path.casefold().endswith(".whl"):
        raise RuntimeError(f"{label} locator must identify a wheel")
    return text


def _immutable_url(value: object, label: str) -> str:
    text = _https_url(value, label)
    if _IMMUTABLE_PATH.search(urlsplit(text).path) is None:
        raise RuntimeError(f"{label} must identify an immutable revision")
    return text


def _nullable_immutable_url(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _immutable_url(value, label)


def _claim_unique(value: str, seen: set[str], label: str) -> None:
    if value in seen:
        raise RuntimeError(f"conformance manifest repeats a {label}")
    seen.add(value)


def _claim_optional_unique(value: str | None, seen: set[str], label: str) -> None:
    if value is not None:
        _claim_unique(value, seen, label)


if __name__ == "__main__":
    raise SystemExit(main())
