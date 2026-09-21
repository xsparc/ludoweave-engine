"""Record and replay in separate isolated wheel processes without dependencies."""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dist", type=Path)
    args = parser.parse_args(argv)
    wheels = sorted(Path(args.dist).resolve().glob("ludoweave-*.whl"))
    if len(wheels) != 1:
        parser.error("dist must contain exactly one LudoWeave wheel")
    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("uv is required")
    example = Path(__file__).resolve().parents[1] / "examples" / "input_replay.py"
    with tempfile.TemporaryDirectory(prefix="ludoweave-input-replay-") as directory:
        work = Path(directory)
        environment = work / "environment"
        python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        subprocess.run(
            [uv, "venv", "--python", sys.executable, str(environment)], cwd=work, check=True
        )
        subprocess.run(
            [uv, "pip", "install", "--python", str(python), "--no-deps", str(wheels[0])],
            cwd=work,
            check=True,
        )
        copied = work / "input_replay.py"
        shutil.copyfile(example, copied)
        artifact = work / "recording.json"
        results: list[str] = []
        for arguments in (
            ["record", str(artifact), "--ticks", "120"],
            ["replay", str(artifact)],
        ):
            result = subprocess.run(
                [str(python), "-I", str(copied), *arguments],
                cwd=work,
                capture_output=True,
                text=True,
                check=True,
                timeout=120,
            )
            results.append(result.stdout.strip())
        if results[0] != results[1]:
            raise RuntimeError("fresh-process installed replay disagrees with recording")
        play = work / "clockwork_arena.py"
        shutil.copyfile(example.with_name("clockwork_arena.py"), play)
        play_artifact = work / "play.json"
        played = subprocess.run(
            [str(python), "-I", str(play), "--ticks", "30", "--record", str(play_artifact)],
            cwd=work,
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
        replayed = subprocess.run(
            [str(python), "-I", str(copied), "replay", str(play_artifact)],
            cwd=work,
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
        summary = json.loads(played.stdout)["arena"]
        verified = json.loads(replayed.stdout)
        if summary["ticks"] != verified["ticks"] or summary["state_hash"] != verified["state_hash"]:
            raise RuntimeError("installed play-session recording diverged")
        viewer = work / "play_input_replay.py"
        shutil.copyfile(example.with_name("play_input_replay.py"), viewer)
        refused = subprocess.run(
            [str(python), "-I", str(viewer), str(play_artifact), "--controls"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        if refused.returncode != 2 or "--controls requires --window" not in refused.stderr:
            raise RuntimeError("installed playback control admission diverged")
        displayed = subprocess.run(
            [str(python), "-I", str(viewer), str(play_artifact)],
            cwd=work,
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
        playback = json.loads(displayed.stdout)
        if (
            playback["schema"] != "ludoweave.input-replay-playback/1"
            or playback["verification"] != "pass"
            or playback["playback"] != "complete"
            or playback["frames"] != 31
            or playback["arena"]["state_hash"] != verified["state_hash"]
        ):
            raise RuntimeError("installed recorded presentation diverged")
    print(json.dumps({"schema": "ludoweave.input-replay-wheel-smoke/1", "status": "pass"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
