"""Strict expected document for M34 agent-tool recovery-rate readiness."""

from typing import cast


def validate_agent_tool_recovery_rate_evidence(
    document: dict[str, object], *, version: str
) -> None:
    """Reject M34 gate behavior, evidence, or exact JSON-type drift."""

    expected: dict[str, object] = {
        "admission": {
            "complete_reviewed_windows": False,
            "historical_windows_preserved": True,
            "manifest_identity_reviewed": True,
            "terminal_call_cohort_complete": False,
            "tool_calls_present": False,
            "reason_codes": ["agent-tool-recovery-rate-evidence-absent"],
        },
        "completion_without_manual_recovery_rate_proven": False,
        "evidence_level": "agent-tool-recovery-rate-admission-readiness",
        "gate_satisfied": False,
        "ludoweave_version": version,
        "metrics": {
            "completed_after_manual_recovery_count": 0,
            "completed_without_manual_recovery_count": 0,
            "completion_without_manual_recovery_rate": None,
            "manifest_sha256": "e952c045b039055e8439069cf88176b6ac1d2ad7de49a94d39b2737e5d06e1d5",
            "manual_recovery_count": 0,
            "measurement_policy": "complete-reviewed-task-directed-agent-tool-calls/1",
            "not_completed_count": 0,
            "records_verified": True,
            "tool_call_count": 0,
            "unobserved_terminal_count": 0,
            "window_count": 0,
        },
        "schema": "ludoweave.evaluation.agent-tool-recovery-rate-readiness/1",
        "status": "not-ready",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("agent-tool recovery-rate readiness evidence drifted")


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
