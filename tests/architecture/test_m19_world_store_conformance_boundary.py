"""M19 world-store conformance remains explicit, storage-neutral, and offline."""

import ast
import inspect
from pathlib import Path

from ludoweave.ecs import run_world_store_conformance

_ROOT = Path(__file__).parents[2]
_MODULE = _ROOT / "src" / "ludoweave" / "ecs" / "conformance.py"


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imports.add(node.module)
    return imports


def test_installed_runner_has_no_discovery_storage_or_side_effect_dependency() -> None:
    imports = _imports(_MODULE)
    forbidden = {
        "importlib",
        "importlib.metadata",
        "os",
        "pathlib",
        "socket",
        "sqlite3",
        "subprocess",
        "urllib",
        "numpy",
        "ludoweave.application",
        "ludoweave.plugins",
        "ludoweave.tools",
        "ludoweave.world",
        "ludoweave.ecs.reference",
        "ludoweave.ecs.storage",
        "ludoweave.render",
        "ludoweave.render.backends",
    }
    assert not imports & forbidden


def test_import_scan_detects_nested_forbidden_fixture(tmp_path: Path) -> None:
    fixture = tmp_path / "invalid_conformance.py"
    fixture.write_text(
        "def discover() -> None:\n"
        "    if True:\n"
        "        import importlib.metadata\n"
        "        from ludoweave.ecs.storage import DenseComponentTable\n",
        encoding="utf-8",
    )

    assert _imports(fixture) == {"importlib.metadata", "ludoweave.ecs.storage"}


def test_runner_imports_only_the_world_store_name_from_world_module() -> None:
    tree = ast.parse(_MODULE.read_text(encoding="utf-8"), filename=str(_MODULE))
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "ludoweave.ecs.world"
        for alias in node.names
    }
    assert imported == {"WorldStore"}


def test_runner_accepts_an_explicit_factory_not_a_module_or_entry_point() -> None:
    signature = inspect.signature(run_world_store_conformance)
    assert tuple(signature.parameters) == ("adapter_id", "factory")
    source = _MODULE.read_text(encoding="utf-8")
    for forbidden in (
        "entry_points",
        "find_spec",
        "module_name",
        "pip install",
        "eval(",
        "exec(",
        "close(",
    ):
        assert forbidden not in source


def test_conformance_is_a_focused_ecs_export_not_a_package_root_export() -> None:
    import ludoweave
    import ludoweave.ecs

    assert "run_world_store_conformance" in ludoweave.ecs.__all__
    assert "run_world_store_conformance" not in ludoweave.__all__
