"""Strict expected document for M28 external sample-game adoption readiness."""

from typing import cast


def validate_external_sample_game_adoption_evidence(
    document: dict[str, object], *, version: str
) -> None:
    """Reject M28 gate behavior, evidence, or exact JSON-type drift."""

    expected: dict[str, object] = {
        "admission": {
            "external_sample_game_present": False,
            "historical_sample_games_preserved": True,
            "manifest_identity_reviewed": True,
            "minimum_external_sample_games": 1,
            "reason_codes": ["external-sample-game-absent"],
        },
        "evidence_level": "external-sample-game-adoption-readiness",
        "external_sample_game_adoption_proven": False,
        "gate_satisfied": False,
        "ludoweave_version": version,
        "sample_games": {
            "distinct_authors": 0,
            "game_count": 0,
            "manifest_sha256": ("ecdd0be75e42f047037c6799205786079274eb6d73d788f81e1061acc82008dd"),
            "observed_ludoweave_versions": [],
            "outcomes": [],
            "records_verified": True,
            "required_capabilities": [
                "headless-fixed-tick",
                "typed-command-receipt",
                "verified-replay",
            ],
            "sample_scopes": [],
        },
        "schema": "ludoweave.evaluation.external-sample-game-adoption-readiness/1",
        "status": "not-ready",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("external sample-game adoption readiness evidence drifted")


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
