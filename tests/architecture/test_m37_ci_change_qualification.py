"""Protect M37 change-aware CI qualification and quota boundaries."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_WORKFLOW = _ROOT / ".github" / "workflows" / "ci.yml"
_RELEASE_WORKFLOW_SHA256 = "fd18b22b4363f183bc986bd013db7a139502f93d103725f429a62219f9ce61ca"


def _job_block(source: str, name: str, next_name: str | None = None) -> str:
    start = source.index(f"\n  {name}:\n")
    if next_name is None:
        return source[start:]
    return source[start : source.index(f"\n  {next_name}:\n", start + 1)]


def _step_block(source: str, name: str, next_name: str) -> str:
    start = source.index(f"      - name: {name}\n")
    return source[start : source.index(f"      - name: {next_name}\n", start + 1)]


def test_linux_classifies_from_the_trusted_base_and_fails_closed() -> None:
    workflow = _WORKFLOW.read_text(encoding="utf-8")
    linux = _job_block(workflow, "linux", "desktop")
    classification = _step_block(
        linux,
        "Classify pull-request changes from trusted base",
        "Install managed compatibility CPython versions",
    )

    assert "fetch-depth: 0" in linux
    assert "outputs:\n      substantive: ${{ steps.scope.outputs.substantive }}" in linux
    assert "${{ github.event.pull_request.base.sha }}" in classification
    assert "${{ github.event.pull_request.head.sha }}" in classification
    assert 'git cat-file -e "${BASE_SHA}:scripts/classify_ci_changes.py"' in classification
    assert 'git show "${BASE_SHA}:scripts/classify_ci_changes.py"' in classification
    assert 'python "$RUNNER_TEMP/classify_ci_changes.py"' in classification
    assert "python scripts/classify_ci_changes.py" not in classification
    assert 'echo "substantive=true" >> "$GITHUB_OUTPUT"' in classification
    assert '"reason":"classifier-not-on-base"' in classification


def test_documentation_lane_retains_one_linux_quality_and_distribution_allocation() -> None:
    workflow = _WORKFLOW.read_text(encoding="utf-8")
    linux = _job_block(workflow, "linux", "desktop")

    docs_sync = _step_block(
        linux,
        "Install locked documentation environment",
        "Check formatting",
    )
    docs_tests = _step_block(
        linux,
        "Run documentation architecture tests",
        "Run CPython 3.12 baseline tests",
    )
    assert "if: steps.scope.outputs.substantive != 'true'" in docs_sync
    assert "uv sync --frozen --all-groups" in docs_sync
    assert "--extra graphics" not in docs_sync
    assert "if: steps.scope.outputs.substantive != 'true'" in docs_tests
    assert "pytest -q tests/architecture" in docs_tests
    always_steps = (
        ("Verify lockfile", "Install locked baseline and graphics environment"),
        ("Check formatting", "Lint"),
        ("Lint", "Type check"),
        ("Build documentation", "Run documentation architecture tests"),
        ("Build sdist and wheel", "Smoke-test installed wheel"),
        ("Smoke-test installed wheel", "Stage release candidate"),
        ("Stage release candidate", "Smoke-test release candidate"),
        ("Smoke-test release candidate", "Run Ubuntu CPython 3.13 tests"),
    )
    for name, next_name in always_steps:
        assert "\n        if:" not in _step_block(linux, name, next_name)
    for command in (
        "uv lock --check",
        "ruff format --check .",
        "ruff check .",
        "mkdocs build --strict",
        "uv build",
        "scripts/smoke_wheel.py .tmp/ci-dist-first",
        "scripts/release_artifacts.py .tmp/ci-dist-first .tmp/ci-release",
        "scripts/smoke_release.py .tmp/ci-release",
    ):
        assert command in linux


def test_substantive_lane_retains_every_m36_slice() -> None:
    workflow = _WORKFLOW.read_text(encoding="utf-8")
    linux = _job_block(workflow, "linux", "desktop")
    desktop = _job_block(workflow, "desktop")

    guarded_linux_steps = (
        "Install managed compatibility CPython versions",
        "Install Linux software-rendering runtime",
        "Install locked baseline and graphics environment",
        "Type check",
        "Run CPython 3.12 baseline tests",
        "Run base profiling contract smoke",
        "Run Linux graphics smoke",
        "Run Linux graphics profiling contract smoke",
        "Run Linux Clockwork Arena wgpu vertical slice",
        "Run Linux Agent World Builder typed-tool loop",
        "Run Ubuntu CPython 3.13 tests",
        "Run Ubuntu CPython 3.14 tests",
    )
    for index, name in enumerate(guarded_linux_steps[:-1]):
        block = _step_block(linux, name, guarded_linux_steps[index + 1])
        assert "if: steps.scope.outputs.substantive == 'true'" in block
    last = linux[linux.index(f"      - name: {guarded_linux_steps[-1]}\n") :]
    assert "if: steps.scope.outputs.substantive == 'true'" in last

    assert "needs: linux" in desktop
    assert "if: needs.linux.outputs.substantive == 'true'" in desktop
    assert desktop.count("          - os:") == 2
    assert "          - os: windows-latest" in desktop
    assert "          - os: macos-latest" in desktop
    assert "fail-fast: false" in desktop


def test_workflow_trigger_security_and_allocation_ceiling_remain_fixed() -> None:
    workflow = _WORKFLOW.read_text(encoding="utf-8")

    assert '\non:\n  pull_request:\n    paths-ignore:\n      - ".project/**"\n' in workflow
    assert workflow.count("\n    runs-on:") == 2
    assert workflow.count("          - os:") == 2
    assert workflow.count("uses: actions/checkout@") == 2
    assert workflow.count("uses: astral-sh/setup-uv@") == 2
    assert workflow.count("persist-credentials: false") == 2
    assert workflow.count("enable-cache: true") == 2
    assert workflow.count("timeout-minutes:") == 2
    assert "permissions:\n  contents: read" in workflow
    assert "cancel-in-progress: true" in workflow
    for forbidden in ("\n  push:", "\n  schedule:", "\n  workflow_dispatch:"):
        assert forbidden not in workflow


def test_m37_changes_no_release_or_runtime_boundary() -> None:
    assert (
        hashlib.sha256((_ROOT / ".github" / "workflows" / "release.yml").read_bytes()).hexdigest()
        == _RELEASE_WORKFLOW_SHA256
    )
    assert not any(
        "m37" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m37_public_docs_state_policy_and_non_claims() -> None:
    readme = (_ROOT / "README.md").read_text(encoding="utf-8")
    architecture = (_ROOT / "docs" / "architecture.md").read_text(encoding="utf-8")
    rfc = (_ROOT / "docs" / "rfcs" / "0020-ci-change-qualification.md").read_text(encoding="utf-8")

    for text in (readme, architecture, rfc):
        assert "M37" in text
        assert "documentation-only" in text.casefold()
        assert "substantive" in text.casefold()
    assert "one hosted allocation" in rfc.casefold()
    assert "three hosted allocations" in rfc.casefold()
    substantive_policy = rfc[
        rfc.index("Everything else is substantive") : rfc.index("A documentation-only pull request")
    ]
    assert "`mkdocs.yml`" in substantive_policy
    assert "does not claim" in rfc.casefold()
    assert "**Status:** Accepted" in rfc
