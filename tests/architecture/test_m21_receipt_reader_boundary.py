"""Keep M21 receipt decoding bounded, explicit, and backend-neutral."""

import ast
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave
import ludoweave.world as world

_ROOT = Path(__file__).parents[2]
_READER_FILES = (
    _ROOT / "src" / "ludoweave" / "world" / "receipt.py",
    _ROOT / "examples" / "receipt_reader.py",
    _ROOT / "scripts" / "receipt_reader_evidence.py",
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
_M21_EXPORTS = (
    "IncompatibleReceiptError",
    "ReceiptDecodeError",
    "ReceiptLimits",
    "TransactionReceipt",
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


def _attempt_limit_mutation(value: object) -> None:
    field_name = "_".join(("max", "bytes"))
    setattr(value, field_name, 2)


def test_receipt_reader_has_no_ambient_or_backend_dependency() -> None:
    for path in _READER_FILES:
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
    fixture = tmp_path / "invalid_reader.py"
    fixture.write_text(source, encoding="utf-8")

    assert _forbidden(_imports(fixture))


def test_receipt_reader_is_focused_and_remains_experimental() -> None:
    assert world.RECEIPT_PROTOCOL == "ludoweave.receipt/1"
    assert ludoweave.__version__ == "0.1.0a1"
    assert hasattr(world.TransactionReceipt, "from_mapping")
    assert hasattr(world.TransactionReceipt, "from_json")
    assert all(world.__stability__[name] == "experimental" for name in _M21_EXPORTS)
    assert all(name not in ludoweave.__all__ for name in _M21_EXPORTS)


def test_receipt_limits_are_frozen_slotted_and_explicit() -> None:
    limits = world.ReceiptLimits()

    assert limits.__slots__
    assert limits.max_bytes == 1_048_576
    assert limits.max_outcomes == 1_024
    assert limits.max_diagnostics == 64
    assert limits.max_aliases == 1_024
    assert limits.max_diff_records == 100_000
    with pytest.raises((AttributeError, TypeError)):
        _attempt_limit_mutation(limits)


def test_m21_adds_no_dependency_or_optional_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["version"] == "0.1.0a1"
    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
