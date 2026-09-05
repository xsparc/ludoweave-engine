"""Unit tests for bounded explicit source manifests."""

from __future__ import annotations

from collections.abc import Callable
from typing import cast

import pytest

from ludoweave.scene import (
    SOURCE_MANIFEST_PROTOCOL,
    SourceManifest,
    SourceManifestEntry,
    SourceManifestLimits,
)
from ludoweave.scene.errors import SceneError
from ludoweave.world import canonical_dumps


def _manifest(*entries: dict[str, object]) -> bytes:
    value: dict[str, object] = {
        "$schema": SOURCE_MANIFEST_PROTOCOL,
        "manifest_id": "project-sources",
        "entries": list(entries),
    }
    return canonical_dumps(value)


def _scene(entry_id: str = "main") -> dict[str, object]:
    return {"entry_id": entry_id, "kind": "scene", "source": "scenes/main.json"}


def _prefab(entry_id: str = "enemy") -> dict[str, object]:
    return {
        "entry_id": entry_id,
        "kind": "prefab",
        "source": "prefabs/enemy.json",
        "instance": "prefabs/enemy-instance.json",
    }


def test_source_manifest_normalizes_entries_and_canonical_bytes() -> None:
    manifest = SourceManifest.from_json(_manifest(_scene("z-scene"), _prefab("a-prefab")))

    assert manifest.protocol == SOURCE_MANIFEST_PROTOCOL
    assert manifest.manifest_id == "project-sources"
    assert tuple(entry.entry_id for entry in manifest.entries) == ("a-prefab", "z-scene")
    assert manifest.canonical_bytes() == canonical_dumps(manifest.as_dict())
    assert manifest.as_dict()["entries"] == [
        {
            "entry_id": "a-prefab",
            "kind": "prefab",
            "source": "prefabs/enemy.json",
            "instance": "prefabs/enemy-instance.json",
        },
        {"entry_id": "z-scene", "kind": "scene", "source": "scenes/main.json"},
    ]


@pytest.mark.parametrize(
    ("document", "code"),
    [
        (
            canonical_dumps(
                {"$schema": "other/1", "manifest_id": "sources", "entries": [_scene()]}
            ),
            "source_manifest.incompatible_protocol",
        ),
        (_manifest(), "source_manifest.limit_exceeded"),
        (_manifest(_scene("same"), _prefab("same")), "source_manifest.duplicate_entry_id"),
        (_manifest(_scene("one"), _scene("two")), "source_manifest.duplicate_source"),
        (
            _manifest(
                {
                    "entry_id": "scene",
                    "kind": "scene",
                    "source": "scene.json",
                    "instance": "instance.json",
                }
            ),
            "source_manifest.invalid_document",
        ),
        (
            _manifest({"entry_id": "prefab", "kind": "prefab", "source": "prefab.json"}),
            "source_manifest.invalid_document",
        ),
        (
            _manifest({"entry_id": "source", "kind": "audio", "source": "audio.wav"}),
            "source_manifest.invalid_entry",
        ),
        (
            _manifest({"entry_id": "escape", "kind": "scene", "source": "../scene.json"}),
            "source_manifest.invalid_path",
        ),
        (
            _manifest({"entry_id": "drive", "kind": "scene", "source": "C:/scene.json"}),
            "source_manifest.invalid_path",
        ),
        (
            _manifest({"entry_id": "reserved", "kind": "scene", "source": "scenes/CON.json"}),
            "source_manifest.invalid_path",
        ),
        (
            _manifest({"entry_id": "colon", "kind": "scene", "source": "scenes/main:old.json"}),
            "source_manifest.invalid_path",
        ),
        (
            _manifest({"entry_id": "trailing", "kind": "scene", "source": "scenes/main."}),
            "source_manifest.invalid_path",
        ),
    ],
)
def test_source_manifest_rejects_invalid_documents(document: bytes, code: str) -> None:
    with pytest.raises(SceneError) as caught:
        SourceManifest.from_json(document)

    assert caught.value.code == code
    assert "../scene.json" not in str(caught.value.as_dict())
    assert "C:/scene.json" not in str(caught.value.as_dict())


def test_source_manifest_applies_tightened_entry_limit() -> None:
    with pytest.raises(SceneError) as caught:
        SourceManifest.from_json(
            _manifest(_scene(), _prefab()),
            limits=SourceManifestLimits(max_entries=1),
        )

    assert caught.value.code == "source_manifest.limit_exceeded"
    assert dict(caught.value.details)["limit"] == 1


@pytest.mark.parametrize(
    "factory",
    [
        lambda: SourceManifestLimits(max_bytes=0),
        lambda: SourceManifestLimits(max_entries=True),
        lambda: SourceManifestLimits(max_path_bytes=1_025),
        lambda: SourceManifest.from_json(
            _manifest(_scene()), limits=cast(SourceManifestLimits, object())
        ),
        lambda: SourceManifestEntry("scene", "scene", "scene.json", "instance.json"),
        lambda: SourceManifestEntry("prefab", "prefab", "prefab.json"),
    ],
)
def test_source_manifest_rejects_invalid_limits_or_direct_entries(
    factory: Callable[[], object],
) -> None:
    with pytest.raises(SceneError):
        factory()
