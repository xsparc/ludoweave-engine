"""Strict expected document for M20 installed command/receipt evidence."""

from typing import cast

_CHECKS = [
    "factory",
    "service_contract",
    "read_isolation",
    "snapshot_baseline",
    "transaction_validation",
    "transaction_commit",
    "stale_hash_atomicity",
    "entity_query",
    "tick_receipts",
    "snapshot_diff",
    "capture_tests_telemetry",
    "close_lifecycle",
]
_STABILITY_EXPORTS = [
    "COMMAND_PROTOCOL",
    "RECEIPT_PROTOCOL",
    "TRANSACTION_PROTOCOL",
    "CommandActor",
    "CommandEnvelope",
    "CommandOutcome",
    "CommandTransaction",
    "IncompatibleReceiptError",
    "ReceiptDiagnostic",
    "ReceiptDecodeError",
    "ReceiptLimits",
    "ReceiptStatus",
    "TransactionReceipt",
    "TransactionService",
]
_BOUNDARY: dict[str, object] = {
    "agent_conformance_checks": _CHECKS,
    "agent_conformance_passed": True,
    "agent_conformance_profile": "agent-tool-baseline/1",
    "agent_conformance_protocol": "ludoweave.agent-tool-conformance/1",
    "behavior": {
        "canonical_round_trip": True,
        "commit_consistent": True,
        "commit_status": "committed",
        "dry_run_atomic": True,
        "dry_run_status": "dry_run",
        "failed_batch_atomic": True,
        "failed_batch_code": "world.transaction.apply_failed",
        "failed_batch_status": "rejected",
        "schema_rejection_code": "world.invalid_command_schema",
        "stale_atomic": True,
        "stale_code": "world.transaction.stale_hash",
        "stale_status": "rejected",
        "unsupported_hash_algorithm_atomic": True,
        "unsupported_hash_algorithm_code": "world.hash.unsupported_algorithm",
    },
    "builtin_operations": [
        "component.add",
        "component.patch",
        "component.remove",
        "entity.destroy",
        "entity.spawn",
        "resource.patch",
        "world.tick",
    ],
    "protocols": {
        "command": "ludoweave.command/1",
        "receipt": "ludoweave.receipt/1",
        "transaction": "ludoweave.transaction/1",
    },
    "public_readers": {
        "command_envelope": True,
        "command_transaction": True,
        "transaction_receipt": True,
    },
    "receipt_fields": [
        "protocol",
        "world_id",
        "transaction_id",
        "actor",
        "status",
        "pre_hash",
        "post_hash",
        "proposed_post_hash",
        "completed_ticks_before",
        "completed_ticks_after",
        "command_outcomes",
        "changes",
        "diagnostics",
        "aliases",
    ],
    "transaction_fields": ["protocol", "world_id", "dry_run", "commands"],
    "world_stability": {name: "experimental" for name in _STABILITY_EXPORTS},
}
_GATES: dict[str, object] = {
    "cross_version_compatibility_corpus": False,
    "external_consumer_feedback": False,
    "operation_argument_compatibility_policy": True,
    "public_receipt_reader_and_bounds": True,
    "receipt_diff_diagnostic_compatibility_policy": True,
    "supported_deprecation_release_channel": False,
}


def validate_command_receipt_stability_evidence(
    document: dict[str, object], *, version: str
) -> None:
    """Reject command/receipt decision or JSON-type drift."""

    expected: dict[str, object] = {
        "current_boundary": _BOUNDARY,
        "current_boundary_confirmed": True,
        "decision": "retain-experimental-command-receipt",
        "ludoweave_version": version,
        "promotion_gates": _GATES,
        "promotion_ready": False,
        "schema": "ludoweave.evaluation.command-receipt-stability/4",
        "status": "deferred",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("command/receipt installed stability evidence drifted")


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
