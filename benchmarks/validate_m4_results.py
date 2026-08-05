"""Validate M4 stress evidence without converting local timing into a pass gate."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import cast

from benchmark_m4 import SCHEMA, STRESS_LEVELS, TARGET_NS, percentile

_COMMIT = re.compile(r"[0-9a-f]{40}\Z")
_PYTHON = re.compile(r"3\.(?:12|13|14)(?:\.\d+)?\Z")
_FORBIDDEN = ("credential", "home", "password", "path", "secret", "token", "user")


def _mapping(value: object, *, location: str) -> Mapping[str, object]:
    if type(value) is not dict:
        raise ValueError(f"{location} must be an object")
    checked = cast(dict[object, object], value)
    if any(type(key) is not str for key in checked):
        raise ValueError(f"{location} keys must be text")
    return cast(Mapping[str, object], checked)


def _integer(value: object, *, location: str, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{location} must be an integer >= {minimum}")
    return value


def _text(value: object, *, location: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(f"{location} must be non-empty text")
    return value


def _reject_sensitive(value: object) -> None:
    if type(value) is dict:
        for key, nested in cast(dict[object, object], value).items():
            if any(fragment in str(key).lower() for fragment in _FORBIDDEN):
                raise ValueError(f"benchmark contains forbidden metadata key {key!r}")
            _reject_sensitive(nested)
    elif type(value) is list:
        for nested in cast(list[object], value):
            _reject_sensitive(nested)


def validate(document: object) -> tuple[int, bool]:
    root = _mapping(document, location="root")
    if set(root) != {"environment", "git", "samples", "schema", "timer", "warmups", "workloads"}:
        raise ValueError("root fields do not match the M4 schema")
    if root["schema"] != SCHEMA or root["timer"] != "time.perf_counter_ns":
        raise ValueError("benchmark schema or timer is unsupported")
    samples = _integer(root["samples"], location="samples", minimum=1)
    warmups = _integer(root["warmups"], location="warmups")
    environment = _mapping(root["environment"], location="environment")
    if set(environment) != {
        "architecture",
        "free_threaded_build",
        "gil_enabled",
        "ludoweave_version",
        "os",
        "os_release",
        "processor",
        "python_build_mode",
        "python_implementation",
        "python_version",
    }:
        raise ValueError("environment fields do not match")
    for field in ("architecture", "ludoweave_version", "os", "os_release", "processor"):
        _text(environment[field], location=f"environment.{field}")
    if environment["python_implementation"] != "CPython":
        raise ValueError("benchmark requires CPython")
    if _PYTHON.fullmatch(_text(environment["python_version"], location="python_version")) is None:
        raise ValueError("Python version is unsupported")
    if environment["python_build_mode"] not in ("debug", "release"):
        raise ValueError("Python build mode is unsupported")
    if (
        type(environment["free_threaded_build"]) is not bool
        or type(environment["gil_enabled"]) is not bool
    ):
        raise ValueError("threading metadata must be boolean")
    git = _mapping(root["git"], location="git")
    if (
        set(git) != {"commit", "dirty"}
        or _COMMIT.fullmatch(_text(git.get("commit"), location="git.commit")) is None
        or type(git.get("dirty")) is not bool
    ):
        raise ValueError("git metadata is malformed")
    raw_workloads = root["workloads"]
    if type(raw_workloads) is not list:
        raise ValueError("workloads must be an array")
    workloads = tuple(
        _mapping(item, location="workload") for item in cast(list[object], raw_workloads)
    )
    if len(workloads) != len(STRESS_LEVELS):
        raise ValueError("stress workload set is incomplete")
    seen: set[int] = set()
    baseline_observed = False
    for workload in workloads:
        if set(workload) != {
            "durations_ns",
            "final_metrics",
            "name",
            "p50_ns",
            "p95_ns",
            "p99_ns",
            "parameters",
            "samples",
            "target",
            "warmups",
            "workload_version",
        }:
            raise ValueError("workload fields do not match")
        parameters = _mapping(workload["parameters"], location="parameters")
        stress = _integer(parameters.get("stress"), location="stress", minimum=1)
        if (
            parameters != {"fixed_seed": 0xC10C_A11E, "stress": stress}
            or stress not in STRESS_LEVELS
        ):
            raise ValueError("stress parameters are unexpected")
        seen.add(stress)
        if workload["name"] != f"clockwork_arena_stress_{stress}":
            raise ValueError("workload name is unexpected")
        if (
            workload["samples"] != samples
            or workload["warmups"] != warmups
            or workload["workload_version"] != 1
        ):
            raise ValueError("workload metadata differs from root")
        raw = workload["durations_ns"]
        if type(raw) is not list:
            raise ValueError("duration sample count is invalid")
        raw_items = cast(list[object], raw)
        if len(raw_items) != samples:
            raise ValueError("duration sample count is invalid")
        durations = tuple(_integer(item, location="duration", minimum=1) for item in raw_items)
        for value in (50, 95, 99):
            if workload[f"p{value}_ns"] != percentile(durations, value):
                raise ValueError("duration percentile does not match raw samples")
        metrics = _mapping(workload["final_metrics"], location="final_metrics")
        if _integer(metrics.get("ticks"), location="final_ticks") != warmups + samples:
            raise ValueError("final tick count is inconsistent")
        if stress == 1:
            observed = cast(int, workload["p95_ns"]) < TARGET_NS
            if workload["target"] != {
                "comparator": "<",
                "limit_ns": TARGET_NS,
                "metric": "p95_ns",
                "observed": observed,
            }:
                raise ValueError("baseline target evidence is inconsistent")
            baseline_observed = observed
        elif workload["target"] is not None:
            raise ValueError("stress workloads must not claim a timing target")
    if seen != set(STRESS_LEVELS):
        raise ValueError("stress levels are incomplete")
    _reject_sensitive(document)
    return len(workloads), baseline_observed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    arguments = parser.parse_args()
    try:
        document = json.loads(arguments.artifact.read_text(encoding="utf-8"))
        workloads, observed = validate(document)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(json.dumps({"error": str(error), "schema": SCHEMA, "valid": False}))
        return 1
    print(
        json.dumps(
            {
                "baseline_target_observed": observed,
                "schema": SCHEMA,
                "valid": True,
                "workloads": workloads,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
