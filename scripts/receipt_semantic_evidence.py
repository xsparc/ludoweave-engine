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
_EXPECTED_COMPLEX_DIFF: dict[str, object] = {
    "created_entities": ["2:0"],
    "destroyed_entities": ["1:0"],
    "changed_entities": ["0:0"],
    "components_added": [
        {
            "entity": "2:0",
            "type_id": "957ef056-ce55-4658-a2aa-03221d911c6f",
            "fields": ["x", "y"],
            "before_epoch": None,
            "after_epoch": 3,
        }
    ],
    "components_removed": [
        {
            "entity": "1:0",
            "type_id": "957ef056-ce55-4658-a2aa-03221d911c6f",
            "fields": ["x", "y"],
            "before_epoch": 2,
            "after_epoch": None,
        }
    ],
    "components_changed": [
        {
            "entity": "0:0",
            "type_id": "957ef056-ce55-4658-a2aa-03221d911c6f",
            "fields": ["x"],
            "before_epoch": 1,
            "after_epoch": 4,
        }
    ],
    "resources_changed": [
        {
            "type_id": "a96920a2-c3e6-4913-885d-66ca38cb9201",
            "before_present": True,
            "after_present": True,
            "value_changed": True,
        }
    ],
    "allocator": {
        "free_before": [],
        "free_after": [1],
        "slots": [
            {
                "index": 1,
                "before_generation": 0,
                "after_generation": 1,
                "before_alive": True,
                "after_alive": False,
            },
            {
                "index": 2,
                "before_generation": None,
                "after_generation": 0,
                "before_alive": None,
                "after_alive": True,
            },
        ],
    },
    "epochs": {
        "world_before": 2,
        "world_after": 5,
        "structural_before": 2,
        "structural_after": 5,
        "tables": [
            {
                "type_id": "957ef056-ce55-4658-a2aa-03221d911c6f",
                "before": 2,
                "after": 5,
            }
        ],
    },
    "completed_ticks_before": 0,
    "completed_ticks_after": 0,
}
_DIAGNOSTIC_CODES = [
    "world.hash.unsupported_algorithm",
    "world.transaction.apply_failed",
    "world.transaction.limit_exceeded",
    "world.transaction.stale_hash",
    "world.transaction.validation_failed",
    "world.transaction.world_mismatch",
]
_DIAGNOSTIC_DEFINITIONS = [
    {
        "code": "world.hash.unsupported_algorithm",
        "meaning": "expected-world-hash-algorithm-is-not-supported",
        "scenario": "non-sha256-expected-world-hash",
    },
    {
        "code": "world.transaction.apply_failed",
        "meaning": "decoded-operation-failed-against-staged-authority",
        "scenario": "stale-entity-destroy-on-staged-authority",
    },
    {
        "code": "world.transaction.limit_exceeded",
        "meaning": "transaction-or-receipt-exceeded-configured-deterministic-limit",
        "scenario": "command-count-above-configured-limit",
    },
    {
        "code": "world.transaction.stale_hash",
        "meaning": "expected-world-hash-did-not-match-live-authority",
        "scenario": "stale-sha256-expected-world-hash",
    },
    {
        "code": "world.transaction.validation_failed",
        "meaning": "built-in-operation-arguments-failed-validation",
        "scenario": "unexpected-entity-spawn-argument",
    },
    {
        "code": "world.transaction.world_mismatch",
        "meaning": "transaction-targeted-a-different-world",
        "scenario": "transaction-world-id-mismatch",
    },
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
            "definitions": _DIAGNOSTIC_DEFINITIONS,
            "fields": ["code", "phase", "message", "details"],
            "machine_identity": "code",
            "metadata_flexible": True,
            "rules": _DIAGNOSTIC_RULES,
            "unknown_code_additive": True,
        },
        "diagnostic_cases": [
            {**definition, "status": "rejected"} for definition in _DIAGNOSTIC_DEFINITIONS
        ],
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
            "complex_diff_exact": True,
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
