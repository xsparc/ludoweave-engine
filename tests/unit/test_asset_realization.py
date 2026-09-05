"""Read-only cache-assisted realization of verified asset plans."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

import ludoweave.assets.execution as asset_execution
from ludoweave.assets import (
    ASSET_BUILD_REALIZATION_PROTOCOL,
    AssetBuildExecutionLimits,
    AssetBuildInput,
    AssetBuildMaterialization,
    AssetBuildPlan,
    AssetBuildResult,
    AssetCacheError,
    AssetCacheStore,
    AssetEntry,
    AssetError,
    AssetKind,
    AssetManifest,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetUri,
    materialize_asset_build_plan,
    realize_asset_build_plan,
)


def _hash(payload: bytes) -> str:
    return f"sha256:{sha256(payload).hexdigest()}"


def _fixture(root: Path) -> tuple[AssetBuildPlan, tuple[AssetBuildInput, ...]]:
    json_uri = AssetUri("asset://data/config.json")
    shader_uri = AssetUri("asset://shaders/main.wgsl")
    sources = {
        json_uri: b'{ "z": 2, "a": 1 }',
        shader_uri: b"@vertex fn main() -> @builtin(position) vec4f { return vec4f(); }",
    }
    manifest = AssetManifest(
        root,
        (
            AssetEntry(json_uri, AssetKind.JSON, "assets/config.json"),
            AssetEntry(shader_uri, AssetKind.WGSL, "assets/main.wgsl"),
        ),
    )
    lock = AssetSourceLock(
        source_lock_sha256=_hash(b"source-lock"),
        asset_manifest_sha256=_hash(manifest.canonical_bytes()),
        roots=(json_uri, shader_uri),
        entries=tuple(
            AssetSourceLockEntry(uri, manifest.entry(uri).kind, _hash(source), len(source))
            for uri, source in sources.items()
        ),
    )
    plan = AssetBuildPlan.from_inputs(manifest, lock)
    return plan, tuple(AssetBuildInput(entry.uri, sources[entry.uri]) for entry in plan.entries)


def _partial(materialized: AssetBuildMaterialization, index: int) -> AssetBuildMaterialization:
    artifact = materialized.artifacts[index]
    return AssetBuildMaterialization(
        AssetBuildResult(
            plan_sha256=materialized.result.plan_sha256,
            source_bytes=artifact.entry.source_bytes,
            artifact_bytes=artifact.entry.artifact_bytes,
            entries=(artifact.entry,),
        ),
        (artifact,),
    )


def _files(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_all_misses_match_uncached_materialization_without_creating_cache(tmp_path: Path) -> None:
    plan, inputs = _fixture(tmp_path)
    cache = tmp_path / "absent-cache"

    realized = realize_asset_build_plan(
        plan,
        inputs,
        AssetCacheStore(cache, writable=False),
    )

    assert realized.protocol == ASSET_BUILD_REALIZATION_PROTOCOL
    assert realized.materialization == materialize_asset_build_plan(plan, inputs)
    assert realized.hits == 0
    assert realized.decoded == 2
    assert [entry.status for entry in realized.entries] == ["decoded", "decoded"]
    assert not cache.exists()


def test_all_hits_bypass_decoders_and_leave_cache_unchanged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plan, inputs = _fixture(tmp_path)
    cache = tmp_path / "cache"
    expected = materialize_asset_build_plan(plan, inputs)
    AssetCacheStore(cache).publish(expected)
    before = _files(cache)

    def reject_decode(kind: AssetKind, source: bytes) -> bytes:
        raise AssertionError((kind, source))

    monkeypatch.setattr(asset_execution, "_decode_payload", reject_decode)
    realized = realize_asset_build_plan(
        plan,
        inputs,
        AssetCacheStore(cache, writable=False),
    )

    assert realized.materialization == expected
    assert realized.hits == 2
    assert realized.decoded == 0
    assert _files(cache) == before


def test_mixed_hits_and_misses_preserve_plan_order(tmp_path: Path) -> None:
    plan, inputs = _fixture(tmp_path)
    expected = materialize_asset_build_plan(plan, inputs)
    cache = tmp_path / "cache"
    AssetCacheStore(cache).publish(_partial(expected, 1))

    realized = realize_asset_build_plan(
        plan,
        inputs,
        AssetCacheStore(cache, writable=False),
    )

    assert realized.materialization == expected
    assert tuple(entry.result.uri for entry in realized.entries) == tuple(
        entry.uri for entry in plan.entries
    )
    assert [entry.status for entry in realized.entries] == ["decoded", "hit"]


def test_complete_source_preflight_precedes_every_cache_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plan, inputs = _fixture(tmp_path)
    changed = (*inputs[:-1], AssetBuildInput(inputs[-1].uri, b"changed"))
    calls = 0
    original = AssetCacheStore.load_action

    def observe(self: AssetCacheStore, entry: object) -> object:
        nonlocal calls
        calls += 1
        return original(self, entry)  # type: ignore[arg-type]

    monkeypatch.setattr(AssetCacheStore, "load_action", observe)
    with pytest.raises(AssetError) as caught:
        realize_asset_build_plan(
            plan,
            changed,
            AssetCacheStore(tmp_path / "cache", writable=False),
        )

    assert caught.value.code == "asset_build.input_mismatch"
    assert calls == 0


def test_every_cache_candidate_is_verified_before_any_miss_decode(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plan, inputs = _fixture(tmp_path)
    expected = materialize_asset_build_plan(plan, inputs)
    cache = tmp_path / "cache"
    AssetCacheStore(cache).publish(_partial(expected, 1))
    action = plan.entries[1].cache_key.removeprefix("sha256:")
    metadata = cache / "actions" / action[:2] / action / "entry.json"
    metadata.write_bytes(b"{}")
    calls = 0

    def observe(kind: AssetKind, source: bytes) -> bytes:
        nonlocal calls
        calls += 1
        return source

    monkeypatch.setattr(asset_execution, "_decode_payload", observe)
    with pytest.raises(AssetCacheError) as caught:
        realize_asset_build_plan(plan, inputs, AssetCacheStore(cache, writable=False))

    assert caught.value.code == "asset_cache.corrupt_entry"
    assert calls == 0


def test_cached_artifacts_obey_tightened_aggregate_limit_before_decode(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plan, inputs = _fixture(tmp_path)
    expected = materialize_asset_build_plan(plan, inputs)
    cache = tmp_path / "cache"
    AssetCacheStore(cache).publish(expected)

    def reject_decode(kind: AssetKind, source: bytes) -> bytes:
        raise AssertionError((kind, source))

    monkeypatch.setattr(asset_execution, "_decode_payload", reject_decode)
    limits = AssetBuildExecutionLimits(max_total_artifact_bytes=expected.result.artifact_bytes - 1)
    with pytest.raises(AssetError) as caught:
        realize_asset_build_plan(
            plan,
            inputs,
            AssetCacheStore(cache, writable=False),
            limits=limits,
        )

    assert caught.value.code == "asset_build.limit_exceeded"
    assert dict(caught.value.details)["field"] == "total_artifact_bytes"


def test_mixed_aggregate_limit_failure_matches_uncached_plan_order(tmp_path: Path) -> None:
    plan, inputs = _fixture(tmp_path)
    expected = materialize_asset_build_plan(plan, inputs)
    cache = tmp_path / "cache"
    AssetCacheStore(cache).publish(_partial(expected, 1))
    limits = AssetBuildExecutionLimits(max_total_artifact_bytes=expected.result.artifact_bytes - 1)

    with pytest.raises(AssetError) as uncached:
        materialize_asset_build_plan(plan, inputs, limits=limits)
    with pytest.raises(AssetError) as cached:
        realize_asset_build_plan(
            plan,
            inputs,
            AssetCacheStore(cache, writable=False),
            limits=limits,
        )

    assert cached.value.code == uncached.value.code == "asset_build.limit_exceeded"
    assert dict(cached.value.details) == dict(uncached.value.details)
