"""Audit preserved receipts without claiming missing cross-version history."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from ludoweave import __version__
from ludoweave.world import RECEIPT_PROTOCOL, TransactionReceipt

_SCHEMA = "ludoweave.evaluation.cross-version-receipt-corpus/1"
_CORPUS_SCHEMA = "ludoweave.compatibility.cross-version-receipt-corpus/1"
_SOURCE_SCHEMA = "ludoweave.compatibility.receipt-corpus/1"
_REVIEWED_CORPUS_SHA256 = "0b1d7b9f68b49ad1f6ab21cff4f744140cf3a16b52c6cdebd691b28b375a72ae"
_MANDATORY_SOURCE_PREFIX = (
    (
        "receipt_v1",
        "0.1.0a1",
        762,
        "ed3f1040294376fafce523e129897ce756d785b2f6d90c54335ad5f8abb84ac3",
    ),
)
_MANDATORY_RELEASE_PREFIX: tuple[tuple[str, str, str, str], ...] = ()
_MAX_MANIFEST_BYTES = 65_536
_MAX_SOURCE_MANIFESTS = 16
_MAX_FIXTURES_PER_MANIFEST = 64
_MAX_RECEIPT_BYTES = 1_048_576
_MAX_SUPPORTED_RELEASES = 32
_EXPECTED_STATUSES = ("committed", "dry_run", "rejected")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corpus",
        type=Path,
        default=None,
        help="explicit local cross-version corpus manifest",
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
    """Return deterministic, path-free admission evidence for one local corpus."""

    raw_corpus = _read_bounded(corpus, _MAX_MANIFEST_BYTES, "corpus manifest")
    document = _object(_loads(raw_corpus, "corpus manifest"), "corpus manifest")
    _exact_fields(
        document,
        {
            "schema",
            "source_package",
            "receipt_protocol",
            "minimum_distinct_observed_versions",
            "source_manifests",
            "supported_releases",
        },
        "corpus manifest",
    )
    if document["schema"] != _CORPUS_SCHEMA:
        raise RuntimeError("cross-version corpus schema is incompatible")
    if document["source_package"] != "ludoweave":
        raise RuntimeError("cross-version corpus package identity is invalid")
    if document["receipt_protocol"] != RECEIPT_PROTOCOL:
        raise RuntimeError("cross-version corpus receipt protocol is incompatible")
    minimum = _positive_int(
        document["minimum_distinct_observed_versions"],
        "minimum distinct observed versions",
    )
    if minimum != 2:
        raise RuntimeError("cross-version corpus minimum must remain two versions")

    source_entries = _list(document["source_manifests"], "source manifests")
    if not source_entries:
        raise RuntimeError("cross-version corpus must preserve a source manifest")
    if len(source_entries) > _MAX_SOURCE_MANIFESTS:
        raise RuntimeError("cross-version corpus exceeds its source-manifest limit")
    source_identities: list[tuple[str, str, int, str]] = []
    statuses: list[str] = []
    fixture_count = 0
    for item in source_entries:
        entry = _object(item, "source manifest entry")
        identity, entry_statuses, count = _audit_source_manifest(corpus.parent, entry)
        if any(previous[1] == identity[1] for previous in source_identities):
            raise RuntimeError("cross-version corpus repeats a source version")
        source_identities.append(identity)
        statuses.extend(entry_statuses)
        fixture_count += count

    corpus_hash = hashlib.sha256(raw_corpus).hexdigest()
    corpus_identity_reviewed = corpus_hash == _REVIEWED_CORPUS_SHA256
    source_versions = tuple(identity[1] for identity in source_identities)
    source_history_preserved = (
        tuple(source_identities[: len(_MANDATORY_SOURCE_PREFIX)]) == _MANDATORY_SOURCE_PREFIX
    )
    release_identities = _release_identities(document["supported_releases"])
    releases = tuple(identity[0] for identity in release_identities)
    release_history_preserved = (
        tuple(release_identities[: len(_MANDATORY_RELEASE_PREFIX)]) == _MANDATORY_RELEASE_PREFIX
    )
    historical_entries_preserved = source_history_preserved and release_history_preserved
    observed_versions = tuple(dict.fromkeys((*source_versions, __version__)))
    required_release_versions = set(observed_versions)
    release_evidence_complete = required_release_versions == set(releases)
    reader_differs_from_source = any(version != __version__ for version in source_versions)
    cross_version_execution = len(observed_versions) >= minimum and reader_differs_from_source
    gate_satisfied = (
        corpus_identity_reviewed
        and historical_entries_preserved
        and cross_version_execution
        and release_evidence_complete
    )
    reasons: list[str] = []
    if not corpus_identity_reviewed:
        reasons.append("corpus-identity-unreviewed")
    if not historical_entries_preserved:
        reasons.append("historical-corpus-entry-missing")
    if not cross_version_execution:
        reasons.append("cross-version-execution-absent")
    if not release_evidence_complete:
        reasons.append("supported-release-evidence-incomplete")

    return {
        "admission": {
            "corpus_identity_reviewed": corpus_identity_reviewed,
            "cross_version_execution": cross_version_execution,
            "historical_entries_preserved": historical_entries_preserved,
            "minimum_distinct_observed_versions": minimum,
            "reason_codes": tuple(reasons),
            "reader_differs_from_source": reader_differs_from_source,
            "supported_release_evidence_complete": release_evidence_complete,
        },
        "corpus": {
            "canonical_round_trip": True,
            "distinct_observed_versions": len(observed_versions),
            "fixture_count": fixture_count,
            "manifest_sha256": corpus_hash,
            "manifests_verified": True,
            "observed_versions": observed_versions,
            "source_versions": tuple(source_versions),
            "statuses": tuple(statuses),
        },
        "cross_version_proven": gate_satisfied,
        "evidence_level": (
            "cross-version-supported-release-evidence"
            if gate_satisfied
            else "single-version-admission-readiness"
        ),
        "gate_satisfied": gate_satisfied,
        "ludoweave_version": __version__,
        "receipt_protocol": RECEIPT_PROTOCOL,
        "schema": _SCHEMA,
        "status": "ready" if gate_satisfied else "not-ready",
        "supported_release_versions": releases,
    }


def _audit_source_manifest(
    root: Path, entry: dict[str, object]
) -> tuple[tuple[str, str, int, str], tuple[str, ...], int]:
    _exact_fields(
        entry,
        {"directory", "source_version", "bytes", "sha256"},
        "source manifest entry",
    )
    directory = _basename(entry["directory"], "source manifest directory")
    expected_version = _text(entry["source_version"], "source version")
    expected_bytes = _bounded_positive_int(
        entry["bytes"], _MAX_MANIFEST_BYTES, "source manifest bytes"
    )
    expected_hash = _sha256_text(entry["sha256"], "source manifest sha256")
    source_root = root / directory
    try:
        resolved_root = root.resolve(strict=True)
        resolved_source = source_root.resolve(strict=True)
    except OSError as error:
        raise RuntimeError("source manifest directory is unavailable") from error
    if source_root.is_symlink() or resolved_source.parent != resolved_root:
        raise RuntimeError("source manifest directory escapes the corpus")
    raw_manifest = _read_bounded(
        source_root / "manifest.json", _MAX_MANIFEST_BYTES, "source manifest"
    )
    if (
        len(raw_manifest) != expected_bytes
        or hashlib.sha256(raw_manifest).hexdigest() != expected_hash
    ):
        raise RuntimeError("source manifest identity does not match the corpus")
    manifest = _object(_loads(raw_manifest, "source manifest"), "source manifest")
    _exact_fields(
        manifest,
        {
            "schema",
            "source_package",
            "source_version",
            "receipt_protocol",
            "evidence_level",
            "fixtures",
        },
        "source manifest",
    )
    if (
        manifest["schema"] != _SOURCE_SCHEMA
        or manifest["source_package"] != "ludoweave"
        or manifest["source_version"] != expected_version
        or manifest["receipt_protocol"] != RECEIPT_PROTOCOL
        or manifest["evidence_level"] != "single-version-baseline"
    ):
        raise RuntimeError("source manifest compatibility identity is invalid")
    fixtures = _list(manifest["fixtures"], "source fixtures")
    if not fixtures or len(fixtures) > _MAX_FIXTURES_PER_MANIFEST:
        raise RuntimeError("source manifest fixture count is outside its limit")
    statuses: list[str] = []
    seen_files: set[str] = set()
    for item in fixtures:
        fixture = _object(item, "source fixture")
        _exact_fields(fixture, {"file", "status", "bytes", "sha256"}, "source fixture")
        filename = _basename(fixture["file"], "source fixture file")
        if filename in seen_files:
            raise RuntimeError("source manifest repeats a fixture file")
        seen_files.add(filename)
        status = _text(fixture["status"], "source fixture status")
        size = _bounded_positive_int(fixture["bytes"], _MAX_RECEIPT_BYTES, "source fixture bytes")
        digest = _sha256_text(fixture["sha256"], "source fixture sha256")
        raw = _read_bounded(source_root / filename, size, "source fixture")
        if len(raw) != size or hashlib.sha256(raw).hexdigest() != digest:
            raise RuntimeError("source fixture identity does not match its manifest")
        receipt = TransactionReceipt.from_json(raw)
        if receipt.status.value != status or receipt.canonical_bytes() != raw.rstrip(b"\r\n"):
            raise RuntimeError("installed reader changed historical receipt behavior")
        statuses.append(status)
    if tuple(statuses) != _EXPECTED_STATUSES:
        raise RuntimeError("source fixture status coverage is incomplete")
    identity = (directory, expected_version, expected_bytes, expected_hash)
    return identity, tuple(statuses), len(fixtures)


def _release_identities(value: object) -> tuple[tuple[str, str, str, str], ...]:
    releases = _list(value, "supported releases")
    if len(releases) > _MAX_SUPPORTED_RELEASES:
        raise RuntimeError("cross-version corpus exceeds its supported-release limit")
    identities: list[tuple[str, str, str, str]] = []
    for item in releases:
        release = _object(item, "supported release")
        _exact_fields(
            release,
            {"version", "tag", "commit", "artifact_sha256"},
            "supported release",
        )
        version = _text(release["version"], "supported release version")
        tag = _text(release["tag"], "supported release tag")
        commit = _git_oid(release["commit"], "supported release commit")
        artifact = _sha256_text(release["artifact_sha256"], "supported release artifact sha256")
        if tag != f"v{version}" or any(previous[0] == version for previous in identities):
            raise RuntimeError("supported release evidence is invalid")
        identities.append((version, tag, commit, artifact))
    return tuple(identities)


def _default_corpus() -> Path:
    bundled = Path(__file__).resolve().parent / "assets" / "cross_version_receipt_corpus.json"
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
    return value.resolve()


def _object(value: object, role: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise RuntimeError(f"{role} must be an object")
    return cast(dict[str, object], value)


def _list(value: object, role: str) -> list[object]:
    if not isinstance(value, list):
        raise RuntimeError(f"{role} must be a list")
    return cast(list[object], value)


def _text(value: object, role: str) -> str:
    if not isinstance(value, str) or not value:
        raise RuntimeError(f"{role} must be non-empty text")
    return value


def _basename(value: object, role: str) -> str:
    name = _text(value, role)
    if Path(name).name != name or name in {".", ".."} or "\\" in name:
        raise RuntimeError(f"{role} must be a safe basename")
    return name


def _positive_int(value: object, role: str) -> int:
    if type(value) is not int or value <= 0:
        raise RuntimeError(f"{role} must be a positive integer")
    return value


def _bounded_positive_int(value: object, maximum: int, role: str) -> int:
    result = _positive_int(value, role)
    if result > maximum:
        raise RuntimeError(f"{role} exceeds its limit")
    return result


def _sha256_text(value: object, role: str) -> str:
    text = _text(value, role)
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise RuntimeError(f"{role} must be lowercase SHA-256")
    return text


def _git_oid(value: object, role: str) -> str:
    text = _text(value, role)
    if len(text) not in {40, 64} or any(character not in "0123456789abcdef" for character in text):
        raise RuntimeError(f"{role} must be a lowercase Git object identity")
    return text


if __name__ == "__main__":
    raise SystemExit(main())
