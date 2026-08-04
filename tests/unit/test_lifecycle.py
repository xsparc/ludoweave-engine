"""Engine lifecycle, ownership, and cleanup tests."""

from collections.abc import Callable
from threading import Thread
from typing import cast

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave import Engine, EngineConfig, LifecycleState
from ludoweave.app import RunSummary
from ludoweave.core.clock import VirtualClock
from ludoweave.core.errors import ConfigurationError, LifecycleError
from ludoweave.render import NullRenderBackend, RenderDescriptor


class RecordingBackend:
    def __init__(
        self,
        *,
        fail_initialize: bool = False,
        fail_render: bool = False,
        fail_close: bool = False,
    ) -> None:
        self.fail_initialize = fail_initialize
        self.fail_render = fail_render
        self.fail_close = fail_close
        self.initialize_calls = 0
        self.close_calls = 0
        self.frames: list[int] = []

    @property
    def name(self) -> str:
        return "recording"

    def initialize(self, descriptor: RenderDescriptor) -> None:
        self.initialize_calls += 1
        if self.fail_initialize:
            raise RuntimeError("deliberate initialization failure")

    def render(self, *, tick: int) -> None:
        if self.fail_render:
            raise RuntimeError("deliberate render failure")
        self.frames.append(tick)

    def close(self) -> None:
        self.close_calls += 1
        if self.fail_close:
            raise RuntimeError("deliberate close failure")


def _new_engine() -> tuple[Engine, NullRenderBackend, VirtualClock]:
    backend = NullRenderBackend()
    clock = VirtualClock(start_ns=7)
    return Engine(EngineConfig(), backend, clock=clock), backend, clock


def _run_from_created(engine: Engine) -> object:
    return engine.run(ticks=1)


def _shutdown_from_created(engine: Engine) -> None:
    engine.shutdown()


def test_valid_lifecycle_transitions_and_exact_deadlines() -> None:
    engine, backend, clock = _new_engine()
    assert engine.state is LifecycleState.CREATED

    engine.initialize()
    assert engine.state is LifecycleState.READY

    summary = engine.run(ticks=3)
    assert summary == RunSummary(
        ticks=3,
        frames=3,
        start_ns=7,
        end_ns=50_000_007,
        fixed_hz=60,
        renderer="null",
    )
    assert engine.state is LifecycleState.STOPPED
    assert clock.now_ns() == 50_000_007
    assert backend.frame_count == 3

    engine.close()
    engine.close()
    assert engine.state is LifecycleState.CLOSED


def test_shutdown_from_ready_then_close() -> None:
    engine, backend, _clock = _new_engine()
    engine.initialize()
    engine.shutdown()
    assert engine.state is LifecycleState.STOPPED
    engine.close()
    assert backend.is_closed


def test_context_manager_closes_after_normal_run() -> None:
    engine, backend, _clock = _new_engine()
    with engine:
        summary = engine.run(ticks=1)
        assert summary.ticks == 1
        assert engine.state is LifecycleState.STOPPED
    assert engine.state is LifecycleState.CLOSED
    assert backend.is_closed


def test_context_manager_closes_owned_backend_exactly_once() -> None:
    backend = RecordingBackend()
    engine = Engine(EngineConfig(), backend, clock=VirtualClock())
    with engine:
        engine.run(ticks=1)
    engine.close()

    assert backend.close_calls == 1


def test_initialization_failure_closes_backend_and_preserves_cause() -> None:
    backend = RecordingBackend(fail_initialize=True)
    engine = Engine(EngineConfig(), backend, clock=VirtualClock())

    with pytest.raises(LifecycleError, match="initialization failed") as captured:
        engine.initialize()

    assert engine.state is LifecycleState.CLOSED
    assert backend.initialize_calls == 1
    assert backend.close_calls == 1
    assert isinstance(captured.value.__cause__, RuntimeError)
    assert dict(captured.value.details)["cause_type"] == "RuntimeError"


def test_close_failure_still_leaves_engine_closed() -> None:
    backend = RecordingBackend(fail_close=True)
    engine = Engine(EngineConfig(), backend, clock=VirtualClock())
    with pytest.raises(LifecycleError, match="close failed"):
        engine.close()
    assert engine.state is LifecycleState.CLOSED
    assert backend.close_calls == 1


def test_run_failure_stops_then_closes_backend() -> None:
    backend = RecordingBackend(fail_render=True)
    engine = Engine(EngineConfig(), backend, clock=VirtualClock())
    engine.initialize()

    with pytest.raises(LifecycleError, match="run failed") as captured:
        engine.run(ticks=1)

    assert engine.state is LifecycleState.STOPPED
    assert isinstance(captured.value.__cause__, RuntimeError)
    engine.close()
    assert backend.close_calls == 1


@pytest.mark.parametrize(
    "operation",
    [
        _run_from_created,
        _shutdown_from_created,
    ],
)
def test_invalid_transition_from_created(operation: Callable[[Engine], object]) -> None:
    engine, _backend, _clock = _new_engine()
    with pytest.raises(LifecycleError, match="created state"):
        operation(engine)
    engine.close()


def test_initialize_twice_is_rejected() -> None:
    engine, _backend, _clock = _new_engine()
    engine.initialize()
    with pytest.raises(LifecycleError, match="ready state"):
        engine.initialize()
    engine.close()


def test_second_run_is_rejected() -> None:
    engine, _backend, _clock = _new_engine()
    engine.initialize()
    engine.run(ticks=0)
    with pytest.raises(LifecycleError, match="stopped state"):
        engine.run(ticks=1)
    engine.close()


@given(st.integers(max_value=-1))
def test_negative_tick_count_is_rejected(ticks: int) -> None:
    engine, _backend, _clock = _new_engine()
    engine.initialize()
    with pytest.raises(ConfigurationError, match="non-negative"):
        engine.run(ticks=ticks)
    assert engine.state is LifecycleState.READY
    engine.close()


@pytest.mark.parametrize("ticks", [True, 1.5, "1"])
def test_non_integer_tick_count_is_rejected(ticks: object) -> None:
    engine, _backend, _clock = _new_engine()
    engine.initialize()
    with pytest.raises(ConfigurationError, match="non-negative"):
        engine.run(ticks=cast(int, ticks))
    engine.close()


def test_wrong_thread_lifecycle_call_is_rejected() -> None:
    engine, _backend, _clock = _new_engine()
    errors: list[BaseException] = []

    def close_from_other_thread() -> None:
        try:
            engine.close()
        except BaseException as error:
            errors.append(error)

    thread = Thread(target=close_from_other_thread)
    thread.start()
    thread.join()

    assert len(errors) == 1
    assert isinstance(errors[0], LifecycleError)
    assert engine.state is LifecycleState.CREATED
    engine.close()
