"""Deterministic dependency-closure behavior for validated asset manifests."""

from pathlib import Path
from typing import cast

import pytest

from ludoweave.assets import AssetEntry, AssetError, AssetKind, AssetManifest, AssetUri


def _uri(value: str) -> AssetUri:
    return AssetUri(f"asset://{value}")


def _manifest(root: Path) -> AssetManifest:
    texture = _uri("textures/player.png")
    material = _uri("materials/player.json")
    level = _uri("levels/one.json")
    sound = _uri("audio/theme.json")
    return AssetManifest(
        root,
        (
            AssetEntry(level, AssetKind.JSON, "assets/level.json", dependencies=(material,)),
            AssetEntry(texture, AssetKind.PNG, "assets/player.png"),
            AssetEntry(
                material,
                AssetKind.JSON,
                "assets/material.json",
                dependencies=(texture,),
            ),
            AssetEntry(sound, AssetKind.JSON, "assets/theme.json"),
        ),
    )


def test_dependency_closure_distinguishes_direct_roots_from_resolved_graph(
    tmp_path: Path,
) -> None:
    manifest = _manifest(tmp_path)
    level = _uri("levels/one.json")

    assert manifest.dependency_closure((level,)) == (
        level,
        _uri("materials/player.json"),
        _uri("textures/player.png"),
    )


def test_dependency_closure_is_unique_sorted_and_root_order_independent(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path)
    level = _uri("levels/one.json")
    texture = _uri("textures/player.png")

    expected = manifest.dependency_closure((level, texture))
    assert manifest.dependency_closure((texture, level)) == expected
    assert expected == tuple(sorted(set(expected)))
    assert manifest.dependency_closure(()) == ()


@pytest.mark.parametrize(
    "roots",
    (
        [_uri("levels/one.json")],
        ("asset://levels/one.json",),
        (_uri("levels/one.json"), _uri("levels/one.json")),
    ),
)
def test_dependency_closure_rejects_nonexact_or_repeated_roots(
    tmp_path: Path,
    roots: object,
) -> None:
    with pytest.raises(AssetError) as raised:
        _manifest(tmp_path).dependency_closure(cast(tuple[AssetUri, ...], roots))

    assert raised.value.code == "asset.invalid_dependency_roots"
    assert raised.value.details == (("field", "roots"),)


def test_dependency_closure_rejects_unknown_direct_root(tmp_path: Path) -> None:
    with pytest.raises(AssetError) as raised:
        _manifest(tmp_path).dependency_closure((_uri("missing/item.json"),))

    assert raised.value.code == "asset.unknown_uri"
    assert raised.value.details == (("uri", "asset://missing/item.json"),)

    oversized = tuple(_uri(f"overflow/item-{index:04}.json") for index in range(4_097))
    with pytest.raises(AssetError) as over_limit:
        _manifest(tmp_path).dependency_closure(oversized)
    assert over_limit.value.code == "asset.invalid_dependency_roots"


def test_dependency_closure_supports_deep_graph_within_manifest_limit(tmp_path: Path) -> None:
    uris = tuple(_uri(f"deep/item-{index:04}.json") for index in range(1_100))
    entries = tuple(
        AssetEntry(
            uri,
            AssetKind.JSON,
            f"assets/item-{index:04}.json",
            dependencies=() if index == len(uris) - 1 else (uris[index + 1],),
        )
        for index, uri in enumerate(uris)
    )

    manifest = AssetManifest(tmp_path, entries)

    assert manifest.dependency_closure((uris[0],)) == uris
