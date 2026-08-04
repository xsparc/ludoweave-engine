"""Record the correctness-first M1 pure-Python performance baseline."""

import argparse
import json
import platform
import random
import subprocess
import sys
import sysconfig
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from time import perf_counter_ns
from types import FunctionType
from typing import Protocol, cast
from uuid import UUID

from ludoweave import __version__
from ludoweave.app import (
    INPUT_SNAPSHOT_RESOURCE,
    ApplicationConfig,
    FixedStepApplication,
    NullInputSource,
)
from ludoweave.core.clock import VirtualClock
from ludoweave.ecs import (
    ComponentRegistry,
    ResourceRegistry,
    ResourceStore,
    Scheduler,
    SystemContext,
    SystemFunction,
    SystemPhase,
    World,
    component,
    system,
)
from ludoweave.render import NullRenderBackend

_SCHEMA = "ludoweave.benchmark.m1/1"
_WORKLOAD_VERSION = 1
_NANOSECONDS = 1_000_000_000
_ENTITY_COUNT = 10_000
_COMMAND_COUNT = 1_000
_SYSTEM_COUNT = 100
_WARMUPS = 3
_TOOL_PACKAGES = (
    "hatchling",
    "hypothesis",
    "mkdocs-material",
    "pyright",
    "pytest",
    "ruff",
)


@component(type_id=UUID("fb000000-0000-0000-0000-000000000001"))
@dataclass(slots=True)
class Position:
    """Simple benchmark position."""

    x: float = 0.0
    y: float = 0.0


@component(type_id=UUID("fb000000-0000-0000-0000-000000000002"))
@dataclass(slots=True)
class Velocity:
    """Simple benchmark velocity."""

    x: float = 1.0
    y: float = -1.0


_EMPTY_COMPONENTS = ComponentRegistry()
_SIMULATION_COMPONENTS = ComponentRegistry((Position, Velocity))
_INPUT_RESOURCES = ResourceRegistry((INPUT_SNAPSHOT_RESOURCE,))


@system(
    name="benchmark.integrate",
    phase=SystemPhase.SIMULATE,
    component_reads=(Velocity,),
    component_writes=(Position,),
)
def _integrate(context: SystemContext, delta: float) -> None:
    with context.query(Position, Velocity).writes(Position).rows() as rows:
        for _entity_id, position, velocity in rows:
            position.x += velocity.x * delta
            position.y += velocity.y * delta


def _noop_system(context: SystemContext, delta: float) -> None:
    del context, delta


class _Operation(Protocol):
    def __call__(self) -> object: ...


class _OperationFactory(Protocol):
    def __call__(self) -> tuple[_Operation, Callable[[], None]]: ...


def _measure(
    factory: _OperationFactory,
    *,
    warmups: int,
    samples: int,
) -> tuple[int, ...]:
    durations: list[int] = []
    for index in range(warmups + samples):
        operation, cleanup = factory()
        try:
            started = perf_counter_ns()
            operation()
            elapsed = perf_counter_ns() - started
        finally:
            cleanup()
        if index >= warmups:
            durations.append(elapsed)
    return tuple(durations)


def _reusable(operation: _Operation) -> _OperationFactory:
    def factory() -> tuple[_Operation, Callable[[], None]]:
        return operation, _do_nothing

    return factory


def _do_nothing() -> None:
    return None


def _entity_lifecycle_factory() -> tuple[_Operation, Callable[[], None]]:
    world = World(_EMPTY_COMPONENTS)

    def operation() -> int:
        initial = tuple(world.spawn() for _ in range(_ENTITY_COUNT))
        for entity_id in initial:
            world.destroy(entity_id)
        reused = tuple(world.spawn() for _ in range(_ENTITY_COUNT))
        if reused[0].generation != 1 or len(world.entities()) != _ENTITY_COUNT:
            raise RuntimeError("entity lifecycle workload produced an invalid result")
        return reused[-1].index

    return operation, _do_nothing


def _query_world() -> World:
    world = World(_SIMULATION_COMPONENTS)
    for index in range(_ENTITY_COUNT):
        scalar = float(index)
        world.spawn(Position(scalar, -scalar), Velocity())
    return world


def _read_query_operation(world: World) -> Callable[[], float]:
    def operation() -> float:
        total = 0.0
        for _entity_id, position, velocity in world.query(Position, Velocity).rows():
            total += position.x + velocity.x
        if total <= 0.0:
            raise RuntimeError("read-query workload produced an invalid checksum")
        return total

    return operation


def _write_query_operation(world: World) -> Callable[[], int]:
    def operation() -> int:
        with world.query(Position, Velocity).writes(Position).rows() as rows:
            for _entity_id, position, velocity in rows:
                position.x += velocity.x
                position.y += velocity.y
        return world.epoch

    return operation


def _scheduler_definitions(seed: int) -> tuple[SystemFunction, ...]:
    randomizer = random.Random(seed)
    names = tuple(f"benchmark.system.{index:03d}" for index in range(_SYSTEM_COUNT))
    definitions: list[SystemFunction] = []
    for index, name in enumerate(names):
        successors: set[str] = set()
        if index + 1 < len(names):
            successors.add(names[index + 1])
        for candidate in range(index + 2, min(len(names), index + 8)):
            if randomizer.random() < 0.25:
                successors.add(names[candidate])
        function_name = f"_benchmark_system_{index:03d}"
        function = FunctionType(_noop_system.__code__, globals(), function_name)
        function.__qualname__ = function_name
        function.__module__ = __name__
        globals()[function_name] = function
        definitions.append(
            cast(
                SystemFunction,
                system(
                    name=name,
                    phase=SystemPhase.SIMULATE,
                    before=tuple(sorted(successors)),
                )(function),
            )
        )
    return tuple(definitions)


def _command_flush_factory() -> tuple[_Operation, Callable[[], None]]:
    world = World(_SIMULATION_COMPONENTS)

    def operation() -> int:
        commands = world.commands()
        for index in range(_COMMAND_COUNT):
            scalar = float(index)
            commands.spawn(Position(scalar, scalar), Velocity())
        return world.flush(commands).command_count

    return operation, _do_nothing


def _empty_application() -> FixedStepApplication:
    world = World(_EMPTY_COMPONENTS)
    schedule = Scheduler(_EMPTY_COMPONENTS, _INPUT_RESOURCES).build(())
    return FixedStepApplication(
        ApplicationConfig(fixed_hz=60, catch_up_limit=4),
        NullRenderBackend(),
        world,
        ResourceStore(_INPUT_RESOURCES),
        schedule,
        NullInputSource(),
        clock=VirtualClock(),
    )


def _fixed_step_factory() -> tuple[_Operation, Callable[[], None]]:
    application = _empty_application()
    application.initialize()

    def operation() -> int:
        return application.run_ticks(3_600).ticks

    return operation, application.close


def _simulation_application(world: World) -> tuple[FixedStepApplication, VirtualClock]:
    schedule = Scheduler(_SIMULATION_COMPONENTS, _INPUT_RESOURCES).build((_integrate,))
    clock = VirtualClock()
    application = FixedStepApplication(
        ApplicationConfig(fixed_hz=60, catch_up_limit=1),
        NullRenderBackend(),
        world,
        ResourceStore(_INPUT_RESOURCES),
        schedule,
        NullInputSource(),
        clock=clock,
    )
    application.initialize()
    return application, clock


def _simulation_operation(
    application: FixedStepApplication,
    clock: VirtualClock,
) -> Callable[[], int]:
    def operation() -> int:
        clock.advance_ns(16_666_667)
        summary = application.pump()
        if summary.ticks_executed != 1:
            raise RuntimeError("simulation workload did not execute exactly one tick")
        return summary.total_ticks

    return operation


def _percentile(values: Sequence[int], percentile: int) -> int:
    ordered = sorted(values)
    index = max(0, ((len(ordered) * percentile + 99) // 100) - 1)
    return ordered[index]


def _result(
    name: str,
    durations: Sequence[int],
    *,
    samples: int,
    parameters: Mapping[str, int | float | str],
    target: Mapping[str, int | float | str | bool] | None = None,
) -> dict[str, object]:
    return {
        "name": name,
        "workload_version": _WORKLOAD_VERSION,
        "warmups": _WARMUPS,
        "samples": samples,
        "parameters": dict(parameters),
        "durations_ns": list(durations),
        "p50_ns": _percentile(durations, 50),
        "p95_ns": _percentile(durations, 95),
        "p99_ns": _percentile(durations, 99),
        "target": None if target is None else dict(target),
    }


def _git_metadata() -> dict[str, object]:
    commit = "unknown"
    dirty = True
    try:
        commit_result = subprocess.run(
            ("git", "rev-parse", "HEAD"),
            check=True,
            capture_output=True,
            text=True,
        )
        status_result = subprocess.run(
            ("git", "status", "--porcelain"),
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return {"commit": commit, "dirty": dirty}
    commit = commit_result.stdout.strip()
    dirty = bool(status_result.stdout.strip())
    return {"commit": commit, "dirty": dirty}


def _dependency_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for package in _TOOL_PACKAGES:
        try:
            versions[package] = version(package)
        except PackageNotFoundError:
            versions[package] = "not-installed"
    return versions


def _environment() -> dict[str, object]:
    free_threaded = sysconfig.get_config_var("Py_GIL_DISABLED") == 1
    gil_probe = cast(object, getattr(sys, "_is_gil_enabled", None))
    if callable(gil_probe):
        gil_result = gil_probe()
        gil_enabled = gil_result if type(gil_result) is bool else None
    else:
        gil_enabled = not free_threaded
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor() or "unknown",
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "python_build_mode": "debug" if hasattr(sys, "gettotalrefcount") else "release",
        "python_threading_build": "free-threaded" if free_threaded else "gil",
        "python_gil_enabled": gil_enabled,
        "ludoweave_version": __version__,
        "dependency_versions": _dependency_versions(),
    }


def run_benchmarks(*, samples: int, seed: int) -> dict[str, object]:
    read_world = _query_world()
    write_world = _query_world()
    scheduler = Scheduler(_EMPTY_COMPONENTS, ResourceRegistry())
    scheduler_definitions = _scheduler_definitions(seed)
    simulation_world = _query_world()
    simulation_application, simulation_clock = _simulation_application(simulation_world)
    try:
        entity_samples = _measure(
            _entity_lifecycle_factory,
            warmups=_WARMUPS,
            samples=samples,
        )
        read_samples = _measure(
            _reusable(_read_query_operation(read_world)),
            warmups=_WARMUPS,
            samples=samples,
        )
        write_samples = _measure(
            _reusable(_write_query_operation(write_world)),
            warmups=_WARMUPS,
            samples=samples,
        )
        scheduler_samples = _measure(
            _reusable(lambda: scheduler.build(scheduler_definitions)),
            warmups=_WARMUPS,
            samples=samples,
        )
        command_samples = _measure(
            _command_flush_factory,
            warmups=_WARMUPS,
            samples=samples,
        )
        fixed_step_samples = _measure(
            _fixed_step_factory,
            warmups=_WARMUPS,
            samples=samples,
        )
        simulation_samples = _measure(
            _reusable(_simulation_operation(simulation_application, simulation_clock)),
            warmups=_WARMUPS,
            samples=samples,
        )
    finally:
        simulation_application.close()

    if simulation_application.total_ticks != _WARMUPS + samples:
        raise RuntimeError("simulation benchmark tick count did not match its measurements")

    simulation_limit = 4_000_000
    fixed_step_limit = 12 * _NANOSECONDS
    workloads = (
        _result(
            "entity_lifecycle",
            entity_samples,
            samples=samples,
            parameters={"entity_count": _ENTITY_COUNT, "cycles": 2},
        ),
        _result(
            "read_query_10000",
            read_samples,
            samples=samples,
            parameters={"entity_count": _ENTITY_COUNT, "component_count": 2},
        ),
        _result(
            "write_query_10000",
            write_samples,
            samples=samples,
            parameters={"entity_count": _ENTITY_COUNT, "component_count": 2},
        ),
        _result(
            "scheduler_plan_generated_dag",
            scheduler_samples,
            samples=samples,
            parameters={"system_count": _SYSTEM_COUNT, "seed": seed},
        ),
        _result(
            "command_buffer_staged_flush",
            command_samples,
            samples=samples,
            parameters={"command_count": _COMMAND_COUNT, "component_count": 2},
        ),
        _result(
            "fixed_step_3600_ticks",
            fixed_step_samples,
            samples=samples,
            parameters={"tick_count": 3_600, "fixed_hz": 60, "simulated_seconds": 60},
            target={
                "name": "headless_5x_realtime",
                "metric": "p95_ns",
                "comparator": "<=",
                "limit_ns": fixed_step_limit,
                "observed": _percentile(fixed_step_samples, 95) <= fixed_step_limit,
            },
        ),
        _result(
            "simulation_tick_10000",
            simulation_samples,
            samples=samples,
            parameters={"entity_count": _ENTITY_COUNT, "system_count": 1, "fixed_hz": 60},
            target={
                "name": "simulation_tick_p95_below_4ms",
                "metric": "p95_ns",
                "comparator": "<",
                "limit_ns": simulation_limit,
                "observed": _percentile(simulation_samples, 95) < simulation_limit,
            },
        ),
    )
    return {
        "schema": _SCHEMA,
        "seed": seed,
        "samples": samples,
        "warmups": _WARMUPS,
        "timer": "time.perf_counter_ns",
        "environment": _environment(),
        "git": _git_metadata(),
        "workloads": workloads,
    }


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be positive")
    return parsed


def _non_negative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must be non-negative")
    return parsed


def main(arguments: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=_positive_int, default=30)
    parser.add_argument("--seed", type=_non_negative_int, default=1)
    parser.add_argument("--json-out", type=Path, required=True)
    options = parser.parse_args(arguments)
    result = run_benchmarks(samples=options.samples, seed=options.seed)
    output = cast(Path, options.json_out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, separators=(",", ":"), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
