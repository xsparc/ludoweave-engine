"""M7 profile artifact schema and tamper-resistance tests."""

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest

_VALIDATOR = Path(__file__).parents[2] / "benchmarks" / "validate_m7_profile.py"


def _hotspot(module: str = "ludoweave.ecs.world") -> dict[str, object]:
    return {
        "cumulative_ns": 1_000,
        "cumulative_ratio_ppm": 1_000_000,
        "function": "operation",
        "line": 10,
        "module": module,
        "primitive_calls": 1,
        "self_ns": 1_000,
        "total_calls": 1,
    }


def _workload(name: str, parameters: dict[str, int], result_invariant: str) -> dict[str, object]:
    return {
        "hotspots": [_hotspot()],
        "name": name,
        "parameters": parameters,
        "primitive_calls": 1,
        "profiled_repeats": 1,
        "result_invariant": result_invariant,
        "total_calls": 1,
        "total_profiled_ns": 1_000,
        "workload_version": 1,
    }


def _document() -> dict[str, object]:
    return {
        "environment": {
            "architecture": "test64",
            "dependency_versions": {
                "glfw": "2.10.2",
                "rendercanvas": "2.7.2",
                "wgpu": "0.32.0",
            },
            "ludoweave_version": "0.1.0a1",
            "os": "TestOS",
            "os_release": "1",
            "processor": "test processor",
            "python_build_mode": "release",
            "python_gil_enabled": True,
            "python_implementation": "CPython",
            "python_threading_build": "gil",
            "python_version": "3.12.13",
            "render_capabilities": None,
        },
        "git": {"commit": "a" * 40, "dirty": True},
        "include_wgpu": False,
        "profiler": "cProfile",
        "repeats": 1,
        "schema": "ludoweave.profile.m7/1",
        "sort": "cumulative_ns_desc",
        "workloads": [
            _workload(
                "simulation_tick_10000",
                {"entity_count": 10_000, "fixed_hz": 60, "systems": 1},
                "positive total tick count",
            ),
            _workload(
                "extract_pack_10000",
                {"visible_sprites": 10_000, "packed_bytes": 640_000},
                "one draw and 10,000 visible sprites",
            ),
        ],
    }


def _validate(document: dict[str, object], tmp_path: Path) -> subprocess.CompletedProcess[str]:
    artifact = tmp_path / "m7-profile.json"
    artifact.write_text(json.dumps(document), encoding="utf-8")
    return subprocess.run(
        (sys.executable, str(_VALIDATOR), str(artifact)),
        check=False,
        capture_output=True,
        text=True,
    )


def test_m7_validator_accepts_exact_sanitized_base_profile(tmp_path: Path) -> None:
    result = _validate(_document(), tmp_path)
    assert result.returncode == 0
    assert result.stdout.strip() == (
        '{"schema":"ludoweave.profile.m7/1","valid":true,"workloads":2}'
    )


@pytest.mark.parametrize(
    "mutation",
    ["parameter", "order", "invariant", "path", "address", "sensitive", "graphics"],
)
def test_m7_validator_rejects_tampering(mutation: str, tmp_path: Path) -> None:
    document = deepcopy(_document())
    workloads = cast(list[dict[str, object]], document["workloads"])
    hotspots = cast(list[dict[str, object]], workloads[0]["hotspots"])
    if mutation == "parameter":
        cast(dict[str, object], workloads[0]["parameters"])["entity_count"] = 9_999
    elif mutation == "order":
        workloads.reverse()
    elif mutation == "invariant":
        workloads[0]["result_invariant"] = "unchecked"
    elif mutation == "path":
        hotspots[0]["module"] = "C:\\Users\\name\\engine.py"
    elif mutation == "address":
        hotspots[0]["function"] = "<object at 0x7FF00A12>"
    elif mutation == "sensitive":
        cast(dict[str, object], document["environment"])["workspace_path"] = "forbidden"
    else:
        document["include_wgpu"] = True

    result = _validate(document, tmp_path)
    assert result.returncode == 1
    failure = json.loads(result.stdout)
    assert failure["schema"] == "ludoweave.profile.m7/1"
    assert failure["valid"] is False
