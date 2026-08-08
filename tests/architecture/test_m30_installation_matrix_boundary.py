"""Keep M30 clean-install matrix evidence strict, offline, and non-runtime."""

import ast
import hashlib
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave

_ROOT = Path(__file__).parents[2]
_MATRIX = _ROOT / "tests" / "fixtures" / "installation_matrix.json"
_EVIDENCE_FILES = (
    _ROOT / "examples" / "installation_matrix_readiness.py",
    _ROOT / "scripts" / "installation_matrix_evidence.py",
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
_ENVIRONMENTS = [
    "ubuntu-cpython-3.12",
    "ubuntu-cpython-3.13",
    "ubuntu-cpython-3.14",
    "macos-cpython-3.12",
    "macos-cpython-3.14",
    "windows-cpython-3.12",
    "windows-cpython-3.14",
]
_CHECKS = ["version", "doctor", "hello-headless", "clockwork-arena-headless"]


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


def test_installation_manifest_is_exact_empty_and_reviewed() -> None:
    payload = _MATRIX.read_bytes()
    document = cast(dict[str, object], json.loads(payload))

    assert len(payload) == 462
    assert hashlib.sha256(payload).hexdigest() == (
        "7c05813a7304e8ff44a009ada37c8e60ff545baec633852fc332e46bdfe03c90"
    )
    assert _literal(_EVIDENCE_FILES[0], "_REVIEWED_MATRIX_SHA256") == (
        "7c05813a7304e8ff44a009ada37c8e60ff545baec633852fc332e46bdfe03c90"
    )
    assert _literal(_EVIDENCE_FILES[0], "_MANDATORY_INSTALLATION_PREFIX") == ()
    assert document == {
        "schema": "ludoweave.community.installation-matrix/1",
        "source_project": "ludoweave-engine",
        "required_environments": _ENVIRONMENTS,
        "required_checks": _CHECKS,
        "installation_records": [],
    }


def test_installation_evidence_files_are_bounded_and_offline() -> None:
    assert _literal(_EVIDENCE_FILES[0], "_MAX_MANIFEST_BYTES") == 65_536
    assert _literal(_EVIDENCE_FILES[0], "_MAX_JSON_NESTING") == 16
    assert _literal(_EVIDENCE_FILES[0], "_MAX_INSTALLATION_RECORDS") == 16
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


def test_m30_adds_no_runtime_export_dependency_version_release_or_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["version"] == "0.1.0a1"
    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
    assert "InstallationMatrix" not in ludoweave.__all__
    assert not any(
        "installation_matrix" in path.name for path in (_ROOT / "src/ludoweave").rglob("*")
    )
    assert hashlib.sha256((_ROOT / ".github/workflows/release.yml").read_bytes()).hexdigest() == (
        "fa6c60642946cc0350f3d2fb78d6918efc4a1ba6f27b54de9f53de3a156c85ae"
    )


def test_public_contract_retains_zero_installation_records() -> None:
    expected = {
        _ROOT / "README.md": "empty reviewed installation-matrix manifest",
        _ROOT / "ROADMAP.md": "M30 installation-matrix admission readiness",
        _ROOT / "docs" / "architecture.md": "M30 installation-matrix boundary",
        _ROOT / "docs" / "installation-matrix-readiness.md": (
            "No published-wheel installation matrix is currently admitted"
        ),
        _ROOT / "docs" / "rfcs" / "0013-installation-matrix-admission-readiness.md": (
            "reviewed manifest contains no installation records"
        ),
    }
    for path, text in expected.items():
        assert text in path.read_text(encoding="utf-8")


def test_source_wheel_and_release_smoke_explicitly_include_m30_evidence() -> None:
    checks = {
        _ROOT / "scripts" / "smoke_wheel.py": (
            "validate_installation_matrix_evidence",
            "installation_matrix_readiness.py",
            "installation_matrix.json",
        ),
        _ROOT / "scripts" / "smoke_release.py": (
            "validate_installation_matrix_evidence",
            "installation_matrix_readiness.py",
        ),
        _ROOT / "scripts" / "release_artifacts.py": (
            "installation_matrix_readiness.py",
            "installation_matrix.json",
        ),
        _ROOT / "tests" / "unit" / "test_release_artifacts.py": (
            "installation_matrix_readiness.py",
            "installation_matrix.json",
        ),
    }
    for path, required in checks.items():
        text = path.read_text(encoding="utf-8")
        assert all(item in text for item in required)
