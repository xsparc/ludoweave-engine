"""Evaluate reviewed external command/receipt feedback without inventing adoption."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from ludoweave import __version__
from ludoweave.world import COMMAND_PROTOCOL, RECEIPT_PROTOCOL, TRANSACTION_PROTOCOL

type _FeedbackIdentity = tuple[
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
]

_SCHEMA = "ludoweave.evaluation.external-consumer-feedback-readiness/1"
_CORPUS_SCHEMA = "ludoweave.compatibility.external-consumer-feedback/1"
_REQUIRED_PROTOCOLS = (COMMAND_PROTOCOL, TRANSACTION_PROTOCOL, RECEIPT_PROTOCOL)
_REVIEWED_FEEDBACK_CORPUS_SHA256 = (
    "b113444f60946461ec6774e2c278b9e82e7d80e08a37450b6cc153e5c5c1500e"
)
_MANDATORY_FEEDBACK_PREFIX: tuple[_FeedbackIdentity, ...] = ()
_MAX_MANIFEST_BYTES = 65_536
_MAX_FEEDBACK_RECORDS = 64
_ALLOWED_OUTCOMES = ("compatible", "issues-found")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corpus",
        type=Path,
        default=None,
        help="explicit local external-consumer feedback manifest",
    )
    arguments = parser.parse_args(tuple(sys.argv[1:] if argv is None else argv))
    corpus_value: object = getattr(arguments, "corpus", None)
    corpus = _default_corpus() if corpus_value is None else _path(corpus_value)
    print(
        json.dumps(
            evaluate(corpus),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


def evaluate(corpus: Path) -> dict[str, object]:
    """Return deterministic, path-free gate-2 admission readiness evidence."""

    raw_corpus = _read_bounded(corpus, _MAX_MANIFEST_BYTES, "feedback manifest")
    document = _object(_loads(raw_corpus, "feedback manifest"), "feedback manifest")
    _exact_fields(
        document,
        {
            "schema",
            "source_package",
            "minimum_independent_consumers",
            "required_protocols",
            "feedback_records",
        },
        "feedback manifest",
    )
    if document["schema"] != _CORPUS_SCHEMA:
        raise RuntimeError("external feedback corpus schema is incompatible")
    if document["source_package"] != "ludoweave":
        raise RuntimeError("external feedback corpus package identity is invalid")
    minimum = _positive_int(
        document["minimum_independent_consumers"], "minimum independent consumers"
    )
    if minimum != 1:
        raise RuntimeError("external feedback minimum must remain one consumer")
    protocols = tuple(
        _bounded_text(item, 64, "required protocol")
        for item in _list(document["required_protocols"], "required protocols")
    )
    if protocols != _REQUIRED_PROTOCOLS:
        raise RuntimeError("external feedback required protocols are incompatible")

    raw_records = _list(document["feedback_records"], "feedback records")
    if len(raw_records) > _MAX_FEEDBACK_RECORDS:
        raise RuntimeError("external feedback corpus exceeds its record limit")
    identities: list[_FeedbackIdentity] = []
    consumer_ids: set[str] = set()
    versions: list[str] = []
    outcomes: list[str] = []
    for item in raw_records:
        identity = _feedback_identity(_object(item, "feedback record"), protocols)
        consumer_id = identity[0]
        if consumer_id in consumer_ids:
            raise RuntimeError("external feedback corpus repeats a consumer")
        consumer_ids.add(consumer_id)
        identities.append(identity)
        versions.append(identity[5])
        outcomes.append(identity[7])

    corpus_hash = hashlib.sha256(raw_corpus).hexdigest()
    corpus_identity_reviewed = corpus_hash == _REVIEWED_FEEDBACK_CORPUS_SHA256
    historical_records_preserved = (
        tuple(identities[: len(_MANDATORY_FEEDBACK_PREFIX)]) == _MANDATORY_FEEDBACK_PREFIX
    )
    independent_consumer_feedback = len(consumer_ids) >= minimum
    gate_satisfied = (
        corpus_identity_reviewed and historical_records_preserved and independent_consumer_feedback
    )
    reasons: list[str] = []
    if not corpus_identity_reviewed:
        reasons.append("feedback-corpus-identity-unreviewed")
    if not historical_records_preserved:
        reasons.append("historical-feedback-record-missing")
    if not independent_consumer_feedback:
        reasons.append("external-consumer-feedback-absent")

    return {
        "admission": {
            "corpus_identity_reviewed": corpus_identity_reviewed,
            "historical_records_preserved": historical_records_preserved,
            "independent_consumer_feedback": independent_consumer_feedback,
            "minimum_independent_consumers": minimum,
            "reason_codes": tuple(reasons),
        },
        "corpus": {
            "distinct_consumers": len(consumer_ids),
            "feedback_count": len(identities),
            "manifest_sha256": corpus_hash,
            "observed_ludoweave_versions": tuple(dict.fromkeys(versions)),
            "outcomes": tuple(outcomes),
            "records_verified": True,
            "required_protocols": protocols,
        },
        "evidence_level": (
            "reviewed-external-consumer-feedback"
            if gate_satisfied
            else "external-consumer-feedback-admission-readiness"
        ),
        "external_feedback_proven": gate_satisfied,
        "gate_satisfied": gate_satisfied,
        "ludoweave_version": __version__,
        "schema": _SCHEMA,
        "status": "ready" if gate_satisfied else "not-ready",
    }


def _feedback_identity(
    record: dict[str, object], required_protocols: tuple[str, ...]
) -> _FeedbackIdentity:
    _exact_fields(
        record,
        {
            "consumer_id",
            "consumer_repository",
            "consumer_revision",
            "relationship",
            "evidence_kind",
            "ludoweave_version",
            "protocols",
            "outcome",
            "integration_sha256",
            "feedback_sha256",
            "evidence_locator",
        },
        "feedback record",
    )
    consumer_id = _consumer_id(record["consumer_id"])
    repository = _https_locator(record["consumer_repository"], 256, "consumer repository")
    revision = _git_oid(record["consumer_revision"], "consumer revision")
    relationship = _bounded_text(record["relationship"], 32, "consumer relationship")
    if relationship != "independent":
        raise RuntimeError("external feedback consumer must be independent")
    evidence_kind = _bounded_text(record["evidence_kind"], 64, "feedback evidence kind")
    if evidence_kind != "public-command-receipt-integration":
        raise RuntimeError("external feedback evidence kind is incompatible")
    version = _version(record["ludoweave_version"])
    protocols = tuple(
        _bounded_text(item, 64, "feedback protocol")
        for item in _list(record["protocols"], "feedback protocols")
    )
    if protocols != required_protocols:
        raise RuntimeError("external feedback protocol coverage is incomplete")
    outcome = _bounded_text(record["outcome"], 32, "feedback outcome")
    if outcome not in _ALLOWED_OUTCOMES:
        raise RuntimeError("external feedback outcome is invalid")
    integration_hash = _sha256_text(record["integration_sha256"], "integration sha256")
    feedback_hash = _sha256_text(record["feedback_sha256"], "feedback sha256")
    locator = _https_locator(record["evidence_locator"], 512, "feedback evidence locator")
    return (
        consumer_id,
        repository,
        revision,
        relationship,
        evidence_kind,
        version,
        protocols,
        outcome,
        integration_hash,
        feedback_hash,
        locator,
    )


def _default_corpus() -> Path:
    bundled = Path(__file__).resolve().parent / "assets" / "external_consumer_feedback.json"
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
        return json.loads(value)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{role} is not valid JSON") from error


def _exact_fields(value: dict[str, object], expected: set[str], role: str) -> None:
    if set(value) != expected:
        raise RuntimeError(f"{role} fields are incompatible")


def _path(value: object) -> Path:
    if not isinstance(value, Path):
        raise TypeError("corpus must be a path")
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


def _consumer_id(value: object) -> str:
    text = _bounded_text(value, 64, "consumer id")
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789._-"
    if not text[0].isalnum() or not text.isascii() or any(char not in allowed for char in text):
        raise RuntimeError("consumer id must be a lowercase safe identifier")
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


if __name__ == "__main__":
    raise SystemExit(main())
