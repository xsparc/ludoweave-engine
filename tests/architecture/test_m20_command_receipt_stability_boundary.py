"""Keep M20 evidence deterministic, offline, and free of runtime expansion."""

import ast
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave
import ludoweave.world as world

_ROOT = Path(__file__).parents[2]
_EVIDENCE_FILES = (
    _ROOT / "examples" / "command_receipt_stability_decision.py",
    _ROOT / "scripts" / "command_receipt_stability_evidence.py",
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
_WORLD_STABILITY_EXPORTS = (
    "COMMAND_PROTOCOL",
    "RECEIPT_PROTOCOL",
    "TRANSACTION_PROTOCOL",
    "CommandActor",
    "CommandEnvelope",
    "CommandOutcome",
    "CommandTransaction",
    "ReceiptDiagnostic",
    "ReceiptStatus",
    "TransactionReceipt",
    "TransactionService",
)
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


def test_evidence_files_have_no_ambient_or_side_effect_dependency() -> None:
    for path in _EVIDENCE_FILES:
        imports = _imports(path)
        assert _forbidden(imports) == set()


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


def test_command_receipt_exports_remain_experimental_and_focused() -> None:
    assert all(world.__stability__[name] == "experimental" for name in _WORLD_STABILITY_EXPORTS)
    assert "CommandEnvelope" not in ludoweave.__all__
    assert "TransactionReceipt" not in ludoweave.__all__
    assert not hasattr(world.TransactionReceipt, "from_mapping")


def test_m20_adds_no_dependency_or_optional_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
