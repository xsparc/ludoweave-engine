"""End-to-end serial system, input, access, and flush-boundary tests."""

from collections.abc import Callable
from dataclasses import dataclass
from threading import get_ident
from typing import cast
from uuid import UUID

import pytest

from ludoweave.app import (
    INPUT_SNAPSHOT_RESOURCE,
    ApplicationConfig,
    ApplicationError,
    FixedStepApplication,
    InputAction,
    InputFrameError,
    InputSnapshot,
    InputSource,
    RecordedInputSource,
    SystemAccessError,
    SystemExecutionError,
    VirtualInputSource,
)
from ludoweave.core.clock import VirtualClock
from ludoweave.ecs import (
    ComponentRegistry,
    EntityId,
    ReferenceWorld,
    ResourceCopyError,
    ResourceRegistry,
    ResourceSpec,
    ResourceStore,
    Scheduler,
    SystemContext,
    SystemFunction,
    SystemPhase,
    SystemRows,
    World,
    WorldStore,
    component,
    system,
    system_spec,
)
from ludoweave.render import NullRenderBackend


@component(type_id=UUID("f6000000-0000-0000-0000-000000000001"))
@dataclass(slots=True)
class Counter:
    value: int = 0


@component(type_id=UUID("f6000000-0000-0000-0000-000000000002"))
@dataclass(slots=True)
class Other:
    value: int = 0


@dataclass(slots=True)
class TickStats:
    before_flush: int = -1
    after_flush: int = -1
    system_calls: int = 0


STATS = ResourceSpec(
    "simulation.tick_stats",
    TickStats,
    lambda value: TickStats(value.before_flush, value.after_flush, value.system_calls),
)
COMPONENTS = ComponentRegistry((Counter, Other))
RESOURCES = ResourceRegistry((INPUT_SNAPSHOT_RESOURCE, STATS))
TRACE: list[tuple[int, str, int]] = []
RETAINED_CONTEXTS: list[SystemContext] = []
RETAINED_ROWS: list[object] = []


@system(
    name="runtime.pre_spawn",
    phase=SystemPhase.PRE_SIMULATE,
    component_writes=(Counter,),
    resource_reads=(INPUT_SNAPSHOT_RESOURCE,),
)
def pre_spawn(context: SystemContext, delta: float) -> None:
    assert delta == 1.0 / 60
    snapshot = context.resource(INPUT_SNAPSHOT_RESOURCE)
    context.commands.spawn(Counter(1 if snapshot.value("jump") is True else 0))
    TRACE.append((context.tick, "pre", get_ident()))


@system(
    name="runtime.sim_observe",
    component_reads=(Counter,),
    resource_writes=(STATS,),
    before=("runtime.integrate",),
)
def simulate_observe(context: SystemContext, delta: float) -> None:
    del delta
    stats = context.resource(STATS)
    stats.before_flush = sum(1 for _ in context.query(Counter).rows())
    stats.system_calls += 1
    TRACE.append((context.tick, "simulate_observe", get_ident()))


@system(name="runtime.integrate", component_writes=(Counter,))
def integrate(context: SystemContext, delta: float) -> None:
    del delta
    with context.query(Counter).writes(Counter).rows() as rows:
        for _entity_id, counter in rows:
            counter.value += 10
    TRACE.append((context.tick, "integrate", get_ident()))


@system(
    name="runtime.post_observe",
    phase=SystemPhase.POST_SIMULATE,
    component_reads=(Counter,),
    resource_writes=(STATS,),
)
def post_observe(context: SystemContext, delta: float) -> None:
    del delta
    stats = context.resource(STATS)
    stats.after_flush = sum(1 for _ in context.query(Counter).rows())
    stats.system_calls += 1
    TRACE.append((context.tick, "post", get_ident()))


RUNTIME_SYSTEMS: tuple[SystemFunction, ...] = (
    pre_spawn,
    simulate_observe,
    integrate,
    post_observe,
)


@system(name="failure.undeclared_query")
def undeclared_query(context: SystemContext, delta: float) -> None:
    del delta
    list(context.query(Counter).rows())


@system(name="failure.entity_set_query")
def entity_set_query(context: SystemContext, delta: float) -> None:
    del delta
    cast(Callable[[], object], context.query)()


@system(name="failure.undeclared_write", component_reads=(Counter,))
def undeclared_write(context: SystemContext, delta: float) -> None:
    del delta
    context.query(Counter).writes(Counter)


@system(name="failure.undeclared_exclude", component_reads=(Counter,))
def undeclared_exclude(context: SystemContext, delta: float) -> None:
    del delta
    context.query(Counter).without(Other)


@system(name="failure.undeclared_changed", component_reads=(Counter,))
def undeclared_changed(context: SystemContext, delta: float) -> None:
    del delta
    context.query(Counter).changed_since(0, Other)


@system(name="failure.undeclared_resource")
def undeclared_resource(context: SystemContext, delta: float) -> None:
    del delta
    context.resource(STATS)


@system(name="failure.undeclared_command")
def undeclared_command(context: SystemContext, delta: float) -> None:
    del delta
    context.commands.spawn(Counter())


@system(
    name="failure.post_commands",
    phase=SystemPhase.POST_SIMULATE,
    component_writes=(Counter,),
)
def post_commands(context: SystemContext, delta: float) -> None:
    del delta
    context.commands.spawn(Counter())


@system(name="failure.flush", component_writes=(Counter,))
def invalid_flush(context: SystemContext, delta: float) -> None:
    del delta
    context.commands.add(EntityId(999, 0), Counter())


@system(name="failure.empty_spawn")
def empty_spawn(context: SystemContext, delta: float) -> None:
    del delta
    cast(Callable[[], object], context.commands.spawn)()


@system(name="failure.destroy")
def destroy_entity(context: SystemContext, delta: float) -> None:
    del delta
    destroy = cast(
        Callable[[EntityId], None],
        object.__getattribute__(context.commands, "destroy"),
    )
    destroy(EntityId(0, 0))


@system(name="failure.retain")
def retain_context(context: SystemContext, delta: float) -> None:
    del delta
    RETAINED_CONTEXTS.append(context)


@system(name="failure.open_cursor", component_writes=(Counter,))
def leave_cursor_open(context: SystemContext, delta: float) -> None:
    del delta
    rows = context.query(Counter).writes(Counter).rows()
    rows.__enter__()
    next(rows)
    RETAINED_ROWS.append(rows)


@system(name="failure.return_value")
def return_value(context: SystemContext, delta: float) -> None:
    del context, delta
    return cast(None, "not-none")


@system(name="failure.post_raise", phase=SystemPhase.POST_SIMULATE)
def post_raise(context: SystemContext, delta: float) -> None:
    del context, delta
    raise RuntimeError("post failed after structural flush")


@system(name="failure.input_writer", resource_writes=(INPUT_SNAPSHOT_RESOURCE,))
def input_writer(context: SystemContext, delta: float) -> None:
    del delta
    context.set_resource(INPUT_SNAPSHOT_RESOURCE, InputSnapshot(context.tick))


class FatalSignal(BaseException):
    pass


@system(name="failure.base_exception", component_writes=(Counter,))
def raise_base_exception(context: SystemContext, delta: float) -> None:
    del delta
    rows = context.query(Counter).writes(Counter).rows()
    rows.__enter__()
    next(rows)
    raise FatalSignal


@dataclass(slots=True)
class OrderedFailure:
    value: int = 0


def copy_ordered_failure(value: OrderedFailure) -> OrderedFailure:
    if value.value < 0:
        raise ValueError("negative resource")
    return OrderedFailure(value.value)


ALPHA_FAILURE = ResourceSpec("failure.alpha", OrderedFailure, copy_ordered_failure)
BETA_FAILURE = ResourceSpec("failure.beta", OrderedFailure, copy_ordered_failure)


@system(
    name="failure.resource_order",
    resource_writes=(BETA_FAILURE, ALPHA_FAILURE),
)
def fail_resources(context: SystemContext, delta: float) -> None:
    del delta
    context.resource(BETA_FAILURE).value = -1
    context.resource(ALPHA_FAILURE).value = -1


class MismatchedInputSource:
    def snapshot_for_tick(self, tick: int) -> InputSnapshot:
        return InputSnapshot(tick + 1)


class RaisingInputSource:
    def snapshot_for_tick(self, tick: int) -> InputSnapshot:
        del tick
        raise RuntimeError("input source failed")


class HostileSnapshot:
    @property
    def tick(self) -> int:
        raise RuntimeError("hostile tick getter")


class HostileInputSource:
    def snapshot_for_tick(self, tick: int) -> InputSnapshot:
        del tick
        return cast(InputSnapshot, HostileSnapshot())


def _application(
    definitions: tuple[SystemFunction, ...],
    source: InputSource,
    *,
    initial_counter: bool = False,
    reference: bool = False,
) -> tuple[
    FixedStepApplication,
    WorldStore,
    ResourceStore,
    NullRenderBackend,
    VirtualClock,
]:
    world: WorldStore = ReferenceWorld(COMPONENTS) if reference else World(COMPONENTS)
    if initial_counter:
        world.spawn(Counter(5))
    resources = ResourceStore(RESOURCES, ((STATS, TickStats()),))
    schedule = Scheduler(COMPONENTS, RESOURCES).build(definitions)
    backend = NullRenderBackend()
    clock = VirtualClock()
    application = FixedStepApplication(
        ApplicationConfig(),
        backend,
        world,
        resources,
        schedule,
        source,
        clock=clock,
    )
    return application, world, resources, backend, clock


type ComponentOutcome = tuple[tuple[tuple[int, int], int], ...]


def _outcome(
    source: InputSource, *, reference: bool = False
) -> tuple[ComponentOutcome, TickStats, list[str]]:
    TRACE.clear()
    application, world, resources, _backend, _clock = _application(
        RUNTIME_SYSTEMS, source, reference=reference
    )
    with application:
        application.run_ticks(3)
    components = tuple(
        (entity_id.as_tuple(), counter.value) for entity_id, counter in world.components(Counter)
    )
    phases = [phase for _tick, phase, _thread in TRACE]
    return components, resources.require(STATS), phases


def test_virtual_and_recorded_input_drive_identical_fixed_tick_outcomes() -> None:
    virtual = VirtualInputSource({0: {"jump": True}, 2: {"jump": True}})
    recorded = RecordedInputSource(
        (
            InputSnapshot(0, (InputAction("jump", True),)),
            InputSnapshot(2, (InputAction("jump", True),)),
        )
    )

    virtual_outcome = _outcome(virtual)
    recorded_outcome = _outcome(recorded)

    assert virtual_outcome == recorded_outcome
    components, stats, phases = virtual_outcome
    assert components == (((0, 0), 21), ((1, 0), 10), ((2, 0), 1))
    assert stats == TickStats(before_flush=2, after_flush=3, system_calls=6)
    assert (
        phases
        == [
            "pre",
            "simulate_observe",
            "integrate",
            "post",
        ]
        * 3
    )
    assert len({thread for _tick, _phase, thread in TRACE}) == 1

    reference_outcome = _outcome(recorded, reference=True)
    assert reference_outcome == recorded_outcome


def test_pre_and_simulate_commands_are_invisible_until_post_flush() -> None:
    application, world, resources, _backend, _clock = _application(
        RUNTIME_SYSTEMS, VirtualInputSource()
    )
    application.initialize()
    application.run_ticks(1)

    assert len(world.entities()) == 1
    assert resources.require(STATS) == TickStats(
        before_flush=0,
        after_flush=1,
        system_calls=2,
    )
    application.close()


@pytest.mark.parametrize(
    ("definition", "initial_counter"),
    [
        (undeclared_query, False),
        (entity_set_query, False),
        (undeclared_write, True),
        (undeclared_exclude, True),
        (undeclared_changed, True),
        (undeclared_resource, False),
        (undeclared_command, False),
        (empty_spawn, False),
        (destroy_entity, True),
        (post_commands, False),
        (leave_cursor_open, True),
        (return_value, False),
    ],
)
def test_system_access_and_return_failures_stop_and_preserve_context(
    definition: SystemFunction, initial_counter: bool
) -> None:
    if definition is leave_cursor_open:
        RETAINED_ROWS.clear()
    application, world, _resources, backend, _clock = _application(
        (definition,), VirtualInputSource(), initial_counter=initial_counter
    )
    before = tuple(world.components(Counter))
    application.initialize()

    with pytest.raises(SystemExecutionError) as caught:
        application.run_ticks(1)

    assert application.state.value == "stopped"
    assert application.total_ticks == 0
    assert backend.frame_count == 0
    assert dict(caught.value.details)["system"] == system_spec(definition).name
    assert isinstance(caught.value.__cause__, SystemAccessError)
    if definition is leave_cursor_open:
        assert tuple(world.components(Counter)) == before
        with pytest.raises(SystemAccessError):
            cast(SystemRows[Counter], RETAINED_ROWS[-1]).abort()
        world.spawn()
    application.close()


def test_context_expires_after_successful_invocation() -> None:
    RETAINED_CONTEXTS.clear()
    application, _world, _resources, _backend, _clock = _application(
        (retain_context,), VirtualInputSource()
    )
    application.initialize()
    application.run_ticks(1)

    assert len(RETAINED_CONTEXTS) == 1
    with pytest.raises(SystemAccessError):
        _ = RETAINED_CONTEXTS[0].tick
    application.close()


def test_flush_failure_is_atomic_clears_queue_and_skips_render_and_post() -> None:
    application, world, _resources, backend, _clock = _application(
        (invalid_flush, post_observe), VirtualInputSource()
    )
    before_epoch = world.epoch
    application.initialize()

    with pytest.raises(ApplicationError) as caught:
        application.run_ticks(1)

    assert caught.value.code == "application.flush_failed"
    assert dict(caught.value.details)["operation_index"] == 0
    assert dict(caught.value.details)["operation_kind"] == "add"
    assert dict(caught.value.details)["system"] == "failure.flush"
    assert world.epoch == before_epoch
    assert world.entities() == ()
    assert application.total_ticks == 0
    assert backend.frame_count == 0
    application.close()


def test_mismatched_input_fails_before_system_or_render_work() -> None:
    TRACE.clear()
    application, world, _resources, backend, _clock = _application(
        RUNTIME_SYSTEMS, MismatchedInputSource()
    )
    application.initialize()

    with pytest.raises(InputFrameError):
        application.run_ticks(1)

    assert TRACE == []
    assert world.entities() == ()
    assert application.total_ticks == 0
    assert backend.frame_count == 0
    application.close()


@pytest.mark.parametrize(
    "source",
    [MismatchedInputSource(), RaisingInputSource(), HostileInputSource()],
)
def test_input_failure_chains_cause_and_does_not_count_tick(source: InputSource) -> None:
    application, world, _resources, backend, _clock = _application(RUNTIME_SYSTEMS, source)
    application.initialize()

    with pytest.raises(InputFrameError) as caught:
        application.run_ticks(1)

    assert application.total_ticks == 0
    assert world.entities() == ()
    assert backend.frame_count == 0
    if isinstance(source, RaisingInputSource):
        assert isinstance(caught.value.__cause__, RuntimeError)
    application.close()


def test_base_exception_expires_context_releases_query_and_stops_application() -> None:
    application, world, _resources, backend, _clock = _application(
        (raise_base_exception,),
        VirtualInputSource(),
        initial_counter=True,
    )
    application.initialize()

    with pytest.raises(FatalSignal):
        application.run_ticks(1)

    assert application.state.value == "stopped"
    assert application.total_ticks == 0
    assert backend.frame_count == 0
    world.spawn(Counter(9))
    application.close()


def test_application_rejects_system_write_access_to_owned_input_snapshot() -> None:
    application, _world, _resources, backend, _clock = _application(
        (input_writer,), VirtualInputSource()
    )

    with pytest.raises(ApplicationError) as caught:
        application.initialize()

    assert caught.value.code == "application.initialization_failed"
    cause = caught.value.__cause__
    assert isinstance(cause, ApplicationError)
    assert cause.code == "application.invalid_schedule"
    assert backend.is_closed


def test_resource_write_failures_follow_canonical_declaration_order() -> None:
    registry = ResourceRegistry((INPUT_SNAPSHOT_RESOURCE, BETA_FAILURE, ALPHA_FAILURE))
    resources = ResourceStore(
        registry,
        (
            (BETA_FAILURE, OrderedFailure()),
            (ALPHA_FAILURE, OrderedFailure()),
        ),
    )
    application = FixedStepApplication(
        ApplicationConfig(),
        NullRenderBackend(),
        World(ComponentRegistry()),
        resources,
        Scheduler(ComponentRegistry(), registry).build((fail_resources,)),
        VirtualInputSource(),
        clock=VirtualClock(),
    )
    application.initialize()

    with pytest.raises(SystemExecutionError) as caught:
        application.run_ticks(1)

    cause = caught.value.__cause__
    assert isinstance(cause, ResourceCopyError)
    assert dict(cause.details)["resource"] == "failure.alpha"
    application.close()


def test_post_failure_is_nontransactional_but_tick_remains_incomplete() -> None:
    application, world, _resources, backend, _clock = _application(
        (pre_spawn, post_raise), VirtualInputSource({0: {"jump": True}})
    )
    application.initialize()

    with pytest.raises(SystemExecutionError) as caught:
        application.run_ticks(1)

    assert caught.value.phase == "post_simulate"
    assert application.total_ticks == 0
    assert world.components(Counter) == ((EntityId(0, 0), Counter(1)),)
    assert backend.frame_count == 0
    application.close()
