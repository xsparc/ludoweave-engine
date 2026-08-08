"""Verify a signed GitHub release tag, checkout identity, and main ancestry."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

_PROTOCOL = "ludoweave.release-ref-integrity/1"
_MAIN_REF = "refs/remotes/origin/main"
_MAX_DOCUMENT_BYTES = 1024 * 1024
_TAG_PATTERN = re.compile(r"v[0-9A-Za-z][0-9A-Za-z._-]{0,127}")
_SHA_PATTERN = re.compile(r"[0-9a-f]{40}")


@dataclass(frozen=True, slots=True)
class ReleaseRefIdentity:
    """Safe release-ref identities after local and GitHub validation."""

    tag: str
    tag_object_sha: str
    commit_sha: str
    main_ref: str


class ReleaseRefIntegrityError(ValueError):
    """A release ref cannot be trusted for publication."""

    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code


def verify_release_ref(
    repository: Path,
    ref_document: object,
    tag_document: object,
    *,
    expected_tag: str,
    expected_commit: str,
) -> ReleaseRefIdentity:
    """Validate GitHub tag evidence against the exact local checkout."""

    tag_name = _tag_name(expected_tag)
    commit_sha = _sha(expected_commit, field="expected commit")
    repo = _repository(repository)
    ref = _object(ref_document, field="tag ref document")
    tag = _object(tag_document, field="tag object document")

    expected_ref = f"refs/tags/{tag_name}"
    if ref.get("ref") != expected_ref:
        raise ReleaseRefIntegrityError(
            "GitHub tag ref does not match the expected tag",
            code="release_ref.ref_mismatch",
        )
    ref_target = _object(ref.get("object"), field="tag ref target")
    if ref_target.get("type") != "tag":
        raise ReleaseRefIntegrityError(
            "release ref must target an annotated tag object",
            code="release_ref.not_annotated",
        )
    tag_object_sha = _sha(ref_target.get("sha"), field="tag object SHA")

    if tag.get("tag") != tag_name or tag.get("sha") != tag_object_sha:
        raise ReleaseRefIntegrityError(
            "GitHub tag object identity does not match the release ref",
            code="release_ref.tag_mismatch",
        )
    tag_target = _object(tag.get("object"), field="tag object target")
    if tag_target.get("type") != "commit" or tag_target.get("sha") != commit_sha:
        raise ReleaseRefIntegrityError(
            "signed tag does not target the expected release commit",
            code="release_ref.commit_mismatch",
        )
    verification = _object(tag.get("verification"), field="tag signature verification")
    if (
        verification.get("verified") is not True
        or verification.get("reason") != "valid"
        or not _nonempty_text(verification.get("signature"))
        or not _nonempty_text(verification.get("payload"))
        or not _nonempty_text(verification.get("verified_at"))
    ):
        raise ReleaseRefIntegrityError(
            "GitHub does not report a valid verified tag signature",
            code="release_ref.unverified_tag",
        )

    _require_git_value(repo, ("rev-parse", "--is-inside-work-tree"), "true")
    _require_git_value(repo, ("rev-parse", "HEAD"), commit_sha, code="checkout_mismatch")
    _require_git_value(
        repo,
        ("rev-parse", "--verify", f"{expected_ref}^{{tag}}"),
        tag_object_sha,
        code="local_tag_mismatch",
    )
    _require_git_value(
        repo,
        ("rev-parse", "--verify", f"{expected_ref}^{{commit}}"),
        commit_sha,
        code="local_tag_mismatch",
    )
    _sha(
        _git(repo, "rev-parse", "--verify", f"{_MAIN_REF}^{{commit}}"),
        field="origin/main commit",
    )
    ancestry = _git_result(repo, "merge-base", "--is-ancestor", commit_sha, _MAIN_REF)
    if ancestry.returncode == 1:
        raise ReleaseRefIntegrityError(
            "release commit is not reachable from origin/main",
            code="release_ref.not_main_ancestor",
        )
    if ancestry.returncode != 0:
        raise ReleaseRefIntegrityError(
            "main ancestry could not be verified",
            code="release_ref.git_failed",
        )

    return ReleaseRefIdentity(tag_name, tag_object_sha, commit_sha, _MAIN_REF)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path, help="checked-out Git repository")
    parser.add_argument("ref_document", type=Path, help="GitHub tag-ref JSON document")
    parser.add_argument("tag_document", type=Path, help="GitHub annotated-tag JSON document")
    parser.add_argument("--expected-tag", required=True, help="exact vVERSION tag name")
    parser.add_argument("--expected-commit", required=True, help="exact checked-out commit SHA")
    args = parser.parse_args(argv)
    try:
        identity = verify_release_ref(
            Path(args.repository),
            _json_document(Path(args.ref_document), role="tag ref"),
            _json_document(Path(args.tag_document), role="tag object"),
            expected_tag=str(args.expected_tag),
            expected_commit=str(args.expected_commit),
        )
    except ReleaseRefIntegrityError as error:
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
                "tag": identity.tag,
                "tag_object_sha": identity.tag_object_sha,
                "commit_sha": identity.commit_sha,
                "main_ref": identity.main_ref,
            }
        )
    )
    return 0


def _repository(value: Path) -> Path:
    try:
        resolved = value.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise ReleaseRefIntegrityError(
            "release repository is unavailable",
            code="release_ref.invalid_repository",
        ) from error
    if not resolved.is_dir():
        raise ReleaseRefIntegrityError(
            "release repository must be a directory",
            code="release_ref.invalid_repository",
        )
    return resolved


def _json_document(path: Path, *, role: str) -> object:
    try:
        if path.is_symlink() or not path.is_file():
            raise OSError
        with path.open("rb") as stream:
            raw = stream.read(_MAX_DOCUMENT_BYTES + 1)
    except OSError as error:
        raise ReleaseRefIntegrityError(
            f"{role} document is unavailable",
            code="release_ref.invalid_document",
        ) from error
    if len(raw) > _MAX_DOCUMENT_BYTES:
        raise ReleaseRefIntegrityError(
            f"{role} document exceeds the size limit",
            code="release_ref.invalid_document",
        )
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError, ReleaseRefIntegrityError) as error:
        if isinstance(error, ReleaseRefIntegrityError):
            raise
        raise ReleaseRefIntegrityError(
            f"{role} document is not strict UTF-8 JSON",
            code="release_ref.invalid_document",
        ) from error


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ReleaseRefIntegrityError(
                "release-ref JSON contains a duplicate object key",
                code="release_ref.invalid_document",
            )
        result[key] = value
    return result


def _tag_name(value: object) -> str:
    if not isinstance(value, str) or _TAG_PATTERN.fullmatch(value) is None:
        raise ReleaseRefIntegrityError(
            "expected release tag is invalid",
            code="release_ref.invalid_identity",
        )
    return value


def _sha(value: object, *, field: str) -> str:
    if not isinstance(value, str) or _SHA_PATTERN.fullmatch(value) is None:
        raise ReleaseRefIntegrityError(
            f"{field} is not an exact lowercase Git SHA-1",
            code="release_ref.invalid_identity",
        )
    return value


def _object(value: object, *, field: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ReleaseRefIntegrityError(
            f"{field} must be a JSON object",
            code="release_ref.invalid_document",
        )
    document = cast(dict[object, object], value)
    if not all(isinstance(key, str) for key in document):
        raise ReleaseRefIntegrityError(
            f"{field} must use string keys",
            code="release_ref.invalid_document",
        )
    return cast(dict[str, object], document)


def _nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _require_git_value(
    repository: Path,
    arguments: tuple[str, ...],
    expected: str,
    *,
    code: str = "git_failed",
) -> None:
    result = _git_result(repository, *arguments)
    if result.returncode != 0 or result.stdout.strip() != expected:
        raise ReleaseRefIntegrityError(
            "local Git identity does not match release evidence",
            code=f"release_ref.{code}",
        )


def _git(repository: Path, *arguments: str) -> str:
    result = _git_result(repository, *arguments)
    if result.returncode != 0:
        raise ReleaseRefIntegrityError(
            "local Git identity could not be read",
            code="release_ref.git_failed",
        )
    return result.stdout.strip()


def _git_result(repository: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", "-C", str(repository), *arguments],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise ReleaseRefIntegrityError(
            "local Git verification could not run",
            code="release_ref.git_failed",
        ) from error


def _json(value: object) -> str:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")
    )


if __name__ == "__main__":
    raise SystemExit(main())
