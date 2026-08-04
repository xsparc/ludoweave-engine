"""Source-tree headless example acceptance test."""

import json
import subprocess
import sys
from pathlib import Path
from typing import cast


def test_headless_example_runs_requested_virtual_ticks() -> None:
    project_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, str(project_root / "examples" / "hello_headless.py"), "--ticks", "7"],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    summary = cast(dict[str, object], json.loads(result.stdout))
    assert summary == {
        "schema": "ludoweave.example.headless/1",
        "ludoweave_version": "0.1.0.dev0",
        "ticks": 7,
        "frames": 7,
        "fixed_hz": 60,
        "elapsed_ns": 116_666_666,
        "renderer": "null",
        "final_state": "closed",
    }
    assert result.stderr == ""
