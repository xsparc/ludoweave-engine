"""Property coverage for stable schedule planning and graph diagnostics."""

from collections.abc import Iterable
from dataclasses import dataclass
from types import FunctionType
from typing import cast
from uuid import UUID

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.ecs import (
    ComponentRegistry,
    ResourceRegistry,
    ScheduleConflictError,
    ScheduleCycleError,
    Scheduler,
    SystemContext,
    SystemFunction,
    component,
    system,
)

NAMES = ("graph.a", "graph.b", "graph.c", "graph.d")
PAIRS = tuple(
    (source, target) for index, source in enumerate(NAMES) for target in NAMES[index + 1 :]
)


@component(type_id=UUID("f5000000-0000-0000-0000-000000000001"))
@dataclass(slots=True)
class GraphValue:
    value: int = 0


SCHEDULER = Scheduler(ComponentRegistry((GraphValue,)), ResourceRegistry())


@system(name="conflict.reader", component_reads=(GraphValue,))
def conflict_reader(context: SystemContext, delta: float) -> None:
    del context, delta


@system(name="conflict.writer", component_writes=(GraphValue,))
def conflict_writer(context: SystemContext, delta: float) -> None:
    del context, delta


@given(
    basis=st.permutations(NAMES),
    enabled=st.lists(st.booleans(), min_size=len(PAIRS), max_size=len(PAIRS)),
    input_order=st.permutations(NAMES),
)
def test_acyclic_graph_plan_matches_stable_topological_model(
    basis: list[str], enabled: list[bool], input_order: list[str]
) -> None:
    rank = {name: index for index, name in enumerate(basis)}
    possible_edges = tuple(
        (source, target) for source in NAMES for target in NAMES if rank[source] < rank[target]
    )
    edges = {edge for edge, include in zip(possible_edges, enabled, strict=True) if include}
    definitions = _definitions_for_edges(edges)

    plan = SCHEDULER.build(tuple(definitions[name] for name in input_order))

    assert tuple(spec.name for spec in plan.systems) == _stable_topological_order(edges)
    assert plan.explicit_edges == tuple(sorted(edges))


@given(input_order=st.permutations(("cycle.a", "cycle.b", "cycle.c")))
def test_cycle_path_is_canonical_across_input_order(input_order: list[str]) -> None:
    edges = {
        ("cycle.a", "cycle.b"),
        ("cycle.b", "cycle.c"),
        ("cycle.c", "cycle.a"),
    }
    definitions = _definitions_for_edges(edges)

    with pytest.raises(ScheduleCycleError) as caught:
        SCHEDULER.build(tuple(definitions[name] for name in input_order))

    assert dict(caught.value.details)["cycle"] == "cycle.a -> cycle.b -> cycle.c -> cycle.a"


@given(order=st.permutations((conflict_reader, conflict_writer)))
def test_unordered_conflict_is_canonical_across_input_order(
    order: list[SystemFunction],
) -> None:
    with pytest.raises(ScheduleConflictError) as caught:
        SCHEDULER.build(order)

    details = dict(caught.value.details)
    assert details["first"] == "conflict.reader"
    assert details["second"] == "conflict.writer"


def _system_template(context: SystemContext, delta: float) -> None:
    del context, delta


def _definitions_for_edges(edges: set[tuple[str, str]]) -> dict[str, SystemFunction]:
    names = sorted({name for edge in edges for name in edge} | set(NAMES))
    definitions: dict[str, SystemFunction] = {}
    for name in names:
        before = tuple(sorted(target for source, target in edges if source == name))
        function_name = name.replace(".", "_").replace(":", "_").replace("-", "_")
        function = FunctionType(_system_template.__code__, globals(), function_name)
        function.__module__ = __name__
        function.__qualname__ = function_name
        typed = cast(SystemFunction, function)
        definitions[name] = system(name=name, before=before)(typed)
    return definitions


def _stable_topological_order(edges: Iterable[tuple[str, str]]) -> tuple[str, ...]:
    adjacency: dict[str, set[str]] = {name: set() for name in NAMES}
    indegree: dict[str, int] = dict.fromkeys(NAMES, 0)
    for source, target in edges:
        adjacency[source].add(target)
        indegree[target] += 1

    ready = sorted(name for name, degree in indegree.items() if degree == 0)
    ordered: list[str] = []
    while ready:
        current = ready.pop(0)
        ordered.append(current)
        for target in sorted(adjacency[current]):
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)
                ready.sort()
    return tuple(ordered)
