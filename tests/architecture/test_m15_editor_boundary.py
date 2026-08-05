"""Keep M15 as a visual-editor admission decision, not an implementation."""

import re
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave

_ROOT = Path(__file__).parents[2]
_EDITOR_TOKENS = frozenset({"editor", "gui", "gizmo", "viewport"})
_ROOT_EXPORTS = ("Engine", "EngineConfig", "LifecycleState", "__version__")
_GRAPHICS_DEPENDENCIES = [
    "glfw==2.10.2",
    "rendercanvas[glfw]==2.7.2",
    "wgpu==0.32.0",
]


def test_engine_source_contains_no_editor_named_runtime_module() -> None:
    source = _ROOT / "src" / "ludoweave"
    modules = [path.relative_to(source).as_posix() for path in source.rglob("*.py")]

    assert [
        name
        for name in modules
        if any(_editor_tokens(part) & _EDITOR_TOKENS for part in Path(name).parts)
    ] == []


def test_engine_root_does_not_export_an_editor_surface() -> None:
    assert tuple(ludoweave.__all__) == _ROOT_EXPORTS
    assert _editor_exports(tuple(ludoweave.__all__)) == ()


@pytest.mark.parametrize(
    "export",
    ["EditorApplication", "GUIEditor", "SceneEditor", "VisualEditor", "WorldViewport"],
)
def test_editor_export_scan_rejects_alternate_names(export: str) -> None:
    assert _editor_exports((*_ROOT_EXPORTS, export)) == (export,)


def test_runtime_dependency_contract_is_unchanged() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}


def _editor_exports(exports: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(name for name in exports if _editor_tokens(name) & _EDITOR_TOKENS)


def _editor_tokens(name: str) -> frozenset[str]:
    words = re.findall(r"[A-Z]+(?=[A-Z][a-z]|[0-9]|$)|[A-Z]?[a-z]+|[0-9]+", name)
    return frozenset(word.casefold() for word in words)
