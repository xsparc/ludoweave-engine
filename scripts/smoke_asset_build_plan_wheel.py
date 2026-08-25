"""Install one wheel and verify deterministic asset build-plan generation."""

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from collections.abc import Sequence
from hashlib import sha256
from pathlib import Path
from typing import cast


def _run(command: Sequence[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed with exit {result.returncode}: "
            f"{subprocess.list2cmdline(command)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def _python_in(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def _canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode(
        "utf-8"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dist", type=Path, help="directory containing exactly one wheel")
    args = parser.parse_args(argv)
    dist: object = getattr(args, "dist", None)
    if not isinstance(dist, Path) or not dist.is_dir():
        parser.error("dist must be an existing directory")
    wheels = sorted(dist.resolve().glob("ludoweave-*.whl"))
    if len(wheels) != 1:
        parser.error(f"expected exactly one LudoWeave wheel in {dist}, found {len(wheels)}")

    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("uv is required for the isolated asset-build-plan wheel smoke")
    project_root = Path(__file__).resolve().parents[1]
    local_temp = project_root / ".tmp"
    local_temp.mkdir(exist_ok=True)
    project: dict[str, object] = {
        "protocol": "ludoweave.headless-project/1",
        "world_id": "installed-asset-build-plan",
        "seed": "0000000000000001",
        "platform_profile": "cpython-portable-empty-v1",
        "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
    }
    scene: dict[str, object] = {
        "$schema": "ludoweave.scene/1",
        "scene_id": "installed-build-plan-scene",
        "entities": [],
        "dependencies": ["asset://materials/player.json"],
    }
    sources: dict[str, object] = {
        "$schema": "ludoweave.source-manifest/1",
        "manifest_id": "installed-build-plan-sources",
        "entries": [{"entry_id": "scene", "kind": "scene", "source": "scene.json"}],
    }
    assets: dict[str, object] = {
        "protocol": "ludoweave.assets/1",
        "assets": [
            {
                "uri": "asset://materials/player.json",
                "kind": "json",
                "source": "assets/material.json",
                "settings": {"mode": "strict"},
                "dependencies": ["asset://textures/player.png"],
            },
            {
                "uri": "asset://textures/player.png",
                "kind": "png",
                "source": "assets/player.png",
                "settings": {},
                "dependencies": [],
            },
        ],
    }
    with tempfile.TemporaryDirectory(
        prefix="ludoweave-asset-build-plan-wheel-smoke-", dir=local_temp
    ) as temp_name:
        temp_root = Path(temp_name)
        environment = temp_root / "venv"
        checked_project = temp_root / "project"
        source_directory = checked_project / "assets"
        source_directory.mkdir(parents=True)
        (checked_project / "ludoweave.project.json").write_bytes(_canonical(project))
        (checked_project / "scene.json").write_bytes(_canonical(scene))
        (checked_project / "sources.json").write_bytes(_canonical(sources))
        (checked_project / "assets.json").write_bytes(_canonical(assets))
        (source_directory / "material.json").write_bytes(b"opaque json source")
        (source_directory / "player.png").write_bytes(b"opaque png source")
        _run([uv, "venv", "--python", "3.12", str(environment)], cwd=temp_root)
        python = _python_in(environment)
        _run(
            [uv, "pip", "install", "--python", str(python), "--no-deps", str(wheels[0])],
            cwd=temp_root,
        )
        common = [
            str(checked_project),
            "--manifest",
            "sources.json",
            "--assets",
            "assets.json",
        ]
        locked = _run(
            [str(python), "-I", "-m", "ludoweave", "source", "asset-lock", *common],
            cwd=temp_root,
        )
        lock_path = checked_project / "assets.lock.json"
        lock_path.write_text(locked.stdout, encoding="utf-8")
        planned = _run(
            [
                str(python),
                "-I",
                "-m",
                "ludoweave",
                "source",
                "asset-plan",
                *common,
                "--lock",
                "assets.lock.json",
            ],
            cwd=temp_root,
        )
        cache_absent = not (checked_project / "cache").exists()

    plan = cast(dict[str, object], json.loads(planned.stdout))
    entries = cast(list[dict[str, object]], plan["entries"])
    if (
        plan.get("$schema") != "ludoweave.asset-build-plan/1"
        or plan.get("loader_protocol") != "ludoweave.assets/1"
        or [entry.get("uri") for entry in entries]
        != ["asset://textures/player.png", "asset://materials/player.json"]
        or not all(str(entry.get("cache_key", "")).startswith("sha256:") for entry in entries)
        or not cache_absent
    ):
        raise RuntimeError(
            f"installed asset build plan was invalid: plan={plan!r}, cache_absent={cache_absent!r}"
        )
    print(
        json.dumps(
            {
                "entries": len(entries),
                "loader_protocol": plan["loader_protocol"],
                "plan_protocol": plan["$schema"],
                "schema": "ludoweave.asset-build-plan-wheel-smoke/1",
                "status": "pass",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
