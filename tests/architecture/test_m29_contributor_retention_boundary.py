"""Keep M29 contributor-retention evidence strict, offline, and non-runtime."""

import ast
import hashlib
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave

_ROOT = Path(__file__).parents[2]
_RETENTION = _ROOT / "tests" / "fixtures" / "external_contributor_retention.json"
_EVIDENCE_FILES = (
    _ROOT / "examples" / "external_contributor_retention_readiness.py",
    _ROOT / "scripts" / "external_contributor_retention_evidence.py",
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


def test_retention_manifest_is_exact_empty_and_reviewed() -> None:
    payload = _RETENTION.read_bytes()
    document = cast(dict[str, object], json.loads(payload))

    assert len(payload) == 274
    assert hashlib.sha256(payload).hexdigest() == (
        "61785ec165e9f9a7c1025c37f7b714d6fa42b2c7081145a0f843395a325b36ee"
    )
    assert _literal(_EVIDENCE_FILES[0], "_REVIEWED_RETENTION_SHA256") == (
        "61785ec165e9f9a7c1025c37f7b714d6fa42b2c7081145a0f843395a325b36ee"
    )
    assert _literal(_EVIDENCE_FILES[0], "_MANDATORY_RETENTION_PREFIX") == ()
    assert document == {
        "schema": "ludoweave.community.external-contributor-retention/1",
        "source_project": "ludoweave-engine",
        "minimum_retained_contributors": 1,
        "required_validation_steps": [
            "clean-setup",
            "focused-check",
            "complete-gate",
        ],
        "retention_records": [],
    }


def test_retention_evidence_files_have_no_ambient_external_dependency() -> None:
    assert _literal(_EVIDENCE_FILES[0], "_MAX_JSON_NESTING") == 16
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


def test_m29_adds_no_runtime_export_dependency_version_release_or_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["version"] == "0.1.0a1"
    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
    assert "ContributorRetention" not in ludoweave.__all__
    assert not any(
        "contributor_retention" in path.name for path in (_ROOT / "src/ludoweave").rglob("*")
    )
    assert hashlib.sha256((_ROOT / ".github/workflows/release.yml").read_bytes()).hexdigest() == (
        "a5c7ff3f80010cad2712592daf32327b80122b8473cee720fe066bbb3eb06e06"
    )


def test_public_contract_retains_zero_retained_external_contributors() -> None:
    expected = {
        _ROOT / "README.md": "empty reviewed contributor-retention manifest",
        _ROOT / "ROADMAP.md": "M29 contributor-retention admission readiness",
        _ROOT / "docs" / "architecture.md": "M29 contributor-retention boundary",
        _ROOT / "docs" / "external-contributor-retention-readiness.md": (
            "No retained external contributor is currently admitted"
        ),
        _ROOT / "docs" / "rfcs" / "0012-external-contributor-retention-admission-readiness.md": (
            "reviewed manifest contains no retention records"
        ),
    }
    for path, text in expected.items():
        assert text in path.read_text(encoding="utf-8")


def test_source_wheel_and_release_smoke_explicitly_include_m29_evidence() -> None:
    checks = {
        _ROOT / "scripts" / "smoke_wheel.py": (
            "validate_external_contributor_retention_evidence",
            "external_contributor_retention_readiness.py",
            "external_contributor_retention.json",
        ),
        _ROOT / "scripts" / "smoke_release.py": (
            "validate_external_contributor_retention_evidence",
            "external_contributor_retention_readiness.py",
        ),
        _ROOT / "scripts" / "release_artifacts.py": (
            "external_contributor_retention_readiness.py",
            "external_contributor_retention.json",
        ),
        _ROOT / "tests" / "unit" / "test_release_artifacts.py": (
            "external_contributor_retention_readiness.py",
            "external_contributor_retention.json",
        ),
    }
    for path, fragments in checks.items():
        source = path.read_text(encoding="utf-8")
        for fragment in fragments:
            assert fragment in source
