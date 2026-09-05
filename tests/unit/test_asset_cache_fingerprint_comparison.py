"""Path-free aggregate comparison of saved cache fingerprints."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

import ludoweave.assets.fingerprint_comparison as comparison_module
from ludoweave.assets import (
    ASSET_CACHE_FINGERPRINT_COMPARISON_PROTOCOL,
    ASSET_CACHE_INVENTORY_MAX_ACTIONS,
    AssetBuildInput,
    AssetBuildPlan,
    AssetCacheError,
    AssetCacheInventoryDelta,
    AssetEntry,
    AssetKind,
    AssetManifest,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetUri,
    compare_asset_cache_fingerprint,
    fingerprint_asset_cache_observation,
    populate_asset_build_cache,
)


def _hash(payload: bytes) -> str:
    return f"sha256:{sha256(payload).hexdigest()}"


def _fixture(root: Path, source: bytes) -> tuple[AssetBuildPlan, tuple[AssetBuildInput, ...]]:
    root.mkdir(parents=True, exist_ok=True)
    uri = AssetUri("asset://data/config.json")
    manifest = AssetManifest(
        root,
        (AssetEntry(uri, AssetKind.JSON, "assets/config.json"),),
    )
    lock = AssetSourceLock(
        source_lock_sha256=_hash(b"source-lock"),
        asset_manifest_sha256=_hash(manifest.canonical_bytes()),
        roots=(uri,),
        entries=(AssetSourceLockEntry(uri, AssetKind.JSON, _hash(source), len(source)),),
    )
    return AssetBuildPlan.from_inputs(manifest, lock), (AssetBuildInput(uri, source),)


def _population(root: Path) -> tuple[AssetBuildPlan, Path]:
    plan, inputs = _fixture(root / "project", b'{"value":1}')
    cache = root / "cache"
    populate_asset_build_cache(plan, inputs, cache)
    return plan, cache


def _files(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _orphan(cache: Path, payload: bytes) -> Path:
    digest = sha256(payload).hexdigest()
    path = cache / "cas" / digest[:2] / digest
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return path


def test_equal_fingerprint_reports_fixed_zero_deltas_read_only(tmp_path: Path) -> None:
    plan, cache = _population(tmp_path)
    saved = fingerprint_asset_cache_observation(plan, cache)
    before = _files(cache)

    report = compare_asset_cache_fingerprint(plan, saved, cache)

    assert report.protocol == ASSET_CACHE_FINGERPRINT_COMPARISON_PROTOCOL
    assert report.equal
    assert report.as_dict() == {
        "$schema": "ludoweave.asset-cache-fingerprint-comparison/1",
        "status": "equal",
        "fingerprint_protocol": "ludoweave.asset-cache-fingerprint/1",
        "plan_sha256": saved.inventory.plan_sha256,
        "observation_equal": True,
        "deltas": {field: 0 for field in AssetCacheInventoryDelta.field_names()},
    }
    assert _files(cache) == before


def test_absent_cache_compares_equal_without_creation(tmp_path: Path) -> None:
    plan, _inputs = _fixture(tmp_path / "project", b'{"value":1}')
    cache = tmp_path / "absent"
    saved = fingerprint_asset_cache_observation(plan, cache)

    report = compare_asset_cache_fingerprint(plan, saved, cache)

    assert report.equal
    assert not cache.exists()


def test_population_after_absent_fingerprint_reports_signed_aggregate_changes(
    tmp_path: Path,
) -> None:
    plan, inputs = _fixture(tmp_path / "project", b'{"value":1}')
    cache = tmp_path / "cache"
    saved = fingerprint_asset_cache_observation(plan, cache)
    populate_asset_build_cache(plan, inputs, cache)

    report = compare_asset_cache_fingerprint(plan, saved, cache)

    assert not report.equal
    assert report.observation_equal is False
    assert report.deltas.current_actions == 1
    assert report.deltas.missing_actions == -1
    assert report.deltas.current_blobs == 1
    assert report.deltas.cas_blobs == 1
    assert report.deltas.current_action_metadata_bytes > 0
    assert report.deltas.current_blob_bytes > 0


def test_new_orphan_reports_only_path_free_orphan_aggregates(tmp_path: Path) -> None:
    plan, cache = _population(tmp_path)
    saved = fingerprint_asset_cache_observation(plan, cache)
    payload = b"new orphan"
    orphan = _orphan(cache, payload)

    report = compare_asset_cache_fingerprint(plan, saved, cache)
    encoded = report.canonical_bytes().decode("utf-8")

    assert report.as_dict()["status"] == "different"
    assert report.deltas.cas_blobs == 1
    assert report.deltas.other_blobs == 1
    assert report.deltas.other_blob_bytes == len(payload)
    assert report.deltas.unreferenced_blobs == 1
    assert report.deltas.unreferenced_blob_bytes == len(payload)
    assert orphan.name not in encoded
    assert saved.observation_sha256 not in encoded


def test_equal_aggregates_with_substituted_content_reports_digest_difference(
    tmp_path: Path,
) -> None:
    plan, cache = _population(tmp_path)
    first = _orphan(cache, b"first orphan")
    saved = fingerprint_asset_cache_observation(plan, cache)
    first.unlink()
    first.parent.rmdir()
    second = _orphan(cache, b"other orphan")
    current = fingerprint_asset_cache_observation(plan, cache)
    assert saved.inventory == current.inventory

    report = compare_asset_cache_fingerprint(plan, saved, cache)
    encoded = report.canonical_bytes().decode("utf-8")

    assert not report.equal
    assert report.observation_equal is False
    assert not report.deltas.changed
    assert second.name not in encoded
    assert saved.observation_sha256 not in encoded
    assert current.observation_sha256 not in encoded


def test_plan_mismatch_precedes_cache_observation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan, cache = _population(tmp_path)
    saved = fingerprint_asset_cache_observation(plan, cache)
    changed_plan, _inputs = _fixture(tmp_path / "changed", b'{"value":2}')
    calls = 0

    def observe(*args: object, **kwargs: object) -> object:
        nonlocal calls
        del args, kwargs
        calls += 1
        raise AssertionError("cache observation must not start")

    monkeypatch.setattr(comparison_module, "fingerprint_asset_cache_observation", observe)
    with pytest.raises(AssetCacheError) as caught:
        compare_asset_cache_fingerprint(changed_plan, saved, cache)

    assert caught.value.code == "asset_cache.fingerprint_mismatch"
    assert dict(caught.value.details) == {"field": "plan_sha256"}
    assert calls == 0


def test_delta_rejects_inventories_from_different_plans(tmp_path: Path) -> None:
    first_plan, _inputs = _fixture(tmp_path / "first", b'{"value":1}')
    second_plan, _inputs = _fixture(tmp_path / "second", b'{"value":2}')
    first = fingerprint_asset_cache_observation(first_plan, tmp_path / "absent-first")
    second = fingerprint_asset_cache_observation(second_plan, tmp_path / "absent-second")

    with pytest.raises(AssetCacheError) as caught:
        AssetCacheInventoryDelta.between(first.inventory, second.inventory)

    assert caught.value.code == "asset_cache.fingerprint_mismatch"
    assert dict(caught.value.details) == {"field": "plan_sha256"}


def test_corrupt_cache_fails_without_repair(tmp_path: Path) -> None:
    plan, cache = _population(tmp_path)
    saved = fingerprint_asset_cache_observation(plan, cache)
    metadata = next(cache.rglob("entry.json"))
    metadata.write_bytes(b"{}")
    before = _files(cache)

    with pytest.raises(AssetCacheError) as caught:
        compare_asset_cache_fingerprint(plan, saved, cache)

    assert caught.value.code == "asset_cache.corrupt_inventory"
    assert _files(cache) == before


def test_delta_rejects_boolean_and_out_of_range_values() -> None:
    values = {field: 0 for field in AssetCacheInventoryDelta.field_names()}
    values["current_actions"] = True
    with pytest.raises(AssetCacheError) as boolean:
        AssetCacheInventoryDelta(**values)  # type: ignore[arg-type]
    values["current_actions"] = ASSET_CACHE_INVENTORY_MAX_ACTIONS + 1
    with pytest.raises(AssetCacheError) as oversized:
        AssetCacheInventoryDelta(**values)  # type: ignore[arg-type]

    assert boolean.value.code == "asset_cache.invalid_fingerprint_comparison"
    assert oversized.value.code == "asset_cache.invalid_fingerprint_comparison"
