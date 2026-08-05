"""Retain inert plugin metadata and defer executable WASM-mod infrastructure."""

import re
import tomllib
from pathlib import Path
from typing import cast

import pytest
from import_rules import check_source_tree

import ludoweave
import ludoweave.plugins as plugins

_ROOT = Path(__file__).parents[2]
_WASM_EXPORT_TOKENS = frozenset({"guest", "modloader", "wasi", "wasm", "webassembly"})
_GRAPHICS_DEPENDENCIES = [
    "glfw==2.10.2",
    "rendercanvas[glfw]==2.7.2",
    "wgpu==0.32.0",
]
_RUNTIME_IDENTIFIERS = frozenset(
    {"pywasm", "wasi", "wasm3", "wasmedge", "wasmedge_sdk", "wasmer", "wasmtime"}
)


def test_source_contains_no_wasm_named_runtime_module() -> None:
    source = _ROOT / "src" / "ludoweave"
    modules = [path.relative_to(source).as_posix() for path in source.rglob("*.py")]

    assert [name for name in modules if _wasm_tokens(name) & _WASM_EXPORT_TOKENS] == []


@pytest.mark.parametrize("name", ["webassembly_runtime.py", "wasm_guest.py", "wasi_host.py"])
def test_import_checker_rejects_wasm_named_runtime_modules(tmp_path: Path, name: str) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "tools" / name
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text("value = 1\n", encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert "defines deferred WebAssembly runtime module" in violations[0].message


def test_source_contains_no_wasm_runtime_identifier() -> None:
    source = _ROOT / "src" / "ludoweave"
    matches: list[tuple[str, str]] = []
    for path in sorted(source.rglob("*.py")):
        words = re.findall(r"[A-Za-z][A-Za-z0-9_.-]*", path.read_text(encoding="utf-8"))
        for word in words:
            normalized = re.sub(r"[-.]+", "_", word).casefold()
            if normalized in _RUNTIME_IDENTIFIERS:
                matches.append((path.relative_to(source).as_posix(), word))

    assert matches == []


def test_public_surfaces_export_no_wasm_execution_contract() -> None:
    exports = (*ludoweave.__all__, *plugins.__all__)

    assert [name for name in exports if _wasm_tokens(name) & _WASM_EXPORT_TOKENS] == []


def test_distribution_adds_no_wasm_runtime_dependency() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}


@pytest.mark.parametrize(
    "runtime",
    ["pywasm", "wasi", "wasm3", "wasmedge_sdk", "wasmer", "wasmtime"],
)
@pytest.mark.parametrize("area", ["plugins", "tools"])
def test_import_checker_explicitly_rejects_wasm_runtimes(
    tmp_path: Path, runtime: str, area: str
) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / area / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text(f"import {runtime}\n", encoding="utf-8")

    violations = check_source_tree(source_root)

    assert any(
        f"deferred WebAssembly runtime {runtime!r}" in violation.message for violation in violations
    )


@pytest.mark.parametrize(
    "source",
    [
        'import importlib\nimportlib.import_module("wasmtime")\n',
        'from importlib import import_module\nimport_module("wasmer")\n',
        '__import__("wasi")\n',
    ],
)
def test_import_checker_rejects_dynamic_wasm_runtime_loading(tmp_path: Path, source: str) -> None:
    source_root = tmp_path / "src"
    bad_module = source_root / "ludoweave" / "tools" / "bad.py"
    bad_module.parent.mkdir(parents=True)
    bad_module.write_text(source, encoding="utf-8")

    violations = check_source_tree(source_root)

    assert len(violations) == 1
    assert "dynamically loads deferred WebAssembly runtime" in violations[0].message


def _wasm_tokens(name: str) -> frozenset[str]:
    words = re.findall(r"[A-Z]+(?=[A-Z][a-z]|[0-9]|$)|[A-Z]?[a-z]+|[0-9]+", name)
    return frozenset(word.casefold() for word in words)
