"""Validate one raw M1 benchmark result without imposing universal timing gates."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import cast

_SCHEMA = "ludoweave.benchmark.m1/1"
_REQUIRED_WORKLOADS = {
    "entity_lifecycle",
    "read_query_10000",
    "write_query_10000",
    "scheduler_plan_generated_dag",
    "command_buffer_staged_flush",
    "fixed_step_3600_ticks",
    "simulation_tick_10000",
}
_ROOT_KEYS = {"schema", "seed", "samples", "warmups", "timer", "environment", "git", "workloads"}
_ENVIRONMENT_KEYS = {
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
}
_DEPENDENCY_KEYS = {
    "hatchling",
    "hypothesis",
    "mkdocs-material",
    "pyright",
    "pytest",
    "ruff",
}
_GIT_KEYS = {"commit", "dirty"}
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
    "target",
}
_TARGET_KEYS = {"name", "metric", "comparator", "limit_ns", "observed"}
_FIXED_PARAMETERS: dict[str, Mapping[str, int]] = {
    "entity_lifecycle": {"entity_count": 10_000, "cycles": 2},
    "read_query_10000": {"entity_count": 10_000, "component_count": 2},
    "write_query_10000": {"entity_count": 10_000, "component_count": 2},
    "command_buffer_staged_flush": {"command_count": 1_000, "component_count": 2},
    "fixed_step_3600_ticks": {"tick_count": 3_600, "fixed_hz": 60, "simulated_seconds": 60},
    "simulation_tick_10000": {"entity_count": 10_000, "system_count": 1, "fixed_hz": 60},
}
_TARGETS: dict[str, Mapping[str, int | str]] = {
    "fixed_step_3600_ticks": {
        "name": "headless_5x_realtime",
        "metric": "p95_ns",
        "comparator": "<=",
        "limit_ns": 12_000_000_000,
    },
    "simulation_tick_10000": {
        "name": "simulation_tick_p95_below_4ms",
        "metric": "p95_ns",
        "comparator": "<",
        "limit_ns": 4_000_000,
    },
}
_COMMIT = re.compile(r"[0-9a-f]{40}\Z")
_PYTHON_VERSION = re.compile(r"3\.(?:12|13|14)(?:\.\d+)?\Z")
_PACKAGE_VERSION = re.compile(r"\d+\.\d+\.\d+(?:[A-Za-z0-9.]+)?\Z")
_FORBIDDEN_KEYS = (
    "credential",
    "environment_value",
    "home",
    "password",
    "path",
    "secret",
    "token",
    "user",
)


def _mapping(value: object, *, location: str) -> Mapping[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{location} must be an object with string keys")
    untyped = cast(dict[object, object], value)
    if any(type(key) is not str for key in untyped):
        raise ValueError(f"{location} must be an object with string keys")
    return cast(Mapping[str, object], untyped)


def _exact_int(value: object, *, location: str, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{location} must be an integer >= {minimum}")
    return value


def _string(value: object, *, location: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(f"{location} must be a non-empty string")
    return value


def _require_keys(value: Mapping[str, object], expected: set[str], *, location: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = ",".join(sorted(expected - actual))
        extra = ",".join(sorted(actual - expected))
        raise ValueError(f"{location} has invalid keys (missing={missing!r}, extra={extra!r})")


def _percentile(values: Sequence[int], percentile: int) -> int:
    ordered = sorted(values)
    index = max(0, ((len(ordered) * percentile + 99) // 100) - 1)
    return ordered[index]


def _reject_sensitive_keys(value: object, *, location: str = "root") -> None:
    if isinstance(value, dict):
        for key, nested in cast(dict[object, object], value).items():
            lowered = str(key).lower()
            if any(fragment in lowered for fragment in _FORBIDDEN_KEYS):
                raise ValueError(f"{location} contains forbidden metadata key {key!r}")
            _reject_sensitive_keys(nested, location=f"{location}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(cast(list[object], value)):
            _reject_sensitive_keys(nested, location=f"{location}[{index}]")


def validate(document: object) -> tuple[int, int]:
    root = _mapping(document, location="root")
    _require_keys(root, _ROOT_KEYS, location="root")
    if root.get("schema") != _SCHEMA:
        raise ValueError("root.schema is unsupported")
    samples = _exact_int(root.get("samples"), location="root.samples", minimum=1)
    warmups = _exact_int(root.get("warmups"), location="root.warmups")
    _exact_int(root.get("seed"), location="root.seed")
    if root.get("timer") != "time.perf_counter_ns":
        raise ValueError("root.timer must identify the monotonic benchmark timer")

    environment = _mapping(root.get("environment"), location="root.environment")
    _require_keys(environment, _ENVIRONMENT_KEYS, location="root.environment")
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
        _string(environment.get(field), location=f"root.environment.{field}")
    if environment["python_implementation"] != "CPython":
        raise ValueError("root.environment.python_implementation must be CPython")
    if not _PYTHON_VERSION.fullmatch(cast(str, environment["python_version"])):
        raise ValueError("root.environment.python_version is outside the supported range")
    if environment["python_build_mode"] not in ("debug", "release"):
        raise ValueError("root.environment.python_build_mode is unsupported")
    if environment["python_threading_build"] not in ("gil", "free-threaded"):
        raise ValueError("root.environment.python_threading_build is unsupported")
    if (
        environment["python_gil_enabled"] is not None
        and type(environment["python_gil_enabled"]) is not bool
    ):
        raise ValueError("root.environment.python_gil_enabled must be bool or null")
    if not _PACKAGE_VERSION.fullmatch(cast(str, environment["ludoweave_version"])):
        raise ValueError("root.environment.ludoweave_version is malformed")
    dependencies = _mapping(
        environment.get("dependency_versions"),
        location="root.environment.dependency_versions",
    )
    _require_keys(dependencies, _DEPENDENCY_KEYS, location="root.environment.dependency_versions")
    for package, package_version in dependencies.items():
        _string(package, location="dependency package")
        _string(package_version, location=f"dependency {package}")

    git = _mapping(root.get("git"), location="root.git")
    _require_keys(git, _GIT_KEYS, location="root.git")
    commit = _string(git.get("commit"), location="root.git.commit")
    if _COMMIT.fullmatch(commit) is None:
        raise ValueError("root.git.commit must be one lowercase 40-character commit hash")
    if type(git.get("dirty")) is not bool:
        raise ValueError("root.git.dirty must be a boolean")

    raw_workloads = root.get("workloads")
    if not isinstance(raw_workloads, list):
        raise ValueError("root.workloads must be an array")
    workloads = tuple(
        _mapping(item, location="workload") for item in cast(list[object], raw_workloads)
    )
    names = {_string(item.get("name"), location="workload.name") for item in workloads}
    if names != _REQUIRED_WORKLOADS or len(workloads) != len(_REQUIRED_WORKLOADS):
        raise ValueError("benchmark result does not contain the exact M1 workload set")

    observed_targets = 0
    target_count = 0
    for workload in workloads:
        _require_keys(workload, _WORKLOAD_KEYS, location="workload")
        name = _string(workload.get("name"), location="workload.name")
        if _exact_int(workload.get("workload_version"), location=f"{name}.version", minimum=1) != 1:
            raise ValueError(f"{name} has an unsupported workload version")
        if _exact_int(workload.get("warmups"), location=f"{name}.warmups") != warmups:
            raise ValueError(f"{name} warmup count differs from the document")
        if _exact_int(workload.get("samples"), location=f"{name}.samples", minimum=1) != samples:
            raise ValueError(f"{name} sample count differs from the document")
        parameters = _mapping(workload.get("parameters"), location=f"{name}.parameters")
        expected_parameters: Mapping[str, int]
        if name == "scheduler_plan_generated_dag":
            expected_parameters = {"system_count": 100, "seed": cast(int, root["seed"])}
        else:
            expected_parameters = _FIXED_PARAMETERS[name]
        if set(parameters) != set(expected_parameters) or any(
            type(parameters[key]) is not int or parameters[key] != expected
            for key, expected in expected_parameters.items()
        ):
            raise ValueError(f"{name} parameters do not match the versioned workload")
        raw_durations = workload.get("durations_ns")
        if not isinstance(raw_durations, list):
            raise ValueError(f"{name} must contain a raw-sample array")
        duration_items = cast(list[object], raw_durations)
        if len(duration_items) != samples:
            raise ValueError(f"{name} must contain exactly {samples} raw samples")
        durations = tuple(
            _exact_int(item, location=f"{name}.durations_ns", minimum=1) for item in duration_items
        )
        for percentile in (50, 95, 99):
            recorded = _exact_int(
                workload.get(f"p{percentile}_ns"),
                location=f"{name}.p{percentile}_ns",
                minimum=1,
            )
            if recorded != _percentile(durations, percentile):
                raise ValueError(f"{name} p{percentile} does not match its raw samples")

        raw_target = workload.get("target")
        expected_target = _TARGETS.get(name)
        if expected_target is None:
            if raw_target is not None:
                raise ValueError(f"{name} must not report an unspecified target")
            continue
        if raw_target is None:
            raise ValueError(f"{name} is missing its required target observation")
        target_count += 1
        target = _mapping(raw_target, location=f"{name}.target")
        _require_keys(target, _TARGET_KEYS, location=f"{name}.target")
        for field, expected_value in expected_target.items():
            if target.get(field) != expected_value:
                raise ValueError(f"{name} target {field} differs from the versioned contract")
        limit = cast(int, expected_target["limit_ns"])
        observed = target.get("observed")
        if type(observed) is not bool:
            raise ValueError(f"{name}.target.observed must be a boolean")
        p95 = cast(int, workload["p95_ns"])
        expected = p95 < limit if expected_target["comparator"] == "<" else p95 <= limit
        if observed is not expected:
            raise ValueError(f"{name} target observation does not match its p95")
        observed_targets += int(observed)

    _reject_sensitive_keys(document)
    if target_count != len(_TARGETS):
        raise ValueError("benchmark result has an incomplete target set")
    return observed_targets, target_count


def main(arguments: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    options = parser.parse_args(arguments)
    path = cast(Path, options.result)
    document = cast(object, json.loads(path.read_text(encoding="utf-8")))
    observed, total = validate(document)
    print(
        json.dumps(
            {
                "schema": "ludoweave.benchmark.validation/1",
                "status": "ok",
                "targets_observed": observed,
                "targets_recorded": total,
                "workloads": len(_REQUIRED_WORKLOADS),
            },
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
