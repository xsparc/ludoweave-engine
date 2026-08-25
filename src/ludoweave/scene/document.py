"""Bounded, immutable, versioned data-only scene documents."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast

from ludoweave.assets import AssetUri
from ludoweave.core.errors import LudoWeaveError
from ludoweave.scene.errors import SceneError
from ludoweave.world.canonical import (
    FrozenJsonValue,
    JsonLimits,
    JsonValue,
    canonical_dumps,
    canonical_loads,
    freeze_json_object,
    thaw_json,
)

SCENE_PROTOCOL = "ludoweave.scene/1"

_STABLE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_LOCAL_ID = re.compile(r"[A-Za-z][A-Za-z0-9._:-]{0,127}\Z")
_COMPONENT_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+\Z")
_MAX_BYTES = 4_194_304
_MAX_DEPTH = 32
_MAX_NODES = 200_000
_MAX_COLLECTION_ITEMS = 10_000
_MAX_STRING_BYTES = 262_144
_MAX_ENTITIES = 4_096
_MAX_DEPENDENCIES = 4_096
_MAX_COMPONENTS_PER_ENTITY = 256
_LIMIT_MAXIMA = (
    ("max_bytes", _MAX_BYTES),
    ("max_depth", _MAX_DEPTH),
    ("max_nodes", _MAX_NODES),
    ("max_collection_items", _MAX_COLLECTION_ITEMS),
    ("max_string_bytes", _MAX_STRING_BYTES),
    ("max_entities", _MAX_ENTITIES),
    ("max_dependencies", _MAX_DEPENDENCIES),
    ("max_components_per_entity", _MAX_COMPONENTS_PER_ENTITY),
)


@dataclass(frozen=True, slots=True)
class SceneLimits:
    """Deterministic resource limits applied before scene planning."""

    max_bytes: int = _MAX_BYTES
    max_depth: int = _MAX_DEPTH
    max_nodes: int = _MAX_NODES
    max_collection_items: int = _MAX_COLLECTION_ITEMS
    max_string_bytes: int = _MAX_STRING_BYTES
    max_entities: int = _MAX_ENTITIES
    max_dependencies: int = _MAX_DEPENDENCIES
    max_components_per_entity: int = _MAX_COMPONENTS_PER_ENTITY

    def __post_init__(self) -> None:
        for field, maximum in _LIMIT_MAXIMA:
            value = getattr(self, field)
            if type(value) is not int or value <= 0:
                raise _scene_error(
                    "scene limits must be exact positive integers",
                    code="scene.invalid_limits",
                    phase="configure",
                    details={"field": field, "actual_type": type(value).__name__},
                )
            if value > maximum:
                raise _scene_error(
                    "scene limits may tighten but not exceed hard maxima",
                    code="scene.invalid_limits",
                    phase="configure",
                    details={"field": field, "actual": value, "maximum": maximum},
                )

    def json_limits(self) -> JsonLimits:
        """Return the corresponding shared canonical-JSON limits."""

        return JsonLimits(
            max_bytes=self.max_bytes,
            max_depth=self.max_depth,
            max_nodes=self.max_nodes,
            max_collection_items=self.max_collection_items,
            max_string_bytes=self.max_string_bytes,
        )


DEFAULT_SCENE_LIMITS = SceneLimits()


@dataclass(frozen=True, slots=True)
class SceneComponent:
    """One versioned component value addressed by qualified schema name."""

    qualified_name: str
    version: int
    values: Mapping[str, FrozenJsonValue]

    def __post_init__(self) -> None:
        if (
            type(self.qualified_name) is not str
            or _COMPONENT_NAME.fullmatch(self.qualified_name) is None
        ):
            raise _scene_error(
                "scene component name must be module-qualified stable text",
                code="scene.invalid_component",
                phase="construct",
                details={"field": "qualified_name"},
            )
        _positive_int(self.version, field="version")
        try:
            frozen = freeze_json_object(self.values)
        except LudoWeaveError as error:
            raise _scene_error(
                "scene component values must be a canonical JSON object",
                code="scene.invalid_component",
                phase="construct",
                details={"component": self.qualified_name, "cause_code": error.code},
            ) from error
        object.__setattr__(self, "values", frozen)

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "version": self.version,
            "values": thaw_json(cast(FrozenJsonValue, self.values)),
        }


@dataclass(frozen=True, slots=True)
class SceneEntity:
    """One named local entity declaration in canonical local-ID order."""

    local_id: str
    name: str
    parent_local_id: str | None
    components: tuple[SceneComponent, ...]

    def __post_init__(self) -> None:
        _local_id(self.local_id, field="local_id")
        _bounded_name(self.name)
        if self.parent_local_id is not None:
            _local_id(self.parent_local_id, field="parent_local_id")
        if self.parent_local_id == self.local_id:
            raise _scene_error(
                "scene entity cannot be its own parent",
                code="scene.invalid_parent",
                phase="construct",
                details={"local_id": self.local_id},
            )
        if type(self.components) is not tuple or any(
            type(item) is not SceneComponent for item in self.components
        ):
            raise _scene_error(
                "scene entity components must be exact SceneComponent values",
                code="scene.invalid_component",
                phase="construct",
                details={"field": "components"},
            )
        names = tuple(item.qualified_name for item in self.components)
        if len(set(names)) != len(names):
            raise _scene_error(
                "scene entity repeats a component name",
                code="scene.invalid_component",
                phase="construct",
                details={"field": "components"},
            )
        object.__setattr__(
            self,
            "components",
            tuple(sorted(self.components, key=lambda item: item.qualified_name)),
        )

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "local_id": self.local_id,
            "name": self.name,
            "parent": self.parent_local_id,
            "components": {
                component.qualified_name: component.as_dict() for component in self.components
            },
        }


@dataclass(frozen=True, slots=True)
class SceneDocument:
    """A normalized scene description that owns no runtime entity state."""

    scene_id: str
    entities: tuple[SceneEntity, ...]
    dependencies: tuple[AssetUri, ...]
    protocol: str = SCENE_PROTOCOL

    def __post_init__(self) -> None:
        if type(self.protocol) is not str or self.protocol != SCENE_PROTOCOL:
            raise _scene_error(
                "scene protocol is unsupported",
                code="scene.incompatible_protocol",
                phase="construct",
                details={"actual_type": type(self.protocol).__name__},
            )
        _stable_id(self.scene_id, field="scene_id")
        if type(self.entities) is not tuple or any(
            type(item) is not SceneEntity for item in self.entities
        ):
            raise _scene_error(
                "scene entities must be exact SceneEntity values",
                code="scene.invalid_document",
                phase="construct",
                details={"field": "entities"},
            )
        local_ids = tuple(item.local_id for item in self.entities)
        names = tuple(item.name for item in self.entities)
        if len(set(local_ids)) != len(local_ids):
            raise _scene_error(
                "scene entities repeat a local ID",
                code="scene.duplicate_local_id",
                phase="construct",
                details={"field": "local_id"},
            )
        if len(set(names)) != len(names):
            raise _scene_error(
                "scene entity names must be unique",
                code="scene.duplicate_name",
                phase="construct",
                details={"field": "name"},
            )
        by_id = {entity.local_id: entity for entity in self.entities}
        for entity in self.entities:
            parent = entity.parent_local_id
            if parent is not None and parent not in by_id:
                raise _scene_error(
                    "scene entity parent does not exist",
                    code="scene.missing_parent",
                    phase="construct",
                    details={"local_id": entity.local_id, "parent": parent},
                )
        _require_acyclic(by_id)
        if type(self.dependencies) is not tuple or any(
            type(item) is not AssetUri for item in self.dependencies
        ):
            raise _scene_error(
                "scene dependencies must be exact AssetUri values",
                code="scene.invalid_asset_dependency",
                phase="construct",
                details={"field": "dependencies"},
            )
        if len(set(self.dependencies)) != len(self.dependencies):
            raise _scene_error(
                "scene dependencies repeat an asset URI",
                code="scene.duplicate_asset_dependency",
                phase="construct",
                details={"field": "dependencies"},
            )
        object.__setattr__(
            self,
            "entities",
            tuple(sorted(self.entities, key=lambda entity: entity.local_id)),
        )
        object.__setattr__(self, "dependencies", tuple(sorted(self.dependencies)))

    @classmethod
    def from_json(
        cls,
        document: str | bytes,
        *,
        limits: SceneLimits = DEFAULT_SCENE_LIMITS,
    ) -> SceneDocument:
        """Decode one bounded canonical-JSON scene document."""

        checked_limits = _require_limits(limits)
        try:
            value = canonical_loads(document, limits=checked_limits.json_limits())
        except LudoWeaveError as error:
            raise _scene_error(
                "scene JSON could not be decoded canonically",
                code="scene.invalid_json",
                phase="decode",
                details={"cause_code": error.code},
            ) from error
        return cls._from_checked(value, limits=checked_limits)

    @classmethod
    def from_mapping(
        cls,
        value: object,
        *,
        limits: SceneLimits = DEFAULT_SCENE_LIMITS,
    ) -> SceneDocument:
        """Validate and detach one decoded scene mapping."""

        checked_limits = _require_limits(limits)
        try:
            encoded = canonical_dumps(value, limits=checked_limits.json_limits())
            checked = canonical_loads(encoded, limits=checked_limits.json_limits())
        except LudoWeaveError as error:
            raise _scene_error(
                "scene document is outside the bounded canonical JSON domain",
                code="scene.invalid_document",
                phase="decode",
                details={"cause_code": error.code},
            ) from error
        return cls._from_checked(checked, limits=checked_limits)

    @classmethod
    def _from_checked(cls, value: object, *, limits: SceneLimits) -> SceneDocument:
        document = _object(value, role="scene")
        _exact_fields(
            document,
            required={"$schema", "scene_id", "entities", "dependencies"},
            role="scene",
        )
        protocol = _text(document["$schema"], field="$schema")
        if protocol != SCENE_PROTOCOL:
            raise _scene_error(
                "scene protocol is unsupported",
                code="scene.incompatible_protocol",
                phase="decode",
                details={"protocol": protocol},
            )
        scene_id = _stable_id(document["scene_id"], field="scene_id")
        entities = _entities(document["entities"], limits=limits)
        dependencies = _dependencies(document["dependencies"], limits=limits)
        return cls(
            protocol=protocol,
            scene_id=scene_id,
            entities=entities,
            dependencies=dependencies,
        )

    def as_dict(self) -> dict[str, JsonValue]:
        """Return a detached ordinary JSON representation."""

        return {
            "$schema": self.protocol,
            "scene_id": self.scene_id,
            "entities": [entity.as_dict() for entity in self.entities],
            "dependencies": [dependency.value for dependency in self.dependencies],
        }

    def canonical_bytes(self) -> bytes:
        """Return deterministic canonical bytes for hashing and persistence."""

        try:
            return canonical_dumps(self.as_dict(), limits=DEFAULT_SCENE_LIMITS.json_limits())
        except LudoWeaveError as error:
            raise _scene_error(
                "scene document could not be encoded within canonical limits",
                code="scene.invalid_document",
                phase="encode",
                details={"cause_code": error.code},
            ) from error


def _entities(value: object, *, limits: SceneLimits) -> tuple[SceneEntity, ...]:
    if not isinstance(value, list):
        raise _field_error("entities", value, "array")
    raw_entities = cast(list[object], value)
    if len(raw_entities) > limits.max_entities:
        raise _scene_error(
            "scene exceeds its entity limit",
            code="scene.limit_exceeded",
            phase="decode",
            details={
                "field": "entities",
                "actual": len(raw_entities),
                "limit": limits.max_entities,
            },
        )
    entities = tuple(_entity(item, limits=limits) for item in raw_entities)
    local_ids = tuple(entity.local_id for entity in entities)
    if len(set(local_ids)) != len(local_ids):
        raise _scene_error(
            "scene entities repeat a local ID",
            code="scene.duplicate_local_id",
            phase="decode",
            details={"field": "local_id"},
        )
    names = tuple(entity.name for entity in entities)
    if len(set(names)) != len(names):
        raise _scene_error(
            "scene entity names must be unique",
            code="scene.duplicate_name",
            phase="decode",
            details={"field": "name"},
        )
    by_id = {entity.local_id: entity for entity in entities}
    for entity in entities:
        parent = entity.parent_local_id
        if parent is not None and parent not in by_id:
            raise _scene_error(
                "scene entity parent does not exist",
                code="scene.missing_parent",
                phase="decode",
                details={"local_id": entity.local_id, "parent": parent},
            )
        if parent == entity.local_id:
            raise _scene_error(
                "scene entity cannot be its own parent",
                code="scene.invalid_parent",
                phase="decode",
                details={"local_id": entity.local_id},
            )
    _require_acyclic(by_id)
    return tuple(sorted(entities, key=lambda entity: entity.local_id))


def _entity(value: object, *, limits: SceneLimits) -> SceneEntity:
    document = _object(value, role="entity")
    _exact_fields(
        document,
        required={"local_id", "name", "parent", "components"},
        role="entity",
    )
    local_id = _local_id(document["local_id"], field="local_id")
    name = _bounded_name(document["name"])
    parent_value = document["parent"]
    parent = None if parent_value is None else _local_id(parent_value, field="parent")
    components = _components(document["components"], limits=limits)
    return SceneEntity(local_id, name, parent, components)


def _components(value: object, *, limits: SceneLimits) -> tuple[SceneComponent, ...]:
    document = _object(value, role="components")
    if len(document) > limits.max_components_per_entity:
        raise _scene_error(
            "scene entity exceeds its component limit",
            code="scene.limit_exceeded",
            phase="decode",
            details={
                "field": "components",
                "actual": len(document),
                "limit": limits.max_components_per_entity,
            },
        )
    components: list[SceneComponent] = []
    for qualified_name, raw_component in document.items():
        if _COMPONENT_NAME.fullmatch(qualified_name) is None:
            raise _scene_error(
                "scene component name must be module-qualified stable text",
                code="scene.invalid_component",
                phase="decode",
                details={"field": "component", "component": qualified_name},
            )
        component = _object(raw_component, role="component")
        _exact_fields(component, required={"version", "values"}, role="component")
        version = _positive_int(component["version"], field="version")
        try:
            values = freeze_json_object(component["values"])
        except LudoWeaveError as error:
            raise _scene_error(
                "scene component values must be a canonical JSON object",
                code="scene.invalid_component",
                phase="decode",
                details={"component": qualified_name, "cause_code": error.code},
            ) from error
        components.append(SceneComponent(qualified_name, version, values))
    return tuple(sorted(components, key=lambda component: component.qualified_name))


def _dependencies(value: object, *, limits: SceneLimits) -> tuple[AssetUri, ...]:
    if not isinstance(value, list):
        raise _field_error("dependencies", value, "array")
    raw_dependencies = cast(list[object], value)
    if len(raw_dependencies) > limits.max_dependencies:
        raise _scene_error(
            "scene exceeds its asset dependency limit",
            code="scene.limit_exceeded",
            phase="decode",
            details={
                "field": "dependencies",
                "actual": len(raw_dependencies),
                "limit": limits.max_dependencies,
            },
        )
    dependencies: list[AssetUri] = []
    for raw_dependency in raw_dependencies:
        if type(raw_dependency) is not str:
            raise _field_error("dependencies", raw_dependency, "asset URI string")
        try:
            dependencies.append(AssetUri(raw_dependency))
        except LudoWeaveError as error:
            raise _scene_error(
                "scene dependency must use canonical asset URI syntax",
                code="scene.invalid_asset_dependency",
                phase="decode",
                details={"cause_code": error.code},
            ) from error
    if len(set(dependencies)) != len(dependencies):
        raise _scene_error(
            "scene dependencies repeat an asset URI",
            code="scene.duplicate_asset_dependency",
            phase="decode",
            details={"field": "dependencies"},
        )
    return tuple(sorted(dependencies))


def _require_acyclic(by_id: Mapping[str, SceneEntity]) -> None:
    resolved: set[str] = set()
    for starting_id in sorted(by_id):
        path: set[str] = set()
        current: str | None = starting_id
        while current is not None and current not in resolved:
            if current in path:
                raise _scene_error(
                    "scene parent relationships contain a cycle",
                    code="scene.parent_cycle",
                    phase="decode",
                    details={"local_id": current},
                )
            path.add(current)
            current = by_id[current].parent_local_id
        resolved.update(path)


def _require_limits(value: object) -> SceneLimits:
    if type(value) is not SceneLimits:
        raise _scene_error(
            "scene limits must be an exact SceneLimits value",
            code="scene.invalid_limits",
            phase="configure",
            details={"actual_type": type(value).__name__},
        )
    return value


def _object(value: object, *, role: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise _scene_error(
            f"scene {role} must be an object",
            code="scene.invalid_document",
            phase="decode",
            details={"role": role, "actual_type": type(value).__name__},
        )
    return cast(dict[str, object], value)


def _exact_fields(value: Mapping[str, object], *, required: set[str], role: str) -> None:
    missing = sorted(required - value.keys())
    unexpected = sorted(value.keys() - required)
    if missing or unexpected:
        raise _scene_error(
            f"scene {role} fields do not match the schema",
            code="scene.invalid_document",
            phase="decode",
            details={
                "role": role,
                "missing": ",".join(missing),
                "unexpected": ",".join(unexpected),
            },
        )


def _text(value: object, *, field: str) -> str:
    if type(value) is not str:
        raise _field_error(field, value, "string")
    return value


def _stable_id(value: object, *, field: str) -> str:
    if type(value) is not str or _STABLE_ID.fullmatch(value) is None:
        raise _scene_error(
            "scene identity must use bounded stable text",
            code="scene.invalid_identity",
            phase="decode",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _local_id(value: object, *, field: str) -> str:
    if type(value) is not str or _LOCAL_ID.fullmatch(value) is None:
        raise _scene_error(
            "scene local ID must be a transaction-alias-compatible stable identifier",
            code="scene.invalid_local_id",
            phase="decode",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _bounded_name(value: object) -> str:
    if type(value) is not str or not value.strip():
        raise _scene_error(
            "scene entity name must be nonempty bounded text",
            code="scene.invalid_name",
            phase="decode",
            details={"field": "name", "actual_type": type(value).__name__},
        )
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError as error:
        raise _scene_error(
            "scene entity name must contain valid Unicode scalar text",
            code="scene.invalid_name",
            phase="decode",
            details={"field": "name"},
        ) from error
    if size > 256:
        raise _scene_error(
            "scene entity name must be nonempty bounded text",
            code="scene.invalid_name",
            phase="decode",
            details={"field": "name", "actual": size},
        )
    return value


def _positive_int(value: object, *, field: str) -> int:
    if type(value) is not int or value <= 0 or value > 2**63 - 1:
        raise _scene_error(
            "scene component version must be a positive signed 64-bit integer",
            code="scene.invalid_component",
            phase="decode",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _field_error(field: str, value: object, expected: str) -> SceneError:
    return _scene_error(
        "scene field has an invalid type",
        code="scene.invalid_document",
        phase="decode",
        details={
            "field": field,
            "expected": expected,
            "actual_type": type(value).__name__,
        },
    )


def _scene_error(
    message: str,
    *,
    code: str,
    phase: str,
    details: Mapping[str, str | int | float | bool | None],
) -> SceneError:
    return SceneError(
        message,
        code=code,
        subsystem="scene",
        phase=phase,
        details=details,
    )
