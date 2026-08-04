"""CLI version and doctor smoke tests."""

import json
import subprocess
import sys
from importlib.metadata import version
from typing import cast

import ludoweave


def _run_module(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "ludoweave", *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def test_python_version_matches_distribution_metadata() -> None:
    assert ludoweave.__version__ == version("ludoweave") == "0.1.0.dev0"
    assert set(ludoweave.__all__) == {"Engine", "EngineConfig", "LifecycleState", "__version__"}


def test_module_version_smoke() -> None:
    result = _run_module("--version")
    assert result.returncode == 0
    assert result.stdout.strip() == "ludoweave 0.1.0.dev0"
    assert result.stderr == ""


def test_doctor_emits_structured_success() -> None:
    result = _run_module("doctor")
    assert result.returncode == 0
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["schema"] == "ludoweave.doctor/1"
    assert report["status"] == "ok"
    assert report["ludoweave_version"] == "0.1.0.dev0"
    assert isinstance(report["checks"], list)
    assert result.stderr == ""
