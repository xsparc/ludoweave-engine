"""Canonical storage-neutral world contract and dense/sparse implementation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite
from typing import Protocol, Self, TypeVar, cast, overload
from uuid import UUID

from ludoweave.core.errors import LudoWeaveError
from ludoweave.ecs._checkpoint import (
    ComponentRowCheckpoint,
    ComponentTableCheckpoint,
    EcsCheckpoint,
)
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
from ludoweave.ecs.entity import EntityAllocator, EntityId
from ludoweave.ecs.errors import (
    ActiveQueryError,
    ComponentAlreadyPresentError,
    ComponentError,
    DeferredCommandError,
    InvalidComponentValueError,
    InvalidDeferredEntityError,
    InvalidQueryError,
    InvalidWorldCheckpointError,
    MissingComponentError,
)
from ludoweave.ecs.query import (
    Query,
    QueryBackend,
    QueryOrder,
    QueryRowState,
    QuerySpec,
)
from ludoweave.ecs.storage import DenseComponentTable

ComponentT = TypeVar("ComponentT")
ComponentT1 = TypeVar("ComponentT1")
ComponentT2 = TypeVar("ComponentT2")
ComponentT3 = TypeVar("ComponentT3")
ComponentT4 = TypeVar("ComponentT4")


class WorldStore(Protocol):
    """Storage-neutral public contract for canonical entity/component state."""

    @property
    def registry(self) -> ComponentRegistry: ...

    @property
    def epoch(self) -> int: ...

    @property
    def structural_epoch(self) -> int: ...

    def spawn(self, *components: object) -> EntityId: ...

    def destroy(self, entity_id: EntityId) -> None: ...

    def add(self, entity_id: EntityId, component: ComponentT) -> ComponentT: ...

    def replace(self, entity_id: EntityId, component: ComponentT) -> ComponentT: ...

    def patch(
        self,
        entity_id: EntityId,
        component_type: type[ComponentT],
        **changes: object,
    ) -> ComponentT: ...

    def remove(self, entity_id: EntityId, component_type: type[ComponentT]) -> ComponentT: ...

    def has(self, entity_id: EntityId, component_type: type[object]) -> bool: ...

    def get(self, entity_id: EntityId, component_type: type[ComponentT]) -> ComponentT: ...

    def entities(self) -> tuple[EntityId, ...]: ...

    def components(
        self, component_type: type[ComponentT]
    ) -> tuple[tuple[EntityId, ComponentT], ...]: ...

    def component_epoch(self, entity_id: EntityId, component_type: type[object]) -> int: ...

    def component_structural_epoch(self, component_type: type[object]) -> int: ...

    def clone(self) -> Self: ...

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

    def commands(self) -> Commands: ...

    def flush(self, commands: Commands) -> FlushResult: ...


@dataclass(frozen=True, slots=True)
class _QueryKey:
    included: tuple[UUID, ...]
    excluded: tuple[UUID, ...]
    changed: tuple[UUID, ...]
    order: QueryOrder


@dataclass(frozen=True, slots=True)
class _QueryPlan:
    driver: type[object] | None
    structural_epoch: int


class World:
    """Own canonical world state behind private pure-Python dense/sparse tables.

    The world copies component values on every public input and output boundary.
    It is single-owner mutable simulation state and is not concurrently safe.
    """

    __slots__ = (
        "_active_read_queries",
        "_active_write_query",
        "_allocator",
        "_command_owner_identity",
        "_entities",
        "_epoch",
        "_query_plans",
        "_registry",
        "_structural_epoch",
        "_tables",
    )

    def __init__(self, registry: ComponentRegistry) -> None:
        self._registry = registry
        self._allocator = EntityAllocator()
        self._active_read_queries = 0
        self._active_write_query = False
        self._command_owner_identity = object()
        self._entities: set[EntityId] = set()
        self._tables = {
            component_type: DenseComponentTable() for component_type in registry.component_types
        }
        self._epoch = 0
        self._structural_epoch = 0
        self._query_plans: dict[_QueryKey, _QueryPlan] = {}

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
                raise _already_present_error(
                    operation="spawn",
                    entity_id=None,
                    schema=schema,
                )
            seen.add(component_type)
            prepared.append(
                (
                    component_type,
                    _copy_component(component, component_type, schema, operation="spawn"),
                )
            )

        entity_id = self._allocator.create()
        next_epoch = self._epoch + 1
        for component_type, value in prepared:
            self._tables[component_type].add(entity_id, value, epoch=next_epoch)
        self._entities.add(entity_id)
        self._epoch = next_epoch
        self._structural_epoch = next_epoch
        return entity_id

    def destroy(self, entity_id: EntityId) -> None:
        self._require_mutation_allowed(operation="destroy")
        self._validate_entity(entity_id, operation="destroy")
        next_epoch = self._epoch + 1
        for component_type in self._registry.component_types:
            table = self._tables[component_type]
            if table.contains(entity_id):
                table.remove(entity_id, epoch=next_epoch)
        self._allocator.destroy(entity_id)
        self._entities.remove(entity_id)
        self._epoch = next_epoch
        self._structural_epoch = next_epoch

    def add(self, entity_id: EntityId, component: ComponentT) -> ComponentT:
        self._require_mutation_allowed(operation="add")
        self._validate_entity(entity_id, operation="add")
        component_type = type(component)
        schema = self._registry.schema_for_type(component_type)
        table = self._tables[component_type]
        if table.contains(entity_id):
            raise _already_present_error(operation="add", entity_id=entity_id, schema=schema)
        canonical = _copy_component(component, component_type, schema, operation="add")
        result = _copy_component(canonical, component_type, schema, operation="add")
        next_epoch = self._epoch + 1
        table.add(entity_id, canonical, epoch=next_epoch)
        self._epoch = next_epoch
        self._structural_epoch = next_epoch
        return cast(ComponentT, result)

    def replace(self, entity_id: EntityId, component: ComponentT) -> ComponentT:
        self._require_mutation_allowed(operation="replace")
        self._validate_entity(entity_id, operation="replace")
        component_type = type(component)
        schema = self._registry.schema_for_type(component_type)
        table = self._tables[component_type]
        if not table.contains(entity_id):
            raise _missing_error(operation="replace", entity_id=entity_id, schema=schema)
        canonical = _copy_component(component, component_type, schema, operation="replace")
        result = _copy_component(canonical, component_type, schema, operation="replace")
        next_epoch = self._epoch + 1
        table.replace(entity_id, canonical, epoch=next_epoch)
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
        table = self._tables[component_type]
        if not table.contains(entity_id):
            raise _missing_error(operation="patch", entity_id=entity_id, schema=schema)
        if not changes:
            raise _invalid_value_error(
                "component patch must include at least one field",
                operation="patch",
                schema=schema,
                details={"reason": "empty_patch"},
            )
        known_fields = {field.name for field in schema.fields}
        unexpected = tuple(sorted(set(changes) - known_fields))
        if unexpected:
            raise _invalid_value_error(
                "component patch contains unknown fields",
                operation="patch",
                schema=schema,
                details={"unexpected_fields": ",".join(unexpected)},
            )
        current = table.get(entity_id)
        try:
            replacement = _copy_component(current, component_type, schema, operation="patch")
            for name, value in changes.items():
                object.__setattr__(replacement, name, value)
        except Exception as error:
            raise _invalid_value_error(
                "component patch could not construct a replacement",
                operation="patch",
                schema=schema,
                details={"cause_type": type(error).__name__},
            ) from error
        canonical = _copy_component(replacement, component_type, schema, operation="patch")
        result = _copy_component(canonical, component_type, schema, operation="patch")
        next_epoch = self._epoch + 1
        table.replace(entity_id, canonical, epoch=next_epoch)
        self._epoch = next_epoch
        return cast(ComponentT, result)

    def remove(self, entity_id: EntityId, component_type: type[ComponentT]) -> ComponentT:
        self._require_mutation_allowed(operation="remove")
        self._validate_entity(entity_id, operation="remove")
        schema = self._registry.schema_for_type(component_type)
        table = self._tables[component_type]
        if not table.contains(entity_id):
            raise _missing_error(operation="remove", entity_id=entity_id, schema=schema)
        result = _copy_component(table.get(entity_id), component_type, schema, operation="remove")
        next_epoch = self._epoch + 1
        table.remove(entity_id, epoch=next_epoch)
        self._epoch = next_epoch
        self._structural_epoch = next_epoch
        return cast(ComponentT, result)

    def has(self, entity_id: EntityId, component_type: type[object]) -> bool:
        self._validate_entity(entity_id, operation="has")
        self._registry.schema_for_type(component_type)
        return self._tables[component_type].contains(entity_id)

    def get(self, entity_id: EntityId, component_type: type[ComponentT]) -> ComponentT:
        self._validate_entity(entity_id, operation="get")
        schema = self._registry.schema_for_type(component_type)
        table = self._tables[component_type]
        if not table.contains(entity_id):
            raise _missing_error(operation="get", entity_id=entity_id, schema=schema)
        value = _copy_component(table.get(entity_id), component_type, schema, operation="get")
        return cast(ComponentT, value)

    def entities(self) -> tuple[EntityId, ...]:
        return tuple(sorted(self._entities, key=EntityId.as_tuple))

    def components(
        self, component_type: type[ComponentT]
    ) -> tuple[tuple[EntityId, ComponentT], ...]:
        schema = self._registry.schema_for_type(component_type)
        table = self._tables[component_type]
        copied = (
            (
                entity_id,
                cast(
                    ComponentT,
                    _copy_component(value, component_type, schema, operation="components"),
                ),
            )
            for entity_id, value in table.items()
        )
        return tuple(sorted(copied, key=lambda item: item[0].as_tuple()))

    def component_epoch(self, entity_id: EntityId, component_type: type[object]) -> int:
        self._validate_entity(entity_id, operation="component_epoch")
        schema = self._registry.schema_for_type(component_type)
        table = self._tables[component_type]
        if not table.contains(entity_id):
            raise _missing_error(operation="component_epoch", entity_id=entity_id, schema=schema)
        return table.changed_epoch(entity_id)

    def component_structural_epoch(self, component_type: type[object]) -> int:
        self._registry.schema_for_type(component_type)
        return self._tables[component_type].structural_epoch

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
        """Build a storage-neutral query preserving caller component order."""

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
        """Validate and canonicalize a query builder specification."""

        checked_included = self._validate_query_types(included, role="include")
        checked_excluded = self._validate_query_types(excluded, role="exclude")
        checked_writable = self._validate_query_types(writable, role="write")
        checked_changed = self._validate_query_types(changed_types, role="changed")
        included_set = set(checked_included)
        overlap = included_set.intersection(checked_excluded)
        if overlap:
            raise _invalid_query_error(
                "included and excluded query types must be disjoint",
                phase="build",
                details={"component_type": self._type_names(overlap)},
            )
        if not set(checked_writable) <= included_set:
            raise _invalid_query_error(
                "writable query types must be included",
                phase="build",
                details={"role": "write"},
            )
        frozen = tuple(
            item for item in checked_writable if self._registry.schema_for_type(item).frozen
        )
        if frozen:
            raise _invalid_query_error(
                "frozen component types cannot be query-writable",
                phase="build",
                details={"component_type": self._type_names(frozen)},
            )
        if changed_since is None:
            if checked_changed:
                raise _invalid_query_error(
                    "changed query types require a changed-since epoch",
                    phase="build",
                    details={"role": "changed"},
                )
        elif type(changed_since) is not int or changed_since < 0:
            raise _invalid_query_error(
                "changed-since epoch must be a non-negative integer",
                phase="build",
                details={"actual_type": type(changed_since).__name__},
            )
        elif not checked_changed:
            raise _invalid_query_error(
                "changed filtering requires at least one included type",
                phase="build",
                details={"role": "changed"},
            )
        if not set(checked_changed) <= included_set:
            raise _invalid_query_error(
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
        """Acquire a query lease and materialize detached candidate rows."""

        writable = bool(spec.writable)
        if writable:
            if self._active_write_query or self._active_read_queries:
                raise _active_query_error(
                    "writable query cannot overlap another active query", operation="query_open"
                )
            self._active_write_query = True
        else:
            if self._active_write_query:
                raise _active_query_error(
                    "read-only query cannot overlap an active writable query",
                    operation="query_open",
                )
            self._active_read_queries += 1
        try:
            if spec.changed_since is not None and spec.changed_since > self._epoch:
                raise _invalid_query_error(
                    "changed-since epoch cannot be later than query activation",
                    phase="open",
                    details={"epoch": spec.changed_since, "world_epoch": self._epoch},
                )
            plan = self._query_plan(spec)
            candidates = (
                tuple(self._entities)
                if plan.driver is None
                else self._tables[plan.driver].entity_ids()
            )
            matched = tuple(
                entity_id for entity_id in candidates if self._matches_query(entity_id, spec)
            )
            if spec.order is QueryOrder.STABLE:
                matched = tuple(sorted(matched, key=EntityId.as_tuple))
            rows: list[QueryRowState] = []
            writable_types = set(spec.writable)
            columns = tuple(
                (
                    component_type,
                    self._registry.schema_for_type(component_type),
                    component_type in writable_types,
                )
                for component_type in spec.included
            )
            for entity_id in matched:
                values: list[object] = []
                signatures: list[tuple[object, ...] | None] = []
                for component_type, schema, capture_signature in columns:
                    stored = self._tables[component_type].get(entity_id)
                    if capture_signature:
                        value, signature = _copy_component_with_signature(
                            stored,
                            component_type,
                            schema,
                            operation="query_read",
                        )
                    else:
                        value = _copy_component(
                            stored,
                            component_type,
                            schema,
                            operation="query_read",
                        )
                        signature = None
                    values.append(value)
                    signatures.append(signature)
                rows.append(QueryRowState(entity_id, tuple(values), tuple(signatures)))
            return tuple(rows)
        except Exception:
            self._release_query(spec)
            raise

    def _commit_query_row(self, spec: QuerySpec, row: QueryRowState) -> None:
        """Validate and atomically write all changed declared values in one row."""

        self._allocator.validate(row.entity_id, operation="query_writeback")
        prepared: list[tuple[type[object], object]] = []
        included_indexes = {item: index for index, item in enumerate(spec.included)}
        for component_type in spec.writable:
            index = included_indexes[component_type]
            schema = self._registry.schema_for_type(component_type)
            canonical, signature = _copy_component_with_signature(
                row.values[index],
                component_type,
                schema,
                operation="query_writeback",
            )
            baseline = row.signatures[index]
            if baseline is None:
                raise RuntimeError("writable query row is missing its captured signature")
            if signature != baseline:
                prepared.append((component_type, canonical))
        if not prepared:
            return
        next_epoch = self._epoch + 1
        for component_type, canonical in prepared:
            table = self._tables[component_type]
            if not table.contains(row.entity_id):
                raise _missing_error(
                    operation="query_writeback",
                    entity_id=row.entity_id,
                    schema=self._registry.schema_for_type(component_type),
                )
            table.replace(row.entity_id, canonical, epoch=next_epoch)
        self._epoch = next_epoch

    def _release_query(self, spec: QuerySpec) -> None:
        """Release one active query lease."""

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
        return _copy_component(component, component_type, schema, operation=operation)

    def _validate_command_component_type(self, component_type: type[object]) -> None:
        self._registry.schema_for_type(component_type)

    def commands(self) -> Commands:
        """Create a reusable local structural buffer bound to this world."""

        return Commands(cast(CommandBackend, self))

    def flush(self, commands: Commands) -> FlushResult:
        """Atomically apply copied local structural commands in enqueue order."""

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
                        "operation_kind": _command_kind(record),
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

    def clone(self) -> World:
        self._require_mutation_allowed(operation="clone")
        duplicate = World(self._registry)
        duplicate._allocator = self._allocator.clone()
        duplicate._entities = set(self._entities)
        duplicate._epoch = self._epoch
        duplicate._structural_epoch = self._structural_epoch
        for component_type in self._registry.component_types:
            schema = self._registry.schema_for_type(component_type)
            duplicate._tables[component_type] = self._tables[component_type].clone(
                lambda value, component_type=component_type, schema=schema: _copy_component(
                    value, component_type, schema, operation="clone"
                )
            )
        return duplicate

    def _capture_checkpoint(self) -> EcsCheckpoint:
        """Capture detached canonical state including allocator and change epochs."""

        self._require_mutation_allowed(operation="capture_checkpoint")
        tables: list[ComponentTableCheckpoint] = []
        for component_type in self._registry.component_types:
            schema = self._registry.schema_for_type(component_type)
            table = self._tables[component_type]
            rows = tuple(
                ComponentRowCheckpoint(
                    entity_id=entity_id,
                    value=_copy_component(
                        value,
                        component_type,
                        schema,
                        operation="capture_checkpoint",
                    ),
                    changed_epoch=table.changed_epoch(entity_id),
                )
                for entity_id, value in sorted(table.items(), key=lambda item: item[0].as_tuple())
            )
            tables.append(
                ComponentTableCheckpoint(
                    component_type=component_type,
                    structural_epoch=table.structural_epoch,
                    rows=rows,
                )
            )
        return EcsCheckpoint(
            allocator=self._allocator.checkpoint(),
            epoch=self._epoch,
            structural_epoch=self._structural_epoch,
            tables=tuple(tables),
        )

    def _restore_checkpoint(self, checkpoint: EcsCheckpoint) -> None:
        """Atomically restore a validated storage-neutral in-memory checkpoint."""

        self._require_mutation_allowed(operation="restore_checkpoint")
        if (
            type(checkpoint.epoch) is not int
            or checkpoint.epoch < 0
            or type(checkpoint.structural_epoch) is not int
            or checkpoint.structural_epoch < 0
            or checkpoint.structural_epoch > checkpoint.epoch
            or (
                checkpoint.allocator.generations
                and (checkpoint.epoch == 0 or checkpoint.structural_epoch == 0)
            )
        ):
            raise _invalid_checkpoint_error("checkpoint epochs are invalid", reason="epoch")
        tables_by_type: dict[type[object], ComponentTableCheckpoint] = {}
        for table in checkpoint.tables:
            if table.component_type in tables_by_type:
                raise _invalid_checkpoint_error(
                    "checkpoint repeats a component table", reason="duplicate_table"
                )
            try:
                self._registry.schema_for_type(table.component_type)
            except ComponentError as error:
                raise _invalid_checkpoint_error(
                    "checkpoint contains an unknown component table", reason="unknown_table"
                ) from error
            tables_by_type[table.component_type] = table
        if set(tables_by_type) != set(self._registry.component_types):
            raise _invalid_checkpoint_error(
                "checkpoint component table set is incomplete", reason="table_set"
            )

        allocator = EntityAllocator.from_checkpoint(checkpoint.allocator)
        entities = {
            EntityId(index, generation)
            for index, (generation, alive) in enumerate(
                zip(checkpoint.allocator.generations, checkpoint.allocator.alive, strict=True)
            )
            if alive
        }
        restored_tables: dict[type[object], DenseComponentTable] = {}
        for component_type in self._registry.component_types:
            table = tables_by_type[component_type]
            if (
                type(table.structural_epoch) is not int
                or table.structural_epoch < 0
                or (table.rows and table.structural_epoch == 0)
                or table.structural_epoch > checkpoint.structural_epoch
            ):
                raise _invalid_checkpoint_error(
                    "checkpoint table epoch is invalid", reason="table_epoch"
                )
            schema = self._registry.schema_for_type(component_type)
            seen: set[EntityId] = set()
            rows: list[tuple[EntityId, object, int]] = []
            for row in table.rows:
                if row.entity_id in seen or row.entity_id not in entities:
                    raise _invalid_checkpoint_error(
                        "checkpoint component row targets an invalid entity",
                        reason="component_entity",
                    )
                if (
                    type(row.changed_epoch) is not int
                    or row.changed_epoch <= 0
                    or row.changed_epoch > checkpoint.epoch
                ):
                    raise _invalid_checkpoint_error(
                        "checkpoint component row epoch is invalid", reason="row_epoch"
                    )
                seen.add(row.entity_id)
                rows.append(
                    (
                        row.entity_id,
                        _copy_component(
                            row.value,
                            component_type,
                            schema,
                            operation="restore_checkpoint",
                        ),
                        row.changed_epoch,
                    )
                )
            restored_tables[component_type] = DenseComponentTable.from_checkpoint_rows(
                tuple(rows), structural_epoch=table.structural_epoch
            )

        self._allocator = allocator
        self._entities = entities
        self._tables = restored_tables
        self._epoch = checkpoint.epoch
        self._structural_epoch = checkpoint.structural_epoch
        self._query_plans.clear()
        self._check_invariants()

    def _validate_query_types(
        self, component_types: tuple[object, ...], *, role: str
    ) -> tuple[type[object], ...]:
        seen: set[type[object]] = set()
        checked: list[type[object]] = []
        for component_type in component_types:
            if not isinstance(component_type, type):
                raise _invalid_query_error(
                    "query component entries must be types",
                    phase="build",
                    details={"role": role, "actual_type": type(component_type).__name__},
                )
            if component_type in seen:
                raise _invalid_query_error(
                    "query component types must be unique within each role",
                    phase="build",
                    details={"role": role, "component_type": component_type.__name__},
                )
            try:
                self._registry.schema_for_type(component_type)
            except ComponentError as error:
                raise _invalid_query_error(
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

    def _query_plan(self, spec: QuerySpec) -> _QueryPlan:
        key = _QueryKey(
            tuple(self._registry.schema_for_type(item).type_id for item in spec.included),
            tuple(self._registry.schema_for_type(item).type_id for item in spec.excluded),
            tuple(self._registry.schema_for_type(item).type_id for item in spec.changed_types),
            spec.order,
        )
        cached = self._query_plans.get(key)
        if cached is not None and cached.structural_epoch == self._structural_epoch:
            return cached
        driver = (
            None
            if not spec.included
            else min(
                spec.included,
                key=lambda item: (
                    len(self._tables[item]),
                    self._registry.schema_for_type(item).type_id.bytes,
                ),
            )
        )
        plan = _QueryPlan(driver, self._structural_epoch)
        self._query_plans[key] = plan
        return plan

    def _matches_query(self, entity_id: EntityId, spec: QuerySpec) -> bool:
        if not all(self._tables[item].contains(entity_id) for item in spec.included):
            return False
        if any(self._tables[item].contains(entity_id) for item in spec.excluded):
            return False
        return spec.changed_since is None or any(
            self._tables[item].changed_epoch(entity_id) > spec.changed_since
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

    def _adopt_staged(self, staged: World) -> None:
        self._allocator = staged._allocator
        self._entities = staged._entities
        self._tables = staged._tables
        self._epoch = staged._epoch
        self._structural_epoch = staged._structural_epoch
        self._query_plans.clear()

    def _require_mutation_allowed(self, *, operation: str) -> None:
        if self._active_write_query or self._active_read_queries:
            raise _active_query_error(
                "world mutation is forbidden while a query cursor is active",
                operation=operation,
            )

    def _validate_entity(self, entity_id: EntityId, *, operation: str) -> None:
        self._allocator.validate(entity_id, operation=operation)

    def _check_invariants(self) -> None:
        assert self._allocator.alive_count == len(self._entities)
        for entity_id in self._entities:
            assert self._allocator.is_alive(entity_id)
        for table in self._tables.values():
            table.check_invariants()


def _invalid_checkpoint_error(message: str, *, reason: str) -> InvalidWorldCheckpointError:
    return InvalidWorldCheckpointError(
        message,
        code="ecs.invalid_world_checkpoint",
        subsystem="ecs",
        phase="restore_checkpoint",
        details={"reason": reason},
    )


def _copy_component(
    value: object,
    component_type: type[object],
    schema: ComponentSchema,
    *,
    operation: str = "store",
) -> object:
    copied, _signature = _prepare_component_copy(
        value,
        component_type,
        schema,
        operation=operation,
        capture_signature=False,
    )
    return copied


def _copy_component_with_signature(
    value: object,
    component_type: type[object],
    schema: ComponentSchema,
    *,
    operation: str,
) -> tuple[object, tuple[object, ...]]:
    copied, signature = _prepare_component_copy(
        value,
        component_type,
        schema,
        operation=operation,
        capture_signature=True,
    )
    if signature is None:
        raise RuntimeError("component signature capture invariant failed")
    return copied, signature


def _prepare_component_copy(
    value: object,
    component_type: type[object],
    schema: ComponentSchema,
    *,
    operation: str,
    capture_signature: bool,
) -> tuple[object, tuple[object, ...] | None]:
    if type(value) is not component_type:
        raise _invalid_value_error(
            "component instance must have its exact registered type",
            operation=operation,
            schema=schema,
            details={"actual_type": type(value).__name__},
        )
    captured = tuple(
        (
            field.name,
            _read_runtime_field(value, field, schema=schema, operation=operation),
        )
        for field in schema.fields
    )
    try:
        copied = object.__new__(component_type)
        for name, field_value in captured:
            object.__setattr__(copied, name, field_value)
        signature = (
            tuple(_signature_value(field_value) for _name, field_value in captured)
            if capture_signature
            else None
        )
        return copied, signature
    except Exception as error:
        raise _invalid_value_error(
            "component value could not be copied",
            operation=operation,
            schema=schema,
            details={"cause_type": type(error).__name__},
        ) from error


def _read_runtime_field(
    value: object,
    field: ComponentField,
    *,
    schema: ComponentSchema,
    operation: str,
) -> object:
    try:
        actual = object.__getattribute__(value, field.name)
    except Exception as error:
        raise _invalid_value_error(
            "component field could not be read",
            operation=operation,
            schema=schema,
            details={
                "field": field.name,
                "reason": "unreadable_field",
                "cause_type": type(error).__name__,
            },
        ) from error
    if actual is None:
        if field.allow_none:
            return actual
        raise _invalid_field_error(field, actual, schema=schema, operation=operation)
    expected = {
        ComponentValueType.BOOL: bool,
        ComponentValueType.INT: int,
        ComponentValueType.FLOAT: float,
        ComponentValueType.STRING: str,
    }[field.value_type]
    if type(actual) is not expected or (isinstance(actual, float) and not isfinite(actual)):
        raise _invalid_field_error(field, actual, schema=schema, operation=operation)
    return actual


def _already_present_error(
    *, operation: str, entity_id: EntityId | None, schema: ComponentSchema
) -> ComponentAlreadyPresentError:
    details: dict[str, str | int | None] = {
        "component_type": schema.qualified_name,
        "entity_index": None if entity_id is None else entity_id.index,
        "entity_generation": None if entity_id is None else entity_id.generation,
    }
    return ComponentAlreadyPresentError(
        "entity already has this component type",
        code="ecs.component_already_present",
        subsystem="ecs",
        phase=operation,
        details=details,
    )


def _missing_error(
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


def _invalid_field_error(
    field: ComponentField,
    actual: object,
    *,
    schema: ComponentSchema,
    operation: str,
) -> InvalidComponentValueError:
    return _invalid_value_error(
        "component field value does not match its schema",
        operation=operation,
        schema=schema,
        details={
            "field": field.name,
            "expected_type": field.annotation,
            "actual_type": type(actual).__name__,
        },
    )


def _invalid_value_error(
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


def _signature_value(value: object) -> object:
    if type(value) is float:
        return value.hex()
    return value


def _invalid_query_error(
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


def _active_query_error(message: str, *, operation: str) -> ActiveQueryError:
    return ActiveQueryError(
        message,
        code="ecs.active_query",
        subsystem="ecs",
        phase=operation,
    )


def _command_kind(record: DeferredCommand) -> str:
    if isinstance(record, SpawnCommand):
        return "spawn"
    if isinstance(record, DestroyCommand):
        return "destroy"
    if isinstance(record, AddCommand):
        return "add"
    return "remove"
