"""Keep M25 external-feedback evidence strict, local, and outside runtime source."""

import ast
import hashlib
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave

_ROOT = Path(__file__).parents[2]
_CORPUS = _ROOT / "tests" / "fixtures" / "external_consumer_feedback.json"
_EVIDENCE_FILES = (
    _ROOT / "examples" / "external_consumer_feedback_readiness.py",
    _ROOT / "scripts" / "external_consumer_feedback_evidence.py",
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


def test_feedback_manifest_is_exact_empty_and_reviewed() -> None:
    payload = _CORPUS.read_bytes()
    document = cast(dict[str, object], json.loads(payload))

    assert len(payload) == 283
    assert hashlib.sha256(payload).hexdigest() == (
        "b113444f60946461ec6774e2c278b9e82e7d80e08a37450b6cc153e5c5c1500e"
    )
    assert _literal(_EVIDENCE_FILES[0], "_REVIEWED_FEEDBACK_CORPUS_SHA256") == (
        "b113444f60946461ec6774e2c278b9e82e7d80e08a37450b6cc153e5c5c1500e"
    )
    assert _literal(_EVIDENCE_FILES[0], "_MANDATORY_FEEDBACK_PREFIX") == ()
    assert document == {
        "schema": "ludoweave.compatibility.external-consumer-feedback/1",
        "source_package": "ludoweave",
        "minimum_independent_consumers": 1,
        "required_protocols": [
            "ludoweave.command/1",
            "ludoweave.transaction/1",
            "ludoweave.receipt/1",
        ],
        "feedback_records": [],
    }


def test_feedback_evidence_files_have_no_ambient_external_dependency() -> None:
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


def test_m25_adds_no_runtime_export_dependency_version_or_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["version"] == "0.1.0a1"
    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
    assert "ExternalConsumerFeedback" not in ludoweave.__all__
