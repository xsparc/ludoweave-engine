"""Validate informational M2 benchmark evidence without timing pass claims."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import cast

_SCHEMA = "ludoweave.benchmark.m2/1"
_WORKLOADS = {
    "canonical_transaction_100": {"command_count": 100},
    "atomic_transaction_apply_100": {"command_count": 100},
    "snapshot_roundtrip_1000": {"entity_count": 1_000, "snapshot_bytes": None},
    "replay_verify_100_batches": {"batch_count": 100, "replay_bytes": None},
}
_ROOT_KEYS = {
    "schema",
    "seed",
    "samples",
    "warmups",
    "timer",
    "memory",
    "environment",
    "git",
    "workloads",
}
_ENVIRONMENT_KEYS = {
    "os",
    "os_release",
    "architecture",
    "python_implementation",
    "python_version",
    "python_threading_build",
    "ludoweave_version",
}
_GIT_KEYS = {"commit", "dirty"}
_WORKLOAD_KEYS = {
    "name",
    "workload_version",
    "warmups",
    "samples",
    "parameters",
    "durations_ns",
    "peak_bytes",
    "p50_ns",
    "p95_ns",
    "p99_ns",
    "peak_p95_bytes",
    "target",
}
_COMMIT = re.compile(r"[0-9a-f]{40}\Z")
_PYTHON = re.compile(r"3\.(?:12|13|14)(?:\.\d+)?\Z")
_VERSION = re.compile(r"\d+\.\d+\.\d+(?:[A-Za-z0-9.]+)?\Z")
_FORBIDDEN_KEYS = ("credential", "home", "password", "path", "secret", "token", "user")


def _mapping(value: object, *, location: str) -> Mapping[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{location} must be an object")
    candidate = cast(dict[object, object], value)
    if any(type(key) is not str for key in candidate):
        raise ValueError(f"{location} must have text keys")
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


def _integer_list(value: object, *, location: str, length: int) -> tuple[int, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{location} must contain exactly {length} samples")
    items = cast(list[object], value)
    if len(items) != length:
        raise ValueError(f"{location} must contain exactly {length} samples")
    result = tuple(
        _integer(item, location=f"{location}[{index}]", minimum=1)
        for index, item in enumerate(items)
    )
    return result


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


def validate(document: object) -> int:
    root = _mapping(document, location="root")
    _keys(root, _ROOT_KEYS, location="root")
    if root["schema"] != _SCHEMA:
        raise ValueError("root.schema is unsupported")
    samples = _integer(root["samples"], location="root.samples", minimum=1)
    warmups = _integer(root["warmups"], location="root.warmups")
    _integer(root["seed"], location="root.seed")
    if root["timer"] != "time.perf_counter_ns":
        raise ValueError("root.timer is unsupported")
    if root["memory"] != "tracemalloc.peak_bytes":
        raise ValueError("root.memory is unsupported")

    environment = _mapping(root["environment"], location="environment")
    _keys(environment, _ENVIRONMENT_KEYS, location="environment")
    for field in ("os", "os_release", "architecture"):
        _text(environment[field], location=f"environment.{field}")
    if environment["python_implementation"] != "CPython":
        raise ValueError("benchmark requires CPython")
    python_version = _text(environment["python_version"], location="python_version")
    if _PYTHON.fullmatch(python_version) is None:
        raise ValueError("python version is outside the supported range")
    if environment["python_threading_build"] not in ("gil", "free-threaded"):
        raise ValueError("threading build is unsupported")
    version = _text(environment["ludoweave_version"], location="ludoweave_version")
    if _VERSION.fullmatch(version) is None:
        raise ValueError("LudoWeave version is malformed")

    git = _mapping(root["git"], location="git")
    _keys(git, _GIT_KEYS, location="git")
    if _COMMIT.fullmatch(_text(git["commit"], location="git.commit")) is None:
        raise ValueError("git commit is malformed")
    if type(git["dirty"]) is not bool:
        raise ValueError("git.dirty must be boolean")

    raw_workloads = root["workloads"]
    if not isinstance(raw_workloads, list):
        raise ValueError("root.workloads must be an array")
    workloads = tuple(
        _mapping(item, location="workload") for item in cast(list[object], raw_workloads)
    )
    if len(workloads) != len(_WORKLOADS):
        raise ValueError("benchmark has the wrong workload count")
    names = {_text(item.get("name"), location="workload.name") for item in workloads}
    if names != set(_WORKLOADS):
        raise ValueError("benchmark has the wrong workload identities")

    for workload in workloads:
        _keys(workload, _WORKLOAD_KEYS, location="workload")
        name = cast(str, workload["name"])
        if _integer(workload["workload_version"], location=f"{name}.version", minimum=1) != 1:
            raise ValueError(f"{name} version is unsupported")
        if _integer(workload["samples"], location=f"{name}.samples") != samples:
            raise ValueError(f"{name} samples differ from root")
        if _integer(workload["warmups"], location=f"{name}.warmups") != warmups:
            raise ValueError(f"{name} warmups differ from root")
        parameters = _mapping(workload["parameters"], location=f"{name}.parameters")
        expected_parameters = _WORKLOADS[name]
        if set(parameters) != set(expected_parameters):
            raise ValueError(f"{name} parameters differ from schema")
        for field, expected in expected_parameters.items():
            actual = _integer(parameters[field], location=f"{name}.{field}", minimum=1)
            if expected is not None and actual != expected:
                raise ValueError(f"{name}.{field} differs from its fixture")
        durations = _integer_list(
            workload["durations_ns"],
            location=f"{name}.durations_ns",
            length=samples,
        )
        peaks = _integer_list(
            workload["peak_bytes"],
            location=f"{name}.peak_bytes",
            length=samples,
        )
        expected_distribution = {
            "p50_ns": _percentile(durations, 50),
            "p95_ns": _percentile(durations, 95),
            "p99_ns": _percentile(durations, 99),
            "peak_p95_bytes": _percentile(peaks, 95),
        }
        for field, expected in expected_distribution.items():
            if _integer(workload[field], location=f"{name}.{field}", minimum=1) != expected:
                raise ValueError(f"{name}.{field} is inconsistent with raw samples")
        if workload["target"] is not None:
            raise ValueError("M2 informational workloads must not claim timing targets")

    _reject_sensitive_keys(document)
    return len(workloads)


def main(arguments: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    options = parser.parse_args(arguments)
    artifact = cast(Path, options.artifact)
    document = json.loads(artifact.read_text(encoding="utf-8"))
    count = validate(document)
    print(f"validated {count} informational M2 workloads with no timing targets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
