"""Strict expected document for M27 contributor-rehearsal readiness."""

from typing import cast


def validate_external_contributor_rehearsal_evidence(
    document: dict[str, object], *, version: str
) -> None:
    """Reject M27 gate behavior, evidence, or exact JSON-type drift."""

    expected: dict[str, object] = {
        "admission": {
            "documentation_without_private_knowledge_proven": False,
            "historical_rehearsals_preserved": True,
            "independent_contributor_rehearsal_present": False,
            "manifest_identity_reviewed": True,
            "minimum_merged_rehearsals": 1,
            "reason_codes": ["external-contributor-rehearsal-absent"],
        },
        "evidence_level": "external-contributor-rehearsal-admission-readiness",
        "first_external_contribution_proven": False,
        "gate_satisfied": False,
        "ludoweave_version": version,
        "rehearsals": {
            "manifest_sha256": ("ecb959e90a0033b4dbe3dcfe8a48db1c1eea915e0ef2840510969b9e25cdb9c7"),
            "record_count": 0,
            "records_verified": True,
            "task_scopes": [],
            "validation_steps": ["clean-setup", "focused-check", "complete-gate"],
        },
        "schema": "ludoweave.evaluation.external-contributor-rehearsal-readiness/1",
        "status": "not-ready",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("external contributor rehearsal evidence drifted")


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
