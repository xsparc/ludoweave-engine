"""Protect M39 signed release-ref integrity and hosted-allocation boundaries."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github" / "workflows" / "ci.yml"
_RELEASE = _ROOT / ".github" / "workflows" / "release.yml"
_VERIFY = "scripts/verify_release_ref.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"


def _step(source: str, name: str, next_name: str) -> str:
    start = source.index(f"      - name: {name}\n")
    return source[start : source.index(f"      - name: {next_name}\n", start + 1)]


def test_tag_identity_is_verified_before_expensive_or_publishing_steps() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    verify = _step(
        workflow,
        "Verify signed release tag and main ancestry",
        "Install Linux software-rendering runtime",
    )

    assert "fetch-depth: 0" in workflow
    assert "GH_TOKEN: ${{ github.token }}" in verify
    assert "RELEASE_COMMIT: ${{ github.sha }}" in verify
    assert "RELEASE_TAG: ${{ github.ref_name }}" in verify
    assert 'git rev-parse --verify "refs/tags/${RELEASE_TAG}^{tag}"' in verify
    assert 'gh api "repos/$GITHUB_REPOSITORY/git/ref/tags/$RELEASE_TAG"' in verify
    assert 'gh api "repos/$GITHUB_REPOSITORY/git/tags/$tag_object_sha"' in verify
    assert f'git show "origin/main:{_VERIFY}"' in verify
    assert 'python "$RUNNER_TEMP/verify_release_ref.py"' in verify
    assert f"python {_VERIFY}" not in verify
    assert "uv run" not in verify
    assert '--expected-tag "$RELEASE_TAG" --expected-commit "$RELEASE_COMMIT"' in verify
    assert workflow.index(_VERIFY) < workflow.index("sudo apt-get update")
    assert workflow.index(_VERIFY) < workflow.index("uv sync --frozen")
    assert workflow.index(_VERIFY) < workflow.index("uv build")
    assert workflow.index(_VERIFY) < workflow.index("actions/attest@")
    assert workflow.index(_VERIFY) < workflow.index("gh release create")


def test_m39_adds_no_runner_action_permission_trigger_or_ci_change() -> None:
    ci = _CI.read_text(encoding="utf-8")
    release = _RELEASE.read_text(encoding="utf-8")

    assert hashlib.sha256(_CI.read_bytes()).hexdigest() == _CI_SHA256
    assert release.count("\n    runs-on:") == 2
    assert release.count("uses: actions/checkout@") == 2
    assert release.count("uses: astral-sh/setup-uv@") == 2
    assert release.count("uses: actions/attest@") == 2
    assert release.count("uses: actions/upload-artifact@") == 1
    assert "attestations: write" in release
    assert "contents: write" in release
    assert "id-token: write" in release
    assert 'tags:\n      - "v*"' in release
    assert "pull_request:" not in release
    assert "workflow_dispatch:" not in release
    assert "schedule:" not in release
    assert ci.count("\n    runs-on:") == 2


def test_m39_changes_no_runtime_dependency_lock_or_version_boundary() -> None:
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert not any(
        "m39" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m39_docs_define_signature_authority_and_nonclaims() -> None:
    readme = (_ROOT / "README.md").read_text(encoding="utf-8")
    architecture = (_ROOT / "docs" / "architecture.md").read_text(encoding="utf-8")
    release = (_ROOT / "docs" / "release-process.md").read_text(encoding="utf-8")
    security = (_ROOT / "SECURITY.md").read_text(encoding="utf-8")
    rfc = (_ROOT / "docs" / "rfcs" / "0022-enforce-release-tag-integrity.md").read_text(
        encoding="utf-8"
    )

    for text in (readme, architecture, release, security, rfc):
        folded = text.casefold()
        assert "m39" in folded
        assert "annotated" in folded
        assert "origin/main" in folded
        assert "signature" in folded
    assert "github" in rfc.casefold()
    assert "key allowlist" in rfc.casefold()
    assert "no additional runner allocation" in " ".join(rfc.split())
    assert "**Status:** Accepted" in rfc
