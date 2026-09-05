"""Install one wheel and verify saved cache-fingerprint comparison evidence offline."""

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
        allow_nan=False,
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
        raise RuntimeError("uv is required for the isolated comparison-verification smoke")

    repository = Path(__file__).resolve().parents[1]
    local_temp = repository / ".tmp"
    local_temp.mkdir(exist_ok=True)
    project_document: dict[str, object] = {
        "protocol": "ludoweave.headless-project/1",
        "world_id": "installed-cache-fingerprint-comparison-verification",
        "seed": "0000000000000001",
        "platform_profile": "cpython-portable-empty-v1",
        "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
    }
    scene: dict[str, object] = {
        "$schema": "ludoweave.scene/1",
        "scene_id": "installed-cache-fingerprint-comparison-verification-scene",
        "entities": [],
        "dependencies": ["asset://data/item.json"],
    }
    sources: dict[str, object] = {
        "$schema": "ludoweave.source-manifest/1",
        "manifest_id": "installed-cache-fingerprint-comparison-verification-sources",
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
        prefix="ludoweave-cache-fingerprint-comparison-verification-wheel-smoke-",
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
        command_prefix = [str(python), "-I", "-m", "ludoweave", "source"]
        locked = _run([*command_prefix, "asset-lock", *common], cwd=temp_root)
        (project / "assets.lock.json").write_text(locked.stdout, encoding="utf-8")
        planned = _run(
            [
                *command_prefix,
                "asset-plan",
                *common,
                "--lock",
                "assets.lock.json",
            ],
            cwd=temp_root,
        )
        (project / "assets.plan.json").write_text(planned.stdout, encoding="utf-8")
        saved_inputs = [
            *common,
            "--lock",
            "assets.lock.json",
            "--plan",
            "assets.plan.json",
        ]
        cache_arguments = [*saved_inputs, "--cache", str(cache)]
        _run([*command_prefix, "asset-cache-populate", *cache_arguments], cwd=temp_root)
        expected = _run(
            [*command_prefix, "asset-cache-fingerprint", *cache_arguments],
            cwd=temp_root,
        )
        (project / "expected.json").write_bytes(expected.stdout.rstrip("\n").encode("utf-8"))
        orphan = b"installed comparison verification orphan"
        digest = sha256(orphan).hexdigest()
        orphan_path = cache / "cas" / digest[:2] / digest
        orphan_path.parent.mkdir(exist_ok=True)
        orphan_path.write_bytes(orphan)
        current = _run(
            [*command_prefix, "asset-cache-fingerprint", *cache_arguments],
            cwd=temp_root,
        )
        current_record = cast(dict[str, object], json.loads(current.stdout))
        (project / "current.json").write_bytes(current.stdout.rstrip("\n").encode("utf-8"))
        record_arguments = [
            *saved_inputs,
            "--expected-fingerprint",
            "expected.json",
            "--current-fingerprint",
            "current.json",
        ]
        comparison_result = _run(
            [
                *command_prefix,
                "asset-cache-fingerprint-record-compare",
                *record_arguments,
            ],
            cwd=temp_root,
            expected=1,
        )
        comparison_bytes = comparison_result.stdout.rstrip("\n").encode("utf-8")
        comparison = cast(dict[str, object], json.loads(comparison_result.stdout))
        (project / "comparison.json").write_bytes(comparison_bytes)
        verify_command = [
            *command_prefix,
            "asset-cache-fingerprint-comparison-verify",
            *record_arguments,
            "--comparison",
            "comparison.json",
        ]
        shutil.rmtree(cache)
        before_project = _files(project)
        first = _run(verify_command, cwd=temp_root)
        second = _run(verify_command, cwd=temp_root)
        verification = cast(dict[str, object], json.loads(first.stdout))
        tampered = dict(comparison)
        tampered_deltas = dict(cast(dict[str, object], comparison["deltas"]))
        tampered_deltas["cas_blobs"] = int(cast(int, tampered_deltas["cas_blobs"])) + 1
        tampered["deltas"] = tampered_deltas
        (project / "comparison.json").write_bytes(_canonical(tampered))
        rejected = _run(verify_command, cwd=temp_root, expected=2)
        error = cast(
            dict[str, object], cast(dict[str, object], json.loads(rejected.stderr))["error"]
        )
        unchanged = _files(project) == {**before_project, "comparison.json": _canonical(tampered)}

    if (
        verification.get("$schema") != "ludoweave.asset-cache-fingerprint-comparison-verification/1"
        or verification.get("status") != "valid"
        or verification.get("comparison_status") != "different"
        or verification.get("comparison_sha256") != f"sha256:{sha256(comparison_bytes).hexdigest()}"
        or first.stdout != second.stdout
        or error.get("code") != "asset_cache.fingerprint_comparison_mismatch"
        or digest in first.stdout
        or str(current_record.get("observation_sha256")) in first.stdout
        or str(project) in first.stdout
        or not unchanged
        or cache.exists()
    ):
        raise RuntimeError(
            "installed cache fingerprint comparison verification was invalid: "
            f"verification={verification!r}, error={error!r}, unchanged={unchanged!r}"
        )
    print(
        json.dumps(
            {
                "schema": (
                    "ludoweave.asset-cache-fingerprint-comparison-verification-wheel-smoke/1"
                ),
                "status": "pass",
                "verification_protocol": verification["$schema"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
