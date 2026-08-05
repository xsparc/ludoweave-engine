"""Record sanitized cProfile evidence for post-alpha native-code decisions."""

from __future__ import annotations

import argparse
import cProfile
import json
import platform
import pstats
import re
import subprocess
import sys
import sysconfig
from collections.abc import Callable, Mapping, Sequence
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Protocol, cast

from benchmarks.benchmark_m1 import simulation_profile_fixture
from benchmarks.benchmark_m3 import (
    extraction_profile_operation,
    submission_profile_fixture,
)
from ludoweave import __version__

_SCHEMA = "ludoweave.profile.m7/1"
_ENTITY_COUNT = 10_000
_SPRITE_COUNT = 10_000
_HOTSPOT_LIMIT = 25
_DEPENDENCIES = ("glfw", "rendercanvas", "wgpu")
_ROOT = Path(__file__).resolve().parents[1]
_SOURCE_ROOT = _ROOT / "src"
_BENCHMARK_ROOT = _ROOT / "benchmarks"
_ADDRESS = re.compile(r"0x[0-9A-Fa-f]+")


class _PStatsView(Protocol):
    stats: Mapping[tuple[str, int, str], tuple[int, int, float, float, object]]
    total_tt: float
    prim_calls: int
    total_calls: int


def run_profiles(*, repeats: int, include_wgpu: bool) -> dict[str, object]:
    """Profile exact established workloads without treating profiler time as a benchmark."""

    if type(repeats) is not int or repeats <= 0:
        raise ValueError("profile repeats must be a positive integer")
    workloads: list[dict[str, object]] = []

    simulation, close_simulation = simulation_profile_fixture()
    try:
        simulation()
        workloads.append(
            _profile_operation(
                "simulation_tick_10000",
                simulation,
                repeats=repeats,
                parameters={"entity_count": _ENTITY_COUNT, "fixed_hz": 60, "systems": 1},
                expected=(_positive_int_result, "positive total tick count"),
            )
        )
    finally:
        close_simulation()

    extraction = extraction_profile_operation(_SPRITE_COUNT)
    extraction()
    workloads.append(
        _profile_operation(
            "extract_pack_10000",
            extraction,
            repeats=repeats,
            parameters={"visible_sprites": _SPRITE_COUNT, "packed_bytes": _SPRITE_COUNT * 64},
            expected=(_one_draw_10000, "one draw and 10,000 visible sprites"),
        )
    )

    graphics_capabilities: Mapping[str, object] | None = None
    if include_wgpu:
        submission, close_submission, graphics_capabilities = submission_profile_fixture(
            _SPRITE_COUNT, graphics=True
        )
        try:
            submission()
            workloads.append(
                _profile_operation(
                    "wgpu_submit_10000",
                    submission,
                    repeats=repeats,
                    parameters={"visible_sprites": _SPRITE_COUNT, "draw_calls": 1},
                    expected=(_one_draw_10000, "one draw and 10,000 submitted sprites"),
                )
            )
        finally:
            close_submission()

    return {
        "schema": _SCHEMA,
        "profiler": "cProfile",
        "sort": "cumulative_ns_desc",
        "repeats": repeats,
        "include_wgpu": include_wgpu,
        "environment": _environment(graphics_capabilities),
        "git": _git_metadata(),
        "workloads": workloads,
    }


def _profile_operation(
    name: str,
    operation: Callable[[], object],
    *,
    repeats: int,
    parameters: Mapping[str, int],
    expected: tuple[Callable[[object], bool], str],
) -> dict[str, object]:
    results: list[object] = []

    def repeated() -> None:
        for _ in range(repeats):
            results.append(operation())

    profiler = cProfile.Profile()
    profiler.runcall(repeated)
    predicate, description = expected
    if len(results) != repeats or not all(predicate(result) for result in results):
        raise RuntimeError(f"{name} violated its reference result: {description}")
    stats = pstats.Stats(profiler)
    stats_view = cast(_PStatsView, stats)
    raw_stats = stats_view.stats
    total_ns = max(1, round(stats_view.total_tt * 1_000_000_000))
    hotspots: list[dict[str, object]] = []
    for (filename, line, function), (
        primitive_calls,
        total_calls,
        self_s,
        cumulative_s,
        _callers,
    ) in raw_stats.items():
        module = _normalized_module(filename)
        if module is None or cumulative_s <= 0.0:
            continue
        self_ns = max(0, round(self_s * 1_000_000_000))
        cumulative_ns = max(0, round(cumulative_s * 1_000_000_000))
        hotspots.append(
            {
                "module": module,
                "line": line,
                "function": _normalized_function(function),
                "primitive_calls": primitive_calls,
                "total_calls": total_calls,
                "self_ns": self_ns,
                "cumulative_ns": cumulative_ns,
                "cumulative_ratio_ppm": round(cumulative_ns * 1_000_000 / total_ns),
            }
        )
    hotspots.sort(
        key=lambda item: (
            -cast(int, item["cumulative_ns"]),
            -cast(int, item["self_ns"]),
            cast(str, item["module"]),
            cast(int, item["line"]),
            cast(str, item["function"]),
        )
    )
    return {
        "name": name,
        "workload_version": 1,
        "parameters": dict(parameters),
        "profiled_repeats": repeats,
        "total_profiled_ns": total_ns,
        "primitive_calls": stats_view.prim_calls,
        "total_calls": stats_view.total_calls,
        "result_invariant": description,
        "hotspots": hotspots[:_HOTSPOT_LIMIT],
    }


def _normalized_module(filename: str) -> str | None:
    if filename.startswith("<"):
        return None
    if filename == "~":
        return "python.builtin"
    path = Path(filename).resolve()
    for root, prefix in ((_SOURCE_ROOT, ""), (_BENCHMARK_ROOT, "benchmarks")):
        try:
            relative = path.relative_to(root).with_suffix("")
        except ValueError:
            continue
        parts = relative.parts
        if parts and parts[-1] == "__init__":
            parts = parts[:-1]
        return ".".join((prefix, *parts)).strip(".")
    lowered = tuple(part.lower() for part in path.parts)
    if "site-packages" in lowered:
        index = lowered.index("site-packages") + 1
        package = lowered[index] if index < len(lowered) else "unknown"
        return f"provider.{package}.{path.stem}"
    return f"python.{path.stem}"


def _normalized_function(function: str) -> str:
    return _ADDRESS.sub("0xADDRESS", function)


def _positive_int_result(value: object) -> bool:
    return type(value) is int and value > 0


def _one_draw_10000(value: object) -> bool:
    return value == (1, _SPRITE_COUNT)


def _package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "not-installed"


def _environment(capabilities: Mapping[str, object] | None) -> dict[str, object]:
    free_threaded = sysconfig.get_config_var("Py_GIL_DISABLED") == 1
    gil_probe = cast(object, getattr(sys, "_is_gil_enabled", None))
    if callable(gil_probe):
        probe_result = gil_probe()
        gil_enabled = probe_result if type(probe_result) is bool else None
    else:
        gil_enabled = not free_threaded
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine() or "unknown",
        "processor": platform.processor() or "unknown",
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "python_build_mode": "debug" if sysconfig.get_config_var("Py_DEBUG") else "release",
        "python_threading_build": "free-threaded" if free_threaded else "gil",
        "python_gil_enabled": gil_enabled,
        "ludoweave_version": __version__,
        "dependency_versions": {name: _package_version(name) for name in _DEPENDENCIES},
        "render_capabilities": None if capabilities is None else dict(capabilities),
    }


def _git_metadata() -> dict[str, object]:
    try:
        commit = subprocess.run(
            ("git", "rev-parse", "HEAD"), check=True, capture_output=True, text=True
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ("git", "status", "--porcelain"), check=True, capture_output=True, text=True
            ).stdout
        )
    except (OSError, subprocess.CalledProcessError):
        return {"commit": "unknown", "dirty": True}
    return {"commit": commit, "dirty": dirty}


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be positive")
    return parsed


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=_positive_int, default=5)
    parser.add_argument("--include-wgpu", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    options = parser.parse_args(argv)
    output = cast(Path, options.output)
    document = run_profiles(
        repeats=cast(int, options.repeats), include_wgpu=cast(bool, options.include_wgpu)
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "schema": _SCHEMA,
                "output": output.name,
                "workloads": len(cast(list[object], document["workloads"])),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
