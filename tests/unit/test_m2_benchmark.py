"""M2 informational benchmark schema and tamper validation."""

from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

import pytest

_ROOT = Path(__file__).parents[2]


class _RunBenchmarks(Protocol):
    def __call__(self, *, samples: int, warmups: int, seed: int) -> dict[str, object]: ...


class _Validate(Protocol):
    def __call__(self, document: object) -> int: ...


def _load_module(name: str, path: Path) -> ModuleType:
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load test module {name}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_BENCHMARK = _load_module("ludoweave_test_benchmark_m2", _ROOT / "benchmarks/benchmark_m2.py")
_VALIDATOR = _load_module(
    "ludoweave_test_validate_m2",
    _ROOT / "benchmarks/validate_m2_results.py",
)
run_benchmarks = cast(_RunBenchmarks, _BENCHMARK.run_benchmarks)
validate = cast(_Validate, _VALIDATOR.validate)


def test_minimal_m2_benchmark_records_raw_time_and_memory_without_targets() -> None:
    result = run_benchmarks(samples=1, warmups=0, seed=7)

    assert validate(result) == 4
    assert result["seed"] == 7
    workloads = cast(list[dict[str, object]], result["workloads"])
    assert all(item["target"] is None for item in workloads)
    assert all(len(cast(list[object], item["durations_ns"])) == 1 for item in workloads)
    assert all(len(cast(list[object], item["peak_bytes"])) == 1 for item in workloads)


def test_m2_benchmark_validator_rejects_tampered_distribution_and_sensitive_metadata() -> None:
    result = run_benchmarks(samples=1, warmups=0, seed=1)
    tampered = deepcopy(result)
    workloads = cast(list[dict[str, object]], tampered["workloads"])
    workloads[0]["p95_ns"] = cast(int, workloads[0]["p95_ns"]) + 1
    with pytest.raises(ValueError, match="inconsistent"):
        validate(tampered)

    sensitive = deepcopy(result)
    environment = cast(dict[str, object], sensitive["environment"])
    environment["workspace_path"] = "forbidden"
    with pytest.raises(ValueError):
        validate(sensitive)
