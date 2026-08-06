"""Keep M22 policy evidence deterministic and outside the runtime package."""

import ast
import hashlib
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave
from ludoweave.world import BUILTIN_OPERATION_SPECS

_ROOT = Path(__file__).parents[2]
_CONTRACT = _ROOT / "tests" / "fixtures" / "operation_arguments_v1" / "contracts.json"
_EVIDENCE_FILES = (
    _ROOT / "examples" / "operation_argument_compatibility.py",
    _ROOT / "scripts" / "operation_argument_evidence.py",
)
_FORBIDDEN_IMPORTS = {
    "http",
    "importlib",
    "multiprocessing",
    "numpy",
    "os",
    "pathlib",
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
        if (
            isinstance(statement, ast.AnnAssign)
            and isinstance(statement.target, ast.Name)
            and statement.target.id == name
            and statement.value is not None
        ):
            return ast.literal_eval(statement.value)
        if isinstance(statement, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in statement.targets
        ):
            return ast.literal_eval(statement.value)
    raise AssertionError(f"{name} was not a literal assignment")


def test_contract_fixture_is_exact_and_matches_installed_evidence_literals() -> None:
    payload = _CONTRACT.read_bytes()
    document = cast(dict[str, object], json.loads(payload))

    assert len(payload) == 2926
    assert hashlib.sha256(payload).hexdigest() == (
        "11ec4b9d9805dc509f18a52e8c0defd50136a475e216ae88fbe6bae68fb27001"
    )
    assert document.keys() == {
        "schema",
        "source_package",
        "source_version",
        "command_protocol",
        "evidence_level",
        "policy",
        "definitions",
        "operations",
    }
    operations = cast(list[dict[str, object]], document["operations"])
    assert [(item["operation"], item["version"]) for item in operations] == [
        (spec.operation, spec.version) for spec in BUILTIN_OPERATION_SPECS
    ]
    example = _EVIDENCE_FILES[0]
    assert list(cast(tuple[object, ...], _literal(example, "_CONTRACTS"))) == operations
    assert _literal(example, "_POLICY") == document["policy"]


def test_evidence_files_have_no_ambient_or_side_effect_dependency() -> None:
    for path in _EVIDENCE_FILES:
        assert _forbidden(_imports(path)) == set()


@pytest.mark.parametrize(
    "source",
    [
        "def nested() -> None:\n    import socket\n",
        "if True:\n    from importlib import import_module\n",
        "try:\n    import subprocess\nexcept ImportError:\n    pass\n",
        "from ludoweave.tools import cli\n",
        "from ludoweave.render.backends.wgpu import WgpuRenderDevice\n",
    ],
)
def test_import_scan_detects_nested_forbidden_fixtures(tmp_path: Path, source: str) -> None:
    fixture = tmp_path / "invalid_evidence.py"
    fixture.write_text(source, encoding="utf-8")

    assert _forbidden(_imports(fixture))


def test_m22_adds_no_runtime_export_dependency_or_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["version"] == "0.1.0a1"
    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
    assert "OperationArgumentPolicy" not in ludoweave.__all__
