"""Bounded immutable identities for selected asset source bytes."""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.assets import (
    ASSET_SOURCE_LOCK_PROTOCOL,
    AssetError,
    AssetKind,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetSourceLockLimits,
    AssetUri,
)

_SOURCE_LOCK = "sha256:" + "1" * 64
_ASSET_MANIFEST = "sha256:" + "2" * 64


def _entry(
    uri: str = "asset://textures/player.png",
    *,
    kind: AssetKind = AssetKind.PNG,
    source_hash: str = "sha256:" + "3" * 64,
    source_bytes: int = 17,
) -> AssetSourceLockEntry:
    return AssetSourceLockEntry(AssetUri(uri), kind, source_hash, source_bytes)


def _lock() -> AssetSourceLock:
    texture = _entry()
    material = _entry(
        "asset://materials/player.json",
        kind=AssetKind.JSON,
        source_hash="sha256:" + "4" * 64,
        source_bytes=23,
    )
    return AssetSourceLock(
        _SOURCE_LOCK,
        _ASSET_MANIFEST,
        (texture.uri,),
        (texture, material),
    )


def test_asset_source_lock_normalizes_and_round_trips_canonical_bytes() -> None:
    original = _lock()
    reversed_lock = AssetSourceLock(
        original.source_lock_sha256,
        original.asset_manifest_sha256,
        tuple(reversed(original.roots)),
        tuple(reversed(original.entries)),
    )

    assert reversed_lock == original
    assert AssetSourceLock.from_json(original.canonical_bytes()) == original
    assert json.loads(original.canonical_bytes()) == original.as_dict()
    assert original.protocol == ASSET_SOURCE_LOCK_PROTOCOL
    assert tuple(entry.uri for entry in original.entries) == tuple(
        sorted(entry.uri for entry in original.entries)
    )


def test_asset_source_lock_accepts_empty_selected_closure() -> None:
    lock = AssetSourceLock(_SOURCE_LOCK, _ASSET_MANIFEST, (), ())

    assert AssetSourceLock.from_json(lock.canonical_bytes()) == lock
    assert lock.roots == ()
    assert lock.entries == ()


@pytest.mark.parametrize(
    "value",
    (
        {"$schema": "ludoweave.asset-source-lock/2"},
        {"$schema": ASSET_SOURCE_LOCK_PROTOCOL, "extra": True},
        [],
    ),
)
def test_asset_source_lock_rejects_nonexact_documents(value: object) -> None:
    with pytest.raises(AssetError):
        AssetSourceLock.from_json(json.dumps(value))


def test_asset_source_lock_rejects_duplicate_json_fields_and_oversized_input() -> None:
    duplicate = (
        _lock()
        .canonical_bytes()
        .replace(b'{"$schema":', b'{"$schema":"ludoweave.asset-source-lock/1","$schema":', 1)
    )
    with pytest.raises(AssetError) as repeated:
        AssetSourceLock.from_json(duplicate)
    assert repeated.value.code == "asset_source_lock.invalid_json"

    with pytest.raises(AssetError) as oversized:
        AssetSourceLock.from_json(
            b" " * 65 + b"{}",
            limits=AssetSourceLockLimits(max_bytes=64),
        )
    assert oversized.value.code == "asset_source_lock.limit_exceeded"


def test_asset_source_lock_rejects_repeated_or_missing_roots_and_entries() -> None:
    entry = _entry()
    with pytest.raises(AssetError) as repeated_root:
        AssetSourceLock(_SOURCE_LOCK, _ASSET_MANIFEST, (entry.uri, entry.uri), (entry,))
    assert repeated_root.value.code == "asset_source_lock.invalid_roots"

    with pytest.raises(AssetError) as missing_root:
        AssetSourceLock(
            _SOURCE_LOCK,
            _ASSET_MANIFEST,
            (AssetUri("asset://missing/item.json"),),
            (entry,),
        )
    assert missing_root.value.code == "asset_source_lock.unknown_root"

    with pytest.raises(AssetError) as repeated_entry:
        AssetSourceLock(_SOURCE_LOCK, _ASSET_MANIFEST, (entry.uri,), (entry, entry))
    assert repeated_entry.value.code == "asset_source_lock.duplicate_uri"


@given(
    st.one_of(
        st.integers(max_value=-1),
        st.integers(min_value=268_435_457, max_value=2**40),
        st.booleans(),
    )
)
def test_asset_source_lock_entry_rejects_invalid_source_byte_counts(value: int) -> None:
    with pytest.raises(AssetError) as raised:
        _entry(source_bytes=value)

    assert raised.value.code == "asset_source_lock.invalid_entry"


@pytest.mark.parametrize(
    ("changed", "field"),
    (
        ({"source_lock_sha256": "sha256:" + "a" * 64}, "source_lock_sha256"),
        (
            {"asset_manifest_sha256": "sha256:" + "b" * 64},
            "asset_manifest_sha256",
        ),
    ),
)
def test_asset_source_lock_verification_uses_stable_content_silent_precedence(
    changed: dict[str, object],
    field: str,
) -> None:
    expected = _lock()
    values: dict[str, object] = {
        "source_lock_sha256": expected.source_lock_sha256,
        "asset_manifest_sha256": expected.asset_manifest_sha256,
        "roots": expected.roots,
        "entries": expected.entries,
    }
    values.update(changed)
    actual = AssetSourceLock(**values)  # type: ignore[arg-type]

    with pytest.raises(AssetError) as raised:
        expected.verify(actual)

    details = dict(raised.value.details)
    assert raised.value.code == "asset_source_lock.mismatch"
    assert details == {"field": field}
    serialized = str(raised.value.as_dict())
    assert "a" * 64 not in serialized
    assert "b" * 64 not in serialized


def test_asset_source_lock_verification_detects_valid_root_and_entry_set_drift() -> None:
    expected = _lock()
    changed_roots = AssetSourceLock(
        expected.source_lock_sha256,
        expected.asset_manifest_sha256,
        (AssetUri("asset://materials/player.json"),),
        expected.entries,
    )
    with pytest.raises(AssetError) as roots_error:
        expected.verify(changed_roots)
    assert dict(roots_error.value.details) == {"field": "roots"}

    changed_entries = AssetSourceLock(
        expected.source_lock_sha256,
        expected.asset_manifest_sha256,
        expected.roots,
        (expected.entries[1],),
    )
    with pytest.raises(AssetError) as entries_error:
        expected.verify(changed_entries)
    assert dict(entries_error.value.details) == {"field": "entries"}


def test_asset_source_lock_verification_reports_first_changed_entry_field() -> None:
    expected = _lock()
    changed_entry = _entry(
        "asset://materials/player.json",
        kind=AssetKind.JSON,
        source_hash="sha256:" + "9" * 64,
        source_bytes=23,
    )
    actual = AssetSourceLock(
        expected.source_lock_sha256,
        expected.asset_manifest_sha256,
        expected.roots,
        (changed_entry, expected.entries[1]),
    )

    with pytest.raises(AssetError) as raised:
        expected.verify(actual)

    assert dict(raised.value.details) == {
        "field": "source_sha256",
        "uri": "asset://materials/player.json",
    }


def test_asset_source_lock_limits_are_frozen_slotted_and_tightening_only() -> None:
    limits = AssetSourceLockLimits(max_bytes=64, max_entries=2, max_roots=1)
    assert not hasattr(limits, "__dict__")
    with pytest.raises(FrozenInstanceError):
        limits.max_bytes = 32  # type: ignore[misc]

    for invalid in (
        lambda: AssetSourceLockLimits(max_bytes=0),
        lambda: AssetSourceLockLimits(max_entries=True),
        lambda: AssetSourceLockLimits(max_roots=4_097),
    ):
        with pytest.raises(AssetError) as raised:
            invalid()
        assert raised.value.code == "asset_source_lock.invalid_limits"
