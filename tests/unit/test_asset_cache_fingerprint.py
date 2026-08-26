"""Deterministic whole-cache observation fingerprint behavior."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

from ludoweave.assets import (
    ASSET_CACHE_FINGERPRINT_PROTOCOL,
    AssetBuildInput,
    AssetBuildPlan,
    AssetCacheError,
    AssetCacheFingerprint,
    AssetEntry,
    AssetKind,
    AssetManifest,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetUri,
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
    plan = AssetBuildPlan.from_inputs(manifest, lock)
    return plan, (AssetBuildInput(uri, source),)


def _populate(root: Path, cache: Path, source: bytes) -> AssetBuildPlan:
    plan, inputs = _fixture(root, source)
    populate_asset_build_cache(plan, inputs, cache)
    return plan


def _files(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _expected_observation(cache: Path) -> str:
    observed = sha256(ASSET_CACHE_FINGERPRINT_PROTOCOL.encode("ascii") + b"\0")
    metadata = sorted(cache.rglob("entry.json"), key=lambda path: path.parent.name)
    for path in metadata:
        payload = path.read_bytes()
        observed.update(b"A")
        observed.update(len(payload).to_bytes(8, "big"))
        observed.update(payload)
    blobs = sorted(path for path in (cache / "cas").rglob("*") if path.is_file())
    for path in blobs:
        payload = bytes.fromhex(path.name) + path.stat().st_size.to_bytes(8, "big")
        observed.update(b"C")
        observed.update(len(payload).to_bytes(8, "big"))
        observed.update(payload)
    return f"sha256:{observed.hexdigest()}"


def test_fingerprint_reports_absent_cache_without_creation(tmp_path: Path) -> None:
    plan, _inputs = _fixture(tmp_path / "project", b'{"value":1}')
    cache = tmp_path / "absent"

    report = fingerprint_asset_cache_observation(plan, cache)

    expected = sha256(ASSET_CACHE_FINGERPRINT_PROTOCOL.encode("ascii") + b"\0")
    assert report.protocol == ASSET_CACHE_FINGERPRINT_PROTOCOL
    assert report.observation_sha256 == f"sha256:{expected.hexdigest()}"
    assert report.inventory.current_actions == 0
    assert report.inventory.missing_actions == 1
    assert not cache.exists()


def test_fingerprint_is_reproducible_and_read_only(tmp_path: Path) -> None:
    first_cache = tmp_path / "first-cache"
    second_cache = tmp_path / "second-cache"
    source = b'{ "value": 1 }'
    first_plan = _populate(tmp_path / "first", first_cache, source)
    second_plan = _populate(tmp_path / "second", second_cache, source)
    first_before = _files(first_cache)
    second_before = _files(second_cache)

    first = fingerprint_asset_cache_observation(first_plan, first_cache)
    second = fingerprint_asset_cache_observation(second_plan, second_cache)

    assert first.observation_sha256 == second.observation_sha256
    assert first.observation_sha256 == _expected_observation(first_cache)
    assert first.canonical_bytes() == second.canonical_bytes()
    assert first.inventory.current_actions == second.inventory.current_actions == 1
    assert _files(first_cache) == first_before
    assert _files(second_cache) == second_before


def test_fingerprint_binds_exact_storage_when_counts_and_bytes_match(tmp_path: Path) -> None:
    first_cache = tmp_path / "first-cache"
    second_cache = tmp_path / "second-cache"
    first_plan = _populate(tmp_path / "first", first_cache, b'{"value":1}')
    second_plan = _populate(tmp_path / "second", second_cache, b'{"value":2}')

    first = fingerprint_asset_cache_observation(first_plan, first_cache)
    second = fingerprint_asset_cache_observation(second_plan, second_cache)

    assert first.inventory.current_actions == second.inventory.current_actions == 1
    assert first.inventory.cas_blobs == second.inventory.cas_blobs == 1
    assert first.inventory.current_blob_bytes == second.inventory.current_blob_bytes
    assert first.observation_sha256 != second.observation_sha256


def test_fingerprint_storage_identity_is_independent_of_current_plan(tmp_path: Path) -> None:
    cache = tmp_path / "cache"
    stored_plan = _populate(tmp_path / "stored", cache, b'{"value":1}')
    other_plan, _inputs = _fixture(tmp_path / "other", b'{"value":2}')

    stored = fingerprint_asset_cache_observation(stored_plan, cache)
    other = fingerprint_asset_cache_observation(other_plan, cache)

    assert stored.observation_sha256 == other.observation_sha256
    assert stored.inventory.plan_sha256 != other.inventory.plan_sha256
    assert (stored.inventory.current_actions, stored.inventory.other_actions) == (1, 0)
    assert (other.inventory.current_actions, other.inventory.other_actions) == (0, 1)


def test_fingerprint_rejects_invalid_digest(tmp_path: Path) -> None:
    plan, _inputs = _fixture(tmp_path / "project", b'{"value":1}')
    inventory = fingerprint_asset_cache_observation(plan, tmp_path / "absent").inventory

    with pytest.raises(AssetCacheError) as caught:
        AssetCacheFingerprint(inventory, "not-a-digest")

    assert caught.value.code == "asset_cache.invalid_fingerprint"
    assert dict(caught.value.details) == {"field": "fingerprint"}
