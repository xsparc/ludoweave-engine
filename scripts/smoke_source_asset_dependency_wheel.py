"""Install one wheel and verify source-to-asset dependency checking."""

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
        raise RuntimeError("uv is required for the isolated source-asset wheel smoke test")
    project_root = Path(__file__).resolve().parents[1]
    local_temp = project_root / ".tmp"
    local_temp.mkdir(exist_ok=True)
    project: dict[str, object] = {
        "protocol": "ludoweave.headless-project/1",
        "world_id": "installed-source-assets",
        "seed": "0000000000000001",
        "platform_profile": "cpython-portable-empty-v1",
        "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
    }
    scene: dict[str, object] = {
        "$schema": "ludoweave.scene/1",
        "scene_id": "installed-scene",
        "entities": [],
        "dependencies": ["asset://materials/player.json"],
    }
    sources: dict[str, object] = {
        "$schema": "ludoweave.source-manifest/1",
        "manifest_id": "installed-source-assets",
        "entries": [{"entry_id": "scene", "kind": "scene", "source": "scene.json"}],
    }
    assets: dict[str, object] = {
        "protocol": "ludoweave.assets/1",
        "assets": [
            {
                "uri": "asset://materials/player.json",
                "kind": "json",
                "source": "assets/material.json",
                "settings": {},
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
        prefix="ludoweave-source-asset-wheel-smoke-", dir=local_temp
    ) as temp_name:
        temp_root = Path(temp_name)
        environment = temp_root / "venv"
        checked_project = temp_root / "project"
        checked_project.mkdir()
        (checked_project / "ludoweave.project.json").write_bytes(_canonical(project))
        (checked_project / "scene.json").write_bytes(_canonical(scene))
        (checked_project / "sources.json").write_bytes(_canonical(sources))
        (checked_project / "assets.json").write_bytes(_canonical(assets))
        _run([uv, "venv", "--python", "3.12", str(environment)], cwd=temp_root)
        python = _python_in(environment)
        _run(
            [uv, "pip", "install", "--python", str(python), "--no-deps", str(wheels[0])],
            cwd=temp_root,
        )
        result = _run(
            [
                str(python),
                "-I",
                "-m",
                "ludoweave",
                "source",
                "assets",
                str(checked_project),
                "--manifest",
                "sources.json",
                "--assets",
                "assets.json",
            ],
            cwd=temp_root,
        )
        sources_absent = not (checked_project / "assets").exists()

    expected: dict[str, object] = {
        "protocol": "ludoweave.cli.source-asset-check/1",
        "status": "valid",
        "source_manifest_protocol": "ludoweave.source-manifest/1",
        "source_manifest_id": "installed-source-assets",
        "source_manifest_sha256": f"sha256:{sha256(_canonical(sources)).hexdigest()}",
        "asset_manifest_protocol": "ludoweave.assets/1",
        "asset_manifest_sha256": f"sha256:{sha256(_canonical(assets)).hexdigest()}",
        "entries": [
            {
                "entry_id": "scene",
                "kind": "scene",
                "direct": ["asset://materials/player.json"],
                "resolved": [
                    "asset://materials/player.json",
                    "asset://textures/player.png",
                ],
            }
        ],
        "entry_count": 1,
        "direct_asset_count": 1,
        "resolved_asset_count": 2,
    }
    summary = cast(dict[str, object], json.loads(result.stdout))
    if summary != expected or not sources_absent:
        raise RuntimeError(
            f"installed source-asset summary was invalid: {summary!r}, "
            f"sources_absent={sources_absent!r}"
        )
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
