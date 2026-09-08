"""Protect M41 release-notes integrity and unchanged hosted boundaries."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github" / "workflows" / "ci.yml"
_RELEASE = _ROOT / ".github" / "workflows" / "release.yml"
_VERIFY = _ROOT / "scripts" / "verify_release_draft.py"
_CI_SHA256 = "883674592dd8cfc7f2c292f379591f863c797fdb0cd65f2c0c83a47e232db686"
_PYPROJECT_SHA256 = "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d"
_LOCK_SHA256 = "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18"


def test_release_notes_are_supplied_then_verified_before_publication() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")

    create = workflow.index("gh release create")
    notes = workflow.index("--notes-file release/RELEASE_NOTES.md", create)
    verify = workflow.index("scripts/verify_release_draft.py", notes)
    publish = workflow.index("gh release edit", verify)

    assert create < notes < verify < publish
    assert hashlib.sha256(_CI.read_bytes()).hexdigest() == _CI_SHA256


def test_release_notes_validator_is_bounded_and_content_silent() -> None:
    verifier = _VERIFY.read_text(encoding="utf-8")

    assert '"ludoweave.release-draft-integrity/4"' in verifier
    assert "_MAX_RELEASE_NOTES_BYTES = 256 * 1024" in verifier
    assert '_RELEASE_NOTES_NAME = "RELEASE_NOTES.md"' in verifier
    assert 'release.get("body") != notes' in verifier
    assert 'code="release_draft.notes_mismatch"' in verifier
    assert (
        "notes"
        not in verifier[verifier.index('"status": "pass"') : verifier.index("def _directory")]
    )
    for forbidden in ("import requests", "import urllib", "import socket", "subprocess"):
        assert forbidden not in verifier


def test_m41_changes_no_runtime_dependency_lock_or_version_boundary() -> None:
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert not any(
        "m41" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m41_docs_define_exact_source_body_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0024-verify-draft-release-notes.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8").casefold()
        assert "m41" in text
        assert "release" in text
        assert "notes" in text
        assert "body" in text
        assert "exact" in text
    rfc = paths[-1].read_text(encoding="utf-8")
    assert "**Status:** Accepted" in rfc
    assert "no additional runner allocation" in " ".join(rfc.split()).casefold()
