"""Immutable deterministic action snapshots and backend-neutral input mapping."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from math import isfinite
from types import MappingProxyType
from typing import Protocol

from ludoweave.app.errors import InputError
from ludoweave.ecs.resources import ResourceSpec
from ludoweave.platform import (
    FocusEvent,
    InputEvent,
    KeyEvent,
    MouseButtonEvent,
    PointerEvent,
)

type ActionValue = bool | float

_ACTION_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_.:-]*\Z")
_CONTROL_NAME = re.compile(r"(?:key|mouse):[A-Za-z0-9_.-]+\Z")


@dataclass(frozen=True, slots=True, eq=False)
class InputAction:
    """One canonical named digital or finite analog action value."""

    name: str
    value: ActionValue

    def __post_init__(self) -> None:
        if type(self.name) is not str or _ACTION_NAME.fullmatch(self.name) is None:
            raise _input_error(
                "input action name must be a stable nonempty identifier",
                phase="snapshot",
                details={"actual_type": type(self.name).__name__},
            )
        if type(self.value) is bool:
            return
        if type(self.value) is not float or not isfinite(self.value):
            raise _input_error(
                "input action value must be an exact bool or finite float",
                phase="snapshot",
                details={
                    "action": self.name,
                    "actual_type": type(self.value).__name__,
                },
            )

    def __eq__(self, other: object) -> bool:
        return (
            type(other) is InputAction
            and self.name == other.name
            and _action_value_signature(self.value) == _action_value_signature(other.value)
        )

    def __hash__(self) -> int:
        return hash((self.name, _action_value_signature(self.value)))


@dataclass(frozen=True, slots=True, init=False)
class InputSnapshot:
    """Canonical immutable action state for one exact zero-based tick."""

    tick: int
    actions: tuple[InputAction, ...]
    just_pressed_actions: tuple[str, ...]
    just_released_actions: tuple[str, ...]

    def __init__(
        self,
        tick: int,
        actions: Iterable[InputAction] = (),
        *,
        just_pressed: Iterable[str] = (),
        just_released: Iterable[str] = (),
    ) -> None:
        checked_tick = _require_tick(tick, phase="snapshot")
        try:
            candidates = tuple(actions)
        except Exception as error:
            raise _input_error(
                "input actions could not be materialized",
                phase="snapshot",
                details={"cause_type": type(error).__name__},
            ) from error
        checked: list[InputAction] = []
        seen: set[str] = set()
        for action in candidates:
            if type(action) is not InputAction:
                raise _input_error(
                    "input snapshot entries must be exact InputAction values",
                    phase="snapshot",
                    details={"actual_type": type(action).__name__},
                )
            if action.name in seen:
                raise _input_error(
                    "input snapshot repeats an action name",
                    phase="snapshot",
                    details={"action": action.name},
                )
            seen.add(action.name)
            checked.append(InputAction(action.name, action.value))
        object.__setattr__(self, "tick", checked_tick)
        object.__setattr__(self, "actions", tuple(sorted(checked, key=lambda item: item.name)))
        pressed = _transition_names(just_pressed, field="just_pressed")
        released = _transition_names(just_released, field="just_released")
        overlap = set(pressed) & set(released)
        if overlap:
            raise _input_error(
                "an action cannot be pressed and released in the same snapshot",
                phase="snapshot",
                details={"action": min(overlap)},
            )
        object.__setattr__(self, "just_pressed_actions", pressed)
        object.__setattr__(self, "just_released_actions", released)

    @classmethod
    def from_mapping(cls, tick: int, actions: Mapping[str, ActionValue]) -> InputSnapshot:
        """Copy and canonicalize one mapping into an immutable snapshot."""

        try:
            entries = tuple(InputAction(name, value) for name, value in actions.items())
        except InputError:
            raise
        except AttributeError as error:
            raise _input_error(
                "input actions must be supplied as a mapping",
                phase="snapshot",
                details={"actual_type": type(actions).__name__},
            ) from error
        except Exception as error:
            raise _input_error(
                "input action mapping could not be materialized",
                phase="snapshot",
                details={"cause_type": type(error).__name__},
            ) from error
        return cls(tick, entries)

    def value(self, name: str, default: ActionValue = False) -> ActionValue:
        """Return one action value without exposing mutable storage."""

        checked = _require_action_lookup(name)
        for action in self.actions:
            if action.name == checked:
                return action.value
        if type(default) is bool:
            return default
        if type(default) is not float or not isfinite(default):
            raise _input_error(
                "input action default must be an exact bool or finite float",
                phase="lookup",
                details={"actual_type": type(default).__name__},
            )
        return default

    def pressed(self, name: str) -> bool:
        """Return whether a digital action is currently pressed."""

        return self.value(name) is True

    def just_pressed(self, name: str) -> bool:
        """Return whether a digital action became pressed on this tick."""

        return _require_action_lookup(name) in self.just_pressed_actions

    def just_released(self, name: str) -> bool:
        """Return whether a digital action became released on this tick."""

        return _require_action_lookup(name) in self.just_released_actions

    def axis2d(self, name: str) -> tuple[float, float]:
        """Return ``<name>.x`` and ``<name>.y`` finite analog values."""

        checked = _require_action_lookup(name)
        x = self.value(f"{checked}.x", 0.0)
        y = self.value(f"{checked}.y", 0.0)
        return (
            x if type(x) is float else 0.0,
            y if type(y) is float else 0.0,
        )


@dataclass(frozen=True, slots=True)
class ActionBinding:
    """Map one provider-neutral control to a digital or analog action value."""

    action: str
    control: str
    value: ActionValue = True

    def __post_init__(self) -> None:
        _require_action_lookup(self.action)
        _require_control_name(self.control)
        if type(self.value) is bool:
            return
        if type(self.value) is not float or not isfinite(self.value) or self.value == 0.0:
            raise _input_error(
                "analog binding value must be a finite nonzero exact float",
                phase="binding",
                details={"action": self.action},
            )


class ActionMap:
    """Immutable canonical set of keyboard and mouse action bindings."""

    __slots__ = ("_bindings",)

    def __init__(self, bindings: Iterable[ActionBinding]) -> None:
        try:
            values = tuple(bindings)
        except Exception as error:
            raise _input_error(
                "action bindings could not be materialized",
                phase="binding",
                details={"cause_type": type(error).__name__},
            ) from error
        if any(type(item) is not ActionBinding for item in values):
            raise _input_error(
                "action map entries must be exact ActionBinding values",
                phase="binding",
                details={"field": "bindings"},
            )
        signatures = {(item.action, item.control) for item in values}
        if len(signatures) != len(values):
            raise _input_error(
                "action map repeats an action/control pair",
                phase="binding",
                details={"field": "bindings"},
            )
        kinds: dict[str, type[bool] | type[float]] = {}
        for item in values:
            kind = bool if type(item.value) is bool else float
            previous = kinds.setdefault(item.action, kind)
            if previous is not kind:
                raise _input_error(
                    "one action cannot mix digital and analog bindings",
                    phase="binding",
                    details={"action": item.action},
                )
        self._bindings = tuple(sorted(values, key=lambda item: (item.action, item.control)))

    @property
    def bindings(self) -> tuple[ActionBinding, ...]:
        return self._bindings


class MappedInputSource:
    """Single-thread event accumulator sampled exactly once per sequential tick."""

    __slots__ = ("_action_map", "_controls", "_last_actions", "_next_tick", "_pointer")

    def __init__(self, action_map: ActionMap) -> None:
        if type(action_map) is not ActionMap:
            raise _input_error(
                "mapped input requires an exact ActionMap",
                phase="binding",
                details={"actual_type": type(action_map).__name__},
            )
        self._action_map = action_map
        self._controls: set[str] = set()
        self._pointer = (0.0, 0.0)
        self._last_actions: dict[str, ActionValue] = {}
        self._next_tick = 0

    def feed(self, event: InputEvent) -> None:
        """Apply one copied provider-neutral event before the next sample."""

        if type(event) is KeyEvent:
            self._set_control(_control("key", event.key), event.pressed)
        elif type(event) is MouseButtonEvent:
            self._set_control(_control("mouse", event.button), event.pressed)
        elif type(event) is PointerEvent:
            self._pointer = event.normalized
        elif type(event) is FocusEvent:
            if not event.focused:
                self._controls.clear()
        else:
            raise _input_error(
                "mapped input requires a provider-neutral input event",
                phase="event",
                details={"actual_type": type(event).__name__},
            )

    def snapshot_for_tick(self, tick: int) -> InputSnapshot:
        checked = _require_tick(tick, phase="sample")
        if checked != self._next_tick:
            raise _input_error(
                "mapped input must be sampled at sequential ticks",
                phase="sample",
                details={"expected_tick": self._next_tick, "actual_tick": checked},
            )
        actions = self._resolve_actions()
        snapshot = _snapshot_with_previous(checked, actions, self._last_actions)
        self._last_actions = actions
        self._next_tick += 1
        return snapshot

    def _set_control(self, control: str, pressed: bool) -> None:
        if pressed:
            self._controls.add(control)
        else:
            self._controls.discard(control)

    def _resolve_actions(self) -> dict[str, ActionValue]:
        digital: dict[str, bool] = {}
        analog: dict[str, float] = {
            "pointer.x": self._pointer[0],
            "pointer.y": self._pointer[1],
        }
        for binding in self._action_map.bindings:
            if binding.control not in self._controls:
                continue
            if type(binding.value) is bool:
                digital[binding.action] = digital.get(binding.action, False) or binding.value
            else:
                analog[binding.action] = min(
                    1.0,
                    max(-1.0, analog.get(binding.action, 0.0) + binding.value),
                )
        return {**digital, **analog}


class InputSource(Protocol):
    """Deterministic source of immutable snapshots indexed by simulation tick."""

    def snapshot_for_tick(self, tick: int) -> InputSnapshot:
        """Return an immutable snapshot whose tick equals the request."""

        ...


class NullInputSource:
    """Input source returning an empty snapshot for every valid tick."""

    __slots__ = ()

    def snapshot_for_tick(self, tick: int) -> InputSnapshot:
        return InputSnapshot(_require_tick(tick, phase="sample"))


class VirtualInputSource:
    """Immutable copied action mapping for deterministic tests and headless runs."""

    __slots__ = ("_snapshots",)

    def __init__(self, timeline: Mapping[int, Mapping[str, ActionValue]] | None = None) -> None:
        snapshots: dict[int, InputSnapshot] = {}
        source: Mapping[int, Mapping[str, ActionValue]] = {} if timeline is None else timeline
        try:
            items = tuple(source.items())
        except AttributeError as error:
            raise _input_error(
                "virtual input timeline must be a mapping",
                phase="timeline",
                details={"actual_type": type(source).__name__},
            ) from error
        except Exception as error:
            raise _input_error(
                "virtual input timeline could not be materialized",
                phase="timeline",
                details={"cause_type": type(error).__name__},
            ) from error
        for tick, actions in items:
            checked_tick = _require_tick(tick, phase="timeline")
            if checked_tick in snapshots:
                raise _input_error(
                    "virtual input timeline repeats a tick",
                    phase="timeline",
                    details={"tick": checked_tick},
                )
            snapshots[checked_tick] = InputSnapshot.from_mapping(checked_tick, actions)
        self._snapshots = MappingProxyType(snapshots)

    def snapshot_for_tick(self, tick: int) -> InputSnapshot:
        checked = _require_tick(tick, phase="sample")
        snapshot = self._snapshots.get(checked)
        if snapshot is None:
            return InputSnapshot(checked)
        return InputSnapshot(
            snapshot.tick,
            snapshot.actions,
            just_pressed=snapshot.just_pressed_actions,
            just_released=snapshot.just_released_actions,
        )


class RecordedInputSource:
    """Immutable in-memory snapshot sequence; not a replay file or codec."""

    __slots__ = ("_snapshots",)

    def __init__(self, snapshots: Iterable[InputSnapshot] = ()) -> None:
        try:
            candidates = tuple(snapshots)
        except Exception as error:
            raise _input_error(
                "recorded input snapshots could not be materialized",
                phase="timeline",
                details={"cause_type": type(error).__name__},
            ) from error
        copied: dict[int, InputSnapshot] = {}
        for candidate in candidates:
            if type(candidate) is not InputSnapshot:
                raise _input_error(
                    "recorded input entries must be exact InputSnapshot values",
                    phase="timeline",
                    details={"actual_type": type(candidate).__name__},
                )
            if candidate.tick in copied:
                raise _input_error(
                    "recorded input timeline repeats a tick",
                    phase="timeline",
                    details={"tick": candidate.tick},
                )
            copied[candidate.tick] = InputSnapshot(
                candidate.tick,
                candidate.actions,
                just_pressed=candidate.just_pressed_actions,
                just_released=candidate.just_released_actions,
            )
        self._snapshots = MappingProxyType(copied)

    def snapshot_for_tick(self, tick: int) -> InputSnapshot:
        checked = _require_tick(tick, phase="sample")
        snapshot = self._snapshots.get(checked)
        if snapshot is None:
            return InputSnapshot(checked)
        return InputSnapshot(
            snapshot.tick,
            snapshot.actions,
            just_pressed=snapshot.just_pressed_actions,
            just_released=snapshot.just_released_actions,
        )


def _copy_input_snapshot(snapshot: InputSnapshot) -> InputSnapshot:
    return InputSnapshot(
        snapshot.tick,
        snapshot.actions,
        just_pressed=snapshot.just_pressed_actions,
        just_released=snapshot.just_released_actions,
    )


def _snapshot_with_previous(
    tick: int,
    actions: Mapping[str, ActionValue],
    previous: Mapping[str, ActionValue],
) -> InputSnapshot:
    pressed = tuple(
        name
        for name, value in actions.items()
        if value is True and previous.get(name, False) is not True
    )
    released = tuple(
        name
        for name, value in previous.items()
        if value is True and actions.get(name, False) is not True
    )
    snapshot = InputSnapshot.from_mapping(tick, actions)
    return InputSnapshot(
        snapshot.tick,
        snapshot.actions,
        just_pressed=pressed,
        just_released=released,
    )


def _action_value_signature(value: ActionValue) -> tuple[str, bool | str]:
    if type(value) is bool:
        return ("bool", value)
    return ("float", value.hex())


INPUT_SNAPSHOT_RESOURCE = ResourceSpec(
    "simulation.input_snapshot",
    InputSnapshot,
    _copy_input_snapshot,
)


def _require_tick(value: object, *, phase: str) -> int:
    if type(value) is not int or value < 0:
        raise _input_error(
            "input tick must be a non-negative integer",
            phase=phase,
            details={"actual_type": type(value).__name__},
        )
    return value


def _require_action_lookup(value: object) -> str:
    if type(value) is not str or _ACTION_NAME.fullmatch(value) is None:
        raise _input_error(
            "input action lookup requires a stable identifier",
            phase="lookup",
            details={"actual_type": type(value).__name__},
        )
    return value


def _transition_names(values: Iterable[str], *, field: str) -> tuple[str, ...]:
    try:
        checked = tuple(_require_action_lookup(value) for value in values)
    except InputError:
        raise
    except Exception as error:
        raise _input_error(
            "input transition names could not be materialized",
            phase="snapshot",
            details={"field": field, "cause_type": type(error).__name__},
        ) from error
    if len(set(checked)) != len(checked):
        raise _input_error(
            "input transition names must be unique",
            phase="snapshot",
            details={"field": field},
        )
    return tuple(sorted(checked))


def _control(prefix: str, value: object) -> str:
    if type(value) is not str or not value:
        raise _input_error(
            "input control must use stable nonempty text",
            phase="event",
            details={"actual_type": type(value).__name__},
        )
    return _require_control_name(f"{prefix}:{value.lower()}")


def _require_control_name(value: object) -> str:
    if type(value) is not str or _CONTROL_NAME.fullmatch(value) is None:
        raise _input_error(
            "input control must be a canonical key: or mouse: identifier",
            phase="binding",
            details={"actual_type": type(value).__name__},
        )
    return value


def _input_error(
    message: str,
    *,
    phase: str,
    details: dict[str, str | int | float | bool | None],
) -> InputError:
    return InputError(
        message,
        code="application.invalid_input",
        subsystem="application",
        phase=phase,
        details=details,
    )
