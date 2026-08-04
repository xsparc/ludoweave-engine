"""Small AST import-rule checker used by architecture acceptance tests."""

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

_BANNED_EXTERNAL_ROOTS = frozenset({"glfw", "numpy", "rust", "wgpu"})


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
            if root in _BANNED_EXTERNAL_ROOTS:
                violations.append(
                    ImportViolation(path, line, f"M0 source imports banned dependency {root!r}")
                )
            if (
                module.startswith("ludoweave.core")
                and root not in sys.stdlib_module_names
                and not imported.startswith("ludoweave.core")
            ):
                violations.append(
                    ImportViolation(
                        path,
                        line,
                        f"core module {module!r} imports non-core module {imported!r}",
                    )
                )
            if imported.startswith("ludoweave.") and not _internal_import_allowed(
                source=module, imported=imported
            ):
                violations.append(
                    ImportViolation(
                        path,
                        line,
                        f"module {module!r} may not import {imported!r}",
                    )
                )
    return violations


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
        return imported.startswith("ludoweave.app")
    if source.startswith("ludoweave.core"):
        return imported.startswith("ludoweave.core")
    if source == "ludoweave.render":
        return imported.startswith(("ludoweave.render.api", "ludoweave.render.backends"))
    if source.startswith("ludoweave.render.api"):
        return imported.startswith(("ludoweave.core", "ludoweave.render.api"))
    if source.startswith("ludoweave.render.backends"):
        return imported.startswith(
            ("ludoweave.core", "ludoweave.render.api", "ludoweave.render.backends")
        )
    if source.startswith("ludoweave.app"):
        return imported.startswith(("ludoweave.app", "ludoweave.core", "ludoweave.render.api"))
    return source.startswith("ludoweave.tools") or source == "ludoweave.__main__"
