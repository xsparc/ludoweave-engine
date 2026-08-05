# pyright: reportPrivateUsage=false
"""Pinned GLFW gamepad translation tests without physical hardware."""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar

import pytest

from ludoweave.platform import (
    FocusEvent,
    GamepadAxis,
    GamepadAxisEvent,
    GamepadButton,
    GamepadButtonEvent,
    GamepadConnectionEvent,
    PlatformEventError,
)
from ludoweave.render.backends.wgpu import _GlfwGamepadPoller, _read_glfw_focus


@dataclass
class _State:
    buttons: Sequence[int]
    axes: Sequence[float]


class _Api:
    def __init__(self) -> None:
        self.states: dict[int, _State | None] = {}
        self.failure: Exception | None = None
        self.query_error = 0
        self._last_error = 0

    def get_gamepad_state(self, slot: int) -> _State | None:
        if self.failure is not None:
            raise self.failure
        self._last_error = self.query_error
        return self.states.get(slot)

    def get_error(self) -> tuple[int, bytes | None]:
        result = self._last_error
        self._last_error = 0
        return result, None


class _WindowApi:
    FOCUSED: ClassVar[int] = 0x00020001

    def __init__(self) -> None:
        self.focused: object = 1
        self.failure: Exception | None = None
        self.query_error = 0
        self._last_error = 0

    def get_window_attrib(self, window: object, attribute: int) -> int:
        assert window is _WINDOW
        assert attribute == self.FOCUSED
        if self.failure is not None:
            raise self.failure
        self._last_error = self.query_error
        return self.focused  # type: ignore[return-value]

    def get_error(self) -> tuple[int, bytes | None]:
        result = self._last_error
        self._last_error = 0
        return result, None


_WINDOW = object()


def test_glfw_poller_emits_complete_ordered_state_and_hotplug() -> None:
    api = _Api()
    api.states[1] = _State(
        [1, *([0] * 14)],
        [-1.0, 0.25, 0.0, 1.0, -1.0, 1.0],
    )
    poller = _GlfwGamepadPoller(api)

    first = poller.poll()
    assert first[0] == GamepadConnectionEvent(1, True)
    assert first[1] == GamepadButtonEvent(1, GamepadButton.A, True)
    assert first[15] == GamepadButtonEvent(1, GamepadButton.DPAD_LEFT, False)
    assert first[16] == GamepadAxisEvent(1, GamepadAxis.LEFT_X, -1.0)
    assert first[-1] == GamepadAxisEvent(1, GamepadAxis.RIGHT_Y, 1.0)
    assert not any(
        type(event) is GamepadAxisEvent
        and event.axis in (GamepadAxis.LEFT_TRIGGER, GamepadAxis.RIGHT_TRIGGER)
        for event in first
    )
    assert len(first) == 20

    second = poller.poll()
    assert len(second) == 19
    assert not any(type(event) is GamepadConnectionEvent for event in second)

    api.states[1] = None
    assert poller.poll() == (GamepadConnectionEvent(1, False),)
    assert poller.poll() == ()


def test_glfw_poller_rejects_malformed_or_failed_provider_state_with_cause() -> None:
    api = _Api()
    api.states[0] = _State([0], [0.0])
    poller = _GlfwGamepadPoller(api)
    with pytest.raises(PlatformEventError) as malformed:
        poller.poll()
    assert malformed.value.code == "platform.gamepad_provider_failure"
    assert isinstance(malformed.value.__cause__, ValueError)

    api.failure = RuntimeError("provider failed")
    with pytest.raises(PlatformEventError) as failed:
        poller.poll()
    assert dict(failed.value.details)["backend"] == "glfw"
    assert isinstance(failed.value.__cause__, RuntimeError)


def test_glfw_poller_distinguishes_query_error_from_disconnection() -> None:
    api = _Api()
    api.query_error = 65537

    with pytest.raises(PlatformEventError) as failure:
        _GlfwGamepadPoller(api).poll()

    assert failure.value.code == "platform.gamepad_provider_failure"
    assert dict(failure.value.details)["provider_code"] == 65537
    assert isinstance(failure.value.__cause__, RuntimeError)


def test_glfw_poller_orders_multiple_occupied_slots() -> None:
    api = _Api()
    state = _State([0] * 15, [0.0] * 6)
    api.states[9] = state
    api.states[2] = state

    events = _GlfwGamepadPoller(api).poll()

    connections = tuple(event for event in events if type(event) is GamepadConnectionEvent)
    assert connections == (
        GamepadConnectionEvent(2, True),
        GamepadConnectionEvent(9, True),
    )
    assert all(event.slot == 2 for event in events[:20])
    assert all(event.slot == 9 for event in events[20:])


def test_glfw_focus_reader_emits_only_transitions_and_rejects_failures() -> None:
    api = _WindowApi()

    focused, event = _read_glfw_focus(api, _WINDOW, None)
    assert focused is True
    assert event == FocusEvent(True)
    assert _read_glfw_focus(api, _WINDOW, focused) == (True, None)

    api.focused = 0
    assert _read_glfw_focus(api, _WINDOW, focused) == (False, FocusEvent(False))

    api.focused = "false"
    with pytest.raises(PlatformEventError, match="focus"):
        _read_glfw_focus(api, _WINDOW, False)

    api.failure = RuntimeError("provider failed")
    with pytest.raises(PlatformEventError) as failure:
        _read_glfw_focus(api, _WINDOW, False)
    assert isinstance(failure.value.__cause__, RuntimeError)


def test_glfw_focus_reader_distinguishes_query_error_from_unfocused() -> None:
    api = _WindowApi()
    api.focused = 0
    api.query_error = 65537

    with pytest.raises(PlatformEventError) as failure:
        _read_glfw_focus(api, _WINDOW, True)

    assert failure.value.code == "platform.focus_provider_failure"
    assert dict(failure.value.details)["provider_code"] == 65537
    assert isinstance(failure.value.__cause__, RuntimeError)
