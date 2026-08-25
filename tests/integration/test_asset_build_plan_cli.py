"""Read-only verified asset build planning through the CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from hashlib import sha256
from pathlib import Path
from typing import cast

from ludoweave.assets import AssetBuildPlan
from ludoweave.tools.headless_project import PROJECT_PROTOCOL
from ludoweave.world import canonical_dumps


def _run_module(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "ludoweave", *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def _write_project(root: Path, *, empty: bool = False) -> None:
    (root / "ludoweave.project.json").write_bytes(
        canonical_dumps(
            {
                "protocol": PROJECT_PROTOCOL,
                "world_id": "asset-build-plan-world",
                "seed": "0000000000000001",
                "platform_profile": "cpython-portable-empty-v1",
                "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
            }
        )
    )
    (root / "scene.json").write_bytes(
        canonical_dumps(
            {
                "$schema": "ludoweave.scene/1",
                "scene_id": "planned-assets-scene",
                "entities": [],
                "dependencies": [] if empty else ["asset://materials/player.json"],
            }
        )
    )
    (root / "sources.json").write_bytes(
        canonical_dumps(
            {
                "$schema": "ludoweave.source-manifest/1",
                "manifest_id": "planned-asset-sources",
                "entries": [{"entry_id": "scene", "kind": "scene", "source": "scene.json"}],
            }
        )
    )
    assets: list[dict[str, object]] = []
    if not empty:
        assets = [
            {
                "uri": "asset://materials/player.json",
                "kind": "json",
                "source": "assets/material.json",
                "settings": {"mode": "strict"},
                "dependencies": ["asset://textures/player.png"],
            },
            {
                "uri": "asset://textures/player.png",
                "kind": "png",
                "source": "assets/player.png",
                "settings": {},
                "dependencies": [],
            },
        ]
    (root / "assets.json").write_bytes(
        canonical_dumps({"protocol": "ludoweave.assets/1", "assets": assets})
    )
    if not empty:
        source_root = root / "assets"
        source_root.mkdir()
        (source_root / "material.json").write_bytes(b"opaque json input")
        (source_root / "player.png").write_bytes(b"opaque png input")


def _common(root: Path) -> tuple[str, ...]:
    return (
        str(root),
        "--manifest",
        "sources.json",
        "--assets",
        "assets.json",
    )


def _files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_asset_plan_verifies_inputs_and_emits_dependency_first_plan_read_only(
    tmp_path: Path,
) -> None:
    _write_project(tmp_path)
    locked = _run_module("source", "asset-lock", *_common(tmp_path))
    assert locked.returncode == 0
    (tmp_path / "assets.lock.json").write_text(locked.stdout, encoding="utf-8")
    before = _files(tmp_path)

    result = _run_module(
        "source",
        "asset-plan",
        *_common(tmp_path),
        "--lock",
        "assets.lock.json",
    )

    assert result.returncode == 0
    assert result.stderr == ""
    plan = AssetBuildPlan.from_json(result.stdout)
    assert [entry.uri.value for entry in plan.entries] == [
        "asset://textures/player.png",
        "asset://materials/player.json",
    ]
    assert plan.entries[-1].dependencies[0].value == "asset://textures/player.png"
    assert all(entry.cache_key.startswith("sha256:") for entry in plan.entries)
    assert result.stdout.encode() == plan.canonical_bytes() + b"\n"
    assert _files(tmp_path) == before
    assert not (tmp_path / "cache").exists()


def test_asset_plan_fails_changed_source_before_any_success_bytes(tmp_path: Path) -> None:
    _write_project(tmp_path)
    locked = _run_module("source", "asset-lock", *_common(tmp_path))
    assert locked.returncode == 0
    (tmp_path / "assets.lock.json").write_text(locked.stdout, encoding="utf-8")
    (tmp_path / "assets" / "material.json").write_bytes(b"changed")
    before = _files(tmp_path)

    result = _run_module(
        "source",
        "asset-plan",
        *_common(tmp_path),
        "--lock",
        "assets.lock.json",
    )

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "asset_source_lock.mismatch"
    assert error["details"] == {
        "field": "source_sha256",
        "uri": "asset://materials/player.json",
    }
    assert str(tmp_path) not in result.stderr
    assert _files(tmp_path) == before


def test_asset_plan_accepts_empty_verified_closure(tmp_path: Path) -> None:
    _write_project(tmp_path, empty=True)
    locked = _run_module("source", "asset-lock", *_common(tmp_path))
    assert locked.returncode == 0
    (tmp_path / "assets.lock.json").write_text(locked.stdout, encoding="utf-8")

    result = _run_module(
        "source",
        "asset-plan",
        *_common(tmp_path),
        "--lock",
        "assets.lock.json",
    )

    assert result.returncode == 0
    plan = AssetBuildPlan.from_json(result.stdout)
    assert plan.roots == ()
    assert plan.entries == ()
