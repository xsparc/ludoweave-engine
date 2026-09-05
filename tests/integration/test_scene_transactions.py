"""Compile data-only scenes into existing atomic world transactions."""

from dataclasses import dataclass
from typing import cast
from uuid import UUID

import pytest

from ludoweave.ecs import (
    ComponentRegistry,
    EntityId,
    ResourceRegistry,
    ResourceStore,
    World,
    component,
)
from ludoweave.scene import SceneDocument, SceneError, SceneNode, compile_scene
from ludoweave.world import (
    AuthorityResourceRegistry,
    CommandActor,
    ReceiptStatus,
    TransactionService,
    WorldSession,
)


@component(type_id=UUID("b604b3fa-31a7-55f4-bb8c-949e48a10ca6"))
@dataclass(frozen=True, slots=True)
class Transform2D:
    x: float
    y: float


def _qualified(component_type: type[object]) -> str:
    return f"{component_type.__module__}.{component_type.__qualname__}"


def _scene(*, component_name: str | None = None) -> SceneDocument:
    document: dict[str, object] = {
        "$schema": "ludoweave.scene/1",
        "scene_id": "level-one",
        "entities": [
            {
                "local_id": "root",
                "name": "Level",
                "parent": None,
                "components": {},
            },
            {
                "local_id": "player",
                "name": "Player",
                "parent": "root",
                "components": {
                    component_name or _qualified(Transform2D): {
                        "version": 1,
                        "values": {"x": 96.0, "y": 64.0},
                    }
                },
            },
        ],
        "dependencies": ["asset://sprites/player.png"],
    }
    return SceneDocument.from_mapping(document)


def _session(registry: ComponentRegistry) -> WorldSession:
    return WorldSession(
        "scene-world",
        World(registry),
        ResourceStore(ResourceRegistry()),
        authority_resources=AuthorityResourceRegistry(),
    )


def _entity(value: str) -> EntityId:
    index, generation = value.split(":")
    return EntityId(int(index), int(generation))


def test_scene_compiles_to_spawn_commands_and_receipt_alias_mapping() -> None:
    registry = ComponentRegistry((SceneNode, Transform2D))
    session = _session(registry)
    plan = compile_scene(
        _scene(),
        registry=registry,
        world_id=session.world_id,
        transaction_id="scene-transaction",
        actor=CommandActor("test", "scene-suite"),
        instance_id="instance-one",
    )

    assert plan.scene_id == "level-one"
    assert plan.instance_id == "instance-one"
    assert tuple(item.value for item in plan.dependencies) == ("asset://sprites/player.png",)
    assert tuple(command.operation for command in plan.transaction.commands) == (
        "entity.spawn",
        "entity.spawn",
    )
    assert tuple(command.arguments["alias"] for command in plan.transaction.commands) == (
        "player",
        "root",
    )

    receipt = TransactionService(session).apply(plan.transaction)
    aliases = dict(receipt.aliases)
    assert receipt.status is ReceiptStatus.COMMITTED
    assert tuple(aliases) == ("player", "root")
    player = _entity(aliases["player"])
    root = _entity(aliases["root"])
    assert session.world.get(player, Transform2D) == Transform2D(96.0, 64.0)
    assert session.world.get(player, SceneNode) == SceneNode(
        scene_id="level-one",
        instance_id="instance-one",
        local_id="player",
        name="Player",
        parent_local_id="root",
    )
    assert session.world.get(root, SceneNode).parent_local_id is None


def test_scene_compilation_is_canonical_across_source_entity_order() -> None:
    source = _scene().as_dict()
    entities = source["entities"]
    assert isinstance(entities, list)
    source["entities"] = list(reversed(entities))
    reordered = SceneDocument.from_mapping(source)
    registry = ComponentRegistry((SceneNode, Transform2D))
    actor = CommandActor("test", "scene-suite")

    assert (
        compile_scene(
            _scene(),
            registry=registry,
            world_id="scene-world",
            transaction_id="scene-transaction",
            actor=actor,
            instance_id="instance-one",
        ).transaction.canonical_bytes()
        == compile_scene(
            reordered,
            registry=registry,
            world_id="scene-world",
            transaction_id="scene-transaction",
            actor=actor,
            instance_id="instance-one",
        ).transaction.canonical_bytes()
    )


def test_unknown_component_fails_before_world_mutation() -> None:
    registry = ComponentRegistry((SceneNode, Transform2D))
    session = _session(registry)
    before = session.state_hash

    with pytest.raises(SceneError) as captured:
        compile_scene(
            _scene(component_name="game.Unknown"),
            registry=registry,
            world_id=session.world_id,
            transaction_id="scene-transaction",
            actor=CommandActor("test", "scene-suite"),
            instance_id="instance-one",
        )

    assert captured.value.code == "scene.unknown_component"
    assert session.state_hash == before
    assert session.world.entities() == ()


def test_scene_node_cannot_be_supplied_as_a_document_component() -> None:
    registry = ComponentRegistry((SceneNode, Transform2D))

    with pytest.raises(SceneError, match="reserved"):
        compile_scene(
            _scene(component_name=_qualified(SceneNode)),
            registry=registry,
            world_id="scene-world",
            transaction_id="scene-transaction",
            actor=CommandActor("test", "scene-suite"),
            instance_id="instance-one",
        )


def test_scene_node_registration_is_required_explicitly() -> None:
    with pytest.raises(SceneError) as captured:
        compile_scene(
            _scene(),
            registry=ComponentRegistry((Transform2D,)),
            world_id="scene-world",
            transaction_id="scene-transaction",
            actor=CommandActor("test", "scene-suite"),
            instance_id="instance-one",
        )

    assert captured.value.code == "scene.registry_mismatch"


def test_invalid_plan_identity_is_a_structured_scene_failure() -> None:
    registry = ComponentRegistry((SceneNode, Transform2D))

    with pytest.raises(SceneError) as captured:
        compile_scene(
            _scene(),
            registry=registry,
            world_id=cast(str, 7),
            transaction_id="scene-transaction",
            actor=CommandActor("test", "scene-suite"),
            instance_id="instance-one",
        )

    assert captured.value.code == "scene.invalid_plan"
    assert captured.value.phase == "plan"


def test_empty_scene_reports_existing_nonempty_transaction_boundary() -> None:
    empty = SceneDocument.from_mapping(
        {
            "$schema": "ludoweave.scene/1",
            "scene_id": "empty-scene",
            "entities": [],
            "dependencies": [],
        }
    )

    with pytest.raises(SceneError) as captured:
        compile_scene(
            empty,
            registry=ComponentRegistry((SceneNode,)),
            world_id="scene-world",
            transaction_id="empty-scene-transaction",
            actor=CommandActor("test", "scene-suite"),
            instance_id="empty-instance",
        )

    assert captured.value.code == "scene.invalid_plan"
