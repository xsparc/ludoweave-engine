"""Benchmark artifact schema and tamper-resistance tests."""

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest

_VALIDATOR = Path(__file__).parents[2] / "benchmarks" / "validate_m1_results.py"


def _workload(
    name: str,
    parameters: dict[str, int],
    *,
    target: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "name": name,
        "workload_version": 1,
        "warmups": 3,
        "samples": 3,
        "parameters": parameters,
        "durations_ns": [1, 2, 3],
        "p50_ns": 2,
        "p95_ns": 3,
        "p99_ns": 3,
        "target": target,
    }


def _valid_document() -> dict[str, object]:
    return {
        "schema": "ludoweave.benchmark.m1/1",
        "seed": 1,
        "samples": 3,
        "warmups": 3,
        "timer": "time.perf_counter_ns",
        "environment": {
            "os": "TestOS",
            "os_release": "1",
            "architecture": "test64",
            "processor": "test processor",
            "python_implementation": "CPython",
            "python_version": "3.12.13",
            "python_build_mode": "release",
            "python_threading_build": "gil",
            "python_gil_enabled": True,
            "ludoweave_version": "0.1.0a1",
            "dependency_versions": {
                "hatchling": "not-installed",
                "hypothesis": "6.160.0",
                "mkdocs-material": "9.7.7",
                "pyright": "1.1.411",
                "pytest": "9.1.1",
                "ruff": "0.15.22",
            },
        },
        "git": {"commit": "a" * 40, "dirty": True},
        "workloads": [
            _workload("entity_lifecycle", {"entity_count": 10_000, "cycles": 2}),
            _workload("read_query_10000", {"entity_count": 10_000, "component_count": 2}),
            _workload("write_query_10000", {"entity_count": 10_000, "component_count": 2}),
            _workload("scheduler_plan_generated_dag", {"system_count": 100, "seed": 1}),
            _workload(
                "command_buffer_staged_flush",
                {"command_count": 1_000, "component_count": 2},
            ),
            _workload(
                "fixed_step_3600_ticks",
                {"tick_count": 3_600, "fixed_hz": 60, "simulated_seconds": 60},
                target={
                    "name": "headless_5x_realtime",
                    "metric": "p95_ns",
                    "comparator": "<=",
                    "limit_ns": 12_000_000_000,
                    "observed": True,
                },
            ),
            _workload(
                "simulation_tick_10000",
                {"entity_count": 10_000, "system_count": 1, "fixed_hz": 60},
                target={
                    "name": "simulation_tick_p95_below_4ms",
                    "metric": "p95_ns",
                    "comparator": "<",
                    "limit_ns": 4_000_000,
                    "observed": True,
                },
            ),
        ],
    }


def _run_validator(document: dict[str, object], tmp_path: Path) -> subprocess.CompletedProcess[str]:
    artifact = tmp_path / "benchmark.json"
    artifact.write_text(json.dumps(document), encoding="utf-8")
    return subprocess.run(
        (sys.executable, str(_VALIDATOR), str(artifact)),
        check=False,
        capture_output=True,
        text=True,
    )


def test_validator_accepts_exact_complete_m1_artifact(tmp_path: Path) -> None:
    result = _run_validator(_valid_document(), tmp_path)

    assert result.returncode == 0
    assert '"targets_observed":2' in result.stdout


@pytest.mark.parametrize(
    ("mutation", "value"),
    [
        ("extra_root", "private-machine-name"),
        ("python_implementation", "PyPy"),
        ("commit", "not-a-commit"),
        ("empty_parameters", {}),
        ("missing_target", None),
        ("wrong_target_limit", 5_000_000),
    ],
)
def test_validator_rejects_tampered_schema_and_gate_contracts(
    mutation: str, value: object, tmp_path: Path
) -> None:
    document = deepcopy(_valid_document())
    if mutation == "extra_root":
        document["hostname"] = value
    elif mutation == "python_implementation":
        cast(dict[str, object], document["environment"])["python_implementation"] = value
    elif mutation == "commit":
        cast(dict[str, object], document["git"])["commit"] = value
    else:
        workloads = cast(list[dict[str, object]], document["workloads"])
        simulation = next(item for item in workloads if item["name"] == "simulation_tick_10000")
        if mutation == "empty_parameters":
            simulation["parameters"] = value
        elif mutation == "missing_target":
            simulation["target"] = value
        else:
            cast(dict[str, object], simulation["target"])["limit_ns"] = value

    result = _run_validator(document, tmp_path)

    assert result.returncode != 0
