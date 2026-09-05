"""Bounded one-level prefab fragments and deterministic instantiation plans."""

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast
from uuid import UUID

from ludoweave.assets import AssetUri
from ludoweave.core.errors import LudoWeaveError
from ludoweave.ecs import ComponentRegistry, ComponentSchema, component
from ludoweave.scene.document import (
    DEFAULT_SCENE_LIMITS,
    SceneComponent,
    SceneDocument,
    SceneEntity,
    SceneLimits,
)
from ludoweave.scene.errors import PrefabError, SceneError
from ludoweave.scene.planning import SceneNode, compile_scene
from ludoweave.world import CommandActor, CommandTransaction
from ludoweave.world.canonical import (
    FrozenJsonValue,
    JsonValue,
    canonical_dumps,
    canonical_loads,
    freeze_json_object,
    thaw_json,
)

PREFAB_PROTOCOL = "ludoweave.prefab/1"
PREFAB_INSTANCE_PROTOCOL = "ludoweave.prefab-instance/1"

_PREFAB_NODE_TYPE_ID = UUID("bd6f600f-6e53-5adf-afdb-a5307bf6db62")
_STABLE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_LOCAL_ID = re.compile(r"[A-Za-z][A-Za-z0-9._:-]{0,127}\Z")
_COMPONENT_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+\Z")
_MAX_OVERRIDES = 4_096
_MAX_FIELDS_PER_OVERRIDE = 256


@dataclass(frozen=True, slots=True)
class PrefabLimits:
    """Hard-bounded prefab decode limits layered over scene limits."""

    scene: SceneLimits = DEFAULT_SCENE_LIMITS
    max_overrides: int = _MAX_OVERRIDES
    max_fields_per_override: int = _MAX_FIELDS_PER_OVERRIDE

    def __post_init__(self) -> None:
        if type(self.scene) is not SceneLimits:
            raise _prefab_error(
                "prefab scene limits must be an exact SceneLimits value",
                code="prefab.invalid_limits",
                phase="configure",
                details={"field": "scene", "actual_type": type(self.scene).__name__},
            )
        for field, maximum in (
            ("max_overrides", _MAX_OVERRIDES),
            ("max_fields_per_override", _MAX_FIELDS_PER_OVERRIDE),
        ):
            value = getattr(self, field)
            if type(value) is not int or value <= 0:
                raise _prefab_error(
                    "prefab limits must be exact positive integers",
                    code="prefab.invalid_limits",
                    phase="configure",
                    details={"field": field, "actual_type": type(value).__name__},
                )
            if value > maximum:
                raise _prefab_error(
                    "prefab limits may tighten but not exceed hard maxima",
                    code="prefab.invalid_limits",
                    phase="configure",
                    details={"field": field, "actual": value, "maximum": maximum},
                )


DEFAULT_PREFAB_LIMITS = PrefabLimits()


@dataclass(frozen=True, slots=True)
class PrefabDocument:
    """An immutable scene fragment with stable local identities."""

    prefab_id: str
    entities: tuple[SceneEntity, ...]
    dependencies: tuple[AssetUri, ...]
    protocol: str = PREFAB_PROTOCOL

    def __post_init__(self) -> None:
        if type(self.protocol) is not str or self.protocol != PREFAB_PROTOCOL:
            raise _prefab_error(
                "prefab protocol is unsupported",
                code="prefab.incompatible_protocol",
                phase="construct",
                details={"actual_type": type(self.protocol).__name__},
            )
        _stable_id(self.prefab_id, field="prefab_id", phase="construct")
        try:
            fragment = SceneDocument(
                scene_id=self.prefab_id,
                entities=self.entities,
                dependencies=self.dependencies,
            )
        except SceneError as error:
            raise _prefab_error(
                "prefab fragment is not a valid scene fragment",
                code="prefab.invalid_fragment",
                phase="construct",
                details={"cause_code": error.code},
            ) from error
        object.__setattr__(self, "entities", fragment.entities)
        object.__setattr__(self, "dependencies", fragment.dependencies)

    @classmethod
    def from_json(
        cls,
        document: str | bytes,
        *,
        limits: PrefabLimits = DEFAULT_PREFAB_LIMITS,
    ) -> "PrefabDocument":
        """Decode one bounded canonical-JSON prefab fragment."""

        checked_limits = _require_limits(limits)
        try:
            value = canonical_loads(document, limits=checked_limits.scene.json_limits())
        except LudoWeaveError as error:
            raise _prefab_error(
                "prefab JSON could not be decoded canonically",
                code="prefab.invalid_json",
                phase="decode",
                details={"cause_code": error.code},
            ) from error
        return cls._from_checked(value, limits=checked_limits)

    @classmethod
    def from_mapping(
        cls,
        value: object,
        *,
        limits: PrefabLimits = DEFAULT_PREFAB_LIMITS,
    ) -> "PrefabDocument":
        """Validate and detach one decoded prefab fragment."""

        checked_limits = _require_limits(limits)
        try:
            encoded = canonical_dumps(value, limits=checked_limits.scene.json_limits())
            checked = canonical_loads(encoded, limits=checked_limits.scene.json_limits())
        except LudoWeaveError as error:
            raise _prefab_error(
                "prefab document is outside the bounded canonical JSON domain",
                code="prefab.invalid_document",
                phase="decode",
                details={"cause_code": error.code},
            ) from error
        return cls._from_checked(checked, limits=checked_limits)

    @classmethod
    def _from_checked(cls, value: object, *, limits: PrefabLimits) -> "PrefabDocument":
        document = _object(value, role="prefab")
        _exact_fields(
            document,
            required={"$schema", "prefab_id", "entities", "dependencies"},
            role="prefab",
        )
        protocol = _text(document["$schema"], field="$schema")
        if protocol != PREFAB_PROTOCOL:
            raise _prefab_error(
                "prefab protocol is unsupported",
                code="prefab.incompatible_protocol",
                phase="decode",
                details={"protocol": protocol},
            )
        prefab_id = _stable_id(document["prefab_id"], field="prefab_id")
        try:
            fragment = SceneDocument.from_mapping(
                {
                    "$schema": "ludoweave.scene/1",
                    "scene_id": prefab_id,
                    "entities": document["entities"],
                    "dependencies": document["dependencies"],
                },
                limits=limits.scene,
            )
        except SceneError as error:
            raise _prefab_error(
                "prefab fragment is not a valid scene fragment",
                code="prefab.invalid_fragment",
                phase="decode",
                details={"cause_code": error.code},
            ) from error
        return cls(
            protocol=protocol,
            prefab_id=prefab_id,
            entities=fragment.entities,
            dependencies=fragment.dependencies,
        )

    def as_dict(self) -> dict[str, JsonValue]:
        """Return a detached ordinary JSON representation."""

        return {
            "$schema": self.protocol,
            "prefab_id": self.prefab_id,
            "entities": [entity.as_dict() for entity in self.entities],
            "dependencies": [dependency.value for dependency in self.dependencies],
        }

    def canonical_bytes(self) -> bytes:
        """Return deterministic canonical bytes for hashing and persistence."""

        try:
            return canonical_dumps(self.as_dict(), limits=DEFAULT_PREFAB_LIMITS.scene.json_limits())
        except LudoWeaveError as error:
            raise _prefab_error(
                "prefab document could not be encoded within canonical limits",
                code="prefab.invalid_document",
                phase="encode",
                details={"cause_code": error.code},
            ) from error


@dataclass(frozen=True, slots=True)
class PrefabOverride:
    """One current-schema field replacement against a stable local entity."""

    local_id: str
    qualified_name: str
    version: int
    changes: Mapping[str, FrozenJsonValue]

    def __post_init__(self) -> None:
        _local_id(self.local_id, field="local_id", phase="construct")
        if (
            type(self.qualified_name) is not str
            or _COMPONENT_NAME.fullmatch(self.qualified_name) is None
        ):
            raise _prefab_error(
                "prefab override component must be module-qualified stable text",
                code="prefab.invalid_override",
                phase="construct",
                details={"field": "component"},
            )
        if type(self.version) is not int or self.version <= 0:
            raise _prefab_error(
                "prefab override version must be an exact positive integer",
                code="prefab.invalid_override",
                phase="construct",
                details={"field": "version", "actual_type": type(self.version).__name__},
            )
        try:
            frozen = freeze_json_object(self.changes)
        except LudoWeaveError as error:
            raise _prefab_error(
                "prefab override changes must be a canonical JSON object",
                code="prefab.invalid_override",
                phase="construct",
                details={"cause_code": error.code},
            ) from error
        if not frozen:
            raise _prefab_error(
                "prefab override changes must not be empty",
                code="prefab.invalid_override",
                phase="construct",
                details={"field": "changes"},
            )
        object.__setattr__(self, "changes", frozen)

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "local_id": self.local_id,
            "component": self.qualified_name,
            "version": self.version,
            "changes": thaw_json(cast(FrozenJsonValue, self.changes)),
        }


@dataclass(frozen=True, slots=True)
class PrefabInstance:
    """One explicit prefab source identity and detached override set."""

    prefab_id: str
    instance_id: str
    overrides: tuple[PrefabOverride, ...]
    protocol: str = PREFAB_INSTANCE_PROTOCOL

    def __post_init__(self) -> None:
        if type(self.protocol) is not str or self.protocol != PREFAB_INSTANCE_PROTOCOL:
            raise _prefab_error(
                "prefab instance protocol is unsupported",
                code="prefab.incompatible_protocol",
                phase="construct",
                details={"actual_type": type(self.protocol).__name__},
            )
        _stable_id(self.prefab_id, field="prefab_id", phase="construct")
        _stable_id(self.instance_id, field="instance_id", phase="construct")
        if type(self.overrides) is not tuple or any(
            type(item) is not PrefabOverride for item in self.overrides
        ):
            raise _prefab_error(
                "prefab overrides must be exact PrefabOverride values",
                code="prefab.invalid_override",
                phase="construct",
                details={"field": "overrides"},
            )
        keys = tuple((item.local_id, item.qualified_name) for item in self.overrides)
        if len(set(keys)) != len(keys):
            raise _prefab_error(
                "prefab instance repeats an entity/component override target",
                code="prefab.duplicate_override",
                phase="construct",
                details={"field": "overrides"},
            )
        object.__setattr__(
            self,
            "overrides",
            tuple(sorted(self.overrides, key=lambda item: (item.local_id, item.qualified_name))),
        )

    @classmethod
    def from_json(
        cls,
        document: str | bytes,
        *,
        limits: PrefabLimits = DEFAULT_PREFAB_LIMITS,
    ) -> "PrefabInstance":
        """Decode one bounded canonical-JSON prefab instance request."""

        checked_limits = _require_limits(limits)
        try:
            value = canonical_loads(document, limits=checked_limits.scene.json_limits())
        except LudoWeaveError as error:
            raise _prefab_error(
                "prefab instance JSON could not be decoded canonically",
                code="prefab.invalid_json",
                phase="decode",
                details={"cause_code": error.code},
            ) from error
        return cls._from_checked(value, limits=checked_limits)

    @classmethod
    def from_mapping(
        cls,
        value: object,
        *,
        limits: PrefabLimits = DEFAULT_PREFAB_LIMITS,
    ) -> "PrefabInstance":
        """Validate and detach one decoded prefab instance request."""

        checked_limits = _require_limits(limits)
        try:
            encoded = canonical_dumps(value, limits=checked_limits.scene.json_limits())
            checked = canonical_loads(encoded, limits=checked_limits.scene.json_limits())
        except LudoWeaveError as error:
            raise _prefab_error(
                "prefab instance is outside the bounded canonical JSON domain",
                code="prefab.invalid_document",
                phase="decode",
                details={"cause_code": error.code},
            ) from error
        return cls._from_checked(checked, limits=checked_limits)

    @classmethod
    def _from_checked(cls, value: object, *, limits: PrefabLimits) -> "PrefabInstance":
        document = _object(value, role="prefab instance")
        _exact_fields(
            document,
            required={"$schema", "prefab_id", "instance_id", "overrides"},
            role="prefab instance",
        )
        protocol = _text(document["$schema"], field="$schema")
        if protocol != PREFAB_INSTANCE_PROTOCOL:
            raise _prefab_error(
                "prefab instance protocol is unsupported",
                code="prefab.incompatible_protocol",
                phase="decode",
                details={"protocol": protocol},
            )
        raw_overrides = document["overrides"]
        if not isinstance(raw_overrides, list):
            raise _field_error("overrides", raw_overrides, "array")
        override_values = cast(list[object], raw_overrides)
        if len(override_values) > limits.max_overrides:
            raise _prefab_error(
                "prefab instance exceeds its override limit",
                code="prefab.limit_exceeded",
                phase="decode",
                details={
                    "field": "overrides",
                    "actual": len(override_values),
                    "limit": limits.max_overrides,
                },
            )
        return cls(
            protocol=protocol,
            prefab_id=_stable_id(document["prefab_id"], field="prefab_id"),
            instance_id=_stable_id(document["instance_id"], field="instance_id"),
            overrides=tuple(_override(item, limits=limits) for item in override_values),
        )

    def as_dict(self) -> dict[str, JsonValue]:
        """Return a detached ordinary JSON representation."""

        return {
            "$schema": self.protocol,
            "prefab_id": self.prefab_id,
            "instance_id": self.instance_id,
            "overrides": [item.as_dict() for item in self.overrides],
        }

    def canonical_bytes(self) -> bytes:
        """Return deterministic canonical bytes for hashing and persistence."""

        try:
            return canonical_dumps(self.as_dict(), limits=DEFAULT_PREFAB_LIMITS.scene.json_limits())
        except LudoWeaveError as error:
            raise _prefab_error(
                "prefab instance could not be encoded within canonical limits",
                code="prefab.invalid_document",
                phase="encode",
                details={"cause_code": error.code},
            ) from error


@component(type_id=_PREFAB_NODE_TYPE_ID)
@dataclass(frozen=True, slots=True)
class PrefabNode:
    """Canonical prefab source provenance stored with each instance entity."""

    prefab_id: str
    instance_id: str
    local_id: str


@dataclass(frozen=True, slots=True)
class PrefabInstantiationPlan:
    """A detached one-level prefab plan ready for transaction application."""

    prefab_id: str
    instance_id: str
    dependencies: tuple[AssetUri, ...]
    transaction: CommandTransaction


def compile_prefab(
    prefab: PrefabDocument,
    instance: PrefabInstance,
    *,
    registry: ComponentRegistry,
    world_id: str,
    transaction_id: str,
    actor: CommandActor,
    expected_world_hash: str | None = None,
    dry_run: bool = False,
) -> PrefabInstantiationPlan:
    """Compile one prefab instance into ordinary ``entity.spawn`` commands."""

    if type(prefab) is not PrefabDocument:
        raise _plan_error(
            "prefab planning requires an exact PrefabDocument value",
            code="prefab.invalid_plan",
            details={"field": "prefab", "actual_type": type(prefab).__name__},
        )
    if type(instance) is not PrefabInstance:
        raise _plan_error(
            "prefab planning requires an exact PrefabInstance value",
            code="prefab.invalid_plan",
            details={"field": "instance", "actual_type": type(instance).__name__},
        )
    if type(registry) is not ComponentRegistry:
        raise _plan_error(
            "prefab planning requires an exact ComponentRegistry value",
            code="prefab.registry_mismatch",
            details={"actual_type": type(registry).__name__},
        )
    if prefab.prefab_id != instance.prefab_id:
        raise _plan_error(
            "prefab instance source identity does not match the fragment",
            code="prefab.source_mismatch",
            details={"prefab_id": prefab.prefab_id, "instance_prefab_id": instance.prefab_id},
        )
    prefab_node_schema = _prefab_node_schema(registry)
    reserved = {prefab_node_schema.qualified_name}
    try:
        reserved.add(registry.schema_for_type(SceneNode).qualified_name)
    except LudoWeaveError as error:
        raise _plan_error(
            "prefab planning registry must explicitly contain SceneNode",
            code="prefab.registry_mismatch",
            details={"cause_code": error.code},
        ) from error
    for entity in prefab.entities:
        for component_value in entity.components:
            if component_value.qualified_name in reserved:
                raise _plan_error(
                    "prefab provenance components are compiler-owned",
                    code="prefab.reserved_component",
                    details={"component": component_value.qualified_name},
                )

    override_index = {(item.local_id, item.qualified_name): item for item in instance.overrides}
    entities_by_id = {item.local_id: item for item in prefab.entities}
    for override in instance.overrides:
        entity = entities_by_id.get(override.local_id)
        if entity is None:
            raise _plan_error(
                "prefab override targets an unknown local entity",
                code="prefab.unknown_target",
                details={"local_id": override.local_id},
            )
        if override.qualified_name not in {
            component_value.qualified_name for component_value in entity.components
        }:
            raise _plan_error(
                "prefab override targets a component absent from the fragment",
                code="prefab.missing_component",
                details={
                    "local_id": override.local_id,
                    "component": override.qualified_name,
                },
            )

    effective_entities: list[SceneEntity] = []
    for entity in prefab.entities:
        components: list[SceneComponent] = []
        for component_value in entity.components:
            override = override_index.get((entity.local_id, component_value.qualified_name))
            components.append(
                component_value
                if override is None
                else _apply_override(component_value, override=override, registry=registry)
            )
        node_values: dict[str, object] = {
            "prefab_id": prefab.prefab_id,
            "instance_id": instance.instance_id,
            "local_id": entity.local_id,
        }
        try:
            checked_node = registry.migrate(
                prefab_node_schema.type_id,
                from_version=prefab_node_schema.version,
                values=node_values,
            )
        except LudoWeaveError as error:
            raise _plan_error(
                "compiler-owned PrefabNode values do not match the registered schema",
                code="prefab.registry_mismatch",
                details={"cause_code": error.code},
            ) from error
        components.append(
            SceneComponent(
                prefab_node_schema.qualified_name,
                prefab_node_schema.version,
                cast(Mapping[str, FrozenJsonValue], checked_node),
            )
        )
        effective_entities.append(
            SceneEntity(entity.local_id, entity.name, entity.parent_local_id, tuple(components))
        )

    try:
        scene_plan = compile_scene(
            SceneDocument(
                scene_id=prefab.prefab_id,
                entities=tuple(effective_entities),
                dependencies=prefab.dependencies,
            ),
            registry=registry,
            world_id=world_id,
            transaction_id=transaction_id,
            actor=actor,
            instance_id=instance.instance_id,
            expected_world_hash=expected_world_hash,
            dry_run=dry_run,
        )
    except SceneError as error:
        raise _plan_error(
            "prefab instance could not compile into a scene transaction",
            code="prefab.invalid_plan",
            details={"cause_code": error.code},
        ) from error
    return PrefabInstantiationPlan(
        prefab_id=prefab.prefab_id,
        instance_id=instance.instance_id,
        dependencies=prefab.dependencies,
        transaction=scene_plan.transaction,
    )


def _prefab_node_schema(registry: ComponentRegistry) -> ComponentSchema:
    try:
        schema = registry.schema_for_type(PrefabNode)
    except LudoWeaveError as error:
        raise _plan_error(
            "prefab planning registry must explicitly contain PrefabNode",
            code="prefab.registry_mismatch",
            details={"cause_code": error.code},
        ) from error
    if schema.type_id != _PREFAB_NODE_TYPE_ID or schema.version != 1:
        raise _plan_error(
            "prefab planning registry contains an incompatible PrefabNode schema",
            code="prefab.registry_mismatch",
            details={"type_id": str(schema.type_id)},
        )
    return schema


def _apply_override(
    component_value: SceneComponent,
    *,
    override: PrefabOverride,
    registry: ComponentRegistry,
) -> SceneComponent:
    try:
        schema = registry.schema_for_name(component_value.qualified_name)
    except LudoWeaveError as error:
        raise _plan_error(
            "prefab names an unknown component schema",
            code="prefab.unknown_component",
            details={
                "component": component_value.qualified_name,
                "cause_code": error.code,
            },
        ) from error
    if override.version != schema.version:
        raise _plan_error(
            "prefab override requires the current component schema version",
            code="prefab.incompatible_override",
            details={
                "component": override.qualified_name,
                "version": override.version,
                "current_version": schema.version,
            },
        )
    base_values = thaw_json(cast(FrozenJsonValue, component_value.values))
    changes = thaw_json(cast(FrozenJsonValue, override.changes))
    assert isinstance(base_values, dict)
    assert isinstance(changes, dict)
    try:
        migrated = registry.migrate(
            schema.type_id,
            from_version=component_value.version,
            values=cast(dict[str, object], base_values),
        )
        merged = dict(migrated)
        merged.update(cast(dict[str, object], changes))
        checked = registry.migrate(
            schema.type_id,
            from_version=schema.version,
            values=merged,
        )
    except LudoWeaveError as error:
        raise _plan_error(
            "prefab override is incompatible with the component schema",
            code="prefab.invalid_override",
            details={"component": override.qualified_name, "cause_code": error.code},
        ) from error
    return SceneComponent(
        schema.qualified_name,
        schema.version,
        cast(Mapping[str, FrozenJsonValue], checked),
    )


def _override(value: object, *, limits: PrefabLimits) -> PrefabOverride:
    document = _object(value, role="prefab override")
    _exact_fields(
        document,
        required={"local_id", "component", "version", "changes"},
        role="prefab override",
    )
    changes = _object(document["changes"], role="prefab override changes")
    if len(changes) > limits.max_fields_per_override:
        raise _prefab_error(
            "prefab override exceeds its field limit",
            code="prefab.limit_exceeded",
            phase="decode",
            details={
                "field": "changes",
                "actual": len(changes),
                "limit": limits.max_fields_per_override,
            },
        )
    return PrefabOverride(
        local_id=_local_id(document["local_id"], field="local_id"),
        qualified_name=_component_name(document["component"]),
        version=_positive_int(document["version"], field="version"),
        changes=cast(Mapping[str, FrozenJsonValue], changes),
    )


def _require_limits(value: object) -> PrefabLimits:
    if type(value) is not PrefabLimits:
        raise _prefab_error(
            "prefab limits must be an exact PrefabLimits value",
            code="prefab.invalid_limits",
            phase="configure",
            details={"actual_type": type(value).__name__},
        )
    return value


def _object(value: object, *, role: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise _prefab_error(
            f"{role} must be an object",
            code="prefab.invalid_document",
            phase="decode",
            details={"role": role, "actual_type": type(value).__name__},
        )
    return cast(dict[str, object], value)


def _exact_fields(value: Mapping[str, object], *, required: set[str], role: str) -> None:
    if set(value) != required:
        raise _prefab_error(
            f"{role} must contain exact fields",
            code="prefab.invalid_document",
            phase="decode",
            details={
                "role": role,
                "missing": ",".join(sorted(required - set(value))),
                "unknown": ",".join(sorted(set(value) - required)),
            },
        )


def _text(value: object, *, field: str) -> str:
    if type(value) is not str:
        raise _field_error(field, value, "string")
    return value


def _stable_id(value: object, *, field: str, phase: str = "decode") -> str:
    if type(value) is not str or _STABLE_ID.fullmatch(value) is None:
        raise _field_error(field, value, "bounded stable ID", phase=phase)
    return value


def _local_id(value: object, *, field: str, phase: str = "decode") -> str:
    if type(value) is not str or _LOCAL_ID.fullmatch(value) is None:
        raise _field_error(field, value, "transaction-alias-compatible local ID", phase=phase)
    return value


def _component_name(value: object) -> str:
    if type(value) is not str or _COMPONENT_NAME.fullmatch(value) is None:
        raise _field_error("component", value, "module-qualified component name")
    return value


def _positive_int(value: object, *, field: str) -> int:
    if type(value) is not int or value <= 0:
        raise _field_error(field, value, "positive integer")
    return value


def _field_error(field: str, value: object, expected: str, *, phase: str = "decode") -> PrefabError:
    return _prefab_error(
        "prefab field has an invalid value",
        code="prefab.invalid_document",
        phase=phase,
        details={"field": field, "expected": expected, "actual_type": type(value).__name__},
    )


def _plan_error(
    message: str,
    *,
    code: str,
    details: Mapping[str, str | int | float | bool | None],
) -> PrefabError:
    return _prefab_error(message, code=code, phase="plan", details=details)


def _prefab_error(
    message: str,
    *,
    code: str,
    phase: str,
    details: Mapping[str, str | int | float | bool | None],
) -> PrefabError:
    return PrefabError(
        message,
        code=code,
        subsystem="scene",
        phase=phase,
        details=details,
    )
