"""Keep M13 evidence offline, deterministic, provider-neutral, and inert."""

import ast
from pathlib import Path

import pytest

_ROOT = Path(__file__).parents[2]
_EVIDENCE_FILES = (
    _ROOT / "examples" / "rollback_readiness.py",
    _ROOT / "scripts" / "validate_rollback_readiness.py",
)
_ALLOWED_DIRECT_IMPORTS = {
    "rollback_readiness.py": {"argparse", "json"},
    "validate_rollback_readiness.py": {"argparse"},
}
_ALLOWED_FROM_IMPORTS = {
    "rollback_readiness.py": {
        "__future__:annotations",
        "collections.abc:Sequence",
        "ludoweave:__version__",
        "ludoweave.app:InputSnapshot",
        "ludoweave.app:RecordedInputSource",
        "ludoweave.samples:clockwork_input",
        "ludoweave.samples:create_clockwork_arena",
        "ludoweave.samples.clockwork_arena:ARENA_LOCK_HASH",
        "ludoweave.samples.clockwork_arena:ARENA_PLATFORM_PROFILE",
        "ludoweave.samples.clockwork_arena:ARENA_PROJECT_SCHEMA",
        "ludoweave.samples.clockwork_arena:ArenaTickExecutor",
        "ludoweave.samples.clockwork_arena:arena_tick_transaction",
        "ludoweave.world:ReceiptStatus",
        "ludoweave.world:ReplayDivergenceError",
        "ludoweave.world:ReplayRecorder",
        "ludoweave.world:ReplayRunner",
        "pathlib:Path",
    },
    "validate_rollback_readiness.py": {
        "__future__:annotations",
        "collections.abc:Mapping",
        "collections.abc:Sequence",
        "ludoweave:__version__",
        "ludoweave.world:JsonLimits",
        "ludoweave.world:canonical_loads",
        "os:fstat",
        "pathlib:Path",
        "stat:S_ISREG",
        "typing:cast",
    },
}
_BANNED_NAMES = {
    "__builtins__",
    "__import__",
    "compile",
    "eval",
    "exec",
    "getattr",
    "globals",
    "input",
    "locals",
    "open",
    "setattr",
    "vars",
}


def test_m13_evidence_files_obey_offline_boundary() -> None:
    violations = {
        path.name: _boundary_violations(path.read_text(encoding="utf-8"), path.name)
        for path in _EVIDENCE_FILES
    }

    assert violations == {path.name: [] for path in _EVIDENCE_FILES}


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("import socket\n", "module:socket"),
        ("from urllib.request import urlopen\n", "from:urllib.request:urlopen"),
        ("import time\n", "module:time"),
        ("import smtplib\n", "module:smtplib"),
        ("import ssl\n", "module:ssl"),
        ("import webbrowser\n", "module:webbrowser"),
        ("eval('1')\n", "name:eval"),
        ("loader = __import__\nloader('socket')\n", "name:__import__"),
        ("runner = eval\nrunner('1')\n", "name:eval"),
        ("from pathlib import os\n", "from:pathlib:os"),
        ("from ludoweave import tools\n", "from:ludoweave:tools"),
    ],
)
def test_m13_boundary_checker_rejects_forbidden_fixtures(source: str, expected: str) -> None:
    assert expected in _boundary_violations(source, "fixture.py")


def _boundary_violations(source: str, filename: str) -> list[str]:
    tree = ast.parse(source)
    violations: list[str] = []
    direct_imports = _ALLOWED_DIRECT_IMPORTS.get(filename, set())
    from_imports = _ALLOWED_FROM_IMPORTS.get(filename, set())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name not in direct_imports:
                    violations.append(f"module:{alias.name.split('.', maxsplit=1)[0]}")
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            for alias in node.names:
                marker = f"{node.module}:{alias.name}"
                if marker not in from_imports:
                    violations.append(f"from:{marker}")
        elif isinstance(node, ast.Name) and node.id in _BANNED_NAMES:
            violations.append(f"name:{node.id}")
    return sorted(violations)
