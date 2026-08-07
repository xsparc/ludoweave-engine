"""Strict expected document for M31 response/review-latency readiness."""

from typing import cast


def validate_response_review_latency_evidence(document: dict[str, object], *, version: str) -> None:
    """Reject M31 gate behavior, evidence, or exact JSON-type drift."""

    expected: dict[str, object] = {
        "admission": {
            "complete_reviewed_windows": False,
            "historical_windows_preserved": True,
            "issue_response_measurements_present": False,
            "manifest_identity_reviewed": True,
            "pull_request_review_measurements_present": False,
            "reason_codes": ["response-review-latency-evidence-absent"],
        },
        "evidence_level": "response-review-latency-admission-readiness",
        "gate_satisfied": False,
        "latency_measurement_proven": False,
        "ludoweave_version": version,
        "metrics": {
            "issue_response": {
                "eligible_count": 0,
                "median_seconds": None,
                "observed_count": 0,
                "p95_seconds": None,
                "pending_count": 0,
            },
            "manifest_sha256": ("bc40bbcc1636229fa2c78aed5f71854d1221fd3c0d33169edc1321dd07e69d4f"),
            "measurement_policy": "first-public-human-maintainer-action/1",
            "pull_request_review": {
                "eligible_count": 0,
                "median_seconds": None,
                "observed_count": 0,
                "p95_seconds": None,
                "pending_count": 0,
            },
            "records_verified": True,
            "window_count": 0,
        },
        "schema": "ludoweave.evaluation.response-review-latency-readiness/1",
        "status": "not-ready",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("response-review-latency readiness evidence drifted")


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
