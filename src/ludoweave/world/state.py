# pyright: reportPrivateUsage=false
"""Single-owner authoritative world session and canonical logical image."""

from __future__ import annotations

import re
import threading
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol, cast

from ludoweave.core.errors import LudoWeaveError
from ludoweave.ecs import (
    ComponentRegistry,
    DeterminismTier,
    ResourceRegistry,
    ResourceStore,
    SerializationPolicy,
    WorldStore,
)
from ludoweave.ecs._checkpoint import EcsCheckpoint
from ludoweave.world.canonical import JsonLimits, JsonValue, canonical_dumps
from ludoweave.world.errors import AuthorityError, TransactionValidationError
from ludoweave.world.random import RandomStreams
from ludoweave.world.resources import AuthorityResourceRegistry, ResourceRole

AUTHORITY_PROTOCOL = "ludoweave.authority/1"
AUTHORITY_JSON_LIMITS = JsonLimits(
    max_bytes=67_108_864,
    max_depth=64,
    max_nodes=8_000_000,
    max_collection_items=4_000_000,
    max_string_bytes=1_048_576,
)
_WORLD_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_MAX_CANONICAL_INT = 2**63 - 1


class TickExecutor(Protocol):
    """Application-owned staged tick kernel used at an atomic safe point."""

    def execute_tick(
        self,
        world: WorldStore,
        resources: ResourceStore,
        random_streams: RandomStreams,
        tick: int,
    ) -> None: ...


class _CheckpointSource(Protocol):
    def _capture_checkpoint(self) -> EcsCheckpoint: ...


@dataclass(frozen=True, slots=True)
class _SessionRecord:
    world: WorldStore
    resources: ResourceStore
    random_streams: RandomStreams
    completed_ticks: int


class WorldSession:
    """Single-owner pointer to all state covered by atomic world transactions.

    Construction transfers ownership of ``world`` and ``resources``. Callers
    must dereference the current values through this session after a successful
    transaction because commit swaps the complete staged record.
    """

    __slots__ = (
        "_authority_resources",
        "_record",
        "_thread_id",
        "_tick_executor",
        "_world_id",
    )

    def __init__(
        self,
        world_id: str,
        world: WorldStore,
        resources: ResourceStore,
        *,
        authority_resources: AuthorityResourceRegistry | None = None,
        completed_ticks: int = 0,
        random_streams: RandomStreams | None = None,
        tick_executor: TickExecutor | None = None,
    ) -> None:
        if type(world_id) is not str or _WORLD_ID.fullmatch(world_id) is None:
            raise _authority_error(
                "world ID must use bounded stable text",
                phase="compose",
                details={"field": "world_id", "actual_type": type(world_id).__name__},
            )
        if (
            type(completed_ticks) is not int
            or completed_ticks < 0
            or completed_ticks > _MAX_CANONICAL_INT
        ):
            raise _authority_error(
                "completed tick count must be a canonical non-negative integer",
                phase="compose",
                details={"field": "completed_ticks"},
            )
        checked_authority = authority_resources or AuthorityResourceRegistry()
        _validate_component_authority(world.registry)
        for schema in checked_authority.schemas:
            if not resources.registry.contains(schema.spec):
                raise _authority_error(
                    "authority resource is not owned by the resource store registry",
                    phase="compose",
                    details={"resource": schema.spec.name},
                )
        registered_specs = set(resources.registry.specs)
        classified_specs = {schema.spec for schema in checked_authority.schemas}
        if registered_specs != classified_specs:
            missing = sorted(spec.name for spec in registered_specs - classified_specs)
            raise _authority_error(
                "every session resource must have exactly one explicit authority role",
                phase="compose",
                details={"unclassified_resources": ",".join(missing)},
            )
        self._world_id = world_id
        self._record = _SessionRecord(
            world,
            resources,
            random_streams or RandomStreams(0),
            completed_ticks,
        )
        self._authority_resources = checked_authority
        self._tick_executor = tick_executor
        self._thread_id = threading.get_ident()
        try:
            self._capture_current()
        except Exception as error:
            cause_code = error.code if isinstance(error, LudoWeaveError) else type(error).__name__
            raise _authority_error(
                "initial authoritative state is not canonically representable",
                phase="compose",
                details={"cause_code": cause_code},
            ) from error

    @property
    def world_id(self) -> str:
        self._assert_owner_thread()
        return self._world_id

    @property
    def world(self) -> WorldStore:
        """Return a detached world copy; mutations cannot bypass transactions."""

        self._assert_owner_thread()
        return self._record.world.clone()

    @property
    def resources(self) -> ResourceStore:
        """Return a detached resource copy; mutations cannot alter authority."""

        self._assert_owner_thread()
        return self._record.resources.clone()

    @property
    def completed_ticks(self) -> int:
        self._assert_owner_thread()
        return self._record.completed_ticks

    @property
    def random_streams(self) -> RandomStreams:
        """Return a detached random-stream copy."""

        self._assert_owner_thread()
        return self._record.random_streams.clone()

    @property
    def authority_resources(self) -> AuthorityResourceRegistry:
        self._assert_owner_thread()
        return self._authority_resources

    @property
    def component_registry(self) -> ComponentRegistry:
        self._assert_owner_thread()
        return self._record.world.registry

    @property
    def resource_registry(self) -> ResourceRegistry:
        self._assert_owner_thread()
        return self._record.resources.registry

    @property
    def random_seed(self) -> int:
        self._assert_owner_thread()
        return self._record.random_streams.seed

    @property
    def _world(self) -> WorldStore:
        self._assert_owner_thread()
        return self._record.world

    @property
    def _resources(self) -> ResourceStore:
        self._assert_owner_thread()
        return self._record.resources

    @property
    def _random_streams(self) -> RandomStreams:
        self._assert_owner_thread()
        return self._record.random_streams

    @property
    def state_hash(self) -> str:
        """Return the versioned SHA-256 hash of current authoritative state."""

        self._assert_owner_thread()
        return self._capture_current()[1]

    def authority_document(self) -> dict[str, JsonValue]:
        """Return a detached canonical logical image for diff/snapshot services."""

        self._assert_owner_thread()
        return _authority_document(self._world_id, self._record, self._authority_resources)

    def _stage(self) -> _SessionRecord:
        self._assert_owner_thread()
        return _SessionRecord(
            world=self._record.world.clone(),
            resources=self._record.resources.clone(),
            random_streams=self._record.random_streams.clone(),
            completed_ticks=self._record.completed_ticks,
        )

    def _adopt(self, staged: _SessionRecord) -> None:
        self._assert_owner_thread()
        self._record = staged

    def _adopt_snapshot(self, candidate: WorldSession) -> None:
        self._assert_owner_thread()
        if candidate.world_id != self._world_id:
            raise _authority_error(
                "snapshot targets a different world",
                phase="restore_snapshot",
                details={"world_id": candidate.world_id},
            )
        # Clone is a non-mutating ownership preflight that rejects active query
        # cursors before the record pointer can change.
        self._record.world.clone()
        restored_resources = candidate._record.resources.clone()
        for schema in self._authority_resources.schemas:
            if schema.role is ResourceRole.STATE or not self._record.resources.contains(
                schema.spec
            ):
                continue
            restored_resources.insert(schema.spec, self._record.resources.require(schema.spec))
        self._record = _SessionRecord(
            candidate._record.world,
            restored_resources,
            candidate._record.random_streams,
            candidate._record.completed_ticks,
        )

    def _execute_tick(self, staged: _SessionRecord) -> _SessionRecord:
        if staged.completed_ticks == _MAX_CANONICAL_INT:
            raise TransactionValidationError(
                "completed tick count cannot exceed the canonical integer domain",
                code="world.transaction.limit_exceeded",
                subsystem="world",
                phase="validate",
                details={"field": "completed_ticks", "limit": _MAX_CANONICAL_INT},
            )
        external_roles = tuple(
            schema.role.value
            for schema in self._authority_resources.schemas
            if schema.role is not ResourceRole.STATE
        )
        if external_roles:
            raise TransactionValidationError(
                "M2 persistent ticks require state-only resources; recorded input arrives in M4",
                code="world.transaction.nontransactional_operation",
                subsystem="world",
                phase="validate",
                details={"operation": "world.tick", "external_roles": ",".join(external_roles)},
            )
        executor = self._tick_executor
        if executor is None:
            raise TransactionValidationError(
                "world tick requires an injected staged tick executor",
                code="world.transaction.nontransactional_operation",
                subsystem="world",
                phase="validate",
                details={"operation": "world.tick"},
            )
        executor.execute_tick(
            staged.world,
            staged.resources,
            staged.random_streams,
            staged.completed_ticks,
        )
        return _SessionRecord(
            staged.world,
            staged.resources,
            staged.random_streams,
            staged.completed_ticks + 1,
        )

    def _hash_staged(self, staged: _SessionRecord) -> str:
        return _hash_record(self._world_id, staged, self._authority_resources)

    def _capture_current(self) -> tuple[dict[str, JsonValue], str]:
        return _capture_record(self._world_id, self._record, self._authority_resources)

    def _capture_staged(self, staged: _SessionRecord) -> tuple[dict[str, JsonValue], str]:
        return _capture_record(self._world_id, staged, self._authority_resources)

    def _assert_owner_thread(self) -> None:
        actual = threading.get_ident()
        if actual != self._thread_id:
            raise AuthorityError(
                "world session operations must run on the constructing thread",
                code="world.session.thread_violation",
                subsystem="world",
                phase="ownership",
                details={"owner": "constructing_thread", "caller": "different_thread"},
            )


def _hash_record(
    world_id: str,
    record: _SessionRecord,
    resources: AuthorityResourceRegistry,
) -> str:
    encoded = canonical_dumps(
        _authority_document(world_id, record, resources), limits=AUTHORITY_JSON_LIMITS
    )
    return f"sha256:{sha256(encoded).hexdigest()}"


def _capture_record(
    world_id: str,
    record: _SessionRecord,
    resources: AuthorityResourceRegistry,
) -> tuple[dict[str, JsonValue], str]:
    document = _authority_document(world_id, record, resources)
    encoded = canonical_dumps(document, limits=AUTHORITY_JSON_LIMITS)
    return document, f"sha256:{sha256(encoded).hexdigest()}"


def authority_hash(document: dict[str, JsonValue]) -> str:
    """Hash one validated authority document using the M2 algorithm profile."""

    return f"sha256:{sha256(canonical_dumps(document, limits=AUTHORITY_JSON_LIMITS)).hexdigest()}"


def _authority_document(
    world_id: str,
    record: _SessionRecord,
    authority_resources: AuthorityResourceRegistry,
) -> dict[str, JsonValue]:
    checkpoint = cast(_CheckpointSource, record.world)._capture_checkpoint()
    component_tables: list[JsonValue] = []
    for table in checkpoint.tables:
        schema = record.world.registry.schema_for_type(table.component_type)
        rows: list[JsonValue] = []
        for row in table.rows:
            values: dict[str, JsonValue] = {}
            for component_field in schema.fields:
                values[component_field.name] = cast(
                    JsonValue, getattr(row.value, component_field.name)
                )
            rows.append(
                {
                    "entity": [row.entity_id.index, row.entity_id.generation],
                    "changed_epoch": row.changed_epoch,
                    "values": values,
                }
            )
        component_tables.append(
            {
                "type_id": str(schema.type_id),
                "version": schema.version,
                "structural_epoch": table.structural_epoch,
                "rows": rows,
            }
        )

    resource_records: list[JsonValue] = []
    for schema in authority_resources.state_schemas:
        present = record.resources.contains(schema.spec)
        encoded_value: JsonValue = None
        if present:
            value = record.resources.require(schema.spec)
            encoded_value = schema.encode(value)
        resource_records.append(
            {
                "type_id": str(schema.type_id),
                "version": schema.version,
                "codec": schema.codec_id,
                "present": present,
                "value": encoded_value,
            }
        )

    allocator = checkpoint.allocator
    random_checkpoint = record.random_streams.checkpoint()
    return {
        "protocol": AUTHORITY_PROTOCOL,
        "world_id": world_id,
        "completed_ticks": record.completed_ticks,
        "component_schemas": _component_schema_manifest(record.world.registry),
        "resource_schemas": [
            {
                "type_id": str(schema.type_id),
                "version": schema.version,
                "codec": schema.codec_id,
                "role": schema.role.value,
                "resource": schema.spec.name,
            }
            for schema in authority_resources.state_schemas
        ],
        "allocator": {
            "generations": list(allocator.generations),
            "alive": list(allocator.alive),
            "free": list(allocator.free),
        },
        "epochs": {
            "world": checkpoint.epoch,
            "structural": checkpoint.structural_epoch,
        },
        "components": component_tables,
        "resources": resource_records,
        "random": {
            "algorithm": random_checkpoint.algorithm,
            "seed": f"{random_checkpoint.seed:016x}",
            "streams": [
                {
                    "name": item.name,
                    "state": f"{item.state:016x}",
                    "increment": f"{item.increment:016x}",
                }
                for item in random_checkpoint.streams
            ],
        },
    }


def _component_schema_manifest(registry: ComponentRegistry) -> list[JsonValue]:
    return [
        {
            "type_id": str(schema.type_id),
            "version": schema.version,
            "determinism": schema.determinism.value,
            "fields": [
                {
                    "name": item.name,
                    "type": item.value_type.value,
                    "optional": item.allow_none,
                }
                for item in schema.fields
            ],
        }
        for schema in registry.schemas
    ]


def _validate_component_authority(registry: ComponentRegistry) -> None:
    for schema in registry.schemas:
        if (
            not schema.authoritative
            or schema.serialization is not SerializationPolicy.CANONICAL
            or schema.determinism is DeterminismTier.D0
        ):
            raise _authority_error(
                "world sessions currently require canonical authoritative components",
                phase="compose",
                details={"type_id": str(schema.type_id)},
            )


def _authority_error(
    message: str,
    *,
    phase: str,
    details: Mapping[str, str | int | float | bool | None],
) -> AuthorityError:
    return AuthorityError(
        message,
        code="world.invalid_authority",
        subsystem="world",
        phase=phase,
        details=details,
    )
