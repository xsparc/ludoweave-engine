"""Strict expected document for M32 CI replay-divergence-rate readiness."""

from typing import cast


def validate_replay_divergence_rate_evidence(document: dict[str, object], *, version: str) -> None:
    """Reject M32 gate behavior, evidence, or exact JSON-type drift."""

    expected: dict[str, object] = {
        "admission": {
            "complete_reviewed_windows": False,
            "historical_windows_preserved": True,
            "manifest_identity_reviewed": True,
            "replay_execution_cohort_complete": False,
            "replay_executions_present": False,
            "reason_codes": ["replay-divergence-rate-evidence-absent"],
        },
        "divergence_rate_proven": False,
        "evidence_level": "ci-replay-divergence-rate-admission-readiness",
        "gate_satisfied": False,
        "ludoweave_version": version,
        "metrics": {
            "diverged_count": 0,
            "divergence_rate": None,
            "execution_count": 0,
            "manifest_sha256": "cff8a32428ac8dcd18029be4f70e9d359b4c9d70fd411ffe2f36d35704d68aa7",
            "measurement_policy": "complete-reviewed-ci-replay-executions/1",
            "not_executed_count": 0,
            "records_verified": True,
            "verified_count": 0,
            "window_count": 0,
        },
        "schema": "ludoweave.evaluation.replay-divergence-rate-readiness/1",
        "status": "not-ready",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("replay-divergence-rate readiness evidence drifted")


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
