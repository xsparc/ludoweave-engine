"""Fail closed unless a GitHub draft exactly matches staged notes and assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

_PROTOCOL = "ludoweave.release-draft-integrity/2"
_MAX_DOCUMENT_BYTES = 4 * 1024 * 1024
_MAX_ASSETS = 32
_MAX_ASSET_BYTES = 256 * 1024 * 1024
_MAX_TOTAL_BYTES = 512 * 1024 * 1024
_MAX_RELEASE_NOTES_BYTES = 256 * 1024
_RELEASE_NOTES_NAME = "RELEASE_NOTES.md"
_TAG_PATTERN = re.compile(r"v[0-9A-Za-z][0-9A-Za-z._-]{0,127}")
_NAME_PATTERN = re.compile(r"[0-9A-Za-z][0-9A-Za-z._+-]{0,255}")
_DIGEST_PATTERN = re.compile(r"sha256:[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class ReleaseAssetIdentity:
    """Safe local/remote identity for one staged release asset."""

    name: str
    bytes: int
    sha256: str


class ReleaseDraftIntegrityError(ValueError):
    """A draft release cannot be trusted for publication."""

    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code


def verify_release_draft(
    staged_directory: Path,
    release_document: object,
    *,
    expected_tag: str,
    expected_title: str,
) -> tuple[ReleaseAssetIdentity, ...]:
    """Return asset identities when remote notes and assets match local staging."""

    tag = _tag_name(expected_tag)
    title = _title(expected_title)
    root = _directory(staged_directory)
    notes = _release_notes(root / _RELEASE_NOTES_NAME)
    local = _local_assets(root)
    release = _object(release_document, field="release document")

    if release.get("tag_name") != tag or release.get("name") != title:
        raise ReleaseDraftIntegrityError(
            "draft release identity does not match the expected tag and title",
            code="release_draft.identity_mismatch",
        )
    if (
        release.get("draft") is not True
        or release.get("prerelease") is not True
        or release.get("immutable") is not False
    ):
        raise ReleaseDraftIntegrityError(
            "release must remain a mutable prerelease draft during asset verification",
            code="release_draft.invalid_state",
        )
    if release.get("body") != notes:
        raise ReleaseDraftIntegrityError(
            "draft release notes do not exactly match local staging",
            code="release_draft.notes_mismatch",
        )

    assets_value = release.get("assets")
    if not isinstance(assets_value, list):
        raise ReleaseDraftIntegrityError(
            "release assets must be a bounded JSON array",
            code="release_draft.invalid_document",
        )
    assets = cast(list[object], assets_value)
    if len(assets) > _MAX_ASSETS:
        raise ReleaseDraftIntegrityError(
            "release assets must be a bounded JSON array",
            code="release_draft.invalid_document",
        )
    remote: dict[str, ReleaseAssetIdentity] = {}
    for value in assets:
        asset = _object(value, field="release asset")
        name = _asset_name(asset.get("name"))
        if name in remote:
            raise ReleaseDraftIntegrityError(
                "draft release contains a duplicate asset name",
                code="release_draft.invalid_document",
            )
        size = _asset_size(asset.get("size"))
        digest = _asset_digest(asset.get("digest"))
        if asset.get("state") != "uploaded":
            raise ReleaseDraftIntegrityError(
                f"draft release asset is not completely uploaded: {name}",
                code="release_draft.asset_mismatch",
            )
        remote[name] = ReleaseAssetIdentity(name, size, digest.removeprefix("sha256:"))

    if remote.keys() != local.keys():
        raise ReleaseDraftIntegrityError(
            "draft release and local staging contain different asset names",
            code="release_draft.asset_set_mismatch",
        )
    for name, identity in local.items():
        if remote[name] != identity:
            raise ReleaseDraftIntegrityError(
                f"draft release asset does not match local staging: {name}",
                code="release_draft.asset_mismatch",
            )
    return tuple(local.values())


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("staged_directory", type=Path, help="local staged release directory")
    parser.add_argument("release_document", type=Path, help="GitHub draft release JSON document")
    parser.add_argument("--expected-tag", required=True, help="exact vVERSION release tag")
    parser.add_argument("--expected-title", required=True, help="exact release title")
    args = parser.parse_args(argv)
    try:
        assets = verify_release_draft(
            Path(args.staged_directory),
            _json_document(Path(args.release_document)),
            expected_tag=str(args.expected_tag),
            expected_title=str(args.expected_title),
        )
    except ReleaseDraftIntegrityError as error:
        print(
            _json(
                {
                    "protocol": _PROTOCOL,
                    "status": "fail",
                    "code": error.code,
                    "message": str(error),
                }
            ),
            file=sys.stderr,
        )
        return 1
    print(
        _json(
            {
                "protocol": _PROTOCOL,
                "status": "pass",
                "tag": str(args.expected_tag),
                "assets": [
                    {"name": item.name, "bytes": item.bytes, "sha256": item.sha256}
                    for item in assets
                ],
            }
        )
    )
    return 0


def _directory(value: Path) -> Path:
    try:
        if value.is_symlink():
            raise OSError
        resolved = value.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise ReleaseDraftIntegrityError(
            "staged release directory is unavailable",
            code="release_draft.invalid_directory",
        ) from error
    if not resolved.is_dir():
        raise ReleaseDraftIntegrityError(
            "staged release path must be a directory",
            code="release_draft.invalid_directory",
        )
    return resolved


def _local_assets(root: Path) -> dict[str, ReleaseAssetIdentity]:
    try:
        entries = sorted(root.iterdir(), key=lambda path: path.name)
    except OSError as error:
        raise ReleaseDraftIntegrityError(
            "staged release directory could not be read",
            code="release_draft.read_failed",
        ) from error
    if not entries or len(entries) > _MAX_ASSETS:
        raise ReleaseDraftIntegrityError(
            "staged release must contain a bounded non-empty asset set",
            code="release_draft.invalid_asset_set",
        )

    total = 0
    result: dict[str, ReleaseAssetIdentity] = {}
    for path in entries:
        name = _asset_name(path.name)
        if path.is_symlink() or not path.is_file():
            raise ReleaseDraftIntegrityError(
                f"staged release contains a non-file entry: {name}",
                code="release_draft.invalid_entry",
            )
        try:
            size_hint = path.stat().st_size
        except OSError as error:
            raise ReleaseDraftIntegrityError(
                f"staged release asset could not be inspected: {name}",
                code="release_draft.read_failed",
            ) from error
        if size_hint > _MAX_ASSET_BYTES:
            raise ReleaseDraftIntegrityError(
                f"staged release asset exceeds the size limit: {name}",
                code="release_draft.size_limit",
            )
        size, digest = _digest(path)
        total += size
        if total > _MAX_TOTAL_BYTES:
            raise ReleaseDraftIntegrityError(
                "staged release exceeds the total size limit",
                code="release_draft.size_limit",
            )
        result[name] = ReleaseAssetIdentity(name, size, digest)
    return result


def _digest(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    try:
        with path.open("rb") as stream:
            while block := stream.read(1024 * 1024):
                size += len(block)
                if size > _MAX_ASSET_BYTES:
                    raise ReleaseDraftIntegrityError(
                        f"staged release asset exceeds the size limit: {path.name}",
                        code="release_draft.size_limit",
                    )
                digest.update(block)
    except OSError as error:
        raise ReleaseDraftIntegrityError(
            f"staged release asset could not be read: {path.name}",
            code="release_draft.read_failed",
        ) from error
    return size, digest.hexdigest()


def _json_document(path: Path) -> object:
    try:
        if path.is_symlink() or not path.is_file():
            raise OSError
        with path.open("rb") as stream:
            raw = stream.read(_MAX_DOCUMENT_BYTES + 1)
    except OSError as error:
        raise ReleaseDraftIntegrityError(
            "draft release document is unavailable",
            code="release_draft.invalid_document",
        ) from error
    if len(raw) > _MAX_DOCUMENT_BYTES:
        raise ReleaseDraftIntegrityError(
            "draft release document exceeds the size limit",
            code="release_draft.invalid_document",
        )
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    except ReleaseDraftIntegrityError:
        raise
    except (UnicodeDecodeError, RecursionError, ValueError) as error:
        raise ReleaseDraftIntegrityError(
            "draft release document is not strict UTF-8 JSON",
            code="release_draft.invalid_document",
        ) from error


def _release_notes(path: Path) -> str:
    try:
        if path.is_symlink() or not path.is_file():
            raise OSError
        with path.open("rb") as stream:
            raw = stream.read(_MAX_RELEASE_NOTES_BYTES + 1)
    except OSError as error:
        raise ReleaseDraftIntegrityError(
            "staged release notes are unavailable",
            code="release_draft.invalid_notes",
        ) from error
    if len(raw) > _MAX_RELEASE_NOTES_BYTES:
        raise ReleaseDraftIntegrityError(
            "staged release notes exceed the size limit",
            code="release_draft.invalid_notes",
        )
    try:
        notes = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ReleaseDraftIntegrityError(
            "staged release notes are not strict UTF-8",
            code="release_draft.invalid_notes",
        ) from error
    if not notes or "\x00" in notes:
        raise ReleaseDraftIntegrityError(
            "staged release notes must contain bounded text",
            code="release_draft.invalid_notes",
        )
    return notes


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ReleaseDraftIntegrityError(
                "draft release JSON contains a duplicate object key",
                code="release_draft.invalid_document",
            )
        result[key] = value
    return result


def _object(value: object, *, field: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ReleaseDraftIntegrityError(
            f"{field} must be a JSON object",
            code="release_draft.invalid_document",
        )
    document = cast(dict[object, object], value)
    if not all(isinstance(key, str) for key in document):
        raise ReleaseDraftIntegrityError(
            f"{field} must use string keys",
            code="release_draft.invalid_document",
        )
    return cast(dict[str, object], document)


def _tag_name(value: object) -> str:
    if not isinstance(value, str) or _TAG_PATTERN.fullmatch(value) is None:
        raise ReleaseDraftIntegrityError(
            "expected release tag is invalid",
            code="release_draft.invalid_identity",
        )
    return value


def _title(value: object) -> str:
    if (
        not isinstance(value, str)
        or not value.strip()
        or len(value) > 200
        or any(ord(character) < 32 for character in value)
    ):
        raise ReleaseDraftIntegrityError(
            "expected release title is invalid",
            code="release_draft.invalid_identity",
        )
    return value


def _asset_name(value: object) -> str:
    if not isinstance(value, str) or _NAME_PATTERN.fullmatch(value) is None:
        raise ReleaseDraftIntegrityError(
            "release asset name is invalid",
            code="release_draft.invalid_document",
        )
    return value


def _asset_size(value: object) -> int:
    if type(value) is not int or value < 0 or value > _MAX_ASSET_BYTES:
        raise ReleaseDraftIntegrityError(
            "release asset size is invalid",
            code="release_draft.invalid_document",
        )
    return value


def _asset_digest(value: object) -> str:
    if not isinstance(value, str) or _DIGEST_PATTERN.fullmatch(value) is None:
        raise ReleaseDraftIntegrityError(
            "release asset digest is not an exact SHA-256 identity",
            code="release_draft.invalid_document",
        )
    return value


def _json(value: object) -> str:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")
    )


if __name__ == "__main__":
    raise SystemExit(main())
