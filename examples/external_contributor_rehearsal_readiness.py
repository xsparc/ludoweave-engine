"""Evaluate reviewed first-external-contribution rehearsal evidence offline."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from ludoweave import __version__

type _RehearsalIdentity = tuple[
    str,
    str,
    bool,
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
    bool,
    bool,
    bool,
    bool,
    bool,
]

_SCHEMA = "ludoweave.evaluation.external-contributor-rehearsal-readiness/1"
_MANIFEST_SCHEMA = "ludoweave.community.external-contributor-rehearsal/1"
_REQUIRED_VALIDATION_STEPS = ("clean-setup", "focused-check", "complete-gate")
_ALLOWED_TASK_SCOPES = ("bugfix", "documentation", "tests", "tooling")
_REVIEWED_REHEARSAL_SHA256 = "ecb959e90a0033b4dbe3dcfe8a48db1c1eea915e0ef2840510969b9e25cdb9c7"
_MANDATORY_REHEARSAL_PREFIX: tuple[_RehearsalIdentity, ...] = ()
_MAX_MANIFEST_BYTES = 65_536
_MAX_REHEARSAL_RECORDS = 64


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rehearsals",
        type=Path,
        default=None,
        help="explicit local reviewed external-contributor rehearsal manifest",
    )
    arguments = parser.parse_args(tuple(sys.argv[1:] if argv is None else argv))
    selected: object = getattr(arguments, "rehearsals", None)
    rehearsals = _default_rehearsals() if selected is None else _path(selected)
    print(
        json.dumps(
            evaluate(rehearsals),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


def evaluate(rehearsals: Path) -> dict[str, object]:
    """Return deterministic, path-free first-contribution readiness evidence."""

    raw_manifest = _read_bounded(rehearsals, _MAX_MANIFEST_BYTES, "contributor-rehearsal manifest")
    document = _object(_loads(raw_manifest, "contributor-rehearsal manifest"), "rehearsal manifest")
    _exact_fields(
        document,
        {
            "schema",
            "source_project",
            "minimum_merged_rehearsals",
            "required_validation_steps",
            "rehearsal_records",
        },
        "contributor-rehearsal manifest",
    )
    if document["schema"] != _MANIFEST_SCHEMA:
        raise RuntimeError("contributor-rehearsal manifest schema is incompatible")
    if document["source_project"] != "ludoweave-engine":
        raise RuntimeError("contributor-rehearsal project identity is invalid")
    minimum = _positive_int(document["minimum_merged_rehearsals"], "minimum rehearsals")
    if minimum != 1:
        raise RuntimeError("contributor-rehearsal minimum must remain one")
    validation_steps = tuple(
        _bounded_text(item, 64, "validation step")
        for item in _list(document["required_validation_steps"], "validation steps")
    )
    if validation_steps != _REQUIRED_VALIDATION_STEPS:
        raise RuntimeError("contributor-rehearsal validation steps are incompatible")

    raw_records = _list(document["rehearsal_records"], "rehearsal records")
    if len(raw_records) > _MAX_REHEARSAL_RECORDS:
        raise RuntimeError("contributor-rehearsal manifest exceeds its record limit")
    identities: list[_RehearsalIdentity] = []
    seen_issue_urls: set[str] = set()
    seen_pull_request_urls: set[str] = set()
    seen_revision_ids: set[str] = set()
    seen_artifact_hashes: set[str] = set()
    for item in raw_records:
        identity = _rehearsal_identity(_object(item, "rehearsal record"), validation_steps)
        if identity[3] in seen_issue_urls or identity[4] in seen_pull_request_urls:
            raise RuntimeError("contributor-rehearsal manifest repeats a public record")
        if identity[6] in seen_revision_ids or identity[7] in seen_revision_ids:
            raise RuntimeError("contributor-rehearsal manifest repeats a revision identity")
        if identity[8] in seen_artifact_hashes or identity[9] in seen_artifact_hashes:
            raise RuntimeError("contributor-rehearsal manifest repeats an artifact identity")
        seen_issue_urls.add(identity[3])
        seen_pull_request_urls.add(identity[4])
        seen_revision_ids.update((identity[6], identity[7]))
        seen_artifact_hashes.update((identity[8], identity[9]))
        identities.append(identity)

    manifest_hash = hashlib.sha256(raw_manifest).hexdigest()
    manifest_identity_reviewed = manifest_hash == _REVIEWED_REHEARSAL_SHA256
    historical_rehearsals_preserved = tuple(
        identities[: len(_MANDATORY_REHEARSAL_PREFIX)]
    ) == _MANDATORY_REHEARSAL_PREFIX and (
        not manifest_identity_reviewed or len(identities) == len(_MANDATORY_REHEARSAL_PREFIX)
    )
    independent_rehearsal_present = len(identities) >= minimum
    gate_satisfied = (
        manifest_identity_reviewed
        and historical_rehearsals_preserved
        and independent_rehearsal_present
    )
    reasons: list[str] = []
    if not manifest_identity_reviewed:
        reasons.append("contributor-rehearsal-identity-unreviewed")
    if not historical_rehearsals_preserved:
        reasons.append("historical-contributor-rehearsal-missing")
    if not independent_rehearsal_present:
        reasons.append("external-contributor-rehearsal-absent")

    return {
        "admission": {
            "documentation_without_private_knowledge_proven": gate_satisfied,
            "historical_rehearsals_preserved": historical_rehearsals_preserved,
            "independent_contributor_rehearsal_present": independent_rehearsal_present,
            "manifest_identity_reviewed": manifest_identity_reviewed,
            "minimum_merged_rehearsals": minimum,
            "reason_codes": tuple(reasons),
        },
        "evidence_level": (
            "reviewed-external-contributor-rehearsal"
            if gate_satisfied
            else "external-contributor-rehearsal-admission-readiness"
        ),
        "first_external_contribution_proven": gate_satisfied,
        "gate_satisfied": gate_satisfied,
        "ludoweave_version": __version__,
        "rehearsals": {
            "manifest_sha256": manifest_hash,
            "record_count": len(identities),
            "records_verified": True,
            "task_scopes": tuple(identity[10] for identity in identities),
            "validation_steps": validation_steps,
        },
        "schema": _SCHEMA,
        "status": "ready" if gate_satisfied else "not-ready",
    }


def _rehearsal_identity(
    record: dict[str, object], required_validation_steps: tuple[str, ...]
) -> _RehearsalIdentity:
    _exact_fields(
        record,
        {
            "contributor_login",
            "contributor_type",
            "independence_reviewed",
            "issue_url",
            "pull_request_url",
            "base_commit",
            "head_commit",
            "merge_commit",
            "patch_sha256",
            "feedback_sha256",
            "task_scope",
            "validation_steps",
            "outcome",
            "dco_valid",
            "private_maintainer_knowledge_used",
            "public_api_changed",
            "persistent_format_changed",
            "dependency_changed",
            "workflow_changed",
        },
        "rehearsal record",
    )
    contributor_login = _github_login(record["contributor_login"])
    contributor_type = _bounded_text(record["contributor_type"], 16, "contributor type")
    if contributor_type != "human":
        raise RuntimeError("contributor rehearsal must identify a human contributor")
    independence_reviewed = _required_true(
        record["independence_reviewed"], "contributor independence"
    )
    issue_url = _project_reference_url(record["issue_url"], "issues", "issue URL")
    pull_request_url = _project_reference_url(
        record["pull_request_url"], "pull", "pull request URL"
    )
    base_commit = _git_oid(record["base_commit"], "base commit")
    head_commit = _git_oid(record["head_commit"], "head commit")
    merge_commit = _git_oid(record["merge_commit"], "merge commit")
    if len({base_commit, head_commit, merge_commit}) != 3:
        raise RuntimeError("contributor-rehearsal revisions must be distinct")
    patch_hash = _sha256_text(record["patch_sha256"], "contribution patch sha256")
    feedback_hash = _sha256_text(record["feedback_sha256"], "feedback sha256")
    if patch_hash == feedback_hash:
        raise RuntimeError("contributor-rehearsal artifact identities must be distinct")
    task_scope = _bounded_text(record["task_scope"], 32, "task scope")
    if task_scope not in _ALLOWED_TASK_SCOPES:
        raise RuntimeError("contributor-rehearsal task scope is not good-first compatible")
    validation_steps = tuple(
        _bounded_text(item, 64, "record validation step")
        for item in _list(record["validation_steps"], "record validation steps")
    )
    if validation_steps != required_validation_steps:
        raise RuntimeError("contributor-rehearsal validation steps are incomplete")
    outcome = _bounded_text(record["outcome"], 32, "contribution outcome")
    if outcome != "merged":
        raise RuntimeError("external contributor rehearsal must have merged")
    dco_valid = _required_true(record["dco_valid"], "DCO validation")
    private_knowledge_used = _required_false(
        record["private_maintainer_knowledge_used"], "private maintainer knowledge"
    )
    public_api_changed = _required_false(record["public_api_changed"], "public API change")
    persistent_format_changed = _required_false(
        record["persistent_format_changed"], "persistent format change"
    )
    dependency_changed = _required_false(record["dependency_changed"], "dependency change")
    workflow_changed = _required_false(record["workflow_changed"], "workflow change")
    return (
        contributor_login,
        contributor_type,
        independence_reviewed,
        issue_url,
        pull_request_url,
        base_commit,
        head_commit,
        merge_commit,
        patch_hash,
        feedback_hash,
        task_scope,
        validation_steps,
        outcome,
        dco_valid,
        private_knowledge_used,
        public_api_changed,
        persistent_format_changed,
        dependency_changed,
        workflow_changed,
    )


def _default_rehearsals() -> Path:
    bundled = Path(__file__).resolve().parent / "assets" / "external_contributor_rehearsal.json"
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
    try:
        return json.loads(value, object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"{role} is not valid JSON") from error


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
        raise TypeError("rehearsals must be a path")
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
    return login


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


def _required_true(value: object, role: str) -> bool:
    if type(value) is not bool or not value:
        raise RuntimeError(f"{role} must be explicitly true")
    return cast(bool, value)


def _required_false(value: object, role: str) -> bool:
    if type(value) is not bool or value:
        raise RuntimeError(f"{role} must be explicitly false")
    return cast(bool, value)


if __name__ == "__main__":
    raise SystemExit(main())
