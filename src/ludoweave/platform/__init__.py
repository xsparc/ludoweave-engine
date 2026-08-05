"""Provider-neutral window and input event records."""

from ludoweave.platform.events import (
    CloseEvent,
    FocusEvent,
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
    "InputEvent",
    "KeyEvent",
    "MouseButtonEvent",
    "PlatformEvent",
    "PlatformEventError",
    "PointerEvent",
    "ResizeEvent",
]
__stability__ = {name: "experimental" for name in __all__}
