"""Remote release state and assets must exactly match bounded local staging."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = _ROOT / "scripts" / "verify_release_draft.py"
_TAG = "v0.1.0a1"
_TITLE = "LudoWeave 0.1.0a1"


def _staging(tmp_path: Path) -> Path:
    staged = tmp_path / "release"
    staged.mkdir()
    (staged / "LICENSE").write_text("license\n", encoding="utf-8")
    (staged / "RELEASE_NOTES.md").write_bytes(b"# Release notes\n\nExact notes.\n")
    (staged / "SHA256SUMS").write_text("checksums\n", encoding="utf-8")
    (staged / "ludoweave-0.1.0a1-py3-none-any.whl").write_bytes(b"wheel")
    return staged


def _identity(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "name": path.name,
        "size": len(data),
        "digest": f"sha256:{hashlib.sha256(data).hexdigest()}",
        "state": "uploaded",
    }


def _document(
    staged: Path, *, expected_state: str = "draft", immutable: bool = False
) -> dict[str, object]:
    published = expected_state == "published"
    return {
        "tag_name": _TAG,
        "name": _TITLE,
        "draft": not published,
        "prerelease": True,
        "immutable": immutable,
        "published_at": "2026-08-09T00:00:00Z" if published else None,
        "body": (staged / "RELEASE_NOTES.md").read_bytes().decode("utf-8"),
        "assets": [_identity(path) for path in sorted(staged.iterdir())],
    }


def _run(
    staged: Path,
    tmp_path: Path,
    document: object,
    *,
    expected_tag: str = _TAG,
    expected_title: str = _TITLE,
    expected_state: str = "draft",
) -> subprocess.CompletedProcess[str]:
    evidence = tmp_path / "draft.json"
    evidence.write_text(json.dumps(document), encoding="utf-8")
    return subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            str(staged),
            str(evidence),
            "--expected-tag",
            expected_tag,
            "--expected-title",
            expected_title,
            "--expected-state",
            expected_state,
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


@pytest.mark.parametrize(
    ("expected_state", "immutable"),
    [("draft", False), ("published", False), ("published", True)],
)
def test_exact_release_emits_stable_safe_identities(
    tmp_path: Path, expected_state: str, immutable: bool
) -> None:
    staged = _staging(tmp_path)

    result = _run(
        staged,
        tmp_path,
        _document(staged, expected_state=expected_state, immutable=immutable),
        expected_state=expected_state,
    )

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    document = json.loads(result.stdout)
    assert document["protocol"] == "ludoweave.release-draft-integrity/3"
    assert document["status"] == "pass"
    assert document["tag"] == _TAG
    assert document["state"] == expected_state
    assert "Exact notes" not in result.stdout
    assert "2026-08-09T00:00:00Z" not in result.stdout
    assert '"immutable"' not in result.stdout
    assert document["assets"] == [
        {
            "bytes": path.stat().st_size,
            "name": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in sorted(staged.iterdir(), key=lambda item: item.name)
    ]


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        ("tag", "release_draft.identity_mismatch"),
        ("title", "release_draft.identity_mismatch"),
        ("published", "release_draft.invalid_state"),
        ("not-prerelease", "release_draft.invalid_state"),
        ("immutable", "release_draft.invalid_state"),
        ("published-at", "release_draft.invalid_state"),
        ("published-at-missing", "release_draft.invalid_state"),
        ("notes", "release_draft.notes_mismatch"),
        ("notes-missing", "release_draft.notes_mismatch"),
        ("notes-null", "release_draft.notes_mismatch"),
        ("missing", "release_draft.asset_set_mismatch"),
        ("extra", "release_draft.asset_set_mismatch"),
        ("size", "release_draft.asset_mismatch"),
        ("digest", "release_draft.asset_mismatch"),
        ("pending", "release_draft.asset_mismatch"),
    ],
)
def test_remote_identity_state_or_asset_drift_fails_closed(
    tmp_path: Path, mutation: str, code: str
) -> None:
    staged = _staging(tmp_path)
    document = _document(staged)
    assets = cast(list[dict[str, object]], document["assets"])
    if mutation == "tag":
        document["tag_name"] = "v0.1.0a2"
    elif mutation == "title":
        document["name"] = "Wrong title"
    elif mutation == "published":
        document["draft"] = False
    elif mutation == "not-prerelease":
        document["prerelease"] = False
    elif mutation == "immutable":
        document["immutable"] = True
    elif mutation == "published-at":
        document["published_at"] = "2026-08-09T00:00:00Z"
    elif mutation == "published-at-missing":
        del document["published_at"]
    elif mutation == "notes":
        document["body"] = "different notes\n"
    elif mutation == "notes-missing":
        del document["body"]
    elif mutation == "notes-null":
        document["body"] = None
    elif mutation == "missing":
        assets.pop()
    elif mutation == "extra":
        assets.append(
            {
                "name": "extra.txt",
                "size": 1,
                "digest": f"sha256:{'0' * 64}",
                "state": "uploaded",
            }
        )
    elif mutation == "size":
        assets[0]["size"] = cast(int, assets[0]["size"]) + 1
    elif mutation == "digest":
        assets[0]["digest"] = f"sha256:{'0' * 64}"
    else:
        assets[0]["state"] = "new"

    result = _run(staged, tmp_path, document)
    failure = _failure(result)
    assert failure["protocol"] == "ludoweave.release-draft-integrity/3"
    assert failure["status"] == "fail"
    assert failure["code"] == code
    assert "Exact notes" not in result.stderr
    assert "different notes" not in result.stderr


@pytest.mark.parametrize(
    "mutation",
    [
        "draft",
        "not-prerelease",
        "immutable-missing",
        "immutable-null",
        "immutable-text",
        "published-at-missing",
        "published-at-null",
        "published-at-empty",
        "published-at-malformed",
    ],
)
def test_invalid_published_state_fails_closed(tmp_path: Path, mutation: str) -> None:
    staged = _staging(tmp_path)
    document = _document(staged, expected_state="published")
    if mutation == "draft":
        document["draft"] = True
    elif mutation == "not-prerelease":
        document["prerelease"] = False
    elif mutation == "immutable-missing":
        del document["immutable"]
    elif mutation == "immutable-null":
        document["immutable"] = None
    elif mutation == "immutable-text":
        document["immutable"] = "false"
    elif mutation == "published-at-missing":
        del document["published_at"]
    elif mutation == "published-at-null":
        document["published_at"] = None
    elif mutation == "published-at-empty":
        document["published_at"] = ""
    else:
        document["published_at"] = "2026-99-99T00:00:00Z"

    result = _run(staged, tmp_path, document, expected_state="published")
    failure = _failure(result)
    assert failure["protocol"] == "ludoweave.release-draft-integrity/3"
    assert failure["code"] == "release_draft.invalid_state"
    assert "2026-99-99T00:00:00Z" not in result.stderr


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        ("notes", "release_draft.notes_mismatch"),
        ("asset", "release_draft.asset_mismatch"),
    ],
)
def test_published_notes_or_assets_drift_fails_closed(
    tmp_path: Path, mutation: str, code: str
) -> None:
    staged = _staging(tmp_path)
    document = _document(staged, expected_state="published")
    if mutation == "notes":
        document["body"] = "different notes\n"
    else:
        assets = cast(list[dict[str, object]], document["assets"])
        assets[0]["digest"] = f"sha256:{'0' * 64}"

    result = _run(staged, tmp_path, document, expected_state="published")
    failure = _failure(result)
    assert failure["code"] == code
    assert "Exact notes" not in result.stderr
    assert "different notes" not in result.stderr
    assert "2026-08-09T00:00:00Z" not in result.stderr


def test_duplicate_remote_asset_name_fails_closed(tmp_path: Path) -> None:
    staged = _staging(tmp_path)
    document = _document(staged)
    assets = cast(list[dict[str, object]], document["assets"])
    assets.append(dict(assets[0]))

    failure = _failure(_run(staged, tmp_path, document))
    assert failure["code"] == "release_draft.invalid_document"


@pytest.mark.parametrize("field", ["size", "digest", "state"])
def test_missing_required_remote_asset_field_fails_closed(tmp_path: Path, field: str) -> None:
    staged = _staging(tmp_path)
    document = _document(staged)
    assets = cast(list[dict[str, object]], document["assets"])
    del assets[0][field]

    failure = _failure(_run(staged, tmp_path, document))
    assert failure["code"] in {
        "release_draft.invalid_document",
        "release_draft.asset_mismatch",
    }


def test_invalid_expected_identity_is_structured(tmp_path: Path) -> None:
    staged = _staging(tmp_path)
    document = _document(staged)

    bad_tag = _failure(
        _run(staged, tmp_path, document, expected_tag="vbad/tag", expected_title=_TITLE)
    )
    assert bad_tag["code"] == "release_draft.invalid_identity"

    bad_title = _failure(
        _run(staged, tmp_path, document, expected_tag=_TAG, expected_title="bad\ntitle")
    )
    assert bad_title["code"] == "release_draft.invalid_identity"


def test_malformed_duplicate_oversized_or_pathological_json_fails_without_traceback(
    tmp_path: Path,
) -> None:
    staged = _staging(tmp_path)
    evidence = tmp_path / "draft.json"
    command = [
        sys.executable,
        str(_SCRIPT),
        str(staged),
        str(evidence),
        "--expected-tag",
        _TAG,
        "--expected-title",
        _TITLE,
        "--expected-state",
        "draft",
    ]
    for content in (
        b"{",
        b'{"tag_name":"one","tag_name":"two"}',
        b"[" * 2_000 + b"0" + b"]" * 2_000,
        b'{"value":' + b"9" * 10_000 + b"}",
        b" " * (4 * 1024 * 1024 + 1),
    ):
        evidence.write_bytes(content)
        result = subprocess.run(command, cwd=_ROOT, check=False, capture_output=True, text=True)
        assert _failure(result)["code"] == "release_draft.invalid_document"


def test_invalid_local_entry_and_asset_size_fail_closed(tmp_path: Path) -> None:
    staged = _staging(tmp_path)
    document = _document(staged)
    (staged / "nested").mkdir()
    failure = _failure(_run(staged, tmp_path, document))
    assert failure["code"] == "release_draft.invalid_entry"

    (staged / "nested").rmdir()
    oversized = staged / "oversized.bin"
    with oversized.open("wb") as stream:
        stream.truncate(256 * 1024 * 1024 + 1)
    failure = _failure(_run(staged, tmp_path, document))
    assert failure["code"] == "release_draft.size_limit"


@pytest.mark.parametrize(
    "content",
    [b"", b"invalid: \xff", b"contains\x00nul", b"x" * (256 * 1024 + 1)],
    ids=["empty", "invalid-utf8", "nul", "oversized"],
)
def test_invalid_local_release_notes_fail_closed(tmp_path: Path, content: bytes) -> None:
    staged = _staging(tmp_path)
    document = _document(staged)
    (staged / "RELEASE_NOTES.md").write_bytes(content)

    failure = _failure(_run(staged, tmp_path, document))
    assert failure["code"] == "release_draft.invalid_notes"


def test_missing_local_release_notes_fail_closed(tmp_path: Path) -> None:
    staged = _staging(tmp_path)
    document = _document(staged)
    (staged / "RELEASE_NOTES.md").unlink()

    failure = _failure(_run(staged, tmp_path, document))
    assert failure["code"] == "release_draft.invalid_notes"


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="symlink support unavailable")
def test_symlinked_local_release_notes_fail_closed_when_supported(tmp_path: Path) -> None:
    staged = _staging(tmp_path)
    document = _document(staged)
    notes = staged / "RELEASE_NOTES.md"
    notes.unlink()
    try:
        notes.symlink_to(staged / "LICENSE")
    except OSError:
        pytest.skip("symlink creation is not permitted")

    failure = _failure(_run(staged, tmp_path, document))
    assert failure["code"] == "release_draft.invalid_notes"


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="symlink support unavailable")
def test_local_symlink_fails_closed_when_supported(tmp_path: Path) -> None:
    staged = _staging(tmp_path)
    document = _document(staged)
    link = staged / "linked.txt"
    try:
        link.symlink_to(staged / "LICENSE")
    except OSError:
        pytest.skip("symlink creation is not permitted")

    failure = _failure(_run(staged, tmp_path, document))
    assert failure["code"] == "release_draft.invalid_entry"
