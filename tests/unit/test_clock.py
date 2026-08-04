"""Monotonic and deterministic virtual clock tests."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.core.clock import MonotonicClock, VirtualClock
from ludoweave.core.errors import ClockError


def test_monotonic_clock_samples_do_not_decrease() -> None:
    clock = MonotonicClock()
    samples = [clock.now_ns() for _ in range(20)]
    assert samples == sorted(samples)


def test_monotonic_clock_waits_until_future_deadline() -> None:
    clock = MonotonicClock()
    deadline_ns = clock.now_ns() + 1_000_000
    clock.wait_until_ns(deadline_ns)
    assert clock.now_ns() >= deadline_ns


def test_virtual_clock_advances_exactly() -> None:
    clock = VirtualClock(start_ns=7)
    assert clock.advance_ns(5) == 12
    clock.wait_until_ns(20)
    assert clock.now_ns() == 20


def test_virtual_clock_rejects_backward_deadline() -> None:
    clock = VirtualClock(start_ns=10)
    with pytest.raises(ClockError, match="cannot move backward"):
        clock.wait_until_ns(9)
    assert clock.now_ns() == 10


@given(st.integers(max_value=-1))
def test_virtual_clock_rejects_negative_deltas(delta_ns: int) -> None:
    clock = VirtualClock()
    with pytest.raises(ClockError, match="non-negative"):
        clock.advance_ns(delta_ns)
