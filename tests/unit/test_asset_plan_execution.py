"""Bounded deterministic execution of verified asset build plans."""

from __future__ import annotations

import json
import struct
import zlib
from hashlib import sha256
from pathlib import Path

import pytest

import ludoweave.assets.execution as asset_execution
from ludoweave.assets import (
    ASSET_BUILD_RESULT_PROTOCOL,
    AssetBuildArtifact,
    AssetBuildExecutionLimits,
    AssetBuildInput,
    AssetBuildMaterialization,
    AssetBuildPlan,
    AssetBuildResult,
    AssetEntry,
    AssetError,
    AssetKind,
    AssetManifest,
    AssetPipeline,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetUri,
    execute_asset_build_plan,
    materialize_asset_build_plan,
)


def _hash(value: bytes) -> str:
    return f"sha256:{sha256(value).hexdigest()}"


def _png(red: int, green: int, blue: int) -> bytes:
    def chunk(kind: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + kind
            + payload
            + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
        )

    header = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
    pixels = zlib.compress(bytes((0, red, green, blue, 255)))
    return (
        b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", pixels) + chunk(b"IEND", b"")
    )


def _fixture(
    root: Path,
) -> tuple[
    AssetManifest,
    AssetBuildPlan,
    tuple[AssetBuildInput, ...],
    dict[AssetUri, bytes],
]:
    png_uri = AssetUri("asset://textures/player.png")
    json_uri = AssetUri("asset://data/config.json")
    wgsl_uri = AssetUri("asset://shaders/main.wgsl")
    audio_uri = AssetUri("asset://audio/tone.raw")
    source_by_uri = {
        png_uri: _png(1, 2, 3),
        json_uri: b'{ "z": 2, "a": [true, null] }',
        wgsl_uri: b"@vertex fn main() -> @builtin(position) vec4f { return vec4f(); }",
        audio_uri: b"\x00\x01\x02\x03",
    }
    entries = (
        AssetEntry(png_uri, AssetKind.PNG, "assets/player.png"),
        AssetEntry(
            json_uri,
            AssetKind.JSON,
            "assets/config.json",
            dependencies=(png_uri,),
        ),
        AssetEntry(wgsl_uri, AssetKind.WGSL, "assets/main.wgsl"),
        AssetEntry(audio_uri, AssetKind.AUDIO, "assets/tone.raw"),
    )
    manifest = AssetManifest(root, entries)
    lock = AssetSourceLock(
        source_lock_sha256=_hash(b"source-lock"),
        asset_manifest_sha256=_hash(manifest.canonical_bytes()),
        roots=(json_uri, wgsl_uri, audio_uri),
        entries=tuple(
            AssetSourceLockEntry(uri, manifest.entry(uri).kind, _hash(source), len(source))
            for uri, source in source_by_uri.items()
        ),
    )
    plan = AssetBuildPlan.from_inputs(manifest, lock)
    inputs = tuple(AssetBuildInput(entry.uri, source_by_uri[entry.uri]) for entry in plan.entries)
    return manifest, plan, inputs, source_by_uri


def test_execute_plan_decodes_builtins_in_order_and_reports_stable_outputs(
    tmp_path: Path,
) -> None:
    _, plan, inputs, source_by_uri = _fixture(tmp_path)

    first = execute_asset_build_plan(plan, inputs)
    second = execute_asset_build_plan(plan, inputs)

    expected_payloads = {
        AssetUri("asset://textures/player.png"): struct.pack(">II", 1, 1) + bytes((1, 2, 3, 255)),
        AssetUri("asset://data/config.json"): b'{"a":[true,null],"z":2}',
        AssetUri("asset://shaders/main.wgsl"): source_by_uri[AssetUri("asset://shaders/main.wgsl")],
        AssetUri("asset://audio/tone.raw"): source_by_uri[AssetUri("asset://audio/tone.raw")],
    }
    assert first == second
    assert first.protocol == ASSET_BUILD_RESULT_PROTOCOL
    assert first.plan_sha256 == _hash(plan.canonical_bytes())
    assert tuple(entry.uri for entry in first.entries) == tuple(entry.uri for entry in plan.entries)
    assert [entry.artifact_sha256 for entry in first.entries] == [
        _hash(expected_payloads[entry.uri]) for entry in plan.entries
    ]
    assert [entry.artifact_bytes for entry in first.entries] == [
        len(expected_payloads[entry.uri]) for entry in plan.entries
    ]
    assert first.source_bytes == sum(len(item.source) for item in inputs)
    assert first.artifact_bytes == sum(len(item) for item in expected_payloads.values())
    assert first.canonical_bytes() == second.canonical_bytes()
    document = json.loads(first.canonical_bytes())
    assert document["$schema"] == ASSET_BUILD_RESULT_PROTOCOL
    assert "payload" not in first.canonical_bytes().decode("utf-8")


def test_materialize_plan_retains_exact_validated_payloads_separately(
    tmp_path: Path,
) -> None:
    _, plan, inputs, _ = _fixture(tmp_path)

    materialized = materialize_asset_build_plan(plan, inputs)

    assert isinstance(materialized, AssetBuildMaterialization)
    assert materialized.result == execute_asset_build_plan(plan, inputs)
    assert tuple(artifact.entry for artifact in materialized.artifacts) == (
        materialized.result.entries
    )
    assert all(isinstance(artifact, AssetBuildArtifact) for artifact in materialized.artifacts)
    assert [artifact.entry.artifact_sha256 for artifact in materialized.artifacts] == [
        _hash(artifact.payload) for artifact in materialized.artifacts
    ]


def test_execute_plan_supports_an_empty_verified_plan(tmp_path: Path) -> None:
    manifest = AssetManifest(tmp_path, ())
    lock = AssetSourceLock(
        source_lock_sha256=_hash(b"source-lock"),
        asset_manifest_sha256=_hash(manifest.canonical_bytes()),
        roots=(),
        entries=(),
    )
    plan = AssetBuildPlan.from_inputs(manifest, lock)

    result = execute_asset_build_plan(plan, ())

    assert result.entries == ()
    assert result.source_bytes == 0
    assert result.artifact_bytes == 0


@pytest.mark.parametrize("field", ["source_bytes", "source_sha256"])
def test_execute_plan_rejects_changed_detached_source_content_silently(
    tmp_path: Path,
    field: str,
) -> None:
    _, plan, inputs, _ = _fixture(tmp_path)
    first = inputs[0]
    changed = b"x" if field == "source_bytes" else bytes([first.source[0] ^ 1]) + first.source[1:]
    actual = (AssetBuildInput(first.uri, changed), *inputs[1:])

    with pytest.raises(AssetError) as caught:
        execute_asset_build_plan(plan, actual)

    assert caught.value.code == "asset_build.input_mismatch"
    assert caught.value.phase == "execute"
    assert dict(caught.value.details) == {"field": field, "uri": first.uri.value}
    rendered = json.dumps(caught.value.as_dict(), sort_keys=True)
    assert first.source.hex() not in rendered
    assert plan.entries[0].source_sha256 not in rendered


def test_complete_source_preflight_rejects_late_mismatch_before_any_decoder(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, plan, inputs, _ = _fixture(tmp_path)
    last = inputs[-1]
    changed = bytes([last.source[0] ^ 1]) + last.source[1:]
    actual = (*inputs[:-1], AssetBuildInput(last.uri, changed))
    decoder_calls: list[AssetKind] = []

    def unexpected_decoder(kind: AssetKind, source: bytes) -> bytes:
        decoder_calls.append(kind)
        return source

    monkeypatch.setattr(asset_execution, "_decode_payload", unexpected_decoder)

    with pytest.raises(AssetError) as caught:
        execute_asset_build_plan(plan, actual)

    assert caught.value.code == "asset_build.input_mismatch"
    assert dict(caught.value.details) == {
        "field": "source_sha256",
        "uri": last.uri.value,
    }
    assert decoder_calls == []


def test_execute_plan_rejects_noncanonical_input_order_and_types(tmp_path: Path) -> None:
    _, plan, inputs, _ = _fixture(tmp_path)

    with pytest.raises(AssetError, match="input") as order_error:
        execute_asset_build_plan(plan, tuple(reversed(inputs)))
    assert order_error.value.code == "asset_build.invalid_inputs"

    with pytest.raises(AssetError) as collection_error:
        execute_asset_build_plan(plan, list(inputs))  # type: ignore[arg-type]
    assert collection_error.value.code == "asset_build.invalid_inputs"

    with pytest.raises(AssetError) as plan_error:
        execute_asset_build_plan(object(), inputs)  # type: ignore[arg-type]
    assert plan_error.value.code == "asset_build.invalid_inputs"


def test_execute_plan_normalizes_decoder_failure_without_success_result(tmp_path: Path) -> None:
    uri = AssetUri("asset://data/invalid.json")
    source = b"not-json"
    manifest = AssetManifest(
        tmp_path,
        (AssetEntry(uri, AssetKind.JSON, "assets/invalid.json"),),
    )
    lock = AssetSourceLock(
        source_lock_sha256=_hash(b"source-lock"),
        asset_manifest_sha256=_hash(manifest.canonical_bytes()),
        roots=(uri,),
        entries=(AssetSourceLockEntry(uri, AssetKind.JSON, _hash(source), len(source)),),
    )
    plan = AssetBuildPlan.from_inputs(manifest, lock)

    with pytest.raises(AssetError) as caught:
        execute_asset_build_plan(plan, (AssetBuildInput(uri, source),))

    assert caught.value.code == "asset_build.decode_failed"
    assert caught.value.phase == "execute"
    assert dict(caught.value.details) == {
        "uri": uri.value,
        "cause_code": "asset.invalid_value",
    }
    assert isinstance(caught.value.__cause__, AssetError)
    assert "not-json" not in json.dumps(caught.value.as_dict())


def test_execute_plan_enforces_source_and_artifact_work_bounds(tmp_path: Path) -> None:
    _, plan, inputs, _ = _fixture(tmp_path)

    with pytest.raises(AssetError) as source_error:
        execute_asset_build_plan(
            plan,
            inputs,
            limits=AssetBuildExecutionLimits(max_source_bytes=1),
        )
    assert source_error.value.code == "asset_build.limit_exceeded"
    assert dict(source_error.value.details)["field"] == "source_bytes"

    with pytest.raises(AssetError) as artifact_error:
        execute_asset_build_plan(
            plan,
            inputs,
            limits=AssetBuildExecutionLimits(max_artifact_bytes=1),
        )
    assert artifact_error.value.code == "asset_build.limit_exceeded"
    assert dict(artifact_error.value.details)["field"] == "artifact_bytes"


def test_execute_plan_enforces_aggregate_source_and_artifact_bounds(tmp_path: Path) -> None:
    _, plan, inputs, _ = _fixture(tmp_path)
    first_source_bytes = len(inputs[0].source)
    first = execute_asset_build_plan(plan, inputs[:1] + inputs[1:])
    first_artifact_bytes = first.entries[0].artifact_bytes

    with pytest.raises(AssetError) as source_error:
        execute_asset_build_plan(
            plan,
            inputs,
            limits=AssetBuildExecutionLimits(max_total_source_bytes=first_source_bytes),
        )
    assert source_error.value.code == "asset_build.limit_exceeded"
    assert dict(source_error.value.details)["field"] == "total_source_bytes"

    with pytest.raises(AssetError) as artifact_error:
        execute_asset_build_plan(
            plan,
            inputs,
            limits=AssetBuildExecutionLimits(max_total_artifact_bytes=first_artifact_bytes),
        )
    assert artifact_error.value.code == "asset_build.limit_exceeded"
    assert dict(artifact_error.value.details)["field"] == "total_artifact_bytes"


def test_execute_plan_matches_existing_builtin_pipeline_outputs(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    manifest, plan, inputs, source_by_uri = _fixture(project_root)
    for entry in manifest.entries:
        source_path = project_root / entry.source
        source_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.write_bytes(source_by_uri[entry.uri])
    pipeline = AssetPipeline(manifest, tmp_path / "cache")

    result = execute_asset_build_plan(plan, inputs)
    pipeline_artifacts = tuple(pipeline.build(entry.uri) for entry in plan.entries)

    assert [entry.cache_key for entry in result.entries] == [
        artifact.cache_key for artifact in pipeline_artifacts
    ]
    assert [entry.artifact_sha256 for entry in result.entries] == [
        _hash(artifact.payload) for artifact in pipeline_artifacts
    ]
    assert [entry.artifact_bytes for entry in result.entries] == [
        len(artifact.payload) for artifact in pipeline_artifacts
    ]


@pytest.mark.parametrize("value", [0, -1, True, 1.5, "1"])
def test_execution_limits_require_exact_positive_integers(value: object) -> None:
    with pytest.raises(AssetError) as caught:
        AssetBuildExecutionLimits(max_source_bytes=value)  # type: ignore[arg-type]
    assert caught.value.code == "asset_build.invalid_limits"


def test_result_values_reject_forged_aggregate_counts(tmp_path: Path) -> None:
    _, plan, inputs, _ = _fixture(tmp_path)
    result = execute_asset_build_plan(plan, inputs)

    with pytest.raises(AssetError) as caught:
        AssetBuildResult(
            plan_sha256=result.plan_sha256,
            source_bytes=result.source_bytes + 1,
            artifact_bytes=result.artifact_bytes,
            entries=result.entries,
        )

    assert caught.value.code == "asset_build.invalid_result"
