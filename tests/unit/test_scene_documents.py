"""Versioned, bounded, immutable scene-document tests."""

from __future__ import annotations

import copy
from collections.abc import Callable
from typing import cast

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.scene import SceneDocument, SceneError, SceneLimits

type SceneMapping = dict[str, object]
type SceneMutator = Callable[[SceneMapping], None]


def _scene() -> SceneMapping:
    return {
        "$schema": "ludoweave.scene/1",
        "scene_id": "level-one",
        "entities": [
            {
                "local_id": "root",
                "name": "Level",
                "parent": None,
                "components": {
                    "game.LevelMetadata": {
                        "version": 1,
                        "values": {"theme": "foundry"},
                    }
                },
            },
            {
                "local_id": "player",
                "name": "Player",
                "parent": "root",
                "components": {
                    "game.Transform2D": {
                        "version": 2,
                        "values": {"x": 96.0, "y": 64.0},
                    }
                },
            },
        ],
        "dependencies": ["asset://sprites/player.png", "asset://data/level.json"],
    }


def _entity(value: SceneMapping, index: int) -> SceneMapping:
    entities = cast(list[object], value["entities"])
    return cast(SceneMapping, entities[index])


def _component(value: SceneMapping, entity_index: int, name: str) -> SceneMapping:
    components = cast(SceneMapping, _entity(value, entity_index)["components"])
    return cast(SceneMapping, components[name])


def _extra_field(value: SceneMapping) -> None:
    value["extra"] = True


def _unsupported_protocol(value: SceneMapping) -> None:
    value["$schema"] = "ludoweave.scene/2"


def _duplicate_local_id(value: SceneMapping) -> None:
    entities = cast(list[object], value["entities"])
    entities.append(copy.deepcopy(entities[0]))


def _duplicate_name(value: SceneMapping) -> None:
    _entity(value, 1)["name"] = "Level"


def _missing_parent(value: SceneMapping) -> None:
    _entity(value, 1)["parent"] = "missing"


def _self_parent(value: SceneMapping) -> None:
    _entity(value, 0)["parent"] = "root"


def _parent_cycle(value: SceneMapping) -> None:
    _entity(value, 0)["parent"] = "player"


def _invalid_asset(value: SceneMapping) -> None:
    value["dependencies"] = ["file://secret"]


def _duplicate_asset(value: SceneMapping) -> None:
    value["dependencies"] = ["asset://same", "asset://same"]


def _boolean_component_version(value: SceneMapping) -> None:
    _component(value, 0, "game.LevelMetadata")["version"] = True


def test_scene_document_normalizes_and_round_trips_canonically() -> None:
    scene = SceneDocument.from_mapping(_scene())

    assert scene.protocol == "ludoweave.scene/1"
    assert scene.scene_id == "level-one"
    assert tuple(entity.local_id for entity in scene.entities) == ("player", "root")
    assert tuple(item.value for item in scene.dependencies) == (
        "asset://data/level.json",
        "asset://sprites/player.png",
    )
    assert SceneDocument.from_json(scene.canonical_bytes()) == scene
    assert scene.canonical_bytes() == SceneDocument.from_mapping(scene.as_dict()).canonical_bytes()


def test_scene_document_detaches_nested_input() -> None:
    source = _scene()
    scene = SceneDocument.from_mapping(source)
    baseline = scene.canonical_bytes()

    entities = source["entities"]
    assert isinstance(entities, list)
    root = cast(SceneMapping, entities[0])
    root["name"] = "Mutated"

    assert scene.canonical_bytes() == baseline


@pytest.mark.parametrize(
    ("mutate", "match"),
    [
        (_extra_field, "fields"),
        (_unsupported_protocol, "protocol"),
        (_duplicate_local_id, "local ID"),
        (_duplicate_name, "name"),
        (_missing_parent, "parent"),
        (_self_parent, "parent"),
        (_parent_cycle, "cycle"),
        (_invalid_asset, "asset"),
        (_duplicate_asset, "repeat"),
        (_boolean_component_version, "version"),
    ],
)
def test_scene_document_rejects_invalid_shapes(mutate: SceneMutator, match: str) -> None:
    source = _scene()
    mutate(source)

    with pytest.raises(SceneError, match=match):
        SceneDocument.from_mapping(source)


def test_scene_limits_are_exact_positive_values() -> None:
    with pytest.raises(SceneError, match="positive"):
        SceneLimits(max_entities=0)

    with pytest.raises(SceneError, match="entity limit"):
        SceneDocument.from_mapping(_scene(), limits=SceneLimits(max_entities=1))

    with pytest.raises(SceneError, match="hard maxima"):
        SceneLimits(max_bytes=4_194_305)


@given(st.integers(max_value=0))
def test_scene_limits_reject_every_non_positive_entity_limit(value: int) -> None:
    with pytest.raises(SceneError, match="positive"):
        SceneLimits(max_entities=value)


def test_duplicate_json_member_is_rejected_before_scene_decoding() -> None:
    document = b'{"$schema":"ludoweave.scene/1","scene_id":"a","scene_id":"b"}'

    with pytest.raises(SceneError) as captured:
        SceneDocument.from_json(document)

    assert captured.value.code == "scene.invalid_json"
