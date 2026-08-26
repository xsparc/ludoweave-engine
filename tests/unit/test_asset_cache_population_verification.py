"""Bounded saved population decoding and current-cache verification."""

from __future__ import annotations

import json
from collections.abc import Callable
from hashlib import sha256
from pathlib import Path
from typing import cast

import pytest

from ludoweave.assets import (
    ASSET_CACHE_POPULATION_RECORD_MAX_BYTES,
    ASSET_CACHE_POPULATION_VERIFICATION_PROTOCOL,
    AssetBuildInput,
    AssetBuildPlan,
    AssetBuildResultEntry,
    AssetCacheError,
    AssetCachePopulationRecord,
    AssetCachePopulationRecordEntry,
    AssetCachePopulationRecordLimits,
    AssetCacheStore,
    AssetEntry,
    AssetKind,
    AssetManifest,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetUri,
    populate_asset_build_cache,
    verify_asset_cache_population,
)


def _hash(payload: bytes) -> str:
    return f"sha256:{sha256(payload).hexdigest()}"


def _fixture(
    root: Path,
    *,
    first_source: bytes = b'{ "z": 2, "a": 1 }',
) -> tuple[AssetBuildPlan, tuple[AssetBuildInput, ...]]:
    first_uri = AssetUri("asset://data/config.json")
    second_uri = AssetUri("asset://shaders/main.wgsl")
    sources = {
        first_uri: first_source,
        second_uri: b"@vertex fn main() -> @builtin(position) vec4f { return vec4f(); }",
    }
    manifest = AssetManifest(
        root,
        (
            AssetEntry(first_uri, AssetKind.JSON, "assets/config.json"),
            AssetEntry(second_uri, AssetKind.WGSL, "assets/main.wgsl"),
        ),
    )
    lock = AssetSourceLock(
        source_lock_sha256=_hash(b"source-lock"),
        asset_manifest_sha256=_hash(manifest.canonical_bytes()),
        roots=(first_uri, second_uri),
        entries=tuple(
            AssetSourceLockEntry(uri, manifest.entry(uri).kind, _hash(source), len(source))
            for uri, source in sources.items()
        ),
    )
    plan = AssetBuildPlan.from_inputs(manifest, lock)
    return plan, tuple(AssetBuildInput(entry.uri, sources[entry.uri]) for entry in plan.entries)


def _population(
    root: Path,
) -> tuple[AssetBuildPlan, AssetCachePopulationRecord, Path]:
    plan, inputs = _fixture(root)
    cache = root / "cache"
    population = populate_asset_build_cache(plan, inputs, cache)
    record = AssetCachePopulationRecord.from_json(population.canonical_bytes())
    return plan, record, cache


def _files(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _add_extra(value: dict[str, object]) -> None:
    value["extra"] = True


def _change_hits(value: dict[str, object]) -> None:
    value["hits"] = 99


def _change_hits_type(value: dict[str, object]) -> None:
    value["hits"] = True


def _change_realization_status(value: dict[str, object]) -> None:
    entries_value = value["entries"]
    assert type(entries_value) is list
    entries = cast(list[object], entries_value)
    entry_value = entries[0]
    assert type(entry_value) is dict
    entry = cast(dict[str, object], entry_value)
    entry["realization_status"] = "other"


_INVALID_CHANGES: tuple[tuple[Callable[[dict[str, object]], None], str], ...] = (
    (_add_extra, "population"),
    (_change_hits, "hits"),
    (_change_hits_type, "hits"),
    (_change_realization_status, "entry"),
)


def test_population_record_round_trips_m135_canonical_bytes(tmp_path: Path) -> None:
    plan, inputs = _fixture(tmp_path)
    population = populate_asset_build_cache(plan, inputs, tmp_path / "cache")

    record = AssetCachePopulationRecord.from_json(population.canonical_bytes())

    assert record.canonical_bytes() == population.canonical_bytes()
    assert (record.hits, record.decoded) == (0, 2)
    assert (record.published, record.reused) == (2, 0)


def test_population_record_accepts_noncanonical_layout_and_normalizes(tmp_path: Path) -> None:
    plan, inputs = _fixture(tmp_path)
    population = populate_asset_build_cache(plan, inputs, tmp_path / "cache")
    document = json.dumps(population.as_dict(), indent=2)

    record = AssetCachePopulationRecord.from_json(document)

    assert record.canonical_bytes() == population.canonical_bytes()


@pytest.mark.parametrize(
    "change,field",
    _INVALID_CHANGES,
)
def test_population_record_rejects_invalid_schema_values(
    tmp_path: Path,
    change: Callable[[dict[str, object]], None],
    field: str,
) -> None:
    plan, inputs = _fixture(tmp_path)
    population = populate_asset_build_cache(plan, inputs, tmp_path / "cache")
    document = population.as_dict()
    change(document)

    with pytest.raises(AssetCacheError) as caught:
        AssetCachePopulationRecord.from_json(json.dumps(document))

    assert caught.value.code == "asset_cache.invalid_population_record"
    assert dict(caught.value.details)["field"] == field


def test_population_record_rejects_duplicate_names(tmp_path: Path) -> None:
    plan, inputs = _fixture(tmp_path)
    population = populate_asset_build_cache(plan, inputs, tmp_path / "cache")
    document = (
        population.canonical_bytes()
        .decode("utf-8")
        .replace(
            '"hits":0',
            '"hits":0,"hits":0',
            1,
        )
    )

    with pytest.raises(AssetCacheError) as caught:
        AssetCachePopulationRecord.from_json(document)

    assert caught.value.code == "asset_cache.invalid_population_json"
    assert dict(caught.value.details)["cause_type"] == "ValueError"


def test_population_record_limits_bytes_and_entries(tmp_path: Path) -> None:
    plan, inputs = _fixture(tmp_path)
    population = populate_asset_build_cache(plan, inputs, tmp_path / "cache")

    with pytest.raises(AssetCacheError) as bytes_caught:
        AssetCachePopulationRecord.from_json(b"x" * (ASSET_CACHE_POPULATION_RECORD_MAX_BYTES + 1))
    with pytest.raises(AssetCacheError) as entries_caught:
        AssetCachePopulationRecord.from_json(
            population.canonical_bytes(),
            limits=AssetCachePopulationRecordLimits(max_entries=1),
        )

    assert bytes_caught.value.code == "asset_cache.population_limit_exceeded"
    assert entries_caught.value.code == "asset_cache.population_limit_exceeded"


def test_saved_population_verifies_against_current_cache_without_mutation(tmp_path: Path) -> None:
    plan, record, cache = _population(tmp_path)
    before = _files(cache)

    verification = verify_asset_cache_population(plan, record, cache)

    assert verification.protocol == ASSET_CACHE_POPULATION_VERIFICATION_PROTOCOL
    assert verification.plan_sha256 == record.plan_sha256
    assert verification.entry_count == 2
    assert verification.as_dict()["status"] == "valid"
    assert _files(cache) == before


def test_plan_mismatch_precedes_every_cache_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _plan, record, cache = _population(tmp_path)
    changed_root = tmp_path / "changed"
    changed_root.mkdir()
    changed_plan, _inputs = _fixture(changed_root, first_source=b'{"changed":true}')
    calls = 0
    original = AssetCacheStore.load_action

    def observe(self: AssetCacheStore, entry: object) -> object:
        nonlocal calls
        calls += 1
        return original(self, entry)  # type: ignore[arg-type]

    monkeypatch.setattr(AssetCacheStore, "load_action", observe)
    with pytest.raises(AssetCacheError) as caught:
        verify_asset_cache_population(changed_plan, record, cache)

    assert caught.value.code == "asset_cache.population_mismatch"
    assert dict(caught.value.details)["field"] == "plan_sha256"
    assert calls == 0


def test_missing_current_cache_action_fails_without_creating_cache(tmp_path: Path) -> None:
    plan, record, _cache = _population(tmp_path)
    absent = tmp_path / "absent"

    with pytest.raises(AssetCacheError) as caught:
        verify_asset_cache_population(plan, record, absent)

    assert caught.value.code == "asset_cache.population_miss"
    assert not absent.exists()


def test_corrupt_current_cache_fails_without_repair(tmp_path: Path) -> None:
    plan, record, cache = _population(tmp_path)
    metadata = sorted(cache.rglob("entry.json"))[-1]
    metadata.write_bytes(b"{}")
    before = _files(cache)

    with pytest.raises(AssetCacheError) as caught:
        verify_asset_cache_population(plan, record, cache)

    assert caught.value.code == "asset_cache.corrupt_entry"
    assert _files(cache) == before


def test_recorded_artifact_mismatch_fails_content_silently(tmp_path: Path) -> None:
    plan, record, cache = _population(tmp_path)
    original = record.entries[0]
    changed_result = AssetBuildResultEntry(
        uri=original.result.uri,
        kind=original.result.kind,
        cache_key=original.result.cache_key,
        source_bytes=original.result.source_bytes,
        artifact_sha256=f"sha256:{'0' * 64}",
        artifact_bytes=original.result.artifact_bytes,
    )
    changed_entry = AssetCachePopulationRecordEntry(
        changed_result,
        original.realization_status,
        original.publication_status,
    )
    changed = AssetCachePopulationRecord(
        plan_sha256=record.plan_sha256,
        source_bytes=record.source_bytes,
        artifact_bytes=record.artifact_bytes,
        entries=(changed_entry, *record.entries[1:]),
    )

    with pytest.raises(AssetCacheError) as caught:
        verify_asset_cache_population(plan, changed, cache)

    assert caught.value.code == "asset_cache.population_mismatch"
    assert dict(caught.value.details) == {
        "field": "artifact",
        "uri": original.uri.value,
    }
    assert original.result.artifact_sha256 not in str(caught.value.as_dict())
