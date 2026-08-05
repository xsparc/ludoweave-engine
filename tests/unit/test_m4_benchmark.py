"""M4 stress benchmark schema and tamper-resistance tests."""

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest

_VALIDATOR = Path(__file__).parents[2] / "benchmarks" / "validate_m4_results.py"


def _workload(stress: int) -> dict[str, object]:
    target = None
    if stress == 1:
        target = {
            "comparator": "<",
            "limit_ns": 16_666_667,
            "metric": "p95_ns",
            "observed": True,
        }
    return {
        "durations_ns": [1, 2, 3],
        "final_metrics": {"state_hash": "sha256:" + "0" * 64, "ticks": 5},
        "name": f"clockwork_arena_stress_{stress}",
        "p50_ns": 2,
        "p95_ns": 3,
        "p99_ns": 3,
        "parameters": {"fixed_seed": 0xC10C_A11E, "stress": stress},
        "samples": 3,
        "target": target,
        "warmups": 2,
        "workload_version": 1,
    }


def _document() -> dict[str, object]:
    return {
        "environment": {
            "architecture": "test64",
            "free_threaded_build": False,
            "gil_enabled": True,
            "ludoweave_version": "0.1.0.dev0",
            "os": "TestOS",
            "os_release": "1",
            "processor": "test processor",
            "python_build_mode": "release",
            "python_implementation": "CPython",
            "python_version": "3.12.13",
        },
        "git": {"commit": "a" * 40, "dirty": True},
        "samples": 3,
        "schema": "ludoweave.benchmark.m4/1",
        "timer": "time.perf_counter_ns",
        "warmups": 2,
        "workloads": [_workload(stress) for stress in (1, 4, 8)],
    }


def _validate(document: dict[str, object], tmp_path: Path) -> subprocess.CompletedProcess[str]:
    artifact = tmp_path / "m4.json"
    artifact.write_text(json.dumps(document), encoding="utf-8")
    return subprocess.run(
        (sys.executable, str(_VALIDATOR), str(artifact)),
        check=False,
        capture_output=True,
        text=True,
    )


def test_m4_validator_accepts_complete_raw_stress_artifact(tmp_path: Path) -> None:
    result = _validate(_document(), tmp_path)
    assert result.returncode == 0
    assert '"workloads":3' in result.stdout


@pytest.mark.parametrize("mutation", ["percentile", "target", "ticks", "sensitive"])
def test_m4_validator_rejects_tampering(mutation: str, tmp_path: Path) -> None:
    document = deepcopy(_document())
    workloads = cast(list[dict[str, object]], document["workloads"])
    if mutation == "percentile":
        workloads[0]["p95_ns"] = 99
    elif mutation == "target":
        cast(dict[str, object], workloads[0]["target"])["observed"] = False
    elif mutation == "ticks":
        cast(dict[str, object], workloads[0]["final_metrics"])["ticks"] = 99
    else:
        cast(dict[str, object], document["environment"])["workspace_path"] = "forbidden"

    result = _validate(document, tmp_path)
    assert result.returncode == 1
    assert '"valid": false' in result.stdout
