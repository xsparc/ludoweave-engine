"""Deliberately simple dictionary model for world-storage conformance tests."""

from __future__ import annotations

from collections.abc import Mapping
from math import isfinite
from typing import TypeVar, cast, overload

from ludoweave.core.errors import LudoWeaveError
from ludoweave.ecs.commands import (
    AddCommand,
    CommandBackend,
    Commands,
    DeferredCommand,
    DeferredEntity,
    DestroyCommand,
    EntityTarget,
    FlushResult,
    SpawnCommand,
)
from ludoweave.ecs.component import (
    ComponentField,
    ComponentRegistry,
    ComponentSchema,
    ComponentValueType,
)
from ludoweave.ecs.entity import EntityId
from ludoweave.ecs.errors import (
    ActiveQueryError,
    ComponentAlreadyPresentError,
    ComponentError,
    DeferredCommandError,
    InvalidComponentValueError,
    InvalidDeferredEntityError,
    InvalidEntityIdError,
    InvalidQueryError,
    MissingComponentError,
    StaleEntityError,
)
from ludoweave.ecs.query import (
    Query,
    QueryBackend,
    QueryOrder,
    QueryRowState,
    QuerySpec,
)

ComponentT = TypeVar("ComponentT")
ComponentT1 = TypeVar("ComponentT1")
ComponentT2 = TypeVar("ComponentT2")
ComponentT3 = TypeVar("ComponentT3")
ComponentT4 = TypeVar("ComponentT4")


class ReferenceWorld:
    """Independent dictionary oracle for the public world-storage contract.

    This model intentionally duplicates allocation, copying, patching, and
    epoch logic. It does not import the production allocator, dense table, or
    world implementation, so randomized comparison can expose those defects.
    """

    __slots__ = (
        "_active_read_queries",
        "_active_write_query",
        "_alive",
        "_changed_epochs",
        "_command_owner_identity",
        "_epoch",
        "_free",
        "_generations",
        "_registry",
        "_structural_epoch",
        "_table_structural_epochs",
        "_values",
    )

    def __init__(self, registry: ComponentRegistry) -> None:
        self._registry = registry
        self._active_read_queries = 0
        self._active_write_query = False
        self._command_owner_identity = object()
        self._generations: list[int] = []
        self._alive: set[EntityId] = set()
        self._free: list[int] = []
        self._values: dict[type[object], dict[EntityId, object]] = {
            component_type: {} for component_type in registry.component_types
        }
        self._changed_epochs: dict[type[object], dict[EntityId, int]] = {
            component_type: {} for component_type in registry.component_types
        }
        self._table_structural_epochs: dict[type[object], int] = {
            component_type: 0 for component_type in registry.component_types
        }
        self._epoch = 0
        self._structural_epoch = 0

    @property
    def registry(self) -> ComponentRegistry:
        return self._registry

    @property
    def epoch(self) -> int:
        return self._epoch

    @property
    def structural_epoch(self) -> int:
        return self._structural_epoch

    def spawn(self, *components: object) -> EntityId:
        self._require_mutation_allowed(operation="spawn")
        prepared: list[tuple[type[object], object]] = []
        seen: set[type[object]] = set()
        for component in components:
            component_type = type(component)
            schema = self._registry.schema_for_type(component_type)
            if component_type in seen:
                raise _reference_already_present_error(
                    operation="spawn", entity_id=None, schema=schema
                )
            seen.add(component_type)
            prepared.append(
                (
                    component_type,
                    _reference_copy_component(component, component_type, schema, operation="spawn"),
                )
            )

        if self._free:
            index = self._free.pop()
        else:
            index = len(self._generations)
            self._generations.append(0)
        entity_id = EntityId(index=index, generation=self._generations[index])
        next_epoch = self._epoch + 1
        self._alive.add(entity_id)
        for component_type, value in prepared:
            self._values[component_type][entity_id] = value
            self._changed_epochs[component_type][entity_id] = next_epoch
            self._table_structural_epochs[component_type] = next_epoch
        self._epoch = next_epoch
        self._structural_epoch = next_epoch
        return entity_id

    def destroy(self, entity_id: EntityId) -> None:
        self._require_mutation_allowed(operation="destroy")
        self._validate_entity(entity_id, operation="destroy")
        next_epoch = self._epoch + 1
        for component_type in self._registry.component_types:
            if entity_id in self._values[component_type]:
                del self._values[component_type][entity_id]
                del self._changed_epochs[component_type][entity_id]
                self._table_structural_epochs[component_type] = next_epoch
        self._alive.remove(entity_id)
        self._generations[entity_id.index] += 1
        self._free.append(entity_id.index)
        self._epoch = next_epoch
        self._structural_epoch = next_epoch

    def add(self, entity_id: EntityId, component: ComponentT) -> ComponentT:
        self._require_mutation_allowed(operation="add")
        self._validate_entity(entity_id, operation="add")
        component_type = type(component)
        schema = self._registry.schema_for_type(component_type)
        values = self._values[component_type]
        if entity_id in values:
            raise _reference_already_present_error(
                operation="add", entity_id=entity_id, schema=schema
            )
        canonical = _reference_copy_component(component, component_type, schema, operation="add")
        result = _reference_copy_component(canonical, component_type, schema, operation="add")
        next_epoch = self._epoch + 1
        values[entity_id] = canonical
        self._changed_epochs[component_type][entity_id] = next_epoch
        self._table_structural_epochs[component_type] = next_epoch
        self._epoch = next_epoch
        self._structural_epoch = next_epoch
        return cast(ComponentT, result)

    def replace(self, entity_id: EntityId, component: ComponentT) -> ComponentT:
        self._require_mutation_allowed(operation="replace")
        self._validate_entity(entity_id, operation="replace")
        component_type = type(component)
        schema = self._registry.schema_for_type(component_type)
        values = self._values[component_type]
        if entity_id not in values:
            raise _reference_missing_error(operation="replace", entity_id=entity_id, schema=schema)
        canonical = _reference_copy_component(
            component, component_type, schema, operation="replace"
        )
        result = _reference_copy_component(canonical, component_type, schema, operation="replace")
        next_epoch = self._epoch + 1
        values[entity_id] = canonical
        self._changed_epochs[component_type][entity_id] = next_epoch
        self._epoch = next_epoch
        return cast(ComponentT, result)

    def patch(
        self,
        entity_id: EntityId,
        component_type: type[ComponentT],
        **changes: object,
    ) -> ComponentT:
        self._require_mutation_allowed(operation="patch")
        self._validate_entity(entity_id, operation="patch")
        schema = self._registry.schema_for_type(component_type)
        values = self._values[component_type]
        if entity_id not in values:
            raise _reference_missing_error(operation="patch", entity_id=entity_id, schema=schema)
        if not changes:
            raise _reference_invalid_value_error(
                "component patch must include at least one field",
                operation="patch",
                schema=schema,
                details={"reason": "empty_patch"},
            )
        known_fields = {field.name for field in schema.fields}
        unexpected = tuple(sorted(set(changes) - known_fields))
        if unexpected:
            raise _reference_invalid_value_error(
                "component patch contains unknown fields",
                operation="patch",
                schema=schema,
                details={"unexpected_fields": ",".join(unexpected)},
            )
        try:
            replacement = _reference_copy_component(
                values[entity_id], component_type, schema, operation="patch"
            )
            for name, value in changes.items():
                object.__setattr__(replacement, name, value)
        except Exception as error:
            raise _reference_invalid_value_error(
                "component patch could not construct a replacement",
                operation="patch",
                schema=schema,
                details={"cause_type": type(error).__name__},
            ) from error
        canonical = _reference_copy_component(
            replacement, component_type, schema, operation="patch"
        )
        result = _reference_copy_component(canonical, component_type, schema, operation="patch")
        next_epoch = self._epoch + 1
        values[entity_id] = canonical
        self._changed_epochs[component_type][entity_id] = next_epoch
        self._epoch = next_epoch
        return cast(ComponentT, result)

    def remove(self, entity_id: EntityId, component_type: type[ComponentT]) -> ComponentT:
        self._require_mutation_allowed(operation="remove")
        self._validate_entity(entity_id, operation="remove")
        schema = self._registry.schema_for_type(component_type)
        values = self._values[component_type]
        if entity_id not in values:
            raise _reference_missing_error(operation="remove", entity_id=entity_id, schema=schema)
        result = _reference_copy_component(
            values[entity_id], component_type, schema, operation="remove"
        )
        next_epoch = self._epoch + 1
        del values[entity_id]
        del self._changed_epochs[component_type][entity_id]
        self._table_structural_epochs[component_type] = next_epoch
        self._epoch = next_epoch
        self._structural_epoch = next_epoch
        return cast(ComponentT, result)

    def has(self, entity_id: EntityId, component_type: type[object]) -> bool:
        self._validate_entity(entity_id, operation="has")
        self._registry.schema_for_type(component_type)
        return entity_id in self._values[component_type]

    def get(self, entity_id: EntityId, component_type: type[ComponentT]) -> ComponentT:
        self._validate_entity(entity_id, operation="get")
        schema = self._registry.schema_for_type(component_type)
        values = self._values[component_type]
        if entity_id not in values:
            raise _reference_missing_error(operation="get", entity_id=entity_id, schema=schema)
        copied = _reference_copy_component(
            values[entity_id], component_type, schema, operation="get"
        )
        return cast(ComponentT, copied)

    def entities(self) -> tuple[EntityId, ...]:
        return tuple(sorted(self._alive, key=EntityId.as_tuple))

    def components(
        self, component_type: type[ComponentT]
    ) -> tuple[tuple[EntityId, ComponentT], ...]:
        schema = self._registry.schema_for_type(component_type)
        copied = (
            (
                entity_id,
                cast(
                    ComponentT,
                    _reference_copy_component(
                        value, component_type, schema, operation="components"
                    ),
                ),
            )
            for entity_id, value in self._values[component_type].items()
        )
        return tuple(sorted(copied, key=lambda item: item[0].as_tuple()))

    def component_epoch(self, entity_id: EntityId, component_type: type[object]) -> int:
        self._validate_entity(entity_id, operation="component_epoch")
        schema = self._registry.schema_for_type(component_type)
        changed = self._changed_epochs[component_type]
        if entity_id not in changed:
            raise _reference_missing_error(
                operation="component_epoch", entity_id=entity_id, schema=schema
            )
        return changed[entity_id]

    def component_structural_epoch(self, component_type: type[object]) -> int:
        self._registry.schema_for_type(component_type)
        return self._table_structural_epochs[component_type]

    @overload
    def query(self) -> Query[()]: ...

    @overload
    def query(self, component_1: type[ComponentT1], /) -> Query[ComponentT1]: ...

    @overload
    def query(
        self,
        component_1: type[ComponentT1],
        component_2: type[ComponentT2],
        /,
    ) -> Query[ComponentT1, ComponentT2]: ...

    @overload
    def query(
        self,
        component_1: type[ComponentT1],
        component_2: type[ComponentT2],
        component_3: type[ComponentT3],
        /,
    ) -> Query[ComponentT1, ComponentT2, ComponentT3]: ...

    @overload
    def query(
        self,
        component_1: type[ComponentT1],
        component_2: type[ComponentT2],
        component_3: type[ComponentT3],
        component_4: type[ComponentT4],
        /,
    ) -> Query[ComponentT1, ComponentT2, ComponentT3, ComponentT4]: ...

    @overload
    def query(
        self,
        component_1: type[object],
        component_2: type[object],
        component_3: type[object],
        component_4: type[object],
        component_5: type[object],
        /,
        *component_types: type[object],
    ) -> Query[*tuple[object, ...]]: ...

    def query(self, *component_types: type[object]) -> object:
        spec = self._make_query_spec(component_types)
        return Query[object](cast(QueryBackend, self), spec)

    def _make_query_spec(
        self,
        included: tuple[object, ...],
        *,
        excluded: tuple[object, ...] = (),
        writable: tuple[object, ...] = (),
        changed_since: int | None = None,
        changed_types: tuple[object, ...] = (),
        order: QueryOrder = QueryOrder.NATIVE,
    ) -> QuerySpec:
        checked_included = self._validate_query_types(included, role="include")
        checked_excluded = self._validate_query_types(excluded, role="exclude")
        checked_writable = self._validate_query_types(writable, role="write")
        checked_changed = self._validate_query_types(changed_types, role="changed")
        included_set = set(checked_included)
        overlap = included_set.intersection(checked_excluded)
        if overlap:
            raise _reference_invalid_query_error(
                "included and excluded query types must be disjoint",
                phase="build",
                details={"component_type": self._type_names(overlap)},
            )
        if not set(checked_writable) <= included_set:
            raise _reference_invalid_query_error(
                "writable query types must be included",
                phase="build",
                details={"role": "write"},
            )
        frozen = tuple(
            item for item in checked_writable if self._registry.schema_for_type(item).frozen
        )
        if frozen:
            raise _reference_invalid_query_error(
                "frozen component types cannot be query-writable",
                phase="build",
                details={"component_type": self._type_names(frozen)},
            )
        if changed_since is None:
            if checked_changed:
                raise _reference_invalid_query_error(
                    "changed query types require a changed-since epoch",
                    phase="build",
                    details={"role": "changed"},
                )
        elif type(changed_since) is not int or changed_since < 0:
            raise _reference_invalid_query_error(
                "changed-since epoch must be a non-negative integer",
                phase="build",
                details={"actual_type": type(changed_since).__name__},
            )
        elif not checked_changed:
            raise _reference_invalid_query_error(
                "changed filtering requires at least one included type",
                phase="build",
                details={"role": "changed"},
            )
        if not set(checked_changed) <= included_set:
            raise _reference_invalid_query_error(
                "changed query types must be included",
                phase="build",
                details={"role": "changed"},
            )
        return QuerySpec(
            included=checked_included,
            excluded=self._sort_query_types(checked_excluded),
            writable=self._sort_query_types(checked_writable),
            changed_since=changed_since,
            changed_types=self._sort_query_types(checked_changed),
            order=order,
        )

    def _open_query(self, spec: QuerySpec) -> tuple[QueryRowState, ...]:
        writable = bool(spec.writable)
        if writable:
            if self._active_write_query or self._active_read_queries:
                raise _reference_active_query_error(
                    "writable query cannot overlap another active query",
                    operation="query_open",
                )
            self._active_write_query = True
        else:
            if self._active_write_query:
                raise _reference_active_query_error(
                    "read-only query cannot overlap an active writable query",
                    operation="query_open",
                )
            self._active_read_queries += 1
        try:
            if spec.changed_since is not None and spec.changed_since > self._epoch:
                raise _reference_invalid_query_error(
                    "changed-since epoch cannot be later than query activation",
                    phase="open",
                    details={"epoch": spec.changed_since, "world_epoch": self._epoch},
                )
            if spec.included:
                driver = min(
                    spec.included,
                    key=lambda item: (
                        len(self._values[item]),
                        self._registry.schema_for_type(item).type_id.bytes,
                    ),
                )
                candidates = tuple(self._values[driver])
            else:
                candidates = tuple(self._alive)
            matched = tuple(
                entity_id for entity_id in candidates if self._matches_query(entity_id, spec)
            )
            if spec.order is QueryOrder.STABLE:
                matched = tuple(sorted(matched, key=EntityId.as_tuple))
            rows: list[QueryRowState] = []
            for entity_id in matched:
                values: list[object] = []
                signatures: list[tuple[object, ...]] = []
                for component_type in spec.included:
                    schema = self._registry.schema_for_type(component_type)
                    value = _reference_copy_component(
                        self._values[component_type][entity_id],
                        component_type,
                        schema,
                        operation="query_read",
                    )
                    values.append(value)
                    signatures.append(
                        _reference_component_signature(value, schema, operation="query_read")
                    )
                rows.append(QueryRowState(entity_id, tuple(values), tuple(signatures)))
            return tuple(rows)
        except Exception:
            self._release_query(spec)
            raise

    def _commit_query_row(self, spec: QuerySpec, row: QueryRowState) -> None:
        self._validate_entity(row.entity_id, operation="query_writeback")
        prepared: list[tuple[type[object], object]] = []
        included_indexes = {item: index for index, item in enumerate(spec.included)}
        for component_type in spec.writable:
            index = included_indexes[component_type]
            schema = self._registry.schema_for_type(component_type)
            canonical = _reference_copy_component(
                row.values[index],
                component_type,
                schema,
                operation="query_writeback",
            )
            signature = _reference_component_signature(
                canonical, schema, operation="query_writeback"
            )
            if signature != row.signatures[index]:
                prepared.append((component_type, canonical))
        if not prepared:
            return
        next_epoch = self._epoch + 1
        for component_type, canonical in prepared:
            if row.entity_id not in self._values[component_type]:
                raise _reference_missing_error(
                    operation="query_writeback",
                    entity_id=row.entity_id,
                    schema=self._registry.schema_for_type(component_type),
                )
            self._values[component_type][row.entity_id] = canonical
            self._changed_epochs[component_type][row.entity_id] = next_epoch
        self._epoch = next_epoch

    def _release_query(self, spec: QuerySpec) -> None:
        if spec.writable:
            self._active_write_query = False
        elif self._active_read_queries > 0:
            self._active_read_queries -= 1

    @property
    def _command_owner_token(self) -> object:
        return self._command_owner_identity

    def _copy_command_component(self, component: object, *, operation: str) -> object:
        component_type = type(component)
        schema = self._registry.schema_for_type(component_type)
        return _reference_copy_component(component, component_type, schema, operation=operation)

    def _validate_command_component_type(self, component_type: type[object]) -> None:
        self._registry.schema_for_type(component_type)

    def commands(self) -> Commands:
        return Commands(cast(CommandBackend, self))

    def flush(self, commands: Commands) -> FlushResult:
        self._require_mutation_allowed(operation="flush")
        records = commands._records_for(  # pyright: ignore[reportPrivateUsage]
            self._command_owner_identity
        )
        start_epoch = self._epoch
        if not records:
            commands._complete_flush()  # pyright: ignore[reportPrivateUsage]
            return FlushResult(0, start_epoch, start_epoch, ())
        staged = self.clone()
        resolutions: dict[DeferredEntity, EntityId] = {}
        for index, record in enumerate(records):
            try:
                staged._apply_deferred_command(record, resolutions)
            except Exception as error:
                cause_code = (
                    error.code if isinstance(error, LudoWeaveError) else type(error).__name__
                )
                raise DeferredCommandError(
                    "deferred structural command could not be applied",
                    code="ecs.deferred_command_failed",
                    subsystem="ecs",
                    phase="flush",
                    details={
                        "operation_index": index,
                        "operation_kind": _reference_command_kind(record),
                        "cause_code": cause_code,
                    },
                ) from error
        self._adopt_staged(staged)
        ordered_resolutions = tuple(
            (record.token, resolutions[record.token])
            for record in records
            if isinstance(record, SpawnCommand)
        )
        commands._complete_flush()  # pyright: ignore[reportPrivateUsage]
        return FlushResult(
            len(records),
            start_epoch,
            self._epoch,
            ordered_resolutions,
        )

    def clone(self) -> ReferenceWorld:
        self._require_mutation_allowed(operation="clone")
        duplicate = ReferenceWorld(self._registry)
        duplicate._generations = list(self._generations)
        duplicate._alive = set(self._alive)
        duplicate._free = list(self._free)
        duplicate._epoch = self._epoch
        duplicate._structural_epoch = self._structural_epoch
        duplicate._table_structural_epochs = dict(self._table_structural_epochs)
        for component_type in self._registry.component_types:
            schema = self._registry.schema_for_type(component_type)
            duplicate._values[component_type] = {
                entity_id: _reference_copy_component(
                    value, component_type, schema, operation="clone"
                )
                for entity_id, value in self._values[component_type].items()
            }
            duplicate._changed_epochs[component_type] = dict(self._changed_epochs[component_type])
        return duplicate

    def _validate_query_types(
        self, component_types: tuple[object, ...], *, role: str
    ) -> tuple[type[object], ...]:
        seen: set[type[object]] = set()
        checked: list[type[object]] = []
        for component_type in component_types:
            if not isinstance(component_type, type):
                raise _reference_invalid_query_error(
                    "query component entries must be types",
                    phase="build",
                    details={"role": role, "actual_type": type(component_type).__name__},
                )
            if component_type in seen:
                raise _reference_invalid_query_error(
                    "query component types must be unique within each role",
                    phase="build",
                    details={"role": role, "component_type": component_type.__name__},
                )
            try:
                self._registry.schema_for_type(component_type)
            except ComponentError as error:
                raise _reference_invalid_query_error(
                    "query component type is not registered",
                    phase="build",
                    details={"role": role, "component_type": component_type.__name__},
                ) from error
            seen.add(component_type)
            checked.append(component_type)
        return tuple(checked)

    def _sort_query_types(
        self, component_types: tuple[type[object], ...]
    ) -> tuple[type[object], ...]:
        return tuple(
            sorted(
                component_types,
                key=lambda item: self._registry.schema_for_type(item).type_id.bytes,
            )
        )

    def _type_names(self, component_types: set[type[object]] | tuple[type[object], ...]) -> str:
        return ",".join(
            self._registry.schema_for_type(item).qualified_name
            for item in self._sort_query_types(tuple(component_types))
        )

    def _matches_query(self, entity_id: EntityId, spec: QuerySpec) -> bool:
        if not all(entity_id in self._values[item] for item in spec.included):
            return False
        if any(entity_id in self._values[item] for item in spec.excluded):
            return False
        return spec.changed_since is None or any(
            self._changed_epochs[item][entity_id] > spec.changed_since
            for item in spec.changed_types
        )

    def _apply_deferred_command(
        self,
        record: DeferredCommand,
        resolutions: dict[DeferredEntity, EntityId],
    ) -> None:
        if isinstance(record, SpawnCommand):
            resolutions[record.token] = self.spawn(*record.components)
            return
        target = self._resolve_deferred_target(record.target, resolutions)
        if isinstance(record, DestroyCommand):
            self.destroy(target)
        elif isinstance(record, AddCommand):
            self.add(target, record.component)
        else:
            self.remove(target, record.component_type)

    def _resolve_deferred_target(
        self,
        target: EntityTarget,
        resolutions: dict[DeferredEntity, EntityId],
    ) -> EntityId:
        if isinstance(target, EntityId):
            return target
        resolved = resolutions.get(target)
        if resolved is None:
            raise InvalidDeferredEntityError(
                "deferred entity target has not been spawned in this flush",
                code="ecs.invalid_deferred_entity",
                subsystem="ecs",
                phase="flush",
                details={"ordinal": target.ordinal},
            )
        return resolved

    def _adopt_staged(self, staged: ReferenceWorld) -> None:
        self._generations = staged._generations
        self._alive = staged._alive
        self._free = staged._free
        self._values = staged._values
        self._changed_epochs = staged._changed_epochs
        self._table_structural_epochs = staged._table_structural_epochs
        self._epoch = staged._epoch
        self._structural_epoch = staged._structural_epoch

    def _require_mutation_allowed(self, *, operation: str) -> None:
        if self._active_write_query or self._active_read_queries:
            raise _reference_active_query_error(
                "world mutation is forbidden while a query cursor is active",
                operation=operation,
            )

    def _validate_entity(self, entity_id: object, *, operation: str) -> None:
        if not isinstance(entity_id, EntityId):
            raise InvalidEntityIdError(
                "public entity operations require an EntityId",
                code="ecs.invalid_entity_id",
                subsystem="ecs",
                phase=operation,
                details={"actual_type": type(entity_id).__name__},
            )
        checked = entity_id
        if checked.index >= len(self._generations):
            raise _reference_stale_error(
                checked,
                operation=operation,
                reason="unknown_index",
                current_generation=None,
            )
        current = self._generations[checked.index]
        if checked not in self._alive:
            slot_is_alive = any(item.index == checked.index for item in self._alive)
            reason = "generation_mismatch" if slot_is_alive else "not_alive"
            raise _reference_stale_error(
                checked,
                operation=operation,
                reason=reason,
                current_generation=current,
            )


def _reference_copy_component(
    value: object,
    component_type: type[object],
    schema: ComponentSchema,
    *,
    operation: str,
) -> object:
    if type(value) is not component_type:
        raise _reference_invalid_value_error(
            "component instance must have its exact registered type",
            operation=operation,
            schema=schema,
            details={"actual_type": type(value).__name__},
        )
    captured = tuple(
        (
            field.name,
            _reference_read_field(value, field, schema=schema, operation=operation),
        )
        for field in schema.fields
    )
    try:
        copied = object.__new__(component_type)
        for name, field_value in captured:
            object.__setattr__(copied, name, field_value)
        return copied
    except Exception as error:
        raise _reference_invalid_value_error(
            "component value could not be copied",
            operation=operation,
            schema=schema,
            details={"cause_type": type(error).__name__},
        ) from error


def _reference_read_field(
    value: object,
    field: ComponentField,
    *,
    schema: ComponentSchema,
    operation: str,
) -> object:
    try:
        actual = object.__getattribute__(value, field.name)
    except Exception as error:
        raise _reference_invalid_value_error(
            "component field could not be read",
            operation=operation,
            schema=schema,
            details={
                "field": field.name,
                "reason": "unreadable_field",
                "cause_type": type(error).__name__,
            },
        ) from error
    if actual is None and field.allow_none:
        return actual
    expected = {
        ComponentValueType.BOOL: bool,
        ComponentValueType.INT: int,
        ComponentValueType.FLOAT: float,
        ComponentValueType.STRING: str,
    }[field.value_type]
    if type(actual) is not expected or (isinstance(actual, float) and not isfinite(actual)):
        raise _reference_invalid_value_error(
            "component field value does not match its schema",
            operation=operation,
            schema=schema,
            details={
                "field": field.name,
                "expected_type": field.annotation,
                "actual_type": type(actual).__name__,
            },
        )
    return actual


def _reference_already_present_error(
    *, operation: str, entity_id: EntityId | None, schema: ComponentSchema
) -> ComponentAlreadyPresentError:
    return ComponentAlreadyPresentError(
        "entity already has this component type",
        code="ecs.component_already_present",
        subsystem="ecs",
        phase=operation,
        details={
            "component_type": schema.qualified_name,
            "entity_index": None if entity_id is None else entity_id.index,
            "entity_generation": None if entity_id is None else entity_id.generation,
        },
    )


def _reference_missing_error(
    *, operation: str, entity_id: EntityId, schema: ComponentSchema
) -> MissingComponentError:
    return MissingComponentError(
        "entity does not have this component type",
        code="ecs.missing_component",
        subsystem="ecs",
        phase=operation,
        details={
            "component_type": schema.qualified_name,
            "entity_index": entity_id.index,
            "entity_generation": entity_id.generation,
        },
    )


def _reference_invalid_value_error(
    message: str,
    *,
    operation: str,
    schema: ComponentSchema,
    details: Mapping[str, str | int | float | bool | None],
) -> InvalidComponentValueError:
    return InvalidComponentValueError(
        message,
        code="ecs.invalid_component_value",
        subsystem="ecs",
        phase=operation,
        details={"component_type": schema.qualified_name, **details},
    )


def _reference_stale_error(
    entity_id: EntityId,
    *,
    operation: str,
    reason: str,
    current_generation: int | None,
) -> StaleEntityError:
    return StaleEntityError(
        "entity ID does not identify a live entity",
        code="ecs.stale_entity",
        subsystem="ecs",
        phase=operation,
        details={
            "index": entity_id.index,
            "generation": entity_id.generation,
            "current_generation": current_generation,
            "reason": reason,
        },
    )


def _reference_component_signature(
    value: object, schema: ComponentSchema, *, operation: str
) -> tuple[object, ...]:
    return tuple(
        _reference_signature_value(
            _reference_read_field(value, field, schema=schema, operation=operation)
        )
        for field in schema.fields
    )


def _reference_signature_value(value: object) -> object:
    if type(value) is float:
        return value.hex()
    return value


def _reference_invalid_query_error(
    message: str,
    *,
    phase: str,
    details: Mapping[str, str | int | float | bool | None],
) -> InvalidQueryError:
    return InvalidQueryError(
        message,
        code="ecs.invalid_query",
        subsystem="ecs",
        phase=phase,
        details=details,
    )


def _reference_active_query_error(message: str, *, operation: str) -> ActiveQueryError:
    return ActiveQueryError(
        message,
        code="ecs.active_query",
        subsystem="ecs",
        phase=operation,
    )


def _reference_command_kind(record: DeferredCommand) -> str:
    if isinstance(record, SpawnCommand):
        return "spawn"
    if isinstance(record, DestroyCommand):
        return "destroy"
    if isinstance(record, AddCommand):
        return "add"
    return "remove"
