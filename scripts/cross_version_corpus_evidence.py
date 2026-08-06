"""Strict expected document for M24 cross-version corpus readiness."""

from typing import cast


def validate_cross_version_corpus_evidence(document: dict[str, object], *, version: str) -> None:
    """Reject admission behavior, evidence, or exact JSON-type drift."""

    expected: dict[str, object] = {
        "admission": {
            "corpus_identity_reviewed": True,
            "cross_version_execution": False,
            "minimum_distinct_observed_versions": 2,
            "reader_differs_from_source": False,
            "reason_codes": [
                "cross-version-execution-absent",
                "supported-release-evidence-incomplete",
            ],
            "supported_release_evidence_complete": False,
        },
        "corpus": {
            "canonical_round_trip": True,
            "distinct_observed_versions": 1,
            "fixture_count": 3,
            "manifest_sha256": ("0b1d7b9f68b49ad1f6ab21cff4f744140cf3a16b52c6cdebd691b28b375a72ae"),
            "manifests_verified": True,
            "observed_versions": ["0.1.0a1"],
            "source_versions": ["0.1.0a1"],
            "statuses": ["committed", "dry_run", "rejected"],
        },
        "cross_version_proven": False,
        "evidence_level": "single-version-admission-readiness",
        "gate_satisfied": False,
        "ludoweave_version": version,
        "receipt_protocol": "ludoweave.receipt/1",
        "schema": "ludoweave.evaluation.cross-version-receipt-corpus/1",
        "status": "not-ready",
        "supported_release_versions": [],
    }
    if not _exact_json(document, expected):
        raise RuntimeError("cross-version corpus installed readiness evidence drifted")


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
