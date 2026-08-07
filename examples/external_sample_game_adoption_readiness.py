"""Evaluate reviewed external sample-game adoption without inventing users."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from ludoweave import __version__

type _SampleGameIdentity = tuple[
    str,
    bool,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    tuple[str, ...],
    str,
    str,
    str,
    str,
    str,
    str,
    bool,
    bool,
    bool,
    bool,
    bool,
    bool,
]

_SCHEMA = "ludoweave.evaluation.external-sample-game-adoption-readiness/1"
_MANIFEST_SCHEMA = "ludoweave.adoption.external-sample-games/1"
_REQUIRED_CAPABILITIES = (
    "headless-fixed-tick",
    "typed-command-receipt",
    "verified-replay",
)
_ALLOWED_SAMPLE_SCOPES = ("2d-game", "layered-2d-game")
_REVIEWED_SAMPLE_GAME_SHA256 = "ecdd0be75e42f047037c6799205786079274eb6d73d788f81e1061acc82008dd"
_MANDATORY_SAMPLE_GAME_PREFIX: tuple[_SampleGameIdentity, ...] = ()
_MAX_MANIFEST_BYTES = 65_536
_MAX_SAMPLE_GAME_RECORDS = 32


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--samples",
        type=Path,
        default=None,
        help="explicit local external sample-game manifest",
    )
    arguments = parser.parse_args(tuple(sys.argv[1:] if argv is None else argv))
    samples_value: object = getattr(arguments, "samples", None)
    samples = _default_samples() if samples_value is None else _path(samples_value)
    print(
        json.dumps(
            evaluate(samples),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


def evaluate(samples: Path) -> dict[str, object]:
    """Return deterministic, sanitized external sample-game adoption evidence."""

    raw_manifest = _read_bounded(samples, _MAX_MANIFEST_BYTES, "sample-game manifest")
    document = _object(_loads(raw_manifest, "sample-game manifest"), "sample-game manifest")
    _exact_fields(
        document,
        {
            "schema",
            "source_project",
            "minimum_external_sample_games",
            "required_capabilities",
            "sample_game_records",
        },
        "sample-game manifest",
    )
    if document["schema"] != _MANIFEST_SCHEMA:
        raise RuntimeError("sample-game manifest schema is incompatible")
    if document["source_project"] != "ludoweave-engine":
        raise RuntimeError("sample-game manifest project identity is invalid")
    minimum = _positive_int(
        document["minimum_external_sample_games"], "minimum external sample games"
    )
    if minimum != 1:
        raise RuntimeError("sample-game minimum must remain one")
    capabilities = tuple(
        _bounded_text(item, 64, "required capability")
        for item in _list(document["required_capabilities"], "required capabilities")
    )
    if capabilities != _REQUIRED_CAPABILITIES:
        raise RuntimeError("sample-game required capabilities are incompatible")

    raw_records = _list(document["sample_game_records"], "sample-game records")
    if len(raw_records) > _MAX_SAMPLE_GAME_RECORDS:
        raise RuntimeError("sample-game manifest exceeds its record limit")
    identities: list[_SampleGameIdentity] = []
    game_slugs: set[str] = set()
    repositories: set[str] = set()
    revisions: set[str] = set()
    artifact_hashes: set[str] = set()
    evidence_locators: set[str] = set()
    for item in raw_records:
        identity = _sample_game_identity(_object(item, "sample-game record"), capabilities)
        if identity[3] in game_slugs:
            raise RuntimeError("sample-game manifest repeats a game slug")
        if identity[4] in repositories:
            raise RuntimeError("sample-game manifest repeats a repository")
        if identity[5] in revisions:
            raise RuntimeError("sample-game manifest repeats a revision identity")
        if identity[14] in evidence_locators:
            raise RuntimeError("sample-game manifest repeats an evidence locator")
        record_hashes = identity[11:14]
        if artifact_hashes.intersection(record_hashes):
            raise RuntimeError("sample-game manifest repeats an artifact identity")
        game_slugs.add(identity[3])
        repositories.add(identity[4])
        revisions.add(identity[5])
        artifact_hashes.update(record_hashes)
        evidence_locators.add(identity[14])
        identities.append(identity)

    manifest_hash = hashlib.sha256(raw_manifest).hexdigest()
    manifest_identity_reviewed = manifest_hash == _REVIEWED_SAMPLE_GAME_SHA256
    historical_sample_games_preserved = tuple(
        identities[: len(_MANDATORY_SAMPLE_GAME_PREFIX)]
    ) == _MANDATORY_SAMPLE_GAME_PREFIX and (
        not manifest_identity_reviewed or len(identities) == len(_MANDATORY_SAMPLE_GAME_PREFIX)
    )
    admitted_identities = (
        identities if manifest_identity_reviewed and historical_sample_games_preserved else []
    )
    admitted_authors = {identity[0] for identity in admitted_identities}
    admitted_versions = [identity[8] for identity in admitted_identities]
    admitted_scopes = [identity[6] for identity in admitted_identities]
    admitted_outcomes = [identity[10] for identity in admitted_identities]
    external_sample_game_present = len(admitted_identities) >= minimum
    gate_satisfied = (
        manifest_identity_reviewed
        and historical_sample_games_preserved
        and external_sample_game_present
    )
    reasons: list[str] = []
    if not manifest_identity_reviewed:
        reasons.append("sample-game-manifest-identity-unreviewed")
    if not historical_sample_games_preserved:
        reasons.append("historical-sample-game-record-missing")
    if not external_sample_game_present:
        reasons.append("external-sample-game-absent")

    return {
        "admission": {
            "external_sample_game_present": external_sample_game_present,
            "historical_sample_games_preserved": historical_sample_games_preserved,
            "manifest_identity_reviewed": manifest_identity_reviewed,
            "minimum_external_sample_games": minimum,
            "reason_codes": tuple(reasons),
        },
        "evidence_level": (
            "reviewed-external-sample-game-adoption"
            if gate_satisfied
            else "external-sample-game-adoption-readiness"
        ),
        "external_sample_game_adoption_proven": gate_satisfied,
        "gate_satisfied": gate_satisfied,
        "ludoweave_version": __version__,
        "sample_games": {
            "distinct_authors": len(admitted_authors),
            "game_count": len(admitted_identities),
            "manifest_sha256": manifest_hash,
            "observed_ludoweave_versions": tuple(dict.fromkeys(admitted_versions)),
            "outcomes": tuple(admitted_outcomes),
            "records_verified": True,
            "required_capabilities": capabilities,
            "sample_scopes": tuple(admitted_scopes),
        },
        "schema": _SCHEMA,
        "status": "ready" if gate_satisfied else "not-ready",
    }


def _sample_game_identity(
    record: dict[str, object], required_capabilities: tuple[str, ...]
) -> _SampleGameIdentity:
    _exact_fields(
        record,
        {
            "external_author_id",
            "authorship_reviewed",
            "relationship",
            "game_slug",
            "repository_url",
            "revision",
            "sample_scope",
            "engine_distribution",
            "ludoweave_version",
            "capabilities",
            "outcome",
            "source_sha256",
            "execution_sha256",
            "review_sha256",
            "evidence_locator",
            "license_spdx",
            "license_reviewed",
            "project_owned",
            "maintainer_authored",
            "independence_reviewed",
            "provenance_reviewed",
            "outcome_reviewed",
        },
        "sample-game record",
    )
    author_id = _safe_id(record["external_author_id"], "external author id")
    authorship_reviewed = _bool(record["authorship_reviewed"], "authorship reviewed")
    if not authorship_reviewed:
        raise RuntimeError("sample-game authorship must be explicitly reviewed")
    relationship = _bounded_text(record["relationship"], 32, "author relationship")
    if relationship != "independent-external":
        raise RuntimeError("sample-game author must be independent and external")
    game_slug = _safe_id(record["game_slug"], "game slug")
    repository = _https_locator(record["repository_url"], 256, "sample-game repository")
    revision = _git_oid(record["revision"], "sample-game revision")
    scope = _bounded_text(record["sample_scope"], 32, "sample-game scope")
    if scope not in _ALLOWED_SAMPLE_SCOPES:
        raise RuntimeError("sample-game scope is incompatible")
    distribution = _bounded_text(record["engine_distribution"], 32, "engine distribution")
    if distribution != "installed-wheel":
        raise RuntimeError("sample game must exercise an installed wheel")
    version = _version(record["ludoweave_version"])
    capabilities = tuple(
        _bounded_text(item, 64, "sample-game capability")
        for item in _list(record["capabilities"], "sample-game capabilities")
    )
    if capabilities != required_capabilities:
        raise RuntimeError("sample-game capability coverage is incomplete")
    outcome = _bounded_text(record["outcome"], 32, "sample-game outcome")
    if outcome != "validated":
        raise RuntimeError("sample-game outcome must be validated")
    source_hash = _sha256_text(record["source_sha256"], "sample-game source sha256")
    execution_hash = _sha256_text(record["execution_sha256"], "sample-game execution sha256")
    review_hash = _sha256_text(record["review_sha256"], "sample-game review sha256")
    if len({source_hash, execution_hash, review_hash}) != 3:
        raise RuntimeError("sample-game artifact identities must be distinct")
    locator = _immutable_https_locator(
        record["evidence_locator"],
        512,
        "sample-game evidence locator",
        (revision, source_hash, execution_hash, review_hash),
    )
    license_spdx = _spdx(record["license_spdx"])
    license_reviewed = _bool(record["license_reviewed"], "license reviewed")
    if not license_reviewed:
        raise RuntimeError("sample-game license must be explicitly reviewed")
    project_owned = _bool(record["project_owned"], "project owned")
    if project_owned:
        raise RuntimeError("project-owned games are not external sample games")
    maintainer_authored = _bool(record["maintainer_authored"], "maintainer authored")
    if maintainer_authored:
        raise RuntimeError("maintainer-authored games are not external sample games")
    independence_reviewed = _bool(record["independence_reviewed"], "independence reviewed")
    if not independence_reviewed:
        raise RuntimeError("sample-game independence must be explicitly reviewed")
    provenance_reviewed = _bool(record["provenance_reviewed"], "provenance reviewed")
    if not provenance_reviewed:
        raise RuntimeError("sample-game provenance must be explicitly reviewed")
    outcome_reviewed = _bool(record["outcome_reviewed"], "outcome reviewed")
    if not outcome_reviewed:
        raise RuntimeError("sample-game outcome must be explicitly reviewed")
    return (
        author_id,
        authorship_reviewed,
        relationship,
        game_slug,
        repository,
        revision,
        scope,
        distribution,
        version,
        capabilities,
        outcome,
        source_hash,
        execution_hash,
        review_hash,
        locator,
        license_spdx,
        license_reviewed,
        project_owned,
        maintainer_authored,
        independence_reviewed,
        provenance_reviewed,
        outcome_reviewed,
    )


def _default_samples() -> Path:
    bundled = Path(__file__).resolve().parent / "assets" / "external_sample_game_adoption.json"
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
            raise ValueError("duplicate object field")
        result[key] = value
    return result


def _exact_fields(value: dict[str, object], expected: set[str], role: str) -> None:
    if set(value) != expected:
        raise RuntimeError(f"{role} fields are incompatible")


def _path(value: object) -> Path:
    if not isinstance(value, Path):
        raise TypeError("samples must be a path")
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


def _bool(value: object, role: str) -> bool:
    if type(value) is not bool:
        raise RuntimeError(f"{role} must be a Boolean")
    return value


def _safe_id(value: object, role: str) -> str:
    text = _bounded_text(value, 64, role)
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789._-"
    if not text[0].isalnum() or not text.isascii() or any(char not in allowed for char in text):
        raise RuntimeError(f"{role} must be a lowercase safe identifier")
    return text


def _https_locator(value: object, maximum: int, role: str) -> str:
    text = _bounded_text(value, maximum, role)
    remainder = text.removeprefix("https://")
    authority = remainder.partition("/")[0]
    labels = authority.split(".")
    if (
        not text.startswith("https://")
        or not text.isascii()
        or any(character.isspace() for character in text)
        or "?" in text
        or "#" in text
        or "@" in authority
        or ":" in authority
        or "\\" in text
        or len(labels) < 2
        or not any(character.isalpha() for character in labels[-1])
        or any(
            not label
            or not label[0].isalnum()
            or not label[-1].isalnum()
            or any(
                character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
                for character in label
            )
            for label in labels
        )
    ):
        raise RuntimeError(f"{role} must be a bounded immutable HTTPS locator")
    return text


def _immutable_https_locator(
    value: object,
    maximum: int,
    role: str,
    immutable_identities: tuple[str, ...],
) -> str:
    text = _https_locator(value, maximum, role)
    path = text.removeprefix("https://").partition("/")[2]
    if not any(identity in path.split("/") for identity in immutable_identities):
        raise RuntimeError(f"{role} must contain a recorded immutable identity")
    return text


def _version(value: object) -> str:
    text = _bounded_text(value, 64, "ludoweave version")
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.+!-_"
    if any(character not in allowed for character in text):
        raise RuntimeError("ludoweave version is invalid")
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


def _spdx(value: object) -> str:
    text = _bounded_text(value, 64, "sample-game SPDX license")
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.+-"
    if (
        not text.isascii()
        or any(character not in allowed for character in text)
        or text in {"NONE", "NOASSERTION"}
    ):
        raise RuntimeError("sample-game SPDX license is invalid")
    return text


if __name__ == "__main__":
    raise SystemExit(main())
