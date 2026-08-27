"""Strict saved unreferenced-preview admission and verification."""

from __future__ import annotations

import json
import shutil
from dataclasses import replace
from hashlib import sha256
from pathlib import Path
from typing import cast

import pytest

from ludoweave.assets import (
    ASSET_CACHE_UNREFERENCED_PREVIEW_RECORD_MAX_BYTES,
    AssetBuildInput,
    AssetBuildPlan,
    AssetCacheError,
    AssetCacheFingerprint,
    AssetCacheUnreferencedPreview,
    AssetCacheUnreferencedPreviewRecordLimits,
    AssetCacheUnreferencedPreviewVerification,
    AssetEntry,
    AssetKind,
    AssetManifest,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetUri,
    decode_asset_cache_unreferenced_preview,
    fingerprint_asset_cache_observation,
    populate_asset_build_cache,
    preview_asset_cache_unreferenced_blobs,
    verify_asset_cache_unreferenced_preview,
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


def _records(
    root: Path,
) -> tuple[AssetBuildPlan, AssetCacheFingerprint, AssetCacheUnreferencedPreview]:
    plan, inputs = _fixture(root / "project", b'{"value":1}')
    cache = root / "cache"
    populate_asset_build_cache(plan, inputs, cache)
    orphan = b"saved unreferenced preview verification orphan"
    digest = sha256(orphan).hexdigest()
    path = cache / "cas" / digest[:2] / digest
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(orphan)
    fingerprint = fingerprint_asset_cache_observation(plan, cache)
    shutil.rmtree(cache)
    preview = preview_asset_cache_unreferenced_blobs(plan, fingerprint)
    return plan, fingerprint, preview


def _document(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def test_canonical_preview_round_trip_and_offline_verification(tmp_path: Path) -> None:
    plan, fingerprint, preview = _records(tmp_path)
    cache = tmp_path / "cache"
    before = (plan, fingerprint, preview)

    decoded = decode_asset_cache_unreferenced_preview(preview.canonical_bytes())
    verification = verify_asset_cache_unreferenced_preview(plan, fingerprint, decoded)

    assert decoded == preview
    assert verification.as_dict() == {
        "$schema": "ludoweave.asset-cache-unreferenced-preview-verification/1",
        "status": "valid",
        "fingerprint_protocol": "ludoweave.asset-cache-fingerprint/1",
        "preview_protocol": "ludoweave.asset-cache-unreferenced-preview/1",
        "plan_sha256": preview.plan_sha256,
        "observation_sha256": preview.observation_sha256,
        "preview_sha256": _hash(preview.canonical_bytes()),
    }
    assert verification.canonical_bytes() == verification.canonical_bytes()
    assert (plan, fingerprint, preview) == before
    assert not cache.exists()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("plan_sha256", _hash(b"other plan")),
        ("observation_sha256", _hash(b"other observation")),
        ("unreferenced_blobs", 2),
        ("unreferenced_blob_bytes", 1),
    ],
)
def test_verification_rejects_tampered_preview_fields(
    tmp_path: Path,
    field: str,
    value: object,
) -> None:
    plan, fingerprint, preview = _records(tmp_path)
    tampered = replace(preview, **{field: value})

    with pytest.raises(AssetCacheError) as caught:
        verify_asset_cache_unreferenced_preview(plan, fingerprint, tampered)

    assert caught.value.code == "asset_cache.unreferenced_preview_verification_mismatch"
    assert dict(caught.value.details) == {"field": field}


@pytest.mark.parametrize("field", ["plan", "fingerprint", "preview"])
def test_verification_requires_exact_value_types(tmp_path: Path, field: str) -> None:
    plan, fingerprint, preview = _records(tmp_path)
    values: dict[str, object] = {
        "plan": plan,
        "fingerprint": fingerprint,
        "preview": preview,
    }
    values[field] = object()

    with pytest.raises(AssetCacheError) as caught:
        verify_asset_cache_unreferenced_preview(
            cast(AssetBuildPlan, values["plan"]),
            cast(AssetCacheFingerprint, values["fingerprint"]),
            cast(AssetCacheUnreferencedPreview, values["preview"]),
        )

    assert caught.value.code == "asset_cache.invalid_unreferenced_preview_verify"
    assert dict(caught.value.details) == {"field": field}


def test_decoder_rejects_schema_status_fields_and_aggregate_ambiguity(tmp_path: Path) -> None:
    _plan, _fingerprint, preview = _records(tmp_path)
    original = preview.as_dict()
    invalid_documents: list[tuple[str, bytes]] = []
    for field in (
        "$schema",
        "fingerprint_protocol",
        "inventory_protocol",
        "plan_sha256",
        "observation_sha256",
    ):
        document = dict(original)
        document[field] = "invalid"
        invalid_documents.append((field, _document(document)))
    status = dict(original)
    status["status"] = "valid"
    invalid_documents.append(("status", _document(status)))
    missing = dict(original)
    del missing["status"]
    invalid_documents.append(("preview", _document(missing)))
    extra = dict(original)
    extra["unexpected"] = 1
    invalid_documents.append(("preview", _document(extra)))
    for field in ("unreferenced_blobs", "unreferenced_blob_bytes"):
        for value in (True, -1, 1.5, 1 << 63):
            document = dict(original)
            document[field] = value
            invalid_documents.append((field, _document(document)))
    inconsistent = dict(original)
    inconsistent["unreferenced_blobs"] = 0
    invalid_documents.append(("preview", _document(inconsistent)))

    for field, document in invalid_documents:
        with pytest.raises(AssetCacheError) as caught:
            decode_asset_cache_unreferenced_preview(document)
        assert caught.value.code in {
            "asset_cache.invalid_unreferenced_preview_json",
            "asset_cache.invalid_unreferenced_preview_record",
        }
        if caught.value.code == "asset_cache.invalid_unreferenced_preview_record":
            assert dict(caught.value.details) == {"field": field}


def test_decoder_rejects_duplicate_nonfinite_noncanonical_and_invalid_unicode(
    tmp_path: Path,
) -> None:
    _plan, _fingerprint, preview = _records(tmp_path)
    canonical = preview.canonical_bytes()
    duplicate = canonical.replace(
        b'{"$schema":',
        b'{"$schema":"ludoweave.asset-cache-unreferenced-preview/1","$schema":',
        1,
    )
    nonfinite = canonical.replace(b'"unreferenced_blobs":1', b'"unreferenced_blobs":NaN', 1)

    for document in (duplicate, nonfinite, b"\xff", "\ud800"):
        with pytest.raises(AssetCacheError) as caught:
            decode_asset_cache_unreferenced_preview(document)
        assert caught.value.code == "asset_cache.invalid_unreferenced_preview_json"
    with pytest.raises(AssetCacheError) as noncanonical:
        decode_asset_cache_unreferenced_preview(canonical + b"\n")
    assert noncanonical.value.code == "asset_cache.noncanonical_unreferenced_preview_record"


def test_decoder_limits_are_exact_and_tightening_only(tmp_path: Path) -> None:
    _plan, _fingerprint, preview = _records(tmp_path)
    canonical = preview.canonical_bytes()
    tightened = AssetCacheUnreferencedPreviewRecordLimits(max_bytes=len(canonical))

    assert decode_asset_cache_unreferenced_preview(canonical, limits=tightened) == preview
    with pytest.raises(AssetCacheError) as limited:
        decode_asset_cache_unreferenced_preview(
            canonical,
            limits=AssetCacheUnreferencedPreviewRecordLimits(max_bytes=len(canonical) - 1),
        )
    with pytest.raises(AssetCacheError) as widened:
        AssetCacheUnreferencedPreviewRecordLimits(
            max_bytes=ASSET_CACHE_UNREFERENCED_PREVIEW_RECORD_MAX_BYTES + 1
        )
    with pytest.raises(AssetCacheError) as boolean:
        AssetCacheUnreferencedPreviewRecordLimits(max_bytes=True)  # type: ignore[arg-type]
    with pytest.raises(AssetCacheError) as wrong_type:
        decode_asset_cache_unreferenced_preview(
            canonical,
            limits=object(),  # type: ignore[arg-type]
        )

    assert limited.value.code == "asset_cache.unreferenced_preview_limit_exceeded"
    assert widened.value.code == "asset_cache.invalid_unreferenced_preview_limits"
    assert boolean.value.code == "asset_cache.invalid_unreferenced_preview_limits"
    assert wrong_type.value.code == "asset_cache.invalid_unreferenced_preview_limits"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("protocol", "invalid"),
        ("preview_protocol", "invalid"),
        ("fingerprint_protocol", "invalid"),
        ("plan_sha256", "invalid"),
        ("observation_sha256", "invalid"),
        ("preview_sha256", "invalid"),
    ],
)
def test_verification_value_rejects_invalid_fields(field: str, value: object) -> None:
    verification = AssetCacheUnreferencedPreviewVerification(
        plan_sha256=_hash(b"plan"),
        observation_sha256=_hash(b"observation"),
        preview_sha256=_hash(b"preview"),
    )

    with pytest.raises(AssetCacheError) as caught:
        replace(verification, **{field: value})

    assert caught.value.code == "asset_cache.invalid_unreferenced_preview_verification"
    assert dict(caught.value.details) == {"field": "verification"}
