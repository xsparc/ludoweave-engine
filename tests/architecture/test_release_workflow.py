"""Release automation remains pinned, least-privilege, and evidence-gated."""

from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_RELEASE = _ROOT / ".github" / "workflows" / "release.yml"
_CI = _ROOT / ".github" / "workflows" / "ci.yml"


def test_release_workflow_is_tag_only_and_pinned() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")

    assert 'tags:\n      - "v*"' in workflow
    assert "pull_request:" not in workflow
    assert "branches:" not in workflow
    assert "contents: read" in workflow
    assert "attestations: write" in workflow
    assert "contents: write" in workflow
    assert "id-token: write" in workflow
    assert "persist-credentials: false" in workflow
    assert "actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd" in workflow
    assert "astral-sh/setup-uv@08807647e7069bb48b6ef5acd8ec9567f424441b" in workflow
    assert workflow.count("actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6") == 2
    assert "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a" in workflow
    assert "uses: actions/checkout@v" not in workflow
    assert "uses: astral-sh/setup-uv@v" not in workflow
    assert "uses: actions/attest@v" not in workflow
    assert "uses: actions/upload-artifact@v" not in workflow


def test_release_workflow_validates_before_publishing() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    required = (
        "uv lock --check",
        "ruff format --check .",
        "ruff check .",
        "pyright",
        "pytest -q",
        "mkdocs build --strict",
        "uv build",
        "scripts/smoke_wheel.py dist",
        "scripts/release_artifacts.py dist release --tag",
        "scripts/smoke_release.py release",
        "gh release create",
    )

    offsets = [workflow.index(command) for command in required]
    assert offsets == sorted(offsets)
    assert 'test "$GITHUB_REF_NAME" = "v$version"' in workflow
    assert "--verify-tag" in workflow
    assert "--prerelease" in workflow
    assert "--notes-file release/RELEASE_NOTES.md" in workflow


def test_cross_platform_wheel_jobs_smoke_complete_release_candidate() -> None:
    workflow = _CI.read_text(encoding="utf-8")

    assert "os: [ubuntu-latest, windows-latest, macos-latest]" in workflow
    wheel_section = workflow.split("  wheel-smoke:", 1)[1].split("  graphics:", 1)[0]
    assert "scripts/smoke_wheel.py dist" in wheel_section
    assert "scripts/release_artifacts.py dist .tmp/ci-release" in wheel_section
    assert "scripts/smoke_release.py .tmp/ci-release" in wheel_section
