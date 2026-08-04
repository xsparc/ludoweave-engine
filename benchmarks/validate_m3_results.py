"""Validate M3 renderer benchmark evidence without rewriting timing outcomes."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import cast

_SCHEMA = "ludoweave.benchmark.m3/1"
_COUNTS = (1_000, 10_000)
_WORKLOADS = {
    **{f"extract_pack_{count}": count for count in _COUNTS},
    **{f"null_submit_{count}": count for count in _COUNTS},
    **{f"wgpu_submit_{count}": count for count in _COUNTS},
}
_TARGETED = {"extract_pack_10000", "wgpu_submit_10000"}
_ROOT_KEYS = {
    "schema",
    "seed",
    "samples",
    "warmups",
    "timer",
    "environment",
    "null_capabilities",
    "git",
    "workloads",
}
_WORKLOAD_KEYS = {
    "name",
    "workload_version",
    "warmups",
    "samples",
    "parameters",
    "durations_ns",
    "p50_ns",
    "p95_ns",
    "p99_ns",
    "draw_calls",
    "target",
}
_ENVIRONMENT_KEYS = {
    "os",
    "os_release",
    "architecture",
    "processor",
    "python_implementation",
    "python_version",
    "python_build_mode",
    "ludoweave_version",
    "dependency_versions",
    "render_capabilities",
}
_CAPABILITY_KEYS = {"backend", "max_texture_dimension_2d", "timestamp_queries"}
_COMMIT = re.compile(r"[0-9a-f]{40}\Z")
_PYTHON = re.compile(r"3\.(?:12|13|14)(?:\.\d+)?\Z")
_VERSION = re.compile(r"\d+\.\d+\.\d+(?:[A-Za-z0-9.]+)?\Z")
_FORBIDDEN_KEYS = ("credential", "home", "password", "path", "secret", "token", "user")


def _mapping(value: object, *, location: str) -> Mapping[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{location} must be an object")
    candidate = cast(dict[object, object], value)
    if any(type(key) is not str for key in candidate):
        raise ValueError(f"{location} keys must be text")
    return cast(Mapping[str, object], candidate)


def _keys(value: Mapping[str, object], expected: set[str], *, location: str) -> None:
    if set(value) != expected:
        raise ValueError(f"{location} fields do not match the schema")


def _text(value: object, *, location: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(f"{location} must be non-empty text")
    return value


def _integer(value: object, *, location: str, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{location} must be an integer >= {minimum}")
    return value


def _percentile(values: Sequence[int], percentile: int) -> int:
    ordered = sorted(values)
    index = max(0, ((len(ordered) * percentile + 99) // 100) - 1)
    return ordered[index]


def _reject_sensitive_keys(value: object) -> None:
    if isinstance(value, dict):
        for key, nested in cast(dict[object, object], value).items():
            lowered = str(key).lower()
            if any(fragment in lowered for fragment in _FORBIDDEN_KEYS):
                raise ValueError(f"benchmark contains forbidden metadata key {key!r}")
            _reject_sensitive_keys(nested)
    elif isinstance(value, list):
        for nested in cast(list[object], value):
            _reject_sensitive_keys(nested)


def _capabilities(value: object, *, backend: str, location: str) -> None:
    capabilities = _mapping(value, location=location)
    _keys(capabilities, _CAPABILITY_KEYS, location=location)
    if capabilities["backend"] != backend:
        raise ValueError(f"{location}.backend is unexpected")
    _integer(
        capabilities["max_texture_dimension_2d"],
        location=f"{location}.max_texture_dimension_2d",
        minimum=1,
    )
    if type(capabilities["timestamp_queries"]) is not bool:
        raise ValueError(f"{location}.timestamp_queries must be boolean")


def validate(document: object) -> tuple[int, int]:
    root = _mapping(document, location="root")
    _keys(root, _ROOT_KEYS, location="root")
    if root["schema"] != _SCHEMA or root["timer"] != "time.perf_counter_ns":
        raise ValueError("benchmark schema or timer is unsupported")
    samples = _integer(root["samples"], location="root.samples", minimum=1)
    warmups = _integer(root["warmups"], location="root.warmups")
    _integer(root["seed"], location="root.seed")

    environment = _mapping(root["environment"], location="environment")
    _keys(environment, _ENVIRONMENT_KEYS, location="environment")
    for field in ("os", "os_release", "architecture", "processor"):
        _text(environment[field], location=f"environment.{field}")
    if environment["python_implementation"] != "CPython":
        raise ValueError("benchmark requires CPython")
    if _PYTHON.fullmatch(_text(environment["python_version"], location="python_version")) is None:
        raise ValueError("python version is outside the supported range")
    if environment["python_build_mode"] not in ("debug", "release"):
        raise ValueError("python build mode is unsupported")
    if _VERSION.fullmatch(_text(environment["ludoweave_version"], location="version")) is None:
        raise ValueError("LudoWeave version is malformed")
    dependencies = _mapping(environment["dependency_versions"], location="dependencies")
    if dependencies != {"glfw": "2.10.2", "rendercanvas": "2.7.2", "wgpu": "0.32.0"}:
        raise ValueError("graphics dependency versions do not match the M3 pins")
    _capabilities(
        environment["render_capabilities"], backend="wgpu", location="render_capabilities"
    )
    _capabilities(root["null_capabilities"], backend="null-device", location="null_capabilities")

    git = _mapping(root["git"], location="git")
    _keys(git, {"commit", "dirty"}, location="git")
    if _COMMIT.fullmatch(_text(git["commit"], location="git.commit")) is None:
        raise ValueError("git commit is malformed")
    if type(git["dirty"]) is not bool:
        raise ValueError("git.dirty must be boolean")

    raw_workloads = root["workloads"]
    if not isinstance(raw_workloads, list):
        raise ValueError("workloads must be an array")
    workload_items = cast(list[object], raw_workloads)
    workloads = tuple(_mapping(item, location="workload") for item in workload_items)
    names = {_text(item.get("name"), location="workload.name") for item in workloads}
    if names != set(_WORKLOADS) or len(workloads) != len(_WORKLOADS):
        raise ValueError("benchmark workload set is incomplete")
    targets_met = 0
    for workload in workloads:
        _keys(workload, _WORKLOAD_KEYS, location="workload")
        name = _text(workload["name"], location="workload.name")
        if workload["workload_version"] != 1:
            raise ValueError("workload version is unsupported")
        if workload["samples"] != samples or workload["warmups"] != warmups:
            raise ValueError("workload sample metadata differs from root")
        parameters = _mapping(workload["parameters"], location="parameters")
        if parameters != {"visible_sprites": _WORKLOADS[name]}:
            raise ValueError("workload parameters are unexpected")
        raw_durations = workload["durations_ns"]
        if not isinstance(raw_durations, list):
            raise ValueError("workload durations have the wrong sample count")
        duration_items = cast(list[object], raw_durations)
        if len(duration_items) != samples:
            raise ValueError("workload durations have the wrong sample count")
        durations = tuple(_integer(item, location="duration", minimum=1) for item in duration_items)
        for percentile in (50, 95, 99):
            if workload[f"p{percentile}_ns"] != _percentile(durations, percentile):
                raise ValueError("workload percentile does not match durations")
        if workload["draw_calls"] != 1:
            raise ValueError("renderer benchmark must use one normal batch draw")
        target = workload["target"]
        if name not in _TARGETED:
            if target is not None:
                raise ValueError("untargeted workload declares a target")
            continue
        target_map = _mapping(target, location="target")
        _keys(
            target_map,
            {"metric", "comparator", "limit_ns", "observed"},
            location="target",
        )
        expected_observation = cast(int, workload["p95_ns"]) < 3_000_000
        if target_map != {
            "metric": "p95_ns",
            "comparator": "<",
            "limit_ns": 3_000_000,
            "observed": expected_observation,
        }:
            raise ValueError("target evidence does not match the measured p95")
        targets_met += int(expected_observation)

    _reject_sensitive_keys(document)
    return len(_TARGETED), targets_met


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    arguments = parser.parse_args()
    try:
        document = json.loads(arguments.artifact.read_text(encoding="utf-8"))
        targets, met = validate(document)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(json.dumps({"schema": _SCHEMA, "valid": False, "error": str(error)}))
        return 1
    print(
        json.dumps(
            {"schema": _SCHEMA, "valid": True, "targets_observed": targets, "targets_met": met},
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
