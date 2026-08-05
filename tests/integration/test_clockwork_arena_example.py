"""Source-tree Clockwork Arena example smoke test."""

import json
import subprocess
import sys
from pathlib import Path


def test_clockwork_arena_example_runs_null_device_and_prints_summary() -> None:
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        (
            sys.executable,
            str(root / "examples" / "clockwork_arena.py"),
            "--ticks",
            "30",
            "--render-every",
            "10",
        ),
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["schema"] == "ludoweave.example.clockwork_arena/1"
    assert payload["renderer"] == "null"
    assert payload["arena"]["ticks"] == 30
    assert payload["draw_calls"] == 3
    assert payload["sprite_instances"] > 0
