"""Small AST import-rule checker used by architecture acceptance tests."""

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

_GRAPHICS_ADAPTER_ROOTS = frozenset({"glfw", "rendercanvas", "wgpu"})
_BANNED_WORLD_CALLS = frozenset({"__import__", "compile", "eval", "exec"})
_BANNED_AGENT_CALLS = frozenset({"__import__", "compile", "eval", "exec"})
_BANNED_PLUGIN_CALLS = frozenset({"__import__", "compile", "eval", "exec", "input", "open"})
_PLUGIN_METADATA_GLOBALS = frozenset({"__all__", "__stability__"})
_PLUGIN_ALLOWED_GLOBAL_CALLS = {
    "ludoweave.plugins.compatibility": {
        "_DETAIL_KEY": "re.compile",
        "_ISSUE_CODE": "re.compile",
        "_PLUGIN_CHECK_LIMITS": "JsonLimits",
    },
    "ludoweave.plugins.manifest": {
        "PLUGIN_MANIFEST_LIMITS": "JsonLimits",
        "_PLUGIN_ID": "re.compile",
        "_PYTHON_VERSION": "re.compile",
        "_VERSION": "re.compile",
    },
}
_PLUGIN_ALLOWED_STDLIB_ROOTS = frozenset(
    {
        "__future__",
        "collections",
        "dataclasses",
        "enum",
        "hashlib",
        "itertools",
        "math",
        "re",
        "sys",
        "typing",
    }
)
_BANNED_MCP_ROOTS = frozenset({"aiohttp", "fastapi", "http", "socket", "starlette", "urllib"})
_LOCAL_STDIO_MODULES = frozenset({"ludoweave.tools.inspector", "ludoweave.tools.mcp"})
_REFERENCE_ALLOWED_IMPORTS = {
    "ludoweave.ecs.commands": frozenset(
        {
            "AddCommand",
            "CommandBackend",
            "Commands",
            "DeferredCommand",
            "DeferredEntity",
            "DestroyCommand",
            "EntityTarget",
            "FlushResult",
            "SpawnCommand",
        }
    ),
    "ludoweave.ecs._checkpoint": frozenset(
        {"ComponentRowCheckpoint", "ComponentTableCheckpoint", "EcsCheckpoint"}
    ),
    "ludoweave.ecs.component": frozenset(
        {"ComponentField", "ComponentRegistry", "ComponentSchema", "ComponentValueType"}
    ),
    "ludoweave.ecs.entity": frozenset({"AllocatorCheckpoint", "EntityId"}),
    "ludoweave.ecs.errors": frozenset(
        {
            "ComponentAlreadyPresentError",
            "ActiveQueryError",
            "ComponentError",
            "DeferredCommandError",
            "InvalidDeferredEntityError",
            "InvalidComponentValueError",
            "InvalidEntityIdError",
            "InvalidQueryError",
            "InvalidWorldCheckpointError",
            "MissingComponentError",
            "StaleEntityError",
        }
    ),
    "ludoweave.ecs.query": frozenset(
        {"Query", "QueryBackend", "QueryOrder", "QueryRowState", "QuerySpec"}
    ),
}


@dataclass(frozen=True, slots=True)
class ImportViolation:
    path: Path
    line: int
    message: str


def check_source_tree(source_root: Path) -> list[ImportViolation]:
    """Return every dependency-rule violation below a ``src`` directory."""

    violations: list[ImportViolation] = []
    package_root = source_root / "ludoweave"
    for path in sorted(package_root.rglob("*.py")):
        module = _module_name(source_root, path)
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for imported, line in _resolved_imports(
            tree, source_module=module, is_package=path.name == "__init__.py"
        ):
            root = imported.partition(".")[0]
            normalized_root = root.casefold()
            adapter_import = (
                normalized_root in _GRAPHICS_ADAPTER_ROOTS
                and module == "ludoweave.render.backends.wgpu"
            )
            plugin_contract = _is_module_or_child(module, "ludoweave.plugins")
            dedicated_network_import = module in _LOCAL_STDIO_MODULES and root in _BANNED_MCP_ROOTS
            external_import = (
                normalized_root != "ludoweave" and normalized_root not in sys.stdlib_module_names
            )
            if (
                external_import
                and not adapter_import
                and not plugin_contract
                and not dedicated_network_import
            ):
                violations.append(
                    ImportViolation(
                        path,
                        line,
                        f"source imports unsupported external dependency {root!r}",
                    )
                )
            if module in _LOCAL_STDIO_MODULES and root in _BANNED_MCP_ROOTS:
                violations.append(
                    ImportViolation(
                        path,
                        line,
                        f"local stdio adapter imports network module {root!r}",
                    )
                )
            if (
                _is_module_or_child(module, "ludoweave.plugins")
                and root != "ludoweave"
                and root not in _PLUGIN_ALLOWED_STDLIB_ROOTS
            ):
                violations.append(
                    ImportViolation(
                        path,
                        line,
                        f"plugin contract imports forbidden module {root!r}",
                    )
                )
            if (
                _is_module_or_child(module, "ludoweave.core")
                and root not in sys.stdlib_module_names
                and not _is_module_or_child(imported, "ludoweave.core")
            ):
                violations.append(
                    ImportViolation(
                        path,
                        line,
                        f"core module {module!r} imports non-core module {imported!r}",
                    )
                )
            if (
                imported == "ludoweave" or imported.startswith("ludoweave.")
            ) and not _internal_import_allowed(source=module, imported=imported):
                violations.append(
                    ImportViolation(
                        path,
                        line,
                        f"module {module!r} may not import {imported!r}",
                    )
                )
        if _is_module_or_child(module, "ludoweave.world"):
            for called, line in _resolved_calls(tree):
                if called in _BANNED_WORLD_CALLS:
                    violations.append(
                        ImportViolation(
                            path,
                            line,
                            f"world protocol module {module!r} calls banned builtin {called!r}",
                        )
                    )
        if _is_module_or_child(module, "ludoweave.agent"):
            for called, line in _resolved_calls(tree):
                if called in _BANNED_AGENT_CALLS:
                    violations.append(
                        ImportViolation(
                            path,
                            line,
                            f"agent service module {module!r} calls banned builtin {called!r}",
                        )
                    )
        if _is_module_or_child(module, "ludoweave.plugins"):
            for referenced, line in _loaded_banned_names(tree, _BANNED_PLUGIN_CALLS):
                violations.append(
                    ImportViolation(
                        path,
                        line,
                        f"plugin contract references banned builtin {referenced!r}",
                    )
                )
            for name, line in _module_mutable_assignments(tree, module=module):
                if name not in _PLUGIN_METADATA_GLOBALS:
                    violations.append(
                        ImportViolation(
                            path,
                            line,
                            f"plugin contract defines module-level mutable state {name!r}",
                        )
                    )
        if module == "ludoweave.tools.inspector":
            for called, line in _resolved_calls(tree):
                if called in _BANNED_AGENT_CALLS:
                    violations.append(
                        ImportViolation(
                            path,
                            line,
                            f"local inspector calls banned builtin {called!r}",
                        )
                    )
    return violations


def check_reference_imports(path: Path) -> list[ImportViolation]:
    """Enforce the reference model's exact public-contract import whitelist."""

    violations: list[ImportViolation] = []
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    package_parts = ["ludoweave", "ecs"]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _is_module_or_child(alias.name, "ludoweave.ecs"):
                    violations.append(
                        ImportViolation(
                            path,
                            node.lineno,
                            f"reference model may not import ECS module {alias.name!r}",
                        )
                    )
            continue
        if not isinstance(node, ast.ImportFrom):
            continue
        module = _reference_import_from_module(node, package_parts)
        if module is None or not _is_module_or_child(module, "ludoweave.ecs"):
            continue
        allowed_names = _REFERENCE_ALLOWED_IMPORTS.get(module)
        imported_names = {alias.name for alias in node.names}
        if allowed_names is None or not imported_names <= allowed_names:
            violations.append(
                ImportViolation(
                    path,
                    node.lineno,
                    f"reference model import {module!r} names {sorted(imported_names)!r} "
                    "is outside its whitelist",
                )
            )
    return violations


def _reference_import_from_module(node: ast.ImportFrom, package_parts: list[str]) -> str | None:
    if node.level == 0:
        return node.module
    parents_to_remove = node.level - 1
    if parents_to_remove > len(package_parts):
        return None
    base_parts = package_parts[: len(package_parts) - parents_to_remove]
    if node.module is not None:
        return ".".join([*base_parts, *node.module.split(".")])
    if len(node.names) == 1:
        return ".".join([*base_parts, *node.names[0].name.split(".")])
    return ".".join(base_parts)


def _module_name(source_root: Path, path: Path) -> str:
    relative = path.relative_to(source_root).with_suffix("")
    parts = relative.parts
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _resolved_imports(
    tree: ast.AST, *, source_module: str, is_package: bool
) -> list[tuple[str, int]]:
    imports: list[tuple[str, int]] = []
    source_parts = source_module.split(".")
    package_parts = source_parts if is_package else source_parts[:-1]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend((alias.name, node.lineno) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                if node.module is not None:
                    imports.append((node.module, node.lineno))
                continue
            parents_to_remove = node.level - 1
            if parents_to_remove > len(package_parts):
                imports.append(("<invalid-relative-import>", node.lineno))
                continue
            base_parts = package_parts[: len(package_parts) - parents_to_remove]
            if node.module is None:
                for alias in node.names:
                    imported_parts = [] if alias.name == "*" else alias.name.split(".")
                    imports.append((".".join([*base_parts, *imported_parts]), node.lineno))
            else:
                imports.append((".".join([*base_parts, *node.module.split(".")]), node.lineno))
    return imports


def _internal_import_allowed(*, source: str, imported: str) -> bool:
    if source == "ludoweave":
        return _is_any_module_or_child(imported, ("ludoweave.app", "ludoweave.core"))
    if _is_module_or_child(source, "ludoweave.core"):
        return _is_module_or_child(imported, "ludoweave.core")
    if _is_module_or_child(source, "ludoweave.ecs"):
        return _is_any_module_or_child(imported, ("ludoweave.core", "ludoweave.ecs"))
    if _is_module_or_child(source, "ludoweave.assets"):
        return _is_any_module_or_child(imported, ("ludoweave.assets", "ludoweave.core"))
    if _is_module_or_child(source, "ludoweave.audio"):
        return _is_any_module_or_child(imported, ("ludoweave.audio", "ludoweave.core"))
    if _is_module_or_child(source, "ludoweave.collision"):
        return _is_any_module_or_child(imported, ("ludoweave.collision", "ludoweave.core"))
    if _is_module_or_child(source, "ludoweave.platform"):
        return _is_any_module_or_child(imported, ("ludoweave.core", "ludoweave.platform"))
    if _is_module_or_child(source, "ludoweave.presentation"):
        return _is_any_module_or_child(
            imported,
            (
                "ludoweave.core",
                "ludoweave.presentation",
                "ludoweave.render.contracts",
                "ludoweave.render.extraction",
                "ludoweave.render.handles",
            ),
        )
    if _is_module_or_child(source, "ludoweave.plugins"):
        return (
            _is_module_or_child(imported, "ludoweave.plugins")
            or imported == "ludoweave.core.errors"
            or imported == "ludoweave.core.version"
            or imported == "ludoweave.world.canonical"
        )
    if _is_module_or_child(source, "ludoweave.world"):
        return _is_any_module_or_child(
            imported, ("ludoweave.core", "ludoweave.ecs", "ludoweave.world")
        )
    if _is_module_or_child(source, "ludoweave.agent"):
        return _is_any_module_or_child(
            imported, ("ludoweave.agent", "ludoweave.core", "ludoweave.world")
        )
    if source == "ludoweave.render":
        return _is_module_or_child(imported, "ludoweave.render")
    if _is_module_or_child(source, "ludoweave.render") and not _is_module_or_child(
        source, "ludoweave.render.backends"
    ):
        return _is_any_module_or_child(
            imported, ("ludoweave.core", "ludoweave.platform", "ludoweave.render")
        )
    if _is_module_or_child(source, "ludoweave.render.backends"):
        return _is_any_module_or_child(
            imported, ("ludoweave.core", "ludoweave.platform", "ludoweave.render")
        )
    if _is_module_or_child(source, "ludoweave.app"):
        return _is_any_module_or_child(
            imported,
            (
                "ludoweave.app",
                "ludoweave.core",
                "ludoweave.ecs",
                "ludoweave.platform",
                "ludoweave.render.api",
                "ludoweave.render.device",
                "ludoweave.render.extraction",
                "ludoweave.world",
            ),
        )
    return (
        _is_module_or_child(source, "ludoweave.samples")
        or _is_module_or_child(source, "ludoweave.tools")
        or source == "ludoweave.__main__"
    )


def _is_module_or_child(name: str, allowed: str) -> bool:
    return name == allowed or name.startswith(f"{allowed}.")


def _is_any_module_or_child(name: str, allowed: tuple[str, ...]) -> bool:
    return any(_is_module_or_child(name, candidate) for candidate in allowed)


def _resolved_calls(tree: ast.AST) -> list[tuple[str, int]]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                aliases[alias.asname or alias.name.partition(".")[0]] = alias.name
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            for alias in node.names:
                aliases[alias.asname or alias.name] = f"{node.module}.{alias.name}"

    calls: list[tuple[str, int]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node.func)
        if name is None:
            continue
        resolved = aliases.get(name, name)
        if "." in name:
            root, separator, remainder = name.partition(".")
            resolved = f"{aliases.get(root, root)}{separator}{remainder}"
        called = resolved.rpartition(".")[2]
        if resolved == called or resolved == f"builtins.{called}":
            calls.append((called, node.lineno))
    return calls


def _call_name(node: ast.expr) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _call_name(node.value)
        return None if base is None else f"{base}.{node.attr}"
    return None


def _module_mutable_assignments(tree: ast.Module, *, module: str) -> list[tuple[str, int]]:
    assignments: list[tuple[str, int]] = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            value = node.value
            targets = node.targets
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            value = node.value
            targets = [node.target]
        else:
            continue
        for target in targets:
            for name in _assignment_names(target):
                if name not in _PLUGIN_METADATA_GLOBALS and not _is_allowed_plugin_global(
                    module, name, value
                ):
                    assignments.append((name, node.lineno))
    return assignments


def _is_allowed_plugin_global(module: str, name: str, node: ast.expr) -> bool:
    if _is_immutable_literal_expression(node):
        return True
    if not isinstance(node, ast.Call):
        return False
    called = _call_name(node.func)
    return _PLUGIN_ALLOWED_GLOBAL_CALLS.get(module, {}).get(name) == called


def _is_immutable_literal_expression(node: ast.expr) -> bool:
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, ast.Tuple):
        return all(_is_immutable_literal_expression(item) for item in node.elts)
    if isinstance(node, ast.UnaryOp):
        return _is_immutable_literal_expression(node.operand)
    if isinstance(node, ast.BinOp):
        return _is_immutable_literal_expression(node.left) and _is_immutable_literal_expression(
            node.right
        )
    return False


def _assignment_names(node: ast.expr) -> list[str]:
    if isinstance(node, ast.Name):
        return [node.id]
    if isinstance(node, (ast.Tuple, ast.List)):
        return [name for item in node.elts for name in _assignment_names(item)]
    return []


def _loaded_banned_names(tree: ast.AST, banned: frozenset[str]) -> list[tuple[str, int]]:
    return sorted(
        (node.id, node.lineno)
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in banned
    )
