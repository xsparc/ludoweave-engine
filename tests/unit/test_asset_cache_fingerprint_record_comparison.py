"""Offline comparison of two admitted cache-fingerprint records."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

import ludoweave.assets.fingerprint_comparison as comparison_module
from ludoweave.assets import (
    AssetBuildInput,
    AssetBuildPlan,
    AssetCacheError,
    AssetCacheFingerprint,
    AssetCacheInventoryDelta,
    AssetEntry,
    AssetKind,
    AssetManifest,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetUri,
    compare_asset_cache_fingerprint_records,
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


def _orphan(cache: Path, payload: bytes) -> Path:
    digest = sha256(payload).hexdigest()
    path = cache / "cas" / digest[:2] / digest
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return path


def test_equal_saved_records_compare_without_observation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan, inputs = _fixture(tmp_path / "project", b'{"value":1}')
    cache = tmp_path / "cache"
    populate_asset_build_cache(plan, inputs, cache)
    saved = fingerprint_asset_cache_observation(plan, cache)

    def observe(*args: object, **kwargs: object) -> object:
        del args, kwargs
        raise AssertionError("offline comparison must not observe a cache")

    monkeypatch.setattr(comparison_module, "fingerprint_asset_cache_observation", observe)
    report = compare_asset_cache_fingerprint_records(plan, saved, saved)

    assert report.equal
    assert report.as_dict() == {
        "$schema": "ludoweave.asset-cache-fingerprint-comparison/1",
        "status": "equal",
        "fingerprint_protocol": "ludoweave.asset-cache-fingerprint/1",
        "plan_sha256": saved.inventory.plan_sha256,
        "observation_equal": True,
        "deltas": {field: 0 for field in AssetCacheInventoryDelta.field_names()},
    }


def test_saved_records_report_signed_aggregate_changes(tmp_path: Path) -> None:
    plan, inputs = _fixture(tmp_path / "project", b'{"value":1}')
    cache = tmp_path / "cache"
    expected = fingerprint_asset_cache_observation(plan, cache)
    populate_asset_build_cache(plan, inputs, cache)
    current = fingerprint_asset_cache_observation(plan, cache)

    report = compare_asset_cache_fingerprint_records(plan, expected, current)

    assert not report.equal
    assert report.observation_equal is False
    assert report.deltas.current_actions == 1
    assert report.deltas.missing_actions == -1
    assert report.deltas.cas_blobs == 1
    assert report.deltas.current_blobs == 1
    assert report.deltas.current_action_metadata_bytes > 0
    assert report.deltas.current_blob_bytes > 0


def test_saved_records_detect_identity_only_substitution_without_disclosure(
    tmp_path: Path,
) -> None:
    plan, inputs = _fixture(tmp_path / "project", b'{"value":1}')
    cache = tmp_path / "cache"
    populate_asset_build_cache(plan, inputs, cache)
    first = _orphan(cache, b"first orphan")
    expected = fingerprint_asset_cache_observation(plan, cache)
    first.unlink()
    first.parent.rmdir()
    second = _orphan(cache, b"other orphan")
    current = fingerprint_asset_cache_observation(plan, cache)
    assert expected.inventory == current.inventory

    report = compare_asset_cache_fingerprint_records(plan, expected, current)
    encoded = report.canonical_bytes().decode("utf-8")

    assert not report.equal
    assert report.observation_equal is False
    assert not report.deltas.changed
    assert first.name not in encoded
    assert second.name not in encoded
    assert expected.observation_sha256 not in encoded
    assert current.observation_sha256 not in encoded


@pytest.mark.parametrize("record", ["expected", "current"])
def test_saved_record_plan_mismatch_fails_closed(tmp_path: Path, record: str) -> None:
    plan, _inputs = _fixture(tmp_path / "project", b'{"value":1}')
    other_plan, _inputs = _fixture(tmp_path / "other", b'{"value":2}')
    matching = fingerprint_asset_cache_observation(plan, tmp_path / "matching")
    other = fingerprint_asset_cache_observation(other_plan, tmp_path / "other-cache")
    expected = other if record == "expected" else matching
    current = other if record == "current" else matching

    with pytest.raises(AssetCacheError) as caught:
        compare_asset_cache_fingerprint_records(plan, expected, current)

    assert caught.value.code == "asset_cache.fingerprint_mismatch"
    assert dict(caught.value.details) == {"field": "plan_sha256", "record": record}


def test_saved_record_comparison_requires_exact_values(tmp_path: Path) -> None:
    plan, _inputs = _fixture(tmp_path / "project", b'{"value":1}')
    saved = fingerprint_asset_cache_observation(plan, tmp_path / "absent")

    with pytest.raises(AssetCacheError) as caught:
        compare_asset_cache_fingerprint_records(
            plan,
            saved,
            object(),  # type: ignore[arg-type]
        )

    assert caught.value.code == "asset_cache.invalid_fingerprint_comparison"
    assert dict(caught.value.details) == {
        "field": "plan_or_fingerprint",
        "record": "current",
    }


def test_saved_record_comparison_preserves_frozen_inputs(tmp_path: Path) -> None:
    plan, _inputs = _fixture(tmp_path / "project", b'{"value":1}')
    saved = fingerprint_asset_cache_observation(plan, tmp_path / "absent")
    before: tuple[AssetCacheFingerprint, AssetCacheFingerprint] = (saved, saved)

    compare_asset_cache_fingerprint_records(plan, saved, saved)

    assert (saved, saved) == before
