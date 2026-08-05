"""Property tests for exact accumulator units and time partition equivalence."""

from hypothesis import given
from hypothesis import strategies as st

from ludoweave.app import (
    INPUT_SNAPSHOT_RESOURCE,
    ApplicationConfig,
    FixedStepApplication,
    NullInputSource,
)
from ludoweave.core.clock import VirtualClock
from ludoweave.ecs import ComponentRegistry, ResourceRegistry, ResourceStore, Scheduler, World
from ludoweave.render import NullRenderBackend


def _application(
    *, fixed_hz: int, catch_up_limit: int
) -> tuple[FixedStepApplication, VirtualClock, ResourceStore]:
    components = ComponentRegistry()
    resource_registry = ResourceRegistry((INPUT_SNAPSHOT_RESOURCE,))
    resources = ResourceStore(resource_registry)
    application = FixedStepApplication(
        ApplicationConfig(fixed_hz=fixed_hz, catch_up_limit=catch_up_limit),
        NullRenderBackend(),
        World(components),
        resources,
        Scheduler(components, resource_registry).build(()),
        NullInputSource(),
        clock=(clock := VirtualClock()),
    )
    application.initialize()
    return application, clock, resources


def _drive_and_drain(
    chunks: list[int], *, fixed_hz: int, catch_up_limit: int
) -> tuple[int, float, int | None]:
    application, clock, resources = _application(
        fixed_hz=fixed_hz,
        catch_up_limit=catch_up_limit,
    )
    final_alpha = 0.0
    for elapsed_ns in chunks:
        clock.advance_ns(elapsed_ns)
        final_alpha = application.pump().interpolation_alpha
    while application.backlog_ticks:
        final_alpha = application.pump().interpolation_alpha
    tick = (
        resources.require(INPUT_SNAPSHOT_RESOURCE).tick
        if resources.contains(INPUT_SNAPSHOT_RESOURCE)
        else None
    )
    total = application.total_ticks
    application.close()
    return total, final_alpha, tick


@given(
    chunks=st.lists(
        st.integers(min_value=0, max_value=100_000_000),
        min_size=1,
        max_size=10,
    ),
    fixed_hz=st.integers(min_value=1, max_value=240),
    catch_up_limit=st.integers(min_value=1, max_value=8),
)
def test_accumulator_matches_independent_integer_units_model(
    chunks: list[int], fixed_hz: int, catch_up_limit: int
) -> None:
    total_ns = sum(chunks)
    expected_ticks, remainder = divmod(total_ns * fixed_hz, 1_000_000_000)

    ticks, alpha, input_tick = _drive_and_drain(
        chunks,
        fixed_hz=fixed_hz,
        catch_up_limit=catch_up_limit,
    )

    assert ticks == expected_ticks
    assert alpha == remainder / 1_000_000_000
    assert input_tick == (expected_ticks - 1 if expected_ticks else None)


@given(
    chunks=st.lists(
        st.integers(min_value=0, max_value=50_000_000),
        min_size=1,
        max_size=8,
    ),
    fixed_hz=st.sampled_from((3, 7, 60, 144)),
    catch_up_limit=st.integers(min_value=1, max_value=5),
)
def test_time_partition_and_catch_up_grouping_do_not_change_tick_outcome(
    chunks: list[int], fixed_hz: int, catch_up_limit: int
) -> None:
    partitioned = _drive_and_drain(
        chunks,
        fixed_hz=fixed_hz,
        catch_up_limit=catch_up_limit,
    )
    single = _drive_and_drain(
        [sum(chunks)],
        fixed_hz=fixed_hz,
        catch_up_limit=catch_up_limit,
    )

    assert partitioned == single
