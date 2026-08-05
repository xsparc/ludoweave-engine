"""Fixed-step timing, lifecycle, and catch-up tests."""

from threading import Thread
from typing import cast

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.app import (
    INPUT_SNAPSHOT_RESOURCE,
    ApplicationConfig,
    ApplicationError,
    ApplicationRunSummary,
    FixedStepApplication,
    NullInputSource,
)
from ludoweave.core.clock import VirtualClock
from ludoweave.core.errors import ConfigurationError
from ludoweave.ecs import (
    ComponentRegistry,
    ResourceRegistry,
    ResourceSpec,
    ResourceStore,
    Schedule,
    Scheduler,
    SystemContext,
    World,
    system,
    system_spec,
)
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
        self.frames = 0
        self.close_calls = 0

    @property
    def name(self) -> str:
        return "recording"

    def initialize(self, descriptor: RenderDescriptor) -> None:
        del descriptor
        if self.fail_initialize:
            raise RuntimeError("initialize failed")

    def render(self, *, tick: int) -> None:
        del tick
        if self.fail_render:
            raise RuntimeError("render failed")
        self.frames += 1

    def close(self) -> None:
        self.close_calls += 1
        if self.fail_close:
            raise RuntimeError("close failed")


class RaisingClock:
    def __init__(self) -> None:
        self.calls = 0

    def now_ns(self) -> int:
        self.calls += 1
        if self.calls > 1:
            raise RuntimeError("clock failed")
        return 0

    def wait_until_ns(self, deadline_ns: int) -> None:
        del deadline_ns


CONFLICTING_RESOURCE = ResourceSpec("test.conflicting", int, int)


@system(name="test.forged_reader", resource_reads=(CONFLICTING_RESOURCE,))
def forged_reader(context: SystemContext, delta: float) -> None:
    del delta
    context.resource(CONFLICTING_RESOURCE)


@system(name="test.forged_writer", resource_writes=(CONFLICTING_RESOURCE,))
def forged_writer(context: SystemContext, delta: float) -> None:
    del delta
    context.set_resource(CONFLICTING_RESOURCE, 1)


def _application_with_services(
    backend: RecordingBackend,
    *,
    clock: VirtualClock | RaisingClock,
) -> FixedStepApplication:
    components = ComponentRegistry()
    resource_registry = ResourceRegistry((INPUT_SNAPSHOT_RESOURCE,))
    return FixedStepApplication(
        ApplicationConfig(),
        backend,
        World(components),
        ResourceStore(resource_registry),
        Scheduler(components, resource_registry).build(()),
        NullInputSource(),
        clock=clock,
    )


def _empty_application(
    *,
    fixed_hz: int = 60,
    catch_up_limit: int = 4,
    start_ns: int = 0,
) -> tuple[FixedStepApplication, VirtualClock, NullRenderBackend, ResourceStore]:
    components = ComponentRegistry()
    resource_registry = ResourceRegistry((INPUT_SNAPSHOT_RESOURCE,))
    resources = ResourceStore(resource_registry)
    schedule = Scheduler(components, resource_registry).build(())
    clock = VirtualClock(start_ns)
    backend = NullRenderBackend()
    application = FixedStepApplication(
        ApplicationConfig(fixed_hz=fixed_hz, catch_up_limit=catch_up_limit),
        backend,
        World(components),
        resources,
        schedule,
        NullInputSource(),
        clock=clock,
    )
    return application, clock, backend, resources


@pytest.mark.parametrize("field", ["fixed_hz", "catch_up_limit"])
@pytest.mark.parametrize("value", [0, -1, True, 1.5, "1"])
def test_application_config_rejects_non_positive_exact_integers(field: str, value: object) -> None:
    arguments: dict[str, object] = {"fixed_hz": 60, "catch_up_limit": 4, field: value}
    with pytest.raises(ConfigurationError):
        ApplicationConfig(**arguments)  # type: ignore[arg-type]


def test_first_pump_sets_no_elapsed_ticks_and_renders_one_frame() -> None:
    application, _clock, backend, resources = _empty_application(start_ns=91)
    application.initialize()

    summary = application.pump()

    assert summary.frame == 1
    assert summary.ticks_executed == 0
    assert summary.total_ticks == 0
    assert summary.backlog_ticks == 0
    assert summary.interpolation_alpha == 0.0
    assert backend.frame_count == 1
    assert not resources.contains(INPUT_SNAPSHOT_RESOURCE)
    application.shutdown()
    application.close()


def test_exact_rational_boundary_avoids_sixty_hertz_rounding_drift() -> None:
    application, clock, _backend, _resources = _empty_application()
    application.initialize()

    clock.advance_ns(16_666_666)
    before = application.pump()
    clock.advance_ns(1)
    boundary = application.pump()

    assert before.ticks_executed == 0
    assert before.interpolation_alpha == pytest.approx(0.99999996)
    assert boundary.ticks_executed == 1
    assert boundary.total_ticks == 1
    assert boundary.interpolation_alpha == pytest.approx(2e-8)
    application.close()


def test_catch_up_limit_retains_and_zero_elapsed_pumps_drain_backlog() -> None:
    application, clock, backend, resources = _empty_application(catch_up_limit=4)
    application.initialize()
    clock.advance_ns(1_000_000_000)

    first = application.pump()
    assert first.ticks_executed == 4
    assert first.backlog_ticks == 56
    assert first.interpolation_alpha == 1.0

    for _ in range(13):
        application.pump()
    final = application.pump()

    assert final.ticks_executed == 4
    assert final.total_ticks == 60
    assert final.backlog_ticks == 0
    assert resources.require(INPUT_SNAPSHOT_RESOURCE).tick == 59
    assert backend.frame_count == 15
    application.close()


def test_run_ticks_uses_absolute_deadlines_stops_and_closes_idempotently() -> None:
    application, clock, backend, _resources = _empty_application(start_ns=7)
    summary: ApplicationRunSummary | None = None
    with application:
        summary = application.run_ticks(3)

    assert summary is not None
    assert summary == ApplicationRunSummary(
        ticks=3,
        frames=3,
        start_ns=7,
        end_ns=50_000_007,
        fixed_hz=60,
        renderer="null",
    )
    assert application.state.value == "closed"
    assert clock.now_ns() == 50_000_007
    assert backend.frame_count == 3
    application.close()


@pytest.mark.parametrize("count", [-1, True, 1.5, "1"])
def test_run_ticks_rejects_invalid_counts_without_starting(count: object) -> None:
    application, _clock, _backend, _resources = _empty_application()
    application.initialize()
    with pytest.raises(ConfigurationError):
        application.run_ticks(cast(int, count))
    assert application.state.value == "ready"
    application.close()


def test_pump_and_exact_tick_modes_cannot_mix() -> None:
    application, _clock, _backend, _resources = _empty_application()
    application.initialize()
    application.pump()
    with pytest.raises(ApplicationError):
        application.run_ticks(1)
    application.close()


def test_backward_clock_and_wrong_thread_stop_or_reject_without_work() -> None:
    application, clock, backend, _resources = _empty_application(start_ns=10)
    application.initialize()
    clock._current_ns = 9  # pyright: ignore[reportPrivateUsage]
    with pytest.raises(ApplicationError, match="backward"):
        application.pump()
    assert application.state.value == "stopped"
    assert backend.frame_count == 0
    application.close()

    other, _clock, _backend, _resources = _empty_application()
    errors: list[BaseException] = []

    def initialize_elsewhere() -> None:
        try:
            other.initialize()
        except BaseException as error:
            errors.append(error)

    thread = Thread(target=initialize_elsewhere)
    thread.start()
    thread.join()
    assert len(errors) == 1
    assert isinstance(errors[0], ApplicationError)
    assert other.state.value == "created"
    other.close()


def test_initialization_render_clock_and_close_failures_preserve_lifecycle_context() -> None:
    initialization_backend = RecordingBackend(fail_initialize=True)
    initializing = _application_with_services(
        initialization_backend,
        clock=VirtualClock(),
    )
    with pytest.raises(ApplicationError) as initialization_error:
        initializing.initialize()
    assert isinstance(initialization_error.value.__cause__, RuntimeError)
    assert initializing.state.value == "closed"
    assert initialization_backend.close_calls == 1

    render_backend = RecordingBackend(fail_render=True)
    rendering = _application_with_services(render_backend, clock=VirtualClock())
    rendering.initialize()
    with pytest.raises(ApplicationError) as render_error:
        rendering.run_ticks(1)
    assert render_error.value.code == "application.render_failed"
    assert rendering.total_ticks == 1
    assert rendering.state.value == "stopped"
    rendering.close()
    assert render_backend.close_calls == 1

    clock_backend = RecordingBackend()
    clock_failure = _application_with_services(clock_backend, clock=RaisingClock())
    clock_failure.initialize()
    with pytest.raises(ApplicationError) as clock_error:
        clock_failure.pump()
    assert clock_error.value.code == "application.clock_failed"
    assert isinstance(clock_error.value.__cause__, RuntimeError)
    assert clock_failure.state.value == "stopped"
    clock_failure.close()


def test_initialization_rejects_schedule_that_bypasses_canonical_planner() -> None:
    components = ComponentRegistry()
    resources = ResourceRegistry((INPUT_SNAPSHOT_RESOURCE, CONFLICTING_RESOURCE))
    forged = Schedule(
        systems=(system_spec(forged_reader), system_spec(forged_writer)),
        conflicts=(),
        explicit_edges=(),
    )
    application = FixedStepApplication(
        ApplicationConfig(),
        NullRenderBackend(),
        World(components),
        ResourceStore(resources, ((CONFLICTING_RESOURCE, 0),)),
        forged,
        NullInputSource(),
        clock=VirtualClock(),
    )

    with pytest.raises(ApplicationError) as caught:
        application.initialize()

    assert caught.value.code == "application.initialization_failed"
    cause = caught.value.__cause__
    assert isinstance(cause, ApplicationError)
    assert cause.code == "application.invalid_schedule"
    assert application.state.value == "closed"


def test_context_manager_does_not_mask_primary_failure_when_close_also_fails() -> None:
    backend = RecordingBackend(fail_close=True)
    application = _application_with_services(backend, clock=VirtualClock())

    with (
        pytest.raises(RuntimeError, match="primary") as caught,
        application,
    ):
        raise RuntimeError("primary")

    assert application.state.value == "closed"
    assert backend.close_calls == 1
    assert any("cleanup also failed" in note for note in caught.value.__notes__)


@given(
    fixed_hz=st.integers(min_value=1, max_value=500),
    elapsed_ns=st.integers(min_value=0, max_value=10**9),
)
def test_unlimited_single_pump_matches_integer_units_model(fixed_hz: int, elapsed_ns: int) -> None:
    expected = (elapsed_ns * fixed_hz) // 1_000_000_000
    application, clock, _backend, _resources = _empty_application(
        fixed_hz=fixed_hz,
        catch_up_limit=max(expected, 1),
    )
    application.initialize()
    clock.advance_ns(elapsed_ns)

    summary = application.pump()

    assert summary.total_ticks == expected
    assert summary.backlog_ticks == 0
    application.close()
