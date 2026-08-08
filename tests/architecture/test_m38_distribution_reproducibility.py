"""Protect M38 distribution reproducibility and hosted-allocation boundaries."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github" / "workflows" / "ci.yml"
_RELEASE = _ROOT / ".github" / "workflows" / "release.yml"
_VERIFY = "scripts/verify_distribution_reproducibility.py"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"


def _step(source: str, name: str, next_name: str) -> str:
    start = source.index(f"      - name: {name}\n")
    return source[start : source.index(f"      - name: {next_name}\n", start + 1)]


def test_ci_builds_twice_and_verifies_before_wheel_smoke() -> None:
    workflow = _CI.read_text(encoding="utf-8")
    build = _step(workflow, "Build sdist and wheel", "Smoke-test installed wheel")

    assert build.count("uv build") == 2
    assert "uv build --out-dir .tmp/ci-dist-first" in build
    assert "uv build --out-dir .tmp/ci-dist-second" in build
    assert f"uv run --frozen python {_VERIFY} .tmp/ci-dist-first .tmp/ci-dist-second" in build
    assert workflow.index(_VERIFY) < workflow.index("scripts/smoke_wheel.py .tmp/ci-dist-first")


def test_release_builds_twice_and_verifies_before_staging_or_attestation() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    build = _step(
        workflow,
        "Build source and wheel distributions",
        "Smoke-test installed wheel",
    )

    assert build.count("uv build") == 2
    assert "uv build --out-dir .tmp/release-dist-first" in build
    assert "uv build --out-dir .tmp/release-dist-second" in build
    assert (
        f"uv run --frozen python {_VERIFY} .tmp/release-dist-first .tmp/release-dist-second"
        in build
    )
    assert workflow.index(_VERIFY) < workflow.index("scripts/release_artifacts.py")
    assert workflow.index(_VERIFY) < workflow.index("actions/attest@")


def test_m38_adds_no_hosted_runner_action_permission_or_trigger() -> None:
    ci = _CI.read_text(encoding="utf-8")
    release = _RELEASE.read_text(encoding="utf-8")

    assert ci.count("\n    runs-on:") == 2
    assert ci.count("          - os:") == 2
    assert ci.count("uses: actions/checkout@") == 2
    assert ci.count("uses: astral-sh/setup-uv@") == 2
    assert "permissions:\n  contents: read" in ci
    assert "\n  push:" not in ci
    assert "\n  schedule:" not in ci
    assert "\n  workflow_dispatch:" not in ci

    assert release.count("\n    runs-on:") == 2
    assert release.count("uses: actions/checkout@") == 2
    assert release.count("uses: astral-sh/setup-uv@") == 2
    assert release.count("uses: actions/attest@") == 2
    assert "attestations: write" in release
    assert "contents: write" in release
    assert "id-token: write" in release
    assert 'tags:\n      - "v*"' in release
    assert "pull_request:" not in release


def test_m38_changes_no_runtime_dependency_lock_or_version_boundary() -> None:
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert not any(
        "m38" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m38_docs_define_the_bounded_claim_and_nonclaims() -> None:
    readme = (_ROOT / "README.md").read_text(encoding="utf-8")
    architecture = (_ROOT / "docs" / "architecture.md").read_text(encoding="utf-8")
    release = (_ROOT / "docs" / "release-process.md").read_text(encoding="utf-8")
    rfc = (_ROOT / "docs" / "rfcs" / "0021-enforce-distribution-reproducibility.md").read_text(
        encoding="utf-8"
    )

    for text in (readme, architecture, release, rfc):
        assert "M38" in text
        assert "reproduc" in text.casefold()
        assert "cross-platform" in text.casefold()
    assert "same-source" in rfc
    assert "no additional runner allocation" in " ".join(rfc.split())
    assert "**Status:** Accepted" in rfc
