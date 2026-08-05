"""Record raw Clockwork Arena tick distributions at bounded stress levels."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import sysconfig
from collections.abc import Sequence
from pathlib import Path
from time import perf_counter_ns

from ludoweave import __version__
from ludoweave.samples import ARENA_FIXED_SEED, clockwork_input, create_clockwork_arena

SCHEMA = "ludoweave.benchmark.m4/1"
STRESS_LEVELS = (1, 4, 8)
TARGET_NS = 16_666_667


def percentile(values: Sequence[int], percentile_value: int) -> int:
    ordered = sorted(values)
    index = max(0, ((len(ordered) * percentile_value + 99) // 100) - 1)
    return ordered[index]


def _git() -> dict[str, object]:
    commit = subprocess.run(
        ("git", "rev-parse", "HEAD"), check=True, capture_output=True, text=True
    ).stdout.strip()
    dirty = bool(
        subprocess.run(
            ("git", "status", "--porcelain"), check=True, capture_output=True, text=True
        ).stdout
    )
    return {"commit": commit, "dirty": dirty}


def _environment() -> dict[str, object]:
    gil_probe = getattr(sys, "_is_gil_enabled", None)
    gil_enabled = True if gil_probe is None else bool(gil_probe())
    return {
        "architecture": platform.machine() or "unknown",
        "free_threaded_build": bool(sysconfig.get_config_var("Py_GIL_DISABLED")),
        "gil_enabled": gil_enabled,
        "ludoweave_version": __version__,
        "os": platform.system(),
        "os_release": platform.release(),
        "processor": platform.processor() or "unknown",
        "python_build_mode": "debug" if sysconfig.get_config_var("Py_DEBUG") else "release",
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
    }


def run(*, samples: int, warmups: int) -> dict[str, object]:
    if samples <= 0 or warmups < 0:
        raise ValueError("samples must be positive and warmups non-negative")
    workloads: list[dict[str, object]] = []
    for stress in STRESS_LEVELS:
        arena = create_clockwork_arena(
            clockwork_input(warmups + samples),
            seed=ARENA_FIXED_SEED,
            stress=stress,
        )
        for _ in range(warmups):
            arena.tick()
        durations: list[int] = []
        for _ in range(samples):
            started = perf_counter_ns()
            arena.tick()
            durations.append(perf_counter_ns() - started)
        summary = arena.summary()
        p95 = percentile(durations, 95)
        target = None
        if stress == 1:
            target = {
                "comparator": "<",
                "limit_ns": TARGET_NS,
                "metric": "p95_ns",
                "observed": p95 < TARGET_NS,
            }
        workloads.append(
            {
                "durations_ns": durations,
                "final_metrics": summary.as_dict(),
                "name": f"clockwork_arena_stress_{stress}",
                "p50_ns": percentile(durations, 50),
                "p95_ns": p95,
                "p99_ns": percentile(durations, 99),
                "parameters": {"fixed_seed": ARENA_FIXED_SEED, "stress": stress},
                "samples": samples,
                "target": target,
                "warmups": warmups,
                "workload_version": 1,
            }
        )
    return {
        "environment": _environment(),
        "git": _git(),
        "samples": samples,
        "schema": SCHEMA,
        "timer": "time.perf_counter_ns",
        "warmups": warmups,
        "workloads": workloads,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=300)
    parser.add_argument("--warmups", type=int, default=60)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    document = run(samples=arguments.samples, warmups=arguments.warmups)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(document, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
