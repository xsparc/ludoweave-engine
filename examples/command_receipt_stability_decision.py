"""Report installed command/receipt facts and the M20 stability decision."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from dataclasses import replace

from ludoweave import __version__
from ludoweave.agent import (
    AGENT_TOOL_CONFORMANCE_PROFILE,
    AGENT_TOOL_CONFORMANCE_PROTOCOL,
    AgentCapture,
    run_agent_tool_conformance,
)
from ludoweave.ecs import ComponentRegistry, ResourceRegistry, ResourceStore, World
from ludoweave.samples import create_agent_world_builder
from ludoweave.world import (
    BUILTIN_OPERATION_SPECS,
    COMMAND_PROTOCOL,
    RECEIPT_PROTOCOL,
    TRANSACTION_PROTOCOL,
    CommandActor,
    CommandEnvelope,
    CommandSchemaError,
    CommandTransaction,
    ReceiptLimits,
    ReceiptStatus,
    TransactionReceipt,
    TransactionService,
    WorldSession,
)
from ludoweave.world import __stability__ as world_stability

_SCHEMA = "ludoweave.evaluation.command-receipt-stability/2"
_STABILITY_EXPORTS = (
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
)
_PROMOTION_GATES = (
    "cross_version_compatibility_corpus",
    "external_consumer_feedback",
    "operation_argument_compatibility_policy",
    "public_receipt_reader_and_bounds",
    "receipt_diff_diagnostic_compatibility_policy",
    "supported_deprecation_release_channel",
)


class _Capture:
    """Deterministic provider-neutral capture for the installed evidence composition."""

    __slots__ = ()

    def capture(self, width: int, height: int) -> AgentCapture:
        return AgentCapture(width, height, b"\x12\x34\x56\xff" * (width * height))

    def close(self) -> None:
        pass


def main(argv: Sequence[str] | None = None) -> int:
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    if arguments:
        raise SystemExit("command_receipt_stability_decision accepts no arguments")
    print(json.dumps(evaluate(), ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0


def evaluate() -> dict[str, object]:
    """Return bounded installed evidence and the resulting stability decision."""

    session = WorldSession(
        "command-receipt-evidence",
        World(ComponentRegistry()),
        ResourceStore(ResourceRegistry()),
    )
    service = TransactionService(session)
    actor = CommandActor("maintainer", "stability-evidence")
    initial_hash = session.state_hash
    transaction = _spawn_transaction(
        actor,
        transaction_id="stability.create",
        command_id="stability.create.spawn",
        expected_hash=initial_hash,
    )
    decoded = CommandTransaction.from_json(transaction.canonical_bytes())
    canonical_round_trip = decoded.canonical_bytes() == transaction.canonical_bytes()
    schema_rejection_code = _schema_rejection_code(transaction)

    dry_run = service.apply(replace(transaction, dry_run=True))
    dry_run_atomic = (
        dry_run.status is ReceiptStatus.DRY_RUN
        and dry_run.pre_hash == initial_hash
        and dry_run.post_hash == initial_hash
        and dry_run.proposed_post_hash is not None
        and dry_run.proposed_post_hash != initial_hash
        and session.state_hash == initial_hash
    )
    committed = service.apply(transaction)
    committed_hash = session.state_hash
    commit_consistent = (
        committed.status is ReceiptStatus.COMMITTED
        and committed.pre_hash == initial_hash
        and committed.post_hash == committed_hash
        and committed.post_hash != committed.pre_hash
        and committed.changes is not None
        and committed.changes.created_entities == ("0:0",)
    )

    stale = service.apply(
        _spawn_transaction(
            actor,
            transaction_id="stability.stale",
            command_id="stability.stale.spawn",
            expected_hash=initial_hash,
        )
    )
    stale_atomic = (
        stale.status is ReceiptStatus.REJECTED
        and stale.pre_hash == committed_hash
        and stale.post_hash == committed_hash
        and stale.changes is None
        and session.state_hash == committed_hash
    )

    unsupported = service.apply(
        _spawn_transaction(
            actor,
            transaction_id="stability.algorithm",
            command_id="stability.algorithm.spawn",
            expected_hash="blake3:" + "0" * 64,
        )
    )
    unsupported_atomic = (
        unsupported.status is ReceiptStatus.REJECTED
        and unsupported.pre_hash == committed_hash
        and unsupported.post_hash == committed_hash
        and unsupported.changes is None
        and session.state_hash == committed_hash
    )

    failed_batch = service.apply(_failed_batch(actor, expected_hash=committed_hash))
    failed_batch_atomic = (
        failed_batch.status is ReceiptStatus.REJECTED
        and failed_batch.pre_hash == committed_hash
        and failed_batch.post_hash == committed_hash
        and failed_batch.changes is None
        and failed_batch.aliases == ()
        and session.state_hash == committed_hash
    )

    agent_report = run_agent_tool_conformance(
        "org.ludoweave.command-receipt-evidence",
        lambda: create_agent_world_builder(write=True, capture_provider=_Capture()).service,
    )
    behavior = {
        "canonical_round_trip": canonical_round_trip,
        "commit_consistent": commit_consistent,
        "commit_status": committed.status.value,
        "dry_run_atomic": dry_run_atomic,
        "dry_run_status": dry_run.status.value,
        "failed_batch_atomic": failed_batch_atomic,
        "failed_batch_code": _diagnostic_code(failed_batch),
        "failed_batch_status": failed_batch.status.value,
        "schema_rejection_code": schema_rejection_code,
        "stale_atomic": stale_atomic,
        "stale_code": _diagnostic_code(stale),
        "stale_status": stale.status.value,
        "unsupported_hash_algorithm_atomic": unsupported_atomic,
        "unsupported_hash_algorithm_code": _diagnostic_code(unsupported),
    }
    readers = {
        "command_envelope": hasattr(CommandEnvelope, "from_mapping"),
        "command_transaction": hasattr(CommandTransaction, "from_mapping"),
        "transaction_receipt": hasattr(TransactionReceipt, "from_mapping"),
    }
    stability = {name: world_stability[name] for name in _STABILITY_EXPORTS}
    current_boundary = {
        "agent_conformance_checks": tuple(check.check_id for check in agent_report.checks),
        "agent_conformance_passed": agent_report.passed,
        "agent_conformance_profile": AGENT_TOOL_CONFORMANCE_PROFILE,
        "agent_conformance_protocol": AGENT_TOOL_CONFORMANCE_PROTOCOL,
        "behavior": behavior,
        "builtin_operations": tuple(spec.operation for spec in BUILTIN_OPERATION_SPECS),
        "protocols": {
            "command": COMMAND_PROTOCOL,
            "receipt": RECEIPT_PROTOCOL,
            "transaction": TRANSACTION_PROTOCOL,
        },
        "public_readers": readers,
        "receipt_fields": tuple(committed.as_dict()),
        "transaction_fields": tuple(transaction.as_dict()),
        "world_stability": stability,
    }
    current_boundary_confirmed = (
        all(value is True for value in behavior.values() if type(value) is bool)
        and agent_report.passed
        and all(value == "experimental" for value in stability.values())
        and readers
        == {
            "command_envelope": True,
            "command_transaction": True,
            "transaction_receipt": True,
        }
        and ReceiptLimits().max_outcomes == 1_024
    )
    if not current_boundary_confirmed:
        raise AssertionError("M20 evidence no longer confirms the command/receipt boundary")

    promotion_gates = {
        name: name == "public_receipt_reader_and_bounds" for name in _PROMOTION_GATES
    }
    promotion_ready = all(promotion_gates.values())
    if promotion_ready:
        raise AssertionError("M20 evidence unexpectedly satisfies every preview promotion gate")
    return {
        "current_boundary": current_boundary,
        "current_boundary_confirmed": current_boundary_confirmed,
        "decision": "retain-experimental-command-receipt",
        "ludoweave_version": __version__,
        "promotion_gates": promotion_gates,
        "promotion_ready": promotion_ready,
        "schema": _SCHEMA,
        "status": "deferred",
    }


def _spawn_transaction(
    actor: CommandActor,
    *,
    transaction_id: str,
    command_id: str,
    expected_hash: str,
) -> CommandTransaction:
    return CommandTransaction(
        (
            CommandEnvelope(
                command_id=command_id,
                transaction_id=transaction_id,
                actor=actor,
                operation="entity.spawn",
                arguments={"components": []},
                expected_world_hash=expected_hash,
            ),
        ),
        "command-receipt-evidence",
    )


def _failed_batch(actor: CommandActor, *, expected_hash: str) -> CommandTransaction:
    transaction_id = "stability.failed-batch"
    return CommandTransaction(
        (
            CommandEnvelope(
                command_id=f"{transaction_id}.spawn",
                transaction_id=transaction_id,
                actor=actor,
                operation="entity.spawn",
                arguments={"alias": "discarded", "components": []},
                expected_world_hash=expected_hash,
            ),
            CommandEnvelope(
                command_id=f"{transaction_id}.destroy",
                transaction_id=transaction_id,
                actor=actor,
                operation="entity.destroy",
                arguments={"entity": {"index": 999, "generation": 0}},
                expected_world_hash=expected_hash,
            ),
        ),
        "command-receipt-evidence",
    )


def _schema_rejection_code(transaction: CommandTransaction) -> str:
    document = transaction.as_dict()
    document["unexpected"] = True
    try:
        CommandTransaction.from_mapping(document)
    except CommandSchemaError as error:
        return error.code
    raise AssertionError("command transaction unexpectedly accepted an unknown field")


def _diagnostic_code(receipt: TransactionReceipt) -> str:
    if len(receipt.diagnostics) != 1:
        raise AssertionError("rejected receipt did not contain one diagnostic")
    return receipt.diagnostics[0].code


if __name__ == "__main__":
    raise SystemExit(main())
