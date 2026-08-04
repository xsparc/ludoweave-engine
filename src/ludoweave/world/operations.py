"""Typed built-in persistent operations decoded before transaction staging."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite
from typing import cast
from uuid import UUID

from ludoweave.ecs import ComponentRegistry, ComponentSchema, ComponentValueType, EntityId
from ludoweave.world.canonical import FrozenJsonValue, JsonValue, thaw_json
from ludoweave.world.command_schema import (
    BUILTIN_OPERATION_SPECS,
    CommandEnvelope,
    OperationRegistry,
)
from ludoweave.world.errors import TransactionValidationError
from ludoweave.world.resources import AuthorityResourceSchema, ResourceRole
from ludoweave.world.state import WorldSession

_ALIAS = re.compile(r"[A-Za-z][A-Za-z0-9_.:-]{0,127}\Z")
_BUILTIN_SPECS = {(spec.operation, spec.version): spec for spec in BUILTIN_OPERATION_SPECS}


@dataclass(frozen=True, slots=True)
class EntityReference:
    entity_id: EntityId | None = None
    alias: str | None = None

    def resolve(self, aliases: Mapping[str, EntityId]) -> EntityId:
        if self.entity_id is not None:
            return self.entity_id
        assert self.alias is not None
        entity_id = aliases.get(self.alias)
        if entity_id is None:
            raise _validation_error(
                "transaction-local entity alias has not been created",
                operation="resolve_entity",
                details={"alias": self.alias},
            )
        return entity_id


@dataclass(frozen=True, slots=True)
class SpawnOperation:
    components: tuple[object, ...]
    alias: str | None


@dataclass(frozen=True, slots=True)
class DestroyOperation:
    target: EntityReference


@dataclass(frozen=True, slots=True)
class AddComponentOperation:
    target: EntityReference
    component: object


@dataclass(frozen=True, slots=True)
class RemoveComponentOperation:
    target: EntityReference
    component_type: type[object]


@dataclass(frozen=True, slots=True)
class PatchComponentOperation:
    target: EntityReference
    component_type: type[object]
    changes: Mapping[str, JsonValue]


@dataclass(frozen=True, slots=True)
class PatchResourceOperation:
    schema: AuthorityResourceSchema[object]
    value: object


@dataclass(frozen=True, slots=True)
class TickOperation:
    count: int


type TypedOperation = (
    SpawnOperation
    | DestroyOperation
    | AddComponentOperation
    | RemoveComponentOperation
    | PatchComponentOperation
    | PatchResourceOperation
    | TickOperation
)


def parse_operation(
    envelope: CommandEnvelope,
    *,
    registry: OperationRegistry,
    session: WorldSession,
) -> TypedOperation:
    """Resolve and fully decode one built-in operation without mutating state."""

    resolved = registry.resolve(envelope.operation, envelope.operation_version)
    expected = _BUILTIN_SPECS.get((envelope.operation, envelope.operation_version))
    if expected is None or resolved != expected:
        raise _validation_error(
            "registered operation is not an exact implemented M2 contract",
            operation=envelope.operation,
            details={"version": envelope.operation_version},
        )
    arguments = cast(dict[str, object], thaw_json(cast(FrozenJsonValue, envelope.arguments)))
    operation = envelope.operation
    if operation == "entity.spawn":
        _exact_fields(arguments, required={"components"}, optional={"alias"}, operation=operation)
        alias_value = arguments.get("alias")
        alias = None if alias_value is None else _require_alias(alias_value, operation=operation)
        components = _decode_component_list(
            arguments["components"], registry=session.component_registry, operation=operation
        )
        return SpawnOperation(components, alias)
    if operation == "entity.destroy":
        _exact_fields(arguments, required={"entity"}, optional=set(), operation=operation)
        return DestroyOperation(_decode_entity(arguments["entity"], operation=operation))
    if operation == "component.add":
        _exact_fields(
            arguments, required={"entity", "component"}, optional=set(), operation=operation
        )
        component = _decode_component(
            arguments["component"], registry=session.component_registry, operation=operation
        )
        return AddComponentOperation(
            _decode_entity(arguments["entity"], operation=operation), component
        )
    if operation == "component.remove":
        _exact_fields(
            arguments, required={"entity", "type_id"}, optional=set(), operation=operation
        )
        component_type = _component_type(
            arguments["type_id"], registry=session.component_registry, operation=operation
        )
        return RemoveComponentOperation(
            _decode_entity(arguments["entity"], operation=operation), component_type
        )
    if operation == "component.patch":
        _exact_fields(
            arguments,
            required={"entity", "type_id", "version", "changes"},
            optional=set(),
            operation=operation,
        )
        component_type = _component_type(
            arguments["type_id"], registry=session.component_registry, operation=operation
        )
        schema = session.component_registry.schema_for_type(component_type)
        version = _require_positive_int(arguments["version"], field="version", operation=operation)
        if version != schema.version:
            raise _validation_error(
                "partial component patches require the current schema version",
                operation=operation,
                details={"type_id": str(schema.type_id), "version": version},
            )
        changes = arguments["changes"]
        if not isinstance(changes, dict) or not changes:
            raise _validation_error(
                "component patch changes must be a non-empty object",
                operation=operation,
                details={"field": "changes"},
            )
        checked_changes = cast(dict[str, object], changes)
        _validate_patch_changes(schema, checked_changes, operation=operation)
        return PatchComponentOperation(
            _decode_entity(arguments["entity"], operation=operation),
            component_type,
            cast(dict[str, JsonValue], checked_changes),
        )
    if operation == "resource.patch":
        _exact_fields(
            arguments,
            required={"type_id", "version", "value"},
            optional=set(),
            operation=operation,
        )
        type_id = _require_uuid(arguments["type_id"], field="type_id", operation=operation)
        resource_schema = session.authority_resources.schema_for_id(type_id)
        if resource_schema.role is not ResourceRole.STATE:
            raise _validation_error(
                "only authoritative state resources can be patched",
                operation=operation,
                details={"type_id": str(type_id)},
            )
        version = _require_positive_int(arguments["version"], field="version", operation=operation)
        if version != resource_schema.version:
            raise _validation_error(
                "resource patch requires the current schema version",
                operation=operation,
                details={"type_id": str(type_id), "version": version},
            )
        return PatchResourceOperation(resource_schema, resource_schema.decode(arguments["value"]))
    if operation == "world.tick":
        _exact_fields(arguments, required={"count"}, optional=set(), operation=operation)
        count = _require_positive_int(arguments["count"], field="count", operation=operation)
        if count != 1:
            raise _validation_error(
                "persistent tick commands advance exactly one branchable tick",
                operation=operation,
                details={"field": "count", "count": count},
            )
        return TickOperation(count)
    raise _validation_error(
        "registered operation has no built-in M2 handler",
        operation=operation,
        details={"version": envelope.operation_version},
    )


def _decode_component_list(
    value: object,
    *,
    registry: ComponentRegistry,
    operation: str,
) -> tuple[object, ...]:
    if not isinstance(value, list):
        raise _validation_error(
            "spawn components must be an array",
            operation=operation,
            details={"field": "components", "actual_type": type(value).__name__},
        )
    values = cast(list[object], value)
    components = tuple(
        _decode_component(item, registry=registry, operation=operation) for item in values
    )
    component_types = tuple(type(component) for component in components)
    if len(set(component_types)) != len(component_types):
        raise _validation_error(
            "spawn components must have unique type IDs",
            operation=operation,
            details={"field": "components"},
        )
    return components


def _decode_component(
    value: object,
    *,
    registry: ComponentRegistry,
    operation: str,
) -> object:
    if not isinstance(value, dict):
        raise _validation_error(
            "component payload must be an object",
            operation=operation,
            details={"field": "component", "actual_type": type(value).__name__},
        )
    payload = cast(dict[str, object], value)
    _exact_fields(
        payload,
        required={"type_id", "version", "values"},
        optional=set(),
        operation=operation,
    )
    type_id = _require_uuid(payload["type_id"], field="type_id", operation=operation)
    version = _require_positive_int(payload["version"], field="version", operation=operation)
    raw_values = payload["values"]
    if not isinstance(raw_values, dict):
        raise _validation_error(
            "component values must be an object",
            operation=operation,
            details={"field": "values", "actual_type": type(raw_values).__name__},
        )
    component_type = registry.component_type_for_id(type_id)
    migrated = registry.migrate(
        type_id,
        from_version=version,
        values=cast(dict[str, object], raw_values),
    )
    try:
        return component_type(**migrated)
    except Exception as error:
        raise _validation_error(
            "component values could not construct the registered type",
            operation=operation,
            details={"type_id": str(type_id), "cause_type": type(error).__name__},
        ) from error


def _decode_entity(value: object, *, operation: str) -> EntityReference:
    if not isinstance(value, dict):
        raise _validation_error(
            "entity reference must be an object",
            operation=operation,
            details={"field": "entity", "actual_type": type(value).__name__},
        )
    reference = cast(dict[str, object], value)
    if set(reference) == {"alias"}:
        return EntityReference(alias=_require_alias(reference["alias"], operation=operation))
    if set(reference) == {"index", "generation"}:
        index = _require_non_negative_int(reference["index"], field="index", operation=operation)
        generation = _require_non_negative_int(
            reference["generation"], field="generation", operation=operation
        )
        return EntityReference(entity_id=EntityId(index, generation))
    raise _validation_error(
        "entity reference must contain exactly an alias or index/generation",
        operation=operation,
        details={"field": "entity"},
    )


def _component_type(
    value: object,
    *,
    registry: ComponentRegistry,
    operation: str,
) -> type[object]:
    return registry.component_type_for_id(
        _require_uuid(value, field="type_id", operation=operation)
    )


def _validate_patch_changes(
    schema: ComponentSchema,
    changes: Mapping[str, object],
    *,
    operation: str,
) -> None:
    fields = {field.name: field for field in schema.fields}
    for name, value in changes.items():
        component_field = fields.get(name)
        if component_field is None:
            raise _validation_error(
                "component patch contains an unknown field",
                operation=operation,
                details={"field": name, "type_id": str(schema.type_id)},
            )
        if value is None:
            if component_field.allow_none:
                continue
            valid = False
        elif component_field.value_type is ComponentValueType.BOOL:
            valid = type(value) is bool
        elif component_field.value_type is ComponentValueType.INT:
            valid = type(value) is int
        elif component_field.value_type is ComponentValueType.FLOAT:
            valid = type(value) is float and isfinite(value)
        else:
            valid = type(value) is str
        if not valid:
            raise _validation_error(
                "component patch field has an invalid value",
                operation=operation,
                details={
                    "field": name,
                    "expected": component_field.value_type.value,
                    "actual_type": type(value).__name__,
                    "type_id": str(schema.type_id),
                },
            )


def _exact_fields(
    value: Mapping[str, object],
    *,
    required: set[str],
    optional: set[str],
    operation: str,
) -> None:
    missing = sorted(required - value.keys())
    unexpected = sorted(value.keys() - required - optional)
    if missing or unexpected:
        raise _validation_error(
            "operation arguments do not match the registered schema",
            operation=operation,
            details={"missing": ",".join(missing), "unexpected": ",".join(unexpected)},
        )


def _require_alias(value: object, *, operation: str) -> str:
    if type(value) is not str or _ALIAS.fullmatch(value) is None:
        raise _validation_error(
            "transaction-local alias must use bounded stable text",
            operation=operation,
            details={"field": "alias", "actual_type": type(value).__name__},
        )
    return value


def _require_uuid(value: object, *, field: str, operation: str) -> UUID:
    if type(value) is not str:
        raise _validation_error(
            "persistent type ID must be UUID text",
            operation=operation,
            details={"field": field, "actual_type": type(value).__name__},
        )
    try:
        type_id = UUID(value)
    except ValueError as error:
        raise _validation_error(
            "persistent type ID must be canonical UUID text",
            operation=operation,
            details={"field": field},
        ) from error
    if str(type_id) != value or type_id.int == 0:
        raise _validation_error(
            "persistent type ID must be canonical nonzero UUID text",
            operation=operation,
            details={"field": field},
        )
    return type_id


def _require_positive_int(value: object, *, field: str, operation: str) -> int:
    checked = _require_non_negative_int(value, field=field, operation=operation)
    if checked == 0:
        raise _validation_error(
            "operation value must be positive",
            operation=operation,
            details={"field": field},
        )
    return checked


def _require_non_negative_int(value: object, *, field: str, operation: str) -> int:
    if type(value) is not int or value < 0:
        raise _validation_error(
            "operation value must be a non-negative integer",
            operation=operation,
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _validation_error(
    message: str,
    *,
    operation: str,
    details: dict[str, str | int | float | bool | None],
) -> TransactionValidationError:
    return TransactionValidationError(
        message,
        code="world.transaction.validation_failed",
        subsystem="world",
        phase="validate",
        details={"operation": operation, **details},
    )
