"""Explicit source-manifest CLI integration tests."""

from __future__ import annotations

import json
import subprocess
import sys
from hashlib import sha256
from pathlib import Path
from typing import cast

from ludoweave.scene import SourceManifest
from ludoweave.tools.headless_project import PROJECT_PROTOCOL
from ludoweave.world import canonical_dumps


def _run_module(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "ludoweave", *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def _project(root: Path) -> None:
    (root / "ludoweave.project.json").write_bytes(
        canonical_dumps(
            {
                "protocol": PROJECT_PROTOCOL,
                "world_id": "manifest-check-world",
                "seed": "0000000000000001",
                "platform_profile": "cpython-portable-empty-v1",
                "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
            }
        )
    )


def _scene_bytes() -> bytes:
    value: dict[str, object] = {
        "$schema": "ludoweave.scene/1",
        "scene_id": "manifest-scene",
        "entities": [{"local_id": "root", "name": "Root", "parent": None, "components": {}}],
        "dependencies": ["asset://manifest/scene.png"],
    }
    return canonical_dumps(value)


def _prefab_bytes(*, prefab_id: str = "manifest-prefab") -> bytes:
    value: dict[str, object] = {
        "$schema": "ludoweave.prefab/1",
        "prefab_id": prefab_id,
        "entities": [{"local_id": "root", "name": "Root", "parent": None, "components": {}}],
        "dependencies": ["asset://manifest/prefab.png"],
    }
    return canonical_dumps(value)


def _instance_bytes(*, prefab_id: str = "manifest-prefab") -> bytes:
    return canonical_dumps(
        {
            "$schema": "ludoweave.prefab-instance/1",
            "prefab_id": prefab_id,
            "instance_id": "manifest-instance",
            "overrides": [],
        }
    )


def _manifest_bytes() -> bytes:
    value: dict[str, object] = {
        "$schema": "ludoweave.source-manifest/1",
        "manifest_id": "checked-sources",
        "entries": [
            {
                "entry_id": "z-prefab",
                "kind": "prefab",
                "source": "prefab.json",
                "instance": "instance.json",
            },
            {"entry_id": "a-scene", "kind": "scene", "source": "scene.json"},
        ],
    }
    return canonical_dumps(value)


def _files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _write_sources(root: Path, *, instance_prefab_id: str = "manifest-prefab") -> None:
    (root / "scene.json").write_bytes(_scene_bytes())
    (root / "prefab.json").write_bytes(_prefab_bytes())
    (root / "instance.json").write_bytes(_instance_bytes(prefab_id=instance_prefab_id))
    (root / "sources.json").write_bytes(_manifest_bytes())


def test_manifest_check_emits_canonical_aggregate_without_mutation(tmp_path: Path) -> None:
    _project(tmp_path)
    _write_sources(tmp_path)
    before = _files(tmp_path)

    result = _run_module("source", "check", str(tmp_path), "--manifest", "sources.json")

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    manifest = SourceManifest.from_json(_manifest_bytes())
    assert report == {
        "protocol": "ludoweave.cli.source-manifest-check/1",
        "status": "valid",
        "manifest_protocol": "ludoweave.source-manifest/1",
        "manifest_id": "checked-sources",
        "manifest_sha256": f"sha256:{sha256(manifest.canonical_bytes()).hexdigest()}",
        "entries": [
            {
                "entry_id": "a-scene",
                "kind": "scene",
                "source_protocol": "ludoweave.scene/1",
                "source_id": "manifest-scene",
                "source_sha256": f"sha256:{sha256(_scene_bytes()).hexdigest()}",
                "entities": 1,
                "dependencies": 1,
            },
            {
                "entry_id": "z-prefab",
                "kind": "prefab",
                "source_protocol": "ludoweave.prefab/1",
                "instance_protocol": "ludoweave.prefab-instance/1",
                "source_id": "manifest-prefab",
                "instance_id": "manifest-instance",
                "source_sha256": f"sha256:{sha256(_prefab_bytes()).hexdigest()}",
                "instance_sha256": f"sha256:{sha256(_instance_bytes()).hexdigest()}",
                "entities": 1,
                "overrides": 0,
                "dependencies": 1,
            },
        ],
        "entry_count": 2,
        "scenes": 1,
        "prefabs": 1,
        "entities": 2,
        "overrides": 0,
        "dependencies": 2,
    }
    assert result.stdout.encode() == canonical_dumps(report) + b"\n"
    assert _files(tmp_path) == before


def test_manifest_check_rejects_mismatched_prefab_without_path_disclosure(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    _write_sources(tmp_path, instance_prefab_id="other-prefab")
    before = _files(tmp_path)

    result = _run_module("source", "check", str(tmp_path), "--manifest", "sources.json")

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "tools.prefab_source_mismatch"
    assert str(tmp_path) not in result.stderr
    assert _files(tmp_path) == before


def test_manifest_check_rejects_unsafe_manifest_entry_without_path_disclosure(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    manifest = canonical_dumps(
        {
            "$schema": "ludoweave.source-manifest/1",
            "manifest_id": "unsafe-sources",
            "entries": [{"entry_id": "escape", "kind": "scene", "source": "../outside.json"}],
        }
    )
    (tmp_path / "sources.json").write_bytes(manifest)

    result = _run_module("source", "check", str(tmp_path), "--manifest", "sources.json")

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "source_manifest.invalid_path"
    assert "../outside.json" not in result.stderr
    assert str(tmp_path) not in result.stderr


def test_manifest_check_inherits_manifest_file_confinement(tmp_path: Path) -> None:
    _project(tmp_path)
    outside = tmp_path.parent / "outside-manifest.json"
    outside.write_bytes(_manifest_bytes())

    result = _run_module("source", "check", str(tmp_path), "--manifest", "../outside-manifest.json")

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "tools.unsafe_path"
    assert str(outside) not in result.stderr


def test_manifest_check_rejects_instance_argument_as_mixed_mode(tmp_path: Path) -> None:
    _project(tmp_path)
    (tmp_path / "sources.json").write_bytes(_manifest_bytes())

    result = _run_module(
        "source",
        "check",
        str(tmp_path),
        "--manifest",
        "sources.json",
        "--instance",
        "instance.json",
    )

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "tools.invalid_argument"
