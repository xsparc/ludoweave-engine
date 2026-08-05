"""Validate sanitized M7 profiling evidence and exact workload invariants."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import cast

_SCHEMA = "ludoweave.profile.m7/1"
_MODULE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\Z")
_BASE_WORKLOADS = {
    "simulation_tick_10000": (
        {"entity_count": 10_000, "fixed_hz": 60, "systems": 1},
        "positive total tick count",
    ),
    "extract_pack_10000": (
        {"visible_sprites": 10_000, "packed_bytes": 640_000},
        "one draw and 10,000 visible sprites",
    ),
}
_WGPU_WORKLOAD = (
    {"visible_sprites": 10_000, "draw_calls": 1},
    "one draw and 10,000 submitted sprites",
)
_WORKLOAD_KEYS = {
    "name",
    "workload_version",
    "parameters",
    "profiled_repeats",
    "total_profiled_ns",
    "primitive_calls",
    "total_calls",
    "result_invariant",
    "hotspots",
}
_HOTSPOT_KEYS = {
    "module",
    "line",
    "function",
    "primitive_calls",
    "total_calls",
    "self_ns",
    "cumulative_ns",
    "cumulative_ratio_ppm",
}


def validate(document: object) -> int:
    root = _mapping(document, location="document")
    _require_exact_keys(
        root,
        {
            "schema",
            "profiler",
            "sort",
            "repeats",
            "include_wgpu",
            "environment",
            "git",
            "workloads",
        },
        location="document",
    )
    if (
        root["schema"] != _SCHEMA
        or root["profiler"] != "cProfile"
        or root["sort"] != "cumulative_ns_desc"
    ):
        raise ValueError("profile identity or ordering contract is invalid")
    repeats = _positive_int(root["repeats"], location="repeats")
    include_wgpu = _boolean(root["include_wgpu"], location="include_wgpu")
    _validate_environment(root["environment"], include_wgpu=include_wgpu)
    _validate_git(root["git"])
    workloads_value = root["workloads"]
    if not isinstance(workloads_value, list):
        raise ValueError("workloads must be a list")
    workloads = cast(list[object], workloads_value)
    expected = dict(_BASE_WORKLOADS)
    if include_wgpu:
        expected["wgpu_submit_10000"] = _WGPU_WORKLOAD
    if len(workloads) != len(expected):
        raise ValueError("profile workload count does not match graphics mode")
    names: list[str] = []
    for index, value in enumerate(workloads):
        workload = _mapping(value, location=f"workloads[{index}]")
        _require_exact_keys(workload, _WORKLOAD_KEYS, location=f"workloads[{index}]")
        name = _text(workload["name"], location=f"workloads[{index}].name")
        if name in names or name not in expected:
            raise ValueError("profile workload identity is duplicate or unknown")
        names.append(name)
        if workload["workload_version"] != 1:
            raise ValueError(f"{name} workload version is incompatible")
        parameters = _mapping(workload["parameters"], location=f"{name}.parameters")
        expected_parameters, expected_invariant = expected[name]
        if parameters != expected_parameters:
            raise ValueError(f"{name} parameters differ from the exact workload")
        if workload["profiled_repeats"] != repeats:
            raise ValueError(f"{name} repeat count differs from the document")
        _positive_int(workload["total_profiled_ns"], location=f"{name}.total_profiled_ns")
        primitive = _positive_int(workload["primitive_calls"], location=f"{name}.primitive_calls")
        total = _positive_int(workload["total_calls"], location=f"{name}.total_calls")
        if primitive > total:
            raise ValueError(f"{name} primitive calls exceed total calls")
        if workload["result_invariant"] != expected_invariant:
            raise ValueError(f"{name} result invariant differs from the exact workload")
        _validate_hotspots(workload["hotspots"], workload=name)
    if names != list(expected):
        raise ValueError("profile workloads are incomplete or out of canonical order")
    return len(workloads)


def _validate_hotspots(value: object, *, workload: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{workload} hotspots must contain 1-25 records")
    records = cast(list[object], value)
    if not 1 <= len(records) <= 25:
        raise ValueError(f"{workload} hotspots must contain 1-25 records")
    previous: tuple[int, int, str, int, str] | None = None
    seen: set[tuple[str, int, str]] = set()
    for index, item in enumerate(records):
        hotspot = _mapping(item, location=f"{workload}.hotspots[{index}]")
        _require_exact_keys(hotspot, _HOTSPOT_KEYS, location=f"{workload}.hotspots[{index}]")
        module = _text(hotspot["module"], location="hotspot.module")
        function = _text(hotspot["function"], location="hotspot.function")
        if not _MODULE.fullmatch(module) or "/" in module or "\\" in module or ":" in module:
            raise ValueError("profile module must be a sanitized dotted name")
        if "/" in function or "\\" in function or ":" in function:
            raise ValueError("profile function must not contain a path")
        if re.search(r"0x[0-9A-Fa-f]{6,}", function):
            raise ValueError("profile function must not contain a memory address")
        line = _non_negative_int(hotspot["line"], location="hotspot.line")
        primitive = _positive_int(hotspot["primitive_calls"], location="hotspot.primitive_calls")
        total = _positive_int(hotspot["total_calls"], location="hotspot.total_calls")
        if primitive > total:
            raise ValueError("hotspot primitive calls exceed total calls")
        self_ns = _non_negative_int(hotspot["self_ns"], location="hotspot.self_ns")
        cumulative_ns = _positive_int(hotspot["cumulative_ns"], location="hotspot.cumulative_ns")
        ratio = _positive_int(
            hotspot["cumulative_ratio_ppm"], location="hotspot.cumulative_ratio_ppm"
        )
        if self_ns > cumulative_ns or ratio > 1_100_000:
            raise ValueError("hotspot timing relationship is invalid")
        identity = (module, line, function)
        if identity in seen:
            raise ValueError("profile hotspot identity is duplicated")
        seen.add(identity)
        order = (-cumulative_ns, -self_ns, module, line, function)
        if previous is not None and order < previous:
            raise ValueError("profile hotspots are not canonically sorted")
        previous = order


def _validate_environment(value: object, *, include_wgpu: bool) -> None:
    environment = _mapping(value, location="environment")
    _require_exact_keys(
        environment,
        {
            "os",
            "os_release",
            "architecture",
            "processor",
            "python_implementation",
            "python_version",
            "python_build_mode",
            "python_threading_build",
            "python_gil_enabled",
            "ludoweave_version",
            "dependency_versions",
            "render_capabilities",
        },
        location="environment",
    )
    for field in (
        "os",
        "os_release",
        "architecture",
        "processor",
        "python_implementation",
        "python_version",
        "python_build_mode",
        "python_threading_build",
        "ludoweave_version",
    ):
        _text(environment[field], location=f"environment.{field}")
    if environment["python_gil_enabled"] is not None:
        _boolean(environment["python_gil_enabled"], location="environment.python_gil_enabled")
    dependencies = _mapping(environment["dependency_versions"], location="dependencies")
    if set(dependencies) != {"glfw", "rendercanvas", "wgpu"} or not all(
        isinstance(value, str) and value for value in dependencies.values()
    ):
        raise ValueError("profile dependency versions are incomplete")
    capabilities = environment["render_capabilities"]
    if include_wgpu:
        capability_map = _mapping(capabilities, location="render_capabilities")
        if capability_map.get("backend") != "wgpu":
            raise ValueError("graphics profile did not use the wgpu backend")
    elif capabilities is not None:
        raise ValueError("base profile must not report render capabilities")


def _validate_git(value: object) -> None:
    git = _mapping(value, location="git")
    _require_exact_keys(git, {"commit", "dirty"}, location="git")
    commit = _text(git["commit"], location="git.commit")
    if commit != "unknown" and not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("profile commit must be a full lowercase Git hash or unknown")
    _boolean(git["dirty"], location="git.dirty")


def _mapping(value: object, *, location: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{location} must be an object with text keys")
    mapping = cast(dict[object, object], value)
    if not all(isinstance(key, str) for key in mapping):
        raise ValueError(f"{location} must be an object with text keys")
    return cast(dict[str, object], mapping)


def _require_exact_keys(value: Mapping[str, object], expected: set[str], *, location: str) -> None:
    if set(value) != expected:
        raise ValueError(f"{location} fields differ from the versioned contract")


def _text(value: object, *, location: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{location} must be non-empty text")
    return value


def _positive_int(value: object, *, location: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{location} must be a positive integer")
    return value


def _non_negative_int(value: object, *, location: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{location} must be a non-negative integer")
    return value


def _boolean(value: object, *, location: str) -> bool:
    if type(value) is not bool:
        raise ValueError(f"{location} must be a boolean")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path)
    options = parser.parse_args(argv)
    profile = cast(Path, options.profile)
    try:
        document: object = json.loads(profile.read_text(encoding="utf-8"))
        workloads = validate(document)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(
            json.dumps(
                {"error": str(error), "schema": _SCHEMA, "valid": False},
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 1
    print(
        json.dumps(
            {"schema": _SCHEMA, "valid": True, "workloads": workloads},
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
