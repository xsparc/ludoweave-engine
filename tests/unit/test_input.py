"""Immutable action snapshot and deterministic input-source tests."""

from collections.abc import Iterator, Mapping
from dataclasses import FrozenInstanceError
from math import inf, nan
from typing import TYPE_CHECKING, assert_type, cast

import pytest

from ludoweave.app.errors import InputError
from ludoweave.app.input import (
    INPUT_SNAPSHOT_RESOURCE,
    InputAction,
    InputSnapshot,
    InputSource,
    NullInputSource,
    RecordedInputSource,
    VirtualInputSource,
)
from ludoweave.ecs import ResourceRegistry, ResourceStore

if TYPE_CHECKING:
    assert_type(INPUT_SNAPSHOT_RESOURCE.value_type, type[InputSnapshot])


class HostileActionMapping(Mapping[str, bool | float]):
    def __getitem__(self, key: str) -> bool | float:
        raise KeyError(key)

    def __iter__(self) -> Iterator[str]:
        raise RuntimeError("bad items")

    def __len__(self) -> int:
        return 1


class HostileTimeline(Mapping[int, Mapping[str, bool | float]]):
    def __getitem__(self, key: int) -> Mapping[str, bool | float]:
        raise KeyError(key)

    def __iter__(self) -> Iterator[int]:
        raise RuntimeError("bad items")

    def __len__(self) -> int:
        return 1


def test_snapshot_is_canonical_frozen_and_supports_exact_lookup() -> None:
    snapshot = InputSnapshot(
        3,
        (
            InputAction("move.x", 0.5),
            InputAction("jump", True),
        ),
    )

    assert snapshot.actions == (
        InputAction("jump", True),
        InputAction("move.x", 0.5),
    )
    assert snapshot.value("jump") is True
    assert snapshot.value("move.x") == 0.5
    assert snapshot.value("missing") is False
    assert snapshot.value("missing", -0.25) == -0.25
    with pytest.raises(FrozenInstanceError):
        snapshot.tick = 4  # type: ignore[misc]


@pytest.mark.parametrize("tick", [-1, True, 1.0, "1"])
def test_snapshot_rejects_invalid_ticks(tick: object) -> None:
    with pytest.raises(InputError):
        InputSnapshot(cast(int, tick))


@pytest.mark.parametrize("name", ["", "bad name", "9bad", "line\nbreak"])
def test_action_rejects_unstable_names(name: str) -> None:
    with pytest.raises(InputError):
        InputAction(name, True)


@pytest.mark.parametrize("value", [0, 1, nan, inf, -inf, None, "true", object()])
def test_action_rejects_values_outside_exact_bool_finite_float_domain(value: object) -> None:
    with pytest.raises(InputError):
        InputAction("action", cast(bool | float, value))


def test_snapshot_rejects_duplicates_and_non_action_entries() -> None:
    with pytest.raises(InputError):
        InputSnapshot(0, (InputAction("jump", True), InputAction("jump", False)))
    with pytest.raises(InputError):
        InputSnapshot(0, cast(tuple[InputAction, ...], (object(),)))


def test_hostile_mapping_materialization_raises_chained_input_errors() -> None:
    with pytest.raises(InputError) as snapshot_error:
        InputSnapshot.from_mapping(0, HostileActionMapping())
    assert isinstance(snapshot_error.value.__cause__, RuntimeError)

    with pytest.raises(InputError) as timeline_error:
        VirtualInputSource(HostileTimeline())
    assert isinstance(timeline_error.value.__cause__, RuntimeError)


def test_action_and_snapshot_equality_preserve_exact_value_semantics() -> None:
    digital = InputSnapshot.from_mapping(0, {"x": True})
    analog = InputSnapshot.from_mapping(0, {"x": 1.0})
    negative_zero = InputSnapshot.from_mapping(0, {"x": -0.0})
    positive_zero = InputSnapshot.from_mapping(0, {"x": 0.0})

    assert digital != analog
    assert negative_zero != positive_zero
    assert len({digital.actions[0], analog.actions[0]}) == 2
    assert len({negative_zero.actions[0], positive_zero.actions[0]}) == 2


def test_virtual_and_recorded_sources_are_owned_repeatable_and_equivalent() -> None:
    tick_actions: dict[str, bool | float] = {"move.x": 1.0, "jump": True}
    timeline = {2: tick_actions}
    virtual = VirtualInputSource(timeline)
    original = InputSnapshot.from_mapping(2, tick_actions)
    recorded = RecordedInputSource((original,))
    tick_actions["move.x"] = -1.0
    timeline[3] = {"late": True}

    for source in (virtual, recorded):
        first = source.snapshot_for_tick(2)
        second = source.snapshot_for_tick(2)
        assert (
            first
            == second
            == InputSnapshot(
                2,
                (InputAction("jump", True), InputAction("move.x", 1.0)),
            )
        )
        assert first is not second
        assert source.snapshot_for_tick(1) == InputSnapshot(1)
        assert source.snapshot_for_tick(3) == InputSnapshot(3)


def test_null_source_and_protocol_return_requested_empty_tick() -> None:
    source: InputSource = NullInputSource()
    assert source.snapshot_for_tick(99) == InputSnapshot(99)


def test_recorded_source_rejects_duplicate_ticks_and_malformed_entries() -> None:
    with pytest.raises(InputError):
        RecordedInputSource((InputSnapshot(1), InputSnapshot(1)))
    with pytest.raises(InputError):
        RecordedInputSource(cast(tuple[InputSnapshot, ...], (object(),)))


def test_input_resource_copier_returns_an_equal_detached_snapshot() -> None:
    source = InputSnapshot(4, (InputAction("jump", True),))
    store = ResourceStore(ResourceRegistry((INPUT_SNAPSHOT_RESOURCE,)))
    store.insert(INPUT_SNAPSHOT_RESOURCE, source)
    copied = store.require(INPUT_SNAPSHOT_RESOURCE)

    assert copied == source
    assert copied is not source
