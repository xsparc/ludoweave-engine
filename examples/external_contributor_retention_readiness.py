"""Evaluate reviewed external-contributor retention without inventing people."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from ludoweave import __version__

type _ContributionIdentity = tuple[
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    tuple[str, ...],
    str,
    bool,
    str,
    bool,
    bool,
]
type _RetentionIdentity = tuple[
    str,
    str,
    str,
    bool,
    bool,
    bool,
    bool,
    bool,
    _ContributionIdentity,
    _ContributionIdentity,
]

_SCHEMA = "ludoweave.evaluation.external-contributor-retention-readiness/1"
_MANIFEST_SCHEMA = "ludoweave.community.external-contributor-retention/1"
_REQUIRED_VALIDATION_STEPS = ("clean-setup", "focused-check", "complete-gate")
_ALLOWED_TASK_SCOPES = (
    "bugfix",
    "documentation",
    "feature",
    "maintenance",
    "tests",
    "tooling",
)
_REVIEWED_RETENTION_SHA256 = "61785ec165e9f9a7c1025c37f7b714d6fa42b2c7081145a0f843395a325b36ee"
_MANDATORY_RETENTION_PREFIX: tuple[_RetentionIdentity, ...] = ()
_MAX_MANIFEST_BYTES = 65_536
_MAX_JSON_NESTING = 16
_MAX_RETENTION_RECORDS = 32


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--retention",
        type=Path,
        default=None,
        help="explicit local reviewed external-contributor retention manifest",
    )
    arguments = parser.parse_args(tuple(sys.argv[1:] if argv is None else argv))
    selected: object = getattr(arguments, "retention", None)
    retention = _default_retention() if selected is None else _path(selected)
    print(
        json.dumps(
            evaluate(retention),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


def evaluate(retention: Path) -> dict[str, object]:
    """Return deterministic, sanitized contributor-retention evidence."""

    raw_manifest = _read_bounded(retention, _MAX_MANIFEST_BYTES, "contributor-retention manifest")
    document = _object(
        _loads(raw_manifest, "contributor-retention manifest"),
        "contributor-retention manifest",
    )
    _exact_fields(
        document,
        {
            "schema",
            "source_project",
            "minimum_retained_contributors",
            "required_validation_steps",
            "retention_records",
        },
        "contributor-retention manifest",
    )
    if document["schema"] != _MANIFEST_SCHEMA:
        raise RuntimeError("contributor-retention manifest schema is incompatible")
    if document["source_project"] != "ludoweave-engine":
        raise RuntimeError("contributor-retention project identity is invalid")
    minimum = _positive_int(
        document["minimum_retained_contributors"], "minimum retained contributors"
    )
    if minimum != 1:
        raise RuntimeError("contributor-retention minimum must remain one")
    validation_steps = tuple(
        _bounded_text(item, 64, "validation step")
        for item in _list(document["required_validation_steps"], "validation steps")
    )
    if validation_steps != _REQUIRED_VALIDATION_STEPS:
        raise RuntimeError("contributor-retention validation steps are incompatible")

    raw_records = _list(document["retention_records"], "retention records")
    if len(raw_records) > _MAX_RETENTION_RECORDS:
        raise RuntimeError("contributor-retention manifest exceeds its record limit")
    identities: list[_RetentionIdentity] = []
    contributors: set[str] = set()
    issue_urls: set[str] = set()
    pull_request_urls: set[str] = set()
    revision_ids: set[str] = set()
    artifact_hashes: set[str] = set()
    for item in raw_records:
        identity = _retention_identity(_object(item, "retention record"), validation_steps)
        if identity[0] in contributors:
            raise RuntimeError("contributor-retention manifest repeats a contributor")
        first = identity[8]
        returned = identity[9]
        record_issue_urls = (first[0], returned[0])
        record_pull_request_urls = (first[1], returned[1])
        record_revision_ids = (first[3], first[4], returned[3], returned[4])
        record_artifact_hashes = (first[5], first[6], returned[5], returned[6])
        if issue_urls.intersection(record_issue_urls):
            raise RuntimeError("contributor-retention manifest repeats an issue")
        if pull_request_urls.intersection(record_pull_request_urls):
            raise RuntimeError("contributor-retention manifest repeats a pull request")
        if revision_ids.intersection(record_revision_ids):
            raise RuntimeError("contributor-retention manifest repeats a revision identity")
        if artifact_hashes.intersection(record_artifact_hashes):
            raise RuntimeError("contributor-retention manifest repeats an artifact identity")
        contributors.add(identity[0])
        issue_urls.update(record_issue_urls)
        pull_request_urls.update(record_pull_request_urls)
        revision_ids.update(record_revision_ids)
        artifact_hashes.update(record_artifact_hashes)
        identities.append(identity)

    manifest_hash = hashlib.sha256(raw_manifest).hexdigest()
    manifest_identity_reviewed = manifest_hash == _REVIEWED_RETENTION_SHA256
    historical_retention_preserved = tuple(
        identities[: len(_MANDATORY_RETENTION_PREFIX)]
    ) == _MANDATORY_RETENTION_PREFIX and (
        not manifest_identity_reviewed or len(identities) == len(_MANDATORY_RETENTION_PREFIX)
    )
    admitted_identities = (
        identities if manifest_identity_reviewed and historical_retention_preserved else []
    )
    retained_contributor_present = len(admitted_identities) >= minimum
    gate_satisfied = (
        manifest_identity_reviewed
        and historical_retention_preserved
        and retained_contributor_present
    )
    task_scopes = [
        scope for identity in admitted_identities for scope in (identity[8][7], identity[9][7])
    ]
    reasons: list[str] = []
    if not manifest_identity_reviewed:
        reasons.append("contributor-retention-manifest-identity-unreviewed")
    if not historical_retention_preserved:
        reasons.append("historical-contributor-retention-record-missing")
    if not retained_contributor_present:
        reasons.append("retained-external-contributor-absent")

    return {
        "admission": {
            "historical_retention_preserved": historical_retention_preserved,
            "manifest_identity_reviewed": manifest_identity_reviewed,
            "minimum_retained_contributors": minimum,
            "reason_codes": tuple(reasons),
            "retained_external_contributor_present": retained_contributor_present,
        },
        "contributor_retention_proven": gate_satisfied,
        "evidence_level": (
            "reviewed-external-contributor-retention"
            if gate_satisfied
            else "external-contributor-retention-admission-readiness"
        ),
        "gate_satisfied": gate_satisfied,
        "ludoweave_version": __version__,
        "retention": {
            "manifest_sha256": manifest_hash,
            "records_verified": True,
            "retained_contributor_count": len(admitted_identities),
            "return_contribution_count": len(admitted_identities),
            "task_scopes": tuple(task_scopes),
            "validation_steps": validation_steps,
        },
        "schema": _SCHEMA,
        "status": "ready" if gate_satisfied else "not-ready",
    }


def _retention_identity(
    record: dict[str, object], required_validation_steps: tuple[str, ...]
) -> _RetentionIdentity:
    _exact_fields(
        record,
        {
            "contributor_login",
            "contributor_type",
            "relationship",
            "identity_reviewed",
            "independence_reviewed",
            "same_contributor_reviewed",
            "chronology_reviewed",
            "retention_reviewed",
            "first_contribution",
            "return_contribution",
        },
        "retention record",
    )
    contributor_login = _github_login(record["contributor_login"])
    contributor_type = _bounded_text(record["contributor_type"], 16, "contributor type")
    if contributor_type != "human":
        raise RuntimeError("contributor retention must identify a human contributor")
    relationship = _bounded_text(record["relationship"], 32, "contributor relationship")
    if relationship != "independent-external":
        raise RuntimeError("retained contributor must remain independent and external")
    identity_reviewed = _required_true(record["identity_reviewed"], "contributor identity")
    independence_reviewed = _required_true(
        record["independence_reviewed"], "contributor independence"
    )
    same_contributor_reviewed = _required_true(
        record["same_contributor_reviewed"], "same-contributor review"
    )
    chronology_reviewed = _required_true(record["chronology_reviewed"], "contribution chronology")
    retention_reviewed = _required_true(record["retention_reviewed"], "retention review")
    first = _contribution_identity(
        _object(record["first_contribution"], "first contribution"),
        required_validation_steps,
        "first",
    )
    returned = _contribution_identity(
        _object(record["return_contribution"], "return contribution"),
        required_validation_steps,
        "return",
    )
    if first[0] == returned[0] or first[1] == returned[1]:
        raise RuntimeError("retention contributions must use distinct public records")
    if set(first[3:5]).intersection(returned[3:5]):
        raise RuntimeError("retention contributions must use distinct revision identities")
    if set(first[5:7]).intersection(returned[5:7]):
        raise RuntimeError("retention contributions must use distinct artifact identities")
    if _utc_key(returned[11]) <= _utc_key(first[11]):
        raise RuntimeError("return contribution must merge after the first contribution")
    return (
        contributor_login,
        contributor_type,
        relationship,
        identity_reviewed,
        independence_reviewed,
        same_contributor_reviewed,
        chronology_reviewed,
        retention_reviewed,
        first,
        returned,
    )


def _contribution_identity(
    contribution: dict[str, object],
    required_validation_steps: tuple[str, ...],
    role: str,
) -> _ContributionIdentity:
    _exact_fields(
        contribution,
        {
            "issue_url",
            "pull_request_url",
            "base_commit",
            "head_commit",
            "merge_commit",
            "patch_sha256",
            "review_sha256",
            "task_scope",
            "validation_steps",
            "outcome",
            "dco_valid",
            "merged_at",
            "provenance_reviewed",
            "validation_reviewed",
        },
        f"{role} contribution",
    )
    issue_url = _project_reference_url(contribution["issue_url"], "issues", f"{role} issue URL")
    pull_request_url = _project_reference_url(
        contribution["pull_request_url"], "pull", f"{role} pull request URL"
    )
    base_commit = _git_oid(contribution["base_commit"], f"{role} base commit")
    head_commit = _git_oid(contribution["head_commit"], f"{role} head commit")
    merge_commit = _git_oid(contribution["merge_commit"], f"{role} merge commit")
    if len({base_commit, head_commit, merge_commit}) != 3:
        raise RuntimeError(f"{role} contribution revisions must be distinct")
    patch_hash = _sha256_text(contribution["patch_sha256"], f"{role} patch sha256")
    review_hash = _sha256_text(contribution["review_sha256"], f"{role} review sha256")
    if patch_hash == review_hash:
        raise RuntimeError(f"{role} contribution artifact identities must be distinct")
    task_scope = _bounded_text(contribution["task_scope"], 32, f"{role} task scope")
    if task_scope not in _ALLOWED_TASK_SCOPES:
        raise RuntimeError(f"{role} contribution task scope is incompatible")
    validation_steps = tuple(
        _bounded_text(item, 64, f"{role} validation step")
        for item in _list(contribution["validation_steps"], f"{role} validation steps")
    )
    if validation_steps != required_validation_steps:
        raise RuntimeError(f"{role} contribution validation steps are incomplete")
    outcome = _bounded_text(contribution["outcome"], 16, f"{role} outcome")
    if outcome != "merged":
        raise RuntimeError(f"{role} contribution must have merged")
    dco_valid = _required_true(contribution["dco_valid"], f"{role} DCO validation")
    merged_at = _utc_timestamp(contribution["merged_at"], f"{role} merge timestamp")
    provenance_reviewed = _required_true(
        contribution["provenance_reviewed"], f"{role} contribution provenance"
    )
    validation_reviewed = _required_true(
        contribution["validation_reviewed"], f"{role} contribution validation"
    )
    return (
        issue_url,
        pull_request_url,
        base_commit,
        head_commit,
        merge_commit,
        patch_hash,
        review_hash,
        task_scope,
        validation_steps,
        outcome,
        dco_valid,
        merged_at,
        provenance_reviewed,
        validation_reviewed,
    )


def _default_retention() -> Path:
    bundled = Path(__file__).resolve().parent / "assets" / "external_contributor_retention.json"
    if bundled.is_file():
        return bundled
    return Path(__file__).resolve().parents[1] / "tests" / "fixtures" / bundled.name


def _read_bounded(path: Path, maximum: int, role: str) -> bytes:
    try:
        if path.is_symlink():
            raise RuntimeError(f"{role} must not be a symbolic link")
        with path.open("rb") as stream:
            value = stream.read(maximum + 1)
    except OSError as error:
        raise RuntimeError(f"{role} is unavailable") from error
    if len(value) > maximum:
        raise RuntimeError(f"{role} exceeds its byte limit")
    return value


def _loads(value: bytes, role: str) -> object:
    _reject_excessive_nesting(value, role)
    try:
        return json.loads(value, object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError, ValueError) as error:
        raise RuntimeError(f"{role} is not valid JSON") from error


def _reject_excessive_nesting(value: bytes, role: str) -> None:
    depth = 0
    in_string = False
    escaped = False
    for character in value:
        if in_string:
            if escaped:
                escaped = False
            elif character == ord("\\"):
                escaped = True
            elif character == ord('"'):
                in_string = False
            continue
        if character == ord('"'):
            in_string = True
        elif character in (ord("{"), ord("[")):
            depth += 1
            if depth > _MAX_JSON_NESTING:
                raise RuntimeError(f"{role} exceeds its nesting limit")
        elif character in (ord("}"), ord("]")) and depth > 0:
            depth -= 1


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def _exact_fields(value: dict[str, object], expected: set[str], role: str) -> None:
    if set(value) != expected:
        raise RuntimeError(f"{role} fields are incompatible")


def _path(value: object) -> Path:
    if not isinstance(value, Path):
        raise TypeError("retention must be a path")
    return value


def _object(value: object, role: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise RuntimeError(f"{role} must be an object")
    return cast(dict[str, object], value)


def _list(value: object, role: str) -> list[object]:
    if not isinstance(value, list):
        raise RuntimeError(f"{role} must be a list")
    return cast(list[object], value)


def _bounded_text(value: object, maximum: int, role: str) -> str:
    if not isinstance(value, str) or not value or len(value) > maximum:
        raise RuntimeError(f"{role} must be bounded non-empty text")
    return value


def _positive_int(value: object, role: str) -> int:
    if type(value) is not int or value <= 0:
        raise RuntimeError(f"{role} must be a positive integer")
    return value


def _github_login(value: object) -> str:
    login = _bounded_text(value, 39, "contributor login")
    if (
        not login.isascii()
        or not login[0].isalnum()
        or not login[-1].isalnum()
        or "--" in login
        or any(not (character.isalnum() or character == "-") for character in login)
        or login.casefold() in {"ludoweave", "ludoweave-engine", "xsparc"}
    ):
        raise RuntimeError("contributor login must identify an external GitHub user")
    return login.casefold()


def _project_reference_url(value: object, kind: str, role: str) -> str:
    text = _bounded_text(value, 512, role)
    prefix = f"https://github.com/xsparc/ludoweave-engine/{kind}/"
    number = text.removeprefix(prefix)
    if (
        not text.startswith(prefix)
        or not number.isascii()
        or not number.isdecimal()
        or number.startswith("0")
    ):
        raise RuntimeError(f"{role} must exactly identify a public project {kind} record")
    return text


def _sha256_text(value: object, role: str) -> str:
    text = _bounded_text(value, 64, role)
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise RuntimeError(f"{role} must be lowercase SHA-256")
    return text


def _git_oid(value: object, role: str) -> str:
    text = _bounded_text(value, 64, role)
    if len(text) not in {40, 64} or any(character not in "0123456789abcdef" for character in text):
        raise RuntimeError(f"{role} must be a lowercase Git object identity")
    return text


def _utc_timestamp(value: object, role: str) -> str:
    text = _bounded_text(value, 20, role)
    if (
        len(text) != 20
        or not text.isascii()
        or text[4] != "-"
        or text[7] != "-"
        or text[10] != "T"
        or text[13] != ":"
        or text[16] != ":"
        or text[19] != "Z"
        or not (
            text[0:4] + text[5:7] + text[8:10] + text[11:13] + text[14:16] + text[17:19]
        ).isdigit()
    ):
        raise RuntimeError(f"{role} must be a canonical UTC timestamp")
    year, month, day, hour, minute, second = _utc_key(text)
    if (
        year < 2000
        or not 1 <= month <= 12
        or not 1 <= day <= _days_in_month(year, month)
        or not 0 <= hour <= 23
        or not 0 <= minute <= 59
        or not 0 <= second <= 59
    ):
        raise RuntimeError(f"{role} must be a canonical UTC timestamp")
    return text


def _utc_key(value: str) -> tuple[int, int, int, int, int, int]:
    return (
        int(value[0:4]),
        int(value[5:7]),
        int(value[8:10]),
        int(value[11:13]),
        int(value[14:16]),
        int(value[17:19]),
    )


def _days_in_month(year: int, month: int) -> int:
    if month == 2:
        return 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28
    return 30 if month in {4, 6, 9, 11} else 31


def _required_true(value: object, role: str) -> bool:
    if type(value) is not bool or not value:
        raise RuntimeError(f"{role} must be explicitly true")
    return cast(bool, value)


if __name__ == "__main__":
    raise SystemExit(main())
