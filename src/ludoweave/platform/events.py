"""Immutable provider-neutral logical-surface event records."""

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite
from typing import Protocol

from ludoweave.core.errors import LudoWeaveError


class PlatformEventError(LudoWeaveError):
    """Raised when an adapter emits an invalid logical-surface event."""


class GamepadButton(StrEnum):
    """Standardized Xbox-like gamepad button locations."""

    A = "a"
    B = "b"
    X = "x"
    Y = "y"
    LEFT_BUMPER = "left_bumper"
    RIGHT_BUMPER = "right_bumper"
    BACK = "back"
    START = "start"
    GUIDE = "guide"
    LEFT_STICK = "left_stick"
    RIGHT_STICK = "right_stick"
    DPAD_UP = "dpad_up"
    DPAD_RIGHT = "dpad_right"
    DPAD_DOWN = "dpad_down"
    DPAD_LEFT = "dpad_left"


class GamepadAxis(StrEnum):
    """Standardized gamepad stick and trigger axes."""

    LEFT_X = "left_x"
    LEFT_Y = "left_y"
    RIGHT_X = "right_x"
    RIGHT_Y = "right_y"
    LEFT_TRIGGER = "left_trigger"
    RIGHT_TRIGGER = "right_trigger"


@dataclass(frozen=True, slots=True)
class KeyEvent:
    key: str
    pressed: bool

    def __post_init__(self) -> None:
        _name(self.key, field="key")
        _bool(self.pressed, field="pressed")


@dataclass(frozen=True, slots=True)
class MouseButtonEvent:
    button: str
    pressed: bool

    def __post_init__(self) -> None:
        _name(self.button, field="button")
        _bool(self.pressed, field="pressed")


@dataclass(frozen=True, slots=True)
class GamepadConnectionEvent:
    """Report whether one bounded logical player slot is connected."""

    slot: int
    connected: bool

    def __post_init__(self) -> None:
        _gamepad_slot(self.slot)
        _bool(self.connected, field="connected")


@dataclass(frozen=True, slots=True)
class GamepadButtonEvent:
    """Report one standardized digital gamepad control."""

    slot: int
    button: GamepadButton
    pressed: bool

    def __post_init__(self) -> None:
        _gamepad_slot(self.slot)
        if type(self.button) is not GamepadButton:
            raise _event_error(
                "gamepad buttons must use an exact engine-owned identity",
                field="button",
            )
        _bool(self.pressed, field="pressed")


@dataclass(frozen=True, slots=True)
class GamepadAxisEvent:
    """Report one normalized gamepad axis value.

    Stick axes use ``[-1.0, 1.0]``. Trigger axes use ``[0.0, 1.0]``.
    """

    slot: int
    axis: GamepadAxis
    value: float

    def __post_init__(self) -> None:
        _gamepad_slot(self.slot)
        if type(self.axis) is not GamepadAxis:
            raise _event_error(
                "gamepad axes must use an exact engine-owned identity",
                field="axis",
            )
        if type(self.value) is not float or not isfinite(self.value):
            raise _event_error(
                "gamepad axis values must be finite exact floats",
                field="value",
            )
        minimum = 0.0 if self.axis in _TRIGGER_AXES else -1.0
        if not minimum <= self.value <= 1.0:
            raise _event_error(
                "gamepad axis value is outside its normalized range",
                field="value",
            )


@dataclass(frozen=True, slots=True)
class PointerEvent:
    x: float
    y: float
    surface_width: int
    surface_height: int

    def __post_init__(self) -> None:
        if (
            type(self.x) is not float
            or type(self.y) is not float
            or not isfinite(self.x)
            or not isfinite(self.y)
        ):
            raise _event_error("pointer coordinates must be finite exact floats", field="position")
        _size(self.surface_width, field="surface_width")
        _size(self.surface_height, field="surface_height")

    @property
    def normalized(self) -> tuple[float, float]:
        return (
            min(1.0, max(-1.0, self.x * 2.0 / self.surface_width - 1.0)),
            min(1.0, max(-1.0, 1.0 - self.y * 2.0 / self.surface_height)),
        )


@dataclass(frozen=True, slots=True)
class FocusEvent:
    focused: bool

    def __post_init__(self) -> None:
        _bool(self.focused, field="focused")


@dataclass(frozen=True, slots=True)
class ResizeEvent:
    width: int
    height: int

    def __post_init__(self) -> None:
        _size(self.width, field="width")
        _size(self.height, field="height")


@dataclass(frozen=True, slots=True)
class CloseEvent:
    """Signal that the user requested logical-surface closure."""


type GamepadEvent = GamepadConnectionEvent | GamepadButtonEvent | GamepadAxisEvent
type InputEvent = (
    KeyEvent
    | MouseButtonEvent
    | GamepadConnectionEvent
    | GamepadButtonEvent
    | GamepadAxisEvent
    | PointerEvent
    | FocusEvent
)
type PlatformEvent = InputEvent | ResizeEvent | CloseEvent


class GamepadProvider(Protocol):
    """Single-owner provider of copied, standardized gamepad events."""

    def poll_gamepads(self) -> tuple[GamepadEvent, ...]:
        """Poll current supported controls in stable slot/control order.

        A provider omits controls whose presence or neutral value it cannot
        determine; it must never synthesize an active value for them.
        """

        ...

    def close(self) -> None:
        """Release provider-owned resources; repeated close is safe."""

        ...


_TRIGGER_AXES = frozenset((GamepadAxis.LEFT_TRIGGER, GamepadAxis.RIGHT_TRIGGER))


def _name(value: object, *, field: str) -> str:
    if (
        type(value) is not str
        or not value
        or len(value) > 128
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise _event_error("platform event names must use bounded visible text", field=field)
    return value


def _bool(value: object, *, field: str) -> bool:
    if type(value) is not bool:
        raise _event_error("platform event flags must be exact booleans", field=field)
    return value


def _size(value: object, *, field: str) -> int:
    if type(value) is not int or value <= 0:
        raise _event_error("logical-surface dimensions must be positive integers", field=field)
    return value


def _gamepad_slot(value: object) -> int:
    if type(value) is not int or not 0 <= value <= 15:
        raise _event_error(
            "gamepad slots must be exact integers between 0 and 15",
            field="slot",
        )
    return value


def _event_error(message: str, *, field: str) -> PlatformEventError:
    return PlatformEventError(
        message,
        code="platform.invalid_event",
        subsystem="platform",
        phase="event",
        details={"field": field},
    )
