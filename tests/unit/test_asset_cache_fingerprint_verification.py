"""Strict saved fingerprint decoding and current-cache verification."""

from __future__ import annotations

import json
from collections.abc import Callable
from hashlib import sha256
from pathlib import Path

import pytest

import ludoweave.assets.fingerprint_verification as verification_module
from ludoweave.assets import (
    ASSET_CACHE_FINGERPRINT_VERIFICATION_PROTOCOL,
    AssetBuildInput,
    AssetBuildPlan,
    AssetCacheError,
    AssetCacheFingerprintRecordLimits,
    AssetEntry,
    AssetKind,
    AssetManifest,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetUri,
    decode_asset_cache_fingerprint,
    fingerprint_asset_cache_observation,
    populate_asset_build_cache,
    verify_asset_cache_fingerprint,
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


def _saved(plan: AssetBuildPlan, cache: Path) -> bytes:
    return fingerprint_asset_cache_observation(plan, cache).canonical_bytes()


def _duplicate_plan_digest(raw: bytes) -> bytes:
    return raw.replace(
        b'"plan_sha256":',
        b'"plan_sha256":"duplicate","plan_sha256":',
        1,
    )


def _nonfinite_count(raw: bytes) -> bytes:
    return raw.replace(b'"current_actions":1', b'"current_actions":NaN', 1)


def _boolean_count(raw: bytes) -> bytes:
    return raw.replace(b'"current_actions":1', b'"current_actions":true', 1)


def _extra_field(raw: bytes) -> bytes:
    return raw.replace(b'{"$schema":', b'{"extra":0,"$schema":', 1)


def _oversized_missing_count(raw: bytes) -> bytes:
    return raw.replace(b'"missing_actions":0', b'"missing_actions":16385', 1)


_INVALID_DOCUMENTS: tuple[tuple[Callable[[bytes], bytes], str], ...] = (
    (_duplicate_plan_digest, "asset_cache.invalid_fingerprint_json"),
    (_nonfinite_count, "asset_cache.invalid_fingerprint_json"),
    (_boolean_count, "asset_cache.invalid_fingerprint_record"),
    (_extra_field, "asset_cache.invalid_fingerprint_record"),
    (_oversized_missing_count, "asset_cache.invalid_fingerprint_record"),
)


def test_fingerprint_record_decodes_exact_m138_canonical_bytes(tmp_path: Path) -> None:
    plan, cache = _population(tmp_path)
    document = _saved(plan, cache)

    record = decode_asset_cache_fingerprint(document)

    assert record.canonical_bytes() == document


def test_fingerprint_record_rejects_noncanonical_layout(tmp_path: Path) -> None:
    plan, cache = _population(tmp_path)
    document = json.dumps(json.loads(_saved(plan, cache)), indent=2)

    with pytest.raises(AssetCacheError) as caught:
        decode_asset_cache_fingerprint(document)

    assert caught.value.code == "asset_cache.noncanonical_fingerprint_record"
    assert dict(caught.value.details) == {"field": "document"}


@pytest.mark.parametrize(
    ("transform", "code"),
    _INVALID_DOCUMENTS,
)
def test_fingerprint_record_rejects_ambiguous_or_invalid_json_values(
    tmp_path: Path,
    transform: Callable[[bytes], bytes],
    code: str,
) -> None:
    plan, cache = _population(tmp_path)

    with pytest.raises(AssetCacheError) as caught:
        decode_asset_cache_fingerprint(transform(_saved(plan, cache)))

    assert caught.value.code == code


def test_fingerprint_record_enforces_tightened_byte_limit(tmp_path: Path) -> None:
    plan, cache = _population(tmp_path)
    document = _saved(plan, cache)

    with pytest.raises(AssetCacheError) as caught:
        decode_asset_cache_fingerprint(
            document,
            limits=AssetCacheFingerprintRecordLimits(max_bytes=len(document) - 1),
        )

    assert caught.value.code == "asset_cache.fingerprint_limit_exceeded"


def test_saved_fingerprint_verifies_one_current_observation_read_only(tmp_path: Path) -> None:
    plan, cache = _population(tmp_path)
    record = decode_asset_cache_fingerprint(_saved(plan, cache))
    before = _files(cache)

    report = verify_asset_cache_fingerprint(plan, record, cache)

    assert report.protocol == ASSET_CACHE_FINGERPRINT_VERIFICATION_PROTOCOL
    assert report.as_dict() == {
        "$schema": "ludoweave.asset-cache-fingerprint-verification/1",
        "status": "valid",
        "fingerprint_protocol": "ludoweave.asset-cache-fingerprint/1",
        "plan_sha256": record.inventory.plan_sha256,
        "observation_sha256": record.observation_sha256,
    }
    assert _files(cache) == before


def test_plan_mismatch_precedes_cache_observation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan, cache = _population(tmp_path)
    record = decode_asset_cache_fingerprint(_saved(plan, cache))
    changed_plan, _inputs = _fixture(tmp_path / "changed", b'{"value":2}')
    calls = 0

    def observe(*args: object, **kwargs: object) -> object:
        nonlocal calls
        del args, kwargs
        calls += 1
        raise AssertionError("cache observation must not start")

    monkeypatch.setattr(verification_module, "fingerprint_asset_cache_observation", observe)
    with pytest.raises(AssetCacheError) as caught:
        verify_asset_cache_fingerprint(changed_plan, record, cache)

    assert caught.value.code == "asset_cache.fingerprint_mismatch"
    assert dict(caught.value.details) == {"field": "plan_sha256"}
    assert calls == 0


def test_absent_cache_fingerprint_verifies_without_creation(tmp_path: Path) -> None:
    plan, _inputs = _fixture(tmp_path / "project", b'{"value":1}')
    cache = tmp_path / "absent"
    record = decode_asset_cache_fingerprint(_saved(plan, cache))

    report = verify_asset_cache_fingerprint(plan, record, cache)

    assert report.observation_sha256 == record.observation_sha256
    assert not cache.exists()


def test_equal_inventory_with_substituted_content_fails_on_digest(tmp_path: Path) -> None:
    plan, cache = _population(tmp_path)
    first = b"first orphan"
    second = b"other orphan"
    assert len(first) == len(second)
    first_digest = sha256(first).hexdigest()
    first_path = cache / "cas" / first_digest[:2] / first_digest
    first_path.parent.mkdir(exist_ok=True)
    first_path.write_bytes(first)
    record = decode_asset_cache_fingerprint(_saved(plan, cache))
    first_path.unlink()
    first_path.parent.rmdir()
    second_digest = sha256(second).hexdigest()
    second_path = cache / "cas" / second_digest[:2] / second_digest
    second_path.parent.mkdir(exist_ok=True)
    second_path.write_bytes(second)
    current = fingerprint_asset_cache_observation(plan, cache)
    assert current.inventory == record.inventory

    with pytest.raises(AssetCacheError) as caught:
        verify_asset_cache_fingerprint(plan, record, cache)

    assert caught.value.code == "asset_cache.fingerprint_mismatch"
    assert dict(caught.value.details) == {"field": "observation_sha256"}
    assert record.observation_sha256 not in str(caught.value.as_dict())
    assert current.observation_sha256 not in str(caught.value.as_dict())


def test_changed_cache_inventory_fails_content_silently(tmp_path: Path) -> None:
    plan, cache = _population(tmp_path)
    record = decode_asset_cache_fingerprint(_saved(plan, cache))
    orphan = b"new orphan"
    digest = sha256(orphan).hexdigest()
    path = cache / "cas" / digest[:2] / digest
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(orphan)

    with pytest.raises(AssetCacheError) as caught:
        verify_asset_cache_fingerprint(plan, record, cache)

    assert caught.value.code == "asset_cache.fingerprint_mismatch"
    assert dict(caught.value.details) == {"field": "inventory"}
    assert digest not in str(caught.value.as_dict())


def test_corrupt_cache_fails_without_repair(tmp_path: Path) -> None:
    plan, cache = _population(tmp_path)
    record = decode_asset_cache_fingerprint(_saved(plan, cache))
    metadata = next(cache.rglob("entry.json"))
    metadata.write_bytes(b"{}")
    before = _files(cache)

    with pytest.raises(AssetCacheError) as caught:
        verify_asset_cache_fingerprint(plan, record, cache)

    assert caught.value.code == "asset_cache.corrupt_inventory"
    assert _files(cache) == before
