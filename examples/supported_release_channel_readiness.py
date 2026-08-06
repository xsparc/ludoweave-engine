"""Evaluate reviewed deprecation-capable release-channel evidence offline."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from ludoweave import __version__

type _ReleaseIdentity = tuple[
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
]

_SCHEMA = "ludoweave.evaluation.supported-release-channel-readiness/1"
_CORPUS_SCHEMA = "ludoweave.compatibility.supported-release-channel/1"
_REQUIRED_PUBLICATION_CHANNELS = ("github-release",)
_REVIEWED_RELEASE_CHANNEL_SHA256 = (
    "f23b4314696384ad288b86c63bc101606f1aa9f323c4fb186486d8c74915ec41"
)
_MANDATORY_RELEASE_PREFIX: tuple[_ReleaseIdentity, ...] = ()
_MAX_MANIFEST_BYTES = 65_536
_MAX_RELEASE_RECORDS = 64


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--channel",
        type=Path,
        default=None,
        help="explicit local reviewed release-channel manifest",
    )
    arguments = parser.parse_args(tuple(sys.argv[1:] if argv is None else argv))
    channel_value: object = getattr(arguments, "channel", None)
    channel = _default_channel() if channel_value is None else _path(channel_value)
    print(
        json.dumps(
            evaluate(channel),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


def evaluate(channel: Path) -> dict[str, object]:
    """Return deterministic, path-free RFC-0003 gate-6 readiness evidence."""

    raw_channel = _read_bounded(channel, _MAX_MANIFEST_BYTES, "release-channel manifest")
    document = _object(_loads(raw_channel, "release-channel manifest"), "release manifest")
    _exact_fields(
        document,
        {
            "schema",
            "source_package",
            "minimum_supported_feature_releases",
            "deprecation_window_feature_releases",
            "required_publication_channels",
            "release_records",
        },
        "release-channel manifest",
    )
    if document["schema"] != _CORPUS_SCHEMA:
        raise RuntimeError("release-channel manifest schema is incompatible")
    if document["source_package"] != "ludoweave":
        raise RuntimeError("release-channel package identity is invalid")
    minimum = _positive_int(
        document["minimum_supported_feature_releases"],
        "minimum supported feature releases",
    )
    if minimum != 2:
        raise RuntimeError("release-channel minimum must remain two feature releases")
    deprecation_window = _positive_int(
        document["deprecation_window_feature_releases"],
        "deprecation window feature releases",
    )
    if deprecation_window != 1:
        raise RuntimeError("release-channel deprecation window must remain one feature release")
    channels = tuple(
        _bounded_text(item, 64, "publication channel")
        for item in _list(
            document["required_publication_channels"], "required publication channels"
        )
    )
    if channels != _REQUIRED_PUBLICATION_CHANNELS:
        raise RuntimeError("release-channel publication channels are incompatible")

    raw_records = _list(document["release_records"], "release records")
    if len(raw_records) > _MAX_RELEASE_RECORDS:
        raise RuntimeError("release-channel manifest exceeds its record limit")
    identities: list[_ReleaseIdentity] = []
    semantic_versions: list[tuple[int, int, int]] = []
    seen_versions: set[str] = set()
    seen_tags: set[str] = set()
    seen_commits: set[str] = set()
    seen_urls: set[str] = set()
    seen_artifacts: set[str] = set()
    for item in raw_records:
        identity, semantic_version = _release_identity(_object(item, "release record"), channels)
        if identity[0] in seen_versions or identity[1] in seen_tags:
            raise RuntimeError("release-channel manifest repeats a version or tag")
        if identity[2] in seen_commits or identity[3] in seen_urls or identity[4] in seen_artifacts:
            raise RuntimeError("release-channel manifest repeats a publication identity")
        seen_versions.add(identity[0])
        seen_tags.add(identity[1])
        seen_commits.add(identity[2])
        seen_urls.add(identity[3])
        seen_artifacts.add(identity[4])
        identities.append(identity)
        semantic_versions.append(semantic_version)
    if semantic_versions != sorted(semantic_versions):
        raise RuntimeError("release-channel feature releases must be strictly increasing")

    channel_hash = hashlib.sha256(raw_channel).hexdigest()
    channel_identity_reviewed = channel_hash == _REVIEWED_RELEASE_CHANNEL_SHA256
    historical_releases_preserved = tuple(
        identities[: len(_MANDATORY_RELEASE_PREFIX)]
    ) == _MANDATORY_RELEASE_PREFIX and (
        not channel_identity_reviewed or len(identities) == len(_MANDATORY_RELEASE_PREFIX)
    )
    feature_lines = tuple(dict.fromkeys((major, minor) for major, minor, _ in semantic_versions))
    supported_feature_release_channel = len(identities) >= minimum and len(feature_lines) >= minimum
    gate_satisfied = (
        channel_identity_reviewed
        and historical_releases_preserved
        and supported_feature_release_channel
    )
    reasons: list[str] = []
    if not channel_identity_reviewed:
        reasons.append("release-channel-identity-unreviewed")
    if not historical_releases_preserved:
        reasons.append("historical-release-record-missing")
    if not supported_feature_release_channel:
        reasons.append("supported-feature-release-channel-absent")

    return {
        "admission": {
            "channel_identity_reviewed": channel_identity_reviewed,
            "deprecation_window_feature_releases": deprecation_window,
            "historical_releases_preserved": historical_releases_preserved,
            "minimum_supported_feature_releases": minimum,
            "reason_codes": tuple(reasons),
            "supported_feature_release_channel": supported_feature_release_channel,
        },
        "channel": {
            "distinct_feature_lines": len(feature_lines),
            "feature_release_count": len(identities),
            "manifest_sha256": channel_hash,
            "publication_channels": channels,
            "records_verified": True,
            "versions": tuple(identity[0] for identity in identities),
        },
        "evidence_level": (
            "reviewed-supported-release-channel"
            if gate_satisfied
            else "supported-release-channel-admission-readiness"
        ),
        "gate_satisfied": gate_satisfied,
        "ludoweave_version": __version__,
        "schema": _SCHEMA,
        "status": "ready" if gate_satisfied else "not-ready",
        "supported_deprecation_release_channel_proven": gate_satisfied,
    }


def _release_identity(
    record: dict[str, object], required_channels: tuple[str, ...]
) -> tuple[_ReleaseIdentity, tuple[int, int, int]]:
    _exact_fields(
        record,
        {
            "version",
            "tag",
            "commit",
            "release_url",
            "artifact_sha256",
            "release_notes_sha256",
            "publication_channels",
            "support_status",
            "yanked",
            "draft",
            "prerelease",
        },
        "release record",
    )
    version, semantic_version = _final_feature_version(record["version"])
    tag = _bounded_text(record["tag"], 72, "release tag")
    if tag != f"v{version}":
        raise RuntimeError("release tag must exactly match its version")
    commit = _git_oid(record["commit"], "release commit")
    release_url = _https_locator(record["release_url"], 512, "release URL")
    if release_url != f"https://github.com/xsparc/ludoweave-engine/releases/tag/{tag}":
        raise RuntimeError("release URL must exactly identify the project tag")
    artifact_hash = _sha256_text(record["artifact_sha256"], "release artifact sha256")
    notes_hash = _sha256_text(record["release_notes_sha256"], "release notes sha256")
    channels = tuple(
        _bounded_text(item, 64, "release publication channel")
        for item in _list(record["publication_channels"], "release publication channels")
    )
    if channels != required_channels:
        raise RuntimeError("release publication channels are incomplete")
    support_status = _bounded_text(record["support_status"], 32, "release support status")
    if support_status != "supported":
        raise RuntimeError("release record must be supported")
    yanked = record["yanked"]
    if type(yanked) is not bool or yanked:
        raise RuntimeError("release record must be explicitly non-yanked")
    draft = record["draft"]
    if type(draft) is not bool or draft:
        raise RuntimeError("release record must be explicitly non-draft")
    prerelease = record["prerelease"]
    if type(prerelease) is not bool or prerelease:
        raise RuntimeError("release record must be explicitly final")
    return (
        (
            version,
            tag,
            commit,
            release_url,
            artifact_hash,
            notes_hash,
            channels,
            support_status,
            yanked,
            draft,
            prerelease,
        ),
        semantic_version,
    )


def _default_channel() -> Path:
    bundled = Path(__file__).resolve().parent / "assets" / "supported_release_channel.json"
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
        raise TypeError("channel must be a path")
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


def _final_feature_version(value: object) -> tuple[str, tuple[int, int, int]]:
    text = _bounded_text(value, 64, "feature release version")
    parts = text.split(".")
    if (
        len(parts) != 3
        or any(not part.isascii() or not part.isdecimal() for part in parts)
        or any(len(part) > 1 and part.startswith("0") for part in parts)
    ):
        raise RuntimeError("feature release version must be final MAJOR.MINOR.PATCH")
    semantic_version = tuple(int(part) for part in parts)
    return text, cast(tuple[int, int, int], semantic_version)


def _https_locator(value: object, maximum: int, role: str) -> str:
    text = _bounded_text(value, maximum, role)
    remainder = text.removeprefix("https://")
    authority, separator, path = remainder.partition("/")
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
        or separator != "/"
        or not path
        or any(segment in {"", ".", ".."} for segment in path.split("/"))
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
        raise RuntimeError(f"{role} must be a bounded public HTTPS locator")
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
