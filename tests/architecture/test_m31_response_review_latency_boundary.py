"""Keep M31 response/review-latency evidence strict, offline, and non-runtime."""

import ast
import hashlib
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave

_ROOT = Path(__file__).parents[2]
_MANIFEST = _ROOT / "tests" / "fixtures" / "response_review_latency.json"
_EVIDENCE_FILES = (
    _ROOT / "examples" / "response_review_latency_readiness.py",
    _ROOT / "scripts" / "response_review_latency_evidence.py",
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


def test_response_review_manifest_is_exact_empty_and_reviewed() -> None:
    payload = _MANIFEST.read_bytes()
    document = cast(dict[str, object], json.loads(payload))

    assert len(payload) == 199
    assert hashlib.sha256(payload).hexdigest() == (
        "bc40bbcc1636229fa2c78aed5f71854d1221fd3c0d33169edc1321dd07e69d4f"
    )
    assert _literal(_EVIDENCE_FILES[0], "_REVIEWED_MANIFEST_SHA256") == (
        "bc40bbcc1636229fa2c78aed5f71854d1221fd3c0d33169edc1321dd07e69d4f"
    )
    assert _literal(_EVIDENCE_FILES[0], "_MANDATORY_WINDOW_PREFIX") == ()
    assert document == {
        "schema": "ludoweave.community.response-review-latency/1",
        "source_project": "ludoweave-engine",
        "measurement_policy": "first-public-human-maintainer-action/1",
        "measurement_windows": [],
    }


def test_response_review_evidence_files_are_bounded_and_offline() -> None:
    assert _literal(_EVIDENCE_FILES[0], "_MAX_MANIFEST_BYTES") == 65_536
    assert _literal(_EVIDENCE_FILES[0], "_MAX_JSON_NESTING") == 16
    assert _literal(_EVIDENCE_FILES[0], "_MAX_MEASUREMENT_WINDOWS") == 12
    assert _literal(_EVIDENCE_FILES[0], "_MAX_MEASUREMENTS_PER_WINDOW") == 256
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


def test_m31_adds_no_runtime_export_dependency_version_workflow_or_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["version"] == "0.1.0a1"
    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
    assert "ResponseReviewLatency" not in ludoweave.__all__
    assert not any(
        "response_review_latency" in path.name for path in (_ROOT / "src/ludoweave").rglob("*")
    )
    assert hashlib.sha256((_ROOT / ".github/workflows/ci.yml").read_bytes()).hexdigest() == (
        "06a5e07918c83fc8de61e6746cb344f865b6421d81f554d79f4455d3718a3b21"
    )
    assert hashlib.sha256((_ROOT / ".github/workflows/release.yml").read_bytes()).hexdigest() == (
        "d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8"
    )


def test_public_contract_retains_empty_measurement_manifest_and_no_sla() -> None:
    expected = {
        _ROOT / "README.md": (
            "empty reviewed measurement manifest",
            "no response-time, review-time, or SLA claim",
        ),
        _ROOT / "ROADMAP.md": (
            "M31 response/review-latency admission readiness",
            "or SLA is claimed",
        ),
        _ROOT / "MAINTAINERS.md": (
            "M31 adds only strict offline issue-response",
            "support, or responsiveness result may be claimed",
        ),
        _ROOT / "docs" / "architecture.md": (
            "M31 response/review-latency boundary",
            "defines no\nSLA",
        ),
        _ROOT / "docs" / "response-review-latency-readiness.md": (
            "response-review-latency-evidence-absent",
            "no target, service-level objective",
        ),
        _ROOT / "docs" / "rfcs" / "0014-response-review-latency-admission-readiness.md": (
            "reviewed manifest contains no measurement windows",
            "No latency threshold, SLA",
        ),
    }
    for path, required in expected.items():
        content = path.read_text(encoding="utf-8")
        assert all(text in content for text in required)


def test_source_wheel_and_release_smoke_explicitly_include_m31_evidence() -> None:
    checks = {
        _ROOT / "scripts" / "smoke_wheel.py": (
            "validate_response_review_latency_evidence",
            "response_review_latency_readiness.py",
            "response_review_latency.json",
        ),
        _ROOT / "scripts" / "smoke_release.py": (
            "validate_response_review_latency_evidence",
            "response_review_latency_readiness.py",
        ),
        _ROOT / "scripts" / "release_artifacts.py": (
            "response_review_latency_readiness.py",
            "response_review_latency.json",
        ),
        _ROOT / "tests" / "unit" / "test_release_artifacts.py": (
            "response_review_latency_readiness.py",
            "response_review_latency.json",
        ),
    }
    for path, required in checks.items():
        text = path.read_text(encoding="utf-8")
        assert all(item in text for item in required)


def test_m31_docs_and_indices_are_registered() -> None:
    required = {
        _ROOT / "mkdocs.yml": (
            "response-review-latency-readiness.md",
            "0014-response-review-latency-admission-readiness.md",
        ),
        _ROOT / "docs" / "rfcs" / "index.md": (
            "RFC-0014: response and review latency admission readiness",
        ),
        _ROOT / "docs" / "api-status.md": ("M31 adds no export",),
        _ROOT / "docs" / "release-process.md": ("M31/RFC-0014",),
        _ROOT / "docs" / "alpha-retrospective.md": ("M31 defines",),
        _ROOT / "examples" / "README.md": ("response_review_latency_readiness.py",),
    }
    for path, values in required.items():
        text = path.read_text(encoding="utf-8")
        assert all(value in text for value in values)
