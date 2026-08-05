"""Provider-neutral window and input event records."""

from ludoweave.platform.events import (
    CloseEvent,
    FocusEvent,
    GamepadAxis,
    GamepadAxisEvent,
    GamepadButton,
    GamepadButtonEvent,
    GamepadConnectionEvent,
    GamepadEvent,
    GamepadProvider,
    InputEvent,
    KeyEvent,
    MouseButtonEvent,
    PlatformEvent,
    PlatformEventError,
    PointerEvent,
    ResizeEvent,
)

__all__ = [
    "CloseEvent",
    "FocusEvent",
    "GamepadAxis",
    "GamepadAxisEvent",
    "GamepadButton",
    "GamepadButtonEvent",
    "GamepadConnectionEvent",
    "GamepadEvent",
    "GamepadProvider",
    "InputEvent",
    "KeyEvent",
    "MouseButtonEvent",
    "PlatformEvent",
    "PlatformEventError",
    "PointerEvent",
    "ResizeEvent",
]
__stability__ = {name: "experimental" for name in __all__}
