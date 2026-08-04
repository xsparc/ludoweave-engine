"""Immutable deterministic action snapshots and in-memory input sources."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from math import isfinite
from types import MappingProxyType
from typing import Protocol

from ludoweave.app.errors import InputError
from ludoweave.ecs.resources import ResourceSpec

type ActionValue = bool | float

_ACTION_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_.:-]*\Z")


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

    def __init__(self, tick: int, actions: Iterable[InputAction] = ()) -> None:
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
        return InputSnapshot(snapshot.tick, snapshot.actions)


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
            copied[candidate.tick] = InputSnapshot(candidate.tick, candidate.actions)
        self._snapshots = MappingProxyType(copied)

    def snapshot_for_tick(self, tick: int) -> InputSnapshot:
        checked = _require_tick(tick, phase="sample")
        snapshot = self._snapshots.get(checked)
        if snapshot is None:
            return InputSnapshot(checked)
        return InputSnapshot(snapshot.tick, snapshot.actions)


def _copy_input_snapshot(snapshot: InputSnapshot) -> InputSnapshot:
    return InputSnapshot(snapshot.tick, snapshot.actions)


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
