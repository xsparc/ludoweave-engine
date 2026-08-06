"""Prove the installed receipt semantic-diff and diagnostic policy."""

import json
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import cast
from uuid import UUID

from ludoweave import __version__
from ludoweave.core import LudoWeaveError
from ludoweave.ecs import (
    ComponentRegistry,
    ResourceRegistry,
    ResourceSpec,
    ResourceStore,
    World,
    component,
)
from ludoweave.world import (
    RECEIPT_PROTOCOL,
    AuthorityResourceRegistry,
    AuthorityResourceSchema,
    CommandActor,
    CommandEnvelope,
    CommandTransaction,
    ReceiptStatus,
    TransactionLimits,
    TransactionReceipt,
    TransactionService,
    WorldSession,
)
from ludoweave.world.canonical import JsonValue

_SCHEMA = "ludoweave.evaluation.receipt-semantic-compatibility/1"
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
_DIFF_FIELDS = (
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
)
_RECORDS = {
    "component_change": ("entity", "type_id", "fields", "before_epoch", "after_epoch"),
    "resource_change": ("type_id", "before_present", "after_present", "value_changed"),
    "allocator": ("free_before", "free_after", "slots"),
    "allocator_slot": (
        "index",
        "before_generation",
        "after_generation",
        "before_alive",
        "after_alive",
    ),
    "epochs": (
        "world_before",
        "world_after",
        "structural_before",
        "structural_after",
        "tables",
    ),
    "table_epoch": ("type_id", "before", "after"),
}
_ORDERING_RULES = (
    "entity-identities-numeric-index-generation",
    "component-records-entity-then-type-id",
    "component-field-names-lexicographic",
    "resource-records-type-id-lexicographic",
    "allocator-slots-index-ascending",
    "epoch-tables-type-id-lexicographic",
)
_SEMANTIC_RULES = (
    "net-authoritative-before-after-change",
    "created-and-destroyed-excluded-from-changed-entities",
    "same-or-reverted-writes-may-report-epoch-change-without-value-fields",
    "dry-run-diff-equals-equivalent-commit-diff",
    "rejected-receipt-exposes-no-partial-diff",
    "component-and-resource-values-never-exposed",
)
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
_DIAGNOSTIC_CODES = (
    "world.hash.unsupported_algorithm",
    "world.transaction.apply_failed",
    "world.transaction.limit_exceeded",
    "world.transaction.stale_hash",
    "world.transaction.validation_failed",
    "world.transaction.world_mismatch",
)
_DIAGNOSTIC_DEFINITIONS = (
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
)
_DIAGNOSTIC_RULES = (
    "rejected-status-remains-authoritative",
    "code-is-dotted-stable-identifier",
    "unknown-well-formed-code-is-readable",
    "message-is-not-for-machine-parsing",
    "phase-is-advisory",
    "details-accept-sanitized-scalar-extension-keys",
)

_POSITION_ID = UUID("957ef056-ce55-4658-a2aa-03221d911c6f")
_SCORE_ID = UUID("a96920a2-c3e6-4913-885d-66ca38cb9201")


@component(type_id=_POSITION_ID)
@dataclass(slots=True)
class _Position:
    x: float
    y: float


_SCORE = ResourceSpec("receipt-policy.score", int, int)


def _decode_score(value: JsonValue) -> int:
    if type(value) is not int:
        raise ValueError("score must be an integer")
    return value


_SCORE_SCHEMA = AuthorityResourceSchema(
    type_id=_SCORE_ID,
    version=1,
    spec=_SCORE,
    codec_id="receipt-policy.score/int-v1",
    encoder=int,
    decoder=_decode_score,
)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    if arguments:
        raise SystemExit("receipt_semantic_compatibility accepts no arguments")
    print(json.dumps(evaluate(), ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0


def evaluate() -> dict[str, object]:
    """Return exact sanitized evidence for the repository compatibility policy."""

    committed = _complex_receipt(dry_run=False)
    dry_run = _complex_receipt(dry_run=True)
    rejected = _rejection("world.transaction.apply_failed")
    if committed.changes is None or dry_run.changes is None or rejected.changes is not None:
        raise AssertionError("receipt change presence no longer matches status")
    change = committed.changes.as_dict()
    records = _actual_records(change)
    diagnostic_cases = tuple(
        {
            **definition,
            "status": _rejection(definition["code"]).status.value,
        }
        for definition in _DIAGNOSTIC_DEFINITIONS
    )
    complex_diff_exact = change == _EXPECTED_COMPLEX_DIFF
    metadata_flexible, unknown_code_additive = _diagnostic_evolution(rejected)
    fail_closed = _fail_closed(committed)
    report: dict[str, object] = {
        "cross_version_proven": False,
        "diagnostic_contract": {
            "current_emitted_codes": _DIAGNOSTIC_CODES,
            "definitions": _DIAGNOSTIC_DEFINITIONS,
            "fields": tuple(rejected.diagnostics[0].as_dict()),
            "machine_identity": "code",
            "metadata_flexible": metadata_flexible,
            "rules": _DIAGNOSTIC_RULES,
            "unknown_code_additive": unknown_code_additive,
        },
        "diagnostic_cases": diagnostic_cases,
        "evidence_level": "single-version-policy-baseline",
        "gate_satisfied": True,
        "ludoweave_version": __version__,
        "policy": _POLICY,
        "reader_fail_closed": fail_closed,
        "receipt_protocol": RECEIPT_PROTOCOL,
        "schema": _SCHEMA,
        "semantic_diff_contract": {
            "complex_diff_exact": complex_diff_exact,
            "dry_run_matches_commit": dry_run.changes == committed.changes,
            "fields": tuple(change),
            "ordering_rules": _ORDERING_RULES,
            "presence_by_status": {
                "committed": "required",
                "dry_run": "required",
                "rejected": "null",
            },
            "records": records,
            "semantic_rules": _SEMANTIC_RULES,
        },
        "status": "pass",
    }
    if tuple(change) != _DIFF_FIELDS or records != _RECORDS:
        raise AssertionError("installed semantic diff no longer matches the frozen field policy")
    if not complex_diff_exact:
        raise AssertionError("installed semantic diff no longer matches the exact frozen semantics")
    if tuple(item["code"] for item in _DIAGNOSTIC_DEFINITIONS) != _DIAGNOSTIC_CODES:
        raise AssertionError("diagnostic definitions no longer cover the frozen code identities")
    if tuple(item["code"] for item in diagnostic_cases) != _DIAGNOSTIC_CODES:
        raise AssertionError("installed diagnostic codes no longer match the frozen policy")
    if not metadata_flexible or not unknown_code_additive:
        raise AssertionError("installed receipt reader no longer supports diagnostic evolution")
    if dry_run.changes != committed.changes:
        raise AssertionError("equivalent dry-run and commit semantic diffs diverged")
    return report


def _session(*, complex_state: bool) -> WorldSession:
    if not complex_state:
        return WorldSession(
            "receipt-policy-world",
            World(ComponentRegistry()),
            ResourceStore(ResourceRegistry()),
        )
    world = World(ComponentRegistry((_Position,)))
    world.spawn(_Position(1.0, 2.0))
    world.spawn(_Position(8.0, 9.0))
    resources = ResourceStore(ResourceRegistry((_SCORE,)), ((_SCORE, 3),))
    return WorldSession(
        "receipt-policy-world",
        world,
        resources,
        authority_resources=AuthorityResourceRegistry((_SCORE_SCHEMA,)),
    )


def _complex_receipt(*, dry_run: bool) -> TransactionReceipt:
    session = _session(complex_state=True)
    actor = CommandActor("evidence", "receipt-policy")
    transaction_id = "receipt-policy.complex"
    commands = (
        _command(
            actor,
            transaction_id,
            0,
            "entity.spawn",
            {
                "alias": "created",
                "components": [
                    {
                        "type_id": str(_POSITION_ID),
                        "version": 1,
                        "values": {"x": 4.0, "y": 5.0},
                    }
                ],
            },
            session.state_hash,
        ),
        _command(
            actor,
            transaction_id,
            1,
            "component.patch",
            {
                "entity": {"index": 0, "generation": 0},
                "type_id": str(_POSITION_ID),
                "version": 1,
                "changes": {"x": 3.0},
            },
            session.state_hash,
        ),
        _command(
            actor,
            transaction_id,
            2,
            "entity.destroy",
            {"entity": {"index": 1, "generation": 0}},
            session.state_hash,
        ),
        _command(
            actor,
            transaction_id,
            3,
            "resource.patch",
            {"type_id": str(_SCORE_ID), "version": 1, "value": 7},
            session.state_hash,
        ),
    )
    return TransactionService(session).apply(
        CommandTransaction(commands, session.world_id, dry_run=dry_run)
    )


def _rejection(code: str) -> TransactionReceipt:
    session = _session(complex_state=False)
    actor = CommandActor("evidence", "receipt-policy")
    transaction_id = f"receipt-policy.{code.rsplit('.', 1)[-1]}"
    expected_hash: str | None = session.state_hash
    world_id = session.world_id
    operation = "entity.spawn"
    arguments: dict[str, object] = {"components": []}
    limits: TransactionLimits | None = None
    count = 1
    if code == "world.hash.unsupported_algorithm":
        expected_hash = "blake3:" + "0" * 64
    elif code == "world.transaction.apply_failed":
        operation = "entity.destroy"
        arguments = {"entity": {"index": 999, "generation": 0}}
    elif code == "world.transaction.limit_exceeded":
        limits = TransactionLimits(max_commands=1)
        count = 2
    elif code == "world.transaction.stale_hash":
        expected_hash = "sha256:" + "0" * 64
    elif code == "world.transaction.validation_failed":
        arguments = {"components": [], "unexpected": True}
    elif code == "world.transaction.world_mismatch":
        world_id = "receipt-policy-other-world"
    else:
        raise AssertionError(f"unrecognized policy code {code}")
    commands = tuple(
        _command(actor, transaction_id, index, operation, arguments, expected_hash)
        for index in range(count)
    )
    receipt = TransactionService(session, limits=limits).apply(
        CommandTransaction(commands, world_id)
    )
    if (
        receipt.status is not ReceiptStatus.REJECTED
        or len(receipt.diagnostics) != 1
        or receipt.diagnostics[0].code != code
    ):
        raise AssertionError(f"expected installed rejection code {code}")
    return receipt


def _command(
    actor: CommandActor,
    transaction_id: str,
    index: int,
    operation: str,
    arguments: dict[str, object],
    expected_hash: str | None,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=f"{transaction_id}.command-{index}",
        transaction_id=transaction_id,
        actor=actor,
        operation=operation,
        arguments=arguments,
        expected_world_hash=expected_hash,
    )


def _actual_records(change: dict[str, JsonValue]) -> dict[str, tuple[str, ...]]:
    components_added = cast(list[dict[str, JsonValue]], change["components_added"])
    components_removed = cast(list[dict[str, JsonValue]], change["components_removed"])
    components_changed = cast(list[dict[str, JsonValue]], change["components_changed"])
    resources_changed = cast(list[dict[str, JsonValue]], change["resources_changed"])
    allocator = cast(dict[str, JsonValue], change["allocator"])
    slots = cast(list[dict[str, JsonValue]], allocator["slots"])
    epochs = cast(dict[str, JsonValue], change["epochs"])
    tables = cast(list[dict[str, JsonValue]], epochs["tables"])
    records = {
        "component_change": tuple(components_added[0]),
        "resource_change": tuple(resources_changed[0]),
        "allocator": tuple(allocator),
        "allocator_slot": tuple(slots[0]),
        "epochs": tuple(epochs),
        "table_epoch": tuple(tables[0]),
    }
    component_order = records["component_change"]
    if any(
        tuple(item) != component_order
        for item in (*components_added, *components_removed, *components_changed)
    ):
        raise AssertionError("installed component diff record ordering drifted")
    return records


def _diagnostic_evolution(receipt: TransactionReceipt) -> tuple[bool, bool]:
    metadata = cast(dict[str, object], receipt.as_dict())
    metadata_items = cast(list[dict[str, object]], metadata["diagnostics"])
    metadata_items[0]["phase"] = None
    metadata_items[0]["message"] = "updated human-readable diagnostic"
    metadata_items[0]["details"] = {"future_hint": True}
    decoded_metadata = TransactionReceipt.from_mapping(metadata)
    metadata_flexible = decoded_metadata.diagnostics[0].code == receipt.diagnostics[0].code

    unknown = cast(dict[str, object], receipt.as_dict())
    unknown_items = cast(list[dict[str, object]], unknown["diagnostics"])
    unknown_items[0]["code"] = "world.future.added"
    decoded_unknown = TransactionReceipt.from_mapping(unknown)
    unknown_additive = (
        decoded_unknown.status is ReceiptStatus.REJECTED
        and decoded_unknown.diagnostics[0].code == "world.future.added"
    )
    return metadata_flexible, unknown_additive


def _fail_closed(receipt: TransactionReceipt) -> dict[str, str]:
    incompatible = receipt.as_dict()
    incompatible["protocol"] = "ludoweave.receipt/2"
    unknown = receipt.as_dict()
    cast(dict[str, object], unknown["changes"])["unexpected"] = True
    missing = receipt.as_dict()
    del cast(dict[str, object], missing["changes"])["created_entities"]
    return {
        "incompatible_protocol": _failure_code(
            lambda: TransactionReceipt.from_mapping(incompatible)
        ),
        "missing_diff_field": _failure_code(lambda: TransactionReceipt.from_mapping(missing)),
        "unknown_diff_field": _failure_code(lambda: TransactionReceipt.from_mapping(unknown)),
    }


def _failure_code(operation: Callable[[], object]) -> str:
    try:
        operation()
    except LudoWeaveError as error:
        return error.code
    raise AssertionError("receipt reader unexpectedly accepted incompatible evidence")


if __name__ == "__main__":
    raise SystemExit(main())
