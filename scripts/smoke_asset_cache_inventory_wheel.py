"""Install one wheel and verify bounded whole-cache inventory behavior."""

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
        raise RuntimeError("uv is required for the isolated cache-inventory smoke")

    repository = Path(__file__).resolve().parents[1]
    local_temp = repository / ".tmp"
    local_temp.mkdir(exist_ok=True)
    project_document: dict[str, object] = {
        "protocol": "ludoweave.headless-project/1",
        "world_id": "installed-cache-inventory",
        "seed": "0000000000000001",
        "platform_profile": "cpython-portable-empty-v1",
        "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
    }
    scene: dict[str, object] = {
        "$schema": "ludoweave.scene/1",
        "scene_id": "installed-cache-inventory-scene",
        "entities": [],
        "dependencies": ["asset://data/item.json"],
    }
    sources: dict[str, object] = {
        "$schema": "ludoweave.source-manifest/1",
        "manifest_id": "installed-cache-inventory-sources",
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
        prefix="ludoweave-cache-inventory-wheel-smoke-",
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
        _run(
            [
                str(python),
                "-I",
                "-m",
                "ludoweave",
                "source",
                "asset-cache-populate",
                *cache_arguments,
            ],
            cwd=temp_root,
        )
        orphan = b"installed verified orphan"
        orphan_digest = sha256(orphan).hexdigest()
        orphan_path = cache / "cas" / orphan_digest[:2] / orphan_digest
        orphan_path.parent.mkdir(exist_ok=True)
        orphan_path.write_bytes(orphan)
        before_project = _files(project)
        before_cache = _files(cache)
        inventory = cast(
            dict[str, object],
            json.loads(
                _run(
                    [
                        str(python),
                        "-I",
                        "-m",
                        "ludoweave",
                        "source",
                        "asset-cache-inventory",
                        *cache_arguments,
                    ],
                    cwd=temp_root,
                ).stdout
            ),
        )
        unchanged = _files(project) == before_project and _files(cache) == before_cache

    if (
        inventory.get("$schema") != "ludoweave.asset-cache-inventory/1"
        or inventory.get("current_actions") != 1
        or inventory.get("missing_actions") != 0
        or inventory.get("other_actions") != 0
        or inventory.get("cas_blobs") != 2
        or inventory.get("current_blobs") != 1
        or inventory.get("other_blobs") != 1
        or inventory.get("unreferenced_blobs") != 1
        or inventory.get("unreferenced_blob_bytes") != len(orphan)
        or not unchanged
    ):
        raise RuntimeError(
            "installed asset cache inventory was invalid: "
            f"report={inventory!r}, unchanged={unchanged!r}"
        )
    print(
        json.dumps(
            {
                "schema": "ludoweave.asset-cache-inventory-wheel-smoke/1",
                "status": "pass",
                "inventory_protocol": inventory["$schema"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
