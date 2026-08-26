"""Verified atomic local cache publication for materialized asset artifacts."""

from __future__ import annotations

import json
from collections.abc import Iterator
from hashlib import sha256
from pathlib import Path

import pytest

import ludoweave.assets.cache as asset_cache
from ludoweave.assets import (
    ASSET_CACHE_ENTRY_PROTOCOL,
    ASSET_CACHE_LOOKUP_PROTOCOL,
    ASSET_CACHE_PUBLISH_PROTOCOL,
    AssetBuildArtifact,
    AssetBuildInput,
    AssetBuildMaterialization,
    AssetBuildPlan,
    AssetBuildResult,
    AssetBuildResultEntry,
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
)


def _hash(value: bytes) -> str:
    return f"sha256:{sha256(value).hexdigest()}"


def _materialization(payload: bytes = b'{"value":1}') -> AssetBuildMaterialization:
    entry = AssetBuildResultEntry(
        uri=AssetUri("asset://data/item.json"),
        kind=AssetKind.JSON,
        cache_key=_hash(b"cache-key"),
        source_bytes=13,
        artifact_sha256=_hash(payload),
        artifact_bytes=len(payload),
    )
    result = AssetBuildResult(
        plan_sha256=_hash(b"plan"),
        source_bytes=13,
        artifact_bytes=len(payload),
        entries=(entry,),
    )
    return AssetBuildMaterialization(result, (AssetBuildArtifact(entry, payload),))


def _entry_root(root: Path, materialized: AssetBuildMaterialization) -> Path:
    digest = materialized.result.entries[0].cache_key.removeprefix("sha256:")
    return root / "actions" / digest[:2] / digest


def _blob_path(root: Path, materialized: AssetBuildMaterialization) -> Path:
    digest = materialized.result.entries[0].artifact_sha256.removeprefix("sha256:")
    return root / "cas" / digest[:2] / digest


def _planned_materialization(
    root: Path,
    *,
    count: int = 1,
) -> tuple[AssetBuildPlan, AssetBuildMaterialization]:
    root.mkdir(parents=True)
    uris = tuple(AssetUri(f"asset://data/item-{index}.json") for index in range(count))
    sources = tuple(f'{{"value":{index}}}'.encode() for index in range(count))
    manifest = AssetManifest(
        root,
        tuple(
            AssetEntry(uri, AssetKind.JSON, f"assets/item-{index}.json")
            for index, uri in enumerate(uris)
        ),
    )
    lock = AssetSourceLock(
        source_lock_sha256=_hash(b"source-lock"),
        asset_manifest_sha256=_hash(manifest.canonical_bytes()),
        roots=uris,
        entries=tuple(
            AssetSourceLockEntry(uri, AssetKind.JSON, _hash(source), len(source))
            for uri, source in zip(uris, sources, strict=True)
        ),
    )
    plan = AssetBuildPlan.from_inputs(manifest, lock)
    materialized = materialize_asset_build_plan(
        plan,
        tuple(AssetBuildInput(entry.uri, sources[uris.index(entry.uri)]) for entry in plan.entries),
    )
    return plan, materialized


def test_cache_publishes_one_complete_entry_and_verifies_reads(tmp_path: Path) -> None:
    root = tmp_path / "cache"
    materialized = _materialization()
    store = AssetCacheStore(root)

    summary = store.publish(materialized)

    entry = materialized.result.entries[0]
    assert summary.protocol == ASSET_CACHE_PUBLISH_PROTOCOL
    assert summary.plan_sha256 == materialized.result.plan_sha256
    assert summary.published == 1
    assert summary.reused == 0
    assert store.load(entry) == materialized.artifacts[0].payload
    entry_root = _entry_root(root, materialized)
    assert sorted(path.name for path in entry_root.iterdir()) == ["entry.json"]
    assert _blob_path(root, materialized).read_bytes() == materialized.artifacts[0].payload
    metadata = json.loads((entry_root / "entry.json").read_bytes())
    assert metadata["$schema"] == ASSET_CACHE_ENTRY_PROTOCOL
    assert metadata["cache_key"] == entry.cache_key
    assert metadata["artifact_sha256"] == entry.artifact_sha256
    report = json.loads(summary.canonical_bytes())
    assert report["$schema"] == ASSET_CACHE_PUBLISH_PROTOCOL
    assert "path" not in summary.canonical_bytes().decode("utf-8")


def test_cache_reuses_verified_entry_without_rewriting(tmp_path: Path) -> None:
    root = tmp_path / "cache"
    materialized = _materialization()
    store = AssetCacheStore(root)
    first = store.publish(materialized)
    before = {
        path.name: (path.read_bytes(), path.stat().st_mtime_ns)
        for path in _entry_root(root, materialized).iterdir()
    }

    second = store.publish(materialized)

    after = {
        path.name: (path.read_bytes(), path.stat().st_mtime_ns)
        for path in _entry_root(root, materialized).iterdir()
    }
    assert first.published == 1
    assert second.published == 0
    assert second.reused == 1
    assert after == before


@pytest.mark.parametrize("target", ["blob", "metadata"])
def test_cache_rejects_corrupt_existing_entry_without_overwrite(
    tmp_path: Path,
    target: str,
) -> None:
    root = tmp_path / "cache"
    materialized = _materialization()
    store = AssetCacheStore(root)
    store.publish(materialized)
    path = (
        _blob_path(root, materialized)
        if target == "blob"
        else _entry_root(root, materialized) / "entry.json"
    )
    path.write_bytes(b"corrupt")
    before = path.read_bytes()

    with pytest.raises(AssetCacheError) as caught:
        store.publish(materialized)

    assert caught.value.code == "asset_cache.corrupt_entry"
    assert path.read_bytes() == before
    assert not list(root.rglob(".staging-*"))


def test_cache_miss_has_no_filesystem_side_effect(tmp_path: Path) -> None:
    root = tmp_path / "cache"
    store = AssetCacheStore(root)
    entry = _materialization().result.entries[0]
    before = sorted(path.relative_to(root) for path in root.rglob("*"))

    assert store.load(entry) is None

    assert sorted(path.relative_to(root) for path in root.rglob("*")) == before


def test_cache_publish_failure_cleans_staging_and_normalizes_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "cache"
    store = AssetCacheStore(root)
    materialized = _materialization()

    def fail_replace(source: Path, target: Path) -> None:
        del source, target
        raise OSError("synthetic")

    monkeypatch.setattr(asset_cache.os, "replace", fail_replace)

    with pytest.raises(AssetCacheError) as caught:
        store.publish(materialized)

    assert caught.value.code == "asset_cache.publish_failed"
    assert dict(caught.value.details) == {"cause_type": "OSError", "field": "entry"}
    assert not _entry_root(root, materialized).exists()
    assert not list(root.rglob(".staging-*"))


def test_action_publish_failure_leaves_only_verified_reusable_blob(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "cache"
    store = AssetCacheStore(root)
    materialized = _materialization()
    original_replace = asset_cache.os.replace
    replacements = 0

    def fail_second_replace(source: Path, target: Path) -> None:
        nonlocal replacements
        replacements += 1
        if replacements == 2:
            raise OSError("synthetic action failure")
        original_replace(source, target)

    monkeypatch.setattr(asset_cache.os, "replace", fail_second_replace)

    with pytest.raises(AssetCacheError) as caught:
        store.publish(materialized)

    assert caught.value.code == "asset_cache.publish_failed"
    assert _blob_path(root, materialized).read_bytes() == materialized.artifacts[0].payload
    assert not _entry_root(root, materialized).exists()
    assert store.load(materialized.result.entries[0]) is None
    assert not list(root.rglob(".staging-*"))

    monkeypatch.setattr(asset_cache.os, "replace", original_replace)
    summary = store.publish(materialized)
    assert summary.published == 1
    assert store.load(materialized.result.entries[0]) == materialized.artifacts[0].payload
    assert len([path for path in (root / "cas").rglob("*") if path.is_file()]) == 1


def test_distinct_action_keys_deduplicate_one_artifact_blob(tmp_path: Path) -> None:
    payload = b'{"shared":true}'
    first = _materialization(payload).result.entries[0]
    second = AssetBuildResultEntry(
        uri=AssetUri("asset://data/second.json"),
        kind=AssetKind.JSON,
        cache_key=_hash(b"second-cache-key"),
        source_bytes=17,
        artifact_sha256=first.artifact_sha256,
        artifact_bytes=first.artifact_bytes,
    )
    result = AssetBuildResult(
        plan_sha256=_hash(b"deduplicated-plan"),
        source_bytes=first.source_bytes + second.source_bytes,
        artifact_bytes=first.artifact_bytes + second.artifact_bytes,
        entries=(first, second),
    )
    materialized = AssetBuildMaterialization(
        result,
        (AssetBuildArtifact(first, payload), AssetBuildArtifact(second, payload)),
    )
    root = tmp_path / "cache"

    summary = AssetCacheStore(root).publish(materialized)

    assert summary.published == 2
    assert len([path for path in (root / "cas").rglob("*") if path.is_file()]) == 1
    assert len([path for path in (root / "actions").rglob("entry.json")]) == 2


@pytest.mark.parametrize("relation", ["same", "inside", "ancestor"])
def test_cache_root_must_not_overlap_project(tmp_path: Path, relation: str) -> None:
    project = tmp_path / "project"
    project.mkdir()
    if relation == "same":
        cache = project
    elif relation == "inside":
        cache = project / "cache"
    else:
        cache = tmp_path

    with pytest.raises(AssetCacheError) as caught:
        AssetCacheStore(cache, project_root=project)

    assert caught.value.code == "asset_cache.invalid_root"
    assert dict(caught.value.details) == {"field": "cache_root"}


def test_cache_values_require_exact_payload_identity(tmp_path: Path) -> None:
    materialized = _materialization()
    entry = materialized.result.entries[0]

    with pytest.raises(AssetError) as artifact_error:
        AssetBuildArtifact(entry, b"changed")
    assert artifact_error.value.code == "asset_cache.invalid_artifact"

    store = AssetCacheStore(tmp_path / "cache")
    with pytest.raises(AssetCacheError) as input_error:
        store.publish(object())  # type: ignore[arg-type]
    assert input_error.value.code == "asset_cache.invalid_materialization"


def test_empty_materialization_has_deterministic_empty_summary(tmp_path: Path) -> None:
    result = AssetBuildResult(
        plan_sha256=_hash(b"empty-plan"),
        source_bytes=0,
        artifact_bytes=0,
        entries=(),
    )
    materialized = AssetBuildMaterialization(result, ())

    summary = AssetCacheStore(tmp_path / "cache").publish(materialized)

    assert summary.published == summary.reused == 0
    assert summary.entries == ()
    assert (
        summary.canonical_bytes()
        == AssetCacheStore(tmp_path / "other").publish(materialized).canonical_bytes()
    )


def test_read_only_lookup_reports_miss_without_creating_cache_root(tmp_path: Path) -> None:
    plan, _ = _planned_materialization(tmp_path / "project")
    root = tmp_path / "absent-cache"
    store = AssetCacheStore(root, writable=False)

    summary = store.inspect(plan)

    assert summary.protocol == ASSET_CACHE_LOOKUP_PROTOCOL
    assert summary.hits == 0
    assert summary.misses == 1
    assert summary.entries[0].status == "miss"
    assert summary.entries[0].artifact_sha256 is None
    assert summary.entries[0].artifact_bytes is None
    assert not root.exists()
    with pytest.raises(AssetCacheError) as caught:
        store.publish(_planned_materialization(tmp_path / "other")[1])
    assert caught.value.code == "asset_cache.read_only"
    assert not root.exists()


def test_lookup_verifies_action_metadata_and_cas_payload(tmp_path: Path) -> None:
    plan, materialized = _planned_materialization(tmp_path / "project")
    root = tmp_path / "cache"
    AssetCacheStore(root).publish(materialized)
    before = {path: path.stat().st_mtime_ns for path in root.rglob("*")}
    store = AssetCacheStore(root, writable=False)

    artifact = store.load_action(plan.entries[0])
    summary = store.inspect(plan)

    assert artifact is not None
    assert artifact == materialized.artifacts[0]
    assert summary.hits == 1
    assert summary.misses == 0
    assert summary.entries[0].artifact_sha256 == artifact.entry.artifact_sha256
    assert summary.entries[0].artifact_bytes == artifact.entry.artifact_bytes
    assert {path: path.stat().st_mtime_ns for path in root.rglob("*")} == before


def test_lookup_reports_plan_ordered_mixed_hits_and_misses(tmp_path: Path) -> None:
    plan, materialized = _planned_materialization(tmp_path / "project", count=2)
    first = materialized.artifacts[0]
    partial = AssetBuildMaterialization(
        AssetBuildResult(
            plan_sha256=materialized.result.plan_sha256,
            source_bytes=first.entry.source_bytes,
            artifact_bytes=first.entry.artifact_bytes,
            entries=(first.entry,),
        ),
        (first,),
    )
    root = tmp_path / "cache"
    AssetCacheStore(root).publish(partial)

    summary = AssetCacheStore(root, writable=False).inspect(plan)

    assert summary.hits == summary.misses == 1
    assert [entry.status for entry in summary.entries] == ["hit", "miss"]
    assert [entry.uri for entry in summary.entries] == [entry.uri for entry in plan.entries]


@pytest.mark.parametrize(
    "mutation",
    ["duplicate", "unknown", "whitespace", "source_bytes", "oversized"],
)
def test_lookup_rejects_noncanonical_or_mismatched_action_metadata(
    tmp_path: Path,
    mutation: str,
) -> None:
    plan, materialized = _planned_materialization(tmp_path / "project")
    root = tmp_path / "cache"
    AssetCacheStore(root).publish(materialized)
    metadata = _entry_root(root, materialized) / "entry.json"
    document = json.loads(metadata.read_bytes())
    if mutation == "duplicate":
        original = metadata.read_text(encoding="utf-8")
        metadata.write_text(original[:-1] + f',"uri":"{plan.entries[0].uri.value}"}}')
    elif mutation == "unknown":
        document["unknown"] = True
        metadata.write_text(json.dumps(document, sort_keys=True), encoding="utf-8")
    elif mutation == "whitespace":
        metadata.write_text(json.dumps(document, indent=2, sort_keys=True), encoding="utf-8")
    elif mutation == "source_bytes":
        document["source_bytes"] += 1
        metadata.write_text(
            json.dumps(document, separators=(",", ":"), sort_keys=True),
            encoding="utf-8",
        )
    else:
        metadata.write_bytes(b" " * 65_537)
    before = metadata.read_bytes()

    with pytest.raises(AssetCacheError) as caught:
        AssetCacheStore(root, writable=False).load_action(plan.entries[0])

    assert caught.value.code == "asset_cache.corrupt_entry"
    assert metadata.read_bytes() == before


def test_lookup_normalizes_action_directory_enumeration_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan, materialized = _planned_materialization(tmp_path / "project")
    root = tmp_path / "cache"
    AssetCacheStore(root).publish(materialized)
    action = _entry_root(root, materialized)
    original_iterdir = Path.iterdir

    def fail_action_iterdir(path: Path) -> Iterator[Path]:
        if path == action:
            raise OSError("synthetic enumeration failure")
        return original_iterdir(path)

    monkeypatch.setattr(Path, "iterdir", fail_action_iterdir)

    with pytest.raises(AssetCacheError) as caught:
        AssetCacheStore(root, writable=False).load_action(plan.entries[0])

    assert caught.value.code == "asset_cache.corrupt_entry"
    assert isinstance(caught.value.__cause__, OSError)


def test_lookup_treats_unreferenced_cas_blob_as_miss(tmp_path: Path) -> None:
    plan, materialized = _planned_materialization(tmp_path / "project")
    root = tmp_path / "cache"
    AssetCacheStore(root).publish(materialized)
    entry_root = _entry_root(root, materialized)
    for path in entry_root.iterdir():
        path.unlink()
    entry_root.rmdir()

    store = AssetCacheStore(root, writable=False)

    assert store.load_action(plan.entries[0]) is None
    assert store.inspect(plan).misses == 1
    assert _blob_path(root, materialized).is_file()


def test_cache_authority_requires_exact_boolean(tmp_path: Path) -> None:
    with pytest.raises(AssetCacheError) as caught:
        AssetCacheStore(tmp_path / "cache", writable=1)  # type: ignore[arg-type]

    assert caught.value.code == "asset_cache.invalid_authority"
    assert not (tmp_path / "cache").exists()
