"""Protect M43 exact-ID asset retrieval and bounded hosted ownership."""

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


def test_published_assets_are_retrieved_by_validated_exact_id_and_reverified() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    published = _step(
        workflow,
        "Verify published GitHub prerelease",
        "Retrieve and verify published release assets",
    )
    retrieval = _step(
        workflow,
        "Retrieve and verify published release assets",
        "Verify published release attestations",
    )

    assert '"$RUNNER_TEMP/release-published.json"' in published
    assert '--asset-plan "$RUNNER_TEMP/release-assets.plan"' in published
    assert "--expected-state published" in published
    assert 'test "$protocol" = "ludoweave.release-asset-retrieval-plan/1"' in retrieval
    assert 'exec 3< "$plan"' in retrieval
    assert "IFS=$'\\t' read -r asset_id expected_bytes asset_name <&3" in retrieval
    assert "^[1-9][0-9]{0,18}$" in retrieval
    assert '"9223372036854775807"' in retrieval
    assert 'test "$asset_count" -lt 32' in retrieval
    assert "^(0|[1-9][0-9]{0,8})$" in retrieval
    assert '"268435456"' in retrieval
    assert 'test "$expected_total" -le 536870912' in retrieval
    assert "^[0-9A-Za-z][0-9A-Za-z._+-]{0,255}$" in retrieval
    assert 'test ! -e "$target"' in retrieval
    assert 'test ! -e "$partial"' in retrieval
    assert '"Accept: application/octet-stream"' in retrieval
    assert '"repos/$GITHUB_REPOSITORY/releases/assets/$asset_id"' in retrieval
    assert 'head -c "$((expected_bytes + 1))"' in retrieval
    assert 'test "$(wc -c < "$partial")" -eq "$expected_bytes"' in retrieval
    assert 'mv "$partial" "$target"' in retrieval
    assert 'test "$asset_count" -gt 0' in retrieval
    assert '"$download_dir" "$RUNNER_TEMP/release-published.json"' in retrieval
    assert "--expected-state published" in retrieval
    assert "--asset-plan" not in retrieval
    assert published.count("scripts/verify_release_draft.py") == 1
    assert retrieval.count("scripts/verify_release_draft.py") == 1
    assert published.count("X-GitHub-Api-Version: 2026-03-10") == 1
    assert retrieval.count("X-GitHub-Api-Version: 2026-03-10") == 1

    for forbidden in (
        "gh release download",
        "/releases/tags/",
        "browser_download_url",
        "--clobber",
        "gh release delete",
        "gh release upload",
        "gh release edit",
        "--method PATCH",
        "--method POST",
        "--method DELETE",
        "curl ",
        "wget ",
        "eval ",
    ):
        assert forbidden not in retrieval

    required = (
        "Verify draft release asset integrity",
        "Publish verified GitHub prerelease",
        "Verify published GitHub prerelease",
        "Retrieve and verify published release assets",
    )
    offsets = [workflow.index(name) for name in required]
    assert offsets == sorted(offsets)


def test_release_validator_emits_only_a_bounded_no_clobber_plan() -> None:
    verifier = _VERIFY.read_text(encoding="utf-8")

    assert '"ludoweave.release-draft-integrity/4"' in verifier
    assert '"ludoweave.release-asset-retrieval-plan/1"' in verifier
    assert "_MAX_ASSET_ID = (1 << 63) - 1" in verifier
    assert "type(value) is not int" in verifier
    assert 'parser.add_argument(\n        "--asset-plan"' in verifier
    assert 'if state != "published"' in verifier
    assert 'target.open("x"' in verifier
    assert 'code="release_draft.plan_write_failed"' in verifier
    assert 'f"{item.asset_id}\\t{item.bytes}\\t{item.name}\\n"' in verifier
    assert '"asset_id"' not in verifier[verifier.index("print(\n        _json(") :]
    for forbidden in (
        "import requests",
        "import urllib",
        "import socket",
        "subprocess",
        "browser_download_url",
        "http://",
        "https://",
    ):
        assert forbidden not in verifier


def test_m43_adds_no_runner_action_permission_trigger_or_dependency() -> None:
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


def test_m43_changes_no_runtime_or_public_package_boundary() -> None:
    assert not any(
        "m43" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m43_docs_define_authenticated_retrieval_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0026-verify-published-release-asset-retrieval.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8").casefold()
        assert "m43" in text
        assert "asset" in text
        assert "retriev" in text

    rfc = paths[-1].read_text(encoding="utf-8")
    normalized = " ".join(rfc.split()).casefold()
    assert "**Status:** Accepted" in rfc
    assert "does not" in normalized
    assert "unauthenticated" in normalized
    for term in ("job", "runner", "action", "permission"):
        assert term in normalized
    assert "after publication" in normalized
