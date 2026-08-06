"""Strict expected document for M23 installed receipt-semantic evidence."""

from typing import cast

_POLICY: dict[str, object] = {
    "same_protocol_breaking_change": "forbidden",
    "breaking_change": "new-receipt-protocol",
    "unknown_receipt_fields": "reject",
    "semantic_meaning_change": "new-receipt-protocol",
    "diagnostic_code_meaning": "stable",
    "new_diagnostic_code": "additive",
    "unknown_diagnostic_code": "status-preserving-fallback",
    "diagnostic_phase": "advisory-non-contractual",
    "diagnostic_message": "human-readable-non-contractual",
    "diagnostic_details": "sanitized-scalar-extension-map",
    "deprecation": "requires-supported-feature-release-after-preview",
}
_DIFF_FIELDS = [
    "created_entities",
    "destroyed_entities",
    "changed_entities",
    "components_added",
    "components_removed",
    "components_changed",
    "resources_changed",
    "allocator",
    "epochs",
    "completed_ticks_before",
    "completed_ticks_after",
]
_RECORDS = {
    "component_change": ["entity", "type_id", "fields", "before_epoch", "after_epoch"],
    "resource_change": ["type_id", "before_present", "after_present", "value_changed"],
    "allocator": ["free_before", "free_after", "slots"],
    "allocator_slot": [
        "index",
        "before_generation",
        "after_generation",
        "before_alive",
        "after_alive",
    ],
    "epochs": [
        "world_before",
        "world_after",
        "structural_before",
        "structural_after",
        "tables",
    ],
    "table_epoch": ["type_id", "before", "after"],
}
_ORDERING_RULES = [
    "entity-identities-numeric-index-generation",
    "component-records-entity-then-type-id",
    "component-field-names-lexicographic",
    "resource-records-type-id-lexicographic",
    "allocator-slots-index-ascending",
    "epoch-tables-type-id-lexicographic",
]
_SEMANTIC_RULES = [
    "net-authoritative-before-after-change",
    "created-and-destroyed-excluded-from-changed-entities",
    "same-or-reverted-writes-may-report-epoch-change-without-value-fields",
    "dry-run-diff-equals-equivalent-commit-diff",
    "rejected-receipt-exposes-no-partial-diff",
    "component-and-resource-values-never-exposed",
]
_DIAGNOSTIC_CODES = [
    "world.hash.unsupported_algorithm",
    "world.transaction.apply_failed",
    "world.transaction.limit_exceeded",
    "world.transaction.stale_hash",
    "world.transaction.validation_failed",
    "world.transaction.world_mismatch",
]
_DIAGNOSTIC_RULES = [
    "rejected-status-remains-authoritative",
    "code-is-dotted-stable-identifier",
    "unknown-well-formed-code-is-readable",
    "message-is-not-for-machine-parsing",
    "phase-is-advisory",
    "details-accept-sanitized-scalar-extension-keys",
]


def validate_receipt_semantic_evidence(document: dict[str, object], *, version: str) -> None:
    """Reject receipt-semantic evidence or exact JSON-type drift."""

    expected: dict[str, object] = {
        "cross_version_proven": False,
        "diagnostic_contract": {
            "current_emitted_codes": _DIAGNOSTIC_CODES,
            "fields": ["code", "phase", "message", "details"],
            "machine_identity": "code",
            "metadata_flexible": True,
            "rules": _DIAGNOSTIC_RULES,
            "unknown_code_additive": True,
        },
        "diagnostic_cases": [{"code": code, "status": "rejected"} for code in _DIAGNOSTIC_CODES],
        "evidence_level": "single-version-policy-baseline",
        "gate_satisfied": True,
        "ludoweave_version": version,
        "policy": _POLICY,
        "reader_fail_closed": {
            "incompatible_protocol": "world.receipt.incompatible",
            "missing_diff_field": "world.receipt.malformed",
            "unknown_diff_field": "world.receipt.malformed",
        },
        "receipt_protocol": "ludoweave.receipt/1",
        "schema": "ludoweave.evaluation.receipt-semantic-compatibility/1",
        "semantic_diff_contract": {
            "dry_run_matches_commit": True,
            "fields": _DIFF_FIELDS,
            "ordering_rules": _ORDERING_RULES,
            "presence_by_status": {
                "committed": "required",
                "dry_run": "required",
                "rejected": "null",
            },
            "records": _RECORDS,
            "semantic_rules": _SEMANTIC_RULES,
        },
        "status": "pass",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("receipt semantic installed compatibility evidence drifted")


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
