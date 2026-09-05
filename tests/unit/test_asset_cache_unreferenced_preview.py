"""Path-free unreferenced-blob preview behavior."""

from __future__ import annotations

import json
import shutil
from dataclasses import FrozenInstanceError, replace
from hashlib import sha256
from pathlib import Path
from typing import cast

import pytest

from ludoweave.assets import (
    ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS,
    ASSET_CACHE_INVENTORY_MAX_CAS_BYTES,
    AssetBuildInput,
    AssetBuildPlan,
    AssetCacheError,
    AssetCacheFingerprint,
    AssetCacheUnreferencedPreview,
    AssetEntry,
    AssetKind,
    AssetManifest,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetUri,
    fingerprint_asset_cache_observation,
    populate_asset_build_cache,
    preview_asset_cache_unreferenced_blobs,
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


def _preview(
    root: Path,
    *,
    orphan: bytes | None,
) -> tuple[AssetBuildPlan, AssetCacheFingerprint, AssetCacheUnreferencedPreview, str | None]:
    plan, inputs = _fixture(root / "project", b'{"value":1}')
    cache = root / "cache"
    populate_asset_build_cache(plan, inputs, cache)
    orphan_digest: str | None = None
    if orphan is not None:
        orphan_digest = sha256(orphan).hexdigest()
        path = cache / "cas" / orphan_digest[:2] / orphan_digest
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(orphan)
    fingerprint = fingerprint_asset_cache_observation(plan, cache)
    shutil.rmtree(cache)
    preview = preview_asset_cache_unreferenced_blobs(plan, fingerprint)
    return plan, fingerprint, preview, orphan_digest


def test_preview_reports_absent_cache_without_creating_or_reading_it(tmp_path: Path) -> None:
    plan, _inputs = _fixture(tmp_path / "project", b'{"value":1}')
    cache = tmp_path / "absent"
    fingerprint = fingerprint_asset_cache_observation(plan, cache)

    preview = preview_asset_cache_unreferenced_blobs(plan, fingerprint)

    assert preview.unreferenced_blobs == 0
    assert preview.unreferenced_blob_bytes == 0
    assert preview.plan_sha256 == fingerprint.inventory.plan_sha256
    assert preview.observation_sha256 == fingerprint.observation_sha256
    assert not cache.exists()


def test_preview_reports_existing_unreferenced_aggregates_without_identity(
    tmp_path: Path,
) -> None:
    orphan = b"unreferenced preview orphan"
    plan, fingerprint, preview, orphan_digest = _preview(tmp_path, orphan=orphan)
    before = (plan, fingerprint)

    document = preview.as_dict()
    encoded = preview.canonical_bytes()

    assert document == {
        "$schema": "ludoweave.asset-cache-unreferenced-preview/1",
        "status": "observed",
        "fingerprint_protocol": "ludoweave.asset-cache-fingerprint/1",
        "inventory_protocol": "ludoweave.asset-cache-inventory/1",
        "plan_sha256": fingerprint.inventory.plan_sha256,
        "observation_sha256": fingerprint.observation_sha256,
        "unreferenced_blobs": 1,
        "unreferenced_blob_bytes": len(orphan),
    }
    assert json.loads(encoded) == document
    assert encoded == preview.canonical_bytes()
    assert orphan_digest is not None
    assert orphan_digest.encode("ascii") not in encoded
    assert (plan, fingerprint) == before


def test_preview_does_not_count_action_referenced_blob(tmp_path: Path) -> None:
    _plan, _fingerprint, preview, orphan_digest = _preview(tmp_path, orphan=None)

    assert orphan_digest is None
    assert preview.unreferenced_blobs == 0
    assert preview.unreferenced_blob_bytes == 0


def test_preview_rejects_fingerprint_from_another_plan(tmp_path: Path) -> None:
    plan, _inputs = _fixture(tmp_path / "current", b'{"value":1}')
    other_plan, _other_inputs = _fixture(tmp_path / "other", b'{"value":2}')
    fingerprint = fingerprint_asset_cache_observation(other_plan, tmp_path / "absent")

    with pytest.raises(AssetCacheError) as caught:
        preview_asset_cache_unreferenced_blobs(plan, fingerprint)

    assert caught.value.code == "asset_cache.unreferenced_preview_mismatch"
    assert dict(caught.value.details) == {"field": "plan_sha256"}


@pytest.mark.parametrize("field", ["plan", "fingerprint"])
def test_preview_requires_exact_value_types(tmp_path: Path, field: str) -> None:
    plan, _inputs = _fixture(tmp_path / "project", b'{"value":1}')
    fingerprint = fingerprint_asset_cache_observation(plan, tmp_path / "absent")
    values: dict[str, object] = {"plan": plan, "fingerprint": fingerprint}
    values[field] = object()

    with pytest.raises(AssetCacheError) as caught:
        preview_asset_cache_unreferenced_blobs(
            cast(AssetBuildPlan, values["plan"]),
            cast(AssetCacheFingerprint, values["fingerprint"]),
        )

    assert caught.value.code == "asset_cache.invalid_unreferenced_preview"
    assert dict(caught.value.details) == {"field": field}


@pytest.mark.parametrize(
    ("changes"),
    [
        {"protocol": "invalid"},
        {"fingerprint_protocol": "invalid"},
        {"inventory_protocol": "invalid"},
        {"plan_sha256": "invalid"},
        {"observation_sha256": "invalid"},
        {"unreferenced_blobs": True},
        {"unreferenced_blobs": -1},
        {"unreferenced_blobs": ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS + 1},
        {"unreferenced_blob_bytes": True},
        {"unreferenced_blob_bytes": -1},
        {"unreferenced_blob_bytes": ASSET_CACHE_INVENTORY_MAX_CAS_BYTES + 1},
        {"unreferenced_blobs": 0, "unreferenced_blob_bytes": 1},
    ],
)
def test_preview_value_rejects_invalid_fields(
    tmp_path: Path,
    changes: dict[str, object],
) -> None:
    _plan, _fingerprint, preview, _orphan_digest = _preview(
        tmp_path,
        orphan=b"orphan",
    )

    with pytest.raises(AssetCacheError) as caught:
        replace(preview, **changes)  # type: ignore[arg-type]

    assert caught.value.code == "asset_cache.invalid_unreferenced_preview"
    assert dict(caught.value.details) == {"field": "preview"}


def test_preview_is_frozen(tmp_path: Path) -> None:
    _plan, _fingerprint, preview, _orphan_digest = _preview(
        tmp_path,
        orphan=b"orphan",
    )

    with pytest.raises(FrozenInstanceError):
        preview.unreferenced_blobs = 0  # type: ignore[misc]
