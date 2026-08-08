"""Protect M42 post-publication integrity and bounded hosted ownership."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github" / "workflows" / "ci.yml"
_RELEASE = _ROOT / ".github" / "workflows" / "release.yml"
_VERIFY = _ROOT / "scripts" / "verify_release_draft.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"


def _step(source: str, name: str, next_name: str | None = None) -> str:
    start = source.index(f"      - name: {name}\n")
    if next_name is None:
        return source[start:]
    return source[start : source.index(f"      - name: {next_name}\n", start + 1)]


def test_exact_release_id_is_reverified_after_publication() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    draft = _step(
        workflow, "Verify draft release asset integrity", "Publish verified GitHub prerelease"
    )
    publish = _step(
        workflow, "Publish verified GitHub prerelease", "Verify published GitHub prerelease"
    )
    published = _step(workflow, "Verify published GitHub prerelease")

    assert "id: verify_draft" in draft
    assert '"repos/$GITHUB_REPOSITORY/releases/$release_id"' in draft
    assert "--expected-state draft" in draft
    assert 'echo "release_id=$release_id" >> "$GITHUB_OUTPUT"' in draft
    assert "gh release edit" in publish
    assert "--draft=false" in publish
    assert "RELEASE_ID: ${{ steps.verify_draft.outputs.release_id }}" in published
    assert '""|*[!0-9]*)' in published
    assert '"repos/$GITHUB_REPOSITORY/releases/$RELEASE_ID"' in published
    assert '"$RUNNER_TEMP/release-published.json"' in published
    assert "--expected-state published" in published
    assert "X-GitHub-Api-Version: 2026-03-10" in published
    assert "/releases/tags/" not in draft + published
    assert workflow.count("scripts/verify_release_draft.py") == 2
    assert workflow.count("X-GitHub-Api-Version: 2026-03-10") == 2
    for mutation in ("gh release delete", "-X PATCH", "--method PATCH", "--clobber"):
        assert mutation not in published

    required = (
        "Create draft GitHub prerelease",
        "Upload draft release assets",
        "Verify draft release asset integrity",
        "Publish verified GitHub prerelease",
        "Verify published GitHub prerelease",
    )
    offsets = [workflow.index(name) for name in required]
    assert offsets == sorted(offsets)


def test_release_validator_has_explicit_bounded_state_contracts() -> None:
    verifier = _VERIFY.read_text(encoding="utf-8")

    assert '"ludoweave.release-draft-integrity/3"' in verifier
    assert 'ReleaseState = Literal["draft", "published"]' in verifier
    assert 'choices=("draft", "published")' in verifier
    assert "required=True" in verifier
    assert '"published_at" not in release' in verifier
    assert "_PUBLISHED_AT_PATTERN.fullmatch" in verifier
    assert "datetime.fromisoformat" in verifier
    assert "type(immutable) is not bool" in verifier
    assert '"state": state' in verifier
    for forbidden in ("import requests", "import urllib", "import socket", "subprocess"):
        assert forbidden not in verifier


def test_m42_adds_no_runner_action_permission_trigger_or_dependency() -> None:
    release = _RELEASE.read_text(encoding="utf-8")

    assert hashlib.sha256(_CI.read_bytes()).hexdigest() == _CI_SHA256
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert release.count("\n    runs-on:") == 1
    assert release.count("uses: actions/checkout@") == 1
    assert release.count("uses: astral-sh/setup-uv@") == 1
    assert release.count("uses: actions/attest@") == 2
    assert release.count("uses: actions/upload-artifact@") == 1
    assert release.count("gh release create") == 1
    assert release.count("gh release upload") == 1
    assert release.count("gh release edit") == 1
    assert "attestations: write" in release
    assert "contents: write" in release
    assert "id-token: write" in release
    assert 'tags:\n      - "v*"' in release
    assert "pull_request:" not in release
    assert "workflow_dispatch:" not in release
    assert "schedule:" not in release


def test_m42_changes_no_runtime_or_public_package_boundary() -> None:
    assert not any(
        "m42" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m42_docs_define_postpublication_observation_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0025-confirm-published-release-state.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8").casefold()
        assert "m42" in text
        assert "publish" in text
        assert "release" in text

    rfc = paths[-1].read_text(encoding="utf-8")
    normalized = " ".join(rfc.split()).casefold()
    assert "**Status:** Accepted" in rfc
    assert "already public" in normalized
    assert "does not make a mutable release immutable" in normalized
    assert "no job, runner, action, permission" in normalized
