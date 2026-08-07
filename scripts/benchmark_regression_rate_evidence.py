"""Strict expected document for M33 benchmark-regression-rate readiness."""

from typing import cast


def validate_benchmark_regression_rate_evidence(
    document: dict[str, object], *, version: str
) -> None:
    """Reject M33 gate behavior, evidence, or exact JSON-type drift."""

    expected: dict[str, object] = {
        "admission": {
            "benchmark_comparisons_present": False,
            "comparison_cohort_complete": False,
            "complete_reviewed_windows": False,
            "historical_windows_preserved": True,
            "manifest_identity_reviewed": True,
            "reason_codes": ["benchmark-regression-rate-evidence-absent"],
        },
        "benchmark_regression_rate_proven": False,
        "evidence_level": "benchmark-regression-rate-admission-readiness",
        "gate_satisfied": False,
        "ludoweave_version": version,
        "metrics": {
            "comparison_count": 0,
            "manifest_sha256": ("720ae794e2a4ba76303196cd43d6ba0f3b21f81cffd4fa8584f526e2a0d48dca"),
            "measurement_policy": "complete-reviewed-controlled-benchmark-comparisons/1",
            "not_executed_count": 0,
            "records_verified": True,
            "regressed_count": 0,
            "regression_rate": None,
            "stable_count": 0,
            "window_count": 0,
        },
        "schema": "ludoweave.evaluation.benchmark-regression-rate-readiness/1",
        "status": "not-ready",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("benchmark-regression-rate readiness evidence drifted")


def _exact_json(actual: object, expected: object) -> bool:
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        actual_mapping = cast(dict[object, object], actual)
        expected_mapping = cast(dict[object, object], expected)
        return actual_mapping.keys() == expected_mapping.keys() and all(
            _exact_json(actual_mapping[key], value) for key, value in expected_mapping.items()
        )
    if isinstance(expected, list):
        actual_items = cast(list[object], actual)
        expected_items = cast(list[object], expected)
        return len(actual_items) == len(expected_items) and all(
            _exact_json(actual_item, expected_item)
            for actual_item, expected_item in zip(actual_items, expected_items, strict=True)
        )
    return actual == expected
