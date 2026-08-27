"""CLI composition for verified local asset cache publication."""

from __future__ import annotations

import json
import shutil
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


def _preview_unreferenced(project: Path, cache: Path) -> subprocess.CompletedProcess[str]:
    return _run(
        "source",
        "asset-cache-unreferenced-preview",
        *_common(project),
        "--lock",
        "assets.lock.json",
        "--plan",
        "assets.plan.json",
        "--cache",
        str(cache),
    )


def _preview_unreferenced_record(
    project: Path,
    *,
    fingerprint: str = "fingerprint.json",
) -> subprocess.CompletedProcess[str]:
    return _run(
        "source",
        "asset-cache-fingerprint-record-preview",
        *_common(project),
        "--lock",
        "assets.lock.json",
        "--plan",
        "assets.plan.json",
        "--fingerprint",
        fingerprint,
    )


def _verify_fingerprint(
    project: Path,
    cache: Path,
    *,
    fingerprint: str = "fingerprint.json",
) -> subprocess.CompletedProcess[str]:
    return _run(
        "source",
        "asset-cache-fingerprint-verify",
        *_common(project),
        "--lock",
        "assets.lock.json",
        "--plan",
        "assets.plan.json",
        "--fingerprint",
        fingerprint,
        "--cache",
        str(cache),
    )


def _compare_fingerprint(
    project: Path,
    cache: Path,
    *,
    fingerprint: str = "fingerprint.json",
) -> subprocess.CompletedProcess[str]:
    return _run(
        "source",
        "asset-cache-fingerprint-compare",
        *_common(project),
        "--lock",
        "assets.lock.json",
        "--plan",
        "assets.plan.json",
        "--fingerprint",
        fingerprint,
        "--cache",
        str(cache),
    )


def _compare_fingerprint_records(
    project: Path,
    *,
    expected: str = "expected-fingerprint.json",
    current: str = "current-fingerprint.json",
) -> subprocess.CompletedProcess[str]:
    return _run(
        "source",
        "asset-cache-fingerprint-record-compare",
        *_common(project),
        "--lock",
        "assets.lock.json",
        "--plan",
        "assets.plan.json",
        "--expected-fingerprint",
        expected,
        "--current-fingerprint",
        current,
    )


def _verify_fingerprint_comparison(
    project: Path,
    *,
    expected: str = "expected-fingerprint.json",
    current: str = "current-fingerprint.json",
    comparison: str = "comparison.json",
) -> subprocess.CompletedProcess[str]:
    return _run(
        "source",
        "asset-cache-fingerprint-comparison-verify",
        *_common(project),
        "--lock",
        "assets.lock.json",
        "--plan",
        "assets.plan.json",
        "--expected-fingerprint",
        expected,
        "--current-fingerprint",
        current,
        "--comparison",
        comparison,
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


def test_asset_cache_unreferenced_preview_reports_absent_cache_without_creation(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "absent"
    _write_project(project)
    _prepare(project)
    before_project = _files(project)

    result = _preview_unreferenced(project, cache)

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["$schema"] == "ludoweave.asset-cache-unreferenced-preview/1"
    assert report["status"] == "observed"
    assert report["fingerprint_protocol"] == "ludoweave.asset-cache-fingerprint/1"
    assert report["inventory_protocol"] == "ludoweave.asset-cache-inventory/1"
    assert report["unreferenced_blobs"] == 0
    assert report["unreferenced_blob_bytes"] == 0
    assert not cache.exists()
    assert _files(project) == before_project


def test_asset_cache_unreferenced_preview_is_stable_path_free_and_read_only(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    orphan = b"preview-only unreferenced blob"
    digest = sha256(orphan).hexdigest()
    path = cache / "cas" / digest[:2] / digest
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(orphan)
    before_project = _files(project)
    before_cache = _files(cache)

    first = _preview_unreferenced(project, cache)
    second = _preview_unreferenced(project, cache)

    assert first.returncode == second.returncode == 0
    assert first.stderr == second.stderr == ""
    assert first.stdout == second.stdout
    report = cast(dict[str, object], json.loads(first.stdout))
    assert report["unreferenced_blobs"] == 1
    assert report["unreferenced_blob_bytes"] == len(orphan)
    assert str(report["plan_sha256"]).startswith("sha256:")
    assert str(report["observation_sha256"]).startswith("sha256:")
    assert digest not in first.stdout
    assert str(project) not in first.stdout
    assert str(cache) not in first.stdout
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_unreferenced_preview_does_not_mark_referenced_blob(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0

    result = _preview_unreferenced(project, cache)

    assert result.returncode == 0
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["unreferenced_blobs"] == 0
    assert report["unreferenced_blob_bytes"] == 0


def test_asset_cache_unreferenced_preview_checks_inputs_before_cache_observation(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "absent"
    _write_project(project)
    _prepare(project)
    (project / "assets/item.json").write_bytes(b'{"value":2}')

    result = _preview_unreferenced(project, cache)

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] != "asset_cache.invalid_root"
    assert not cache.exists()
    assert str(project) not in result.stderr
    assert str(cache) not in result.stderr


def test_asset_cache_fingerprint_record_preview_is_stable_offline_and_read_only(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    orphan = b"offline unreferenced preview orphan"
    digest = sha256(orphan).hexdigest()
    path = cache / "cas" / digest[:2] / digest
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(orphan)
    fingerprint = _fingerprint(project, cache)
    assert fingerprint.returncode == 0
    (project / "fingerprint.json").write_bytes(fingerprint.stdout.rstrip("\n").encode("utf-8"))
    shutil.rmtree(cache)
    before = _files(project)

    first = _preview_unreferenced_record(project)
    second = _preview_unreferenced_record(project)

    assert first.returncode == second.returncode == 0
    assert first.stderr == second.stderr == ""
    assert first.stdout == second.stdout
    report = cast(dict[str, object], json.loads(first.stdout))
    assert report["$schema"] == "ludoweave.asset-cache-unreferenced-preview/1"
    assert report["status"] == "observed"
    assert report["unreferenced_blobs"] == 1
    assert report["unreferenced_blob_bytes"] == len(orphan)
    assert digest not in first.stdout
    assert str(project) not in first.stdout
    assert str(cache) not in first.stdout
    assert _files(project) == before
    assert not cache.exists()


def test_asset_cache_fingerprint_record_preview_rejects_another_plan(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    fingerprint = _fingerprint(project, cache)
    assert fingerprint.returncode == 0
    (project / "fingerprint.json").write_bytes(fingerprint.stdout.rstrip("\n").encode("utf-8"))
    (project / "assets/item.json").write_bytes(b'{"value":2}')
    _prepare(project)
    before = _files(project)

    result = _preview_unreferenced_record(project)

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] == "asset_cache.unreferenced_preview_mismatch"
    assert str(project) not in result.stderr
    assert str(cache) not in result.stderr
    assert _files(project) == before
    assert not cache.exists()


def test_asset_cache_fingerprint_record_preview_preflights_before_record_read(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    _write_project(project)
    _prepare(project)
    (project / "assets/item.json").write_bytes(b'{"value":2}')

    result = _preview_unreferenced_record(project, fingerprint="missing.json")

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] != "tools.input_unavailable"
    assert str(project) not in result.stderr


def test_asset_cache_fingerprint_verify_reads_exact_saved_record_and_current_cache(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    fingerprint = _fingerprint(project, cache)
    assert fingerprint.returncode == 0
    (project / "fingerprint.json").write_bytes(fingerprint.stdout.rstrip("\n").encode("utf-8"))
    before_project = _files(project)
    before_cache = _files(cache)

    result = _verify_fingerprint(project, cache)

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["$schema"] == "ludoweave.asset-cache-fingerprint-verification/1"
    assert report["fingerprint_protocol"] == "ludoweave.asset-cache-fingerprint/1"
    assert report["status"] == "valid"
    assert str(report["plan_sha256"]).startswith("sha256:")
    assert str(report["observation_sha256"]).startswith("sha256:")
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_fingerprint_verify_rejects_changed_cache_content_silently(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    fingerprint = _fingerprint(project, cache)
    assert fingerprint.returncode == 0
    (project / "fingerprint.json").write_bytes(fingerprint.stdout.rstrip("\n").encode("utf-8"))
    orphan = b"changed cache content"
    digest = sha256(orphan).hexdigest()
    path = cache / "cas" / digest[:2] / digest
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(orphan)
    before_project = _files(project)
    before_cache = _files(cache)

    result = _verify_fingerprint(project, cache)

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] == "asset_cache.fingerprint_mismatch"
    assert str(project) not in result.stderr
    assert str(cache) not in result.stderr
    assert digest not in result.stderr
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_fingerprint_verify_checks_current_inputs_before_record_read(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "absent"
    _write_project(project)
    _prepare(project)
    (project / "assets/item.json").write_bytes(b'{"value":2}')

    result = _verify_fingerprint(project, cache, fingerprint="missing.json")

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] != "tools.input_unavailable"
    assert str(project) not in result.stderr
    assert str(cache) not in result.stderr
    assert not cache.exists()


def test_asset_cache_fingerprint_compare_reports_equal_read_only(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    fingerprint = _fingerprint(project, cache)
    assert fingerprint.returncode == 0
    (project / "fingerprint.json").write_bytes(fingerprint.stdout.rstrip("\n").encode("utf-8"))
    before_project = _files(project)
    before_cache = _files(cache)

    result = _compare_fingerprint(project, cache)

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    deltas = cast(dict[str, object], report["deltas"])
    assert report["$schema"] == "ludoweave.asset-cache-fingerprint-comparison/1"
    assert report["fingerprint_protocol"] == "ludoweave.asset-cache-fingerprint/1"
    assert report["status"] == "equal"
    assert report["observation_equal"] is True
    assert len(deltas) == 12
    assert set(deltas.values()) == {0}
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_fingerprint_compare_reports_aggregate_difference(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    fingerprint = _fingerprint(project, cache)
    assert fingerprint.returncode == 0
    saved = cast(dict[str, object], json.loads(fingerprint.stdout))
    saved_observation = str(saved["observation_sha256"])
    (project / "fingerprint.json").write_bytes(fingerprint.stdout.rstrip("\n").encode("utf-8"))
    orphan = b"diagnostic orphan"
    digest = sha256(orphan).hexdigest()
    path = cache / "cas" / digest[:2] / digest
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(orphan)
    before_project = _files(project)
    before_cache = _files(cache)

    result = _compare_fingerprint(project, cache)

    assert result.returncode == 1
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    deltas = cast(dict[str, object], report["deltas"])
    assert report["status"] == "different"
    assert report["observation_equal"] is False
    assert deltas["cas_blobs"] == 1
    assert deltas["other_blobs"] == 1
    assert deltas["unreferenced_blobs"] == 1
    assert deltas["unreferenced_blob_bytes"] == len(orphan)
    assert digest not in result.stdout
    assert saved_observation not in result.stdout
    assert str(project) not in result.stdout
    assert str(cache) not in result.stdout
    assert _files(project) == before_project
    assert _files(cache) == before_cache


def test_asset_cache_fingerprint_compare_detects_same_size_content_substitution(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    first = b"first orphan"
    first_digest = sha256(first).hexdigest()
    first_path = cache / "cas" / first_digest[:2] / first_digest
    first_path.parent.mkdir(exist_ok=True)
    first_path.write_bytes(first)
    fingerprint = _fingerprint(project, cache)
    assert fingerprint.returncode == 0
    (project / "fingerprint.json").write_bytes(fingerprint.stdout.rstrip("\n").encode("utf-8"))
    first_path.unlink()
    second = b"other orphan"
    assert len(first) == len(second)
    second_digest = sha256(second).hexdigest()
    second_path = cache / "cas" / second_digest[:2] / second_digest
    second_path.parent.mkdir(exist_ok=True)
    second_path.write_bytes(second)

    result = _compare_fingerprint(project, cache)

    assert result.returncode == 1
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    deltas = cast(dict[str, object], report["deltas"])
    assert report["status"] == "different"
    assert report["observation_equal"] is False
    assert set(deltas.values()) == {0}
    assert first_digest not in result.stdout
    assert second_digest not in result.stdout


def test_asset_cache_fingerprint_compare_checks_current_inputs_before_record_read(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "absent"
    _write_project(project)
    _prepare(project)
    (project / "assets/item.json").write_bytes(b'{"value":2}')

    result = _compare_fingerprint(project, cache, fingerprint="missing.json")

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] != "tools.input_unavailable"
    assert str(project) not in result.stderr
    assert str(cache) not in result.stderr
    assert not cache.exists()


def test_asset_cache_fingerprint_record_compare_is_offline_and_equal(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    fingerprint = _fingerprint(project, cache)
    assert fingerprint.returncode == 0
    canonical = fingerprint.stdout.rstrip("\n").encode("utf-8")
    (project / "expected-fingerprint.json").write_bytes(canonical)
    (project / "current-fingerprint.json").write_bytes(canonical)
    shutil.rmtree(cache)
    before = _files(project)

    result = _compare_fingerprint_records(project)

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    deltas = cast(dict[str, object], report["deltas"])
    assert report["$schema"] == "ludoweave.asset-cache-fingerprint-comparison/1"
    assert report["status"] == "equal"
    assert report["observation_equal"] is True
    assert len(deltas) == 12
    assert set(deltas.values()) == {0}
    assert _files(project) == before
    assert not cache.exists()


def test_asset_cache_fingerprint_record_compare_reports_offline_aggregate_change(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    expected = _fingerprint(project, cache)
    assert expected.returncode == 0
    (project / "expected-fingerprint.json").write_bytes(
        expected.stdout.rstrip("\n").encode("utf-8")
    )
    orphan = b"offline diagnostic orphan"
    digest = sha256(orphan).hexdigest()
    path = cache / "cas" / digest[:2] / digest
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(orphan)
    current = _fingerprint(project, cache)
    assert current.returncode == 0
    current_document = cast(dict[str, object], json.loads(current.stdout))
    current_observation = str(current_document["observation_sha256"])
    (project / "current-fingerprint.json").write_bytes(current.stdout.rstrip("\n").encode("utf-8"))
    shutil.rmtree(cache)
    before = _files(project)

    result = _compare_fingerprint_records(project)

    assert result.returncode == 1
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    deltas = cast(dict[str, object], report["deltas"])
    assert report["status"] == "different"
    assert report["observation_equal"] is False
    assert deltas["cas_blobs"] == 1
    assert deltas["other_blobs"] == 1
    assert deltas["unreferenced_blobs"] == 1
    assert deltas["unreferenced_blob_bytes"] == len(orphan)
    assert digest not in result.stdout
    assert current_observation not in result.stdout
    assert str(project) not in result.stdout
    assert _files(project) == before
    assert not cache.exists()


def test_asset_cache_fingerprint_record_compare_detects_identity_only_change(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    first = b"first orphan"
    first_digest = sha256(first).hexdigest()
    first_path = cache / "cas" / first_digest[:2] / first_digest
    first_path.parent.mkdir(exist_ok=True)
    first_path.write_bytes(first)
    expected = _fingerprint(project, cache)
    assert expected.returncode == 0
    (project / "expected-fingerprint.json").write_bytes(
        expected.stdout.rstrip("\n").encode("utf-8")
    )
    first_path.unlink()
    second = b"other orphan"
    assert len(first) == len(second)
    second_digest = sha256(second).hexdigest()
    second_path = cache / "cas" / second_digest[:2] / second_digest
    second_path.parent.mkdir(exist_ok=True)
    second_path.write_bytes(second)
    current = _fingerprint(project, cache)
    assert current.returncode == 0
    (project / "current-fingerprint.json").write_bytes(current.stdout.rstrip("\n").encode("utf-8"))
    shutil.rmtree(cache)

    result = _compare_fingerprint_records(project)

    assert result.returncode == 1
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    deltas = cast(dict[str, object], report["deltas"])
    assert report["status"] == "different"
    assert report["observation_equal"] is False
    assert set(deltas.values()) == {0}
    assert first_digest not in result.stdout
    assert second_digest not in result.stdout
    assert not cache.exists()


def test_asset_cache_fingerprint_record_compare_checks_inputs_before_records(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    _write_project(project)
    _prepare(project)
    (project / "assets/item.json").write_bytes(b'{"value":2}')

    result = _compare_fingerprint_records(
        project,
        expected="missing-expected.json",
        current="missing-current.json",
    )

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] != "tools.input_unavailable"
    assert str(project) not in result.stderr


def test_asset_cache_fingerprint_comparison_verify_accepts_equal_report_offline(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    fingerprint = _fingerprint(project, cache)
    assert fingerprint.returncode == 0
    canonical = fingerprint.stdout.rstrip("\n").encode("utf-8")
    (project / "expected-fingerprint.json").write_bytes(canonical)
    (project / "current-fingerprint.json").write_bytes(canonical)
    comparison = _compare_fingerprint_records(project)
    assert comparison.returncode == 0
    comparison_bytes = comparison.stdout.rstrip("\n").encode("utf-8")
    (project / "comparison.json").write_bytes(comparison_bytes)
    shutil.rmtree(cache)
    before = _files(project)

    result = _verify_fingerprint_comparison(project)

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report == {
        "$schema": "ludoweave.asset-cache-fingerprint-comparison-verification/1",
        "status": "valid",
        "fingerprint_protocol": "ludoweave.asset-cache-fingerprint/1",
        "comparison_protocol": "ludoweave.asset-cache-fingerprint-comparison/1",
        "plan_sha256": cast(dict[str, object], json.loads(comparison.stdout))["plan_sha256"],
        "comparison_status": "equal",
        "comparison_sha256": f"sha256:{sha256(comparison_bytes).hexdigest()}",
    }
    assert _files(project) == before
    assert not cache.exists()


def test_asset_cache_fingerprint_comparison_verify_accepts_different_report_offline(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    expected = _fingerprint(project, cache)
    assert expected.returncode == 0
    (project / "expected-fingerprint.json").write_bytes(
        expected.stdout.rstrip("\n").encode("utf-8")
    )
    orphan = b"comparison verification orphan"
    digest = sha256(orphan).hexdigest()
    path = cache / "cas" / digest[:2] / digest
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(orphan)
    current = _fingerprint(project, cache)
    assert current.returncode == 0
    current_document = cast(dict[str, object], json.loads(current.stdout))
    (project / "current-fingerprint.json").write_bytes(current.stdout.rstrip("\n").encode("utf-8"))
    comparison = _compare_fingerprint_records(project)
    assert comparison.returncode == 1
    comparison_bytes = comparison.stdout.rstrip("\n").encode("utf-8")
    (project / "comparison.json").write_bytes(comparison_bytes)
    shutil.rmtree(cache)
    before = _files(project)

    result = _verify_fingerprint_comparison(project)

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["status"] == "valid"
    assert report["comparison_status"] == "different"
    assert report["comparison_sha256"] == f"sha256:{sha256(comparison_bytes).hexdigest()}"
    assert digest not in result.stdout
    assert str(current_document["observation_sha256"]) not in result.stdout
    assert str(project) not in result.stdout
    assert _files(project) == before
    assert not cache.exists()


def test_asset_cache_fingerprint_comparison_verify_rejects_tampered_report(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    cache = tmp_path / "cache"
    _write_project(project)
    _prepare(project)
    assert _populate(project, cache).returncode == 0
    fingerprint = _fingerprint(project, cache)
    assert fingerprint.returncode == 0
    canonical = fingerprint.stdout.rstrip("\n").encode("utf-8")
    (project / "expected-fingerprint.json").write_bytes(canonical)
    (project / "current-fingerprint.json").write_bytes(canonical)
    comparison = _compare_fingerprint_records(project)
    assert comparison.returncode == 0
    document = cast(dict[str, object], json.loads(comparison.stdout))
    deltas = cast(dict[str, object], document["deltas"])
    deltas["cas_blobs"] = 1
    document["status"] = "different"
    (project / "comparison.json").write_bytes(canonical_dumps(document))
    shutil.rmtree(cache)
    before = _files(project)

    result = _verify_fingerprint_comparison(project)

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] == "asset_cache.fingerprint_comparison_mismatch"
    assert error["details"] == {"field": "deltas"}
    assert str(project) not in result.stderr
    assert _files(project) == before
    assert not cache.exists()


def test_asset_cache_fingerprint_comparison_verify_checks_inputs_before_records(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    _write_project(project)
    _prepare(project)
    (project / "assets/item.json").write_bytes(b'{"value":2}')

    result = _verify_fingerprint_comparison(
        project,
        expected="missing-expected.json",
        current="missing-current.json",
        comparison="missing-comparison.json",
    )

    assert result.returncode == 2
    assert result.stdout == ""
    error = cast(dict[str, object], cast(dict[str, object], json.loads(result.stderr))["error"])
    assert error["code"] != "tools.input_unavailable"
    assert str(project) not in result.stderr


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
