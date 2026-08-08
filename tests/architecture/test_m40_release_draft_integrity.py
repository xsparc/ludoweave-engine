"""Protect M40 draft-asset integrity and existing hosted boundaries."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github" / "workflows" / "ci.yml"
_RELEASE = _ROOT / ".github" / "workflows" / "release.yml"
_VERIFY = "scripts/verify_release_draft.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"


def _step(source: str, name: str, next_name: str | None = None) -> str:
    start = source.index(f"      - name: {name}\n")
    if next_name is None:
        return source[start:]
    return source[start : source.index(f"      - name: {next_name}\n", start + 1)]


def test_remote_assets_are_verified_while_release_remains_draft() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    create = _step(workflow, "Create draft GitHub prerelease", "Upload draft release assets")
    upload = _step(workflow, "Upload draft release assets", "Verify draft release asset integrity")
    verify = _step(
        workflow, "Verify draft release asset integrity", "Publish verified GitHub prerelease"
    )
    publish = _step(workflow, "Publish verified GitHub prerelease")

    assert "gh release create" in create
    assert "--verify-tag" in create
    assert "--draft" in create
    assert "--prerelease" in create
    assert "--latest=false" in create
    assert "release/*" not in create
    assert "gh release upload" in upload
    assert "release/*" in upload
    assert "--clobber" not in upload
    assert "X-GitHub-Api-Version: 2026-03-10" in verify
    assert 'gh release view "$GITHUB_REF_NAME"' in verify
    assert "--json databaseId --jq .databaseId" in verify
    assert '""|*[!0-9]*)' in verify
    assert '"repos/$GITHUB_REPOSITORY/releases/$release_id"' in verify
    assert "/releases/tags/" not in verify
    assert '"$RUNNER_TEMP/release-draft.json"' in verify
    assert _VERIFY in verify
    assert '--expected-tag "$GITHUB_REF_NAME"' in verify
    assert '--expected-title "$RELEASE_TITLE"' in verify
    assert "gh release edit" in publish
    assert "--verify-tag" in publish
    assert "--draft=false" in publish
    assert "--prerelease" in publish
    assert "--latest=false" in publish
    assert "gh release create" not in publish

    required = (
        "actions/attest@",
        "actions/upload-artifact@",
        "gh release create",
        "gh release upload",
        _VERIFY,
        "gh release edit",
    )
    offsets = [workflow.index(value) for value in required]
    assert offsets == sorted(offsets)


def test_m40_adds_no_runner_action_permission_trigger_or_ci_change() -> None:
    ci = _CI.read_text(encoding="utf-8")
    release = _RELEASE.read_text(encoding="utf-8")

    assert hashlib.sha256(_CI.read_bytes()).hexdigest() == _CI_SHA256
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
    assert ci.count("\n    runs-on:") == 2


def test_m40_changes_no_runtime_dependency_lock_or_version_boundary() -> None:
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert not any(
        "m40" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m40_docs_define_draft_digest_authority_and_nonclaims() -> None:
    readme = (_ROOT / "README.md").read_text(encoding="utf-8")
    architecture = (_ROOT / "docs" / "architecture.md").read_text(encoding="utf-8")
    release = (_ROOT / "docs" / "release-process.md").read_text(encoding="utf-8")
    security = (_ROOT / "SECURITY.md").read_text(encoding="utf-8")
    rfc = (_ROOT / "docs" / "rfcs" / "0023-verify-draft-release-assets.md").read_text(
        encoding="utf-8"
    )

    for text in (readme, architecture, release, security, rfc):
        folded = text.casefold()
        assert "m40" in folded
        assert "draft" in folded
        assert "sha-256" in folded
        assert "immutable" in folded
    normalized_rfc = " ".join(rfc.split()).casefold()
    assert "github" in normalized_rfc
    assert "no additional runner allocation" in normalized_rfc
    assert "without `--clobber`" in rfc
    assert "**Status:** Accepted" in rfc
