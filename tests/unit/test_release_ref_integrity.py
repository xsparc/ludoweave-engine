"""Signed release-ref validation is strict, local, and fail closed."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = _ROOT / "scripts" / "verify_release_ref.py"
_TAG = "v0.1.0a1"


def _git(repository: Path, *arguments: str, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    return result.stdout.strip()


def _repository(tmp_path: Path, *, annotated: bool = True) -> tuple[Path, str, str]:
    repository = tmp_path / "repository"
    repository.mkdir()
    _git(repository, "init", "--initial-branch=main")
    _git(repository, "config", "user.name", "Release Test")
    _git(repository, "config", "user.email", "release@example.invalid")
    (repository / "source.txt").write_text("release source\n", encoding="utf-8")
    _git(repository, "add", "source.txt")
    _git(repository, "commit", "-m", "release source")
    commit_sha = _git(repository, "rev-parse", "HEAD")
    if annotated:
        _git(repository, "tag", "-a", _TAG, "-m", "release tag")
    else:
        _git(repository, "tag", _TAG)
    tag_sha = _git(repository, "rev-parse", f"refs/tags/{_TAG}")
    _git(repository, "update-ref", "refs/remotes/origin/main", commit_sha)
    return repository, commit_sha, tag_sha


def _documents(tmp_path: Path, *, commit_sha: str, tag_sha: str) -> tuple[Path, Path]:
    ref = tmp_path / "ref.json"
    tag = tmp_path / "tag.json"
    ref.write_text(
        json.dumps(
            {
                "ref": f"refs/tags/{_TAG}",
                "object": {"type": "tag", "sha": tag_sha},
            }
        ),
        encoding="utf-8",
    )
    tag.write_text(
        json.dumps(
            {
                "sha": tag_sha,
                "tag": _TAG,
                "object": {"type": "commit", "sha": commit_sha},
                "verification": {
                    "verified": True,
                    "reason": "valid",
                    "signature": "signed-value",
                    "payload": "signed-payload",
                    "verified_at": "2026-08-08T00:00:00Z",
                },
            }
        ),
        encoding="utf-8",
    )
    return ref, tag


def _run(
    repository: Path,
    ref: Path,
    tag: Path,
    *,
    expected_tag: str = _TAG,
    expected_commit: str | None = None,
) -> subprocess.CompletedProcess[str]:
    commit = expected_commit or _git(repository, "rev-parse", f"{_TAG}^{{commit}}")
    return subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            str(repository),
            str(ref),
            str(tag),
            "--expected-tag",
            expected_tag,
            "--expected-commit",
            commit,
        ],
        cwd=_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _failure(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    assert result.returncode == 1
    assert result.stdout == ""
    assert "Traceback" not in result.stderr
    return cast(dict[str, object], json.loads(result.stderr))


def test_verified_annotated_tag_on_main_emits_safe_identity(tmp_path: Path) -> None:
    repository, commit_sha, tag_sha = _repository(tmp_path)
    ref, tag = _documents(tmp_path, commit_sha=commit_sha, tag_sha=tag_sha)

    result = _run(repository, ref, tag, expected_commit=commit_sha)

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    document = json.loads(result.stdout)
    assert document == {
        "commit_sha": commit_sha,
        "main_ref": "refs/remotes/origin/main",
        "protocol": "ludoweave.release-ref-integrity/1",
        "status": "pass",
        "tag": _TAG,
        "tag_object_sha": tag_sha,
    }
    assert "signed-value" not in result.stdout
    assert "signed-payload" not in result.stdout


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        ("ref-name", "release_ref.ref_mismatch"),
        ("lightweight-api", "release_ref.not_annotated"),
        ("tag-name", "release_ref.tag_mismatch"),
        ("tag-sha", "release_ref.tag_mismatch"),
        ("commit", "release_ref.commit_mismatch"),
        ("unsigned", "release_ref.unverified_tag"),
        ("bad-reason", "release_ref.unverified_tag"),
        ("missing-signature", "release_ref.unverified_tag"),
    ],
)
def test_github_identity_or_signature_mismatch_fails_closed(
    tmp_path: Path, mutation: str, code: str
) -> None:
    repository, commit_sha, tag_sha = _repository(tmp_path)
    ref_path, tag_path = _documents(tmp_path, commit_sha=commit_sha, tag_sha=tag_sha)
    ref = cast(dict[str, object], json.loads(ref_path.read_text(encoding="utf-8")))
    tag = cast(dict[str, object], json.loads(tag_path.read_text(encoding="utf-8")))
    ref_target = cast(dict[str, object], ref["object"])
    tag_target = cast(dict[str, object], tag["object"])
    verification = cast(dict[str, object], tag["verification"])
    if mutation == "ref-name":
        ref["ref"] = "refs/tags/v0.1.0a2"
    elif mutation == "lightweight-api":
        ref_target["type"] = "commit"
    elif mutation == "tag-name":
        tag["tag"] = "v0.1.0a2"
    elif mutation == "tag-sha":
        tag["sha"] = "0" * 40
    elif mutation == "commit":
        tag_target["sha"] = "0" * 40
    elif mutation == "unsigned":
        verification["verified"] = False
    elif mutation == "bad-reason":
        verification["reason"] = "unsigned"
    else:
        verification["signature"] = None
    ref_path.write_text(json.dumps(ref), encoding="utf-8")
    tag_path.write_text(json.dumps(tag), encoding="utf-8")

    document = _failure(_run(repository, ref_path, tag_path, expected_commit=commit_sha))
    assert document["status"] == "fail"
    assert document["code"] == code


def test_local_lightweight_tag_fails_even_when_api_documents_claim_success(tmp_path: Path) -> None:
    repository, commit_sha, lightweight_sha = _repository(tmp_path, annotated=False)
    ref, tag = _documents(tmp_path, commit_sha=commit_sha, tag_sha=lightweight_sha)

    document = _failure(_run(repository, ref, tag, expected_commit=commit_sha))
    assert document["code"] == "release_ref.local_tag_mismatch"


def test_checkout_mismatch_fails_closed(tmp_path: Path) -> None:
    repository, commit_sha, tag_sha = _repository(tmp_path)
    ref, tag = _documents(tmp_path, commit_sha=commit_sha, tag_sha=tag_sha)
    (repository / "later.txt").write_text("later\n", encoding="utf-8")
    _git(repository, "add", "later.txt")
    _git(repository, "commit", "-m", "later checkout")

    document = _failure(_run(repository, ref, tag, expected_commit=commit_sha))
    assert document["code"] == "release_ref.checkout_mismatch"


def test_release_commit_must_be_reachable_from_origin_main(tmp_path: Path) -> None:
    repository, commit_sha, tag_sha = _repository(tmp_path)
    ref, tag = _documents(tmp_path, commit_sha=commit_sha, tag_sha=tag_sha)
    environment = dict(os.environ)
    environment.update(
        {
            "GIT_AUTHOR_NAME": "Release Test",
            "GIT_AUTHOR_EMAIL": "release@example.invalid",
            "GIT_COMMITTER_NAME": "Release Test",
            "GIT_COMMITTER_EMAIL": "release@example.invalid",
        }
    )
    tree = _git(repository, "rev-parse", "HEAD^{tree}")
    unrelated = _git(repository, "commit-tree", tree, "-m", "unrelated main", env=environment)
    _git(repository, "update-ref", "refs/remotes/origin/main", unrelated)

    document = _failure(_run(repository, ref, tag, expected_commit=commit_sha))
    assert document["code"] == "release_ref.not_main_ancestor"


@pytest.mark.parametrize(
    ("content", "code"),
    [
        ("{", "release_ref.invalid_document"),
        ('{"ref":"one","ref":"two"}', "release_ref.invalid_document"),
    ],
)
def test_malformed_or_duplicate_json_fails_without_traceback(
    tmp_path: Path, content: str, code: str
) -> None:
    repository, commit_sha, tag_sha = _repository(tmp_path)
    ref, tag = _documents(tmp_path, commit_sha=commit_sha, tag_sha=tag_sha)
    ref.write_text(content, encoding="utf-8")

    document = _failure(_run(repository, ref, tag, expected_commit=commit_sha))
    assert document["code"] == code


def test_invalid_expected_tag_and_commit_are_structured(tmp_path: Path) -> None:
    repository, commit_sha, tag_sha = _repository(tmp_path)
    ref, tag = _documents(tmp_path, commit_sha=commit_sha, tag_sha=tag_sha)

    invalid_tag = _failure(
        _run(repository, ref, tag, expected_tag="vbad/tag", expected_commit=commit_sha)
    )
    assert invalid_tag["code"] == "release_ref.invalid_identity"

    invalid_commit = _failure(_run(repository, ref, tag, expected_commit="ABC"))
    assert invalid_commit["code"] == "release_ref.invalid_identity"


def test_missing_or_oversized_document_fails_closed(tmp_path: Path) -> None:
    repository, commit_sha, tag_sha = _repository(tmp_path)
    ref, tag = _documents(tmp_path, commit_sha=commit_sha, tag_sha=tag_sha)

    missing = _failure(_run(repository, tmp_path / "missing.json", tag))
    assert missing["code"] == "release_ref.invalid_document"

    ref.write_bytes(b" " * (1024 * 1024 + 1))
    oversized = _failure(_run(repository, ref, tag))
    assert oversized["code"] == "release_ref.invalid_document"
