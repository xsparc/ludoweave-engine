"""M18 agent conformance remains explicit, transport-neutral, and offline."""

import ast
import inspect
from pathlib import Path

from ludoweave.agent import run_agent_tool_conformance

_ROOT = Path(__file__).parents[2]
_MODULE = _ROOT / "src" / "ludoweave" / "agent" / "conformance.py"


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imports.add(node.module)
    return imports


def _forbidden_imports(imports: set[str]) -> set[str]:
    forbidden_roots = {
        "importlib",
        "os",
        "pathlib",
        "socket",
        "subprocess",
        "urllib",
        "ludoweave.plugins",
        "ludoweave.render",
        "ludoweave.samples",
        "ludoweave.tools",
    }
    return {
        imported
        for imported in imports
        if any(imported == root or imported.startswith(f"{root}.") for root in forbidden_roots)
    }


def test_installed_runner_has_no_discovery_transport_or_composition_dependency() -> None:
    imports = _imports(_MODULE)
    assert not _forbidden_imports(imports)


def test_import_guard_rejects_nested_forbidden_modules(tmp_path: Path) -> None:
    invalid = tmp_path / "invalid.py"
    invalid.write_text(
        "import importlib.util\nfrom ludoweave.tools import mcp\n",
        encoding="utf-8",
    )

    assert _forbidden_imports(_imports(invalid)) == {"importlib.util", "ludoweave.tools"}


def test_runner_accepts_an_explicit_factory_not_a_module_or_entry_point() -> None:
    signature = inspect.signature(run_agent_tool_conformance)
    assert tuple(signature.parameters) == ("adapter_id", "factory")
    source = _MODULE.read_text(encoding="utf-8")
    for forbidden in (
        "entry_points",
        "find_spec",
        "module_name",
        "pip install",
        "create_subprocess",
        "eval(",
        "exec(",
    ):
        assert forbidden not in source


def test_conformance_is_a_focused_agent_export_not_a_package_root_export() -> None:
    import ludoweave
    import ludoweave.agent

    assert "run_agent_tool_conformance" in ludoweave.agent.__all__
    assert "run_agent_tool_conformance" not in ludoweave.__all__
