"""Exercise the bounded public receipt reader without exposing world state."""

from __future__ import annotations

import json
import sys
from collections.abc import Callable, Sequence

from ludoweave import __version__
from ludoweave.ecs import ComponentRegistry, ResourceRegistry, ResourceStore, World
from ludoweave.world import (
    RECEIPT_PROTOCOL,
    CommandActor,
    CommandEnvelope,
    CommandTransaction,
    IncompatibleReceiptError,
    ReceiptDecodeError,
    ReceiptLimits,
    TransactionReceipt,
    TransactionService,
    WorldSession,
)

_SCHEMA = "ludoweave.example.receipt-reader/1"
_BASELINE_SOURCE_VERSION = "0.1.0a1"


def main(argv: Sequence[str] | None = None) -> int:
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    if arguments:
        raise SystemExit("receipt_reader accepts no arguments")
    print(json.dumps(evaluate(), ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0


def evaluate() -> dict[str, object]:
    """Return sanitized installed evidence for each receipt status and failure class."""

    committed = _apply("reader.committed", dry_run=False, rejected=False)
    dry_run = _apply("reader.dry-run", dry_run=True, rejected=False)
    rejected = _apply("reader.rejected", dry_run=False, rejected=True)
    cases = tuple(_read_case(receipt) for receipt in (committed, dry_run, rejected))

    incompatible = committed.as_dict()
    incompatible["protocol"] = "ludoweave.receipt/2"
    incompatible_code = _failure_code(lambda: TransactionReceipt.from_mapping(incompatible))

    malformed = committed.as_dict()
    del malformed["status"]
    malformed_code = _failure_code(lambda: TransactionReceipt.from_mapping(malformed))

    oversized_code = _failure_code(
        lambda: TransactionReceipt.from_mapping(
            committed.as_dict(), limits=ReceiptLimits(max_diff_records=1)
        )
    )
    limits = ReceiptLimits()
    report: dict[str, object] = {
        "baseline": {
            "cross_version_proven": False,
            "evidence_level": "single-version-baseline",
            "source_version": _BASELINE_SOURCE_VERSION,
        },
        "cases": cases,
        "failures": {
            "incompatible": incompatible_code,
            "malformed": malformed_code,
            "oversized": oversized_code,
        },
        "limits": {
            "max_aliases": limits.max_aliases,
            "max_bytes": limits.max_bytes,
            "max_collection_items": limits.max_collection_items,
            "max_depth": limits.max_depth,
            "max_diagnostic_details": limits.max_diagnostic_details,
            "max_diagnostics": limits.max_diagnostics,
            "max_diff_records": limits.max_diff_records,
            "max_nodes": limits.max_nodes,
            "max_outcomes": limits.max_outcomes,
            "max_string_bytes": limits.max_string_bytes,
        },
        "ludoweave_version": __version__,
        "receipt_protocol": RECEIPT_PROTOCOL,
        "schema": _SCHEMA,
    }
    if incompatible_code != "world.receipt.incompatible":
        raise AssertionError("receipt reader did not reject an incompatible protocol")
    if malformed_code != "world.receipt.malformed":
        raise AssertionError("receipt reader did not reject a malformed receipt")
    if oversized_code != "world.receipt.oversized":
        raise AssertionError("receipt reader did not enforce semantic limits")
    return report


def _apply(transaction_id: str, *, dry_run: bool, rejected: bool) -> TransactionReceipt:
    session = WorldSession(
        "receipt-reader-example",
        World(ComponentRegistry()),
        ResourceStore(ResourceRegistry()),
    )
    actor = CommandActor("example", "receipt-reader")
    operation = "entity.destroy" if rejected else "entity.spawn"
    arguments: dict[str, object] = (
        {"entity": {"index": 999, "generation": 0}}
        if rejected
        else {"alias": "created", "components": []}
    )
    command = CommandEnvelope(
        command_id=f"{transaction_id}.command",
        transaction_id=transaction_id,
        actor=actor,
        operation=operation,
        arguments=arguments,
        expected_world_hash=session.state_hash,
    )
    return TransactionService(session).apply(
        CommandTransaction((command,), session.world_id, dry_run=dry_run)
    )


def _read_case(receipt: TransactionReceipt) -> dict[str, object]:
    from_mapping = TransactionReceipt.from_mapping(receipt.as_dict())
    from_json = TransactionReceipt.from_json(receipt.canonical_bytes())
    return {
        "aliases": len(from_json.aliases),
        "diagnostic_codes": tuple(item.code for item in from_json.diagnostics),
        "has_changes": from_json.changes is not None,
        "mapping_round_trip": from_mapping == receipt,
        "outcomes": len(from_json.command_outcomes),
        "status": from_json.status.value,
        "wire_round_trip": from_json.canonical_bytes() == receipt.canonical_bytes(),
    }


def _failure_code(operation: Callable[[], object]) -> str:
    try:
        operation()
    except (IncompatibleReceiptError, ReceiptDecodeError) as error:
        return error.code
    raise AssertionError("receipt reader unexpectedly accepted invalid evidence")


if __name__ == "__main__":
    raise SystemExit(main())
