"""PR #252 regressions: direct construction bounds and text decoding errors."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from ludoweave.assets import AssetCacheError, AssetCachePopulationRecord
from ludoweave.assets.fingerprint_verification import decode_asset_cache_fingerprint
from ludoweave.scene import PrefabError, PrefabInstance, SceneDocument, SceneError
from ludoweave.scene.document import SceneEntity
from ludoweave.scene.prefab import PrefabOverride


def _entities(count: int) -> tuple[SceneEntity, ...]:
    return tuple(SceneEntity(f"e{i}", f"Entity {i}", None, ()) for i in range(count))


def _overrides(count: int) -> tuple[PrefabOverride, ...]:
    return tuple(PrefabOverride(f"e{i}", "game.Component", 1, {"value": 1}) for i in range(count))


def test_direct_scene_accepts_exact_hard_limit_and_round_trips() -> None:
    scene = SceneDocument("limit", _entities(4_096), ())
    assert len(scene.entities) == 4_096
    assert SceneDocument.from_json(scene.canonical_bytes()) == scene


def test_direct_scene_rejects_one_over_hard_limit() -> None:
    with pytest.raises(SceneError) as caught:
        SceneDocument("limit", _entities(4_097), ())
    assert caught.value.code == "scene.limit_exceeded"
    assert caught.value.phase == "construct"
    assert dict(caught.value.details) == {"field": "entities", "actual": 4_097, "limit": 4_096}


def test_direct_prefab_accepts_exact_hard_limit_and_round_trips() -> None:
    instance = PrefabInstance("limit", "instance", _overrides(4_096))
    assert len(instance.overrides) == 4_096
    assert PrefabInstance.from_json(instance.canonical_bytes()) == instance


def test_direct_prefab_rejects_one_over_hard_limit() -> None:
    with pytest.raises(PrefabError) as caught:
        PrefabInstance("limit", "instance", _overrides(4_097))
    assert caught.value.code == "prefab.limit_exceeded"
    assert caught.value.phase == "construct"
    assert dict(caught.value.details) == {"field": "overrides", "actual": 4_097, "limit": 4_096}


@pytest.mark.parametrize(
    "decoder,code",
    [
        (decode_asset_cache_fingerprint, "asset_cache.invalid_fingerprint_json"),
        (AssetCachePopulationRecord.from_json, "asset_cache.invalid_population_json"),
    ],
)
@pytest.mark.parametrize("document", ["\ud800", "\udfff", '{"private":"\ud800"}', "\ud800\udc00"])
def test_cache_text_encoding_errors_are_structured(
    decoder: Callable[[str | bytes], object], code: str, document: str
) -> None:
    with pytest.raises(AssetCacheError) as caught:
        decoder(document)
    assert caught.value.code == code
    assert caught.value.phase == "decode"
    assert dict(caught.value.details) == {"cause_type": "UnicodeEncodeError"}
    assert isinstance(caught.value.__cause__, UnicodeEncodeError)
    assert "private" not in str(caught.value)


@pytest.mark.parametrize(
    "decoder,code",
    [
        (decode_asset_cache_fingerprint, "asset_cache.invalid_fingerprint_json"),
        (AssetCachePopulationRecord.from_json, "asset_cache.invalid_population_json"),
    ],
)
def test_invalid_utf8_bytes_keep_existing_structured_error(
    decoder: Callable[[str | bytes], object], code: str
) -> None:
    with pytest.raises(AssetCacheError) as caught:
        decoder(b"\xff")
    assert caught.value.code == code
    assert dict(caught.value.details) == {"cause_type": "UnicodeDecodeError"}
    assert isinstance(caught.value.__cause__, UnicodeDecodeError)
