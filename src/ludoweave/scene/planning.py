"""Deterministic compilation of scene documents into world transactions."""

import re
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from typing import cast
from uuid import UUID

from ludoweave.assets import AssetUri
from ludoweave.core.errors import LudoWeaveError
from ludoweave.ecs import ComponentRegistry, component
from ludoweave.scene.document import SceneComponent, SceneDocument
from ludoweave.scene.errors import SceneError
from ludoweave.world import CommandActor, CommandEnvelope, CommandTransaction
from ludoweave.world.canonical import FrozenJsonValue, JsonValue, thaw_json

_SCENE_NODE_TYPE_ID = UUID("f08fe416-fcb5-5b34-bea5-9b01ca8e4972")
_STABLE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")


@component(type_id=_SCENE_NODE_TYPE_ID)
@dataclass(frozen=True, slots=True)
class SceneNode:
    """Canonical scene provenance stored with each instantiated entity."""

    scene_id: str
    instance_id: str
    local_id: str
    name: str
    parent_local_id: str | None


@dataclass(frozen=True, slots=True)
class SceneInstantiationPlan:
    """A detached scene plan ready for ordinary transaction application."""

    scene_id: str
    instance_id: str
    dependencies: tuple[AssetUri, ...]
    transaction: CommandTransaction


def compile_scene(
    scene: SceneDocument,
    *,
    registry: ComponentRegistry,
    world_id: str,
    transaction_id: str,
    actor: CommandActor,
    instance_id: str,
    expected_world_hash: str | None = None,
    dry_run: bool = False,
) -> SceneInstantiationPlan:
    """Compile a data-only scene into canonical ``entity.spawn`` commands."""

    if type(scene) is not SceneDocument:
        raise _planning_error(
            "scene planning requires an exact SceneDocument value",
            code="scene.invalid_plan",
            details={"field": "scene", "actual_type": type(scene).__name__},
        )
    if type(registry) is not ComponentRegistry:
        raise _planning_error(
            "scene planning requires an exact ComponentRegistry value",
            code="scene.registry_mismatch",
            details={"actual_type": type(registry).__name__},
        )
    checked_world_id = _stable_id(world_id, field="world_id")
    checked_transaction_id = _stable_id(transaction_id, field="transaction_id")
    checked_instance_id = _stable_id(instance_id, field="instance_id")
    if type(actor) is not CommandActor:
        raise _planning_error(
            "scene planning requires an exact CommandActor value",
            code="scene.invalid_plan",
            details={"field": "actor", "actual_type": type(actor).__name__},
        )
    if type(dry_run) is not bool:
        raise _planning_error(
            "scene dry-run intent must be an exact boolean",
            code="scene.invalid_plan",
            details={"field": "dry_run", "actual_type": type(dry_run).__name__},
        )
    try:
        scene_node_schema = registry.schema_for_type(SceneNode)
    except LudoWeaveError as error:
        raise _planning_error(
            "scene planning registry must explicitly contain SceneNode",
            code="scene.registry_mismatch",
            details={"cause_code": error.code},
        ) from error
    if scene_node_schema.type_id != _SCENE_NODE_TYPE_ID or scene_node_schema.version != 1:
        raise _planning_error(
            "scene planning registry contains an incompatible SceneNode schema",
            code="scene.registry_mismatch",
            details={"type_id": str(scene_node_schema.type_id)},
        )

    command_seed = sha256(
        b"ludoweave.scene.plan/1\0"
        + scene.canonical_bytes()
        + b"\0"
        + checked_world_id.encode("utf-8")
        + b"\0"
        + checked_transaction_id.encode("utf-8")
        + b"\0"
        + checked_instance_id.encode("utf-8")
    ).hexdigest()[:24]
    commands: list[CommandEnvelope] = []
    for index, entity in enumerate(scene.entities):
        if any(
            component_value.qualified_name == scene_node_schema.qualified_name
            for component_value in entity.components
        ):
            raise _planning_error(
                "SceneNode is reserved for compiler-owned scene provenance",
                code="scene.reserved_component",
                details={"component": scene_node_schema.qualified_name},
            )
        payloads = [
            _compile_component(component_value, registry=registry)
            for component_value in entity.components
        ]
        scene_node_values: dict[str, object] = {
            "scene_id": scene.scene_id,
            "instance_id": checked_instance_id,
            "local_id": entity.local_id,
            "name": entity.name,
            "parent_local_id": entity.parent_local_id,
        }
        try:
            checked_node_values = registry.migrate(
                scene_node_schema.type_id,
                from_version=scene_node_schema.version,
                values=scene_node_values,
            )
        except LudoWeaveError as error:
            raise _planning_error(
                "compiler-owned SceneNode values do not match the registered schema",
                code="scene.registry_mismatch",
                details={"cause_code": error.code},
            ) from error
        payloads.append(
            {
                "type_id": str(scene_node_schema.type_id),
                "version": scene_node_schema.version,
                "values": cast(JsonValue, checked_node_values),
            }
        )
        payloads.sort(key=lambda payload: cast(str, payload["type_id"]))
        try:
            commands.append(
                CommandEnvelope(
                    command_id=f"scene.{command_seed}.{index}",
                    transaction_id=checked_transaction_id,
                    actor=actor,
                    operation="entity.spawn",
                    arguments={"alias": entity.local_id, "components": payloads},
                    expected_world_hash=expected_world_hash,
                )
            )
        except LudoWeaveError as error:
            raise _planning_error(
                "scene spawn command could not be constructed",
                code="scene.invalid_plan",
                details={"local_id": entity.local_id, "cause_code": error.code},
            ) from error
    try:
        transaction = CommandTransaction(
            commands=tuple(commands),
            world_id=checked_world_id,
            dry_run=dry_run,
        )
    except LudoWeaveError as error:
        raise _planning_error(
            "scene transaction could not be constructed",
            code="scene.invalid_plan",
            details={"cause_code": error.code},
        ) from error
    return SceneInstantiationPlan(
        scene_id=scene.scene_id,
        instance_id=checked_instance_id,
        dependencies=scene.dependencies,
        transaction=transaction,
    )


def _compile_component(
    value: SceneComponent,
    *,
    registry: ComponentRegistry,
) -> dict[str, JsonValue]:
    try:
        schema = registry.schema_for_name(value.qualified_name)
    except LudoWeaveError as error:
        raise _planning_error(
            "scene names an unknown component schema",
            code="scene.unknown_component",
            details={"component": value.qualified_name, "cause_code": error.code},
        ) from error
    raw_values = thaw_json(cast(FrozenJsonValue, value.values))
    assert isinstance(raw_values, dict)
    try:
        checked_values = registry.migrate(
            schema.type_id,
            from_version=value.version,
            values=cast(dict[str, object], raw_values),
        )
    except LudoWeaveError as error:
        raise _planning_error(
            "scene component values are incompatible with the registered schema",
            code="scene.invalid_component",
            details={"component": value.qualified_name, "cause_code": error.code},
        ) from error
    return {
        "type_id": str(schema.type_id),
        "version": schema.version,
        "values": cast(JsonValue, checked_values),
    }


def _stable_id(value: object, *, field: str) -> str:
    if type(value) is not str or _STABLE_ID.fullmatch(value) is None:
        raise _planning_error(
            "scene plan identity must use bounded stable text",
            code="scene.invalid_plan",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _planning_error(
    message: str,
    *,
    code: str,
    details: Mapping[str, str | int | float | bool | None],
) -> SceneError:
    return SceneError(
        message,
        code=code,
        subsystem="scene",
        phase="plan",
        details=details,
    )
