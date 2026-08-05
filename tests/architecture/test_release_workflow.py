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


def test_ci_keeps_one_complete_distribution_gate_and_minimal_platform_matrix() -> None:
    workflow = _CI.read_text(encoding="utf-8")

    verify_section = workflow.split("  verify:", 1)[1].split("  tests:", 1)[0]
    assert "uv run --frozen pytest -q --ignore=tests/integration/test_wgpu_render.py" in (
        verify_section
    )
    assert "scripts/smoke_wheel.py dist" in verify_section
    assert "scripts/release_artifacts.py dist .tmp/ci-release" in verify_section
    assert "scripts/smoke_release.py .tmp/ci-release" in verify_section

    compatibility_section = workflow.split("  tests:", 1)[1].split("  graphics:", 1)[0]
    assert compatibility_section.count("          - os:") == 4
    assert 'os: ubuntu-latest\n            python: "3.13"' in compatibility_section
    assert 'os: ubuntu-latest\n            python: "3.14"' in compatibility_section
    assert 'os: windows-latest\n            python: "3.14"' in compatibility_section
    assert 'os: macos-latest\n            python: "3.14"' in compatibility_section

    assert "os: [ubuntu-latest, windows-latest, macos-latest]" in workflow
    assert "  wheel-smoke:" not in workflow
    assert "permissions:\n  contents: read" in workflow
    assert "cancel-in-progress: true" in workflow
    assert workflow.count("timeout-minutes:") == 3
    assert workflow.count("enable-cache: true") == 3
    assert workflow.count("persist-credentials: false") == 3
    assert workflow.count("fail-fast: false") == 2
    assert workflow.count("actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd") == 3
    assert workflow.count("astral-sh/setup-uv@08807647e7069bb48b6ef5acd8ec9567f424441b") == 3
