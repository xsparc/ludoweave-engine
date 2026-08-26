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


def _check(project: Path, cache: Path) -> subprocess.CompletedProcess[str]:
    return _run(
        "source",
        "asset-cache-check",
        *_common(project),
        "--lock",
        "assets.lock.json",
        "--plan",
        "assets.plan.json",
        "--cache",
        str(cache),
    )


def _realize(project: Path, cache: Path) -> subprocess.CompletedProcess[str]:
    return _run(
        "source",
        "asset-realize",
        *_common(project),
        "--lock",
        "assets.lock.json",
        "--plan",
        "assets.plan.json",
        "--cache",
        str(cache),
    )


def _populate(project: Path, cache: Path) -> subprocess.CompletedProcess[str]:
    return _run(
        "source",
        "asset-cache-populate",
        *_common(project),
        "--lock",
        "assets.lock.json",
        "--plan",
        "assets.plan.json",
        "--cache",
        str(cache),
    )


def _verify_population(
    project: Path,
    cache: Path,
    *,
    population: str = "population.json",
) -> subprocess.CompletedProcess[str]:
    return _run(
        "source",
        "asset-cache-population-verify",
        *_common(project),
        "--lock",
        "assets.lock.json",
        "--plan",
        "assets.plan.json",
        "--population",
        population,
        "--cache",
        str(cache),
    )


def _inventory(project: Path, cache: Path) -> subprocess.CompletedProcess[str]:
    return _run(
        "source",
        "asset-cache-inventory",
        *_common(project),
        "--lock",
        "assets.lock.json",
        "--plan",
        "assets.plan.json",
        "--cache",
        str(cache),
    )


def _fingerprint(project: Path, cache: Path) -> subprocess.CompletedProcess[str]:
    return _run(
        "source",
        "asset-cache-fingerprint",
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


def test_asset_cache_check_reports_miss_without_creating_cache(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "absent-cache"
    _write_project(project)
    _prepare(project)
    before = _files(project)

    result = _check(project, cache)

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["$schema"] == "ludoweave.asset-cache-lookup/1"
    assert report["hits"] == 0
    assert report["misses"] == 1
    assert _files(project) == before
    assert not cache.exists()


def test_asset_realize_decodes_miss_without_creating_cache_or_writing_project(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "absent-cache"
    _write_project(project)
    _prepare(project)
    before = _files(project)

    result = _realize(project, cache)

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["$schema"] == "ludoweave.asset-build-realization/1"
    assert report["hits"] == 0
    assert report["decoded"] == 1
    assert _files(project) == before
    assert not cache.exists()


def test_asset_realize_reuses_hit_without_writing_project_or_cache(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _publish(project, cache).returncode == 0
    before_project = _files(project)
    before_cache = _files(cache)

    result = _realize(project, cache)

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["hits"] == 1
    assert report["decoded"] == 0
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_realize_rejects_corrupt_hit_without_success_or_mutation(tmp_path: Path) -> None:
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

    result = _realize(project, cache)

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] == "asset_cache.corrupt_entry"
    assert str(project) not in result.stderr
    assert str(cache) not in result.stderr
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_populate_decodes_then_reuses_without_project_write(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    before_project = _files(project)

    first = _populate(project, cache)
    after_first = _files(cache)
    second = _populate(project, cache)

    assert first.returncode == second.returncode == 0
    assert first.stderr == second.stderr == ""
    first_report = cast(dict[str, object], json.loads(first.stdout))
    second_report = cast(dict[str, object], json.loads(second.stdout))
    assert first_report["$schema"] == "ludoweave.asset-cache-population/1"
    assert (first_report["hits"], first_report["decoded"]) == (0, 1)
    assert (first_report["published"], first_report["reused"]) == (1, 0)
    assert (second_report["hits"], second_report["decoded"]) == (1, 0)
    assert (second_report["published"], second_report["reused"]) == (0, 1)
    assert _files(project) == before_project
    assert _files(cache) == after_first


def test_asset_cache_populate_rejects_stale_source_before_cache_creation(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    (project / "assets/item.json").write_bytes(b'{"value":2}')

    result = _populate(project, cache)

    assert result.returncode == 2
    assert result.stdout == ""
    assert str(project) not in result.stderr
    assert str(cache) not in result.stderr
    assert not cache.exists()


def test_asset_cache_populate_rejects_corruption_without_success_or_repair(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    metadata = next(cache.rglob("entry.json"))
    metadata.write_bytes(b"{}")
    before_project = _files(project)
    before_cache = _files(cache)

    result = _populate(project, cache)

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] == "asset_cache.corrupt_entry"
    assert str(project) not in result.stderr
    assert str(cache) not in result.stderr
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_population_verify_reads_saved_report_and_current_cache(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    population = _populate(project, cache)
    assert population.returncode == 0
    (project / "population.json").write_text(population.stdout, encoding="utf-8")
    before_project = _files(project)
    before_cache = _files(cache)

    result = _verify_population(project, cache)

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["$schema"] == "ludoweave.asset-cache-population-verification/1"
    assert report["population_protocol"] == "ludoweave.asset-cache-population/1"
    assert report["status"] == "valid"
    assert report["entry_count"] == 1
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_population_verify_reports_missing_action_without_creation(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    populated = tmp_path / "populated"
    absent = tmp_path / "absent"
    _write_project(project)
    _prepare(project)
    population = _populate(project, populated)
    assert population.returncode == 0
    (project / "population.json").write_text(population.stdout, encoding="utf-8")

    result = _verify_population(project, absent)

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] == "asset_cache.population_miss"
    assert str(project) not in result.stderr
    assert str(absent) not in result.stderr
    assert not absent.exists()


def test_asset_cache_population_verify_rejects_saved_artifact_mismatch_read_only(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    population = _populate(project, cache)
    assert population.returncode == 0
    document = cast(dict[str, object], json.loads(population.stdout))
    entries = cast(list[dict[str, object]], document["entries"])
    entries[0]["artifact_sha256"] = f"sha256:{'0' * 64}"
    (project / "population.json").write_bytes(canonical_dumps(document))
    before_project = _files(project)
    before_cache = _files(cache)

    result = _verify_population(project, cache)

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] == "asset_cache.population_mismatch"
    assert str(project) not in result.stderr
    assert str(cache) not in result.stderr
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_inventory_reports_absent_cache_without_creation(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "absent"
    _write_project(project)
    _prepare(project)
    before_project = _files(project)

    result = _inventory(project, cache)

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["$schema"] == "ludoweave.asset-cache-inventory/1"
    assert report["current_actions"] == 0
    assert report["missing_actions"] == 1
    assert report["other_actions"] == 0
    assert report["cas_blobs"] == 0
    assert not cache.exists()
    assert _files(project) == before_project


def test_asset_cache_inventory_verifies_populated_cache_read_only(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    populated = _populate(project, cache)
    assert populated.returncode == 0
    before_project = _files(project)
    before_cache = _files(cache)

    result = _inventory(project, cache)

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["current_actions"] == 1
    assert report["missing_actions"] == 0
    assert report["other_actions"] == 0
    assert report["cas_blobs"] == 1
    assert report["current_blobs"] == 1
    assert report["unreferenced_blobs"] == 0
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_inventory_rejects_corrupt_orphan_content_silently(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    populated = _populate(project, cache)
    assert populated.returncode == 0
    claimed = sha256(b"claimed").hexdigest()
    orphan = cache / "cas" / claimed[:2] / claimed
    orphan.parent.mkdir(exist_ok=True)
    orphan.write_bytes(b"different")
    before_project = _files(project)
    before_cache = _files(cache)

    result = _inventory(project, cache)

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] == "asset_cache.corrupt_inventory"
    assert str(project) not in result.stderr
    assert str(cache) not in result.stderr
    assert claimed not in result.stderr
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_fingerprint_reports_absent_cache_without_creation(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "absent"
    _write_project(project)
    _prepare(project)
    before_project = _files(project)

    result = _fingerprint(project, cache)

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    inventory = cast(dict[str, object], report["inventory"])
    assert report["$schema"] == "ludoweave.asset-cache-fingerprint/1"
    assert str(report["observation_sha256"]).startswith("sha256:")
    assert inventory["$schema"] == "ludoweave.asset-cache-inventory/1"
    assert inventory["current_actions"] == 0
    assert inventory["missing_actions"] == 1
    assert not cache.exists()
    assert _files(project) == before_project


def test_asset_cache_fingerprint_is_stable_and_read_only(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    before_project = _files(project)
    before_cache = _files(cache)

    first = _fingerprint(project, cache)
    second = _fingerprint(project, cache)

    assert first.returncode == second.returncode == 0
    assert first.stderr == second.stderr == ""
    assert first.stdout == second.stdout
    report = cast(dict[str, object], json.loads(first.stdout))
    inventory = cast(dict[str, object], report["inventory"])
    assert inventory["current_actions"] == 1
    assert inventory["missing_actions"] == 0
    assert inventory["cas_blobs"] == 1
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_fingerprint_rejects_corrupt_orphan_content_silently(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    claimed = sha256(b"claimed").hexdigest()
    orphan = cache / "cas" / claimed[:2] / claimed
    orphan.parent.mkdir(exist_ok=True)
    orphan.write_bytes(b"different")
    before_project = _files(project)
    before_cache = _files(cache)

    result = _fingerprint(project, cache)

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] == "asset_cache.corrupt_inventory"
    assert str(project) not in result.stderr
    assert str(cache) not in result.stderr
    assert claimed not in result.stderr
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_check_verifies_hit_without_writing(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _publish(project, cache).returncode == 0
    before_project = _files(project)
    before_cache = _files(cache)

    result = _check(project, cache)

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["hits"] == 1
    assert report["misses"] == 0
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_check_rejects_corruption_without_mutation(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _publish(project, cache).returncode == 0
    metadata = next(cache.rglob("entry.json"))
    metadata.write_bytes(b'{"duplicate":1,"duplicate":1}')
    before_project = _files(project)
    before_cache = _files(cache)

    result = _check(project, cache)

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] == "asset_cache.corrupt_entry"
    assert str(project) not in result.stderr
    assert str(cache) not in result.stderr
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_check_revalidates_sources_before_cache_access(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _publish(project, cache).returncode == 0
    before_cache = _files(cache)
    (project / "assets/item.json").write_bytes(b'{"value":2}')

    result = _check(project, cache)

    assert result.returncode == 2
    assert result.stdout == ""
    assert _files(cache) == before_cache
