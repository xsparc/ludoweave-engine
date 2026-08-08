"""CI change classification is strict, NUL-safe, and fail closed."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Protocol, cast

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = _ROOT / "scripts" / "classify_ci_changes.py"


class _Classifier(Protocol):
    def is_documentation_path(self, value: str) -> bool: ...

    def requires_substantive_ci(self, paths: Sequence[str]) -> bool: ...

    def changed_paths(self, base: str, head: str, *, cwd: Path) -> tuple[str, ...]: ...


def _load_classifier() -> _Classifier:
    spec = importlib.util.spec_from_file_location("classify_ci_changes", _SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load CI classifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return cast(_Classifier, module)


_CLASSIFIER = _load_classifier()


@pytest.mark.parametrize(
    "path",
    [
        "README.md",
        "CHANGELOG.md",
        "docs/architecture.md",
        "docs/rfcs/0020-ci-change-qualification.md",
        ".project/TEST_EVIDENCE.md",
        ".github/ISSUE_TEMPLATE/bug.yml",
        ".github/ISSUE_TEMPLATE/config.yaml",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/labels.yml",
    ],
)
def test_documentation_paths_are_narrowly_admitted(path: str) -> None:
    assert _CLASSIFIER.is_documentation_path(path)


@pytest.mark.parametrize(
    "path",
    [
        "",
        "LICENSE",
        "NOTICE",
        "mkdocs.yml",
        "pyproject.toml",
        "src/ludoweave/engine.py",
        "tests/unit/test_clock.py",
        "scripts/smoke_wheel.py",
        ".github/workflows/ci.yml",
        ".github/dependabot.yml",
        ".github/CODEOWNERS",
        ".github/ISSUE_TEMPLATE/helper.py",
        "docs/hooks.py",
        "docs/evidence.json",
        ".project/evidence.toml",
        "../README.md",
        "/docs/architecture.md",
        "docs\\architecture.md",
    ],
)
def test_every_non_documentation_or_ambiguous_path_is_substantive(path: str) -> None:
    assert not _CLASSIFIER.is_documentation_path(path)


def test_classification_fails_closed_for_empty_or_mixed_changes() -> None:
    assert _CLASSIFIER.requires_substantive_ci([])
    assert not _CLASSIFIER.requires_substantive_ci(
        ["README.md", "docs/architecture.md", ".project/PROJECT_STATE.md"]
    )
    assert _CLASSIFIER.requires_substantive_ci(["docs/architecture.md", "uv.lock"])


def _git(cwd: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _commit(cwd: Path, message: str) -> str:
    _git(cwd, "add", ".")
    _git(
        cwd,
        "-c",
        "user.name=LudoWeave Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-m",
        message,
    )
    return _git(cwd, "rev-parse", "HEAD")


def test_git_diff_and_cli_preserve_unusual_names_and_emit_outputs(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    _git(repository, "init", "--initial-branch=main")
    (repository / "README.md").write_text("base\n", encoding="utf-8")
    base = _commit(repository, "base")

    docs = repository / "docs"
    docs.mkdir()
    (docs / "name with spaces.md").write_text("docs\n", encoding="utf-8")
    head = _commit(repository, "docs")
    assert _CLASSIFIER.changed_paths(base, head, cwd=repository) == ("docs/name with spaces.md",)

    output = tmp_path / "github-output.txt"
    result = subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            "--base",
            base,
            "--head",
            head,
            "--github-output",
            str(output),
        ],
        cwd=repository,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {
        "changed_count": 1,
        "classification": "documentation",
    }
    assert output.read_text(encoding="utf-8") == "substantive=false\nchanged_count=1\n"


def test_invalid_revision_cannot_be_interpreted_as_git_options(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="full hexadecimal object id"):
        _CLASSIFIER.changed_paths("--output=/tmp/unsafe", "0" * 40, cwd=tmp_path)
