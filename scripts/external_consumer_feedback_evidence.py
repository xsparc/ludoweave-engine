"""Strict expected document for M25 external-feedback admission readiness."""

from typing import cast


def validate_external_consumer_feedback_evidence(
    document: dict[str, object], *, version: str
) -> None:
    """Reject M25 gate behavior, evidence, or exact JSON-type drift."""

    expected: dict[str, object] = {
        "admission": {
            "corpus_identity_reviewed": True,
            "historical_records_preserved": True,
            "independent_consumer_feedback": False,
            "minimum_independent_consumers": 1,
            "reason_codes": ["external-consumer-feedback-absent"],
        },
        "corpus": {
            "distinct_consumers": 0,
            "feedback_count": 0,
            "manifest_sha256": ("b113444f60946461ec6774e2c278b9e82e7d80e08a37450b6cc153e5c5c1500e"),
            "observed_ludoweave_versions": [],
            "outcomes": [],
            "records_verified": True,
            "required_protocols": [
                "ludoweave.command/1",
                "ludoweave.transaction/1",
                "ludoweave.receipt/1",
            ],
        },
        "evidence_level": "external-consumer-feedback-admission-readiness",
        "external_feedback_proven": False,
        "gate_satisfied": False,
        "ludoweave_version": version,
        "schema": "ludoweave.evaluation.external-consumer-feedback-readiness/1",
        "status": "not-ready",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("external consumer feedback readiness evidence drifted")


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
