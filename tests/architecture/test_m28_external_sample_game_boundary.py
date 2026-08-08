"""Keep M28 sample-game adoption evidence strict, offline, and outside runtime."""

import ast
import hashlib
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave

_ROOT = Path(__file__).parents[2]
_SAMPLES = _ROOT / "tests" / "fixtures" / "external_sample_game_adoption.json"
_EVIDENCE_FILES = (
    _ROOT / "examples" / "external_sample_game_adoption_readiness.py",
    _ROOT / "scripts" / "external_sample_game_adoption_evidence.py",
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


def test_sample_game_manifest_is_exact_empty_and_reviewed() -> None:
    payload = _SAMPLES.read_bytes()
    document = cast(dict[str, object], json.loads(payload))

    assert len(payload) == 280
    assert hashlib.sha256(payload).hexdigest() == (
        "ecdd0be75e42f047037c6799205786079274eb6d73d788f81e1061acc82008dd"
    )
    assert _literal(_EVIDENCE_FILES[0], "_REVIEWED_SAMPLE_GAME_SHA256") == (
        "ecdd0be75e42f047037c6799205786079274eb6d73d788f81e1061acc82008dd"
    )
    assert _literal(_EVIDENCE_FILES[0], "_MANDATORY_SAMPLE_GAME_PREFIX") == ()
    assert document == {
        "schema": "ludoweave.adoption.external-sample-games/1",
        "source_project": "ludoweave-engine",
        "minimum_external_sample_games": 1,
        "required_capabilities": [
            "headless-fixed-tick",
            "typed-command-receipt",
            "verified-replay",
        ],
        "sample_game_records": [],
    }


def test_sample_game_evidence_files_have_no_ambient_external_dependency() -> None:
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


def test_m28_adds_no_runtime_export_dependency_version_release_or_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["version"] == "0.1.0a1"
    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
    assert "ExternalSampleGame" not in ludoweave.__all__
    assert not any("external_sample" in path.name for path in (_ROOT / "src/ludoweave").rglob("*"))
    assert hashlib.sha256((_ROOT / ".github/workflows/release.yml").read_bytes()).hexdigest() == (
        "36822c260af578e3cd5a3456d17d655848c71bb305e861c4361cd03798aa86d2"
    )


def test_public_contract_retains_zero_external_sample_games() -> None:
    expected = {
        _ROOT / "README.md": "empty reviewed sample-game manifest",
        _ROOT / "ROADMAP.md": "M28 external sample-game adoption admission readiness",
        _ROOT / "docs/architecture.md": "M28 external sample-game adoption boundary",
        _ROOT / "docs/external-sample-game-adoption-readiness.md": (
            "No externally authored sample game is currently admitted"
        ),
        _ROOT / "docs/rfcs/0011-external-sample-game-adoption-admission-readiness.md": (
            "reviewed manifest contains no sample-game records"
        ),
    }
    for path, text in expected.items():
        assert text in path.read_text(encoding="utf-8")


def test_source_wheel_and_release_smoke_explicitly_include_m28_evidence() -> None:
    checks = {
        _ROOT / "scripts/smoke_wheel.py": (
            "validate_external_sample_game_adoption_evidence",
            "external_sample_game_adoption_readiness.py",
            "external_sample_game_adoption.json",
        ),
        _ROOT / "scripts/smoke_release.py": (
            "validate_external_sample_game_adoption_evidence",
            "external_sample_game_adoption_readiness.py",
        ),
        _ROOT / "scripts/release_artifacts.py": (
            "external_sample_game_adoption_readiness.py",
            "external_sample_game_adoption.json",
        ),
        _ROOT / "tests/unit/test_release_artifacts.py": (
            "external_sample_game_adoption_readiness.py",
            "external_sample_game_adoption.json",
        ),
    }
    for path, fragments in checks.items():
        source = path.read_text(encoding="utf-8")
        for fragment in fragments:
            assert fragment in source
