"""Protect M36 CI quota consolidation without coverage loss."""

from pathlib import Path

_ROOT = Path(__file__).parents[2]
_WORKFLOW = _ROOT / ".github" / "workflows" / "ci.yml"
_RELEASE_WORKFLOW_SHA256 = "3e82735e95120ab3fcbd9d2f0b658765a2e524e808d8b64a25062e799454dfae"


def _job_block(source: str, name: str, next_name: str | None = None) -> str:
    start = source.index(f"\n  {name}:\n")
    if next_name is None:
        return source[start:]
    return source[start : source.index(f"\n  {next_name}:\n", start + 1)]


def test_m36_allocates_exactly_one_linux_and_two_desktop_runners() -> None:
    workflow = _WORKFLOW.read_text(encoding="utf-8")
    linux = _job_block(workflow, "linux", "desktop")
    desktop = _job_block(workflow, "desktop")

    assert workflow.count("\n    runs-on:") == 2
    assert "runs-on: ubuntu-latest" in linux
    assert "runs-on: ${{ matrix.os }}" in desktop
    assert desktop.count("          - os:") == 2
    assert "          - os: windows-latest" in desktop
    assert "          - os: macos-latest" in desktop
    assert "fail-fast: false" in desktop
    assert workflow.count("uses: actions/checkout@") == 2
    assert workflow.count("uses: astral-sh/setup-uv@") == 2


def test_m36_preserves_every_version_and_platform_validation_slice() -> None:
    workflow = _WORKFLOW.read_text(encoding="utf-8")
    linux = _job_block(workflow, "linux", "desktop")
    desktop = _job_block(workflow, "desktop")

    assert 'python-version: "3.12"' in linux
    assert "uv python install 3.13 3.14" in linux
    assert linux.index("uv python install 3.13 3.14") < linux.index(
        "uv sync --frozen --all-groups --extra graphics"
    )
    assert "uv sync --frozen --all-groups --python 3.13" in linux
    assert "uv run --frozen --python 3.13 pytest -q" in linux
    assert "uv sync --frozen --all-groups --python 3.14" in linux
    assert "uv run --frozen --python 3.14 pytest -q" in linux
    assert 'python-version: "3.12"' in desktop
    assert "uv python install 3.14" in desktop
    assert desktop.index("uv python install 3.14") < desktop.index(
        "uv sync --frozen --all-groups --extra graphics"
    )
    assert "uv sync --frozen --all-groups --python 3.14" in desktop
    assert "uv run --frozen --python 3.14 pytest -q" in desktop


def test_m36_preserves_quality_distribution_and_three_graphics_slices() -> None:
    workflow = _WORKFLOW.read_text(encoding="utf-8")
    linux = _job_block(workflow, "linux", "desktop")
    desktop = _job_block(workflow, "desktop")

    for command in (
        "uv lock --check",
        "ruff format --check .",
        "ruff check .",
        "pyright",
        "mkdocs build --strict",
        "pytest -q --ignore=tests/integration/test_wgpu_render.py",
        "benchmarks.profile_m7 --repeats 1 --output",
        "uv build",
        "scripts/smoke_wheel.py .tmp/ci-dist-first",
        "scripts/release_artifacts.py .tmp/ci-dist-first .tmp/ci-release",
        "scripts/smoke_release.py .tmp/ci-release",
    ):
        assert command in linux
    for command in (
        "pytest -q tests/integration/test_wgpu_render.py",
        "benchmarks.profile_m7 --repeats 1 --include-wgpu",
        "examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10",
        "examples/agent_world_builder.py",
    ):
        assert command in linux
        assert command in desktop


def test_m36_retains_trigger_security_pins_timeouts_and_cache() -> None:
    workflow = _WORKFLOW.read_text(encoding="utf-8")

    assert '\non:\n  pull_request:\n    paths-ignore:\n      - ".project/**"\n' in workflow
    for forbidden in ("\n  push:", "\n  schedule:", "\n  workflow_dispatch:"):
        assert forbidden not in workflow
    assert "permissions:\n  contents: read" in workflow
    assert "cancel-in-progress: true" in workflow
    assert workflow.count("persist-credentials: false") == 2
    assert workflow.count("timeout-minutes:") == 2
    assert workflow.count("enable-cache: true") == 2
    assert workflow.count("cache-dependency-glob: uv.lock") == 2
    assert workflow.count("actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd") == 2
    assert workflow.count("astral-sh/setup-uv@08807647e7069bb48b6ef5acd8ec9567f424441b") == 2


def test_m36_changes_no_release_or_runtime_boundary() -> None:
    import hashlib

    assert hashlib.sha256(
        (_ROOT / ".github" / "workflows" / "release.yml").read_bytes()
    ).hexdigest() == (_RELEASE_WORKFLOW_SHA256)
    assert not any(
        "m36" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m36_docs_state_three_allocations_and_preserved_slices() -> None:
    readme = (_ROOT / "README.md").read_text(encoding="utf-8")
    architecture = (_ROOT / "docs" / "architecture.md").read_text(encoding="utf-8")
    rfc = (_ROOT / "docs" / "rfcs" / "0019-ci-runner-consolidation.md").read_text(encoding="utf-8")

    for text in (readme, architecture, rfc):
        assert "M36" in text
        assert "three" in text.casefold()
        assert "eight validation slices" in text.casefold()
    assert "five fewer runner allocations" in " ".join(readme.casefold().split())
    assert "**Status:** Accepted" in rfc
