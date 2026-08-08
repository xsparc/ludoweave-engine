"""Keep M27 contributor-rehearsal evidence strict, offline, and non-runtime."""

import ast
import hashlib
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave

_ROOT = Path(__file__).parents[2]
_REHEARSALS = _ROOT / "tests" / "fixtures" / "external_contributor_rehearsal.json"
_CONTRIBUTOR_GUIDE = _ROOT / "docs" / "first-contribution.md"
_PULL_REQUEST_TEMPLATE = _ROOT / ".github" / "pull_request_template.md"
_GOOD_FIRST_TEMPLATE = _ROOT / ".github" / "ISSUE_TEMPLATE" / "good_first_issue.yml"
_RELEASE_WORKFLOW = _ROOT / ".github" / "workflows" / "release.yml"
_EVIDENCE_FILES = (
    _ROOT / "examples" / "external_contributor_rehearsal_readiness.py",
    _ROOT / "scripts" / "external_contributor_rehearsal_evidence.py",
)
_FORBIDDEN_IMPORTS = {
    "http",
    "importlib",
    "multiprocessing",
    "numpy",
    "os",
    "requests",
    "socket",
    "sqlite3",
    "subprocess",
    "time",
    "urllib",
    "webbrowser",
    "ludoweave.plugins",
    "ludoweave.render.backends",
    "ludoweave.tools",
}
_GRAPHICS_DEPENDENCIES = [
    "glfw==2.10.2",
    "rendercanvas[glfw]==2.7.2",
    "wgpu==0.32.0",
]


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imports.add(node.module)
    return imports


def _forbidden(imports: set[str]) -> set[str]:
    return {
        imported
        for imported in imports
        if any(imported == name or imported.startswith(f"{name}.") for name in _FORBIDDEN_IMPORTS)
    }


def _literal(path: Path, name: str) -> object:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for statement in tree.body:
        if isinstance(statement, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in statement.targets
        ):
            return ast.literal_eval(statement.value)
        if (
            isinstance(statement, ast.AnnAssign)
            and isinstance(statement.target, ast.Name)
            and statement.target.id == name
            and statement.value is not None
        ):
            return ast.literal_eval(statement.value)
    raise AssertionError(f"{name} was not a literal assignment")


def test_rehearsal_manifest_is_exact_empty_and_reviewed() -> None:
    payload = _REHEARSALS.read_bytes()
    document = cast(dict[str, object], json.loads(payload))

    assert len(payload) == 270
    assert hashlib.sha256(payload).hexdigest() == (
        "ecb959e90a0033b4dbe3dcfe8a48db1c1eea915e0ef2840510969b9e25cdb9c7"
    )
    assert _literal(_EVIDENCE_FILES[0], "_REVIEWED_REHEARSAL_SHA256") == (
        "ecb959e90a0033b4dbe3dcfe8a48db1c1eea915e0ef2840510969b9e25cdb9c7"
    )
    assert _literal(_EVIDENCE_FILES[0], "_MANDATORY_REHEARSAL_PREFIX") == ()
    assert document == {
        "schema": "ludoweave.community.external-contributor-rehearsal/1",
        "source_project": "ludoweave-engine",
        "minimum_merged_rehearsals": 1,
        "required_validation_steps": [
            "clean-setup",
            "focused-check",
            "complete-gate",
        ],
        "rehearsal_records": [],
    }


def test_public_contributor_path_is_complete_but_claims_no_external_study() -> None:
    guide = _CONTRIBUTOR_GUIDE.read_text(encoding="utf-8")
    pull_request_template = _PULL_REQUEST_TEMPLATE.read_text(encoding="utf-8")
    good_first_template = _GOOD_FIRST_TEMPLATE.read_text(encoding="utf-8")

    for marker in (
        "without private\nmaintainer knowledge",
        "uv sync --frozen --all-groups --extra graphics",
        "uv run --frozen pytest -q",
        "git commit -s",
        "No external-contributor usability study has yet\nbeen recorded",
    ):
        assert marker in guide
    assert "Every commit includes a valid DCO" in pull_request_template
    assert "No credentials, private prompts, or personal data" in pull_request_template
    assert "The task can be reviewed independently" in good_first_template


def test_m27_preserves_the_release_workflow_exactly() -> None:
    assert hashlib.sha256(_RELEASE_WORKFLOW.read_bytes()).hexdigest() == (
        "fa6c60642946cc0350f3d2fb78d6918efc4a1ba6f27b54de9f53de3a156c85ae"
    )


def test_rehearsal_evidence_files_have_no_ambient_external_dependency() -> None:
    for path in _EVIDENCE_FILES:
        assert _forbidden(_imports(path)) == set()


@pytest.mark.parametrize(
    "source",
    [
        "def nested() -> None:\n    import socket\n",
        "if True:\n    from importlib import import_module\n",
        "try:\n    import subprocess\nexcept ImportError:\n    pass\n",
        "from urllib.parse import urlparse\n",
        "from ludoweave.tools import cli\n",
    ],
)
def test_import_scan_detects_nested_forbidden_fixtures(tmp_path: Path, source: str) -> None:
    fixture = tmp_path / "invalid_evidence.py"
    fixture.write_text(source, encoding="utf-8")

    assert _forbidden(_imports(fixture))


def test_m27_adds_no_runtime_export_dependency_version_or_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["version"] == "0.1.0a1"
    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
    assert "ExternalContributorRehearsal" not in ludoweave.__all__
