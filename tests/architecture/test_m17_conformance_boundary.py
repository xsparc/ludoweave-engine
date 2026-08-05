"""M17 conformance remains explicit, provider-neutral, and offline."""

import ast
import inspect
from pathlib import Path

from ludoweave.render import run_render_device_conformance

_ROOT = Path(__file__).parents[2]
_MODULE = _ROOT / "src" / "ludoweave" / "render" / "conformance.py"


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imports.add(node.module)
    return imports


def test_installed_runner_has_no_adapter_discovery_or_side_effect_dependency() -> None:
    imports = _imports(_MODULE)
    forbidden = {
        "importlib",
        "importlib.metadata",
        "os",
        "pathlib",
        "socket",
        "subprocess",
        "urllib",
        "ludoweave.plugins",
        "ludoweave.render.backends",
        "ludoweave.render.backends.null_device",
        "ludoweave.render.backends.wgpu",
    }
    assert not imports & forbidden


def test_runner_accepts_an_explicit_factory_not_a_module_or_entry_point() -> None:
    signature = inspect.signature(run_render_device_conformance)
    assert tuple(signature.parameters) == ("adapter_id", "factory")
    source = _MODULE.read_text(encoding="utf-8")
    for forbidden in ("entry_points", "find_spec", "module_name", "pip install", "eval(", "exec("):
        assert forbidden not in source


def test_conformance_is_a_focused_render_export_not_a_package_root_export() -> None:
    import ludoweave
    import ludoweave.render

    assert "run_render_device_conformance" in ludoweave.render.__all__
    assert "run_render_device_conformance" not in ludoweave.__all__
