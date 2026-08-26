"""CLI composition for verified local asset cache publication."""

from __future__ import annotations

import json
import subprocess
import sys
from hashlib import sha256
from pathlib import Path
from typing import cast

from ludoweave.tools.headless_project import PROJECT_PROTOCOL
from ludoweave.world import canonical_dumps


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
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
                "world_id": "asset-cache-world",
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
                "scene_id": "asset-cache-scene",
                "entities": [],
                "dependencies": ["asset://data/item.json"],
            }
        )
    )
    (root / "sources.json").write_bytes(
        canonical_dumps(
            {
                "$schema": "ludoweave.source-manifest/1",
                "manifest_id": "asset-cache-sources",
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
    (root / "assets/item.json").write_bytes(b'{ "value": 1 }')


def _common(project: Path) -> tuple[str, ...]:
    return (
        str(project),
        "--manifest",
        "sources.json",
        "--assets",
        "assets.json",
    )


def _prepare(project: Path) -> None:
    lock = _run("source", "asset-lock", *_common(project))
    assert lock.returncode == 0
    (project / "assets.lock.json").write_text(lock.stdout, encoding="utf-8")
    plan = _run("source", "asset-plan", *_common(project), "--lock", "assets.lock.json")
    assert plan.returncode == 0
    (project / "assets.plan.json").write_text(plan.stdout, encoding="utf-8")


def _publish(project: Path, cache: Path) -> subprocess.CompletedProcess[str]:
    return _run(
        "source",
        "asset-cache",
        *_common(project),
        "--lock",
        "assets.lock.json",
        "--plan",
        "assets.plan.json",
        "--cache",
        str(cache),
    )


def _files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_asset_cache_publishes_then_reuses_without_project_write(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    before = _files(project)

    first = _publish(project, cache)
    second = _publish(project, cache)

    assert first.returncode == second.returncode == 0
    assert first.stderr == second.stderr == ""
    first_report = cast(dict[str, object], json.loads(first.stdout))
    second_report = cast(dict[str, object], json.loads(second.stdout))
    assert first_report["$schema"] == "ludoweave.asset-cache-publish/1"
    assert first_report["published"] == 1
    assert first_report["reused"] == 0
    assert second_report["published"] == 0
    assert second_report["reused"] == 1
    assert _files(project) == before
    assert len(list(cache.rglob("entry.json"))) == 1
    assert len([path for path in (cache / "cas").rglob("*") if path.is_file()]) == 1


def test_asset_cache_rejects_corruption_without_repair_or_success(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _publish(project, cache).returncode == 0
    payload = next(path for path in (cache / "cas").rglob("*") if path.is_file())
    payload.write_bytes(b"corrupt")
    before_project = _files(project)
    before_cache = _files(cache)

    result = _publish(project, cache)

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] == "asset_cache.corrupt_entry"
    assert str(project) not in result.stderr
    assert str(cache) not in result.stderr
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_rejects_project_overlap_before_cache_write(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    _write_project(project)
    _prepare(project)
    before = _files(project)

    result = _publish(project, project / "cache")

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] == "asset_cache.invalid_root"
    assert _files(project) == before
    assert not (project / "cache").exists()


def test_asset_cache_rejects_stale_source_before_creating_cache(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    (project / "assets/item.json").write_bytes(b'{"value":2}')

    result = _publish(project, cache)

    assert result.returncode == 2
    assert result.stdout == ""
    assert not cache.exists()
