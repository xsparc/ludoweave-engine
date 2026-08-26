"""Explicit cache population after complete cache-assisted realization."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Never

import pytest

import ludoweave.assets.population as asset_population
import ludoweave.assets.realization as asset_realization
from ludoweave.assets import (
    ASSET_CACHE_POPULATION_PROTOCOL,
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
    populate_asset_build_cache,
)


def _hash(payload: bytes) -> str:
    return f"sha256:{sha256(payload).hexdigest()}"


def _fixture(
    root: Path,
    *,
    json_source: bytes = b'{ "z": 2, "a": 1 }',
) -> tuple[AssetBuildPlan, tuple[AssetBuildInput, ...]]:
    json_uri = AssetUri("asset://data/config.json")
    shader_uri = AssetUri("asset://shaders/main.wgsl")
    sources = {
        json_uri: json_source,
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


def test_missing_cache_is_populated_only_after_complete_realization(tmp_path: Path) -> None:
    plan, inputs = _fixture(tmp_path)
    cache = tmp_path / "cache"

    population = populate_asset_build_cache(plan, inputs, cache)

    assert population.protocol == ASSET_CACHE_POPULATION_PROTOCOL
    assert population.realization.materialization == materialize_asset_build_plan(plan, inputs)
    assert (population.hits, population.decoded) == (0, 2)
    assert (population.published, population.reused) == (2, 0)
    assert [entry.realization.status for entry in population.entries] == [
        "decoded",
        "decoded",
    ]
    assert [entry.publication.status for entry in population.entries] == [
        "published",
        "published",
    ]
    assert len(list(cache.rglob("entry.json"))) == 2


def test_second_population_reuses_hits_without_decoder_or_cache_change(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan, inputs = _fixture(tmp_path)
    cache = tmp_path / "cache"
    populate_asset_build_cache(plan, inputs, cache)
    before = _files(cache)

    def reject_decode(kind: AssetKind, source: bytes) -> bytes:
        raise AssertionError((kind, source))

    monkeypatch.setattr(asset_realization, "_decode_payload", reject_decode)
    population = populate_asset_build_cache(plan, inputs, cache)

    assert (population.hits, population.decoded) == (2, 0)
    assert (population.published, population.reused) == (0, 2)
    assert _files(cache) == before


def test_mixed_population_decodes_only_miss_and_preserves_plan_order(tmp_path: Path) -> None:
    plan, inputs = _fixture(tmp_path)
    expected = materialize_asset_build_plan(plan, inputs)
    cache = tmp_path / "cache"
    AssetCacheStore(cache).publish(_partial(expected, 1))

    population = populate_asset_build_cache(plan, inputs, cache)

    assert tuple(entry.uri for entry in population.entries) == tuple(
        entry.uri for entry in plan.entries
    )
    assert [entry.realization.status for entry in population.entries] == ["decoded", "hit"]
    assert [entry.publication.status for entry in population.entries] == [
        "published",
        "reused",
    ]


def test_source_preflight_failure_never_reads_or_creates_cache(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan, inputs = _fixture(tmp_path)
    cache = tmp_path / "cache"
    changed = (*inputs[:-1], AssetBuildInput(inputs[-1].uri, b"changed"))
    calls = 0
    original = AssetCacheStore.load_action

    def observe(self: AssetCacheStore, entry: object) -> object:
        nonlocal calls
        calls += 1
        return original(self, entry)  # type: ignore[arg-type]

    monkeypatch.setattr(AssetCacheStore, "load_action", observe)
    with pytest.raises(AssetError) as caught:
        populate_asset_build_cache(plan, changed, cache)

    assert caught.value.code == "asset_build.input_mismatch"
    assert calls == 0
    assert not cache.exists()


def test_corrupt_later_cache_entry_prevents_decoder_and_publication(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan, inputs = _fixture(tmp_path)
    expected = materialize_asset_build_plan(plan, inputs)
    cache = tmp_path / "cache"
    AssetCacheStore(cache).publish(_partial(expected, 1))
    action = plan.entries[1].cache_key.removeprefix("sha256:")
    metadata = cache / "actions" / action[:2] / action / "entry.json"
    metadata.write_bytes(b"{}")
    before = _files(cache)
    calls = 0

    def observe(kind: AssetKind, source: bytes) -> bytes:
        nonlocal calls
        calls += 1
        return source

    monkeypatch.setattr(asset_realization, "_decode_payload", observe)
    with pytest.raises(AssetCacheError) as caught:
        populate_asset_build_cache(plan, inputs, cache)

    assert caught.value.code == "asset_cache.corrupt_entry"
    assert calls == 0
    assert _files(cache) == before


def test_decoder_failure_does_not_acquire_write_authority_or_create_cache(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan, inputs = _fixture(tmp_path, json_source=b"not-json")
    cache = tmp_path / "cache"
    writable_authorities = 0
    original = AssetCacheStore

    def observe_store(
        root: Path,
        *,
        project_root: Path | None = None,
        writable: bool = True,
    ) -> AssetCacheStore:
        nonlocal writable_authorities
        if writable:
            writable_authorities += 1
        return original(root, project_root=project_root, writable=writable)

    monkeypatch.setattr(asset_population, "AssetCacheStore", observe_store)
    with pytest.raises(AssetError) as caught:
        populate_asset_build_cache(plan, inputs, cache)

    assert caught.value.code == "asset_build.decode_failed"
    assert writable_authorities == 0
    assert not cache.exists()


def test_limit_failure_does_not_create_cache(tmp_path: Path) -> None:
    plan, inputs = _fixture(tmp_path)
    cache = tmp_path / "cache"
    limits = AssetBuildExecutionLimits(max_total_artifact_bytes=1)

    with pytest.raises(AssetError) as caught:
        populate_asset_build_cache(plan, inputs, cache, limits=limits)

    assert caught.value.code == "asset_build.limit_exceeded"
    assert not cache.exists()


def test_publication_failure_has_no_success_report_and_keeps_original_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan, inputs = _fixture(tmp_path)
    cache = tmp_path / "cache"

    def reject_publish(self: AssetCacheStore, materialized: object) -> Never:
        raise AssetCacheError(
            "publication failed",
            code="asset_cache.publish_failed",
            subsystem="asset_cache",
            phase="publish",
            details={"field": "entry", "cause_type": "OSError"},
        )

    monkeypatch.setattr(AssetCacheStore, "publish", reject_publish)
    with pytest.raises(AssetCacheError) as caught:
        populate_asset_build_cache(plan, inputs, cache)

    assert caught.value.code == "asset_cache.publish_failed"
    assert cache.is_dir()
