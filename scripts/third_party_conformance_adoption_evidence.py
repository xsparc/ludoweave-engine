"""Strict expected document for M35 third-party conformance readiness."""

from typing import cast


def validate_third_party_conformance_adoption_evidence(
    document: dict[str, object], *, version: str
) -> None:
    """Reject M35 gate behavior, evidence, or exact JSON-type drift."""

    expected: dict[str, object] = {
        "admission": {
            "accepted_profile_count": 3,
            "historical_submissions_preserved": True,
            "manifest_identity_reviewed": True,
            "passing_third_party_implementation_present": False,
            "reviewed_submission_present": False,
            "reason_codes": ["third-party-conformance-evidence-absent"],
            "submission_census_complete_reviewed": True,
        },
        "evidence_level": "third-party-conformance-adoption-readiness",
        "gate_satisfied": False,
        "ludoweave_version": version,
        "metrics": {
            "failed_submission_count": 0,
            "manifest_sha256": "adee8c68b5d89923ee2682162eb24cd9542a4601b1ff6fb901709ebcc0066767",
            "measurement_policy": (
                "complete-reviewed-project-accepted-third-party-conformance-submissions/1"
            ),
            "not_executed_submission_count": 0,
            "passing_adapter_count": 0,
            "passing_by_profile": {
                "agent-tool-baseline/1": 0,
                "render-device-baseline/1": 0,
                "world-store-baseline/1": 0,
            },
            "passing_implementation_count": 0,
            "passing_plugin_adapter_count": 0,
            "records_verified": True,
            "reviewed_submission_count": 0,
        },
        "schema": "ludoweave.evaluation.third-party-conformance-adoption-readiness/1",
        "status": "not-ready",
        "third_party_conformance_adoption_proven": False,
    }
    if not _exact_json(document, expected):
        raise RuntimeError("third-party conformance readiness evidence drifted")


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
