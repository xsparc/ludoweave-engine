"""Strict expected document for M26 release-channel admission readiness."""

from typing import cast


def validate_supported_release_channel_evidence(
    document: dict[str, object], *, version: str
) -> None:
    """Reject M26 gate behavior, evidence, or exact JSON-type drift."""

    expected: dict[str, object] = {
        "admission": {
            "channel_identity_reviewed": True,
            "deprecation_window_feature_releases": 1,
            "historical_releases_preserved": True,
            "minimum_supported_feature_releases": 2,
            "reason_codes": ["supported-feature-release-channel-absent"],
            "supported_feature_release_channel": False,
        },
        "channel": {
            "distinct_feature_lines": 0,
            "feature_release_count": 0,
            "manifest_sha256": ("f23b4314696384ad288b86c63bc101606f1aa9f323c4fb186486d8c74915ec41"),
            "publication_channels": ["github-release"],
            "records_verified": True,
            "versions": [],
        },
        "evidence_level": "supported-release-channel-admission-readiness",
        "gate_satisfied": False,
        "ludoweave_version": version,
        "schema": "ludoweave.evaluation.supported-release-channel-readiness/1",
        "status": "not-ready",
        "supported_deprecation_release_channel_proven": False,
    }
    if not _exact_json(document, expected):
        raise RuntimeError("supported release channel readiness evidence drifted")


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
