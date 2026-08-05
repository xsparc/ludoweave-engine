"""Immutable action snapshot and deterministic input-source tests."""

from collections.abc import Iterator, Mapping
from dataclasses import FrozenInstanceError
from math import inf, nan
from typing import TYPE_CHECKING, assert_type, cast

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.app.errors import InputError
from ludoweave.app.input import (
    INPUT_SNAPSHOT_RESOURCE,
    ActionBinding,
    ActionMap,
    FocusEvent,
    GamepadAxis,
    GamepadAxisEvent,
    GamepadButton,
    GamepadButtonEvent,
    GamepadConnectionEvent,
    InputAction,
    InputSnapshot,
    InputSource,
    KeyEvent,
    MappedInputSource,
    MouseButtonEvent,
    NullInputSource,
    PointerEvent,
    RecordedInputSource,
    VirtualInputSource,
)
from ludoweave.ecs import ResourceRegistry, ResourceStore
from ludoweave.platform import PlatformEventError

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


def test_mapped_keyboard_mouse_transitions_axes_pointer_and_focus_loss() -> None:
    source = MappedInputSource(
        ActionMap(
            (
                ActionBinding("move.x", "key:a", -1.0),
                ActionBinding("move.x", "key:d", 1.0),
                ActionBinding("fire", "mouse:primary"),
            )
        )
    )
    source.feed(KeyEvent("D", True))
    source.feed(MouseButtonEvent("PRIMARY", True))
    source.feed(PointerEvent(75.0, 25.0, 100, 100))

    first = source.snapshot_for_tick(0)
    assert first.axis2d("move") == (1.0, 0.0)
    assert first.pressed("fire")
    assert first.just_pressed("fire")
    assert first.value("pointer.x") == 0.5
    assert first.value("pointer.y") == 0.5

    second = source.snapshot_for_tick(1)
    assert second.pressed("fire")
    assert not second.just_pressed("fire")

    source.feed(FocusEvent(False))
    third = source.snapshot_for_tick(2)
    assert third.just_released("fire")
    assert third.axis2d("move") == (0.0, 0.0)


def test_recorded_source_preserves_transition_metadata_from_virtual_capture() -> None:
    mapped = MappedInputSource(ActionMap((ActionBinding("restart", "key:r"),)))
    mapped.feed(KeyEvent("r", True))
    captured = mapped.snapshot_for_tick(0)
    replayed = RecordedInputSource((captured,)).snapshot_for_tick(0)

    assert replayed == captured
    assert replayed.just_pressed("restart")


def test_mapped_source_requires_sequential_sampling_and_valid_bindings() -> None:
    with pytest.raises(InputError):
        ActionMap(
            (
                ActionBinding("mixed", "key:a", True),
                ActionBinding("mixed", "key:b", 1.0),
            )
        )
    source = MappedInputSource(ActionMap(()))
    with pytest.raises(InputError):
        source.snapshot_for_tick(1)


def test_gamepad_events_are_frozen_bounded_and_normalized() -> None:
    connection = GamepadConnectionEvent(0, True)
    button = GamepadButtonEvent(0, GamepadButton.A, True)
    stick = GamepadAxisEvent(0, GamepadAxis.LEFT_X, -1.0)
    trigger = GamepadAxisEvent(0, GamepadAxis.RIGHT_TRIGGER, 1.0)

    assert connection.connected
    assert button.button is GamepadButton.A
    assert stick.value == -1.0
    assert trigger.value == 1.0
    with pytest.raises(FrozenInstanceError):
        connection.slot = 1  # type: ignore[misc]


def test_gamepad_events_require_exact_identities_and_boolean_flags() -> None:
    with pytest.raises(PlatformEventError, match="exact engine-owned identity"):
        GamepadButtonEvent(0, cast(GamepadButton, "a"), True)
    with pytest.raises(PlatformEventError, match="exact engine-owned identity"):
        GamepadAxisEvent(0, cast(GamepadAxis, "left_x"), 0.0)
    with pytest.raises(PlatformEventError, match="exact booleans"):
        GamepadConnectionEvent(0, cast(bool, 1))
    with pytest.raises(PlatformEventError, match="exact booleans"):
        GamepadButtonEvent(0, GamepadButton.A, cast(bool, 1))


@pytest.mark.parametrize("slot", [-1, 16, True, 1.0, "0"])
def test_gamepad_events_reject_invalid_slots(slot: object) -> None:
    with pytest.raises(PlatformEventError, match="gamepad slots"):
        GamepadConnectionEvent(cast(int, slot), True)


@pytest.mark.parametrize("value", [nan, inf, -inf, -1.1, 1.1, 0, True])
def test_gamepad_stick_rejects_invalid_axis_values(value: object) -> None:
    with pytest.raises(PlatformEventError, match="gamepad axis"):
        GamepadAxisEvent(0, GamepadAxis.LEFT_X, cast(float, value))


@pytest.mark.parametrize("value", [-1.0, -0.1, 1.1])
def test_gamepad_trigger_rejects_values_outside_zero_to_one(value: float) -> None:
    with pytest.raises(PlatformEventError, match="gamepad axis"):
        GamepadAxisEvent(0, GamepadAxis.LEFT_TRIGGER, value)


def test_mapped_gamepad_axes_buttons_focus_and_hotplug() -> None:
    source = MappedInputSource(
        ActionMap(
            (
                ActionBinding("move.x", "gamepad:0:axis:left_x", 1.0, 0.2),
                ActionBinding("move.y", "gamepad:0:axis:left_y", -1.0, 0.2),
                ActionBinding("fire", "gamepad:0:button:a"),
            )
        )
    )
    source.feed(GamepadConnectionEvent(0, True))
    source.feed(GamepadAxisEvent(0, GamepadAxis.LEFT_X, 0.1))
    assert source.snapshot_for_tick(0).axis2d("move") == (0.0, 0.0)

    source.feed(GamepadAxisEvent(0, GamepadAxis.LEFT_X, 0.6))
    source.feed(GamepadAxisEvent(0, GamepadAxis.LEFT_Y, -1.0))
    source.feed(GamepadButtonEvent(0, GamepadButton.A, True))
    active = source.snapshot_for_tick(1)
    assert active.axis2d("move") == pytest.approx((0.5, 1.0))
    assert active.pressed("fire")
    assert active.just_pressed("fire")

    source.feed(FocusEvent(False))
    source.feed(GamepadButtonEvent(0, GamepadButton.A, True))
    source.feed(GamepadAxisEvent(0, GamepadAxis.LEFT_X, 1.0))
    unfocused = source.snapshot_for_tick(2)
    assert unfocused.axis2d("move") == (0.0, 0.0)
    assert unfocused.just_released("fire")

    source.feed(FocusEvent(True))
    source.feed(GamepadButtonEvent(0, GamepadButton.A, True))
    source.feed(GamepadAxisEvent(0, GamepadAxis.LEFT_X, 1.0))
    assert source.snapshot_for_tick(3).pressed("fire")
    source.feed(GamepadConnectionEvent(0, False))
    disconnected = source.snapshot_for_tick(4)
    assert disconnected.axis2d("move") == (0.0, 0.0)
    assert disconnected.just_released("fire")


def test_gamepad_axis_bindings_require_analog_scale_and_scoped_deadzone() -> None:
    with pytest.raises(InputError, match="axis binding scale"):
        ActionBinding("move.x", "gamepad:0:axis:left_x")
    with pytest.raises(InputError, match="deadzones"):
        ActionBinding("jump", "gamepad:0:button:a", True, 0.1)
    with pytest.raises(InputError, match="deadzone"):
        ActionBinding("move.x", "gamepad:0:axis:left_x", 1.0, 1.0)
    with pytest.raises(InputError, match="canonical"):
        ActionBinding("move.x", "gamepad:00:axis:left_x", 1.0)


@given(
    value=st.floats(min_value=-1.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    deadzone=st.floats(
        min_value=0.0,
        max_value=0.99,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_gamepad_deadzone_mapping_remains_normalized(value: float, deadzone: float) -> None:
    source = MappedInputSource(
        ActionMap((ActionBinding("move.x", "gamepad:0:axis:left_x", 1.0, deadzone),))
    )
    source.feed(GamepadAxisEvent(0, GamepadAxis.LEFT_X, value))
    mapped = source.snapshot_for_tick(0).value("move.x", 0.0)
    assert type(mapped) is float
    assert -1.0 <= mapped <= 1.0
