"""M3 benchmark artifact validation and tamper-resistance tests."""

from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest

_VALIDATOR = Path(__file__).parents[2] / "benchmarks" / "validate_m3_results.py"
_NAMES = (
    "extract_pack_1000",
    "extract_pack_10000",
    "null_submit_1000",
    "null_submit_10000",
    "wgpu_submit_1000",
    "wgpu_submit_10000",
)


def _workload(name: str) -> dict[str, object]:
    targeted = name in ("extract_pack_10000", "wgpu_submit_10000")
    return {
        "name": name,
        "workload_version": 1,
        "warmups": 3,
        "samples": 3,
        "parameters": {"visible_sprites": 10_000 if name.endswith("10000") else 1_000},
        "durations_ns": [1, 2, 3],
        "p50_ns": 2,
        "p95_ns": 3,
        "p99_ns": 3,
        "draw_calls": 1,
        "target": (
            {
                "metric": "p95_ns",
                "comparator": "<",
                "limit_ns": 3_000_000,
                "observed": True,
            }
            if targeted
            else None
        ),
    }


def _capabilities(backend: str) -> dict[str, object]:
    return {
        "backend": backend,
        "max_texture_dimension_2d": 16_384,
        "timestamp_queries": False,
    }


def _document() -> dict[str, object]:
    return {
        "schema": "ludoweave.benchmark.m3/1",
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
            "ludoweave_version": "0.1.0a1",
            "dependency_versions": {
                "glfw": "2.10.2",
                "rendercanvas": "2.7.2",
                "wgpu": "0.32.0",
            },
            "render_capabilities": _capabilities("wgpu"),
        },
        "null_capabilities": _capabilities("null-device"),
        "git": {"commit": "a" * 40, "dirty": True},
        "workloads": [_workload(name) for name in _NAMES],
    }


def _validate(document: dict[str, object], tmp_path: Path) -> subprocess.CompletedProcess[str]:
    artifact = tmp_path / "m3.json"
    artifact.write_text(json.dumps(document), encoding="utf-8")
    return subprocess.run(
        (sys.executable, str(_VALIDATOR), str(artifact)),
        check=False,
        capture_output=True,
        text=True,
    )


def test_m3_validator_accepts_complete_exact_artifact(tmp_path: Path) -> None:
    result = _validate(_document(), tmp_path)
    assert result.returncode == 0
    assert '"targets_met":2' in result.stdout


@pytest.mark.parametrize(
    "mutation",
    ["dependency", "draw_calls", "target", "percentile", "sensitive_key"],
)
def test_m3_validator_rejects_tampering(mutation: str, tmp_path: Path) -> None:
    document = deepcopy(_document())
    environment = cast(dict[str, object], document["environment"])
    workloads = cast(list[dict[str, object]], document["workloads"])
    if mutation == "dependency":
        cast(dict[str, str], environment["dependency_versions"])["wgpu"] = "latest"
    elif mutation == "draw_calls":
        workloads[0]["draw_calls"] = 1_000
    elif mutation == "target":
        cast(dict[str, object], workloads[1]["target"])["observed"] = False
    elif mutation == "percentile":
        workloads[0]["p95_ns"] = 99
    else:
        environment["home_path"] = "private"

    result = _validate(document, tmp_path)
    assert result.returncode == 1
    assert '"valid": false' in result.stdout
