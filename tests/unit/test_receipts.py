"""Structured transaction receipt and exact semantic-diff tests."""

from dataclasses import dataclass, replace
from uuid import UUID

from ludoweave.ecs import ComponentRegistry, ResourceRegistry, ResourceStore, World, component
from ludoweave.world import (
    CommandActor,
    CommandEnvelope,
    CommandTransaction,
    ReceiptStatus,
    TransactionService,
    WorldSession,
    canonical_loads,
)

POSITION_ID = UUID("111e4a30-8866-48c7-9730-f001428a2e89")


@component(type_id=POSITION_ID)
@dataclass(slots=True)
class Position:
    x: float
    y: float


def _session(world: World | None = None) -> WorldSession:
    selected = World(ComponentRegistry((Position,))) if world is None else world
    return WorldSession("receipt-world", selected, ResourceStore(ResourceRegistry()))


def _transaction(
    operations: list[tuple[str, dict[str, object]]],
    *,
    dry_run: bool = False,
    expected_hash: str | None = None,
) -> CommandTransaction:
    actor = CommandActor("human", "maintainer")
    return CommandTransaction(
        commands=tuple(
            CommandEnvelope(
                command_id=f"receipt-command-{index}",
                transaction_id="receipt-transaction",
                actor=actor,
                operation=operation,
                arguments=arguments,
                expected_world_hash=expected_hash,
            )
            for index, (operation, arguments) in enumerate(operations)
        ),
        world_id="receipt-world",
        dry_run=dry_run,
    )


def _payload(x: float, y: float) -> dict[str, object]:
    return {
        "type_id": str(POSITION_ID),
        "version": 1,
        "values": {"x": x, "y": y},
    }


def _id(index: int, generation: int = 0) -> dict[str, object]:
    return {"index": index, "generation": generation}


def test_receipt_lists_exact_created_destroyed_and_changed_entities() -> None:
    world = World(ComponentRegistry((Position,)))
    changed_entity = world.spawn(Position(1.0, 2.0))
    destroyed_entity = world.spawn(Position(8.0, 9.0))
    session = _session(world)
    receipt = TransactionService(session).apply(
        _transaction(
            [
                (
                    "entity.spawn",
                    {"alias": "created", "components": [_payload(4.0, 5.0)]},
                ),
                (
                    "component.patch",
                    {
                        "entity": _id(changed_entity.index),
                        "type_id": str(POSITION_ID),
                        "version": 1,
                        "changes": {"x": 3.0},
                    },
                ),
                ("entity.destroy", {"entity": _id(destroyed_entity.index)}),
            ],
            expected_hash=session.state_hash,
        )
    )

    assert receipt.status is ReceiptStatus.COMMITTED
    assert receipt.changes is not None
    assert receipt.changes.created_entities == ("2:0",)
    assert receipt.changes.destroyed_entities == ("1:0",)
    assert receipt.changes.changed_entities == ("0:0",)
    assert tuple(
        (item.entity, item.type_id, item.fields) for item in receipt.changes.components_added
    ) == (("2:0", str(POSITION_ID), ("x", "y")),)
    assert tuple(
        (item.entity, item.type_id, item.fields) for item in receipt.changes.components_removed
    ) == (("1:0", str(POSITION_ID), ("x", "y")),)
    assert tuple(
        (item.entity, item.type_id, item.fields) for item in receipt.changes.components_changed
    ) == (("0:0", str(POSITION_ID), ("x",)),)
    assert receipt.changes.allocator.changed
    assert receipt.changes.epochs.changed
    assert receipt.aliases == (("created", "2:0"),)
    assert receipt.diagnostics == ()


def test_same_value_and_reverted_writes_report_epoch_change_without_false_field_change() -> None:
    world = World(ComponentRegistry((Position,)))
    entity = world.spawn(Position(1.0, -0.0))
    session = _session(world)
    receipt = TransactionService(session).apply(
        _transaction(
            [
                (
                    "component.patch",
                    {
                        "entity": _id(entity.index),
                        "type_id": str(POSITION_ID),
                        "version": 1,
                        "changes": {"x": 2.0},
                    },
                ),
                (
                    "component.patch",
                    {
                        "entity": _id(entity.index),
                        "type_id": str(POSITION_ID),
                        "version": 1,
                        "changes": {"x": 1.0},
                    },
                ),
            ]
        )
    )

    assert receipt.changes is not None
    assert receipt.changes.changed_entities == ("0:0",)
    assert len(receipt.changes.components_changed) == 1
    change = receipt.changes.components_changed[0]
    assert change.fields == ()
    assert change.before_epoch == 1
    assert change.after_epoch == 3
    assert receipt.pre_hash != receipt.post_hash


def test_spawn_then_destroy_is_net_empty_but_allocator_and_command_audit_remain() -> None:
    session = _session()
    receipt = TransactionService(session).apply(
        _transaction(
            [
                ("entity.spawn", {"alias": "temporary", "components": []}),
                ("entity.destroy", {"entity": {"alias": "temporary"}}),
            ]
        )
    )

    assert receipt.changes is not None
    assert receipt.changes.created_entities == ()
    assert receipt.changes.destroyed_entities == ()
    assert receipt.changes.components_added == ()
    assert receipt.changes.components_removed == ()
    assert receipt.changes.allocator.changed
    assert receipt.changes.allocator.free_after == (0,)
    assert tuple(item.status for item in receipt.command_outcomes) == (
        ReceiptStatus.COMMITTED,
        ReceiptStatus.COMMITTED,
    )


def test_dry_run_receipt_has_actual_and_proposed_hashes_and_matches_commit_diff() -> None:
    session = _session()
    transaction = _transaction(
        [("entity.spawn", {"alias": "preview", "components": [_payload(-0.0, 1.0)]})],
        dry_run=True,
        expected_hash=session.state_hash,
    )
    service = TransactionService(session)

    preview = service.apply(transaction)
    committed = service.apply(replace(transaction, dry_run=False))

    assert preview.status is ReceiptStatus.DRY_RUN
    assert preview.post_hash == preview.pre_hash
    assert preview.proposed_post_hash == committed.post_hash
    assert preview.changes == committed.changes
    assert preview.aliases == committed.aliases


def test_rejected_receipt_is_canonical_sanitized_and_never_describes_partial_changes() -> None:
    session = _session()
    transaction = _transaction(
        [
            ("entity.spawn", {"alias": "discarded", "components": []}),
            ("entity.destroy", {"entity": _id(900)}),
        ]
    )
    receipt = TransactionService(session).apply(transaction)

    assert receipt.status is ReceiptStatus.REJECTED
    assert receipt.pre_hash == receipt.post_hash
    assert receipt.proposed_post_hash is None
    assert receipt.changes is None
    assert receipt.aliases == ()
    assert tuple(item.status for item in receipt.command_outcomes) == (
        ReceiptStatus.REJECTED,
        ReceiptStatus.REJECTED,
    )
    assert receipt.diagnostics[0].code == "world.transaction.apply_failed"
    assert "900" not in receipt.diagnostics[0].message
    assert canonical_loads(receipt.canonical_bytes()) == receipt.as_dict()
    assert receipt.canonical_bytes() == receipt.canonical_bytes()
    assert session.world.entities() == ()
