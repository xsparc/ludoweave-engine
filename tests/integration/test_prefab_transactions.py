"""One-level prefab override planning through ordinary world transactions."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast
from uuid import UUID

import pytest

from ludoweave.ecs import (
    ComponentMigration,
    ComponentRegistry,
    EntityId,
    ResourceRegistry,
    ResourceStore,
    World,
    component,
)
from ludoweave.scene import (
    PrefabDocument,
    PrefabError,
    PrefabInstance,
    PrefabNode,
    SceneNode,
    compile_prefab,
)
from ludoweave.world import (
    AuthorityResourceRegistry,
    CommandActor,
    ReceiptStatus,
    TransactionService,
    WorldSession,
)
from ludoweave.world.canonical import JsonValue


def _transform_v1_to_v2(values: Mapping[str, object]) -> Mapping[str, object]:
    return {"x": values["x"], "y": values["y"]}


@component(
    type_id=UUID("d96bd556-83e7-5dd7-a4d2-fc5f46356764"),
    version=2,
    migrations=(ComponentMigration(1, 2, _transform_v1_to_v2),),
)
@dataclass(frozen=True, slots=True)
class Transform2D:
    x: float
    y: float


def _qualified(component_type: type[object]) -> str:
    return f"{component_type.__module__}.{component_type.__qualname__}"


def _prefab() -> PrefabDocument:
    return PrefabDocument.from_mapping(
        {
            "$schema": "ludoweave.prefab/1",
            "prefab_id": "enemy.scout",
            "entities": [
                {
                    "local_id": "root",
                    "name": "Scout",
                    "parent": None,
                    "components": {
                        _qualified(Transform2D): {
                            "version": 1,
                            "values": {"x": 2.0, "y": 3.0},
                        }
                    },
                }
            ],
            "dependencies": ["asset://sprites/scout.png"],
        }
    )


def _instance(*, changes: dict[str, JsonValue] | None = None) -> PrefabInstance:
    return PrefabInstance.from_mapping(
        {
            "$schema": "ludoweave.prefab-instance/1",
            "prefab_id": "enemy.scout",
            "instance_id": "scout-one",
            "overrides": [
                {
                    "local_id": "root",
                    "component": _qualified(Transform2D),
                    "version": 2,
                    "changes": changes if changes is not None else {"x": 5.0},
                }
            ],
        }
    )


def _registry() -> ComponentRegistry:
    return ComponentRegistry((PrefabNode, SceneNode, Transform2D))


def _session() -> WorldSession:
    registry = _registry()
    return WorldSession(
        "prefab-world",
        World(registry),
        ResourceStore(ResourceRegistry()),
        authority_resources=AuthorityResourceRegistry(),
    )


def _entity(value: str) -> EntityId:
    index, generation = value.split(":")
    return EntityId(int(index), int(generation))


def test_prefab_compiles_to_spawn_commands_and_receipt_aliases() -> None:
    session = _session()
    plan = compile_prefab(
        _prefab(),
        _instance(),
        registry=_registry(),
        world_id=session.world_id,
        transaction_id="prefab-transaction",
        actor=CommandActor("test", "prefab-suite"),
    )

    assert plan.prefab_id == "enemy.scout"
    assert plan.instance_id == "scout-one"
    assert tuple(item.value for item in plan.dependencies) == ("asset://sprites/scout.png",)
    assert tuple(command.operation for command in plan.transaction.commands) == ("entity.spawn",)

    receipt = TransactionService(session).apply(plan.transaction)
    aliases = dict(receipt.aliases)
    entity = _entity(aliases["root"])
    assert receipt.status is ReceiptStatus.COMMITTED
    assert session.world.get(entity, Transform2D) == Transform2D(5.0, 3.0)
    assert session.world.get(entity, PrefabNode) == PrefabNode(
        prefab_id="enemy.scout",
        instance_id="scout-one",
        local_id="root",
    )
    assert session.world.get(entity, SceneNode) == SceneNode(
        scene_id="enemy.scout",
        instance_id="scout-one",
        local_id="root",
        name="Scout",
        parent_local_id=None,
    )


def test_prefab_planning_is_canonical_and_does_not_mutate_sources() -> None:
    prefab = _prefab()
    instance = _instance()
    prefab_bytes = prefab.canonical_bytes()
    instance_bytes = instance.canonical_bytes()
    registry = _registry()
    actor = CommandActor("test", "prefab-suite")

    first = compile_prefab(
        prefab,
        instance,
        registry=registry,
        world_id="prefab-world",
        transaction_id="prefab-transaction",
        actor=actor,
    )
    reordered = instance.as_dict()
    overrides = reordered["overrides"]
    assert isinstance(overrides, list)
    reordered["overrides"] = list(reversed(overrides))
    second = compile_prefab(
        PrefabDocument.from_json(prefab_bytes),
        PrefabInstance.from_mapping(reordered),
        registry=registry,
        world_id="prefab-world",
        transaction_id="prefab-transaction",
        actor=actor,
    )

    assert first.transaction.canonical_bytes() == second.transaction.canonical_bytes()
    assert prefab.canonical_bytes() == prefab_bytes
    assert instance.canonical_bytes() == instance_bytes


@pytest.mark.parametrize(
    ("instance", "expected_code"),
    [
        (
            {
                "$schema": "ludoweave.prefab-instance/1",
                "prefab_id": "other",
                "instance_id": "scout-one",
                "overrides": [],
            },
            "prefab.source_mismatch",
        ),
        (
            {
                "$schema": "ludoweave.prefab-instance/1",
                "prefab_id": "enemy.scout",
                "instance_id": "scout-one",
                "overrides": [
                    {
                        "local_id": "missing",
                        "component": _qualified(Transform2D),
                        "version": 2,
                        "changes": {"x": 5.0},
                    }
                ],
            },
            "prefab.unknown_target",
        ),
        (
            {
                "$schema": "ludoweave.prefab-instance/1",
                "prefab_id": "enemy.scout",
                "instance_id": "scout-one",
                "overrides": [
                    {
                        "local_id": "root",
                        "component": "game.Missing",
                        "version": 2,
                        "changes": {"x": 5.0},
                    }
                ],
            },
            "prefab.missing_component",
        ),
        (
            {
                "$schema": "ludoweave.prefab-instance/1",
                "prefab_id": "enemy.scout",
                "instance_id": "scout-one",
                "overrides": [
                    {
                        "local_id": "root",
                        "component": _qualified(Transform2D),
                        "version": 1,
                        "changes": {"x": 5.0},
                    }
                ],
            },
            "prefab.incompatible_override",
        ),
    ],
)
def test_prefab_semantic_failures_precede_world_mutation(
    instance: dict[str, JsonValue], expected_code: str
) -> None:
    session = _session()
    before = session.state_hash
    with pytest.raises(PrefabError) as captured:
        compile_prefab(
            _prefab(),
            PrefabInstance.from_mapping(instance),
            registry=_registry(),
            world_id=session.world_id,
            transaction_id="prefab-transaction",
            actor=CommandActor("test", "prefab-suite"),
        )
    assert captured.value.code == expected_code
    assert session.state_hash == before
    assert session.world.entities() == ()


@pytest.mark.parametrize(
    ("changes", "expected_cause"),
    [
        ({"unknown": 1.0}, "ecs.invalid_component_data"),
        ({"x": cast(JsonValue, "bad")}, "ecs.invalid_component_data"),
    ],
)
def test_schema_aware_override_rejects_unknown_or_invalid_fields(
    changes: dict[str, JsonValue], expected_cause: str
) -> None:
    with pytest.raises(PrefabError) as captured:
        compile_prefab(
            _prefab(),
            _instance(changes=changes),
            registry=_registry(),
            world_id="prefab-world",
            transaction_id="prefab-transaction",
            actor=CommandActor("test", "prefab-suite"),
        )
    assert captured.value.code == "prefab.invalid_override"
    assert dict(captured.value.details)["cause_code"] == expected_cause


def test_empty_override_set_uses_migrated_fragment_values() -> None:
    session = _session()
    instance = PrefabInstance.from_mapping(
        {
            "$schema": "ludoweave.prefab-instance/1",
            "prefab_id": "enemy.scout",
            "instance_id": "scout-default",
            "overrides": [],
        }
    )
    plan = compile_prefab(
        _prefab(),
        instance,
        registry=_registry(),
        world_id=session.world_id,
        transaction_id="prefab-default-transaction",
        actor=CommandActor("test", "prefab-suite"),
    )
    receipt = TransactionService(session).apply(plan.transaction)
    entity = _entity(dict(receipt.aliases)["root"])
    assert session.world.get(entity, Transform2D) == Transform2D(2.0, 3.0)


@pytest.mark.parametrize(
    "registry",
    [
        ComponentRegistry((SceneNode, Transform2D)),
        ComponentRegistry((PrefabNode, Transform2D)),
    ],
)
def test_prefab_provenance_registrations_are_explicit(registry: ComponentRegistry) -> None:
    with pytest.raises(PrefabError) as captured:
        compile_prefab(
            _prefab(),
            _instance(),
            registry=registry,
            world_id="prefab-world",
            transaction_id="prefab-transaction",
            actor=CommandActor("test", "prefab-suite"),
        )
    assert captured.value.code == "prefab.registry_mismatch"


def test_stale_hash_rejection_keeps_prefab_instantiation_atomic() -> None:
    session = _session()
    plan = compile_prefab(
        _prefab(),
        _instance(),
        registry=_registry(),
        world_id=session.world_id,
        transaction_id="prefab-transaction",
        actor=CommandActor("test", "prefab-suite"),
        expected_world_hash="sha256:" + "0" * 64,
    )

    receipt = TransactionService(session).apply(plan.transaction)
    assert receipt.status is ReceiptStatus.REJECTED
    assert receipt.aliases == ()
    assert session.world.entities() == ()


def test_prefab_node_is_compiler_owned() -> None:
    source = _prefab().as_dict()
    entities = cast(list[JsonValue], source["entities"])
    root = cast(dict[str, JsonValue], entities[0])
    components = cast(dict[str, JsonValue], root["components"])
    components[_qualified(PrefabNode)] = {
        "version": 1,
        "values": {"prefab_id": "enemy.scout", "instance_id": "x", "local_id": "root"},
    }

    with pytest.raises(PrefabError) as captured:
        compile_prefab(
            PrefabDocument.from_mapping(source),
            _instance(),
            registry=_registry(),
            world_id="prefab-world",
            transaction_id="prefab-transaction",
            actor=CommandActor("test", "prefab-suite"),
        )
    assert captured.value.code == "prefab.reserved_component"


def test_prefab_planner_requires_exact_public_values() -> None:
    with pytest.raises(PrefabError) as captured:
        compile_prefab(
            cast(PrefabDocument, object()),
            _instance(),
            registry=_registry(),
            world_id="prefab-world",
            transaction_id="prefab-transaction",
            actor=CommandActor("test", "prefab-suite"),
        )
    assert captured.value.code == "prefab.invalid_plan"
