"""Immutable system declarations and deterministic serial schedule planning."""

from __future__ import annotations

import heapq
import inspect
import re
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from itertools import pairwise
from typing import Protocol, Self, TypeVar, cast, overload

from ludoweave.ecs.commands import DeferredEntity, EntityTarget
from ludoweave.ecs.component import ComponentRegistry, DeterminismTier
from ludoweave.ecs.entity import EntityId
from ludoweave.ecs.errors import (
    ComponentError,
    DuplicateSystemError,
    InvalidSystemDependencyError,
    InvalidSystemSpecError,
    NondeterministicSystemError,
    ScheduleConflictError,
    ScheduleCycleError,
    UnknownSystemDependencyError,
    UnsupportedExecutionClassError,
)
from ludoweave.ecs.resources import ResourceRegistry, ResourceSpec

SystemFunctionT = TypeVar("SystemFunctionT", bound=Callable[..., object])
_SYSTEM_ATTRIBUTE = "__ludoweave_system_spec__"
_SYSTEM_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_.:-]*\Z")


class SystemPhase(StrEnum):
    """Fixed deterministic simulation phases in execution order."""

    PRE_SIMULATE = "pre_simulate"
    SIMULATE = "simulate"
    POST_SIMULATE = "post_simulate"


class ExecutionClass(StrEnum):
    """Declared implementation class; only Python is executable in M1."""

    PYTHON = "python"
    VECTORIZED = "vectorized"
    NATIVE = "native"
    PROCESS = "process"


class SystemRows[*ComponentTs](Protocol):
    """Context-owned row cursor that cannot outlive one system invocation."""

    @property
    def closed(self) -> bool: ...

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: object,
    ) -> bool: ...

    def __iter__(self) -> Self: ...

    def __next__(self) -> tuple[EntityId, *ComponentTs]: ...

    def close(self) -> None: ...

    def abort(self) -> None: ...


class SystemQuery[*ComponentTs](Protocol):
    """Declaration-enforcing storage-neutral query used by systems."""

    def without(self, *component_types: type[object]) -> SystemQuery[*ComponentTs]: ...

    def writes(self, *component_types: type[object]) -> SystemQuery[*ComponentTs]: ...

    def changed_since(
        self, epoch: int, *component_types: type[object]
    ) -> SystemQuery[*ComponentTs]: ...

    def stable(self) -> SystemQuery[*ComponentTs]: ...

    def rows(self) -> SystemRows[*ComponentTs]: ...


class SystemCommands(Protocol):
    """Structural command facade restricted by one system declaration."""

    def spawn(self, component: object, /, *components: object) -> DeferredEntity: ...

    def add(self, target: EntityTarget, component: object) -> None: ...

    def remove(self, target: EntityTarget, component_type: type[object]) -> None: ...


class SystemContext(Protocol):
    """Typed declaration-enforcing seam for one serial system invocation."""

    @property
    def tick(self) -> int: ...

    @property
    def commands(self) -> SystemCommands: ...

    @overload
    def query[ComponentT1](self, component_1: type[ComponentT1], /) -> SystemQuery[ComponentT1]: ...

    @overload
    def query[ComponentT1, ComponentT2](
        self,
        component_1: type[ComponentT1],
        component_2: type[ComponentT2],
        /,
    ) -> SystemQuery[ComponentT1, ComponentT2]: ...

    @overload
    def query[ComponentT1, ComponentT2, ComponentT3](
        self,
        component_1: type[ComponentT1],
        component_2: type[ComponentT2],
        component_3: type[ComponentT3],
        /,
    ) -> SystemQuery[ComponentT1, ComponentT2, ComponentT3]: ...

    @overload
    def query[ComponentT1, ComponentT2, ComponentT3, ComponentT4](
        self,
        component_1: type[ComponentT1],
        component_2: type[ComponentT2],
        component_3: type[ComponentT3],
        component_4: type[ComponentT4],
        /,
    ) -> SystemQuery[ComponentT1, ComponentT2, ComponentT3, ComponentT4]: ...

    @overload
    def query(
        self,
        component_1: type[object],
        component_2: type[object],
        component_3: type[object],
        component_4: type[object],
        component_5: type[object],
        /,
        *component_types: type[object],
    ) -> SystemQuery[*tuple[object, ...]]: ...

    def resource[ResourceT](self, spec: ResourceSpec[ResourceT]) -> ResourceT: ...

    def set_resource[ResourceT](self, spec: ResourceSpec[ResourceT], value: ResourceT) -> None: ...


type SystemFunction = Callable[[SystemContext, float], None]


@dataclass(frozen=True, slots=True)
class SystemSpec:
    """Validated immutable metadata attached to one module-level callable."""

    name: str
    qualified_name: str
    phase: SystemPhase
    component_reads: tuple[type[object], ...]
    component_writes: tuple[type[object], ...]
    resource_reads: tuple[ResourceSpec[object], ...]
    resource_writes: tuple[ResourceSpec[object], ...]
    before: tuple[str, ...]
    after: tuple[str, ...]
    deterministic: bool
    execution_class: ExecutionClass
    function: SystemFunction = field(repr=False, compare=False)

    def __post_init__(self) -> None:
        """Reject forged or directly constructed invalid metadata."""

        _validate_system_name(self.name, field_name="name")
        function_name = _validate_system_function(self.function)
        if self.qualified_name != function_name:
            raise _invalid_system_spec(
                "system qualified name must identify its function",
                details={"system": self.name, "qualified_name": self.qualified_name},
            )
        _require_enum(self.phase, SystemPhase, field_name="phase")
        _require_enum(self.execution_class, ExecutionClass, field_name="execution_class")
        _require_normalized(
            self.component_reads,
            _validate_component_accesses(self.component_reads, role="component_reads"),
            role="component_reads",
        )
        _require_normalized(
            self.component_writes,
            _validate_component_accesses(self.component_writes, role="component_writes"),
            role="component_writes",
        )
        _reject_overlap(
            self.component_reads,
            self.component_writes,
            read_role="component_reads",
            write_role="component_writes",
        )
        _require_normalized(
            self.resource_reads,
            _validate_resource_accesses(self.resource_reads, role="resource_reads"),
            role="resource_reads",
        )
        _require_normalized(
            self.resource_writes,
            _validate_resource_accesses(self.resource_writes, role="resource_writes"),
            role="resource_writes",
        )
        _reject_overlap(
            self.resource_reads,
            self.resource_writes,
            read_role="resource_reads",
            write_role="resource_writes",
        )
        _require_normalized(
            self.before,
            _validate_dependencies(self.before, role="before"),
            role="before",
        )
        _require_normalized(
            self.after,
            _validate_dependencies(self.after, role="after"),
            role="after",
        )
        overlap = set(self.before).intersection(self.after)
        if overlap:
            raise _invalid_system_spec(
                "one dependency cannot appear in both before and after",
                details={"target": min(overlap)},
            )
        if self.name in self.before or self.name in self.after:
            raise _invalid_system_spec(
                "system cannot order itself",
                details={"system": self.name},
            )
        if type(self.deterministic) is not bool:
            raise _invalid_system_spec(
                "system deterministic eligibility must be a boolean",
                details={"actual_type": type(self.deterministic).__name__},
            )


@dataclass(frozen=True, slots=True)
class SystemConflict:
    """Canonical conflict metadata separate from the explicit precedence DAG."""

    first: str
    second: str
    component_types: tuple[type[object], ...]
    resources: tuple[ResourceSpec[object], ...]


@dataclass(frozen=True, slots=True)
class Schedule:
    """Immutable total serial order plus explicit edges and conflict metadata."""

    systems: tuple[SystemSpec, ...]
    conflicts: tuple[SystemConflict, ...]
    explicit_edges: tuple[tuple[str, str], ...]

    def systems_for_phase(self, phase: SystemPhase) -> tuple[SystemSpec, ...]:
        """Return the planned systems for one exact fixed phase."""

        return tuple(spec for spec in self.systems if spec.phase is phase)


def system(
    *,
    name: str | None = None,
    phase: SystemPhase = SystemPhase.SIMULATE,
    component_reads: Iterable[object] = (),
    component_writes: Iterable[object] = (),
    resource_reads: Iterable[object] = (),
    resource_writes: Iterable[object] = (),
    before: Iterable[object] = (),
    after: Iterable[object] = (),
    deterministic: bool = True,
    execution_class: ExecutionClass = ExecutionClass.PYTHON,
) -> Callable[[SystemFunctionT], SystemFunctionT]:
    """Attach one validated system specification without global registration."""

    checked_phase = _require_enum(phase, SystemPhase, field_name="phase")
    checked_execution = _require_enum(execution_class, ExecutionClass, field_name="execution_class")
    checked_component_reads = _validate_component_accesses(component_reads, role="component_reads")
    checked_component_writes = _validate_component_accesses(
        component_writes, role="component_writes"
    )
    _reject_overlap(
        checked_component_reads,
        checked_component_writes,
        read_role="component_reads",
        write_role="component_writes",
    )
    checked_resource_reads = _validate_resource_accesses(resource_reads, role="resource_reads")
    checked_resource_writes = _validate_resource_accesses(resource_writes, role="resource_writes")
    _reject_overlap(
        checked_resource_reads,
        checked_resource_writes,
        read_role="resource_reads",
        write_role="resource_writes",
    )
    checked_before = _validate_dependencies(before, role="before")
    checked_after = _validate_dependencies(after, role="after")
    overlap = set(checked_before).intersection(checked_after)
    if overlap:
        raise _invalid_system_spec(
            "one dependency cannot appear in both before and after",
            details={"target": min(overlap)},
        )
    if type(deterministic) is not bool:
        raise _invalid_system_spec(
            "system deterministic eligibility must be a boolean",
            details={"actual_type": type(deterministic).__name__},
        )
    if name is not None:
        checked_explicit_name = _validate_system_name(name, field_name="name")
    else:
        checked_explicit_name = None

    def decorate(function: SystemFunctionT) -> SystemFunctionT:
        qualified_name = _validate_system_function(function)
        system_name = checked_explicit_name or qualified_name
        if system_name in checked_before or system_name in checked_after:
            raise _invalid_system_spec(
                "system cannot order itself",
                details={"system": system_name},
            )
        if _SYSTEM_ATTRIBUTE in vars(function):
            raise _invalid_system_spec(
                "system function is already decorated",
                details={"system": system_name},
            )
        spec = SystemSpec(
            name=system_name,
            qualified_name=qualified_name,
            phase=checked_phase,
            component_reads=checked_component_reads,
            component_writes=checked_component_writes,
            resource_reads=checked_resource_reads,
            resource_writes=checked_resource_writes,
            before=checked_before,
            after=checked_after,
            deterministic=deterministic,
            execution_class=checked_execution,
            function=cast(SystemFunction, function),
        )
        setattr(function, _SYSTEM_ATTRIBUTE, spec)
        return function

    return decorate


def system_spec(definition: object) -> SystemSpec:
    """Return attached metadata or raise a structured declaration error."""

    if not callable(definition):
        raise _invalid_system_spec(
            "system lookup requires a callable",
            details={"actual_type": type(definition).__name__},
            phase="inspect",
        )
    try:
        spec = vars(definition).get(_SYSTEM_ATTRIBUTE)
    except TypeError as error:
        raise _invalid_system_spec(
            "system callable has no inspectable declaration metadata",
            details={"actual_type": type(definition).__name__},
            phase="inspect",
        ) from error
    if isinstance(spec, SystemSpec):
        return spec
    raise _invalid_system_spec(
        "callable is not decorated with @system",
        details={"callable_type": type(definition).__name__},
        phase="inspect",
    )


class Scheduler:
    """Build deterministic serial plans without invoking system functions."""

    __slots__ = ("_component_registry", "_resource_registry")

    def __init__(
        self,
        component_registry: ComponentRegistry,
        resource_registry: ResourceRegistry,
    ) -> None:
        self._component_registry = component_registry
        self._resource_registry = resource_registry

    def build(
        self,
        definitions: Iterable[object],
        *,
        require_deterministic: bool = True,
    ) -> Schedule:
        """Validate declarations and return one immutable stable serial plan."""

        if type(require_deterministic) is not bool:
            raise _invalid_system_spec(
                "require_deterministic must be a boolean",
                details={"actual_type": type(require_deterministic).__name__},
                phase="plan",
            )
        by_name: dict[str, SystemSpec] = {}
        for definition in _declaration_items(definitions, role="systems", phase="plan"):
            spec = system_spec(definition)
            if spec.name in by_name:
                raise DuplicateSystemError(
                    "schedule contains a duplicate system identity",
                    code="ecs.duplicate_system",
                    subsystem="ecs",
                    phase="plan",
                    details={"system": spec.name},
                )
            self._validate_accesses(spec)
            if spec.execution_class is not ExecutionClass.PYTHON:
                raise UnsupportedExecutionClassError(
                    "M1 schedules support only Python systems",
                    code="ecs.unsupported_execution_class",
                    subsystem="ecs",
                    phase="plan",
                    details={
                        "system": spec.name,
                        "execution_class": spec.execution_class.value,
                    },
                )
            if require_deterministic and not spec.deterministic:
                raise NondeterministicSystemError(
                    "deterministic schedule includes an ineligible system",
                    code="ecs.nondeterministic_system",
                    subsystem="ecs",
                    phase="plan",
                    details={"system": spec.name},
                )
            if require_deterministic:
                nondeterministic_components = tuple(
                    self._component_registry.schema_for_type(component_type)
                    for component_type in (*spec.component_reads, *spec.component_writes)
                    if self._component_registry.schema_for_type(component_type).determinism
                    is DeterminismTier.D0
                )
                if nondeterministic_components:
                    raise NondeterministicSystemError(
                        "deterministic schedule accesses a D0 component",
                        code="ecs.nondeterministic_component",
                        subsystem="ecs",
                        phase="plan",
                        details={
                            "system": spec.name,
                            "components": ",".join(
                                schema.qualified_name
                                for schema in sorted(
                                    nondeterministic_components,
                                    key=lambda item: item.type_id.bytes,
                                )
                            ),
                            "component_type_ids": ",".join(
                                str(schema.type_id)
                                for schema in sorted(
                                    nondeterministic_components,
                                    key=lambda item: item.type_id.bytes,
                                )
                            ),
                        },
                    )
                nondeterministic_resources = tuple(
                    resource.name
                    for resource in (*spec.resource_reads, *spec.resource_writes)
                    if not resource.deterministic
                )
                if nondeterministic_resources:
                    raise NondeterministicSystemError(
                        "deterministic schedule accesses an ineligible resource",
                        code="ecs.nondeterministic_resource",
                        subsystem="ecs",
                        phase="plan",
                        details={
                            "system": spec.name,
                            "resources": ",".join(sorted(nondeterministic_resources)),
                        },
                    )
            by_name[spec.name] = spec

        adjacency, edge_sources = _build_explicit_graph(by_name)
        ordered_names: list[str] = []
        for phase in SystemPhase:
            phase_names = tuple(
                sorted(name for name, spec in by_name.items() if spec.phase is phase)
            )
            ordered_names.extend(
                _topological_phase_order(phase, phase_names, adjacency, edge_sources)
            )

        conflicts = self._conflicts(by_name)
        for conflict in conflicts:
            first = by_name[conflict.first]
            second = by_name[conflict.second]
            if first.phase is second.phase and not (
                _has_path(first.name, second.name, adjacency)
                or _has_path(second.name, first.name, adjacency)
            ):
                raise ScheduleConflictError(
                    "same-phase write conflict requires explicit ordering",
                    code="ecs.ambiguous_schedule_conflict",
                    subsystem="ecs",
                    phase="plan",
                    details={
                        "first": conflict.first,
                        "second": conflict.second,
                        "components": ",".join(
                            self._component_registry.schema_for_type(item).qualified_name
                            for item in conflict.component_types
                        ),
                        "resources": ",".join(item.name for item in conflict.resources),
                    },
                )

        return Schedule(
            systems=tuple(by_name[name] for name in ordered_names),
            conflicts=conflicts,
            explicit_edges=tuple(sorted(edge_sources)),
        )

    def _validate_accesses(self, spec: SystemSpec) -> None:
        for component_type in (*spec.component_reads, *spec.component_writes):
            try:
                self._component_registry.schema_for_type(component_type)
            except ComponentError as error:
                raise _invalid_system_spec(
                    "system accesses an unregistered component type",
                    details={
                        "system": spec.name,
                        "component_type": _type_name(component_type),
                    },
                    phase="plan",
                ) from error
        for resource in (*spec.resource_reads, *spec.resource_writes):
            if not self._resource_registry.contains(resource):
                raise _invalid_system_spec(
                    "system accesses a resource from another registry",
                    details={"system": spec.name, "resource": resource.name},
                    phase="plan",
                )

    def _conflicts(self, by_name: Mapping[str, SystemSpec]) -> tuple[SystemConflict, ...]:
        records: list[SystemConflict] = []
        names = tuple(sorted(by_name))
        for index, first_name in enumerate(names):
            first = by_name[first_name]
            for second_name in names[index + 1 :]:
                second = by_name[second_name]
                component_conflicts = _conflicting_items(
                    first.component_reads,
                    first.component_writes,
                    second.component_reads,
                    second.component_writes,
                )
                resource_conflicts = _conflicting_items(
                    first.resource_reads,
                    first.resource_writes,
                    second.resource_reads,
                    second.resource_writes,
                )
                if not component_conflicts and not resource_conflicts:
                    continue
                records.append(
                    SystemConflict(
                        first=first_name,
                        second=second_name,
                        component_types=tuple(
                            sorted(
                                component_conflicts,
                                key=lambda item: (
                                    self._component_registry.schema_for_type(item).type_id.bytes
                                ),
                            )
                        ),
                        resources=tuple(
                            sorted(
                                resource_conflicts,
                                key=lambda item: item.name,
                            )
                        ),
                    )
                )
        return tuple(records)


def _build_explicit_graph(
    by_name: Mapping[str, SystemSpec],
) -> tuple[dict[str, set[str]], dict[tuple[str, str], str]]:
    adjacency = {name: set[str]() for name in by_name}
    edge_sources: dict[tuple[str, str], str] = {}
    for name in sorted(by_name):
        spec = by_name[name]
        for target in spec.before:
            _add_dependency(
                spec,
                target,
                source=name,
                destination=target,
                by_name=by_name,
                adjacency=adjacency,
                edge_sources=edge_sources,
                declaration="before",
            )
        for target in spec.after:
            _add_dependency(
                spec,
                target,
                source=target,
                destination=name,
                by_name=by_name,
                adjacency=adjacency,
                edge_sources=edge_sources,
                declaration="after",
            )
    return adjacency, edge_sources


def _add_dependency(
    spec: SystemSpec,
    target: str,
    *,
    source: str,
    destination: str,
    by_name: Mapping[str, SystemSpec],
    adjacency: dict[str, set[str]],
    edge_sources: dict[tuple[str, str], str],
    declaration: str,
) -> None:
    target_spec = by_name.get(target)
    if target_spec is None:
        raise UnknownSystemDependencyError(
            "system ordering target is not registered",
            code="ecs.unknown_system_dependency",
            subsystem="ecs",
            phase="plan",
            details={"system": spec.name, "target": target, "declaration": declaration},
        )
    if target_spec.phase is not spec.phase:
        raise InvalidSystemDependencyError(
            "explicit ordering edges must remain within one fixed phase",
            code="ecs.cross_phase_dependency",
            subsystem="ecs",
            phase="plan",
            details={
                "system": spec.name,
                "target": target,
                "system_phase": spec.phase.value,
                "target_phase": target_spec.phase.value,
            },
        )
    edge = (source, destination)
    if edge in edge_sources:
        raise InvalidSystemDependencyError(
            "logical system ordering edge is declared more than once",
            code="ecs.duplicate_system_dependency",
            subsystem="ecs",
            phase="plan",
            details={"source": source, "destination": destination},
        )
    adjacency[source].add(destination)
    edge_sources[edge] = f"{spec.name}.{declaration}({target})"


def _topological_phase_order(
    phase: SystemPhase,
    names: tuple[str, ...],
    adjacency: Mapping[str, set[str]],
    edge_sources: Mapping[tuple[str, str], str],
) -> tuple[str, ...]:
    members = set(names)
    indegree = {name: 0 for name in names}
    for source in names:
        for destination in adjacency[source]:
            if destination in members:
                indegree[destination] += 1
    ready = [name for name in names if indegree[name] == 0]
    heapq.heapify(ready)
    ordered: list[str] = []
    while ready:
        current = heapq.heappop(ready)
        ordered.append(current)
        for destination in sorted(adjacency[current]):
            if destination not in members:
                continue
            indegree[destination] -= 1
            if indegree[destination] == 0:
                heapq.heappush(ready, destination)
    if len(ordered) != len(names):
        cycle = _canonical_cycle(names, adjacency)
        descriptions = tuple(edge_sources[(left, right)] for left, right in pairwise(cycle))
        raise ScheduleCycleError(
            "explicit system ordering contains a cycle",
            code="ecs.schedule_cycle",
            subsystem="ecs",
            phase="plan",
            details={
                "schedule_phase": phase.value,
                "cycle": " -> ".join(cycle),
                "edges": " | ".join(descriptions),
            },
        )
    return tuple(ordered)


def _canonical_cycle(names: tuple[str, ...], adjacency: Mapping[str, set[str]]) -> tuple[str, ...]:
    members = set(names)
    index = 0
    indexes: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    components: list[tuple[str, ...]] = []

    def connect(node: str) -> None:
        nonlocal index
        indexes[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for neighbor in sorted(item for item in adjacency[node] if item in members):
            if neighbor not in indexes:
                connect(neighbor)
                lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
            elif neighbor in on_stack:
                lowlinks[node] = min(lowlinks[node], indexes[neighbor])
        if lowlinks[node] != indexes[node]:
            return
        component: list[str] = []
        while True:
            current = stack.pop()
            on_stack.remove(current)
            component.append(current)
            if current == node:
                break
        if len(component) > 1:
            components.append(tuple(sorted(component)))

    for name in sorted(names):
        if name not in indexes:
            connect(name)
    selected = min(components, key=lambda item: item[0])
    selected_set = set(selected)
    start = selected[0]

    def find_path(current: str, path: tuple[str, ...]) -> tuple[str, ...] | None:
        for neighbor in sorted(item for item in adjacency[current] if item in selected_set):
            if neighbor == start:
                return (*path, start)
            if neighbor in path:
                continue
            found = find_path(neighbor, (*path, neighbor))
            if found is not None:
                return found
        return None

    result = find_path(start, (start,))
    assert result is not None
    return result


def _has_path(source: str, destination: str, adjacency: Mapping[str, set[str]]) -> bool:
    pending = [source]
    visited: set[str] = set()
    while pending:
        current = pending.pop()
        if current in visited:
            continue
        visited.add(current)
        for neighbor in sorted(adjacency[current], reverse=True):
            if neighbor == destination:
                return True
            pending.append(neighbor)
    return False


def _conflicting_items[ItemT](
    first_reads: tuple[ItemT, ...],
    first_writes: tuple[ItemT, ...],
    second_reads: tuple[ItemT, ...],
    second_writes: tuple[ItemT, ...],
) -> set[ItemT]:
    first_read_set = set(first_reads)
    first_write_set = set(first_writes)
    second_read_set = set(second_reads)
    second_write_set = set(second_writes)
    return (first_write_set & (second_read_set | second_write_set)) | (
        second_write_set & (first_read_set | first_write_set)
    )


def _validate_system_function(function: object) -> str:
    if (
        not inspect.isfunction(function)
        or inspect.iscoroutinefunction(function)
        or inspect.isgeneratorfunction(function)
        or inspect.isasyncgenfunction(function)
    ):
        raise _invalid_system_spec(
            "system must be a synchronous module-level Python function",
            details={"actual_type": type(function).__name__},
        )
    qualified_name = f"{function.__module__}.{function.__qualname__}"
    if (
        "<locals>" in qualified_name
        or function.__name__ == "<lambda>"
        or function.__qualname__ != function.__name__
    ):
        raise _invalid_system_spec(
            "system function must have a stable module-qualified name",
            details={"qualified_name": qualified_name},
        )
    try:
        parameters = tuple(inspect.signature(function).parameters.values())
    except Exception as error:
        raise _invalid_system_spec(
            "system function signature could not be inspected",
            details={
                "qualified_name": qualified_name,
                "cause_type": type(error).__name__,
            },
        ) from error
    if len(parameters) != 2 or any(
        parameter.kind
        not in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        or parameter.default is not inspect.Parameter.empty
        for parameter in parameters
    ):
        raise _invalid_system_spec(
            "system function must accept exactly context and delta positional arguments",
            details={"qualified_name": qualified_name},
        )
    return qualified_name


def _validate_component_accesses(
    values: Iterable[object], *, role: str
) -> tuple[type[object], ...]:
    checked: list[type[object]] = []
    seen: set[type[object]] = set()
    for value in _declaration_items(values, role=role):
        if not isinstance(value, type):
            raise _invalid_system_spec(
                "component access declarations must contain classes",
                details={"role": role, "actual_type": type(value).__name__},
            )
        if value in seen:
            raise _invalid_system_spec(
                "component access declaration contains a duplicate type",
                details={"role": role, "component_type": _type_name(value)},
            )
        seen.add(value)
        checked.append(value)
    return tuple(sorted(checked, key=_type_name))


def _validate_resource_accesses(
    values: Iterable[object], *, role: str
) -> tuple[ResourceSpec[object], ...]:
    checked: list[ResourceSpec[object]] = []
    seen: set[ResourceSpec[object]] = set()
    for value in _declaration_items(values, role=role):
        if not isinstance(value, ResourceSpec):
            raise _invalid_system_spec(
                "resource access declarations must contain ResourceSpec values",
                details={"role": role, "actual_type": type(value).__name__},
            )
        spec = cast(ResourceSpec[object], value)
        if spec in seen:
            raise _invalid_system_spec(
                "resource access declaration contains a duplicate key",
                details={"role": role, "resource": spec.name},
            )
        seen.add(spec)
        checked.append(spec)
    return tuple(sorted(checked, key=lambda item: item.name))


def _validate_dependencies(values: Iterable[object], *, role: str) -> tuple[str, ...]:
    checked: list[str] = []
    seen: set[str] = set()
    for value in _declaration_items(values, role=role):
        name = _validate_system_name(value, field_name=role)
        if name in seen:
            raise _invalid_system_spec(
                "system dependency declaration contains a duplicate target",
                details={"role": role, "target": name},
            )
        seen.add(name)
        checked.append(name)
    return tuple(sorted(checked))


def _reject_overlap[ItemT](
    reads: tuple[ItemT, ...],
    writes: tuple[ItemT, ...],
    *,
    read_role: str,
    write_role: str,
) -> None:
    if set(reads).intersection(writes):
        raise _invalid_system_spec(
            "write access already includes read capability",
            details={"read_role": read_role, "write_role": write_role},
        )


def _require_normalized[ItemT](
    actual: tuple[ItemT, ...], expected: tuple[ItemT, ...], *, role: str
) -> None:
    if actual != expected:
        raise _invalid_system_spec(
            "system metadata must use canonical tuple ordering",
            details={"role": role},
        )


def _declaration_items(
    values: Iterable[object], *, role: str, phase: str = "define"
) -> tuple[object, ...]:
    if isinstance(values, (str, bytes)):
        raise _invalid_system_spec(
            "system declaration collection must be an iterable of values",
            details={"role": role, "actual_type": type(values).__name__},
            phase=phase,
        )
    try:
        return tuple(values)
    except Exception as error:
        raise _invalid_system_spec(
            "system declaration collection could not be materialized",
            details={
                "role": role,
                "actual_type": type(values).__name__,
                "cause_type": type(error).__name__,
            },
            phase=phase,
        ) from error


def _validate_system_name(value: object, *, field_name: str) -> str:
    if type(value) is not str or _SYSTEM_NAME.fullmatch(value) is None:
        raise _invalid_system_spec(
            "system identity and dependency names must be stable nonempty strings",
            details={"field": field_name, "actual_type": type(value).__name__},
        )
    return value


def _require_enum[EnumT: StrEnum](
    value: object, enum_type: type[EnumT], *, field_name: str
) -> EnumT:
    if not isinstance(value, enum_type):
        raise _invalid_system_spec(
            "system enum metadata must use the declared enum type",
            details={"field": field_name, "actual_type": type(value).__name__},
        )
    return value


def _type_name(value: type[object]) -> str:
    return f"{value.__module__}.{value.__qualname__}"


def _invalid_system_spec(
    message: str,
    *,
    details: dict[str, str | int | float | bool | None],
    phase: str = "define",
) -> InvalidSystemSpecError:
    return InvalidSystemSpecError(
        message,
        code="ecs.invalid_system_spec",
        subsystem="ecs",
        phase=phase,
        details=details,
    )
