"""Generated command sequences compared with independent direct world operations."""

from dataclasses import dataclass
from uuid import UUID

from hypothesis import given, settings
from hypothesis import strategies as st

from ludoweave.ecs import (
    ComponentRegistry,
    EntityId,
    ReferenceWorld,
    ResourceRegistry,
    ResourceSpec,
    ResourceStore,
    World,
    WorldStore,
    component,
)
from ludoweave.world import (
    AuthorityResourceRegistry,
    AuthorityResourceSchema,
    CommandActor,
    CommandEnvelope,
    CommandTransaction,
    ReceiptStatus,
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


def encode_score(value: int) -> object:
    return value


def decode_score(value: JsonValue) -> int:
    if type(value) is not int:
        raise ValueError
    return value


SCORE_SCHEMA = AuthorityResourceSchema(
    type_id=UUID("c16a2451-0f09-4207-badd-37ade4739c9f"),
    version=1,
    spec=SCORE,
    codec_id="game.score/int-v1",
    encoder=encode_score,
    decoder=decode_score,
)


def make_session(*, world: WorldStore | None = None) -> WorldSession:
    registry = ComponentRegistry((Position, Health))
    return WorldSession(
        "arena",
        World(registry) if world is None else world,
        ResourceStore(ResourceRegistry((SCORE,)), ((SCORE, 0),)),
        authority_resources=AuthorityResourceRegistry((SCORE_SCHEMA,)),
    )


def make_transaction(
    session: WorldSession, operations: list[tuple[str, dict[str, object]]]
) -> CommandTransaction:
    actor = CommandActor("test", "property")
    return CommandTransaction(
        commands=tuple(
            CommandEnvelope(
                command_id=f"cmd-{index}",
                transaction_id="tx-property",
                actor=actor,
                operation=operation,
                arguments=arguments,
            )
            for index, (operation, arguments) in enumerate(operations)
        ),
        world_id=session.world_id,
    )


def component_payload(component_type: type[object], values: dict[str, object]) -> dict[str, object]:
    schema = ComponentRegistry((component_type,)).schema_for_type(component_type)
    return {"type_id": str(schema.type_id), "version": schema.version, "values": values}


def entity_alias(name: str) -> dict[str, object]:
    return {"alias": name}


@dataclass(frozen=True, slots=True)
class Action:
    kind: str
    value: int


_actions = st.lists(
    st.builds(
        Action,
        kind=st.sampled_from(("spawn", "patch", "destroy", "score")),
        value=st.integers(min_value=-20, max_value=20),
    ),
    min_size=1,
    max_size=30,
)


@given(_actions)
@settings(max_examples=75, deadline=None)
def test_valid_generated_transaction_matches_direct_reference_world(actions: list[Action]) -> None:
    production_session = make_session()
    registry = ComponentRegistry((Position, Health))
    reference_world = ReferenceWorld(registry)
    reference_resources = ResourceStore(ResourceRegistry((SCORE,)), ((SCORE, 0),))
    reference_session = WorldSession(
        "arena",
        reference_world,
        reference_resources,
        authority_resources=AuthorityResourceRegistry((SCORE_SCHEMA,)),
    )

    operations: list[tuple[str, dict[str, object]]] = []
    alive: list[tuple[str, EntityId]] = []
    next_alias = 0
    for action in actions:
        if action.kind == "spawn" or (not alive and action.kind in {"patch", "destroy"}):
            alias = f"entity-{next_alias}"
            next_alias += 1
            position = Position(float(action.value), -0.0 if action.value == 0 else 1.0)
            operations.append(
                (
                    "entity.spawn",
                    {
                        "alias": alias,
                        "components": [
                            component_payload(Position, {"x": position.x, "y": position.y})
                        ],
                    },
                )
            )
            entity_id = reference_world.spawn(position)
            alive.append((alias, entity_id))
        elif action.kind == "patch":
            alias, entity_id = alive[abs(action.value) % len(alive)]
            value = float(action.value)
            operations.append(
                (
                    "component.patch",
                    {
                        "entity": entity_alias(alias),
                        "type_id": str(UUID("91619a10-e096-4bb1-8e47-3ce84bd219aa")),
                        "version": 1,
                        "changes": {"x": value},
                    },
                )
            )
            reference_world.patch(entity_id, Position, x=value)
        elif action.kind == "destroy":
            selected = abs(action.value) % len(alive)
            alias, entity_id = alive.pop(selected)
            operations.append(("entity.destroy", {"entity": entity_alias(alias)}))
            reference_world.destroy(entity_id)
        else:
            operations.append(
                (
                    "resource.patch",
                    {
                        "type_id": str(SCORE_SCHEMA.type_id),
                        "version": SCORE_SCHEMA.version,
                        "value": action.value,
                    },
                )
            )
            reference_resources.replace(SCORE, action.value)

    result = TransactionService(production_session).apply(
        make_transaction(production_session, operations)
    )

    assert result.status is ReceiptStatus.COMMITTED
    assert production_session.authority_document() == reference_session.authority_document()
    assert production_session.state_hash == reference_session.state_hash


@given(st.integers(min_value=0, max_value=20), st.integers(min_value=1, max_value=20))
@settings(max_examples=40, deadline=None)
def test_generated_failure_position_never_changes_authority(
    prefix_spawns: int, suffix_spawns: int
) -> None:
    session = make_session()
    operations: list[tuple[str, dict[str, object]]] = [
        ("entity.spawn", {"alias": f"before-{index}", "components": []})
        for index in range(prefix_spawns)
    ]
    operations.append(("entity.destroy", {"entity": {"index": 999, "generation": 0}}))
    operations.extend(
        ("entity.spawn", {"alias": f"after-{index}", "components": []})
        for index in range(suffix_spawns)
    )
    before = session.authority_document()
    before_hash = session.state_hash

    receipt = TransactionService(session).apply(make_transaction(session, operations))
    assert receipt.status is ReceiptStatus.REJECTED

    assert session.authority_document() == before
    assert session.state_hash == before_hash
