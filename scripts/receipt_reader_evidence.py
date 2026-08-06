"""Strict expected document for the M21 installed receipt-reader example."""

from typing import cast


def validate_receipt_reader_evidence(document: dict[str, object], *, version: str) -> None:
    """Reject receipt-reader behavior, boundary, or JSON-type drift."""

    expected: dict[str, object] = {
        "baseline": {
            "cross_version_proven": False,
            "evidence_level": "single-version-baseline",
            "source_version": "0.1.0a1",
        },
        "cases": [
            {
                "aliases": 1,
                "diagnostic_codes": [],
                "has_changes": True,
                "mapping_round_trip": True,
                "outcomes": 1,
                "status": "committed",
                "wire_round_trip": True,
            },
            {
                "aliases": 1,
                "diagnostic_codes": [],
                "has_changes": True,
                "mapping_round_trip": True,
                "outcomes": 1,
                "status": "dry_run",
                "wire_round_trip": True,
            },
            {
                "aliases": 0,
                "diagnostic_codes": ["world.transaction.apply_failed"],
                "has_changes": False,
                "mapping_round_trip": True,
                "outcomes": 1,
                "status": "rejected",
                "wire_round_trip": True,
            },
        ],
        "failures": {
            "incompatible": "world.receipt.incompatible",
            "malformed": "world.receipt.malformed",
            "oversized": "world.receipt.oversized",
        },
        "limits": {
            "max_aliases": 1_024,
            "max_bytes": 1_048_576,
            "max_collection_items": 10_000,
            "max_depth": 32,
            "max_diagnostic_details": 64,
            "max_diagnostics": 64,
            "max_diff_records": 100_000,
            "max_nodes": 100_000,
            "max_outcomes": 1_024,
            "max_string_bytes": 262_144,
        },
        "ludoweave_version": version,
        "receipt_protocol": "ludoweave.receipt/1",
        "schema": "ludoweave.example.receipt-reader/1",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("installed receipt-reader evidence drifted")


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
