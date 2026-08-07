"""Strict expected document for M29 contributor-retention readiness."""

from typing import cast


def validate_external_contributor_retention_evidence(
    document: dict[str, object], *, version: str
) -> None:
    """Reject M29 gate behavior, evidence, or exact JSON-type drift."""

    expected: dict[str, object] = {
        "admission": {
            "historical_retention_preserved": True,
            "manifest_identity_reviewed": True,
            "minimum_retained_contributors": 1,
            "reason_codes": ["retained-external-contributor-absent"],
            "retained_external_contributor_present": False,
        },
        "contributor_retention_proven": False,
        "evidence_level": "external-contributor-retention-admission-readiness",
        "gate_satisfied": False,
        "ludoweave_version": version,
        "retention": {
            "manifest_sha256": "61785ec165e9f9a7c1025c37f7b714d6fa42b2c7081145a0f843395a325b36ee",
            "records_verified": True,
            "retained_contributor_count": 0,
            "return_contribution_count": 0,
            "task_scopes": [],
            "validation_steps": ["clean-setup", "focused-check", "complete-gate"],
        },
        "schema": "ludoweave.evaluation.external-contributor-retention-readiness/1",
        "status": "not-ready",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("external contributor-retention readiness evidence drifted")


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
