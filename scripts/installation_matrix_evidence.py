"""Strict expected document for M30 clean-install matrix readiness."""

from typing import cast


def validate_installation_matrix_evidence(document: dict[str, object], *, version: str) -> None:
    """Reject M30 gate behavior, evidence, or exact JSON-type drift."""

    expected: dict[str, object] = {
        "admission": {
            "complete_environment_matrix": False,
            "historical_matrix_preserved": True,
            "immutable_release_artifact": False,
            "isolated_clean_install": False,
            "manifest_identity_reviewed": True,
            "reason_codes": ["installation-matrix-evidence-absent"],
        },
        "evidence_level": "installation-matrix-admission-readiness",
        "gate_satisfied": False,
        "installation": {
            "environments": [],
            "manifest_sha256": ("7c05813a7304e8ff44a009ada37c8e60ff545baec633852fc332e46bdfe03c90"),
            "records_verified": True,
            "release_versions": [],
            "required_checks": [
                "version",
                "doctor",
                "hello-headless",
                "clockwork-arena-headless",
            ],
            "required_environment_count": 7,
            "successful_environment_count": 0,
        },
        "installation_matrix_proven": False,
        "ludoweave_version": version,
        "schema": "ludoweave.evaluation.installation-matrix-readiness/1",
        "status": "not-ready",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("installation-matrix readiness evidence drifted")


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
