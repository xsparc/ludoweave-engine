# pyright: reportPrivateUsage=false
"""Additive fixed-step application runtime over public ECS contracts."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from threading import get_ident
from types import TracebackType
from typing import Protocol, Self, cast, overload

from ludoweave.app.errors import (
    ApplicationError,
    InputFrameError,
    SystemAccessError,
    SystemExecutionError,
)
from ludoweave.app.input import INPUT_SNAPSHOT_RESOURCE, InputSnapshot, InputSource
from ludoweave.app.lifecycle import LifecycleState
from ludoweave.core.clock import Clock, MonotonicClock
from ludoweave.core.errors import ConfigurationError, LudoWeaveError
from ludoweave.ecs.commands import Commands, DeferredEntity, EntityTarget
from ludoweave.ecs.component import DeterminismTier
from ludoweave.ecs.query import Query, QueryRows
from ludoweave.ecs.resources import ResourceSpec, ResourceStore
from ludoweave.ecs.schedule import (
    ExecutionClass,
    Schedule,
    Scheduler,
    SystemCommands,
    SystemContext,
    SystemPhase,
    SystemQuery,
    SystemSpec,
)
from ludoweave.ecs.world import WorldStore
from ludoweave.render.api import RenderBackend, RenderDescriptor

_TICK_UNITS = 1_000_000_000


@dataclass(frozen=True, slots=True)
class ApplicationConfig:
    """Exact fixed-step and catch-up policy for one application."""

    fixed_hz: int = 60
    catch_up_limit: int = 4

    def __post_init__(self) -> None:
        _require_positive_config(self.fixed_hz, field="fixed_hz")
        _require_positive_config(self.catch_up_limit, field="catch_up_limit")


@dataclass(frozen=True, slots=True)
class FrameSummary:
    """Presentation-frame result; only tick counts are authoritative."""

    frame: int
    ticks_executed: int
    total_ticks: int
    backlog_ticks: int
    interpolation_alpha: float
    sampled_ns: int
    renderer: str


@dataclass(frozen=True, slots=True)
class ApplicationRunSummary:
    """Immutable result of deterministic exact-tick convenience execution."""

    ticks: int
    frames: int
    start_ns: int
    end_ns: int
    fixed_hz: int
    renderer: str

    @property
    def elapsed_ns(self) -> int:
        return self.end_ns - self.start_ns


class _AbortableRows(Protocol):
    @property
    def closed(self) -> bool: ...

    @property
    def writable(self) -> bool: ...

    def _abort_for_cleanup(self) -> None: ...


class _QueryWorld(Protocol):
    def query(self, *component_types: type[object]) -> Query[*tuple[object, ...]]: ...


class _ManagedRows[*ComponentTs]:
    """Invocation-scoped cursor wrapper tracked by its system context."""

    __slots__ = ("_context", "_rows", "_writable")

    def __init__(
        self,
        context: _InvocationContext,
        rows: QueryRows[*ComponentTs],
        *,
        writable: bool,
    ) -> None:
        self._context = context
        self._rows = rows
        self._writable = writable

    @property
    def closed(self) -> bool:
        return self._rows.closed

    @property
    def writable(self) -> bool:
        return self._writable

    def __enter__(self) -> Self:
        self._context._require_active(operation="query_enter")
        self._rows.__enter__()
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: object,
    ) -> bool:
        self._context._require_active(operation="query_exit")
        return self._rows.__exit__(
            exception_type,
            exception,
            cast(TracebackType | None, traceback),
        )

    def __iter__(self) -> Self:
        self._context._require_active(operation="query_iterate")
        iter(self._rows)
        return self

    def __next__(self) -> tuple[object, ...]:
        self._context._require_active(operation="query_iterate")
        return cast(tuple[object, ...], next(self._rows))

    def close(self) -> None:
        self._context._require_active(operation="query_close")
        self._rows.close()

    def abort(self) -> None:
        self._context._require_active(operation="query_abort")
        self._rows.abort()

    def _abort_for_cleanup(self) -> None:
        self._rows.abort()


class _RestrictedQuery[*ComponentTs]:
    """Query builder that checks every extension against one system spec."""

    __slots__ = ("_context", "_query", "_writable")

    def __init__(
        self,
        context: _InvocationContext,
        query: Query[*ComponentTs],
        *,
        writable: bool = False,
    ) -> None:
        self._context = context
        self._query = query
        self._writable = writable

    def without(self, *component_types: type[object]) -> _RestrictedQuery[*ComponentTs]:
        self._context._require_component_access(
            component_types, write=False, operation="query_without"
        )
        return _RestrictedQuery(
            self._context,
            self._query.without(*component_types),
            writable=self._writable,
        )

    def writes(self, *component_types: type[object]) -> _RestrictedQuery[*ComponentTs]:
        self._context._require_component_access(
            component_types, write=True, operation="query_writes"
        )
        return _RestrictedQuery(
            self._context,
            self._query.writes(*component_types),
            writable=True,
        )

    def changed_since(
        self, epoch: int, *component_types: type[object]
    ) -> _RestrictedQuery[*ComponentTs]:
        watched = component_types
        if watched:
            self._context._require_component_access(
                watched, write=False, operation="query_changed_since"
            )
        self._context._require_active(operation="query_changed_since")
        return _RestrictedQuery(
            self._context,
            self._query.changed_since(epoch, *component_types),
            writable=self._writable,
        )

    def stable(self) -> _RestrictedQuery[*ComponentTs]:
        self._context._require_active(operation="query_stable")
        return _RestrictedQuery(
            self._context,
            self._query.stable(),
            writable=self._writable,
        )

    def rows(self) -> _ManagedRows[*ComponentTs]:
        self._context._require_active(operation="query_rows")
        rows = _ManagedRows(
            self._context,
            self._query.rows(),
            writable=self._writable,
        )
        self._context._track_rows(cast(_AbortableRows, rows))
        return rows


class _RestrictedCommands:
    """Invocation-scoped command facade enforcing declared component writes."""

    __slots__ = ("_commands", "_context", "_structural_allowed")

    def __init__(
        self,
        context: _InvocationContext,
        commands: Commands,
        *,
        structural_allowed: bool,
    ) -> None:
        self._context = context
        self._commands = commands
        self._structural_allowed = structural_allowed

    def spawn(self, *components: object) -> DeferredEntity:
        self._require_structural("commands_spawn")
        if not components:
            raise self._context._access_error(
                "empty entity creation has no M1 structural access declaration",
                operation="commands_spawn",
                target="world.structure",
                requested="write",
            )
        self._context._require_component_access(
            tuple(type(component) for component in components),
            write=True,
            operation="commands_spawn",
        )
        return self._commands.spawn(*components)

    def destroy(self, target: EntityTarget) -> None:
        del target
        self._require_structural("commands_destroy")
        raise self._context._access_error(
            "entity destruction cannot be represented by M1 component access declarations",
            operation="commands_destroy",
            target="world.structure",
            requested="write",
        )

    def add(self, target: EntityTarget, component: object) -> None:
        self._require_structural("commands_add")
        self._context._require_component_access(
            (type(component),), write=True, operation="commands_add"
        )
        self._commands.add(target, component)

    def remove(self, target: EntityTarget, component_type: type[object]) -> None:
        self._require_structural("commands_remove")
        self._context._require_component_access(
            (component_type,), write=True, operation="commands_remove"
        )
        self._commands.remove(target, component_type)

    def _require_structural(self, operation: str) -> None:
        self._context._require_active(operation=operation)
        if not self._structural_allowed:
            raise self._context._access_error(
                "post-simulate systems cannot enqueue structural commands",
                operation=operation,
                target="world.structure",
                requested="write",
            )


class _InvocationContext:
    """Concrete access-enforcing context active for one synchronous call."""

    __slots__ = (
        "_active",
        "_commands_facade",
        "_component_reads",
        "_component_writes",
        "_phase",
        "_resource_reads",
        "_resource_values",
        "_resource_writes",
        "_resources",
        "_rows",
        "_spec",
        "_staged_resources",
        "_tick",
        "_world",
    )

    def __init__(
        self,
        *,
        tick: int,
        phase: SystemPhase,
        spec: SystemSpec,
        world: WorldStore,
        resources: ResourceStore,
        commands: Commands,
    ) -> None:
        self._tick = tick
        self._phase = phase
        self._spec = spec
        self._world = world
        self._resources = resources
        self._component_reads = frozenset((*spec.component_reads, *spec.component_writes))
        self._component_writes = frozenset(spec.component_writes)
        self._resource_reads = frozenset((*spec.resource_reads, *spec.resource_writes))
        self._resource_writes = frozenset(spec.resource_writes)
        self._resource_values: dict[ResourceSpec[object], object] = {}
        self._staged_resources: dict[ResourceSpec[object], object] = {}
        self._rows: list[_AbortableRows] = []
        self._active = True
        self._commands_facade = _RestrictedCommands(
            self,
            commands,
            structural_allowed=phase is not SystemPhase.POST_SIMULATE,
        )

    @property
    def tick(self) -> int:
        self._require_active(operation="tick")
        return self._tick

    @property
    def commands(self) -> SystemCommands:
        self._require_active(operation="commands")
        return self._commands_facade

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

    def query(self, *component_types: type[object]) -> object:
        if not component_types:
            raise self._access_error(
                "entity-set queries have no M1 structural access declaration",
                operation="query",
                target="world.structure",
                requested="read",
            )
        self._require_component_access(component_types, write=False, operation="query")
        world = cast(_QueryWorld, self._world)
        raw = world.query(*component_types).stable()
        return _RestrictedQuery(self, raw)

    def resource[ResourceT](self, spec: ResourceSpec[ResourceT]) -> ResourceT:
        self._require_resource_access(spec, write=False, operation="resource")
        checked = cast(ResourceSpec[object], spec)
        if checked not in self._resource_values:
            self._resource_values[checked] = self._resources.require(spec)
        return cast(ResourceT, self._resource_values[checked])

    def set_resource[ResourceT](self, spec: ResourceSpec[ResourceT], value: ResourceT) -> None:
        self._require_resource_access(spec, write=True, operation="set_resource")
        checked = cast(ResourceSpec[object], spec)
        self._resource_values[checked] = value
        self._staged_resources[checked] = value

    def finish(self, *, failed: bool) -> None:
        pending_writable = False
        try:
            for rows in self._rows:
                if rows.closed:
                    continue
                pending_writable = pending_writable or rows.writable
                rows._abort_for_cleanup()
            if failed:
                return
            if pending_writable:
                raise self._access_error(
                    "system returned with an open writable query cursor",
                    operation="system_return",
                    target="query.cursor",
                    requested="close",
                )
            for resource in self._spec.resource_writes:
                if resource in self._resource_values:
                    self._staged_resources[resource] = self._resource_values[resource]
            self._resources.replace_many(
                tuple(
                    (resource, self._staged_resources[resource])
                    for resource in self._spec.resource_writes
                    if resource in self._staged_resources
                )
            )
        finally:
            self._resource_values.clear()
            self._staged_resources.clear()
            self._active = False

    def _track_rows(self, rows: _AbortableRows) -> None:
        self._rows.append(rows)

    def _require_active(self, *, operation: str) -> None:
        if not self._active:
            raise self._access_error(
                "system context is no longer active",
                operation=operation,
                target="system.context",
                requested="use",
            )

    def _require_component_access(
        self,
        component_types: Iterable[object],
        *,
        write: bool,
        operation: str,
    ) -> None:
        self._require_active(operation=operation)
        allowed = self._component_writes if write else self._component_reads
        for component_type in component_types:
            candidate: object = component_type
            if not isinstance(candidate, type) or candidate not in allowed:
                raise self._access_error(
                    "system component access exceeds its declaration",
                    operation=operation,
                    target=_type_name(candidate),
                    requested="write" if write else "read",
                )

    def _require_resource_access(
        self,
        spec: object,
        *,
        write: bool,
        operation: str,
    ) -> None:
        self._require_active(operation=operation)
        allowed = self._resource_writes if write else self._resource_reads
        if not isinstance(spec, ResourceSpec) or spec not in allowed:
            target = spec.name if isinstance(spec, ResourceSpec) else type(spec).__name__
            raise self._access_error(
                "system resource access exceeds its declaration",
                operation=operation,
                target=target,
                requested="write" if write else "read",
            )

    def _access_error(
        self,
        message: str,
        *,
        operation: str,
        target: str,
        requested: str,
    ) -> SystemAccessError:
        return SystemAccessError(
            message,
            code="application.system_access_denied",
            subsystem="application",
            phase=self._phase.value,
            details={
                "tick": self._tick,
                "system": self._spec.name,
                "operation": operation,
                "target": target,
                "requested": requested,
            },
        )


class FixedStepApplication:
    """Single-owner fixed-step world runner with explicit render lifecycle."""

    __slots__ = (
        "_accumulator_units",
        "_backend",
        "_clock",
        "_config",
        "_descriptor",
        "_frames",
        "_input_source",
        "_last_sample_ns",
        "_mode",
        "_owner_thread",
        "_resources",
        "_schedule",
        "_start_ns",
        "_state",
        "_total_ticks",
        "_world",
    )

    def __init__(
        self,
        config: ApplicationConfig,
        backend: RenderBackend,
        world: WorldStore,
        resources: ResourceStore,
        schedule: Schedule,
        input_source: InputSource,
        *,
        clock: Clock | None = None,
        descriptor: RenderDescriptor | None = None,
    ) -> None:
        self._config = config
        self._backend = backend
        self._world = world
        self._resources = resources
        self._schedule = schedule
        self._input_source = input_source
        self._clock = MonotonicClock() if clock is None else clock
        self._descriptor = (
            RenderDescriptor(label="fixed_step_application") if descriptor is None else descriptor
        )
        self._owner_thread = get_ident()
        self._state = LifecycleState.CREATED
        self._start_ns = 0
        self._last_sample_ns = 0
        self._accumulator_units = 0
        self._total_ticks = 0
        self._frames = 0
        self._mode: str | None = None

    @property
    def state(self) -> LifecycleState:
        return self._state

    @property
    def config(self) -> ApplicationConfig:
        return self._config

    @property
    def total_ticks(self) -> int:
        return self._total_ticks

    @property
    def frames(self) -> int:
        return self._frames

    @property
    def backlog_ticks(self) -> int:
        return self._accumulator_units // _TICK_UNITS

    def initialize(self) -> None:
        """Validate composition, initialize rendering, and anchor monotonic time."""

        self._assert_owner_thread()
        self._require_state("initialize", LifecycleState.CREATED)
        self._state = LifecycleState.INITIALIZING
        try:
            self._validate_composition()
            self._backend.initialize(self._descriptor)
            start_ns = self._sample_clock(phase="initialize")
        except BaseException as error:
            self._state = LifecycleState.FAILED
            cleanup_error = self._cleanup_failed_initialization()
            if not isinstance(error, Exception):
                if cleanup_error is not None:
                    error.add_note(
                        "fixed-step application initialization cleanup also failed: "
                        f"{cleanup_error}"
                    )
                raise
            details: dict[str, str | int | float | bool | None] = {
                "cause_type": type(error).__name__
            }
            if cleanup_error is not None:
                details["cleanup_error_type"] = cleanup_error
            raise ApplicationError(
                "fixed-step application initialization failed",
                code="application.initialization_failed",
                subsystem="application",
                phase="initialize",
                details=details,
            ) from error
        self._start_ns = start_ns
        self._last_sample_ns = start_ns
        self._state = LifecycleState.READY

    def pump(self) -> FrameSummary:
        """Advance due ticks up to the catch-up limit, then render one frame."""

        self._assert_owner_thread()
        self._require_state("pump", LifecycleState.READY, LifecycleState.RUNNING)
        self._require_mode("pump")
        self._state = LifecycleState.RUNNING
        try:
            sampled_ns = self._sample_clock(phase="pump")
            if sampled_ns < self._last_sample_ns:
                raise ApplicationError(
                    "application clock moved backward",
                    code="application.backward_clock",
                    subsystem="application",
                    phase="pump",
                    details={
                        "previous_ns": self._last_sample_ns,
                        "sampled_ns": sampled_ns,
                    },
                )
            elapsed_ns = sampled_ns - self._last_sample_ns
            self._last_sample_ns = sampled_ns
            self._accumulator_units += elapsed_ns * self._config.fixed_hz
            due = self.backlog_ticks
            count = min(due, self._config.catch_up_limit)
            for _ in range(count):
                self._execute_tick()
                self._accumulator_units -= _TICK_UNITS
            self._render()
        except BaseException:
            self._state = LifecycleState.STOPPED
            raise

        remainder = self._accumulator_units % _TICK_UNITS
        alpha = 1.0 if self.backlog_ticks else remainder / _TICK_UNITS
        return FrameSummary(
            frame=self._frames,
            ticks_executed=count,
            total_ticks=self._total_ticks,
            backlog_ticks=self.backlog_ticks,
            interpolation_alpha=alpha,
            sampled_ns=sampled_ns,
            renderer=self._backend.name,
        )

    def run_ticks(self, count: int) -> ApplicationRunSummary:
        """Run exactly ``count`` absolute-deadline ticks and stop orderly."""

        self._assert_owner_thread()
        self._require_state("run_ticks", LifecycleState.READY)
        _require_non_negative_count(count, field="count", phase="run_ticks")
        self._require_mode("run_ticks")
        self._state = LifecycleState.RUNNING
        starting_tick = self._total_ticks
        try:
            for _ in range(count):
                deadline = (
                    self._start_ns
                    + ((self._total_ticks + 1) * _TICK_UNITS) // self._config.fixed_hz
                )
                current = self._sample_clock(phase="run_ticks")
                if current < self._last_sample_ns:
                    raise ApplicationError(
                        "application clock moved backward",
                        code="application.backward_clock",
                        subsystem="application",
                        phase="run_ticks",
                        details={
                            "previous_ns": self._last_sample_ns,
                            "sampled_ns": current,
                        },
                    )
                if current < deadline:
                    self._wait_until(deadline, phase="run_ticks")
                sampled = self._sample_clock(phase="run_ticks")
                if sampled < max(current, deadline):
                    raise ApplicationError(
                        "application clock did not reach the tick deadline",
                        code="application.invalid_clock",
                        subsystem="application",
                        phase="run_ticks",
                        details={"deadline_ns": deadline, "sampled_ns": sampled},
                    )
                self._last_sample_ns = sampled
                self._execute_tick()
                self._render()
        except BaseException:
            self._state = LifecycleState.STOPPED
            raise
        self.shutdown()
        return ApplicationRunSummary(
            ticks=self._total_ticks - starting_tick,
            frames=self._frames,
            start_ns=self._start_ns,
            end_ns=self._sample_clock(phase="run_ticks"),
            fixed_hz=self._config.fixed_hz,
            renderer=self._backend.name,
        )

    def shutdown(self) -> None:
        """Stop a ready or running application without closing rendering."""

        self._assert_owner_thread()
        self._require_state("shutdown", LifecycleState.READY, LifecycleState.RUNNING)
        self._state = LifecycleState.STOPPED

    def close(self) -> None:
        """Close the owned render backend exactly once."""

        self._assert_owner_thread()
        if self._state is LifecycleState.CLOSED:
            return
        if self._state in (LifecycleState.READY, LifecycleState.RUNNING):
            self._state = LifecycleState.STOPPED
        try:
            self._backend.close()
        except Exception as error:
            raise ApplicationError(
                "fixed-step application close failed",
                code="application.close_failed",
                subsystem="application",
                phase="close",
                details={"cause_type": type(error).__name__},
            ) from error
        finally:
            self._state = LifecycleState.CLOSED

    def __enter__(self) -> FixedStepApplication:
        self.initialize()
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        del exception_type, traceback
        try:
            self.close()
        except Exception as cleanup_error:
            if exception is None:
                raise
            exception.add_note(
                f"fixed-step application cleanup also failed: {type(cleanup_error).__name__}"
            )
        return False

    def _execute_tick(self) -> None:
        tick = self._total_ticks
        try:
            snapshot = self._input_source.snapshot_for_tick(tick)
        except Exception as error:
            raise InputFrameError(
                "input source failed for simulation tick",
                code="application.input_failed",
                subsystem="application",
                phase="input",
                details={"tick": tick, "cause_type": type(error).__name__},
            ) from error
        if type(snapshot) is not InputSnapshot:
            raise InputFrameError(
                "input source returned an invalid snapshot type",
                code="application.input_mismatch",
                subsystem="application",
                phase="input",
                details={
                    "tick": tick,
                    "actual_type": type(snapshot).__name__,
                    "snapshot_tick": None,
                },
            )
        if snapshot.tick != tick:
            raise InputFrameError(
                "input source returned a mismatched snapshot",
                code="application.input_mismatch",
                subsystem="application",
                phase="input",
                details={
                    "tick": tick,
                    "actual_type": type(snapshot).__name__,
                    "snapshot_tick": snapshot.tick,
                },
            )
        try:
            if self._resources.contains(INPUT_SNAPSHOT_RESOURCE):
                self._resources.replace(INPUT_SNAPSHOT_RESOURCE, snapshot)
            else:
                self._resources.insert(INPUT_SNAPSHOT_RESOURCE, snapshot)
        except Exception as error:
            raise InputFrameError(
                "input snapshot could not be published",
                code="application.input_publish_failed",
                subsystem="application",
                phase="input",
                details={"tick": tick, "cause_type": type(error).__name__},
            ) from error

        commands = self._world.commands()
        command_ranges: list[tuple[int, int, str]] = []
        try:
            for phase in (SystemPhase.PRE_SIMULATE, SystemPhase.SIMULATE):
                for spec in self._schedule.systems_for_phase(phase):
                    before = len(commands)
                    self._invoke_system(tick, phase, spec, commands)
                    after = len(commands)
                    if after > before:
                        command_ranges.append((before, after, spec.name))
            try:
                self._world.flush(commands)
            except Exception as error:
                details = dict(error.details) if isinstance(error, LudoWeaveError) else {}
                operation_index = details.get("operation_index")
                attributed = "unknown"
                if type(operation_index) is int:
                    for start, end, system_name in command_ranges:
                        if start <= operation_index < end:
                            attributed = system_name
                            break
                commands.clear()
                raise ApplicationError(
                    "deferred structural command flush failed",
                    code="application.flush_failed",
                    subsystem="application",
                    phase="flush",
                    details={
                        "tick": tick,
                        "system": attributed,
                        "cause_type": type(error).__name__,
                        "cause_code": error.code if isinstance(error, LudoWeaveError) else None,
                        "operation_index": operation_index
                        if type(operation_index) is int
                        else None,
                        "operation_kind": details.get("operation_kind")
                        if type(details.get("operation_kind")) is str
                        else None,
                    },
                ) from error
            for spec in self._schedule.systems_for_phase(SystemPhase.POST_SIMULATE):
                self._invoke_system(tick, SystemPhase.POST_SIMULATE, spec, commands)
        except BaseException:
            commands.clear()
            raise
        self._total_ticks += 1

    def _invoke_system(
        self,
        tick: int,
        phase: SystemPhase,
        spec: SystemSpec,
        commands: Commands,
    ) -> None:
        context = _InvocationContext(
            tick=tick,
            phase=phase,
            spec=spec,
            world=self._world,
            resources=self._resources,
            commands=commands,
        )
        try:
            result = spec.function(cast(SystemContext, context), 1.0 / self._config.fixed_hz)
            if result is not None:
                raise SystemAccessError(
                    "system function must return None",
                    code="application.invalid_system_return",
                    subsystem="application",
                    phase=phase.value,
                    details={
                        "tick": tick,
                        "system": spec.name,
                        "actual_type": type(result).__name__,
                    },
                )
            context.finish(failed=False)
        except BaseException as error:
            try:
                context.finish(failed=True)
            except Exception as cleanup_error:
                error.add_note(
                    f"system context cleanup also failed: {type(cleanup_error).__name__}"
                )
            if not isinstance(error, Exception):
                raise
            raise SystemExecutionError(
                "planned system invocation failed",
                code="application.system_failed",
                subsystem="application",
                phase=phase.value,
                details={
                    "tick": tick,
                    "system": spec.name,
                    "cause_type": type(error).__name__,
                },
            ) from error

    def _render(self) -> None:
        tick = max(self._total_ticks - 1, 0)
        try:
            self._backend.render(tick=tick)
        except Exception as error:
            raise ApplicationError(
                "application render failed after committed ticks",
                code="application.render_failed",
                subsystem="application",
                phase="render",
                details={
                    "ticks_completed": self._total_ticks,
                    "cause_type": type(error).__name__,
                },
            ) from error
        self._frames += 1

    def _sample_clock(self, *, phase: str) -> int:
        try:
            value = self._clock.now_ns()
        except Exception as error:
            raise ApplicationError(
                "application clock sampling failed",
                code="application.clock_failed",
                subsystem="application",
                phase=phase,
                details={"cause_type": type(error).__name__},
            ) from error
        return _require_clock_sample(value, phase=phase)

    def _wait_until(self, deadline_ns: int, *, phase: str) -> None:
        try:
            self._clock.wait_until_ns(deadline_ns)
        except Exception as error:
            raise ApplicationError(
                "application clock deadline wait failed",
                code="application.clock_failed",
                subsystem="application",
                phase=phase,
                details={
                    "cause_type": type(error).__name__,
                    "deadline_ns": deadline_ns,
                },
            ) from error

    def _validate_composition(self) -> None:
        if not self._resources.registry.contains(INPUT_SNAPSHOT_RESOURCE):
            raise ApplicationError(
                "resource registry must include the engine input snapshot key",
                code="application.missing_input_resource",
                subsystem="application",
                phase="initialize",
            )
        try:
            canonical_schedule = Scheduler(
                self._world.registry,
                self._resources.registry,
            ).build(tuple(spec.function for spec in self._schedule.systems))
        except LudoWeaveError as error:
            raise ApplicationError(
                "application schedule does not satisfy deterministic planning rules",
                code="application.invalid_schedule",
                subsystem="application",
                phase="initialize",
                details={"cause_code": error.code},
            ) from error
        if self._schedule != canonical_schedule:
            raise ApplicationError(
                "application schedule differs from its canonical deterministic plan",
                code="application.invalid_schedule",
                subsystem="application",
                phase="initialize",
                details={
                    "systems": len(self._schedule.systems),
                    "explicit_edges": len(self._schedule.explicit_edges),
                    "conflicts": len(self._schedule.conflicts),
                },
            )
        seen_names: set[str] = set()
        previous_phase = -1
        phase_index = {phase: index for index, phase in enumerate(SystemPhase)}
        for spec in self._schedule.systems:
            if spec.name in seen_names:
                raise ApplicationError(
                    "application schedule repeats a system",
                    code="application.invalid_schedule",
                    subsystem="application",
                    phase="initialize",
                    details={"system": spec.name},
                )
            seen_names.add(spec.name)
            current_phase = phase_index[spec.phase]
            if current_phase < previous_phase:
                raise ApplicationError(
                    "application schedule phases are out of order",
                    code="application.invalid_schedule",
                    subsystem="application",
                    phase="initialize",
                    details={"system": spec.name},
                )
            previous_phase = current_phase
            if not spec.deterministic or spec.execution_class is not ExecutionClass.PYTHON:
                raise ApplicationError(
                    "application requires deterministic Python systems",
                    code="application.invalid_schedule",
                    subsystem="application",
                    phase="initialize",
                    details={"system": spec.name},
                )
            for component_type in (*spec.component_reads, *spec.component_writes):
                schema = self._world.registry.schema_for_type(component_type)
                if schema.determinism is DeterminismTier.D0:
                    raise ApplicationError(
                        "application schedule accesses a D0 component",
                        code="application.invalid_schedule",
                        subsystem="application",
                        phase="initialize",
                        details={"system": spec.name, "component": schema.qualified_name},
                    )
            for resource in (*spec.resource_reads, *spec.resource_writes):
                if not self._resources.registry.contains(resource):
                    raise ApplicationError(
                        "application schedule uses a foreign resource key",
                        code="application.invalid_schedule",
                        subsystem="application",
                        phase="initialize",
                        details={"system": spec.name, "resource": resource.name},
                    )
                if not resource.deterministic:
                    raise ApplicationError(
                        "application schedule accesses a nondeterministic resource",
                        code="application.invalid_schedule",
                        subsystem="application",
                        phase="initialize",
                        details={"system": spec.name, "resource": resource.name},
                    )
                if resource is INPUT_SNAPSHOT_RESOURCE and resource in spec.resource_writes:
                    raise ApplicationError(
                        "systems cannot write the application-owned input snapshot",
                        code="application.invalid_schedule",
                        subsystem="application",
                        phase="initialize",
                        details={"system": spec.name, "resource": resource.name},
                    )
                if resource is not INPUT_SNAPSHOT_RESOURCE and not self._resources.contains(
                    resource
                ):
                    raise ApplicationError(
                        "application schedule requires a missing resource value",
                        code="application.missing_resource",
                        subsystem="application",
                        phase="initialize",
                        details={"system": spec.name, "resource": resource.name},
                    )

    def _require_mode(self, mode: str) -> None:
        if self._mode is None:
            self._mode = mode
        elif self._mode != mode:
            raise ApplicationError(
                "pump and exact-tick execution modes cannot be mixed",
                code="application.mixed_run_mode",
                subsystem="application",
                phase=mode,
                details={"active_mode": self._mode},
            )

    def _assert_owner_thread(self) -> None:
        current = get_ident()
        if current != self._owner_thread:
            raise ApplicationError(
                "application lifecycle methods must run on the creating thread",
                code="application.wrong_thread",
                subsystem="application",
                phase="threading",
                details={"operation_thread": current, "owner_thread": self._owner_thread},
            )

    def _require_state(self, operation: str, *allowed: LifecycleState) -> None:
        if self._state not in allowed:
            raise ApplicationError(
                f"cannot {operation} application from {self._state.value} state",
                code="application.invalid_transition",
                subsystem="application",
                phase=operation,
                details={
                    "operation": operation,
                    "state": self._state.value,
                    "allowed": ",".join(state.value for state in allowed),
                },
            )

    def _cleanup_failed_initialization(self) -> str | None:
        cleanup_error: str | None = None
        try:
            self._backend.close()
        except Exception as error:
            cleanup_error = type(error).__name__
        finally:
            self._state = LifecycleState.CLOSED
        return cleanup_error


def _require_positive_config(value: object, *, field: str) -> int:
    if type(value) is not int or value <= 0:
        raise ConfigurationError(
            f"{field} must be a positive integer",
            code="config.invalid_application_value",
            subsystem="application",
            phase="configuration",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _require_non_negative_count(value: object, *, field: str, phase: str) -> int:
    if type(value) is not int or value < 0:
        raise ConfigurationError(
            f"{field} must be a non-negative integer",
            code="config.invalid_application_value",
            subsystem="application",
            phase=phase,
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _require_clock_sample(value: object, *, phase: str) -> int:
    if type(value) is not int or value < 0:
        raise ApplicationError(
            "application clock returned an invalid sample",
            code="application.invalid_clock",
            subsystem="application",
            phase=phase,
            details={"actual_type": type(value).__name__},
        )
    return value


def _type_name(component_type: object) -> str:
    if isinstance(component_type, type):
        return f"{component_type.__module__}.{component_type.__qualname__}"
    return type(component_type).__name__
