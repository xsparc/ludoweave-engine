"""Monotonic real-time and deterministic virtual-time clocks."""

import time
from typing import Protocol

from ludoweave.core.errors import ClockError


class Clock(Protocol):
    """Clock used by the fixed-tick runner.

    Values are monotonic nanoseconds, never civil or wall-clock timestamps.
    Implementations must not move backward.
    """

    def now_ns(self) -> int:
        """Return the current monotonic time in nanoseconds."""

        ...

    def wait_until_ns(self, deadline_ns: int) -> None:
        """Wait or advance until ``deadline_ns`` is current."""

        ...


def _require_non_negative(value: object, *, field: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ClockError(
            f"{field} must be a non-negative integer",
            code="clock.invalid_value",
            subsystem="clock",
            phase="validation",
            details={"field": field, "value": repr(value)},
        )


class MonotonicClock:
    """Operating-system monotonic clock.

    Waiting may block the owning thread. The implementation uses no wall-clock
    state and owns no resource that needs closing.
    """

    def now_ns(self) -> int:
        return time.monotonic_ns()

    def wait_until_ns(self, deadline_ns: int) -> None:
        _require_non_negative(deadline_ns, field="deadline_ns")
        while True:
            remaining_ns = deadline_ns - self.now_ns()
            if remaining_ns <= 0:
                return
            time.sleep(remaining_ns / 1_000_000_000)


class VirtualClock:
    """Deterministic clock that advances instantly and never sleeps."""

    __slots__ = ("_current_ns",)

    def __init__(self, start_ns: int = 0) -> None:
        _require_non_negative(start_ns, field="start_ns")
        self._current_ns = start_ns

    @property
    def current_ns(self) -> int:
        """Current deterministic time, exposed read-only."""

        return self._current_ns

    def now_ns(self) -> int:
        return self._current_ns

    def advance_ns(self, delta_ns: int) -> int:
        """Advance by a non-negative delta and return the new time."""

        _require_non_negative(delta_ns, field="delta_ns")
        self._current_ns += delta_ns
        return self._current_ns

    def wait_until_ns(self, deadline_ns: int) -> None:
        _require_non_negative(deadline_ns, field="deadline_ns")
        if deadline_ns < self._current_ns:
            raise ClockError(
                "virtual clock cannot move backward",
                code="clock.backward_deadline",
                subsystem="clock",
                phase="wait",
                details={"current_ns": self._current_ns, "deadline_ns": deadline_ns},
            )
        self._current_ns = deadline_ns
