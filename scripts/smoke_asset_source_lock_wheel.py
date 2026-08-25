"""Install one wheel and verify bounded asset-source lock generation/verification."""

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
        raise RuntimeError("uv is required for the isolated asset-source-lock wheel smoke")
    project_root = Path(__file__).resolve().parents[1]
    local_temp = project_root / ".tmp"
    local_temp.mkdir(exist_ok=True)
    project: dict[str, object] = {
        "protocol": "ludoweave.headless-project/1",
        "world_id": "installed-asset-source-lock",
        "seed": "0000000000000001",
        "platform_profile": "cpython-portable-empty-v1",
        "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
    }
    scene: dict[str, object] = {
        "$schema": "ludoweave.scene/1",
        "scene_id": "installed-lock-scene",
        "entities": [],
        "dependencies": ["asset://materials/player.json"],
    }
    sources: dict[str, object] = {
        "$schema": "ludoweave.source-manifest/1",
        "manifest_id": "installed-asset-lock-sources",
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
        prefix="ludoweave-asset-source-lock-wheel-smoke-", dir=local_temp
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
        generated = _run(
            [str(python), "-I", "-m", "ludoweave", "source", "asset-lock", *common],
            cwd=temp_root,
        )
        lock_path = checked_project / "asset-source.lock.json"
        lock_path.write_text(generated.stdout, encoding="utf-8")
        verified = _run(
            [
                str(python),
                "-I",
                "-m",
                "ludoweave",
                "source",
                "asset-verify",
                *common,
                "--lock",
                "asset-source.lock.json",
            ],
            cwd=temp_root,
        )
        cache_absent = not (checked_project / "cache").exists()

    lock = cast(dict[str, object], json.loads(generated.stdout))
    report = cast(dict[str, object], json.loads(verified.stdout))
    entries = cast(list[dict[str, object]], lock["entries"])
    if (
        lock.get("$schema") != "ludoweave.asset-source-lock/1"
        or [entry.get("uri") for entry in entries]
        != ["asset://materials/player.json", "asset://textures/player.png"]
        or report
        != {
            "entry_count": 2,
            "lock_protocol": "ludoweave.asset-source-lock/1",
            "protocol": "ludoweave.cli.asset-source-lock-verify/1",
            "root_count": 1,
            "status": "valid",
        }
        or not cache_absent
    ):
        raise RuntimeError(
            f"installed asset-source lock result was invalid: lock={lock!r}, "
            f"report={report!r}, cache_absent={cache_absent!r}"
        )
    print(
        json.dumps(
            {
                "entries": len(entries),
                "lock_protocol": lock["$schema"],
                "schema": "ludoweave.asset-source-lock-wheel-smoke/1",
                "status": "pass",
                "verify_protocol": report["protocol"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
