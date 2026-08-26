"""Install one wheel and execute a verified asset plan without cache or project writes."""

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
        raise RuntimeError("uv is required for the isolated asset-plan execution smoke")

    project_root = Path(__file__).resolve().parents[1]
    local_temp = project_root / ".tmp"
    local_temp.mkdir(exist_ok=True)
    project: dict[str, object] = {
        "protocol": "ludoweave.headless-project/1",
        "world_id": "installed-asset-plan-execution",
        "seed": "0000000000000001",
        "platform_profile": "cpython-portable-empty-v1",
        "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
    }
    scene: dict[str, object] = {
        "$schema": "ludoweave.scene/1",
        "scene_id": "installed-asset-plan-execution-scene",
        "entities": [],
        "dependencies": ["asset://data/item.json"],
    }
    sources: dict[str, object] = {
        "$schema": "ludoweave.source-manifest/1",
        "manifest_id": "installed-asset-plan-execution-sources",
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
        prefix="ludoweave-asset-plan-execution-wheel-smoke-",
        dir=local_temp,
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
        source = b'{ "value": 1 }'
        artifact = b'{"value":1}'
        (source_directory / "item.json").write_bytes(source)
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
        (checked_project / "assets.lock.json").write_text(locked.stdout, encoding="utf-8")
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
        (checked_project / "assets.plan.json").write_text(planned.stdout, encoding="utf-8")
        before = _files(checked_project)
        executed = _run(
            [
                str(python),
                "-I",
                "-m",
                "ludoweave",
                "source",
                "asset-build",
                *common,
                "--lock",
                "assets.lock.json",
                "--plan",
                "assets.plan.json",
            ],
            cwd=temp_root,
        )
        unchanged = _files(checked_project) == before
        cache_absent = not (checked_project / "cache").exists()

    report = cast(dict[str, object], json.loads(executed.stdout))
    entries = cast(list[dict[str, object]], report.get("entries"))
    if (
        report.get("$schema") != "ludoweave.asset-build-result/1"
        or report.get("loader_protocol") != "ludoweave.assets/1"
        or report.get("source_bytes") != len(source)
        or report.get("artifact_bytes") != len(artifact)
        or len(entries) != 1
        or entries[0].get("uri") != "asset://data/item.json"
        or entries[0].get("artifact_sha256") != f"sha256:{sha256(artifact).hexdigest()}"
        or not unchanged
        or not cache_absent
    ):
        raise RuntimeError(
            "installed asset plan execution was invalid: "
            f"report={report!r}, unchanged={unchanged!r}, cache_absent={cache_absent!r}"
        )
    print(
        json.dumps(
            {
                "entries": len(entries),
                "result_protocol": report["$schema"],
                "schema": "ludoweave.asset-plan-execution-wheel-smoke/1",
                "status": "pass",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
