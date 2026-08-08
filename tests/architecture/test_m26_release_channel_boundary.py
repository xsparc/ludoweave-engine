"""Keep M26 release-channel evidence strict, offline, and outside runtime source."""

import ast
import hashlib
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave

_ROOT = Path(__file__).parents[2]
_CHANNEL = _ROOT / "tests" / "fixtures" / "supported_release_channel.json"
_RELEASE_WORKFLOW = _ROOT / ".github" / "workflows" / "release.yml"
_COMPATIBILITY_POLICY = _ROOT / "API_COMPATIBILITY.md"
_EVIDENCE_FILES = (
    _ROOT / "examples" / "supported_release_channel_readiness.py",
    _ROOT / "scripts" / "supported_release_channel_evidence.py",
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


def test_release_channel_manifest_is_exact_empty_and_reviewed() -> None:
    payload = _CHANNEL.read_bytes()
    document = cast(dict[str, object], json.loads(payload))

    assert len(payload) == 278
    assert hashlib.sha256(payload).hexdigest() == (
        "f23b4314696384ad288b86c63bc101606f1aa9f323c4fb186486d8c74915ec41"
    )
    assert _literal(_EVIDENCE_FILES[0], "_REVIEWED_RELEASE_CHANNEL_SHA256") == (
        "f23b4314696384ad288b86c63bc101606f1aa9f323c4fb186486d8c74915ec41"
    )
    assert _literal(_EVIDENCE_FILES[0], "_MANDATORY_RELEASE_PREFIX") == ()
    assert document == {
        "schema": "ludoweave.compatibility.supported-release-channel/1",
        "source_package": "ludoweave",
        "minimum_supported_feature_releases": 2,
        "deprecation_window_feature_releases": 1,
        "required_publication_channels": ["github-release"],
        "release_records": [],
    }


def test_m26_does_not_relabel_or_expand_the_existing_release_workflow() -> None:
    workflow = _RELEASE_WORKFLOW.read_bytes()

    assert hashlib.sha256(workflow).hexdigest() == (
        "3983cd82f0201fcac8fe2156f77715e1136998781b428c60a192b3f3a3522871"
    )
    text = workflow.decode("utf-8")
    assert 'tags:\n      - "v*"' in text
    assert "--prerelease" in text
    assert "pypi" not in text.casefold()
    assert "workflow_dispatch" not in text


def test_release_channel_window_matches_the_public_compatibility_policy() -> None:
    policy = _COMPATIBILITY_POLICY.read_text(encoding="utf-8")

    assert (
        "preview`: intended to stabilize; incompatible removal requires a documented\n"
        "  deprecation in at least one feature release;"
    ) in policy


def test_release_channel_evidence_files_have_no_ambient_external_dependency() -> None:
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


def test_m26_adds_no_runtime_export_dependency_version_or_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["version"] == "0.1.0a1"
    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
    assert "SupportedReleaseChannel" not in ludoweave.__all__
