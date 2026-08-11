"""Keep M33 benchmark-regression-rate evidence strict, offline, and non-runtime."""

import ast
import hashlib
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave

_ROOT = Path(__file__).parents[2]
_MANIFEST = _ROOT / "tests" / "fixtures" / "benchmark_regression_rate.json"
_EVIDENCE_FILES = (
    _ROOT / "examples" / "benchmark_regression_rate_readiness.py",
    _ROOT / "scripts" / "benchmark_regression_rate_evidence.py",
)
_FORBIDDEN_IMPORTS = {
    "http",
    "importlib",
    "multiprocessing",
    "numpy",
    "os",
    "requests",
    "socket",
    "sqlite3",
    "subprocess",
    "time",
    "urllib",
    "webbrowser",
    "ludoweave.benchmark",
    "ludoweave.plugins",
    "ludoweave.render.backends",
    "ludoweave.tools",
}
_GRAPHICS_DEPENDENCIES = [
    "glfw==2.10.2",
    "rendercanvas[glfw]==2.7.2",
    "wgpu==0.32.0",
]


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imports.add(node.module)
    return imports


def _forbidden(imports: set[str]) -> set[str]:
    return {
        imported
        for imported in imports
        if any(imported == name or imported.startswith(f"{name}.") for name in _FORBIDDEN_IMPORTS)
    }


def _literal(path: Path, name: str) -> object:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for statement in tree.body:
        if isinstance(statement, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in statement.targets
        ):
            return ast.literal_eval(statement.value)
        if (
            isinstance(statement, ast.AnnAssign)
            and isinstance(statement.target, ast.Name)
            and statement.target.id == name
            and statement.value is not None
        ):
            return ast.literal_eval(statement.value)
    raise AssertionError(f"{name} was not a literal assignment")


def test_benchmark_regression_manifest_is_exact_empty_and_reviewed() -> None:
    payload = _MANIFEST.read_bytes()
    document = cast(dict[str, object], json.loads(payload))

    assert len(payload) == 199
    assert hashlib.sha256(payload).hexdigest() == (
        "720ae794e2a4ba76303196cd43d6ba0f3b21f81cffd4fa8584f526e2a0d48dca"
    )
    assert _literal(_EVIDENCE_FILES[0], "_REVIEWED_MANIFEST_SHA256") == (
        "720ae794e2a4ba76303196cd43d6ba0f3b21f81cffd4fa8584f526e2a0d48dca"
    )
    assert _literal(_EVIDENCE_FILES[0], "_MANDATORY_WINDOW_PREFIX") == ()
    assert document == {
        "schema": "ludoweave.performance.benchmark-regression-rate/1",
        "source_project": "ludoweave-engine",
        "measurement_policy": "complete-reviewed-controlled-benchmark-comparisons/1",
        "evaluation_windows": [],
    }


def test_benchmark_regression_evidence_files_are_bounded_and_offline() -> None:
    assert _literal(_EVIDENCE_FILES[0], "_MAX_MANIFEST_BYTES") == 131_072
    assert _literal(_EVIDENCE_FILES[0], "_MAX_JSON_NESTING") == 16
    assert _literal(_EVIDENCE_FILES[0], "_MAX_EVALUATION_WINDOWS") == 12
    assert _literal(_EVIDENCE_FILES[0], "_MAX_COMPARISONS_PER_WINDOW") == 512
    for path in _EVIDENCE_FILES:
        assert _forbidden(_imports(path)) == set()


@pytest.mark.parametrize(
    "source",
    [
        "def nested() -> None:\n    import socket\n",
        "if True:\n    from importlib import import_module\n",
        "try:\n    import subprocess\nexcept ImportError:\n    pass\n",
        "from urllib.parse import urlparse\n",
        "from ludoweave.tools import cli\n",
    ],
)
def test_import_scan_detects_nested_forbidden_fixtures(tmp_path: Path, source: str) -> None:
    fixture = tmp_path / "invalid_evidence.py"
    fixture.write_text(source, encoding="utf-8")

    assert _forbidden(_imports(fixture))


def test_m33_adds_no_runtime_export_dependency_version_release_or_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["version"] == "0.1.0a1"
    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
    assert "BenchmarkRegressionRate" not in ludoweave.__all__
    assert not any(
        "benchmark_regression_rate" in path.name
        for path in (_ROOT / "src" / "ludoweave").rglob("*")
    )
    assert hashlib.sha256((_ROOT / ".github/workflows/release.yml").read_bytes()).hexdigest() == (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    )


def test_evaluator_registers_exact_perf_counter_benchmark_sources_only() -> None:
    evaluator = _EVIDENCE_FILES[0].read_text(encoding="utf-8")

    for source in (
        "benchmarks/benchmark_m1.py",
        "benchmarks/benchmark_m2.py",
        "benchmarks/benchmark_m3.py",
        "benchmarks/benchmark_m4.py",
    ):
        assert source in evaluator
    assert "ludoweave.profile.m7/1" not in evaluator
    assert 'metric != "p95_ns"' in evaluator
    assert "candidate_p95 * 10_000 > baseline_p95 * (10_000 + tolerance_bps)" in evaluator


def test_source_wheel_and_release_smoke_explicitly_include_m33_evidence() -> None:
    checks = {
        _ROOT / "scripts" / "smoke_wheel.py": (
            "validate_benchmark_regression_rate_evidence",
            "benchmark_regression_rate_readiness.py",
            "benchmark_regression_rate.json",
        ),
        _ROOT / "scripts" / "smoke_release.py": (
            "validate_benchmark_regression_rate_evidence",
            "benchmark_regression_rate_readiness.py",
        ),
        _ROOT / "scripts" / "release_artifacts.py": (
            "benchmark_regression_rate_readiness.py",
            "benchmark_regression_rate.json",
        ),
        _ROOT / "tests" / "unit" / "test_release_artifacts.py": (
            "benchmark_regression_rate_readiness.py",
            "benchmark_regression_rate.json",
        ),
    }
    for path, required in checks.items():
        text = path.read_text(encoding="utf-8")
        assert all(item in text for item in required)


def test_m33_public_contract_and_indices_are_registered() -> None:
    required = {
        _ROOT / "README.md": (
            "empty reviewed comparison manifest",
            "no measured regression rate",
        ),
        _ROOT / "ROADMAP.md": (
            "M33 benchmark-regression-rate admission readiness",
            "M7 cProfile output",
        ),
        _ROOT / "MAINTAINERS.md": (
            "M33 adds only strict offline benchmark-regression-rate",
            "M7 cProfile diagnostics are not timing evidence",
        ),
        _ROOT / "docs" / "architecture.md": (
            "M33 benchmark-regression-rate boundary",
            "no comparison count or regression rate is exposed",
        ),
        _ROOT / "docs" / "benchmark-regression-rate-readiness.md": (
            "benchmark-regression-rate-evidence-absent",
            "measured zero-regression result",
            "candidate_p95_ns * 10_000",
        ),
        _ROOT / "docs" / "rfcs" / "0016-benchmark-regression-rate-admission-readiness.md": (
            "reviewed manifest contains no evaluation windows",
            "No project-wide threshold",
            "cProfile attribution documents",
        ),
        _ROOT / "mkdocs.yml": (
            "benchmark-regression-rate-readiness.md",
            "0016-benchmark-regression-rate-admission-readiness.md",
        ),
        _ROOT / "docs" / "rfcs" / "index.md": (
            "RFC-0016: benchmark-regression-rate admission readiness",
        ),
        _ROOT / "docs" / "api-status.md": ("M33 adds no export",),
        _ROOT / "docs" / "release-process.md": ("M33/RFC-0016",),
        _ROOT / "docs" / "alpha-retrospective.md": ("M33 defines",),
        _ROOT / "examples" / "README.md": ("benchmark_regression_rate_readiness.py",),
    }
    for path, values in required.items():
        text = path.read_text(encoding="utf-8")
        assert all(value in text for value in values)


def test_neutral_repository_metadata_convention_remains_active() -> None:
    assert (_ROOT / "MAINTAINERS.md").is_file()
    assert (_ROOT / ".project").is_dir()
