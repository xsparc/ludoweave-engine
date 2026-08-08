"""Protect M41 release-notes integrity and unchanged hosted boundaries."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github" / "workflows" / "ci.yml"
_RELEASE = _ROOT / ".github" / "workflows" / "release.yml"
_VERIFY = _ROOT / "scripts" / "verify_release_draft.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_RELEASE_SHA256 = "3983cd82f0201fcac8fe2156f77715e1136998781b428c60a192b3f3a3522871"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"


def test_release_notes_are_supplied_then_verified_before_publication() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")

    create = workflow.index("gh release create")
    notes = workflow.index("--notes-file release/RELEASE_NOTES.md", create)
    verify = workflow.index("scripts/verify_release_draft.py", notes)
    publish = workflow.index("gh release edit", verify)

    assert create < notes < verify < publish
    assert hashlib.sha256(_CI.read_bytes()).hexdigest() == _CI_SHA256
    assert hashlib.sha256(_RELEASE.read_bytes()).hexdigest() == _RELEASE_SHA256


def test_release_notes_validator_is_bounded_and_content_silent() -> None:
    verifier = _VERIFY.read_text(encoding="utf-8")

    assert '"ludoweave.release-draft-integrity/2"' in verifier
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
