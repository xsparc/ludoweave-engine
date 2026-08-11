"""Keep M34 agent-tool recovery-rate evidence strict, offline, and non-runtime."""

import ast
import hashlib
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave
from ludoweave.agent import AGENT_TOOL_NAMES

_ROOT = Path(__file__).parents[2]
_MANIFEST = _ROOT / "tests" / "fixtures" / "agent_tool_recovery_rate.json"
_EVIDENCE_FILES = (
    _ROOT / "examples" / "agent_tool_recovery_rate_readiness.py",
    _ROOT / "scripts" / "agent_tool_recovery_rate_evidence.py",
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
    "ludoweave.agent",
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


def test_agent_tool_recovery_manifest_is_exact_empty_and_reviewed() -> None:
    payload = _MANIFEST.read_bytes()
    document = cast(dict[str, object], json.loads(payload))

    assert len(payload) == 195
    assert hashlib.sha256(payload).hexdigest() == (
        "e952c045b039055e8439069cf88176b6ac1d2ad7de49a94d39b2737e5d06e1d5"
    )
    assert _literal(_EVIDENCE_FILES[0], "_REVIEWED_MANIFEST_SHA256") == (
        "e952c045b039055e8439069cf88176b6ac1d2ad7de49a94d39b2737e5d06e1d5"
    )
    assert _literal(_EVIDENCE_FILES[0], "_MANDATORY_WINDOW_PREFIX") == ()
    assert document == {
        "schema": "ludoweave.operations.agent-tool-recovery-rate/1",
        "source_project": "ludoweave-engine",
        "measurement_policy": "complete-reviewed-task-directed-agent-tool-calls/1",
        "evaluation_windows": [],
    }


def test_agent_tool_recovery_evidence_files_are_bounded_and_offline() -> None:
    assert _literal(_EVIDENCE_FILES[0], "_MAX_MANIFEST_BYTES") == 131_072
    assert _literal(_EVIDENCE_FILES[0], "_MAX_JSON_NESTING") == 16
    assert _literal(_EVIDENCE_FILES[0], "_MAX_EVALUATION_WINDOWS") == 12
    assert _literal(_EVIDENCE_FILES[0], "_MAX_CALLS_PER_WINDOW") == 2_048
    for path in _EVIDENCE_FILES:
        assert _forbidden(_imports(path)) == set()


@pytest.mark.parametrize(
    "source",
    [
        "def nested() -> None:\n    import socket\n",
        "if True:\n    from importlib import import_module\n",
        "try:\n    import subprocess\nexcept ImportError:\n    pass\n",
        "from urllib.parse import urlparse\n",
        "from ludoweave.agent import AGENT_TOOL_NAMES\n",
    ],
)
def test_import_scan_detects_nested_forbidden_fixtures(tmp_path: Path, source: str) -> None:
    fixture = tmp_path / "invalid_evidence.py"
    fixture.write_text(source, encoding="utf-8")

    assert _forbidden(_imports(fixture))


def test_m34_adds_no_runtime_export_dependency_version_release_or_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["version"] == "0.1.0a1"
    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
    assert "AgentToolRecoveryRate" not in ludoweave.__all__
    assert not any(
        "agent_tool_recovery_rate" in path.name for path in (_ROOT / "src" / "ludoweave").rglob("*")
    )
    assert hashlib.sha256((_ROOT / ".github/workflows/release.yml").read_bytes()).hexdigest() == (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    )


def test_evaluator_registers_the_exact_product_tool_set_without_importing_it() -> None:
    assert _literal(_EVIDENCE_FILES[0], "_TOOL_NAMES") == AGENT_TOOL_NAMES
    assert _literal(_EVIDENCE_FILES[0], "_SERVICE_PROTOCOL") == "ludoweave.agent.service/1"


def test_ci_retains_the_m34_pr_only_quota_boundary() -> None:
    workflow = (_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert '\non:\n  pull_request:\n    paths-ignore:\n      - ".project/**"\n' in workflow
    assert "\n  push:" not in workflow
    assert "\n  schedule:" not in workflow
    assert "\n  workflow_dispatch:" not in workflow
    assert "permissions:\n  contents: read" in workflow
    assert "cancel-in-progress: true" in workflow


def test_source_wheel_and_release_smoke_explicitly_include_m34_evidence() -> None:
    checks = {
        _ROOT / "scripts" / "smoke_wheel.py": (
            "validate_agent_tool_recovery_rate_evidence",
            "agent_tool_recovery_rate_readiness.py",
            "agent_tool_recovery_rate.json",
        ),
        _ROOT / "scripts" / "smoke_release.py": (
            "validate_agent_tool_recovery_rate_evidence",
            "agent_tool_recovery_rate_readiness.py",
        ),
        _ROOT / "scripts" / "release_artifacts.py": (
            "agent_tool_recovery_rate_readiness.py",
            "agent_tool_recovery_rate.json",
        ),
        _ROOT / "tests" / "unit" / "test_release_artifacts.py": (
            "agent_tool_recovery_rate_readiness.py",
            "agent_tool_recovery_rate.json",
        ),
    }
    for path, required in checks.items():
        text = path.read_text(encoding="utf-8")
        assert all(item in text for item in required)


def test_m34_public_contract_and_indices_are_registered() -> None:
    required = {
        _ROOT / "README.md": (
            "empty reviewed agent-tool call manifest",
            "no measured recovery-free completion rate",
        ),
        _ROOT / "ROADMAP.md": (
            "M34 agent-tool recovery-rate admission readiness",
            "terminal-unobserved",
        ),
        _ROOT / "MAINTAINERS.md": (
            "M34 adds strict offline agent-tool recovery-rate admission readiness",
            "one substantive pull-request run",
        ),
        _ROOT / "docs" / "architecture.md": (
            "M34 agent-tool recovery-rate boundary",
            "no call count or recovery-free completion rate is exposed",
        ),
        _ROOT / "docs" / "agent-tool-recovery-rate-readiness.md": (
            "agent-tool-recovery-rate-evidence-absent",
            "completed-after-manual-recovery",
            "Required approval before dispatch",
        ),
        _ROOT / "docs" / "rfcs" / "0017-agent-tool-recovery-rate-admission-readiness.md": (
            "reviewed manifest contains no evaluation windows",
            "No success target",
            "synthetic fixtures, conformance profiles",
        ),
        _ROOT / "mkdocs.yml": (
            "agent-tool-recovery-rate-readiness.md",
            "0017-agent-tool-recovery-rate-admission-readiness.md",
        ),
        _ROOT / "docs" / "rfcs" / "index.md": (
            "RFC-0017: agent-tool recovery-rate admission readiness",
        ),
        _ROOT / "docs" / "api-status.md": ("M34 adds no export",),
        _ROOT / "docs" / "release-process.md": ("M34/RFC-0017",),
        _ROOT / "docs" / "alpha-retrospective.md": ("M34 defines",),
        _ROOT / "examples" / "README.md": ("agent_tool_recovery_rate_readiness.py",),
    }
    for path, values in required.items():
        text = path.read_text(encoding="utf-8")
        assert all(value in text for value in values)


def test_neutral_repository_metadata_convention_remains_active() -> None:
    assert (_ROOT / "MAINTAINERS.md").is_file()
    assert (_ROOT / ".project").is_dir()
