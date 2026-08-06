"""Strict expected document for M22 installed operation-argument evidence."""

from typing import cast

_POLICY: dict[str, object] = {
    "same_identity_change": "forbidden",
    "breaking_change": "new-operation-version",
    "unknown_fields": "reject",
    "new_operation_identity": "additive",
    "deprecation": "requires-supported-feature-release-after-preview",
}
_CONTRACTS: list[dict[str, object]] = [
    {
        "operation": "component.add",
        "version": 1,
        "required": ["component", "entity"],
        "optional": [],
        "rules": ["component-payload-v1", "entity-reference-v1"],
    },
    {
        "operation": "component.patch",
        "version": 1,
        "required": ["changes", "entity", "type_id", "version"],
        "optional": [],
        "rules": [
            "entity-reference-v1",
            "canonical-registered-component-type-id",
            "current-schema-version",
            "non-empty-exact-registered-field-map",
        ],
    },
    {
        "operation": "component.remove",
        "version": 1,
        "required": ["entity", "type_id"],
        "optional": [],
        "rules": ["entity-reference-v1", "canonical-registered-component-type-id"],
    },
    {
        "operation": "entity.destroy",
        "version": 1,
        "required": ["entity"],
        "optional": [],
        "rules": ["entity-reference-v1"],
    },
    {
        "operation": "entity.spawn",
        "version": 1,
        "required": ["components"],
        "optional": ["alias"],
        "rules": [
            "bounded-stable-optional-alias",
            "component-payload-v1-array",
            "unique-component-type-ids",
        ],
    },
    {
        "operation": "resource.patch",
        "version": 1,
        "required": ["type_id", "value", "version"],
        "optional": [],
        "rules": [
            "canonical-registered-resource-type-id",
            "authoritative-state-resource-only",
            "current-schema-version",
            "registered-codec-value",
        ],
    },
    {
        "operation": "world.tick",
        "version": 1,
        "required": ["count"],
        "optional": [],
        "rules": ["exact-positive-integer-one", "transaction-safe-point"],
    },
]


def validate_operation_argument_evidence(document: dict[str, object], *, version: str) -> None:
    """Reject operation-argument evidence or exact JSON-type drift."""

    expected_contracts = [
        {
            **contract,
            "missing_required_code": "world.transaction.validation_failed",
            "missing_required_status": "rejected",
            "unexpected_field_code": "world.transaction.validation_failed",
            "unexpected_field_status": "rejected",
            "valid_status": "committed",
        }
        for contract in _CONTRACTS
    ]
    expected: dict[str, object] = {
        "command_protocol": "ludoweave.command/1",
        "contracts": expected_contracts,
        "cross_version_proven": False,
        "evidence_level": "single-version-policy-baseline",
        "gate_satisfied": True,
        "ludoweave_version": version,
        "policy": _POLICY,
        "schema": "ludoweave.evaluation.operation-argument-compatibility/1",
        "status": "pass",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("operation-argument installed compatibility evidence drifted")


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
