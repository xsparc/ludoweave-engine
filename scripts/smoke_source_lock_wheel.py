"""Install one built wheel and verify source-lock generation and checking."""

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
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode()


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
        raise RuntimeError("uv is required for the isolated source-lock wheel smoke test")
    project_root = Path(__file__).resolve().parents[1]
    local_temp = project_root / ".tmp"
    local_temp.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory(
        prefix="ludoweave-source-lock-wheel-smoke-", dir=local_temp
    ) as temp_name:
        temp_root = Path(temp_name)
        environment = temp_root / "venv"
        project = temp_root / "project"
        project.mkdir()
        (project / "ludoweave.project.json").write_bytes(
            _canonical(
                {
                    "protocol": "ludoweave.headless-project/1",
                    "world_id": "installed-source-lock",
                    "seed": "0000000000000001",
                    "platform_profile": "cpython-portable-empty-v1",
                    "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
                }
            )
        )
        (project / "scene.json").write_bytes(
            _canonical(
                {
                    "$schema": "ludoweave.scene/1",
                    "scene_id": "installed-lock-scene",
                    "entities": [],
                    "dependencies": [],
                }
            )
        )
        (project / "prefab.json").write_bytes(
            _canonical(
                {
                    "$schema": "ludoweave.prefab/1",
                    "prefab_id": "installed-lock-prefab",
                    "entities": [],
                    "dependencies": [],
                }
            )
        )
        (project / "instance.json").write_bytes(
            _canonical(
                {
                    "$schema": "ludoweave.prefab-instance/1",
                    "prefab_id": "installed-lock-prefab",
                    "instance_id": "installed-lock-instance",
                    "overrides": [],
                }
            )
        )
        (project / "sources.json").write_bytes(
            _canonical(
                {
                    "$schema": "ludoweave.source-manifest/1",
                    "manifest_id": "installed-locked-sources",
                    "entries": [
                        {"entry_id": "scene", "kind": "scene", "source": "scene.json"},
                        {
                            "entry_id": "prefab",
                            "kind": "prefab",
                            "source": "prefab.json",
                            "instance": "instance.json",
                        },
                    ],
                }
            )
        )
        _run([uv, "venv", "--python", "3.12", str(environment)], cwd=temp_root)
        python = _python_in(environment)
        _run(
            [uv, "pip", "install", "--python", str(python), "--no-deps", str(wheels[0])],
            cwd=temp_root,
        )
        _run(
            [
                str(python),
                "-I",
                "-c",
                (
                    "import ludoweave.scene as scene; "
                    "names = {'SOURCE_LOCK_PROTOCOL', 'SourceLock', "
                    "'SourceLockEntry', 'SourceLockLimits'}; "
                    "assert names <= set(scene.__all__); "
                    "assert all(scene.__stability__[name] == 'experimental' for name in names)"
                ),
            ],
            cwd=temp_root,
        )
        lock_result = _run(
            [
                str(python),
                "-I",
                "-m",
                "ludoweave",
                "source",
                "lock",
                str(project),
                "--manifest",
                "sources.json",
            ],
            cwd=temp_root,
        )
        (project / "sources.lock.json").write_text(lock_result.stdout, encoding="utf-8")
        verify_result = _run(
            [
                str(python),
                "-I",
                "-m",
                "ludoweave",
                "source",
                "verify",
                str(project),
                "--manifest",
                "sources.json",
                "--lock",
                "sources.lock.json",
            ],
            cwd=temp_root,
        )

    lock = cast(dict[str, object], json.loads(lock_result.stdout))
    verification = cast(dict[str, object], json.loads(verify_result.stdout))
    entries = cast(list[object], lock.get("entries"))
    summary: dict[str, object] = {
        "schema": "ludoweave.source-lock-wheel-smoke/1",
        "status": "pass",
        "lock_protocol": lock.get("$schema"),
        "verify_protocol": verification.get("protocol"),
        "manifest_id": verification.get("manifest_id"),
        "entry_count": verification.get("entry_count"),
        "locked_entries": len(entries),
    }
    expected: dict[str, object] = {
        "schema": "ludoweave.source-lock-wheel-smoke/1",
        "status": "pass",
        "lock_protocol": "ludoweave.source-lock/1",
        "verify_protocol": "ludoweave.cli.source-lock-verify/1",
        "manifest_id": "installed-locked-sources",
        "entry_count": 2,
        "locked_entries": 2,
    }
    if summary != expected:
        raise RuntimeError(f"installed source-lock summary was invalid: {summary!r}")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
