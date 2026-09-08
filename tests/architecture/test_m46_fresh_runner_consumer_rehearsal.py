"""Protect M46 fresh-runner handoff while M47 widens operating-system coverage."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github" / "workflows" / "ci.yml"
_RELEASE = _ROOT / ".github" / "workflows" / "release.yml"
_PUBLIC_SCRIPT = _ROOT / "scripts" / "verify_public_release.py"
_CI_SHA256 = "67fc471f84d7dde8b239bd9e92235a34f780cc3d3370b0dbf451e6a922a027f1"
_PYPROJECT_SHA256 = "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d"
_LOCK_SHA256 = "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18"
_CHECKOUT = "actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd"
_SETUP_UV = "astral-sh/setup-uv@08807647e7069bb48b6ef5acd8ec9567f424441b"
_DOWNLOAD = "actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c"


def _job(source: str, name: str) -> str:
    start = source.index(f"  {name}:\n")
    if name == "release":
        return source[start : source.index("\n  fresh-consumer:\n", start)]
    return source[start:]


def test_fresh_consumer_runs_only_after_successful_release_job() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    release = _job(workflow, "release")
    consumer = _job(workflow, "fresh-consumer")

    assert workflow.index("  release:\n") < workflow.index("  fresh-consumer:\n")
    assert "release_id: ${{ steps.verify_draft.outputs.release_id }}" in release
    assert "release_version: ${{ steps.version.outputs.version }}" in release
    assert "needs: release" in consumer
    assert "timeout-minutes: 25" in consumer
    assert "permissions:\n      contents: read" in consumer
    assert workflow.count("\n    runs-on:") == 2


def test_fresh_consumer_uses_exact_pinned_candidate_handoff() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    consumer = _job(workflow, "fresh-consumer")

    assert workflow.count(f"uses: {_CHECKOUT}") == 2
    assert workflow.count(f"uses: {_SETUP_UV}") == 2
    assert workflow.count("uses: actions/upload-artifact@") == 1
    assert workflow.count(f"uses: {_DOWNLOAD}") == 1
    assert "# v8.0.1" in consumer
    assert "persist-credentials: false" in consumer
    assert 'python-version: "3.12"' in consumer
    assert "enable-cache: false" in consumer
    assert "name: ludoweave-${{ needs.release.outputs.release_version }}" in consumer
    assert "path: .tmp/m47-expected-release" in consumer
    for forbidden in ("github-token:", "run-id:", "repository:", "merge-multiple:"):
        assert forbidden not in consumer


def test_fresh_consumer_reuses_exact_bounded_public_verifier() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    release = _job(workflow, "release")
    consumer = _job(workflow, "fresh-consumer")
    script = _PUBLIC_SCRIPT.read_text(encoding="utf-8")

    assert "python scripts/verify_public_release.py release --use-existing-plan" in release
    assert "RELEASE_ID: ${{ needs.release.outputs.release_id }}" in consumer
    assert "RELEASE_TITLE: LudoWeave ${{ needs.release.outputs.release_version }}" in consumer
    assert "python scripts/verify_public_release.py .tmp/m47-expected-release" in consumer
    assert 'environment.get("GITHUB_REPOSITORY") != _REPOSITORY' in script
    assert "context.use_existing_plan" in script
    assert "elif _path_entry_exists(" in script
    assert 'failure_code="public_release.plan_unavailable"' in script
    assert 'verify_arguments.extend(("--asset-plan", str(plan)))' in script
    assert "_run_release_validator(verify_arguments)" in script
    assert "_run_release_validator(final_arguments)" in script
    assert "_run_release_smoke([str(public_directory)])" in script
    assert "_is_exact_success_status(smoke_result)" in script


def test_fresh_consumer_has_no_release_mutation_or_public_request_credential() -> None:
    consumer = _job(_RELEASE.read_text(encoding="utf-8"), "fresh-consumer")
    script = _PUBLIC_SCRIPT.read_text(encoding="utf-8")

    for forbidden in (
        "GH_TOKEN",
        "GITHUB_TOKEN",
        "github.token",
        "Authorization:",
        "Cookie:",
        "gh release",
        "gh api",
        "retry",
        "clobber",
        "unpublish",
        "delete",
    ):
        assert forbidden not in consumer
    assert 'environment.get("GH_TOKEN")' in script
    assert 'environment.get("GITHUB_TOKEN")' in script
    for forbidden_permission in ("contents: write", "attestations: write", "id-token: write"):
        assert forbidden_permission not in consumer


def test_m46_changes_no_ci_runtime_dependency_or_public_package_boundary() -> None:
    assert hashlib.sha256(_CI.read_bytes()).hexdigest() == _CI_SHA256
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert not any(
        "m46" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m46_docs_define_fresh_runner_rehearsal_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0029-fresh-runner-consumer-rehearsal.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8").casefold()
        assert "m46" in text
        assert "fresh" in text

    normalized = " ".join(paths[-1].read_text(encoding="utf-8").split()).casefold()
    assert "**status:** accepted" in normalized
    for term in (
        "same workflow",
        "not independent",
        "external",
        "cross-platform",
        "future availability",
        "supported release channel",
        "one additional",
        "no release mutation",
    ):
        assert term in normalized
