"""Keep M23 receipt policy evidence deterministic and outside runtime source."""

import ast
import hashlib
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave

_ROOT = Path(__file__).parents[2]
_CONTRACT = _ROOT / "tests" / "fixtures" / "receipt_semantics_v1" / "contracts.json"
_EVIDENCE_FILES = (
    _ROOT / "examples" / "receipt_semantic_compatibility.py",
    _ROOT / "scripts" / "receipt_semantic_evidence.py",
)
_TRANSACTION = _ROOT / "src" / "ludoweave" / "world" / "transaction.py"
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


def _json_value(value: object) -> object:
    return json.loads(json.dumps(value))


def _literal_error_codes(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        keyword.value.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        for keyword in node.keywords
        if keyword.arg == "code"
        and isinstance(keyword.value, ast.Constant)
        and isinstance(keyword.value.value, str)
    }


def test_contract_fixture_is_exact_and_matches_installed_evidence_literals() -> None:
    payload = _CONTRACT.read_bytes()
    document = cast(dict[str, object], json.loads(payload))

    assert len(payload) == 6286
    assert hashlib.sha256(payload).hexdigest() == (
        "f724a189e1ca23b6bc2637e1037d897bda4fa6dd3eda701ff5d538882a633619"
    )
    assert document.keys() == {
        "schema",
        "source_package",
        "source_version",
        "receipt_protocol",
        "evidence_level",
        "policy",
        "semantic_diff",
        "diagnostics",
    }
    semantic = cast(dict[str, object], document["semantic_diff"])
    diagnostics = cast(dict[str, object], document["diagnostics"])
    for evidence in _EVIDENCE_FILES:
        assert _json_value(_literal(evidence, "_POLICY")) == document["policy"]
        assert _json_value(_literal(evidence, "_DIFF_FIELDS")) == semantic["fields"]
        assert _json_value(_literal(evidence, "_RECORDS")) == semantic["records"]
        assert _json_value(_literal(evidence, "_ORDERING_RULES")) == semantic["ordering_rules"]
        assert _json_value(_literal(evidence, "_SEMANTIC_RULES")) == semantic["semantic_rules"]
        assert (
            _json_value(_literal(evidence, "_EXPECTED_COMPLEX_DIFF"))
            == semantic["evidence_complex_diff"]
        )
        assert (
            _json_value(_literal(evidence, "_DIAGNOSTIC_CODES"))
            == diagnostics["current_emitted_codes"]
        )
        assert (
            _json_value(_literal(evidence, "_DIAGNOSTIC_DEFINITIONS")) == diagnostics["definitions"]
        )
        assert _json_value(_literal(evidence, "_DIAGNOSTIC_RULES")) == diagnostics["rules"]


def test_evidence_files_have_no_ambient_or_side_effect_dependency() -> None:
    for path in _EVIDENCE_FILES:
        assert _forbidden(_imports(path)) == set()


def test_frozen_codes_cover_direct_transaction_diagnostic_identities() -> None:
    recorded = cast(tuple[str, ...], _literal(_EVIDENCE_FILES[0], "_DIAGNOSTIC_CODES"))

    assert _literal_error_codes(_TRANSACTION) == set(recorded) | {
        "world.transaction.invalid_limits"
    }


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


def test_m23_adds_no_runtime_export_dependency_or_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["version"] == "0.1.0a1"
    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
    assert "ReceiptSemanticPolicy" not in ludoweave.__all__
