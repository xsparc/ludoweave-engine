"""Keep M32 replay-divergence-rate evidence strict, offline, and non-runtime."""

import ast
import hashlib
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave

_ROOT = Path(__file__).parents[2]
_MANIFEST = _ROOT / "tests" / "fixtures" / "replay_divergence_rate.json"
_EVIDENCE_FILES = (
    _ROOT / "examples" / "replay_divergence_rate_readiness.py",
    _ROOT / "scripts" / "replay_divergence_rate_evidence.py",
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


def test_replay_divergence_manifest_is_exact_empty_and_reviewed() -> None:
    payload = _MANIFEST.read_bytes()
    document = cast(dict[str, object], json.loads(payload))

    assert len(payload) == 175
    assert hashlib.sha256(payload).hexdigest() == (
        "cff8a32428ac8dcd18029be4f70e9d359b4c9d70fd411ffe2f36d35704d68aa7"
    )
    assert _literal(_EVIDENCE_FILES[0], "_REVIEWED_MANIFEST_SHA256") == (
        "cff8a32428ac8dcd18029be4f70e9d359b4c9d70fd411ffe2f36d35704d68aa7"
    )
    assert _literal(_EVIDENCE_FILES[0], "_MANDATORY_WINDOW_PREFIX") == ()
    assert document == {
        "schema": "ludoweave.ci.replay-divergence-rate/1",
        "source_project": "ludoweave-engine",
        "measurement_policy": "complete-reviewed-ci-replay-executions/1",
        "evaluation_windows": [],
    }


def test_replay_divergence_evidence_files_are_bounded_and_offline() -> None:
    assert _literal(_EVIDENCE_FILES[0], "_MAX_MANIFEST_BYTES") == 65_536
    assert _literal(_EVIDENCE_FILES[0], "_MAX_JSON_NESTING") == 16
    assert _literal(_EVIDENCE_FILES[0], "_MAX_EVALUATION_WINDOWS") == 12
    assert _literal(_EVIDENCE_FILES[0], "_MAX_EXECUTIONS_PER_WINDOW") == 512
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


def test_m32_adds_no_runtime_export_dependency_version_release_or_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["version"] == "0.1.0a1"
    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
    assert "ReplayDivergenceRate" not in ludoweave.__all__
    assert not any(
        "replay_divergence_rate" in path.name for path in (_ROOT / "src/ludoweave").rglob("*")
    )
    assert hashlib.sha256((_ROOT / ".github/workflows/release.yml").read_bytes()).hexdigest() == (
        "d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8"
    )


def test_evaluator_uses_the_runtime_replay_divergence_code() -> None:
    runtime = (_ROOT / "src" / "ludoweave" / "world" / "replay.py").read_text(encoding="utf-8")
    evaluator = _EVIDENCE_FILES[0].read_text(encoding="utf-8")

    assert 'code="world.replay.diverged"' in runtime
    assert 'outcome_code != "world.replay.diverged"' in evaluator
    assert "world.replay.divergence" not in evaluator


def test_public_contract_retains_empty_execution_manifest_and_no_rate_claim() -> None:
    expected = {
        _ROOT / "README.md": (
            "empty reviewed execution manifest",
            "no measured divergence rate",
        ),
        _ROOT / "ROADMAP.md": (
            "M32 replay-divergence-rate admission readiness",
            "no execution count or divergence rate is claimed",
        ),
        _ROOT / "MAINTAINERS.md": (
            "M32 adds only strict offline CI replay-divergence-rate",
            "no zero-divergence, reliability, quality",
        ),
        _ROOT / "docs" / "architecture.md": (
            "M32 replay-divergence-rate boundary",
            "no measured rate",
        ),
        _ROOT / "docs" / "replay-divergence-rate-readiness.md": (
            "replay-divergence-rate-evidence-absent",
            "not a measured zero-divergence result",
            "Intentionally corrupted negative fixtures",
        ),
        _ROOT / "docs" / "rfcs" / "0015-replay-divergence-rate-admission-readiness.md": (
            "reviewed manifest contains no evaluation windows",
            "No threshold, quality verdict",
            "intentionally divergent negative fixtures",
        ),
    }
    for path, required in expected.items():
        content = path.read_text(encoding="utf-8")
        assert all(text in content for text in required)


def test_source_wheel_and_release_smoke_explicitly_include_m32_evidence() -> None:
    checks = {
        _ROOT / "scripts" / "smoke_wheel.py": (
            "validate_replay_divergence_rate_evidence",
            "replay_divergence_rate_readiness.py",
            "replay_divergence_rate.json",
        ),
        _ROOT / "scripts" / "smoke_release.py": (
            "validate_replay_divergence_rate_evidence",
            "replay_divergence_rate_readiness.py",
        ),
        _ROOT / "scripts" / "release_artifacts.py": (
            "replay_divergence_rate_readiness.py",
            "replay_divergence_rate.json",
        ),
        _ROOT / "tests" / "unit" / "test_release_artifacts.py": (
            "replay_divergence_rate_readiness.py",
            "replay_divergence_rate.json",
        ),
    }
    for path, required in checks.items():
        text = path.read_text(encoding="utf-8")
        assert all(item in text for item in required)


def test_m32_docs_and_indices_are_registered() -> None:
    required = {
        _ROOT / "mkdocs.yml": (
            "replay-divergence-rate-readiness.md",
            "0015-replay-divergence-rate-admission-readiness.md",
        ),
        _ROOT / "docs" / "rfcs" / "index.md": (
            "RFC-0015: replay-divergence-rate admission readiness",
        ),
        _ROOT / "docs" / "api-status.md": ("M32 adds no export",),
        _ROOT / "docs" / "release-process.md": ("M32/RFC-0015",),
        _ROOT / "docs" / "alpha-retrospective.md": ("M32 defines",),
        _ROOT / "examples" / "README.md": ("replay_divergence_rate_readiness.py",),
    }
    for path, values in required.items():
        text = path.read_text(encoding="utf-8")
        assert all(value in text for value in values)


def test_neutral_repository_metadata_convention_remains_active() -> None:
    assert (_ROOT / "MAINTAINERS.md").is_file()
    assert (_ROOT / ".project").is_dir()
    for retired in (".ai", ".agents", ".codex", "AGENTS.md"):
        assert not (_ROOT / retired).exists()
