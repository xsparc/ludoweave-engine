"""Dependency-direction and backend-isolation acceptance tests."""

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
