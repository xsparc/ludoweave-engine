"""Installed-shape CLI execution of one exact saved asset build plan."""

from __future__ import annotations

import json
import subprocess
import sys
from hashlib import sha256
from pathlib import Path
from typing import cast

from ludoweave.tools.headless_project import PROJECT_PROTOCOL
from ludoweave.world import canonical_dumps


def _run_module(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "ludoweave", *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def _write_project(root: Path) -> None:
    (root / "ludoweave.project.json").write_bytes(
        canonical_dumps(
            {
                "protocol": PROJECT_PROTOCOL,
                "world_id": "asset-plan-execute-world",
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
                "scene_id": "asset-plan-execute-scene",
                "entities": [],
                "dependencies": ["asset://data/item.json"],
            }
        )
    )
    (root / "sources.json").write_bytes(
        canonical_dumps(
            {
                "$schema": "ludoweave.source-manifest/1",
                "manifest_id": "asset-plan-execute-sources",
                "entries": [{"entry_id": "scene", "kind": "scene", "source": "scene.json"}],
            }
        )
    )
    assets_document: dict[str, object] = {
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
    (root / "assets.json").write_bytes(canonical_dumps(assets_document))
    (root / "assets").mkdir()
    (root / "assets" / "item.json").write_bytes(b'{ "value": 1 }')


def _common(root: Path) -> tuple[str, ...]:
    return (
        str(root),
        "--manifest",
        "sources.json",
        "--assets",
        "assets.json",
    )


def _create_lock_and_plan(root: Path) -> None:
    locked = _run_module("source", "asset-lock", *_common(root))
    assert locked.returncode == 0
    (root / "assets.lock.json").write_text(locked.stdout, encoding="utf-8")
    planned = _run_module(
        "source",
        "asset-plan",
        *_common(root),
        "--lock",
        "assets.lock.json",
    )
    assert planned.returncode == 0
    (root / "assets.plan.json").write_text(planned.stdout, encoding="utf-8")


def _files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _execute(root: Path) -> subprocess.CompletedProcess[str]:
    return _run_module(
        "source",
        "asset-build",
        *_common(root),
        "--lock",
        "assets.lock.json",
        "--plan",
        "assets.plan.json",
    )


def test_asset_build_executes_verified_plan_without_project_or_cache_write(
    tmp_path: Path,
) -> None:
    _write_project(tmp_path)
    _create_lock_and_plan(tmp_path)
    before = _files(tmp_path)

    first = _execute(tmp_path)
    second = _execute(tmp_path)

    assert first.returncode == second.returncode == 0
    assert first.stderr == second.stderr == ""
    assert first.stdout == second.stdout
    report = cast(dict[str, object], json.loads(first.stdout))
    entries = cast(list[dict[str, object]], report["entries"])
    assert report["$schema"] == "ludoweave.asset-build-result/1"
    assert report["loader_protocol"] == "ludoweave.assets/1"
    assert report["source_bytes"] == len(b'{ "value": 1 }')
    assert report["artifact_bytes"] == len(b'{"value":1}')
    assert len(entries) == 1
    assert entries[0]["uri"] == "asset://data/item.json"
    assert entries[0]["kind"] == "json"
    assert entries[0]["artifact_sha256"] == (f"sha256:{sha256(b'{"value":1}').hexdigest()}")
    assert _files(tmp_path) == before
    assert not (tmp_path / "cache").exists()


def test_asset_build_rejects_stale_source_before_success_output(tmp_path: Path) -> None:
    _write_project(tmp_path)
    _create_lock_and_plan(tmp_path)
    (tmp_path / "assets" / "item.json").write_bytes(b'{"value":2}')
    before = _files(tmp_path)

    result = _execute(tmp_path)

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "asset_source_lock.mismatch"
    assert str(tmp_path) not in result.stderr
    assert _files(tmp_path) == before


def test_asset_build_decoder_failure_emits_no_partial_success_or_write(tmp_path: Path) -> None:
    _write_project(tmp_path)
    (tmp_path / "assets" / "item.json").write_bytes(b"not-json")
    _create_lock_and_plan(tmp_path)
    before = _files(tmp_path)

    result = _execute(tmp_path)

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "asset_build.decode_failed"
    assert str(tmp_path) not in result.stderr
    assert _files(tmp_path) == before


def test_asset_build_rejects_invalid_plan_before_source_read(tmp_path: Path) -> None:
    _write_project(tmp_path)
    _create_lock_and_plan(tmp_path)
    (tmp_path / "assets.plan.json").write_bytes(b"not json")
    (tmp_path / "assets" / "item.json").unlink()
    before = _files(tmp_path)

    result = _execute(tmp_path)

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "asset_build_plan.invalid_json"
    assert str(tmp_path) not in result.stderr
    assert _files(tmp_path) == before
