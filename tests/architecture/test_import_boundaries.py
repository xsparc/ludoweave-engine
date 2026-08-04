"""Dependency-direction and backend-isolation acceptance tests."""

from pathlib import Path

from import_rules import check_source_tree


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
