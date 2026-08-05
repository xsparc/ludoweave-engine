"""Atomic persistent transaction validation, staging, and rollback tests."""

import threading
from dataclasses import dataclass, replace
from uuid import UUID

import pytest

from ludoweave.ecs import (
    ComponentRegistry,
    ReferenceWorld,
    ResourceRegistry,
    ResourceSpec,
    ResourceStore,
    World,
    WorldStore,
    component,
)
from ludoweave.world import (
    AuthorityError,
    AuthorityResourceRegistry,
    AuthorityResourceSchema,
    CommandActor,
    CommandEnvelope,
    CommandTransaction,
    OperationRegistry,
    OperationSpec,
    RandomStreams,
    ReceiptStatus,
    ResourceRole,
    TickExecutor,
    TransactionLimits,
    TransactionService,
    WorldSession,
)
from ludoweave.world.canonical import JsonValue


@component(type_id=UUID("91619a10-e096-4bb1-8e47-3ce84bd219aa"))
@dataclass(slots=True)
class Position:
    x: float
    y: float


@component(type_id=UUID("06797031-77f0-4b54-a056-4259c6627600"))
@dataclass(slots=True)
class Health:
    value: int


SCORE = ResourceSpec("game.score", int, int)
SCORE_TYPE_ID = UUID("c16a2451-0f09-4207-badd-37ade4739c9f")


def _encode_score(value: int) -> object:
    return value


def _decode_score(value: JsonValue) -> int:
    if type(value) is not int:
        raise ValueError("score must be an integer")
    return value


SCORE_SCHEMA = AuthorityResourceSchema(
    type_id=SCORE_TYPE_ID,
    version=1,
    spec=SCORE,
    codec_id="game.score/int-v1",
    encoder=_encode_score,
    decoder=_decode_score,
)


def _session(
    *,
    world: WorldStore | None = None,
    score: int = 0,
    tick_executor: TickExecutor | None = None,
) -> WorldSession:
    registry = ComponentRegistry((Position, Health))
    selected_world = World(registry) if world is None else world
    resources = ResourceStore(ResourceRegistry((SCORE,)), ((SCORE, score),))
    return WorldSession(
        "arena",
        selected_world,
        resources,
        authority_resources=AuthorityResourceRegistry((SCORE_SCHEMA,)),
        tick_executor=tick_executor,
    )


def _transaction(
    session: WorldSession,
    operations: list[tuple[str, dict[str, object]]],
    *,
    transaction_id: str = "tx-1",
    expected_hash: str | None = None,
    dry_run: bool = False,
) -> CommandTransaction:
    actor = CommandActor("test", "suite")
    commands = tuple(
        CommandEnvelope(
            command_id=f"cmd-{index}",
            transaction_id=transaction_id,
            actor=actor,
            operation=operation,
            arguments=arguments,
            expected_world_hash=expected_hash,
        )
        for index, (operation, arguments) in enumerate(operations)
    )
    return CommandTransaction(commands=commands, world_id=session.world_id, dry_run=dry_run)


def _component_payload(
    component_type: type[object], values: dict[str, object]
) -> dict[str, object]:
    schema = ComponentRegistry((component_type,)).schema_for_type(component_type)
    return {"type_id": str(schema.type_id), "version": schema.version, "values": values}


def _alias(name: str) -> dict[str, object]:
    return {"alias": name}


def _entity(index: int, generation: int) -> dict[str, object]:
    return {"index": index, "generation": generation}


def test_valid_entity_component_transaction_commits_one_staged_record() -> None:
    session = _session()
    old_world = session.world
    transaction = _transaction(
        session,
        [
            (
                "entity.spawn",
                {
                    "alias": "player",
                    "components": [_component_payload(Position, {"x": 1.0, "y": 2.0})],
                },
            ),
            (
                "component.add",
                {
                    "entity": _alias("player"),
                    "component": _component_payload(Health, {"value": 10}),
                },
            ),
            (
                "component.patch",
                {
                    "entity": _alias("player"),
                    "type_id": str(UUID("91619a10-e096-4bb1-8e47-3ce84bd219aa")),
                    "version": 1,
                    "changes": {"x": -0.0},
                },
            ),
            (
                "component.remove",
                {
                    "entity": _alias("player"),
                    "type_id": str(UUID("06797031-77f0-4b54-a056-4259c6627600")),
                },
            ),
        ],
        expected_hash=session.state_hash,
    )

    result = TransactionService(session).apply(transaction)

    assert result.status is ReceiptStatus.COMMITTED
    assert result.pre_hash != result.post_hash == session.state_hash
    assert old_world.entities() == ()
    player = session.world.entities()[0]
    assert result.aliases == (("player", f"{player.index}:{player.generation}"),)
    assert session.world.entities() == (player,)
    assert session.world.get(player, Position) == Position(-0.0, 2.0)
    assert not session.world.has(player, Health)


def test_failed_middle_operation_leaves_live_hash_pointer_and_allocator_unchanged() -> None:
    session = _session()
    service = TransactionService(session)
    before_world = session.world
    before_document = session.authority_document()
    before_hash = session.state_hash
    transaction = _transaction(
        session,
        [
            ("entity.spawn", {"alias": "temporary", "components": []}),
            ("entity.destroy", {"entity": _entity(999, 0)}),
            ("entity.spawn", {"alias": "never", "components": []}),
        ],
        expected_hash=before_hash,
    )

    raised = service.apply(transaction)

    assert raised.status is ReceiptStatus.REJECTED
    assert raised.diagnostics[0].details == (
        ("cause_code", "ecs.stale_entity"),
        ("command_id", "cmd-1"),
        ("operation_index", 1),
    )
    assert session.world.entities() == before_world.entities()
    assert session.state_hash == before_hash
    assert session.authority_document() == before_document
    committed = service.apply(
        _transaction(session, [("entity.spawn", {"alias": "first", "components": []})])
    )
    first = session.world.entities()[0]
    assert committed.aliases == (("first", f"{first.index}:{first.generation}"),)
    assert first.index == 0


def test_stale_hash_rejects_before_resource_decoder_or_staging() -> None:
    calls = 0

    def decode(value: JsonValue) -> int:
        nonlocal calls
        calls += 1
        return _decode_score(value)

    schema = AuthorityResourceSchema(
        type_id=SCORE_TYPE_ID,
        version=1,
        spec=SCORE,
        codec_id="game.score/counting-v1",
        encoder=_encode_score,
        decoder=decode,
    )
    resources = ResourceStore(ResourceRegistry((SCORE,)), ((SCORE, 0),))
    session = WorldSession(
        "arena",
        World(ComponentRegistry((Position, Health))),
        resources,
        authority_resources=AuthorityResourceRegistry((schema,)),
    )
    transaction = _transaction(
        session,
        [
            (
                "resource.patch",
                {"type_id": str(SCORE_TYPE_ID), "version": 1, "value": 9},
            )
        ],
        expected_hash="sha256:" + "0" * 64,
    )

    rejected = TransactionService(session).apply(transaction)

    assert rejected.status is ReceiptStatus.REJECTED
    assert rejected.diagnostics[0].code == "world.transaction.stale_hash"
    assert calls == 0
    assert session.resources.require(SCORE) == 0


def test_dry_run_predicts_commit_without_adopting_state() -> None:
    session = _session()
    service = TransactionService(session)
    before_world = session.world
    before_hash = session.state_hash
    transaction = _transaction(
        session,
        [("entity.spawn", {"alias": "preview", "components": []})],
        expected_hash=before_hash,
        dry_run=True,
    )

    preview = service.apply(transaction)

    assert preview.status is ReceiptStatus.DRY_RUN
    assert preview.post_hash == preview.pre_hash
    assert preview.proposed_post_hash != preview.pre_hash
    assert session.world.entities() == before_world.entities()
    assert session.state_hash == before_hash
    assert session.world.entities() == ()

    committed = service.apply(replace(transaction, dry_run=False))
    assert committed.post_hash == preview.proposed_post_hash
    assert committed.aliases == preview.aliases


def test_resource_patch_is_staged_and_rolls_back_with_later_failure() -> None:
    session = _session(score=3)
    before_hash = session.state_hash
    transaction = _transaction(
        session,
        [
            (
                "resource.patch",
                {"type_id": str(SCORE_TYPE_ID), "version": 1, "value": 7},
            ),
            ("entity.destroy", {"entity": _entity(50, 0)}),
        ],
    )

    rejected = TransactionService(session).apply(transaction)

    assert rejected.status is ReceiptStatus.REJECTED
    assert session.resources.require(SCORE) == 3
    assert session.state_hash == before_hash


class _ScoreTickExecutor:
    def __init__(self, fail_at: int | None = None) -> None:
        self.fail_at = fail_at

    def execute_tick(
        self,
        world: WorldStore,
        resources: ResourceStore,
        random_streams: RandomStreams,
        tick: int,
    ) -> None:
        del world, random_streams
        resources.replace(SCORE, resources.require(SCORE) + 1)
        if self.fail_at == tick:
            raise RuntimeError("tick failed with a private message")


def test_tick_executor_runs_only_on_staged_resources_and_commits_ticks() -> None:
    session = _session(tick_executor=_ScoreTickExecutor())
    result = TransactionService(session).apply(
        _transaction(session, [("world.tick", {"count": 1})])
    )

    assert result.completed_ticks_before == 0
    assert result.completed_ticks_after == 1
    assert result.changes is not None
    assert result.changes.completed_ticks_before == 0
    assert result.changes.completed_ticks_after == 1
    assert result.changes.resources_changed[0].type_id == str(SCORE_TYPE_ID)
    assert session.completed_ticks == 1
    assert session.resources.require(SCORE) == 1


def test_tick_failure_discards_all_staged_tick_mutation_and_private_message() -> None:
    session = _session(score=2, tick_executor=_ScoreTickExecutor(fail_at=0))
    before_hash = session.state_hash

    raised = TransactionService(session).apply(
        _transaction(session, [("world.tick", {"count": 1})])
    )

    assert raised.status is ReceiptStatus.REJECTED
    assert "private message" not in str(raised)
    assert session.completed_ticks == 0
    assert session.resources.require(SCORE) == 2
    assert session.state_hash == before_hash


class _InterruptingTickExecutor:
    def execute_tick(
        self,
        world: WorldStore,
        resources: ResourceStore,
        random_streams: RandomStreams,
        tick: int,
    ) -> None:
        del world, random_streams, tick
        resources.replace(SCORE, 99)
        raise KeyboardInterrupt


def test_base_exception_from_staged_tick_propagates_without_adoption() -> None:
    session = _session(score=4, tick_executor=_InterruptingTickExecutor())
    before_world = session.world
    before_hash = session.state_hash

    with pytest.raises(KeyboardInterrupt):
        TransactionService(session).apply(_transaction(session, [("world.tick", {"count": 1})]))

    assert session.world.entities() == before_world.entities()
    assert session.resources.require(SCORE) == 4
    assert session.state_hash == before_hash


def test_tick_without_executor_and_nonfinal_or_repeated_tick_are_rejected() -> None:
    session = _session()
    service = TransactionService(session)
    no_executor = service.apply(_transaction(session, [("world.tick", {"count": 1})]))
    assert no_executor.status is ReceiptStatus.REJECTED
    assert dict(no_executor.diagnostics[0].details)["cause_code"] == (
        "world.transaction.nontransactional_operation"
    )

    sequences: tuple[list[tuple[str, dict[str, object]]], ...] = (
        [
            ("world.tick", {"count": 1}),
            ("entity.spawn", {"components": list[object]()}),
        ],
        [
            ("world.tick", {"count": 1}),
            ("world.tick", {"count": 1}),
        ],
    )
    for operations in sequences:
        assert service.apply(_transaction(session, operations)).status is ReceiptStatus.REJECTED

    multi_tick = service.apply(_transaction(session, [("world.tick", {"count": 2})]))
    assert multi_tick.status is ReceiptStatus.REJECTED


@pytest.mark.parametrize(
    "spec",
    [
        OperationSpec("entity.spawn", version=2),
        OperationSpec("entity.spawn", mutating=False, transactional=False),
    ],
)
def test_registry_cannot_reclassify_or_version_builtin_handlers(spec: OperationSpec) -> None:
    session = _session()
    command = CommandEnvelope(
        "cmd-custom-operation",
        "tx-custom-operation",
        CommandActor("test", "suite"),
        "entity.spawn",
        {"components": []},
        operation_version=spec.version,
    )
    transaction = CommandTransaction((command,), session.world_id)

    receipt = TransactionService(session, operations=OperationRegistry((spec,))).apply(transaction)

    assert receipt.status is ReceiptStatus.REJECTED
    assert session.world.entities() == ()


def test_limits_and_duplicate_aliases_fail_before_staging() -> None:
    session = _session()
    service = TransactionService(
        session,
        limits=TransactionLimits(max_bytes=1_048_576, max_commands=1, max_ticks=2, max_aliases=1),
    )
    before_world = session.world
    rejected = service.apply(
        _transaction(
            session,
            [
                ("entity.spawn", {"components": []}),
                ("entity.spawn", {"components": []}),
            ],
        )
    )
    assert rejected.status is ReceiptStatus.REJECTED
    assert session.world.entities() == before_world.entities()

    duplicate = _transaction(
        session,
        [
            ("entity.spawn", {"alias": "same", "components": []}),
            ("entity.spawn", {"alias": "same", "components": []}),
        ],
    )
    assert TransactionService(session).apply(duplicate).status is ReceiptStatus.REJECTED


def test_decode_failure_attributes_the_exact_repeated_operation() -> None:
    session = _session()
    transaction = _transaction(
        session,
        [
            ("entity.destroy", {"entity": _entity(0, 0)}),
            ("entity.destroy", {"entity": {"index": "bad", "generation": 0}}),
        ],
    )

    receipt = TransactionService(session).apply(transaction)

    assert receipt.status is ReceiptStatus.REJECTED
    details = dict(receipt.diagnostics[0].details)
    assert details["operation_index"] == 1
    assert details["command_id"] == "cmd-1"
    assert details["operation"] == "entity.destroy"


def test_diff_and_receipt_limits_reject_before_adoption() -> None:
    for limits in (
        TransactionLimits(max_diff_records=1),
        TransactionLimits(max_receipt_bytes=64),
    ):
        session = _session()
        before_world = session.world
        receipt = TransactionService(session, limits=limits).apply(
            _transaction(
                session,
                [
                    ("entity.spawn", {"alias": "one", "components": []}),
                    ("entity.spawn", {"alias": "two", "components": []}),
                ],
            )
        )

        assert receipt.status is ReceiptStatus.REJECTED
        assert receipt.diagnostics[0].code == "world.transaction.limit_exceeded"
        assert session.world.entities() == before_world.entities()
        assert session.world.entities() == ()


_PRECLONE_INVALID_OPERATIONS: tuple[list[tuple[str, dict[str, object]]], ...] = (
    [
        ("entity.spawn", {"components": []}),
        ("component.patch", {"entity": {"index": 0, "generation": 0}}),
    ],
    [
        (
            "component.patch",
            {
                "entity": {"index": 0, "generation": 0},
                "type_id": "06797031-77f0-4b54-a056-4259c6627600",
                "version": 1,
                "changes": {"unknown": 1},
            },
        )
    ],
    [
        (
            "component.patch",
            {
                "entity": {"index": 0, "generation": 0},
                "type_id": "06797031-77f0-4b54-a056-4259c6627600",
                "version": 1,
                "changes": {"value": "bad"},
            },
        )
    ],
    [("entity.destroy", {"entity": {"alias": "missing"}})],
    [
        ("entity.destroy", {"entity": {"alias": "later"}}),
        ("entity.spawn", {"alias": "later", "components": []}),
    ],
)


@pytest.mark.parametrize(
    "operations",
    _PRECLONE_INVALID_OPERATIONS,
)
def test_all_operation_documents_and_aliases_validate_before_resource_clone(
    operations: list[tuple[str, dict[str, object]]],
) -> None:
    copies = 0

    def copy_score(value: int) -> int:
        nonlocal copies
        copies += 1
        return int(value)

    score = ResourceSpec("test.counted_score", int, copy_score)
    schema = AuthorityResourceSchema(
        type_id=UUID("24e59ef7-cf95-408f-b182-9073866329e3"),
        version=1,
        spec=score,
        codec_id="test.counted-score/int-v1",
        encoder=_encode_score,
        decoder=_decode_score,
    )
    resources = ResourceStore(ResourceRegistry((score,)), ((score, 1),))
    session = WorldSession(
        "arena",
        World(ComponentRegistry((Position, Health))),
        resources,
        authority_resources=AuthorityResourceRegistry((schema,)),
    )
    copies = 0
    malformed = _transaction(session, operations)

    assert TransactionService(session).apply(malformed).status is ReceiptStatus.REJECTED

    # One copy comes from pre-hash capture. A staged ResourceStore clone would
    # invoke the copier a second time.
    assert copies == 1


def test_runtime_excluded_resource_value_does_not_change_authoritative_hash() -> None:
    runtime = ResourceSpec("runtime.presentation_counter", int, int, deterministic=False)
    runtime_schema = AuthorityResourceSchema(
        UUID("1a8b7114-8768-4d94-9e2c-b5bca8f01be6"),
        1,
        runtime,
        "runtime.counter/int-v1",
        int,
        _decode_score,
        role=ResourceRole.RUNTIME_EXCLUDED,
    )
    registry = ResourceRegistry((SCORE, runtime))
    authority = AuthorityResourceRegistry((SCORE_SCHEMA, runtime_schema))
    left = WorldSession(
        "arena",
        World(ComponentRegistry((Position, Health))),
        ResourceStore(registry, ((SCORE, 0), (runtime, 1))),
        authority_resources=authority,
        tick_executor=_ScoreTickExecutor(),
    )
    right = WorldSession(
        "arena",
        World(ComponentRegistry((Position, Health))),
        ResourceStore(registry, ((SCORE, 0), (runtime, 2))),
        authority_resources=authority,
    )

    assert left.state_hash == right.state_hash
    tick_receipt = TransactionService(left).apply(
        _transaction(left, [("world.tick", {"count": 1})])
    )
    assert tick_receipt.status is ReceiptStatus.REJECTED
    assert dict(tick_receipt.diagnostics[0].details)["cause_code"] == (
        "world.transaction.nontransactional_operation"
    )


def test_world_session_rejects_unclassified_resources() -> None:
    hidden = ResourceSpec("hidden.future_input", int, int)
    with pytest.raises(AuthorityError) as raised:
        WorldSession(
            "arena",
            World(ComponentRegistry((Position, Health))),
            ResourceStore(ResourceRegistry((hidden,)), ((hidden, 1),)),
        )

    assert raised.value.details == (("unclassified_resources", "hidden.future_input"),)


def test_world_session_rejects_tick_values_outside_canonical_integer_domain() -> None:
    with pytest.raises(AuthorityError):
        WorldSession(
            "arena",
            World(ComponentRegistry((Position, Health))),
            ResourceStore(ResourceRegistry((SCORE,)), ((SCORE, 0),)),
            authority_resources=AuthorityResourceRegistry((SCORE_SCHEMA,)),
            completed_ticks=2**63,
        )

    session = WorldSession(
        "arena",
        World(ComponentRegistry((Position, Health))),
        ResourceStore(ResourceRegistry((SCORE,)), ((SCORE, 0),)),
        authority_resources=AuthorityResourceRegistry((SCORE_SCHEMA,)),
        completed_ticks=2**63 - 1,
        tick_executor=_ScoreTickExecutor(),
    )
    receipt = TransactionService(session).apply(
        _transaction(session, [("world.tick", {"count": 1})])
    )
    assert receipt.status is ReceiptStatus.REJECTED
    assert session.completed_ticks == 2**63 - 1


def test_world_session_rejects_initial_authority_outside_canonical_domain() -> None:
    world = World(ComponentRegistry((Position, Health)))
    world.spawn(Health(2**63))
    with pytest.raises(AuthorityError) as component_error:
        _session(world=world)
    assert component_error.value.code == "world.invalid_authority"
    assert component_error.value.__cause__ is not None

    with pytest.raises(AuthorityError) as resource_error:
        _session(score=2**63)
    assert resource_error.value.code == "world.invalid_authority"
    assert resource_error.value.__cause__ is not None


def test_world_session_accessors_return_detached_authority_views() -> None:
    session = _session()
    world_view = session.world
    resources_view = session.resources
    random_view = session.random_streams
    before = session.state_hash

    world_view.spawn()
    resources_view.replace(SCORE, 99)
    random_view.next_u32("detached")

    assert session.state_hash == before
    assert session.world.entities() == ()
    assert session.resources.require(SCORE) == 0


def test_allocator_churn_participates_in_hash_even_when_live_world_is_empty() -> None:
    session = _session()
    initial_hash = session.state_hash
    TransactionService(session).apply(
        _transaction(
            session,
            [
                ("entity.spawn", {"alias": "temporary", "components": []}),
                ("entity.destroy", {"entity": _alias("temporary")}),
            ],
        )
    )

    assert session.world.entities() == ()
    assert session.state_hash != initial_hash


def test_production_and_reference_worlds_have_equal_authority_hashes() -> None:
    registry = ComponentRegistry((Position, Health))
    production = World(registry)
    reference = ReferenceWorld(registry)
    for world in (production, reference):
        entity = world.spawn(Position(1.0, -0.0), Health(4))
        world.patch(entity, Health, value=3)
    production_session = _session(world=production, score=8)
    reference_session = _session(world=reference, score=8)

    assert production_session.authority_document() == reference_session.authority_document()
    assert production_session.state_hash == reference_session.state_hash


def test_world_session_enforces_constructing_thread() -> None:
    session = _session()
    failures: list[BaseException] = []

    def read_hash() -> None:
        try:
            _ = session.state_hash
        except BaseException as error:
            failures.append(error)

    thread = threading.Thread(target=read_hash)
    thread.start()
    thread.join()

    assert len(failures) == 1
    assert isinstance(failures[0], AuthorityError)
    assert failures[0].details == (
        ("caller", "different_thread"),
        ("owner", "constructing_thread"),
    )
