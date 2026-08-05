"""Source-tree render-device conformance example acceptance."""

import json
import subprocess
import sys
from pathlib import Path
from typing import cast


def test_null_conformance_example_emits_versioned_path_free_success() -> None:
    example = Path(__file__).parents[2] / "examples" / "render_device_conformance.py"
    result = subprocess.run(
        (sys.executable, str(example)),
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["protocol"] == "ludoweave.render-device-conformance/1"
    assert report["profile"] == "render-device-baseline/1"
    assert report["adapter_id"] == "org.ludoweave.null"
    assert report["adapter_name"] == "null-device"
    assert report["status"] == "pass"
    checks = cast(list[dict[str, object]], report["checks"])
    assert len(checks) == 9
    assert all(check["status"] == "pass" for check in checks)
    assert str(example.parent) not in result.stdout


def test_conformance_example_rejects_unknown_backend_without_importing_it() -> None:
    example = Path(__file__).parents[2] / "examples" / "render_device_conformance.py"
    result = subprocess.run(
        (sys.executable, str(example), "--backend", "unknown"),
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "invalid choice" in result.stderr
