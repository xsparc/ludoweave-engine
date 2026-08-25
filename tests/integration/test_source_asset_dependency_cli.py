"""Read-only source-to-asset dependency checking through the installed CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from hashlib import sha256
from pathlib import Path
from typing import cast

from ludoweave.assets import AssetManifest
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
                "world_id": "source-asset-world",
                "seed": "0000000000000001",
                "platform_profile": "cpython-portable-empty-v1",
                "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
            }
        )
    )


def _scene_bytes(*, dependency: str = "asset://materials/player.json") -> bytes:
    return canonical_dumps(
        {
            "$schema": "ludoweave.scene/1",
            "scene_id": "asset-scene",
            "entities": [],
            "dependencies": [dependency],
        }
    )


def _prefab_bytes() -> bytes:
    return canonical_dumps(
        {
            "$schema": "ludoweave.prefab/1",
            "prefab_id": "asset-prefab",
            "entities": [],
            "dependencies": ["asset://audio/theme.json"],
        }
    )


def _instance_bytes() -> bytes:
    return canonical_dumps(
        {
            "$schema": "ludoweave.prefab-instance/1",
            "prefab_id": "asset-prefab",
            "instance_id": "asset-instance",
            "overrides": [],
        }
    )


def _source_manifest_bytes() -> bytes:
    return canonical_dumps(
        {
            "$schema": "ludoweave.source-manifest/1",
            "manifest_id": "asset-sources",
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
    )


def _asset_manifest_bytes() -> bytes:
    value: dict[str, object] = {
        "protocol": "ludoweave.assets/1",
        "assets": [
            {
                "uri": "asset://textures/player.png",
                "kind": "png",
                "source": "assets/player.png",
                "settings": {},
                "dependencies": [],
            },
            {
                "uri": "asset://materials/player.json",
                "kind": "json",
                "source": "assets/material.json",
                "settings": {},
                "dependencies": ["asset://textures/player.png"],
            },
            {
                "uri": "asset://audio/theme.json",
                "kind": "json",
                "source": "assets/theme.json",
                "settings": {},
                "dependencies": [],
            },
            {
                "uri": "asset://unused/item.json",
                "kind": "json",
                "source": "assets/unused.json",
                "settings": {},
                "dependencies": [],
            },
        ],
    }
    return canonical_dumps(value)


def _write_inputs(root: Path, *, scene_dependency: str = "asset://materials/player.json") -> None:
    (root / "scene.json").write_bytes(_scene_bytes(dependency=scene_dependency))
    (root / "prefab.json").write_bytes(_prefab_bytes())
    (root / "instance.json").write_bytes(_instance_bytes())
    (root / "sources.json").write_bytes(_source_manifest_bytes())
    (root / "assets.json").write_bytes(_asset_manifest_bytes())


def _files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_source_assets_emits_canonical_direct_and_resolved_dependencies(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    _write_inputs(tmp_path)
    before = _files(tmp_path)

    result = _run_module(
        "source",
        "assets",
        str(tmp_path),
        "--manifest",
        "sources.json",
        "--assets",
        "assets.json",
    )

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    source_manifest = SourceManifest.from_json(_source_manifest_bytes())
    asset_manifest = AssetManifest.from_json(_asset_manifest_bytes(), project_root=tmp_path)
    assert report == {
        "protocol": "ludoweave.cli.source-asset-check/1",
        "status": "valid",
        "source_manifest_protocol": "ludoweave.source-manifest/1",
        "source_manifest_id": "asset-sources",
        "source_manifest_sha256": (
            f"sha256:{sha256(source_manifest.canonical_bytes()).hexdigest()}"
        ),
        "asset_manifest_protocol": "ludoweave.assets/1",
        "asset_manifest_sha256": f"sha256:{sha256(asset_manifest.canonical_bytes()).hexdigest()}",
        "entries": [
            {
                "entry_id": "a-scene",
                "kind": "scene",
                "direct": ["asset://materials/player.json"],
                "resolved": [
                    "asset://materials/player.json",
                    "asset://textures/player.png",
                ],
            },
            {
                "entry_id": "z-prefab",
                "kind": "prefab",
                "direct": ["asset://audio/theme.json"],
                "resolved": ["asset://audio/theme.json"],
            },
        ],
        "entry_count": 2,
        "direct_asset_count": 2,
        "resolved_asset_count": 3,
    }
    assert result.stdout.encode() == canonical_dumps(report) + b"\n"
    assert not (tmp_path / "assets").exists()
    assert _files(tmp_path) == before


def test_source_assets_rejects_first_missing_direct_dependency_without_mutation(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    _write_inputs(tmp_path, scene_dependency="asset://missing/item.json")
    before = _files(tmp_path)

    result = _run_module(
        "source",
        "assets",
        str(tmp_path),
        "--manifest",
        "sources.json",
        "--assets",
        "assets.json",
    )

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "tools.missing_asset_dependency"
    assert error["details"] == {
        "dependency": "asset://missing/item.json",
        "entry_id": "a-scene",
    }
    assert str(tmp_path) not in result.stderr
    assert _files(tmp_path) == before


def test_source_assets_accepts_empty_declared_and_asset_graphs(tmp_path: Path) -> None:
    _project(tmp_path)
    _write_inputs(tmp_path)
    (tmp_path / "scene.json").write_bytes(
        canonical_dumps(
            {
                "$schema": "ludoweave.scene/1",
                "scene_id": "asset-scene",
                "entities": [],
                "dependencies": [],
            }
        )
    )
    (tmp_path / "prefab.json").write_bytes(
        canonical_dumps(
            {
                "$schema": "ludoweave.prefab/1",
                "prefab_id": "asset-prefab",
                "entities": [],
                "dependencies": [],
            }
        )
    )
    (tmp_path / "assets.json").write_bytes(
        canonical_dumps({"protocol": "ludoweave.assets/1", "assets": []})
    )
    before = _files(tmp_path)

    result = _run_module(
        "source",
        "assets",
        str(tmp_path),
        "--manifest",
        "sources.json",
        "--assets",
        "assets.json",
    )

    assert result.returncode == 0
    report = cast(dict[str, object], json.loads(result.stdout))
    entries = cast(list[dict[str, object]], report["entries"])
    assert [(entry["direct"], entry["resolved"]) for entry in entries] == [
        ([], []),
        ([], []),
    ]
    assert report["direct_asset_count"] == 0
    assert report["resolved_asset_count"] == 0
    assert result.stdout.encode() == canonical_dumps(report) + b"\n"
    assert _files(tmp_path) == before
