"""Immutable provider-neutral logical-surface event records."""

from dataclasses import dataclass
from math import isfinite

from ludoweave.core.errors import LudoWeaveError


class PlatformEventError(LudoWeaveError):
    """Raised when an adapter emits an invalid logical-surface event."""


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


type InputEvent = KeyEvent | MouseButtonEvent | PointerEvent | FocusEvent
type PlatformEvent = InputEvent | ResizeEvent | CloseEvent


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


def _event_error(message: str, *, field: str) -> PlatformEventError:
    return PlatformEventError(
        message,
        code="platform.invalid_event",
        subsystem="platform",
        phase="event",
        details={"field": field},
    )
