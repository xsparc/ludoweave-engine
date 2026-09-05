"""Install one wheel and verify one saved unreferenced preview offline."""

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
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _files(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
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
        raise RuntimeError("uv is required for the isolated saved-preview verification smoke")

    repository = Path(__file__).resolve().parents[1]
    local_temp = repository / ".tmp"
    local_temp.mkdir(exist_ok=True)
    project_document: dict[str, object] = {
        "protocol": "ludoweave.headless-project/1",
        "world_id": "installed-unreferenced-preview-verification",
        "seed": "0000000000000001",
        "platform_profile": "cpython-portable-empty-v1",
        "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
    }
    scene: dict[str, object] = {
        "$schema": "ludoweave.scene/1",
        "scene_id": "installed-unreferenced-preview-verification-scene",
        "entities": [],
        "dependencies": ["asset://data/item.json"],
    }
    sources: dict[str, object] = {
        "$schema": "ludoweave.source-manifest/1",
        "manifest_id": "installed-unreferenced-preview-verification-sources",
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
        prefix="ludoweave-unreferenced-preview-verification-wheel-smoke-",
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
        prefix = [str(python), "-I", "-m", "ludoweave", "source"]
        common = [str(project), "--manifest", "sources.json", "--assets", "assets.json"]
        locked = _run([*prefix, "asset-lock", *common], cwd=temp_root)
        (project / "assets.lock.json").write_text(locked.stdout, encoding="utf-8")
        planned = _run(
            [*prefix, "asset-plan", *common, "--lock", "assets.lock.json"],
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
        _run([*prefix, "asset-cache-populate", *cache_arguments], cwd=temp_root)
        orphan = b"installed saved-preview verification orphan"
        orphan_digest = sha256(orphan).hexdigest()
        orphan_path = cache / "cas" / orphan_digest[:2] / orphan_digest
        orphan_path.parent.mkdir(exist_ok=True)
        orphan_path.write_bytes(orphan)
        fingerprint = _run([*prefix, "asset-cache-fingerprint", *cache_arguments], cwd=temp_root)
        (project / "fingerprint.json").write_text(
            fingerprint.stdout.rstrip("\n"),
            encoding="utf-8",
        )
        shutil.rmtree(cache)
        record_arguments = [
            *common,
            "--lock",
            "assets.lock.json",
            "--plan",
            "assets.plan.json",
            "--fingerprint",
            "fingerprint.json",
        ]
        preview = _run(
            [*prefix, "asset-cache-fingerprint-record-preview", *record_arguments],
            cwd=temp_root,
        )
        preview_bytes = preview.stdout.rstrip("\n").encode("utf-8")
        (project / "preview.json").write_bytes(preview_bytes)
        before_project = _files(project)
        command = [
            *prefix,
            "asset-cache-unreferenced-preview-verify",
            *record_arguments,
            "--preview",
            "preview.json",
        ]
        first = _run(command, cwd=temp_root)
        second = _run(command, cwd=temp_root)
        report = cast(dict[str, object], json.loads(first.stdout))
        unchanged = _files(project) == before_project
        cache_absent = not cache.exists()

    if (
        first.stdout != second.stdout
        or report.get("$schema") != "ludoweave.asset-cache-unreferenced-preview-verification/1"
        or report.get("status") != "valid"
        or report.get("fingerprint_protocol") != "ludoweave.asset-cache-fingerprint/1"
        or report.get("preview_protocol") != "ludoweave.asset-cache-unreferenced-preview/1"
        or report.get("preview_sha256") != f"sha256:{sha256(preview_bytes).hexdigest()}"
        or orphan_digest in first.stdout
        or str(project) in first.stdout
        or str(cache) in first.stdout
        or not unchanged
        or not cache_absent
    ):
        raise RuntimeError(
            "installed saved-preview verification was invalid: "
            f"report={report!r}, unchanged={unchanged!r}, cache_absent={cache_absent!r}"
        )
    print(
        json.dumps(
            {
                "schema": "ludoweave.asset-cache-unreferenced-preview-verification-wheel-smoke/1",
                "status": "pass",
                "verification_protocol": report["$schema"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
