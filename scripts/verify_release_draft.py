"""Fail closed unless a GitHub release matches its expected state and staging."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal, cast

_PROTOCOL = "ludoweave.release-draft-integrity/4"
_ASSET_PLAN_PROTOCOL = "ludoweave.release-asset-retrieval-plan/1"
_MAX_DOCUMENT_BYTES = 4 * 1024 * 1024
_MAX_ASSETS = 32
_MAX_ASSET_BYTES = 256 * 1024 * 1024
_MAX_TOTAL_BYTES = 512 * 1024 * 1024
_MAX_RELEASE_NOTES_BYTES = 256 * 1024
_MAX_ASSET_ID = (1 << 63) - 1
_RELEASE_NOTES_NAME = "RELEASE_NOTES.md"
_TAG_PATTERN = re.compile(r"v[0-9A-Za-z][0-9A-Za-z._-]{0,127}")
_NAME_PATTERN = re.compile(r"[0-9A-Za-z][0-9A-Za-z._+-]{0,255}")
_DIGEST_PATTERN = re.compile(r"sha256:[0-9a-f]{64}")
_PUBLISHED_AT_PATTERN = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,9})?Z"
)

ReleaseState = Literal["draft", "published"]


@dataclass(frozen=True, slots=True)
class ReleaseAssetIdentity:
    """Safe local/remote identity for one staged release asset."""

    name: str
    bytes: int
    sha256: str


@dataclass(frozen=True, slots=True)
class ReleaseAssetRetrieval:
    """Validated GitHub asset identity used only by the workflow retrieval plan."""

    asset_id: int
    bytes: int
    name: str


class ReleaseDraftIntegrityError(ValueError):
    """A release cannot be trusted for or after publication."""

    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code


def verify_release(
    staged_directory: Path,
    release_document: object,
    *,
    expected_tag: str,
    expected_title: str,
    expected_state: ReleaseState,
) -> tuple[ReleaseAssetIdentity, ...]:
    """Return asset identities when state, notes, and assets match expectations."""

    assets, _ = _verify_release(
        staged_directory,
        release_document,
        expected_tag=expected_tag,
        expected_title=expected_title,
        expected_state=expected_state,
    )
    return assets


def _verify_release(
    staged_directory: Path,
    release_document: object,
    *,
    expected_tag: str,
    expected_title: str,
    expected_state: ReleaseState,
) -> tuple[tuple[ReleaseAssetIdentity, ...], tuple[ReleaseAssetRetrieval, ...]]:
    """Return safe asset and retrieval identities after complete validation."""

    tag = _tag_name(expected_tag)
    title = _title(expected_title)
    root = _directory(staged_directory)
    notes = _release_notes(root / _RELEASE_NOTES_NAME)
    local = _local_assets(root)
    release = _object(release_document, field="release document")

    if release.get("tag_name") != tag or release.get("name") != title:
        raise ReleaseDraftIntegrityError(
            "release identity does not match the expected tag and title",
            code="release_draft.identity_mismatch",
        )
    _validate_release_state(release, expected_state=expected_state)
    if release.get("body") != notes:
        raise ReleaseDraftIntegrityError(
            "release notes do not exactly match local staging",
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
    retrievals: dict[str, ReleaseAssetRetrieval] = {}
    asset_ids: set[int] = set()
    for value in assets:
        asset = _object(value, field="release asset")
        name = _asset_name(asset.get("name"))
        if name in remote:
            raise ReleaseDraftIntegrityError(
                "release contains a duplicate asset name",
                code="release_draft.invalid_document",
            )
        asset_id = _asset_id(asset.get("id"))
        if asset_id in asset_ids:
            raise ReleaseDraftIntegrityError(
                "release contains a duplicate asset id",
                code="release_draft.invalid_document",
            )
        asset_ids.add(asset_id)
        size = _asset_size(asset.get("size"))
        digest = _asset_digest(asset.get("digest"))
        if asset.get("state") != "uploaded":
            raise ReleaseDraftIntegrityError(
                f"release asset is not completely uploaded: {name}",
                code="release_draft.asset_mismatch",
            )
        remote[name] = ReleaseAssetIdentity(name, size, digest.removeprefix("sha256:"))
        retrievals[name] = ReleaseAssetRetrieval(asset_id, size, name)

    if remote.keys() != local.keys():
        raise ReleaseDraftIntegrityError(
            "release and local staging contain different asset names",
            code="release_draft.asset_set_mismatch",
        )
    for name, identity in local.items():
        if remote[name] != identity:
            raise ReleaseDraftIntegrityError(
                f"release asset does not match local staging: {name}",
                code="release_draft.asset_mismatch",
            )
    return tuple(local.values()), tuple(retrievals[name] for name in local)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("staged_directory", type=Path, help="local staged release directory")
    parser.add_argument("release_document", type=Path, help="GitHub release JSON document")
    parser.add_argument("--expected-tag", required=True, help="exact vVERSION release tag")
    parser.add_argument("--expected-title", required=True, help="exact release title")
    parser.add_argument(
        "--expected-state",
        required=True,
        choices=("draft", "published"),
        help="required release publication state",
    )
    parser.add_argument(
        "--asset-plan",
        type=Path,
        help="new file that receives a bounded published-asset retrieval plan",
    )
    args = parser.parse_args(argv)
    try:
        state = _release_state(str(args.expected_state))
        assets, retrievals = _verify_release(
            Path(args.staged_directory),
            _json_document(Path(args.release_document)),
            expected_tag=str(args.expected_tag),
            expected_title=str(args.expected_title),
            expected_state=state,
        )
        plan_path = cast(Path | None, args.asset_plan)
        if plan_path is not None:
            if state != "published":
                raise ReleaseDraftIntegrityError(
                    "asset retrieval plans require published release state",
                    code="release_draft.invalid_plan",
                )
            _write_asset_plan(plan_path, retrievals)
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
                "state": state,
                "assets": [
                    {"name": item.name, "bytes": item.bytes, "sha256": item.sha256}
                    for item in assets
                ],
            }
        )
    )
    return 0


def _release_state(value: str) -> ReleaseState:
    if value == "draft" or value == "published":
        return value
    raise ReleaseDraftIntegrityError(
        "expected release state is invalid",
        code="release_draft.invalid_identity",
    )


def _validate_release_state(release: dict[str, object], *, expected_state: ReleaseState) -> None:
    if release.get("prerelease") is not True:
        raise ReleaseDraftIntegrityError(
            "release is not in the expected prerelease state",
            code="release_draft.invalid_state",
        )
    immutable = release.get("immutable")
    if expected_state == "draft":
        if (
            release.get("draft") is not True
            or immutable is not False
            or "published_at" not in release
            or release["published_at"] is not None
        ):
            raise ReleaseDraftIntegrityError(
                "release must remain an unpublished mutable prerelease draft",
                code="release_draft.invalid_state",
            )
        return

    published_at = release.get("published_at")
    if (
        release.get("draft") is not False
        or type(immutable) is not bool
        or not _is_published_at(published_at)
    ):
        raise ReleaseDraftIntegrityError(
            "release is not a published prerelease with a valid publication time",
            code="release_draft.invalid_state",
        )


def _is_published_at(value: object) -> bool:
    if not isinstance(value, str) or _PUBLISHED_AT_PATTERN.fullmatch(value) is None:
        return False
    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return timestamp.tzinfo == UTC


def _write_asset_plan(path: Path, retrievals: tuple[ReleaseAssetRetrieval, ...]) -> None:
    payload = (
        _ASSET_PLAN_PROTOCOL
        + "\n"
        + "".join(f"{item.asset_id}\t{item.bytes}\t{item.name}\n" for item in retrievals)
    )
    try:
        if path.is_symlink() or path.exists():
            raise OSError
        parent = path.parent.resolve(strict=True)
        if not parent.is_dir():
            raise OSError
        target = parent / path.name
        with target.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
    except (OSError, RuntimeError) as error:
        raise ReleaseDraftIntegrityError(
            "asset retrieval plan could not be created",
            code="release_draft.plan_write_failed",
        ) from error


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
            "release document is unavailable",
            code="release_draft.invalid_document",
        ) from error
    if len(raw) > _MAX_DOCUMENT_BYTES:
        raise ReleaseDraftIntegrityError(
            "release document exceeds the size limit",
            code="release_draft.invalid_document",
        )
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    except ReleaseDraftIntegrityError:
        raise
    except (UnicodeDecodeError, RecursionError, ValueError) as error:
        raise ReleaseDraftIntegrityError(
            "release document is not strict UTF-8 JSON",
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
                "release JSON contains a duplicate object key",
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


def _asset_id(value: object) -> int:
    if type(value) is not int or not 0 < value <= _MAX_ASSET_ID:
        raise ReleaseDraftIntegrityError(
            "release asset id is invalid",
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
