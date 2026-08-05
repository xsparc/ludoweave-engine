"""Run a bounded, isolated admission probe for the optional Box2D candidate.

The script is deliberately outside the LudoWeave package. Install the pinned
candidate into an ephemeral environment when running it; it is not a project
dependency and this probe is not a supported runtime adapter.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
from collections.abc import Iterable, Sequence
from importlib import import_module
from importlib.metadata import Distribution, PackageNotFoundError, distribution
from importlib.util import find_spec
from pathlib import Path
from typing import Protocol, Self, cast

_SCHEMA = "ludoweave.evaluation.box2d/1"
_DISTRIBUTION = "box2d-python"
_FIXED_STEP = 1.0 / 60.0
_SUBSTEPS = 4
_MAX_ITERATIONS = 100
_MAX_STEPS = 10_000
_MAX_TOTAL_STEPS = 100_000


class _Body(Protocol):
    @property
    def position(self) -> object: ...


class _BodyBuilder(Protocol):
    def dynamic(self) -> Self: ...

    def static(self) -> Self: ...

    def position(self, x: float, y: float) -> Self: ...

    def box(self, half_width: float, half_height: float) -> Self: ...

    def build(self) -> _Body: ...


class _World(Protocol):
    def new_body(self) -> _BodyBuilder: ...

    def step(self, time_step: float, substep_count: int) -> None: ...

    def destroy(self) -> None: ...


class _WorldFactory(Protocol):
    def __call__(self, *, gravity: tuple[float, float], threads: int) -> _World: ...


class _Box2DModule(Protocol):
    World: _WorldFactory


class _CandidateOwnershipError(RuntimeError):
    """The imported module cannot be attributed to the named distribution."""


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--iterations",
        type=int,
        default=25,
        help="world create/step/destroy repetitions (2-100; default: 25)",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=120,
        help="fixed steps per repetition (1-10000; default: 120)",
    )
    args = parser.parse_args(argv)
    iterations = _integer_argument(args, "iterations")
    steps = _integer_argument(args, "steps")
    if not 2 <= iterations <= _MAX_ITERATIONS:
        parser.error(f"iterations must be between 2 and {_MAX_ITERATIONS}")
    if not 1 <= steps <= _MAX_STEPS:
        parser.error(f"steps must be between 1 and {_MAX_STEPS}")
    if iterations * steps > _MAX_TOTAL_STEPS:
        parser.error(f"iterations * steps must not exceed {_MAX_TOTAL_STEPS}")

    try:
        candidate_distribution = distribution(_DISTRIBUTION)
    except PackageNotFoundError:
        _emit(_document(status="unavailable", iterations=iterations, steps=steps))
        return 2
    except Exception as error:
        _emit(
            _document(
                status="failed",
                iterations=iterations,
                steps=steps,
                error_type=type(error).__name__,
            )
        )
        return 1

    candidate_version: str | None = None
    try:
        candidate_version = candidate_distribution.version
        candidate = _load_owned_candidate(candidate_distribution)
        traces = tuple(_run_scenario(candidate.World, steps=steps) for _ in range(iterations))
        reference = traces[0]
        repeat_equal = all(trace == reference for trace in traces[1:])
        digest = hashlib.sha256(_trace_bytes(reference)).hexdigest()
        document = _document(
            status="ok" if repeat_equal else "mismatch",
            iterations=iterations,
            steps=steps,
            candidate_version=candidate_version,
            repeat_equal=repeat_equal,
            trace_sha256=digest,
        )
    except Exception as error:
        document = _document(
            status="failed",
            iterations=iterations,
            steps=steps,
            candidate_version=candidate_version,
            error_type=type(error).__name__,
        )
        _emit(document)
        return 1

    _emit(document)
    return 0 if repeat_equal else 1


def _load_owned_candidate(candidate_distribution: Distribution) -> _Box2DModule:
    spec = find_spec("box2d")
    files = candidate_distribution.files
    if spec is None or spec.origin is None or files is None:
        raise _CandidateOwnershipError("candidate module ownership is not verifiable")
    origin = Path(spec.origin).resolve()
    owned_paths = {
        Path(str(candidate_distribution.locate_file(package_path))).resolve()
        for package_path in files
    }
    if origin not in owned_paths:
        raise _CandidateOwnershipError("candidate module is not owned by its distribution")
    candidate_module = import_module("box2d")
    loaded_file = getattr(candidate_module, "__file__", None)
    if not isinstance(loaded_file, str) or Path(loaded_file).resolve() != origin:
        raise _CandidateOwnershipError("loaded candidate identity changed during import")
    return cast(_Box2DModule, candidate_module)


def _run_scenario(factory: _WorldFactory, *, steps: int) -> tuple[tuple[str, str], ...]:
    world = factory(gravity=(0.0, -10.0), threads=1)
    try:
        world.new_body().static().position(0.0, -10.0).box(50.0, 10.0).build()
        body = world.new_body().dynamic().position(0.0, 5.0).box(0.5, 0.5).build()
        initial_position = _position_hex(body)
        trace: list[tuple[str, str]] = []
        for _ in range(steps):
            world.step(_FIXED_STEP, _SUBSTEPS)
            trace.append(_position_hex(body))
        if all(position == initial_position for position in trace):
            raise RuntimeError("candidate step produced no observable movement")
        return tuple(trace)
    finally:
        world.destroy()
        world.destroy()


def _position_hex(body: _Body) -> tuple[str, str]:
    values = tuple(cast(Iterable[object], body.position))
    if len(values) != 2:
        raise ValueError("candidate body position must contain exactly two values")
    return _finite_float(values[0]).hex(), _finite_float(values[1]).hex()


def _finite_float(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("candidate body position values must be numeric")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("candidate body position values must be finite")
    return number


def _trace_bytes(trace: tuple[tuple[str, str], ...]) -> bytes:
    return "".join(f"{x},{y}\n" for x, y in trace).encode("ascii")


def _document(
    *,
    status: str,
    iterations: int,
    steps: int,
    candidate_version: str | None = None,
    repeat_equal: bool | None = None,
    trace_sha256: str | None = None,
    error_type: str | None = None,
) -> dict[str, object]:
    candidate: dict[str, object] = {"distribution": _DISTRIBUTION}
    if candidate_version is not None:
        candidate["version"] = candidate_version
    probe: dict[str, object] = {
        "fixed_step_hex": _FIXED_STEP.hex(),
        "iterations": iterations,
        "steps": steps,
        "substeps": _SUBSTEPS,
        "threads": 1,
    }
    if repeat_equal is not None:
        probe["repeat_equal"] = repeat_equal
    if trace_sha256 is not None:
        probe["trace_sha256"] = trace_sha256
    if error_type is not None:
        probe["error_type"] = error_type
    return {
        "candidate": candidate,
        "environment": {
            "implementation": platform.python_implementation(),
            "machine": platform.machine(),
            "platform": sys.platform,
            "python": platform.python_version(),
        },
        "probe": probe,
        "schema": _SCHEMA,
        "status": status,
    }


def _emit(document: dict[str, object]) -> None:
    print(json.dumps(document, ensure_ascii=True, separators=(",", ":"), sort_keys=True))


def _integer_argument(namespace: argparse.Namespace, name: str) -> int:
    value = getattr(namespace, name)
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
