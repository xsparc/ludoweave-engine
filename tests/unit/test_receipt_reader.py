"""Bounded public receipt decoding and semantic-invariant tests."""

import json
from copy import deepcopy
from dataclasses import dataclass
from typing import cast
from uuid import UUID

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.ecs import (
    ComponentRegistry,
    ResourceRegistry,
    ResourceSpec,
    ResourceStore,
    World,
    component,
)
from ludoweave.world import (
    AuthorityResourceRegistry,
    AuthorityResourceSchema,
    CommandActor,
    CommandEnvelope,
    CommandTransaction,
    IncompatibleReceiptError,
    ReceiptDecodeError,
    ReceiptLimits,
    ReceiptStatus,
    TransactionReceipt,
    TransactionService,
    WorldSession,
    canonical_loads,
)
from ludoweave.world.canonical import JsonValue

POSITION_ID = UUID("957ef056-ce55-4658-a2aa-03221d911c6f")
SCORE_ID = UUID("a96920a2-c3e6-4913-885d-66ca38cb9201")


@component(type_id=POSITION_ID)
@dataclass(slots=True)
class Position:
    x: float
    y: float


SCORE = ResourceSpec("reader.score", int, int)


def _decode_score(value: JsonValue) -> int:
    if type(value) is not int:
        raise ValueError("score must be an integer")
    return value


SCORE_SCHEMA = AuthorityResourceSchema(
    type_id=SCORE_ID,
    version=1,
    spec=SCORE,
    codec_id="reader.score/int-v1",
    encoder=int,
    decoder=_decode_score,
)


def _session() -> tuple[WorldSession, str, str]:
    world = World(ComponentRegistry((Position,)))
    changed = world.spawn(Position(1.0, 2.0))
    destroyed = world.spawn(Position(8.0, 9.0))
    resources = ResourceStore(ResourceRegistry((SCORE,)), ((SCORE, 3),))
    session = WorldSession(
        "reader-world",
        world,
        resources,
        authority_resources=AuthorityResourceRegistry((SCORE_SCHEMA,)),
    )
    return (
        session,
        f"{changed.index}:{changed.generation}",
        f"{destroyed.index}:{destroyed.generation}",
    )


def _payload(x: float, y: float) -> dict[str, object]:
    return {
        "type_id": str(POSITION_ID),
        "version": 1,
        "values": {"x": x, "y": y},
    }


def _transaction(
    session: WorldSession,
    operations: list[tuple[str, dict[str, object]]],
    *,
    transaction_id: str,
    dry_run: bool = False,
) -> CommandTransaction:
    actor = CommandActor("reader", "fixture")
    return CommandTransaction(
        tuple(
            CommandEnvelope(
                command_id=f"{transaction_id}.command-{index}",
                transaction_id=transaction_id,
                actor=actor,
                operation=operation,
                arguments=arguments,
                expected_world_hash=session.state_hash,
            )
            for index, (operation, arguments) in enumerate(operations)
        ),
        session.world_id,
        dry_run=dry_run,
    )


def _successful_receipt(*, dry_run: bool) -> TransactionReceipt:
    session, changed, destroyed = _session()
    transaction = _transaction(
        session,
        [
            (
                "entity.spawn",
                {"alias": "created", "components": [_payload(4.0, 5.0)]},
            ),
            (
                "component.patch",
                {
                    "entity": _entity_mapping(changed),
                    "type_id": str(POSITION_ID),
                    "version": 1,
                    "changes": {"x": 3.0},
                },
            ),
            ("entity.destroy", {"entity": _entity_mapping(destroyed)}),
            (
                "resource.patch",
                {"type_id": str(SCORE_ID), "version": 1, "value": 7},
            ),
        ],
        transaction_id="reader.success",
        dry_run=dry_run,
    )
    return TransactionService(session).apply(transaction)


def _rejected_receipt() -> TransactionReceipt:
    session, _, _ = _session()
    transaction = _transaction(
        session,
        [("entity.destroy", {"entity": {"index": 999, "generation": 0}})],
        transaction_id="reader.rejected",
    )
    return TransactionService(session).apply(transaction)


def _entity_mapping(value: str) -> dict[str, int]:
    index, generation = value.split(":", 1)
    return {"index": int(index), "generation": int(generation)}


@pytest.mark.parametrize(
    "receipt",
    [
        pytest.param(_successful_receipt(dry_run=False), id="committed"),
        pytest.param(_successful_receipt(dry_run=True), id="dry-run"),
        pytest.param(_rejected_receipt(), id="rejected"),
    ],
)
def test_receipt_reader_round_trips_every_status(receipt: TransactionReceipt) -> None:
    from_mapping = TransactionReceipt.from_mapping(receipt.as_dict())
    from_json = TransactionReceipt.from_json(receipt.canonical_bytes())

    assert from_mapping == receipt
    assert from_json == receipt
    assert from_json.canonical_bytes() == receipt.canonical_bytes()


def test_receipt_reader_detaches_mutable_input() -> None:
    receipt = _successful_receipt(dry_run=False)
    document = receipt.as_dict()
    decoded = TransactionReceipt.from_mapping(document)

    cast(dict[str, object], document)["status"] = "rejected"
    cast(list[object], document["command_outcomes"]).clear()

    assert decoded == receipt


def test_complex_receipt_exercises_every_semantic_change_family() -> None:
    decoded = TransactionReceipt.from_json(_successful_receipt(dry_run=False).canonical_bytes())

    assert decoded.status is ReceiptStatus.COMMITTED
    assert decoded.changes is not None
    assert len(decoded.changes.components_added) == 1
    assert len(decoded.changes.components_removed) == 1
    assert len(decoded.changes.components_changed) == 1
    assert len(decoded.changes.resources_changed) == 1
    assert decoded.changes.allocator.changed
    assert decoded.changes.epochs.changed


def test_receipt_reader_rejects_incompatible_protocol() -> None:
    document = _successful_receipt(dry_run=False).as_dict()
    document["protocol"] = "ludoweave.receipt/2"

    with pytest.raises(IncompatibleReceiptError) as caught:
        TransactionReceipt.from_mapping(document)

    assert caught.value.code == "world.receipt.incompatible"
    assert caught.value.phase == "compatibility"
    assert dict(caught.value.details) == {"field": "protocol"}


@pytest.mark.parametrize(
    ("mutation", "field"),
    [
        ("unexpected", "receipt"),
        ("outcome_status", "command_outcomes.status"),
        ("invalid_hash", "pre_hash"),
        ("duplicate_alias", "aliases.alias"),
        ("overlap_entity", "changes.entities"),
        ("backward_epoch", "epochs"),
        ("missing_changes", "status"),
    ],
)
def test_receipt_reader_rejects_schema_and_semantic_drift(mutation: str, field: str) -> None:
    document = cast(dict[str, object], _successful_receipt(dry_run=False).as_dict())
    changes = cast(dict[str, object], document["changes"])
    if mutation == "unexpected":
        document["unexpected"] = True
    elif mutation == "outcome_status":
        outcomes = cast(list[dict[str, object]], document["command_outcomes"])
        outcomes[0]["status"] = "rejected"
    elif mutation == "invalid_hash":
        document["pre_hash"] = "sha256:0"
    elif mutation == "duplicate_alias":
        aliases = cast(list[dict[str, object]], document["aliases"])
        aliases.append(deepcopy(aliases[0]))
    elif mutation == "overlap_entity":
        changes["changed_entities"] = deepcopy(changes["created_entities"])
    elif mutation == "backward_epoch":
        epochs = cast(dict[str, object], changes["epochs"])
        epochs["world_after"] = 0
    else:
        document["changes"] = None

    with pytest.raises(ReceiptDecodeError) as caught:
        TransactionReceipt.from_mapping(document)

    assert caught.value.code == "world.receipt.malformed"
    assert dict(caught.value.details).get("field", dict(caught.value.details).get("role")) == field


def test_rejected_receipt_status_invariants_are_enforced() -> None:
    document = _rejected_receipt().as_dict()
    document["aliases"] = [{"alias": "leak", "entity": "0:0"}]

    with pytest.raises(ReceiptDecodeError, match="status invariants"):
        TransactionReceipt.from_mapping(document)


def test_reader_limits_apply_to_json_and_nested_semantics() -> None:
    receipt = _successful_receipt(dry_run=False)

    with pytest.raises(ReceiptDecodeError) as bytes_error:
        TransactionReceipt.from_json(receipt.canonical_bytes(), limits=ReceiptLimits(max_bytes=32))
    assert bytes_error.value.code == "world.receipt.oversized"
    assert dict(bytes_error.value.details) == {
        "actual": len(receipt.canonical_bytes()),
        "cause_code": "world.invalid_canonical_json",
        "field": "json.decode",
        "limit": 32,
    }
    assert bytes_error.value.__cause__ is not None

    with pytest.raises(ReceiptDecodeError) as mapping_bytes_error:
        TransactionReceipt.from_mapping(receipt.as_dict(), limits=ReceiptLimits(max_bytes=32))
    assert mapping_bytes_error.value.code == "world.receipt.oversized"
    assert dict(mapping_bytes_error.value.details)["field"] == "json.encode"
    assert mapping_bytes_error.value.__cause__ is not None

    with pytest.raises(ReceiptDecodeError) as outcome_error:
        TransactionReceipt.from_mapping(receipt.as_dict(), limits=ReceiptLimits(max_outcomes=1))
    assert outcome_error.value.code == "world.receipt.oversized"
    assert dict(outcome_error.value.details)["field"] == "command_outcomes"

    with pytest.raises(ReceiptDecodeError) as diff_error:
        TransactionReceipt.from_mapping(receipt.as_dict(), limits=ReceiptLimits(max_diff_records=1))
    assert diff_error.value.code == "world.receipt.oversized"
    assert dict(diff_error.value.details)["field"] == "changes.records"


@given(value=st.integers(max_value=0))
def test_receipt_limits_reject_non_positive_integers(value: int) -> None:
    with pytest.raises(ReceiptDecodeError) as caught:
        ReceiptLimits(max_outcomes=value)

    assert caught.value.code == "world.receipt.invalid_limits"
    assert dict(caught.value.details)["field"] == "max_outcomes"


@pytest.mark.parametrize("value", [True, 1.0, "1"])
def test_receipt_limits_reject_non_integer_types(value: object) -> None:
    with pytest.raises(ReceiptDecodeError):
        ReceiptLimits(max_aliases=cast(int, value))


def test_reader_rejects_duplicate_json_keys_and_preserves_cause() -> None:
    receipt = _successful_receipt(dry_run=False)
    text = receipt.canonical_bytes().decode("utf-8")
    malformed = text.replace(
        '"protocol":"ludoweave.receipt/1"',
        '"protocol":"ludoweave.receipt/1","protocol":"ludoweave.receipt/1"',
        1,
    )

    with pytest.raises(ReceiptDecodeError) as caught:
        TransactionReceipt.from_json(malformed)

    assert caught.value.code == "world.receipt.malformed"
    assert dict(caught.value.details) == {"cause_code": "world.invalid_canonical_json"}
    assert caught.value.__cause__ is not None


def test_reader_rejects_huge_entity_identity_as_structured_error() -> None:
    document = _successful_receipt(dry_run=False).as_dict()
    aliases = cast(list[dict[str, object]], document["aliases"])
    aliases[0]["entity"] = f"{'9' * 5_000}:0"

    with pytest.raises(ReceiptDecodeError) as caught:
        TransactionReceipt.from_mapping(document)

    assert caught.value.code == "world.receipt.malformed"
    assert dict(caught.value.details)["field"] == "alias.entity"


def test_reader_requires_exact_nested_diff_fields_and_forward_component_epoch() -> None:
    missing = _successful_receipt(dry_run=False).as_dict()
    missing_changes = cast(dict[str, object], missing["changes"])
    missing_allocator = cast(dict[str, object], missing_changes["allocator"])
    del missing_allocator["slots"]

    with pytest.raises(ReceiptDecodeError) as missing_error:
        TransactionReceipt.from_mapping(missing)
    assert dict(missing_error.value.details)["role"] == "changes.allocator"

    stationary = _successful_receipt(dry_run=False).as_dict()
    stationary_changes = cast(dict[str, object], stationary["changes"])
    changed = cast(list[dict[str, object]], stationary_changes["components_changed"])
    changed[0]["after_epoch"] = changed[0]["before_epoch"]

    with pytest.raises(ReceiptDecodeError) as epoch_error:
        TransactionReceipt.from_mapping(stationary)
    assert dict(epoch_error.value.details)["field"] == "component_changed.epochs"


def test_reader_accepts_noncanonical_json_and_emits_canonical_bytes() -> None:
    receipt = _successful_receipt(dry_run=False)
    document = cast(dict[str, object], canonical_loads(receipt.canonical_bytes()))
    noncanonical = json.dumps(document, indent=2, ensure_ascii=True)

    decoded = TransactionReceipt.from_json(noncanonical)

    assert decoded == receipt
    assert decoded.canonical_bytes() == receipt.canonical_bytes()
