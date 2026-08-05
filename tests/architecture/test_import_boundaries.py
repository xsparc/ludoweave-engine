"""Dependency-direction and backend-isolation acceptance tests."""

import subprocess
import sys
from pathlib import Path

import pytest
from import_rules import check_reference_imports, check_source_tree


def test_real_source_obeys_import_rules() -> None:
    source_root = Path(__file__).resolve().parents[2] / "src"
    violations = check_source_tree(source_root)
    messages = [f"{item.path}:{item.line}: {item.message}" for item in violations]
    assert messages == []


def test_checker_rejects_intentionally_forbidden_dependency(tmp_path: Path) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "core" / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text("from ludoweave.app import Engine\n", encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 2
    assert all("bad.py" in str(item.path) for item in violations)
    assert any("non-core" in item.message for item in violations)
    assert any("may not import" in item.message for item in violations)


def test_checker_resolves_forbidden_relative_dependency(tmp_path: Path) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "core" / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text("from ..app import Engine\n", encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 2
    assert all("ludoweave.app" in item.message for item in violations)


def test_checker_resolves_relative_sibling_alias(tmp_path: Path) -> None:
    source_root = tmp_path / "src"
    package = source_root / "ludoweave" / "__init__.py"
    package.parent.mkdir(parents=True)
    package.write_text("from . import render\n", encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert "ludoweave.render" in violations[0].message


def test_checker_rejects_ecs_importing_application(tmp_path: Path) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "ecs" / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text("from ludoweave.app import Engine\n", encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert "ludoweave.ecs.bad" in violations[0].message
    assert "ludoweave.app" in violations[0].message


@pytest.mark.parametrize(
    "provider",
    [
        "glfw",
        "rendercanvas",
        "wgpu",
        "numpy",
        "sdl3",
        "pysdl3",
        "box2d",
        "Box2D",
        "box2d_python",
    ],
)
def test_provider_and_storage_imports_are_confined_to_exact_adapter(
    tmp_path: Path, provider: str
) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "render" / "api_leak.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text(f"import {provider}\n", encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert f"banned dependency '{provider}'" in violations[0].message


def test_package_and_render_contract_imports_do_not_eagerly_load_graphics_providers() -> None:
    script = (
        "import sys; import ludoweave; import ludoweave.render; "
        "assert not ({'wgpu','rendercanvas','glfw','numpy'} & set(sys.modules))"
    )
    result = subprocess.run(
        (sys.executable, "-I", "-c", script),
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    "source",
    [
        "from ludoweave.app import Engine\n",
        "from ludoweave.render.api import RenderBackend\n",
        "from ludoweave.tools.cli import main\n",
    ],
)
def test_world_protocol_rejects_upward_and_service_imports(tmp_path: Path, source: str) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "world" / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text(source, encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert "ludoweave.world.bad" in violations[0].message


@pytest.mark.parametrize(
    "call",
    [
        "eval('1')",
        "exec('x = 1')",
        "compile('1', '', 'eval')",
        "import builtins\nbuiltins.eval('1')",
        "import builtins as safe\nsafe.exec('x = 1')",
        "from builtins import compile as build\nbuild('1', '', 'eval')",
    ],
)
def test_world_protocol_rejects_arbitrary_python_evaluation(tmp_path: Path, call: str) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "world" / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text(f"{call}\n", encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert "banned builtin" in violations[0].message


@pytest.mark.parametrize(
    "source",
    [
        "from ludoweave import Engine\n",
        "from ludoweave import __version__\n",
    ],
)
def test_world_protocol_rejects_package_root_imports(tmp_path: Path, source: str) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "world" / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text(source, encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert "may not import 'ludoweave'" in violations[0].message


@pytest.mark.parametrize(
    "source",
    [
        "from ludoweave.render import RenderDevice\n",
        "from ludoweave.samples import create_clockwork_arena\n",
        "from ludoweave.tools.cli import main\n",
    ],
)
def test_agent_service_rejects_composition_and_transport_imports(
    tmp_path: Path, source: str
) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "agent" / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text(source, encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert "ludoweave.agent.bad" in violations[0].message


@pytest.mark.parametrize("call", ["eval('1')", "exec('x=1')", "compile('1','','eval')"])
def test_agent_service_rejects_arbitrary_python_evaluation(tmp_path: Path, call: str) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "agent" / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text(f"{call}\n", encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert "banned builtin" in violations[0].message


@pytest.mark.parametrize("adapter", ["inspector.py", "mcp.py"])
@pytest.mark.parametrize("module", ["socket", "http.server", "urllib.request", "fastapi"])
def test_local_stdio_adapters_reject_network_modules(
    tmp_path: Path, adapter: str, module: str
) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "tools" / adapter
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text(f"import {module}\n", encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert "network module" in violations[0].message


@pytest.mark.parametrize("call", ["eval('1')", "exec('x=1')", "compile('1','','eval')"])
def test_local_inspector_rejects_arbitrary_python_evaluation(tmp_path: Path, call: str) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "tools" / "inspector.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text(f"{call}\n", encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert "banned builtin" in violations[0].message


def test_application_may_compose_ecs_but_still_rejects_concrete_backends(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "src"
    valid_module = source_root / "ludoweave" / "app" / "valid.py"
    valid_module.parent.mkdir(parents=True)
    valid_module.write_text("from ludoweave.ecs import World\n", encoding="utf-8")
    assert check_source_tree(source_root) == []

    valid_module.write_text(
        "from ludoweave.render.backends.null import NullRenderBackend\n",
        encoding="utf-8",
    )
    violations = check_source_tree(source_root)
    assert len(violations) == 1
    assert "ludoweave.render.backends.null" in violations[0].message


@pytest.mark.parametrize(
    "source",
    [
        "from ludoweave.ecs import World\n",
        "from ludoweave.world import WorldSession\n",
        "from ludoweave.render.backends.wgpu import WgpuRenderDevice\n",
        "from ludoweave.tools.cli import main\n",
    ],
)
def test_presentation_authoring_rejects_authority_backends_and_tools(
    tmp_path: Path, source: str
) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "presentation" / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text(source, encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert "ludoweave.presentation.bad" in violations[0].message


@pytest.mark.parametrize(
    "source",
    [
        "import ctypes\n",
        "import ftplib\n",
        "import importlib.metadata\n",
        "import os\n",
        "from pathlib import Path\n",
        "import pickle\n",
        "import pkg_resources\n",
        "import pkgutil\n",
        "import runpy\n",
        "import subprocess\n",
        "import socket\n",
        "import third_party_plugin\n",
        "from ludoweave.app import Engine\n",
        "from ludoweave.core.clock import MonotonicClock\n",
        "from ludoweave.tools.cli import main\n",
    ],
)
def test_plugin_contract_rejects_discovery_execution_and_upward_imports(
    tmp_path: Path, source: str
) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "plugins" / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text(source, encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert any(
        marker in violations[0].message
        for marker in ("ludoweave", "forbidden module", "arbitrary external")
    )


@pytest.mark.parametrize(
    "source",
    [
        "PLUGIN_REGISTRY = {}\n",
        "_handlers: dict[str, object] = dict()\n",
        "class Registry: pass\nPLUGIN_REGISTRY = Registry()\n",
        "from collections import UserDict\nPLUGIN_REGISTRY = UserDict()\n",
    ],
)
def test_plugin_contract_rejects_module_level_mutable_state(tmp_path: Path, source: str) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "plugins" / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text(source, encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert "module-level mutable state" in violations[0].message


@pytest.mark.parametrize(
    "call",
    [
        "eval('1')",
        "exec('x=1')",
        "compile('1','','eval')",
        "open('manifest.json', 'rb')",
        "input('manifest: ')",
        "loader = __import__\nloader('os')",
        "runner = eval\nrunner('1')",
    ],
)
def test_plugin_contract_rejects_arbitrary_python_evaluation(tmp_path: Path, call: str) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "plugins" / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text(f"{call}\n", encoding="utf-8")

    violations = check_source_tree(source_root)

    assert violations
    assert any("banned builtin" in violation.message for violation in violations)


def test_checker_rejects_near_prefix_module_names(tmp_path: Path) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "ecs" / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text("from ludoweave.ecs_tools import World\n", encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert "ludoweave.ecs_tools" in violations[0].message


def test_reference_world_is_independent_of_production_storage_and_allocator() -> None:
    source_root = Path(__file__).resolve().parents[2] / "src"
    path = source_root / "ludoweave" / "ecs" / "reference.py"
    assert check_reference_imports(path) == []


@pytest.mark.parametrize(
    "source",
    [
        "from ludoweave.ecs import EntityAllocator\n",
        "import ludoweave.ecs.entity as entity_module\n",
        "from .entity import EntityAllocator\n",
        "from ludoweave.ecs.world import World\n",
        "from ludoweave.ecs.storage import DenseComponentTable\n",
        "from ludoweave.ecs.query import _QueryPlan\n",
    ],
)
def test_reference_import_guard_rejects_production_bypasses(tmp_path: Path, source: str) -> None:
    path = tmp_path / "reference.py"
    path.write_text(source, encoding="utf-8")

    violations = check_reference_imports(path)

    assert len(violations) == 1
    assert "reference model" in violations[0].message
