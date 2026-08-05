"""Every explicitly exported Python symbol has machine-checkable stability."""

import importlib
from pathlib import Path
from types import ModuleType
from typing import cast

_ALLOWED = {"experimental", "preview", "stable"}
_MODULES = {
    "ludoweave",
    "ludoweave.agent",
    "ludoweave.app",
    "ludoweave.assets",
    "ludoweave.audio",
    "ludoweave.collision",
    "ludoweave.core",
    "ludoweave.ecs",
    "ludoweave.platform",
    "ludoweave.presentation",
    "ludoweave.render",
    "ludoweave.render.backends",
    "ludoweave.render.backends.wgpu",
    "ludoweave.samples",
    "ludoweave.world",
}


def test_every_exporting_module_is_in_the_stability_inventory() -> None:
    source_root = Path(__file__).resolve().parents[2] / "src" / "ludoweave"
    exporting: set[str] = set()
    for path in source_root.rglob("*.py"):
        if "__all__ =" not in path.read_text(encoding="utf-8"):
            continue
        relative = path.relative_to(source_root)
        parts = list(relative.with_suffix("").parts)
        if parts[-1] == "__init__":
            parts.pop()
        exporting.add(".".join(("ludoweave", *parts)).rstrip("."))

    assert exporting == _MODULES


def test_every_public_export_has_exact_valid_stability_metadata() -> None:
    for module_name in sorted(_MODULES):
        module: ModuleType = importlib.import_module(module_name)
        exports_value: object = getattr(module, "__all__", None)
        stability_value: object = getattr(module, "__stability__", None)
        assert isinstance(exports_value, list), module_name
        assert isinstance(stability_value, dict), module_name
        exports = cast(list[object], exports_value)
        stability = cast(dict[object, object], stability_value)
        assert exports
        assert all(isinstance(name, str) and name for name in exports)
        assert len(exports) == len(set(cast(list[str], exports)))
        assert set(stability) == set(exports)
        assert set(stability.values()) <= _ALLOWED
        assert all(hasattr(module, cast(str, name)) for name in exports)
