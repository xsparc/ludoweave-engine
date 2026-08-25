"""Read-only asset-source lock generation and verification through the CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from hashlib import sha256
from pathlib import Path
from typing import cast

from ludoweave.assets import AssetManifest, AssetSourceLock
from ludoweave.scene import SourceLock
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
                "world_id": "asset-lock-world",
                "seed": "0000000000000001",
                "platform_profile": "cpython-portable-empty-v1",
                "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
            }
        )
    )


def _scene_bytes(*, dependencies: list[str] | None = None) -> bytes:
    return canonical_dumps(
        {
            "$schema": "ludoweave.scene/1",
            "scene_id": "locked-assets-scene",
            "entities": [],
            "dependencies": (
                ["asset://materials/player.json"] if dependencies is None else dependencies
            ),
        }
    )


def _source_manifest_bytes() -> bytes:
    return canonical_dumps(
        {
            "$schema": "ludoweave.source-manifest/1",
            "manifest_id": "locked-asset-sources",
            "entries": [{"entry_id": "scene", "kind": "scene", "source": "scene.json"}],
        }
    )


def _asset_manifest_bytes(*, missing: bool = False, empty: bool = False) -> bytes:
    assets: list[dict[str, object]]
    if empty:
        assets = []
    else:
        assets = [
            {
                "uri": "asset://materials/player.json",
                "kind": "json",
                "source": "assets/missing.json" if missing else "assets/material.json",
                "settings": {},
                "dependencies": ["asset://textures/player.png"],
            },
            {
                "uri": "asset://textures/player.png",
                "kind": "png",
                "source": "assets/player.png",
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
        ]
    return canonical_dumps({"protocol": "ludoweave.assets/1", "assets": assets})


def _write_inputs(root: Path, *, missing: bool = False, empty: bool = False) -> None:
    (root / "scene.json").write_bytes(_scene_bytes(dependencies=[] if empty else None))
    (root / "sources.json").write_bytes(_source_manifest_bytes())
    (root / "assets.json").write_bytes(_asset_manifest_bytes(missing=missing, empty=empty))
    if not empty:
        assets = root / "assets"
        assets.mkdir()
        if not missing:
            (assets / "material.json").write_bytes(b"not decoded as json")
        (assets / "player.png").write_bytes(b"not decoded as png")


def _lock_arguments(root: Path) -> tuple[str, ...]:
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


def test_asset_source_lock_generation_is_canonical_selected_and_read_only(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    _write_inputs(tmp_path)
    before = _files(tmp_path)

    source_lock_result = _run_module("source", "lock", *_lock_arguments(tmp_path)[:-2])
    result = _run_module("source", "asset-lock", *_lock_arguments(tmp_path))

    assert source_lock_result.returncode == 0
    assert result.returncode == 0
    assert result.stderr == ""
    lock = AssetSourceLock.from_json(result.stdout)
    source_lock = SourceLock.from_json(source_lock_result.stdout)
    asset_manifest = AssetManifest.from_json(_asset_manifest_bytes(), project_root=tmp_path)
    assert lock.source_lock_sha256 == (
        f"sha256:{sha256(source_lock.canonical_bytes()).hexdigest()}"
    )
    assert lock.asset_manifest_sha256 == (
        f"sha256:{sha256(asset_manifest.canonical_bytes()).hexdigest()}"
    )
    assert [root.value for root in lock.roots] == ["asset://materials/player.json"]
    assert [entry.as_dict() for entry in lock.entries] == [
        {
            "uri": "asset://materials/player.json",
            "kind": "json",
            "source_sha256": f"sha256:{sha256(b'not decoded as json').hexdigest()}",
            "source_bytes": 19,
        },
        {
            "uri": "asset://textures/player.png",
            "kind": "png",
            "source_sha256": f"sha256:{sha256(b'not decoded as png').hexdigest()}",
            "source_bytes": 18,
        },
    ]
    assert result.stdout.encode() == lock.canonical_bytes() + b"\n"
    material = tmp_path / "assets" / "material.json"
    moved = material.with_suffix(".moved")
    material.rename(moved)
    moved.rename(material)
    assert _files(tmp_path) == before
    assert not (tmp_path / "cache").exists()


def test_asset_source_lock_verification_detects_content_drift_without_disclosure(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    _write_inputs(tmp_path)
    generated = _run_module("source", "asset-lock", *_lock_arguments(tmp_path))
    assert generated.returncode == 0
    (tmp_path / "asset-source.lock.json").write_text(generated.stdout, encoding="utf-8")
    before_verify = _files(tmp_path)

    valid = _run_module(
        "source",
        "asset-verify",
        *_lock_arguments(tmp_path),
        "--lock",
        "asset-source.lock.json",
    )

    assert valid.returncode == 0
    assert valid.stderr == ""
    assert json.loads(valid.stdout) == {
        "protocol": "ludoweave.cli.asset-source-lock-verify/1",
        "status": "valid",
        "lock_protocol": "ludoweave.asset-source-lock/1",
        "root_count": 1,
        "entry_count": 2,
    }
    assert _files(tmp_path) == before_verify

    (tmp_path / "assets" / "material.json").write_bytes(b"changed")
    drift = _run_module(
        "source",
        "asset-verify",
        *_lock_arguments(tmp_path),
        "--lock",
        "asset-source.lock.json",
    )

    assert drift.returncode == 2
    assert drift.stdout == ""
    report = cast(dict[str, object], json.loads(drift.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "asset_source_lock.mismatch"
    assert error["details"] == {
        "field": "source_sha256",
        "uri": "asset://materials/player.json",
    }
    assert "sha256:" not in drift.stderr
    assert str(tmp_path) not in drift.stderr


def test_asset_source_lock_reports_first_missing_source_without_success_bytes(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    _write_inputs(tmp_path, missing=True)
    before = _files(tmp_path)

    result = _run_module("source", "asset-lock", *_lock_arguments(tmp_path))

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "tools.asset_source_unavailable"
    assert error["details"] == {
        "cause_code": "tools.unsafe_path",
        "uri": "asset://materials/player.json",
    }
    assert str(tmp_path) not in result.stderr
    assert _files(tmp_path) == before


def test_asset_source_lock_accepts_empty_resolved_closure(tmp_path: Path) -> None:
    _project(tmp_path)
    _write_inputs(tmp_path, empty=True)
    before = _files(tmp_path)

    result = _run_module("source", "asset-lock", *_lock_arguments(tmp_path))

    assert result.returncode == 0
    lock = AssetSourceLock.from_json(result.stdout)
    assert lock.roots == ()
    assert lock.entries == ()
    assert _files(tmp_path) == before


def test_asset_source_lock_rejects_one_oversized_source_before_read(tmp_path: Path) -> None:
    _project(tmp_path)
    (tmp_path / "scene.json").write_bytes(_scene_bytes(dependencies=["asset://audio/large.bin"]))
    (tmp_path / "sources.json").write_bytes(_source_manifest_bytes())
    oversized_manifest: dict[str, object] = {
        "protocol": "ludoweave.assets/1",
        "assets": [
            {
                "uri": "asset://audio/large.bin",
                "kind": "audio",
                "source": "assets/large.bin",
                "settings": {},
                "dependencies": [],
            }
        ],
    }
    (tmp_path / "assets.json").write_bytes(canonical_dumps(oversized_manifest))
    assets = tmp_path / "assets"
    assets.mkdir()
    with (assets / "large.bin").open("wb") as handle:
        handle.seek(268_435_456)
        handle.write(b"x")

    result = _run_module("source", "asset-lock", *_lock_arguments(tmp_path))

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "tools.asset_source_oversized"
    assert error["details"] == {
        "cause_code": "tools.input_oversized",
        "uri": "asset://audio/large.bin",
    }
    assert str(tmp_path) not in result.stderr
