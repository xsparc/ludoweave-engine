"""Protect M44 exact-source attestation verification and bounded ownership."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github" / "workflows" / "ci.yml"
_RELEASE = _ROOT / ".github" / "workflows" / "release.yml"
_VERIFY = _ROOT / "scripts" / "verify_release_attestations.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"


def _step(source: str, name: str, next_name: str | None = None) -> str:
    start = source.index(f"      - name: {name}\n")
    if next_name is None:
        return source[start:]
    return source[start : source.index(f"      - name: {next_name}\n", start + 1)]


def test_attestations_are_verified_after_exact_asset_retrieval() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    retrieval = _step(
        workflow,
        "Retrieve and verify published release assets",
        "Verify published release attestations",
    )
    attestations = _step(
        workflow,
        "Verify published release attestations",
        "Verify public release consumer path",
    )

    assert "scripts/verify_release_draft.py" in retrieval
    assert '"$download_dir" "$RUNNER_TEMP/release-published.json"' in retrieval
    assert "GH_TOKEN: ${{ github.token }}" in attestations
    assert "scripts/verify_release_attestations.py" in attestations
    assert '"$RUNNER_TEMP/release-download"' in attestations
    assert '"$RUNNER_TEMP/release-assets.plan"' in attestations
    assert '--expected-tag "$GITHUB_REF_NAME"' in attestations
    assert '--expected-commit "$GITHUB_SHA"' in attestations

    required = (
        "Attest release artifacts",
        "Attest wheel SBOM",
        "Publish verified GitHub prerelease",
        "Verify published GitHub prerelease",
        "Retrieve and verify published release assets",
        "Verify published release attestations",
    )
    offsets = [workflow.index(name) for name in required]
    assert offsets == sorted(offsets)


def test_attestation_verifier_is_exact_bounded_and_content_silent() -> None:
    verifier = _VERIFY.read_text(encoding="utf-8")

    for required in (
        '"ludoweave.release-attestation-integrity/1"',
        '"ludoweave.release-asset-retrieval-plan/1"',
        '"xsparc/ludoweave-engine"',
        '"xsparc/ludoweave-engine/.github/workflows/release.yml"',
        '"https://slsa.dev/provenance/v1"',
        '"https://spdx.dev/Document/v2.3"',
        '"https://token.actions.githubusercontent.com"',
        '"--signer-workflow"',
        '"--signer-digest"',
        '"--source-ref"',
        '"--source-digest"',
        '"--cert-oidc-issuer"',
        '"--deny-self-hosted-runners"',
        "_MAX_PLAN_BYTES = 16 * 1024",
        "_MAX_ASSETS = 32",
        "_MAX_ASSET_BYTES = 256 * 1024 * 1024",
        "_MAX_TOTAL_BYTES = 512 * 1024 * 1024",
        "_ATTESTATION_LIMIT = 30",
        "_VERIFY_TIMEOUT_SECONDS = 30.0",
        "stdin=subprocess.DEVNULL",
        "stdout=subprocess.DEVNULL",
        "stderr=subprocess.DEVNULL",
    ):
        assert required in verifier

    assert "for asset in assets:" in verifier
    assert "files[wheel_names[0]]" in verifier
    assert "len(wheel_names) != 1" in verifier
    assert '"assets": summary.assets' in verifier
    assert '"provenance_checks": summary.provenance_checks' in verifier
    assert '"sbom_checks": summary.sbom_checks' in verifier
    for forbidden in (
        "import requests",
        "import urllib",
        "import socket",
        "shell=True",
        "capture_output=True",
        "text=True",
        "eval(",
        "exec(",
        "gh release",
        "gh api",
        "actions/attest",
    ):
        assert forbidden not in verifier


def test_m44_adds_no_runner_action_permission_trigger_or_dependency() -> None:
    release = _RELEASE.read_text(encoding="utf-8")

    assert hashlib.sha256(_CI.read_bytes()).hexdigest() == _CI_SHA256
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert release.count("\n    runs-on:") == 2
    assert release.count("uses: actions/checkout@") == 2
    assert release.count("uses: astral-sh/setup-uv@") == 2
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


def test_m44_changes_no_runtime_or_public_package_boundary() -> None:
    assert not any(
        "m44" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m44_docs_define_attestation_identity_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0027-verify-published-release-attestations.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8").casefold()
        assert "m44" in text
        assert "attestation" in text

    rfc = paths[-1].read_text(encoding="utf-8")
    normalized = " ".join(rfc.split()).casefold()
    assert "**Status:** Accepted" in rfc
    assert "does not" in normalized
    assert "after publication" in normalized
    for term in (
        "artifact security",
        "independent build",
        "predicate",
        "revocation",
        "job",
        "runner",
        "action",
        "permission",
        "rollback",
    ):
        assert term in normalized
