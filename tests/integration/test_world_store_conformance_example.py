"""Source-tree WorldStore conformance example acceptance."""

import json
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

_EXAMPLE = Path(__file__).parents[2] / "examples" / "world_store_conformance.py"


@pytest.mark.parametrize("backend", ("world", "reference"))
def test_builtin_world_store_example_emits_path_free_success(backend: str) -> None:
    result = subprocess.run(
        (sys.executable, str(_EXAMPLE), "--backend", backend),
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["protocol"] == "ludoweave.world-store-conformance/1"
    assert report["profile"] == "world-store-baseline/1"
    assert report["adapter_id"] == f"ludoweave.{backend}"
    assert report["status"] == "pass"
    checks = cast(list[dict[str, object]], report["checks"])
    assert len(checks) == 10
    assert all(check["status"] == "pass" for check in checks)
    assert str(_EXAMPLE.parent) not in result.stdout


def test_world_store_example_rejects_unknown_backend_without_importing_it() -> None:
    result = subprocess.run(
        (sys.executable, str(_EXAMPLE), "--backend", "arbitrary.module"),
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "invalid choice" in result.stderr
