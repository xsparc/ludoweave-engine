"""Install one wheel and compare two saved cache fingerprints offline."""

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


def _run(
    command: Sequence[str],
    *,
    cwd: Path,
    expected: int = 0,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True)
    if result.returncode != expected:
        raise RuntimeError(
            f"command exited {result.returncode}, expected {expected}: "
            f"{subprocess.list2cmdline(command)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def _python_in(environment: Path) -> Path:
    return environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


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
        raise RuntimeError("uv is required for the isolated record-comparison smoke")

    repository = Path(__file__).resolve().parents[1]
    local_temp = repository / ".tmp"
    local_temp.mkdir(exist_ok=True)
    project_document: dict[str, object] = {
        "protocol": "ludoweave.headless-project/1",
        "world_id": "installed-cache-fingerprint-record-comparison",
        "seed": "0000000000000001",
        "platform_profile": "cpython-portable-empty-v1",
        "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
    }
    scene: dict[str, object] = {
        "$schema": "ludoweave.scene/1",
        "scene_id": "installed-cache-fingerprint-record-comparison-scene",
        "entities": [],
        "dependencies": ["asset://data/item.json"],
    }
    sources: dict[str, object] = {
        "$schema": "ludoweave.source-manifest/1",
        "manifest_id": "installed-cache-fingerprint-record-comparison-sources",
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
        prefix="ludoweave-cache-fingerprint-record-comparison-wheel-smoke-",
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
        common = [str(project), "--manifest", "sources.json", "--assets", "assets.json"]
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
        expected = _run(
            [
                str(python),
                "-I",
                "-m",
                "ludoweave",
                "source",
                "asset-cache-fingerprint",
                *cache_arguments,
            ],
            cwd=temp_root,
        )
        (project / "expected.json").write_bytes(expected.stdout.rstrip("\n").encode("utf-8"))
        orphan = b"installed offline comparison orphan"
        digest = sha256(orphan).hexdigest()
        orphan_path = cache / "cas" / digest[:2] / digest
        orphan_path.parent.mkdir(exist_ok=True)
        orphan_path.write_bytes(orphan)
        current = _run(
            [
                str(python),
                "-I",
                "-m",
                "ludoweave",
                "source",
                "asset-cache-fingerprint",
                *cache_arguments,
            ],
            cwd=temp_root,
        )
        current_record = cast(dict[str, object], json.loads(current.stdout))
        (project / "current.json").write_bytes(current.stdout.rstrip("\n").encode("utf-8"))
        compare_prefix = [
            str(python),
            "-I",
            "-m",
            "ludoweave",
            "source",
            "asset-cache-fingerprint-record-compare",
            *common,
            "--lock",
            "assets.lock.json",
            "--plan",
            "assets.plan.json",
            "--expected-fingerprint",
            "expected.json",
        ]
        equal_command = [*compare_prefix, "--current-fingerprint", "expected.json"]
        changed_command = [*compare_prefix, "--current-fingerprint", "current.json"]
        shutil.rmtree(cache)
        before_project = _files(project)
        equal_first = _run(equal_command, cwd=temp_root)
        equal_second = _run(equal_command, cwd=temp_root)
        changed_result = _run(changed_command, cwd=temp_root, expected=1)
        equal = cast(dict[str, object], json.loads(equal_first.stdout))
        changed = cast(dict[str, object], json.loads(changed_result.stdout))
        equal_deltas = cast(dict[str, object], equal.get("deltas"))
        changed_deltas = cast(dict[str, object], changed.get("deltas"))
        unchanged = _files(project) == before_project and not cache.exists()

    if (
        equal.get("$schema") != "ludoweave.asset-cache-fingerprint-comparison/1"
        or equal.get("status") != "equal"
        or equal.get("observation_equal") is not True
        or set(equal_deltas.values()) != {0}
        or equal_first.stdout != equal_second.stdout
        or changed.get("status") != "different"
        or changed.get("observation_equal") is not False
        or changed_deltas.get("unreferenced_blobs") != 1
        or digest in changed_result.stdout
        or str(current_record.get("observation_sha256")) in changed_result.stdout
        or not unchanged
    ):
        raise RuntimeError(
            "installed offline cache fingerprint comparison was invalid: "
            f"equal={equal!r}, changed={changed!r}, unchanged={unchanged!r}"
        )
    print(
        json.dumps(
            {
                "schema": "ludoweave.asset-cache-fingerprint-record-comparison-wheel-smoke/1",
                "status": "pass",
                "comparison_protocol": equal["$schema"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
