"""Install one wheel and verify read-only cache-assisted asset realization."""

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
    return environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def _canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode(
        "utf-8"
    )


def _files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


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
        raise RuntimeError("uv is required for the isolated asset-realization smoke")

    repository = Path(__file__).resolve().parents[1]
    local_temp = repository / ".tmp"
    local_temp.mkdir(exist_ok=True)
    project_document: dict[str, object] = {
        "protocol": "ludoweave.headless-project/1",
        "world_id": "installed-asset-realization",
        "seed": "0000000000000001",
        "platform_profile": "cpython-portable-empty-v1",
        "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
    }
    scene: dict[str, object] = {
        "$schema": "ludoweave.scene/1",
        "scene_id": "installed-asset-realization-scene",
        "entities": [],
        "dependencies": ["asset://data/item.json"],
    }
    sources: dict[str, object] = {
        "$schema": "ludoweave.source-manifest/1",
        "manifest_id": "installed-asset-realization-sources",
        "entries": [{"entry_id": "scene", "kind": "scene", "source": "scene.json"}],
    }
    assets: dict[str, object] = {
        "protocol": "ludoweave.assets/1",
        "assets": [
            {
                "uri": "asset://data/item.json",
                "kind": "json",
                "source": "assets/item.json",
                "settings": {},
                "dependencies": [],
            }
        ],
    }
    with tempfile.TemporaryDirectory(
        prefix="ludoweave-asset-realization-wheel-smoke-",
        dir=local_temp,
    ) as temp_name:
        temp_root = Path(temp_name)
        environment = temp_root / "venv"
        project = temp_root / "project"
        cache = temp_root / "cache"
        (project / "assets").mkdir(parents=True)
        (project / "ludoweave.project.json").write_bytes(_canonical(project_document))
        (project / "scene.json").write_bytes(_canonical(scene))
        (project / "sources.json").write_bytes(_canonical(sources))
        (project / "assets.json").write_bytes(_canonical(assets))
        (project / "assets/item.json").write_bytes(b'{ "value": 1 }')
        _run([uv, "venv", "--python", "3.12", str(environment)], cwd=temp_root)
        python = _python_in(environment)
        _run(
            [uv, "pip", "install", "--python", str(python), "--no-deps", str(wheels[0])],
            cwd=temp_root,
        )
        common = [
            str(project),
            "--manifest",
            "sources.json",
            "--assets",
            "assets.json",
        ]
        locked = _run(
            [str(python), "-I", "-m", "ludoweave", "source", "asset-lock", *common],
            cwd=temp_root,
        )
        (project / "assets.lock.json").write_text(locked.stdout, encoding="utf-8")
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
        (project / "assets.plan.json").write_text(planned.stdout, encoding="utf-8")
        cache_arguments = [
            *common,
            "--lock",
            "assets.lock.json",
            "--plan",
            "assets.plan.json",
            "--cache",
            str(cache),
        ]
        realization_command = [
            str(python),
            "-I",
            "-m",
            "ludoweave",
            "source",
            "asset-realize",
            *cache_arguments,
        ]
        before_project = _files(project)
        miss = cast(
            dict[str, object],
            json.loads(_run(realization_command, cwd=temp_root).stdout),
        )
        absent_after_miss = not cache.exists()
        unchanged_after_miss = _files(project) == before_project
        _run(
            [
                str(python),
                "-I",
                "-m",
                "ludoweave",
                "source",
                "asset-cache",
                *cache_arguments,
            ],
            cwd=temp_root,
        )
        before_project = _files(project)
        before_cache = _files(cache)
        hit = cast(
            dict[str, object],
            json.loads(_run(realization_command, cwd=temp_root).stdout),
        )
        unchanged_after_hit = _files(project) == before_project and _files(cache) == before_cache

    if (
        miss.get("$schema") != "ludoweave.asset-build-realization/1"
        or miss.get("hits") != 0
        or miss.get("decoded") != 1
        or hit.get("hits") != 1
        or hit.get("decoded") != 0
        or not absent_after_miss
        or not unchanged_after_miss
        or not unchanged_after_hit
    ):
        raise RuntimeError(
            "installed asset realization was invalid: "
            f"miss={miss!r}, hit={hit!r}, absent={absent_after_miss!r}, "
            f"unchanged_miss={unchanged_after_miss!r}, "
            f"unchanged_hit={unchanged_after_hit!r}"
        )
    print(
        json.dumps(
            {
                "realization_protocol": hit["$schema"],
                "schema": "ludoweave.asset-realization-wheel-smoke/1",
                "status": "pass",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
