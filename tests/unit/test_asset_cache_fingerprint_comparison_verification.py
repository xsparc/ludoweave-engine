"""Strict saved cache-fingerprint comparison admission and verification."""

from __future__ import annotations

import json
from dataclasses import replace
from hashlib import sha256
from pathlib import Path
from typing import cast

import pytest

import ludoweave.assets.fingerprint_comparison as comparison_module
from ludoweave.assets import (
    ASSET_CACHE_FINGERPRINT_COMPARISON_RECORD_MAX_BYTES,
    AssetBuildInput,
    AssetBuildPlan,
    AssetCacheError,
    AssetCacheFingerprint,
    AssetCacheFingerprintComparison,
    AssetCacheFingerprintComparisonRecordLimits,
    AssetEntry,
    AssetKind,
    AssetManifest,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetUri,
    compare_asset_cache_fingerprint_records,
    decode_asset_cache_fingerprint_comparison,
    fingerprint_asset_cache_observation,
    populate_asset_build_cache,
    verify_asset_cache_fingerprint_comparison,
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
    *,
    different: bool,
) -> tuple[
    AssetBuildPlan,
    AssetCacheFingerprint,
    AssetCacheFingerprint,
    AssetCacheFingerprintComparison,
]:
    plan, inputs = _fixture(root / "project", b'{"value":1}')
    cache = root / "cache"
    populate_asset_build_cache(plan, inputs, cache)
    expected = fingerprint_asset_cache_observation(plan, cache)
    if different:
        orphan = b"saved comparison verification orphan"
        digest = sha256(orphan).hexdigest()
        path = cache / "cas" / digest[:2] / digest
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(orphan)
    current = fingerprint_asset_cache_observation(plan, cache)
    comparison = compare_asset_cache_fingerprint_records(plan, expected, current)
    return plan, expected, current, comparison


def _document(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


@pytest.mark.parametrize("different", [False, True])
def test_canonical_comparison_round_trip_and_offline_verification(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    different: bool,
) -> None:
    plan, expected, current, comparison = _records(tmp_path, different=different)

    def observe(*args: object, **kwargs: object) -> object:
        del args, kwargs
        raise AssertionError("saved comparison verification must not observe a cache")

    monkeypatch.setattr(comparison_module, "fingerprint_asset_cache_observation", observe)
    decoded = decode_asset_cache_fingerprint_comparison(comparison.canonical_bytes())
    verification = verify_asset_cache_fingerprint_comparison(
        plan,
        expected,
        current,
        decoded,
    )

    assert decoded == comparison
    assert verification.as_dict() == {
        "$schema": "ludoweave.asset-cache-fingerprint-comparison-verification/1",
        "status": "valid",
        "fingerprint_protocol": "ludoweave.asset-cache-fingerprint/1",
        "comparison_protocol": "ludoweave.asset-cache-fingerprint-comparison/1",
        "plan_sha256": comparison.plan_sha256,
        "comparison_status": "different" if different else "equal",
        "comparison_sha256": _hash(comparison.canonical_bytes()),
    }


@pytest.mark.parametrize("field", ["observation_equal", "deltas"])
def test_verification_rejects_tampered_comparison_fields(tmp_path: Path, field: str) -> None:
    plan, expected, current, comparison = _records(tmp_path, different=False)
    if field == "observation_equal":
        tampered = replace(comparison, observation_equal=False)
    else:
        tampered = replace(
            comparison,
            deltas=replace(comparison.deltas, current_actions=1),
        )

    with pytest.raises(AssetCacheError) as caught:
        verify_asset_cache_fingerprint_comparison(plan, expected, current, tampered)

    assert caught.value.code == "asset_cache.fingerprint_comparison_mismatch"
    assert dict(caught.value.details) == {"field": field}


def test_verification_rejects_comparison_from_another_plan(tmp_path: Path) -> None:
    plan, expected, current, _comparison = _records(tmp_path / "first", different=False)
    other_plan, _inputs = _fixture(
        tmp_path / "other" / "project",
        b'{"value":2}',
    )
    other_expected = fingerprint_asset_cache_observation(
        other_plan,
        tmp_path / "other-cache",
    )
    other_current = other_expected
    other_comparison = compare_asset_cache_fingerprint_records(
        other_plan,
        other_expected,
        other_current,
    )
    assert plan != other_plan
    assert other_expected == other_current

    with pytest.raises(AssetCacheError) as caught:
        verify_asset_cache_fingerprint_comparison(
            plan,
            expected,
            current,
            other_comparison,
        )

    assert caught.value.code == "asset_cache.fingerprint_comparison_mismatch"
    assert dict(caught.value.details) == {"field": "plan_sha256"}


@pytest.mark.parametrize("field", ["plan", "expected", "current", "comparison"])
def test_verification_requires_exact_value_types(tmp_path: Path, field: str) -> None:
    plan, expected, current, comparison = _records(tmp_path, different=False)
    values: dict[str, object] = {
        "plan": plan,
        "expected": expected,
        "current": current,
        "comparison": comparison,
    }
    values[field] = object()

    with pytest.raises(AssetCacheError) as caught:
        verify_asset_cache_fingerprint_comparison(
            cast(AssetBuildPlan, values["plan"]),
            cast(AssetCacheFingerprint, values["expected"]),
            cast(AssetCacheFingerprint, values["current"]),
            cast(AssetCacheFingerprintComparison, values["comparison"]),
        )

    assert caught.value.code == "asset_cache.invalid_fingerprint_comparison_verify"
    assert dict(caught.value.details) == {"field": field}


def test_decoder_rejects_schema_status_and_delta_ambiguity(tmp_path: Path) -> None:
    _plan, _expected, _current, comparison = _records(tmp_path, different=False)
    original = comparison.as_dict()
    invalid_documents: list[tuple[str, bytes]] = []
    for field in ("$schema", "fingerprint_protocol", "plan_sha256"):
        document = dict(original)
        document[field] = "invalid"
        invalid_documents.append((field, _document(document)))
    for field in ("status", "observation_equal"):
        document = dict(original)
        document[field] = "different" if field == "status" else 1
        invalid_documents.append((field, _document(document)))
    missing = dict(original)
    del missing["status"]
    invalid_documents.append(("comparison", _document(missing)))
    extra = dict(original)
    extra["unexpected"] = 1
    invalid_documents.append(("comparison", _document(extra)))
    delta_missing = dict(cast(dict[str, object], original["deltas"]))
    del delta_missing["cas_blobs"]
    missing_delta_document = dict(original)
    missing_delta_document["deltas"] = delta_missing
    invalid_documents.append(("deltas", _document(missing_delta_document)))
    for value in (True, 1.0, 1 << 63):
        invalid_delta_document = dict(original)
        deltas = dict(cast(dict[str, object], original["deltas"]))
        deltas["cas_blobs"] = value
        invalid_delta_document["deltas"] = deltas
        invalid_documents.append(("cas_blobs", _document(invalid_delta_document)))

    for field, document in invalid_documents:
        with pytest.raises(AssetCacheError) as caught:
            decode_asset_cache_fingerprint_comparison(document)
        assert caught.value.code in {
            "asset_cache.invalid_fingerprint_comparison_json",
            "asset_cache.invalid_fingerprint_comparison_record",
        }
        if caught.value.code == "asset_cache.invalid_fingerprint_comparison_record":
            assert dict(caught.value.details) == {"field": field}


def test_decoder_rejects_duplicate_nonfinite_noncanonical_and_invalid_unicode(
    tmp_path: Path,
) -> None:
    _plan, _expected, _current, comparison = _records(tmp_path, different=False)
    canonical = comparison.canonical_bytes()
    duplicate = canonical.replace(
        b'{"$schema":',
        b'{"$schema":"ludoweave.asset-cache-fingerprint-comparison/1","$schema":',
        1,
    )
    nonfinite = canonical.replace(b'"cas_blobs":0', b'"cas_blobs":NaN', 1)

    for document in (duplicate, nonfinite, b"\xff", "\ud800"):
        with pytest.raises(AssetCacheError) as caught:
            decode_asset_cache_fingerprint_comparison(document)
        assert caught.value.code == "asset_cache.invalid_fingerprint_comparison_json"
    with pytest.raises(AssetCacheError) as noncanonical:
        decode_asset_cache_fingerprint_comparison(canonical + b"\n")
    assert noncanonical.value.code == "asset_cache.noncanonical_fingerprint_comparison_record"


def test_decoder_limits_are_exact_and_tightening_only(tmp_path: Path) -> None:
    _plan, _expected, _current, comparison = _records(tmp_path, different=False)
    canonical = comparison.canonical_bytes()
    tightened = AssetCacheFingerprintComparisonRecordLimits(max_bytes=len(canonical))

    assert decode_asset_cache_fingerprint_comparison(canonical, limits=tightened) == comparison
    with pytest.raises(AssetCacheError) as limited:
        decode_asset_cache_fingerprint_comparison(
            canonical,
            limits=AssetCacheFingerprintComparisonRecordLimits(max_bytes=len(canonical) - 1),
        )
    with pytest.raises(AssetCacheError) as widened:
        AssetCacheFingerprintComparisonRecordLimits(
            max_bytes=ASSET_CACHE_FINGERPRINT_COMPARISON_RECORD_MAX_BYTES + 1
        )
    with pytest.raises(AssetCacheError) as boolean:
        AssetCacheFingerprintComparisonRecordLimits(max_bytes=True)  # type: ignore[arg-type]
    with pytest.raises(AssetCacheError) as wrong_type:
        decode_asset_cache_fingerprint_comparison(
            canonical,
            limits=object(),  # type: ignore[arg-type]
        )

    assert limited.value.code == "asset_cache.fingerprint_comparison_limit_exceeded"
    assert widened.value.code == "asset_cache.invalid_fingerprint_comparison_limits"
    assert boolean.value.code == "asset_cache.invalid_fingerprint_comparison_limits"
    assert wrong_type.value.code == "asset_cache.invalid_fingerprint_comparison_limits"


def test_verification_preserves_all_frozen_inputs(tmp_path: Path) -> None:
    plan, expected, current, comparison = _records(tmp_path, different=True)
    before = (plan, expected, current, comparison)

    verify_asset_cache_fingerprint_comparison(plan, expected, current, comparison)

    assert (plan, expected, current, comparison) == before
