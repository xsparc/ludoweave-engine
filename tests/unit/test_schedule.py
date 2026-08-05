"""System declaration, conflict validation, and deterministic graph tests."""

from dataclasses import FrozenInstanceError, dataclass, replace
from types import FunctionType
from typing import TYPE_CHECKING, assert_type, cast
from uuid import UUID

import pytest

from ludoweave.ecs import (
    ComponentRegistry,
    DeferredEntity,
    DeterminismTier,
    DuplicateSystemError,
    ExecutionClass,
    InvalidSystemDependencyError,
    InvalidSystemSpecError,
    NondeterministicSystemError,
    ResourceRegistry,
    ResourceSpec,
    Schedule,
    ScheduleConflictError,
    ScheduleCycleError,
    Scheduler,
    SerializationPolicy,
    SystemContext,
    SystemFunction,
    SystemPhase,
    SystemQuery,
    UnknownSystemDependencyError,
    UnsupportedExecutionClassError,
    component,
    system,
    system_spec,
)


@component(type_id=UUID("f4000000-0000-0000-0000-000000000001"))
@dataclass(slots=True)
class Position:
    value: int = 0


@component(type_id=UUID("f4000000-0000-0000-0000-000000000002"))
@dataclass(slots=True)
class Velocity:
    value: int = 0


@component(type_id=UUID("f4000000-0000-0000-0000-000000000003"))
@dataclass(slots=True)
class Marker:
    value: bool = True


@component(
    type_id=UUID("f4000000-0000-0000-0000-000000000004"),
    authoritative=False,
    serialization=SerializationPolicy.EXCLUDED,
    determinism=DeterminismTier.D0,
)
@dataclass(slots=True)
class PresentationMarker:
    value: bool = True


@dataclass(slots=True)
class ClockState:
    tick: int = 0


@dataclass(slots=True)
class InputState:
    pressed: bool = False


CLOCK = ResourceSpec("simulation.clock", ClockState, lambda value: ClockState(value.tick))
INPUT = ResourceSpec("simulation.input", InputState, lambda value: InputState(value.pressed))
NONDETERMINISTIC = ResourceSpec(
    "presentation.input",
    InputState,
    lambda value: InputState(value.pressed),
    deterministic=False,
)
COMPONENTS = ComponentRegistry((Velocity, Marker, Position, PresentationMarker))
RESOURCES = ResourceRegistry((INPUT, NONDETERMINISTIC, CLOCK))
SCHEDULER = Scheduler(COMPONENTS, RESOURCES)
TRACE: list[str] = []


@system(name="phase.pre", phase=SystemPhase.PRE_SIMULATE)
def phase_pre(context: SystemContext, delta: float) -> None:
    del context, delta
    TRACE.append("pre")


@system(name="phase.sim_b")
def phase_sim_b(context: SystemContext, delta: float) -> None:
    del context, delta
    TRACE.append("sim_b")


@system(name="phase.sim_a")
def phase_sim_a(context: SystemContext, delta: float) -> None:
    del context, delta
    TRACE.append("sim_a")


@system(name="phase.post", phase=SystemPhase.POST_SIMULATE)
def phase_post(context: SystemContext, delta: float) -> None:
    del context, delta
    TRACE.append("post")


@system(name="explicit.z", before=("explicit.a",))
def explicit_z(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="explicit.a", after=())
def explicit_a(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="after.first")
def after_first(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="after.last", after=("after.first",))
def after_last(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="read.one", component_reads=(Position,))
def read_one(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="read.two", component_reads=(Position,))
def read_two(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="ambiguous.writer", component_writes=(Position,))
def ambiguous_writer(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="ambiguous.reader", component_reads=(Position,))
def ambiguous_reader(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="ambiguous.second_writer", component_writes=(Position,))
def ambiguous_second_writer(context: SystemContext, delta: float) -> None:
    del context, delta


@system(
    name="ordered.writer",
    component_writes=(Position,),
    before=("ordered.reader",),
)
def ordered_writer(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="ordered.reader", component_reads=(Position,))
def ordered_reader(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="transitive.writer", component_writes=(Position,), before=("transitive.bridge",))
def transitive_writer(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="transitive.bridge", before=("transitive.reader",))
def transitive_bridge(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="transitive.reader", component_reads=(Position,))
def transitive_reader(context: SystemContext, delta: float) -> None:
    del context, delta


@system(
    name="resource.writer",
    resource_writes=(CLOCK,),
    before=("resource.reader",),
)
def resource_writer(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="resource.reader", resource_reads=(CLOCK,))
def resource_reader(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="resource.ambiguous", resource_writes=(CLOCK,))
def resource_ambiguous(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="resource.second_writer", resource_writes=(CLOCK,))
def resource_second_writer(context: SystemContext, delta: float) -> None:
    del context, delta


@system(
    name="cross.pre_writer",
    phase=SystemPhase.PRE_SIMULATE,
    component_writes=(Velocity,),
)
def cross_pre_writer(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="cross.sim_reader", component_reads=(Velocity,))
def cross_sim_reader(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="unknown.source", before=("unknown.target",))
def unknown_source(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="cross.edge", phase=SystemPhase.PRE_SIMULATE, before=("phase.sim_a",))
def cross_edge(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="duplicate.a", before=("duplicate.b",))
def duplicate_a(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="duplicate.b", after=("duplicate.a",))
def duplicate_b(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="cycle.a", before=("cycle.b",))
def cycle_a(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="cycle.b", before=("cycle.c",))
def cycle_b(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="cycle.c", before=("cycle.a",))
def cycle_c(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="eligibility.system", deterministic=False)
def nondeterministic_system(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="eligibility.resource", resource_reads=(NONDETERMINISTIC,))
def nondeterministic_resource(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="execution.native", execution_class=ExecutionClass.NATIVE)
def native_system(context: SystemContext, delta: float) -> None:
    del context, delta


@component(type_id=UUID("f4000000-0000-0000-0000-000000000004"))
@dataclass(slots=True)
class UnregisteredComponent:
    value: int = 0


FOREIGN_CLOCK = ResourceSpec(
    CLOCK.name,
    ClockState,
    lambda value: ClockState(value.tick),
)


@system(name="invalid.component", component_reads=(UnregisteredComponent,))
def invalid_component(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="invalid.resource", resource_reads=(FOREIGN_CLOCK,))
def invalid_resource(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="nondeterministic.component", component_reads=(PresentationMarker,))
def nondeterministic_component(context: SystemContext, delta: float) -> None:
    del context, delta


def undecorated(context: SystemContext, delta: float) -> None:
    del context, delta


def generator_system(context: SystemContext, delta: float):  # type: ignore[no-untyped-def]
    del context, delta
    yield None


def bad_signature(context: SystemContext) -> None:
    del context


def malformed_signature_metadata(context: SystemContext, delta: float) -> None:
    del context, delta


class SystemHolder:
    @staticmethod
    def member(context: SystemContext, delta: float) -> None:
        del context, delta


if TYPE_CHECKING:
    assert_type(system_spec(phase_pre).function, SystemFunction)

    def _assert_system_context_shapes(context: SystemContext) -> None:
        assert_type(context.query(Position), SystemQuery[Position])
        assert_type(context.commands.spawn(Position()), DeferredEntity)

    _ = _assert_system_context_shapes


def test_system_decorator_preserves_callable_and_freezes_normalized_metadata() -> None:
    assert system_spec(phase_pre).function is phase_pre
    spec = system_spec(ordered_writer)
    assert spec.name == "ordered.writer"
    assert spec.phase is SystemPhase.SIMULATE
    assert spec.component_writes == (Position,)
    assert spec.before == ("ordered.reader",)
    with pytest.raises(FrozenInstanceError):
        spec.name = "changed"  # type: ignore[misc]


def test_build_is_stable_across_input_order_and_never_executes_functions() -> None:
    TRACE.clear()
    first = SCHEDULER.build((phase_post, phase_sim_b, phase_pre, phase_sim_a))
    second = SCHEDULER.build((phase_sim_a, phase_pre, phase_post, phase_sim_b))

    assert [spec.name for spec in first.systems] == [
        "phase.pre",
        "phase.sim_a",
        "phase.sim_b",
        "phase.post",
    ]
    assert first == second
    assert first.systems_for_phase(SystemPhase.SIMULATE) == (
        system_spec(phase_sim_a),
        system_spec(phase_sim_b),
    )
    assert TRACE == []


def test_explicit_order_overrides_lexical_tie_for_nonconflicting_systems() -> None:
    plan = SCHEDULER.build((explicit_a, explicit_z))
    assert [spec.name for spec in plan.systems] == ["explicit.z", "explicit.a"]
    assert plan.explicit_edges == (("explicit.z", "explicit.a"),)

    after_plan = SCHEDULER.build((after_last, after_first))
    assert [spec.name for spec in after_plan.systems] == ["after.first", "after.last"]
    assert after_plan.explicit_edges == (("after.first", "after.last"),)


def test_read_read_is_not_a_conflict() -> None:
    plan = SCHEDULER.build((read_two, read_one))
    assert [spec.name for spec in plan.systems] == ["read.one", "read.two"]
    assert plan.conflicts == ()


def test_unordered_component_and_resource_write_conflicts_fail_deterministically() -> None:
    with pytest.raises(ScheduleConflictError) as component_error:
        SCHEDULER.build((ambiguous_writer, ambiguous_reader))
    assert dict(component_error.value.details) == {
        "components": f"{Position.__module__}.{Position.__qualname__}",
        "first": "ambiguous.reader",
        "resources": "",
        "second": "ambiguous.writer",
    }

    with pytest.raises(ScheduleConflictError) as resource_error:
        SCHEDULER.build((resource_ambiguous, resource_reader))
    assert dict(resource_error.value.details)["resources"] == CLOCK.name

    with pytest.raises(ScheduleConflictError):
        SCHEDULER.build((ambiguous_writer, ambiguous_second_writer))
    with pytest.raises(ScheduleConflictError):
        SCHEDULER.build((resource_ambiguous, resource_second_writer))


def test_direct_and_transitive_order_resolve_conflicts_and_record_metadata() -> None:
    direct = SCHEDULER.build((ordered_reader, ordered_writer))
    assert [spec.name for spec in direct.systems] == ["ordered.writer", "ordered.reader"]
    assert direct.conflicts[0].component_types == (Position,)

    transitive = SCHEDULER.build((transitive_reader, transitive_bridge, transitive_writer))
    assert [spec.name for spec in transitive.systems] == [
        "transitive.writer",
        "transitive.bridge",
        "transitive.reader",
    ]

    resource = SCHEDULER.build((resource_reader, resource_writer))
    assert resource.conflicts[0].resources == (CLOCK,)


def test_fixed_phase_order_resolves_cross_phase_conflict() -> None:
    plan = SCHEDULER.build((cross_sim_reader, cross_pre_writer))
    assert [spec.name for spec in plan.systems] == ["cross.pre_writer", "cross.sim_reader"]
    assert len(plan.conflicts) == 1


def test_unknown_cross_phase_duplicate_and_self_edges_fail_clearly() -> None:
    with pytest.raises(UnknownSystemDependencyError):
        SCHEDULER.build((unknown_source,))
    with pytest.raises(InvalidSystemDependencyError):
        SCHEDULER.build((cross_edge, phase_sim_a))
    with pytest.raises(InvalidSystemDependencyError) as duplicate:
        SCHEDULER.build((duplicate_b, duplicate_a))
    assert duplicate.value.code == "ecs.duplicate_system_dependency"

    candidate = _make_function("dynamic.self")
    with pytest.raises(InvalidSystemSpecError):
        system(name="dynamic.self", before=("dynamic.self",))(candidate)


def test_cycle_error_has_canonical_closed_actionable_path() -> None:
    with pytest.raises(ScheduleCycleError) as caught:
        SCHEDULER.build((cycle_c, cycle_a, cycle_b))

    details = dict(caught.value.details)
    assert details["cycle"] == "cycle.a -> cycle.b -> cycle.c -> cycle.a"
    assert details["schedule_phase"] == "simulate"
    assert details["edges"] == (
        "cycle.a.before(cycle.b) | cycle.b.before(cycle.c) | cycle.c.before(cycle.a)"
    )


def test_empty_and_duplicate_system_plans_are_atomic() -> None:
    assert SCHEDULER.build(()).systems == ()
    with pytest.raises(DuplicateSystemError):
        SCHEDULER.build((phase_pre, phase_pre))


def test_determinism_and_execution_class_gates_run_before_any_invocation() -> None:
    with pytest.raises(NondeterministicSystemError):
        SCHEDULER.build((nondeterministic_system,))
    assert SCHEDULER.build((nondeterministic_system,), require_deterministic=False).systems == (
        system_spec(nondeterministic_system),
    )
    with pytest.raises(NondeterministicSystemError):
        SCHEDULER.build((nondeterministic_resource,))
    with pytest.raises(NondeterministicSystemError) as component_error:
        SCHEDULER.build((nondeterministic_component,))
    details = dict(component_error.value.details)
    assert details["components"] == (
        f"{PresentationMarker.__module__}.{PresentationMarker.__qualname__}"
    )
    assert details["component_type_ids"] == "f4000000-0000-0000-0000-000000000004"
    assert SCHEDULER.build((nondeterministic_component,), require_deterministic=False).systems == (
        system_spec(nondeterministic_component),
    )
    with pytest.raises(UnsupportedExecutionClassError):
        SCHEDULER.build((native_system,), require_deterministic=False)
    assert TRACE == []


def test_unregistered_component_resource_and_undecorated_callable_fail() -> None:
    with pytest.raises(InvalidSystemSpecError):
        SCHEDULER.build((invalid_component,))
    with pytest.raises(InvalidSystemSpecError):
        SCHEDULER.build((invalid_resource,))
    with pytest.raises(InvalidSystemSpecError):
        SCHEDULER.build((undecorated,))


def test_invalid_declaration_collections_and_metadata_fail_before_decoration() -> None:
    with pytest.raises(InvalidSystemSpecError):
        system(component_reads=(Position, Position))
    with pytest.raises(InvalidSystemSpecError):
        system(component_reads=(Position,), component_writes=(Position,))
    with pytest.raises(InvalidSystemSpecError):
        system(resource_reads=(CLOCK,), resource_writes=(CLOCK,))
    with pytest.raises(InvalidSystemSpecError):
        system(resource_reads=(object(),))
    with pytest.raises(InvalidSystemSpecError):
        system(before=("target", "target"))
    with pytest.raises(InvalidSystemSpecError):
        system(before=("target",), after=("target",))
    with pytest.raises(InvalidSystemSpecError):
        system(phase="simulate")  # type: ignore[arg-type]
    with pytest.raises(InvalidSystemSpecError):
        system(deterministic=1)  # type: ignore[arg-type]
    with pytest.raises(InvalidSystemSpecError):
        system(name="bad name")
    with pytest.raises(InvalidSystemSpecError):
        system(component_reads=1)  # type: ignore[arg-type]
    with pytest.raises(InvalidSystemSpecError):
        system(before="target")
    with pytest.raises(InvalidSystemSpecError):
        SCHEDULER.build(1)  # type: ignore[arg-type]


def test_local_lambda_async_and_double_decorated_functions_fail() -> None:
    def local(context: SystemContext, delta: float) -> None:
        del context, delta

    async def asynchronous(context: SystemContext, delta: float) -> None:
        del context, delta

    invalid_lambda: SystemFunction = lambda context, delta: None  # noqa: E731

    with pytest.raises(InvalidSystemSpecError):
        system()(local)
    with pytest.raises(InvalidSystemSpecError):
        system()(invalid_lambda)
    with pytest.raises(InvalidSystemSpecError):
        system()(asynchronous)
    with pytest.raises(InvalidSystemSpecError):
        system()(cast(SystemFunction, generator_system))
    with pytest.raises(InvalidSystemSpecError):
        system()(cast(SystemFunction, bad_signature))
    with pytest.raises(InvalidSystemSpecError):
        system()(SystemHolder.member)
    malformed_signature_metadata.__signature__ = 1  # type: ignore[attr-defined]
    try:
        with pytest.raises(InvalidSystemSpecError) as malformed:
            system()(malformed_signature_metadata)
        assert isinstance(malformed.value.__cause__, TypeError)
    finally:
        del malformed_signature_metadata.__signature__  # type: ignore[attr-defined]

    decorated = _make_function("dynamic.once")
    system(name="dynamic.once")(decorated)
    with pytest.raises(InvalidSystemSpecError):
        system(name="dynamic.twice")(decorated)


def test_schedule_is_frozen() -> None:
    plan = SCHEDULER.build((phase_sim_a,))
    assert isinstance(plan, Schedule)
    with pytest.raises(FrozenInstanceError):
        plan.systems = ()  # type: ignore[misc]


def test_system_spec_direct_reconstruction_revalidates_metadata() -> None:
    with pytest.raises(InvalidSystemSpecError):
        replace(system_spec(phase_pre), name="bad name")


def _template(context: SystemContext, delta: float) -> None:
    del context, delta


def _make_function(name: str) -> FunctionType:
    function_name = name.replace(".", "_").replace(":", "_").replace("-", "_")
    function = FunctionType(_template.__code__, globals(), function_name)
    function.__module__ = __name__
    function.__qualname__ = function_name
    return function
