"""Logical asset, cache invalidation, PNG, and hot replacement tests."""

import json
import struct
import zlib
from pathlib import Path

import pytest

from ludoweave.assets import (
    AssetError,
    AssetKind,
    AssetManifest,
    AssetPipeline,
    AssetUri,
    PngTexture,
    TextureAsset,
    TextureSlot,
    decode_png,
)


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


def _project(tmp_path: Path) -> tuple[Path, AssetManifest]:
    project = tmp_path / "project"
    sources = project / "assets"
    sources.mkdir(parents=True)
    (sources / "player.png").write_bytes(_png(255, 0, 0))
    (sources / "scene.json").write_text('{"name":"arena"}', encoding="utf-8")
    (sources / "unrelated.json").write_text('{"stable":true}', encoding="utf-8")
    manifest_path = project / "ludoweave.assets.json"
    manifest_path.write_text(
        json.dumps(
            {
                "protocol": "ludoweave.assets/1",
                "assets": [
                    {
                        "uri": "asset://textures/player.png",
                        "kind": "png",
                        "source": "assets/player.png",
                        "settings": {},
                        "dependencies": [],
                    },
                    {
                        "uri": "asset://scenes/arena.json",
                        "kind": "json",
                        "source": "assets/scene.json",
                        "settings": {},
                        "dependencies": ["asset://textures/player.png"],
                    },
                    {
                        "uri": "asset://data/unrelated.json",
                        "kind": "json",
                        "source": "assets/unrelated.json",
                        "settings": {},
                        "dependencies": [],
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    return project, AssetManifest.load(manifest_path, project_root=project)


@pytest.mark.parametrize(
    "value",
    ["file://player.png", "asset://../secret", "asset:///player.png", "asset://a//b"],
)
def test_asset_uri_rejects_noncanonical_or_traversing_values(value: str) -> None:
    with pytest.raises(AssetError):
        AssetUri(value)


def test_png_decoder_and_texture_slot_retain_old_revision_until_release(tmp_path: Path) -> None:
    project, manifest = _project(tmp_path)
    pipeline = AssetPipeline(manifest, tmp_path / "cache")
    uri = AssetUri("asset://textures/player.png")
    first = pipeline.build(uri)
    width, height = struct.unpack_from(">II", first.payload)
    slot = TextureSlot(
        TextureAsset(uri, first.source_hash, 0, PngTexture(width, height, first.payload[8:]))
    )

    (project / "assets" / "player.png").write_bytes(_png(0, 255, 0))
    replacement = pipeline.build(uri)
    current = slot.replace(replacement)

    assert decode_png(_png(1, 2, 3)).rgba8 == bytes((1, 2, 3, 255))
    assert current.revision == 1
    assert current.texture.rgba8 == bytes((0, 255, 0, 255))
    assert slot.retired[0].texture.rgba8 == bytes((255, 0, 0, 255))
    assert slot.release_retired() and slot.retired == ()


def test_content_change_invalidates_asset_and_dependents_only(tmp_path: Path) -> None:
    project, manifest = _project(tmp_path)
    pipeline = AssetPipeline(manifest, tmp_path / "cache")
    before = {item.uri.value: item for item in pipeline.build_all()}

    (project / "assets" / "player.png").write_bytes(_png(0, 0, 255))
    after = {item.uri.value: item for item in pipeline.build_all()}

    assert (
        after["asset://textures/player.png"].cache_key
        != before["asset://textures/player.png"].cache_key
    )
    assert (
        after["asset://scenes/arena.json"].cache_key
        != before["asset://scenes/arena.json"].cache_key
    )
    assert (
        after["asset://data/unrelated.json"].cache_key
        == before["asset://data/unrelated.json"].cache_key
    )
    assert tuple((tmp_path / "cache").rglob("*.json"))


def test_manifest_rejects_source_escape(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    manifest_path = project / "assets.json"
    manifest_path.write_text(
        json.dumps(
            {
                "protocol": "ludoweave.assets/1",
                "assets": [
                    {
                        "uri": "asset://bad.txt",
                        "kind": AssetKind.JSON.value,
                        "source": "../bad.txt",
                        "settings": {},
                        "dependencies": [],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(AssetError):
        AssetManifest.load(manifest_path, project_root=project)


def test_shipped_clockwork_arena_project_manifest_resolves_inside_examples() -> None:
    root = Path(__file__).resolve().parents[2]
    examples = root / "examples"
    manifest = AssetManifest.load(
        examples / "clockwork_arena.assets.json",
        project_root=examples,
    )

    uri = AssetUri("asset://scenes/clockwork-arena.json")
    assert manifest.entry(uri).kind is AssetKind.JSON
    assert manifest.source_path(uri).is_file()
