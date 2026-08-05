"""Source-tree acceptance for the M11 headless rich-2D showcase."""

import json
import subprocess
import sys
from pathlib import Path
from typing import cast

_ROOT = Path(__file__).resolve().parents[2]


def _run() -> dict[str, object]:
    result = subprocess.run(
        (sys.executable, str(_ROOT / "examples" / "rich_2d_showcase.py"), "--ticks", "6"),
        cwd=_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return cast(dict[str, object], json.loads(result.stdout))


def test_rich_2d_showcase_is_repeatable_and_exercises_every_module() -> None:
    first = _run()
    second = _run()

    assert first == second
    assert first["schema"] == "ludoweave.example.rich_2d/1"
    assert first["ticks"] == 6
    assert first["audio_gain"] == 0.2
    assert first["glyphs"] == 9
    assert first["particles"] == 10
    assert first["tile_instances"] == 8
    assert first["sprite_instances"] == 20
    assert first["draw_calls"] == 2
