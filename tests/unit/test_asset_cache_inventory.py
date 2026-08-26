"""Bounded whole-cache integrity inventory behavior."""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

import pytest

from ludoweave.assets import (
    ASSET_CACHE_INVENTORY_MAX_ACTIONS,
    ASSET_CACHE_INVENTORY_PROTOCOL,
    AssetBuildInput,
    AssetBuildPlan,
    AssetCacheError,
    AssetCacheInventoryLimits,
    AssetEntry,
    AssetKind,
    AssetManifest,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetUri,
    inspect_asset_cache_inventory,
    populate_asset_build_cache,
)


def _hash(payload: bytes) -> str:
    return f"sha256:{sha256(payload).hexdigest()}"


def _fixture(
    root: Path,
    *,
    first_source: bytes = b'{ "z": 2, "a": 1 }',
) -> tuple[AssetBuildPlan, tuple[AssetBuildInput, ...]]:
    root.mkdir(parents=True, exist_ok=True)
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


def _populate(
    root: Path,
    cache: Path,
    *,
    first_source: bytes = b'{ "z": 2, "a": 1 }',
) -> AssetBuildPlan:
    plan, inputs = _fixture(root, first_source=first_source)
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


def test_inventory_reports_absent_cache_without_creation(tmp_path: Path) -> None:
    plan, _inputs = _fixture(tmp_path)
    cache = tmp_path / "absent"

    report = inspect_asset_cache_inventory(plan, cache)

    assert report.protocol == ASSET_CACHE_INVENTORY_PROTOCOL
    assert report.current_actions == 0
    assert report.missing_actions == 2
    assert report.other_actions == 0
    assert report.cas_blobs == 0
    assert report.unreferenced_blobs == 0
    assert not cache.exists()


def test_inventory_verifies_complete_current_cache_without_mutation(tmp_path: Path) -> None:
    cache = tmp_path / "cache"
    plan = _populate(tmp_path, cache)
    before = _files(cache)
    metadata_bytes = sum(
        len(payload) for name, payload in before.items() if name.endswith("entry.json")
    )
    cas_bytes = sum(len(payload) for name, payload in before.items() if name.startswith("cas/"))

    report = inspect_asset_cache_inventory(plan, cache)

    assert report.as_dict() == {
        "$schema": "ludoweave.asset-cache-inventory/1",
        "plan_sha256": _hash(plan.canonical_bytes()),
        "current_actions": 2,
        "missing_actions": 0,
        "other_actions": 0,
        "current_action_metadata_bytes": metadata_bytes,
        "other_action_metadata_bytes": 0,
        "cas_blobs": 2,
        "current_blobs": 2,
        "other_blobs": 0,
        "current_blob_bytes": cas_bytes,
        "other_blob_bytes": 0,
        "unreferenced_blobs": 0,
        "unreferenced_blob_bytes": 0,
    }
    assert json.loads(report.canonical_bytes()) == report.as_dict()
    assert _files(cache) == before


def test_inventory_classifies_other_actions_and_unreferenced_blob(tmp_path: Path) -> None:
    cache = tmp_path / "cache"
    _populate(tmp_path / "old", cache, first_source=b'{"version":1}')
    current = _populate(tmp_path / "current", cache, first_source=b'{"version":2}')
    orphan = b"verified orphan"
    digest = sha256(orphan).hexdigest()
    orphan_path = cache / "cas" / digest[:2] / digest
    orphan_path.parent.mkdir(exist_ok=True)
    orphan_path.write_bytes(orphan)
    before = _files(cache)

    report = inspect_asset_cache_inventory(current, cache)

    assert (report.current_actions, report.missing_actions, report.other_actions) == (2, 0, 1)
    assert (report.current_blobs, report.other_blobs) == (2, 2)
    assert report.cas_blobs == 4
    assert report.unreferenced_blobs == 1
    assert report.unreferenced_blob_bytes == len(orphan)
    assert _files(cache) == before


def test_inventory_rejects_unknown_root_member_read_only(tmp_path: Path) -> None:
    cache = tmp_path / "cache"
    plan = _populate(tmp_path, cache)
    (cache / "unknown").write_bytes(b"unexpected")
    before = _files(cache)

    with pytest.raises(AssetCacheError) as caught:
        inspect_asset_cache_inventory(plan, cache)

    assert caught.value.code == "asset_cache.invalid_inventory_layout"
    assert dict(caught.value.details) == {"field": "cache_root"}
    assert _files(cache) == before


def test_inventory_rejects_noncanonical_action_metadata(tmp_path: Path) -> None:
    cache = tmp_path / "cache"
    plan = _populate(tmp_path, cache)
    metadata = sorted(cache.rglob("entry.json"))[0]
    metadata.write_text(json.dumps(json.loads(metadata.read_bytes()), indent=2), encoding="utf-8")
    before = _files(cache)

    with pytest.raises(AssetCacheError) as caught:
        inspect_asset_cache_inventory(plan, cache)

    assert caught.value.code == "asset_cache.corrupt_inventory"
    assert dict(caught.value.details) == {"field": "metadata"}
    assert _files(cache) == before


def test_inventory_hashes_and_rejects_corrupt_unreferenced_blob(tmp_path: Path) -> None:
    cache = tmp_path / "cache"
    plan = _populate(tmp_path, cache)
    claimed = sha256(b"claimed").hexdigest()
    blob = cache / "cas" / claimed[:2] / claimed
    blob.parent.mkdir(exist_ok=True)
    blob.write_bytes(b"different")
    before = _files(cache)

    with pytest.raises(AssetCacheError) as caught:
        inspect_asset_cache_inventory(plan, cache)

    assert caught.value.code == "asset_cache.corrupt_inventory"
    assert dict(caught.value.details) == {"field": "cas_digest"}
    assert _files(cache) == before


def test_inventory_rejects_action_without_referenced_blob(tmp_path: Path) -> None:
    cache = tmp_path / "cache"
    plan = _populate(tmp_path, cache)
    blob = sorted(path for path in (cache / "cas").rglob("*") if path.is_file())[0]
    blob.unlink()
    before = _files(cache)

    with pytest.raises(AssetCacheError) as caught:
        inspect_asset_cache_inventory(plan, cache)

    assert caught.value.code == "asset_cache.corrupt_inventory"
    assert dict(caught.value.details) == {"field": "action_blob"}
    assert _files(cache) == before


def test_inventory_enforces_tightened_action_and_byte_limits(tmp_path: Path) -> None:
    cache = tmp_path / "cache"
    plan = _populate(tmp_path, cache)

    with pytest.raises(AssetCacheError) as actions_caught:
        inspect_asset_cache_inventory(
            plan,
            cache,
            limits=AssetCacheInventoryLimits(max_actions=1),
        )
    with pytest.raises(AssetCacheError) as bytes_caught:
        inspect_asset_cache_inventory(
            plan,
            cache,
            limits=AssetCacheInventoryLimits(max_cas_bytes=1),
        )

    assert actions_caught.value.code == "asset_cache.inventory_limit_exceeded"
    assert dict(actions_caught.value.details)["field"] == "actions"
    assert bytes_caught.value.code == "asset_cache.inventory_limit_exceeded"
    assert dict(bytes_caught.value.details)["field"] == "cas_bytes"


def test_inventory_rejects_cas_budget_before_blob_open(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cache = tmp_path / "cache"
    plan = _populate(tmp_path, cache)
    original = Path.open
    cas_opens = 0

    def observe(self: Path, *args: object, **kwargs: object) -> object:
        nonlocal cas_opens
        if "cas" in self.parts:
            cas_opens += 1
        return original(self, *args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(Path, "open", observe)
    with pytest.raises(AssetCacheError) as caught:
        inspect_asset_cache_inventory(
            plan,
            cache,
            limits=AssetCacheInventoryLimits(max_cas_bytes=1),
        )

    assert caught.value.code == "asset_cache.inventory_limit_exceeded"
    assert dict(caught.value.details)["field"] == "cas_bytes"
    assert cas_opens == 0


@pytest.mark.parametrize("value", [0, True, ASSET_CACHE_INVENTORY_MAX_ACTIONS + 1])
def test_inventory_limits_require_tightening_positive_integers(value: object) -> None:
    with pytest.raises(AssetCacheError) as caught:
        AssetCacheInventoryLimits(max_actions=value)  # type: ignore[arg-type]

    assert caught.value.code == "asset_cache.invalid_inventory_limits"


def test_inventory_rejects_current_action_identity_mismatch_content_silently(
    tmp_path: Path,
) -> None:
    cache = tmp_path / "cache"
    plan = _populate(tmp_path, cache)
    metadata = sorted(cache.rglob("entry.json"))[0]
    document = json.loads(metadata.read_bytes())
    assert type(document) is dict
    document["uri"] = "asset://data/other.json"
    metadata.write_text(
        json.dumps(document, ensure_ascii=False, separators=(",", ":"), sort_keys=True),
        encoding="utf-8",
    )

    with pytest.raises(AssetCacheError) as caught:
        inspect_asset_cache_inventory(plan, cache)

    assert caught.value.code == "asset_cache.corrupt_inventory"
    assert dict(caught.value.details) == {"field": "current_action"}
    assert plan.entries[0].cache_key not in str(caught.value.as_dict())
