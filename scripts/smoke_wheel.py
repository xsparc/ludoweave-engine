"""Install the built wheel into a temporary environment and run M0 smoke checks."""

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from collections.abc import Sequence
from pathlib import Path
from typing import cast


def _run(command: Sequence[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        rendered = subprocess.list2cmdline(command)
        raise RuntimeError(
            f"command failed with exit {result.returncode}: {rendered}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def _python_in(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def _ludoweave_in(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "ludoweave.exe"
    return environment / "bin" / "ludoweave"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dist", type=Path, help="directory containing exactly one wheel")
    args = parser.parse_args(argv)
    dist: object = getattr(args, "dist", None)
    if not isinstance(dist, Path):
        parser.error("dist must be a directory path")
    wheels = sorted(dist.resolve().glob("ludoweave-*.whl"))
    if len(wheels) != 1:
        parser.error(f"expected exactly one LudoWeave wheel in {dist}, found {len(wheels)}")

    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("uv is required for the isolated wheel smoke test")

    project_root = Path(__file__).resolve().parents[1]
    local_temp = project_root / ".tmp"
    local_temp.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ludoweave-wheel-smoke-", dir=local_temp) as temp_name:
        temp_root = Path(temp_name)
        environment = temp_root / "venv"
        _run([uv, "venv", "--python", "3.12", str(environment)], cwd=temp_root)
        python = _python_in(environment)
        _run(
            [uv, "pip", "install", "--python", str(python), "--no-deps", str(wheels[0])],
            cwd=temp_root,
        )

        ludoweave = _ludoweave_in(environment)
        version_result = _run([str(ludoweave), "--version"], cwd=temp_root)
        if version_result.stdout.strip() != "ludoweave 0.1.0.dev0":
            raise RuntimeError(f"unexpected version output: {version_result.stdout!r}")

        doctor_result = _run([str(ludoweave), "doctor"], cwd=temp_root)
        doctor = cast(dict[str, object], json.loads(doctor_result.stdout))
        if doctor.get("status") != "ok":
            raise RuntimeError(f"doctor did not report success: {doctor!r}")

        example_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "hello_headless.py"),
                "--ticks",
                "3",
            ],
            cwd=temp_root,
        )
        summary = cast(dict[str, object], json.loads(example_result.stdout))
        expected = {"ticks": 3, "frames": 3, "renderer": "null", "final_state": "closed"}
        if any(summary.get(key) != value for key, value in expected.items()):
            raise RuntimeError(f"headless example summary was invalid: {summary!r}")

    print(f"wheel smoke passed: {wheels[0].name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
