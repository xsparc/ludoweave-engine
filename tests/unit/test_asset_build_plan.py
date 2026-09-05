"""Pure deterministic planning for verified selected asset inputs."""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from hashlib import sha256
from pathlib import Path

import pytest

from ludoweave.assets import (
    ASSET_BUILD_PLAN_PROTOCOL,
    ASSET_LOADER_PROTOCOL,
    AssetBuildPlan,
    AssetBuildPlanLimits,
    AssetEntry,
    AssetError,
    AssetKind,
    AssetManifest,
    AssetPipeline,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetUri,
)


def _uri(value: str) -> AssetUri:
    return AssetUri(f"asset://{value}")


def _manifest(root: Path, *, reversed_entries: bool = False) -> AssetManifest:
    independent = AssetEntry(_uri("a/independent.json"), AssetKind.JSON, "assets/independent.json")
    dependency = AssetEntry(_uri("z/dependency.json"), AssetKind.JSON, "assets/dependency.json")
    consumer = AssetEntry(
        _uri("z/root.json"),
        AssetKind.JSON,
        "assets/root.json",
        settings=(("mode", "strict"),),
        dependencies=(dependency.uri,),
    )
    values = (consumer, dependency, independent)
    return AssetManifest(root, tuple(reversed(values)) if reversed_entries else values)


def _lock(manifest: AssetManifest) -> AssetSourceLock:
    content = {
        _uri("a/independent.json"): b'{"value":1}',
        _uri("z/dependency.json"): b'{"value":2}',
        _uri("z/root.json"): b'{"value":3}',
    }
    entries = tuple(
        AssetSourceLockEntry(
            uri,
            manifest.entry(uri).kind,
            f"sha256:{sha256(source).hexdigest()}",
            len(source),
        )
        for uri, source in sorted(content.items())
    )
    return AssetSourceLock(
        "sha256:" + "1" * 64,
        f"sha256:{sha256(manifest.canonical_bytes()).hexdigest()}",
        (_uri("z/root.json"), _uri("a/independent.json")),
        entries,
    )


def test_asset_build_plan_is_dependency_first_canonical_and_order_independent(
    tmp_path: Path,
) -> None:
    manifest = _manifest(tmp_path)
    lock = _lock(manifest)

    plan = AssetBuildPlan.from_inputs(manifest, lock)
    reversed_plan = AssetBuildPlan.from_inputs(
        _manifest(tmp_path, reversed_entries=True),
        lock,
    )

    assert plan == reversed_plan
    assert plan.protocol == ASSET_BUILD_PLAN_PROTOCOL
    assert plan.loader_protocol == ASSET_LOADER_PROTOCOL
    assert [entry.uri.value for entry in plan.entries] == [
        "asset://a/independent.json",
        "asset://z/dependency.json",
        "asset://z/root.json",
    ]
    assert plan.entries[-1].dependencies == (_uri("z/dependency.json"),)
    assert plan.asset_source_lock_sha256 == (f"sha256:{sha256(lock.canonical_bytes()).hexdigest()}")
    assert AssetBuildPlan.from_json(plan.canonical_bytes()) == plan
    assert json.loads(plan.canonical_bytes()) == plan.as_dict()


def test_asset_build_plan_cache_keys_match_existing_pipeline_exactly(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path)
    sources = {
        "independent.json": b'{"value":1}',
        "dependency.json": b'{"value":2}',
        "root.json": b'{"value":3}',
    }
    directory = tmp_path / "assets"
    directory.mkdir()
    for name, source in sources.items():
        (directory / name).write_bytes(source)
    plan = AssetBuildPlan.from_inputs(manifest, _lock(manifest))

    pipeline = AssetPipeline(manifest, tmp_path.parent / f"{tmp_path.name}-cache")
    built = {
        artifact.uri: artifact.cache_key
        for artifact in (pipeline.build(entry.uri) for entry in plan.entries)
    }

    assert {entry.uri: entry.cache_key for entry in plan.entries} == built


def test_asset_build_plan_accepts_empty_verified_closure(tmp_path: Path) -> None:
    manifest = AssetManifest(tmp_path, ())
    lock = AssetSourceLock(
        "sha256:" + "1" * 64,
        f"sha256:{sha256(manifest.canonical_bytes()).hexdigest()}",
        (),
        (),
    )

    plan = AssetBuildPlan.from_inputs(manifest, lock)

    assert plan.roots == ()
    assert plan.entries == ()
    assert AssetBuildPlan.from_json(plan.canonical_bytes()) == plan


def test_asset_build_plan_orders_deep_graph_iteratively(tmp_path: Path) -> None:
    uris = tuple(_uri(f"deep/item-{index:04}.json") for index in range(1_100))
    manifest = AssetManifest(
        tmp_path,
        tuple(
            AssetEntry(
                uri,
                AssetKind.JSON,
                f"assets/item-{index:04}.json",
                dependencies=() if index == len(uris) - 1 else (uris[index + 1],),
            )
            for index, uri in enumerate(uris)
        ),
    )
    entries = tuple(
        AssetSourceLockEntry(uri, AssetKind.JSON, "sha256:" + "3" * 64, 0) for uri in uris
    )
    lock = AssetSourceLock(
        "sha256:" + "1" * 64,
        f"sha256:{sha256(manifest.canonical_bytes()).hexdigest()}",
        (uris[0],),
        entries,
    )

    plan = AssetBuildPlan.from_inputs(manifest, lock)

    assert tuple(entry.uri for entry in plan.entries) == tuple(reversed(uris))


def test_asset_build_plan_rejects_manifest_closure_or_kind_disagreement(
    tmp_path: Path,
) -> None:
    manifest = _manifest(tmp_path)
    lock = _lock(manifest)
    extra = AssetSourceLockEntry(
        _uri("unused/item.json"),
        AssetKind.JSON,
        "sha256:" + "9" * 64,
        0,
    )
    with pytest.raises(AssetError) as wrong_manifest:
        AssetBuildPlan.from_inputs(
            manifest,
            AssetSourceLock(
                lock.source_lock_sha256,
                "sha256:" + "8" * 64,
                lock.roots,
                lock.entries,
            ),
        )
    assert wrong_manifest.value.code == "asset_build_plan.input_mismatch"
    assert wrong_manifest.value.details == (("field", "asset_manifest_sha256"),)

    with pytest.raises(AssetError) as extra_entry:
        AssetBuildPlan.from_inputs(
            AssetManifest(
                tmp_path,
                (*manifest.entries, AssetEntry(extra.uri, extra.kind, "assets/unused.json")),
            ),
            AssetSourceLock(
                lock.source_lock_sha256,
                f"sha256:{sha256(AssetManifest(tmp_path, (*manifest.entries, AssetEntry(extra.uri, extra.kind, 'assets/unused.json'))).canonical_bytes()).hexdigest()}",
                lock.roots,
                (*lock.entries, extra),
            ),
        )
    assert extra_entry.value.code == "asset_build_plan.input_mismatch"
    assert extra_entry.value.details == (("field", "entries"),)

    changed = tuple(
        AssetSourceLockEntry(
            entry.uri,
            AssetKind.AUDIO if entry.uri == _uri("z/root.json") else entry.kind,
            entry.source_sha256,
            entry.source_bytes,
        )
        for entry in lock.entries
    )
    with pytest.raises(AssetError) as wrong_kind:
        AssetBuildPlan.from_inputs(
            manifest,
            AssetSourceLock(
                lock.source_lock_sha256,
                lock.asset_manifest_sha256,
                lock.roots,
                changed,
            ),
        )
    assert wrong_kind.value.code == "asset_build_plan.input_mismatch"
    assert wrong_kind.value.details == (
        ("field", "kind"),
        ("uri", "asset://z/root.json"),
    )


def test_asset_build_plan_decoder_rejects_reordered_dependencies_and_extra_fields(
    tmp_path: Path,
) -> None:
    plan = AssetBuildPlan.from_inputs(_manifest(tmp_path), _lock(_manifest(tmp_path)))
    document = plan.as_dict()
    entries = list(reversed(document["entries"]))  # type: ignore[arg-type]
    reordered = {**document, "entries": entries}
    with pytest.raises(AssetError) as order:
        AssetBuildPlan.from_json(json.dumps(reordered))
    assert order.value.code == "asset_build_plan.invalid_order"

    same_level = plan.as_dict()
    same_level_entries = list(same_level["entries"])  # type: ignore[arg-type]
    same_level_entries[0], same_level_entries[1] = (
        same_level_entries[1],
        same_level_entries[0],
    )
    with pytest.raises(AssetError) as tie_break:
        AssetBuildPlan.from_json(json.dumps({**same_level, "entries": same_level_entries}))
    assert tie_break.value.code == "asset_build_plan.invalid_order"

    with pytest.raises(AssetError):
        AssetBuildPlan.from_json(json.dumps({**document, "extra": True}))


def test_asset_build_plan_limits_are_frozen_slotted_and_tightening_only() -> None:
    limits = AssetBuildPlanLimits(max_bytes=512, max_entries=2, max_roots=1)
    assert not hasattr(limits, "__dict__")
    with pytest.raises(FrozenInstanceError):
        limits.max_bytes = 256  # type: ignore[misc]

    for invalid in (
        lambda: AssetBuildPlanLimits(max_bytes=0),
        lambda: AssetBuildPlanLimits(max_entries=True),
        lambda: AssetBuildPlanLimits(max_roots=4_097),
    ):
        with pytest.raises(AssetError) as raised:
            invalid()
        assert raised.value.code == "asset_build_plan.invalid_limits"
