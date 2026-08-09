"""Protect M45 credential-free public retrieval and installed consumer smoke."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github" / "workflows" / "ci.yml"
_RELEASE = _ROOT / ".github" / "workflows" / "release.yml"
_PUBLIC_SCRIPT = _ROOT / "scripts" / "verify_public_release.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"


def test_public_consumer_path_follows_attestation_verification() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    public_start = workflow.index("      - name: Verify public release consumer path\n")
    public = workflow[public_start : workflow.index("\n\n  fresh-consumer:", public_start)]
    script = _PUBLIC_SCRIPT.read_text(encoding="utf-8")

    required = (
        "Publish verified GitHub prerelease",
        "Verify published GitHub prerelease",
        "Retrieve and verify published release assets",
        "Verify published release attestations",
        "Verify public release consumer path",
    )
    offsets = [workflow.index(name) for name in required]
    assert offsets == sorted(offsets)

    assert "RELEASE_ID: ${{ steps.verify_draft.outputs.release_id }}" in public
    assert "python scripts/verify_public_release.py release --use-existing-plan" in public
    assert '_ID_PATTERN = re.compile(r"[1-9][0-9]{0,18}")' in script
    assert "_MAX_RELEASE_ID = (1 << 63) - 1" in script
    assert 'public_document = context.runner_temp / "release-public.json"' in script
    assert 'public_directory = context.runner_temp / "release-public-download"' in script


def test_public_document_and_assets_use_exact_bounded_https_requests() -> None:
    public = _PUBLIC_SCRIPT.read_text(encoding="utf-8")

    for required in (
        "http.client.HTTPSConnection",
        "ssl.create_default_context()",
        "_MAX_ASSET_REDIRECTS = 3",
        "_CONNECT_TIMEOUT_SECONDS = 10.0",
        "_REQUEST_TIMEOUT_SECONDS = 30.0",
        '"Accept": accept',
        '"Accept-Encoding": "identity"',
        '"Connection": "close"',
        'headers["X-GitHub-Api-Version"] = _API_VERSION',
        'f"https://{_API_HOST}/repos/{_REPOSITORY}/releases/{context.release_id}"',
        'f"https://{_API_HOST}/repos/{_REPOSITORY}/releases/assets/{item.asset_id}"',
        "maximum_bytes=_MAX_DOCUMENT_BYTES",
        "maximum_bytes=item.bytes",
        "expected_bytes=item.bytes",
    ):
        assert required in public

    for forbidden in (
        "import requests",
        "import urllib.request",
        "browser_download_url",
        "Authorization",
        "Cookie",
        "gh api",
        "gh release",
        "http://",
        "subprocess",
        "eval(",
    ):
        assert forbidden not in public
    assert 'environment.get("GH_TOKEN")' in public
    assert 'environment.get("GITHUB_TOKEN")' in public
    assert "http.client.HTTPException" in public


def test_public_retrieval_revalidates_plan_set_and_installed_candidate() -> None:
    public = _PUBLIC_SCRIPT.read_text(encoding="utf-8")

    for required in (
        'plan = context.runner_temp / "release-assets.plan"',
        '"ludoweave.release-asset-retrieval-plan/1"',
        "_MAX_ASSETS = 32",
        "_MAX_ASSET_BYTES = 256 * 1024 * 1024",
        "_MAX_TOTAL_BYTES = 512 * 1024 * 1024",
        'fields = line.split("\\t")',
        "asset_id in asset_ids",
        "name in names",
        "total > _MAX_TOTAL_BYTES",
        'partial_name=f".asset-{item.asset_id}.part"',
        "os.link(partial, target)",
        "_run_release_validator(verify_arguments)",
        "_run_release_validator(final_arguments)",
        "smoke_release.main([str(public_directory)])",
    ):
        assert required in public

    assert public.index("_run_release_validator(verify_arguments)") < public.index(
        "for item in items:"
    )
    assert public.index("_run_release_validator(final_arguments)") < public.index(
        "smoke_release.main([str(public_directory)])"
    )


def test_m45_publication_authority_and_package_boundary_remain_stable() -> None:
    release = _RELEASE.read_text(encoding="utf-8")
    public = _PUBLIC_SCRIPT.read_text(encoding="utf-8")

    assert hashlib.sha256(_CI.read_bytes()).hexdigest() == _CI_SHA256
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert "if: github.repository == 'xsparc/ludoweave-engine'" in release
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
    assert "gh " not in public


def test_m45_changes_no_runtime_or_public_package_boundary() -> None:
    assert not any(
        "m45" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m45_docs_define_public_consumer_path_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0028-verify-public-release-consumer-path.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8").casefold()
        assert "m45" in text
        assert "public" in text

    rfc = paths[-1].read_text(encoding="utf-8")
    normalized = " ".join(rfc.split()).casefold()
    assert "**status:** accepted" in normalized
    assert "without a github credential" in normalized
    assert "does not" in normalized
    for term in (
        "independent",
        "future availability",
        "immutability",
        "supported release channel",
        "job",
        "runner",
        "action",
        "permission",
        "publication",
    ):
        assert term in normalized
