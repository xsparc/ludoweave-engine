"""Bounded data-only prefab fragment and instance document tests."""

from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from typing import cast

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.scene import (
    PREFAB_INSTANCE_PROTOCOL,
    PREFAB_PROTOCOL,
    PrefabDocument,
    PrefabError,
    PrefabInstance,
    PrefabLimits,
)
from ludoweave.world.canonical import JsonValue

PrefabMapping = dict[str, JsonValue]
PrefabMutator = Callable[[PrefabMapping], None]


def _prefab() -> PrefabMapping:
    return {
        "$schema": PREFAB_PROTOCOL,
        "prefab_id": "enemy.scout",
        "entities": [
            {
                "local_id": "root",
                "name": "Scout",
                "parent": None,
                "components": {
                    "game.Transform2D": {
                        "version": 1,
                        "values": {"x": 2.0, "y": 3.0},
                    }
                },
            },
            {
                "local_id": "sensor",
                "name": "Sensor",
                "parent": "root",
                "components": {"game.Sensor": {"version": 1, "values": {"radius": 4.0}}},
            },
        ],
        "dependencies": ["asset://sprites/scout.png", "asset://audio/scout.wav"],
    }


def _instance() -> PrefabMapping:
    return {
        "$schema": PREFAB_INSTANCE_PROTOCOL,
        "prefab_id": "enemy.scout",
        "instance_id": "scout-one",
        "overrides": [
            {
                "local_id": "sensor",
                "component": "game.Sensor",
                "version": 1,
                "changes": {"radius": 8.0},
            },
            {
                "local_id": "root",
                "component": "game.Transform2D",
                "version": 1,
                "changes": {"x": 5.0},
            },
        ],
    }


def _unsupported_prefab_protocol(value: PrefabMapping) -> None:
    value["$schema"] = "ludoweave.prefab/2"


def _nested_prefabs(value: PrefabMapping) -> None:
    value["nested_prefabs"] = []


def _invalid_prefab_id(value: PrefabMapping) -> None:
    value["prefab_id"] = "bad id"


def _duplicate_prefab_entity(value: PrefabMapping) -> None:
    entities = cast(list[JsonValue], value["entities"])
    entities.append(deepcopy(entities[0]))


def _unsupported_instance_protocol(value: PrefabMapping) -> None:
    value["$schema"] = "ludoweave.prefab-instance/2"


def _instance_parameters(value: PrefabMapping) -> None:
    value["parameters"] = {}


def _empty_changes(value: PrefabMapping) -> None:
    overrides = cast(list[JsonValue], value["overrides"])
    override = cast(dict[str, JsonValue], overrides[0])
    override["changes"] = {}


def _duplicate_override(value: PrefabMapping) -> None:
    overrides = cast(list[JsonValue], value["overrides"])
    overrides.append(deepcopy(overrides[0]))


def test_prefab_document_normalizes_detaches_and_round_trips() -> None:
    source = _prefab()
    original = deepcopy(source)
    prefab = PrefabDocument.from_mapping(source)
    source["prefab_id"] = "mutated"

    assert prefab.prefab_id == "enemy.scout"
    assert tuple(entity.local_id for entity in prefab.entities) == ("root", "sensor")
    assert tuple(item.value for item in prefab.dependencies) == (
        "asset://audio/scout.wav",
        "asset://sprites/scout.png",
    )
    assert prefab.as_dict() == PrefabDocument.from_mapping(original).as_dict()
    assert PrefabDocument.from_json(prefab.canonical_bytes()) == prefab


def test_prefab_instance_normalizes_detaches_and_round_trips() -> None:
    source = _instance()
    original = deepcopy(source)
    instance = PrefabInstance.from_mapping(source)
    overrides = cast(list[JsonValue], source["overrides"])
    first = cast(dict[str, JsonValue], overrides[0])
    changes = cast(dict[str, JsonValue], first["changes"])
    changes["radius"] = 99.0

    assert tuple((item.local_id, item.qualified_name) for item in instance.overrides) == (
        ("root", "game.Transform2D"),
        ("sensor", "game.Sensor"),
    )
    assert instance.as_dict() == PrefabInstance.from_mapping(original).as_dict()
    assert PrefabInstance.from_json(instance.canonical_bytes()) == instance


@pytest.mark.parametrize(
    "mutate, expected_code",
    [
        (_unsupported_prefab_protocol, "prefab.incompatible_protocol"),
        (_nested_prefabs, "prefab.invalid_document"),
        (_invalid_prefab_id, "prefab.invalid_document"),
        (_duplicate_prefab_entity, "prefab.invalid_fragment"),
    ],
)
def test_prefab_document_rejects_invalid_or_nested_shapes(
    mutate: PrefabMutator, expected_code: str
) -> None:
    value = _prefab()
    mutate(value)
    with pytest.raises(PrefabError) as captured:
        PrefabDocument.from_mapping(value)
    assert captured.value.code == expected_code


@pytest.mark.parametrize(
    "mutate, expected_code",
    [
        (_unsupported_instance_protocol, "prefab.incompatible_protocol"),
        (_instance_parameters, "prefab.invalid_document"),
        (_empty_changes, "prefab.invalid_override"),
        (_duplicate_override, "prefab.duplicate_override"),
    ],
)
def test_prefab_instance_rejects_invalid_shapes(mutate: PrefabMutator, expected_code: str) -> None:
    value = _instance()
    mutate(value)
    with pytest.raises(PrefabError) as captured:
        PrefabInstance.from_mapping(value)
    assert captured.value.code == expected_code


def test_prefab_limits_bound_override_count_and_fields() -> None:
    instance = _instance()
    with pytest.raises(PrefabError) as count_error:
        PrefabInstance.from_mapping(instance, limits=PrefabLimits(max_overrides=1))
    assert count_error.value.code == "prefab.limit_exceeded"

    overrides = cast(list[JsonValue], instance["overrides"])
    first = cast(dict[str, JsonValue], overrides[0])
    first["changes"] = {"radius": 8.0, "enabled": True}
    with pytest.raises(PrefabError) as fields_error:
        PrefabInstance.from_mapping(instance, limits=PrefabLimits(max_fields_per_override=1))
    assert fields_error.value.code == "prefab.limit_exceeded"

    with pytest.raises(PrefabError, match="hard maxima"):
        PrefabLimits(max_overrides=4_097)
    with pytest.raises(PrefabError, match="positive"):
        PrefabLimits(max_fields_per_override=cast(int, True))


@given(st.integers(max_value=0))
def test_prefab_limits_reject_non_positive_override_limits(value: int) -> None:
    with pytest.raises(PrefabError, match="positive"):
        PrefabLimits(max_overrides=value)


def test_duplicate_json_members_fail_before_prefab_decoding() -> None:
    with pytest.raises(PrefabError) as captured:
        PrefabInstance.from_json(
            '{"$schema":"ludoweave.prefab-instance/1",'
            '"prefab_id":"one","prefab_id":"two",'
            '"instance_id":"instance","overrides":[]}'
        )
    assert captured.value.code == "prefab.invalid_json"
