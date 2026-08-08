"""Remote draft release assets must exactly match bounded local staging."""

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


def _document(staged: Path) -> dict[str, object]:
    return {
        "tag_name": _TAG,
        "name": _TITLE,
        "draft": True,
        "prerelease": True,
        "immutable": False,
        "assets": [_identity(path) for path in sorted(staged.iterdir())],
    }


def _run(
    staged: Path,
    tmp_path: Path,
    document: object,
    *,
    expected_tag: str = _TAG,
    expected_title: str = _TITLE,
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


def test_exact_uploaded_draft_emits_stable_safe_identities(tmp_path: Path) -> None:
    staged = _staging(tmp_path)

    result = _run(staged, tmp_path, _document(staged))

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    document = json.loads(result.stdout)
    assert document["protocol"] == "ludoweave.release-draft-integrity/1"
    assert document["status"] == "pass"
    assert document["tag"] == _TAG
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

    failure = _failure(_run(staged, tmp_path, document))
    assert failure["protocol"] == "ludoweave.release-draft-integrity/1"
    assert failure["status"] == "fail"
    assert failure["code"] == code


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


def test_malformed_duplicate_or_oversized_json_fails_without_traceback(tmp_path: Path) -> None:
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
    ]
    for content in (b"{", b'{"tag_name":"one","tag_name":"two"}', b" " * (4 * 1024 * 1024 + 1)):
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
