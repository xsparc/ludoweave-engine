# pyright: reportPrivateUsage=false
"""Immutable canonical snapshot codec for complete authoritative sessions."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast
from uuid import UUID

from ludoweave.core.errors import LudoWeaveError
from ludoweave.core.version import __version__
from ludoweave.ecs import (
    ComponentRegistry,
    EntityId,
    ResourceRegistry,
    ResourceStore,
    World,
)
from ludoweave.ecs._checkpoint import (
    ComponentRowCheckpoint,
    ComponentTableCheckpoint,
    EcsCheckpoint,
)
from ludoweave.ecs.entity import AllocatorCheckpoint
from ludoweave.world.canonical import JsonLimits, JsonValue, canonical_dumps, canonical_loads
from ludoweave.world.errors import (
    IncompatibleSnapshotError,
    SnapshotCaptureError,
    SnapshotDecodeError,
    SnapshotHashMismatchError,
    WorldProtocolError,
)
from ludoweave.world.random import (
    RANDOM_ALGORITHM,
    RandomStreams,
    RandomStreamsSnapshot,
    RandomStreamState,
)
from ludoweave.world.resources import AuthorityResourceRegistry
from ludoweave.world.state import AUTHORITY_PROTOCOL, TickExecutor, WorldSession, authority_hash

SNAPSHOT_PROTOCOL = "ludoweave.snapshot/1"
_PLATFORM_PROFILE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/+-]{0,127}\Z")


@dataclass(frozen=True, slots=True)
class SnapshotBinding:
    """Optional composition identity required by a snapshot codec."""

    project_schema: str
    dependency_lock_hash: str
    platform_profile: str

    def __post_init__(self) -> None:
        for field in ("project_schema", "dependency_lock_hash"):
            value = getattr(self, field)
            if (
                type(value) is not str
                or len(value) != 71
                or not value.startswith("sha256:")
                or any(character not in "0123456789abcdef" for character in value[7:])
            ):
                raise _snapshot_error(
                    "snapshot binding hash is invalid",
                    phase="configure",
                    details={"field": field},
                )
        if (
            type(self.platform_profile) is not str
            or _PLATFORM_PROFILE.fullmatch(self.platform_profile) is None
        ):
            raise _snapshot_error(
                "snapshot binding platform profile is invalid",
                phase="configure",
                details={"field": "platform_profile"},
            )

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "project_schema": self.project_schema,
            "dependency_lock_hash": self.dependency_lock_hash,
            "platform_profile": self.platform_profile,
        }


@dataclass(frozen=True, slots=True)
class SnapshotLimits:
    """Whole-document and semantic count limits for snapshot codecs."""

    max_bytes: int = 67_108_864
    max_depth: int = 64
    max_nodes: int = 8_000_000
    max_entities: int = 1_000_000
    max_components: int = 4_000_000
    max_resources: int = 4_096
    max_random_streams: int = 4_096

    def __post_init__(self) -> None:
        for name in (
            "max_bytes",
            "max_components",
            "max_depth",
            "max_entities",
            "max_nodes",
            "max_random_streams",
            "max_resources",
        ):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise SnapshotDecodeError(
                    "snapshot limits must be positive integers",
                    code="world.snapshot.invalid_limits",
                    subsystem="world",
                    phase="configure",
                    details={"field": name, "actual_type": type(value).__name__},
                )


class SnapshotCodec:
    """Composition-owned codec for one exact component/resource schema set."""

    __slots__ = (
        "_authority_resources",
        "_binding",
        "_component_registry",
        "_json_limits",
        "_limits",
        "_resource_registry",
    )

    def __init__(
        self,
        component_registry: ComponentRegistry,
        resource_registry: ResourceRegistry,
        *,
        authority_resources: AuthorityResourceRegistry | None = None,
        binding: SnapshotBinding | None = None,
        limits: SnapshotLimits | None = None,
    ) -> None:
        self._component_registry = component_registry
        self._resource_registry = resource_registry
        self._authority_resources = authority_resources or AuthorityResourceRegistry()
        self._binding = binding
        self._limits = limits or SnapshotLimits()
        max_collection = max(
            self._limits.max_components,
            self._limits.max_entities,
            self._limits.max_resources,
        )
        self._json_limits = JsonLimits(
            max_bytes=self._limits.max_bytes,
            max_depth=self._limits.max_depth,
            max_nodes=self._limits.max_nodes,
            max_collection_items=max_collection,
            max_string_bytes=min(self._limits.max_bytes, 1_048_576),
        )
        for schema in self._authority_resources.schemas:
            if not self._resource_registry.contains(schema.spec):
                raise _snapshot_error(
                    "snapshot authority resource is absent from the resource registry",
                    phase="configure",
                    details={"resource": schema.spec.name},
                )

    def encode(self, session: WorldSession) -> bytes:
        """Capture immutable canonical bytes from one compatible session."""

        self._require_compatible_session(session)
        try:
            authority, state_hash = session._capture_current()
        except LudoWeaveError as error:
            raise SnapshotCaptureError(
                "snapshot could not be captured at the current safe point",
                code="world.snapshot.capture_failed",
                subsystem="world",
                phase="capture",
                details={"cause_code": error.code},
            ) from error
        wrapper: dict[str, JsonValue] = {
            "protocol": SNAPSHOT_PROTOCOL,
            "engine_version": __version__,
            "state_hash": state_hash,
            "authority": authority,
        }
        if self._binding is not None:
            wrapper["composition"] = self._binding.as_dict()
        return canonical_dumps(wrapper, limits=self._json_limits)

    def decode(
        self,
        document: str | bytes,
        *,
        tick_executor: TickExecutor | None = None,
    ) -> WorldSession:
        """Decode into a new session; no caller-owned destination is mutated."""

        try:
            decoded = canonical_loads(document, limits=self._json_limits)
        except WorldProtocolError as error:
            raise _snapshot_error(
                "snapshot document is malformed or oversized",
                phase="decode",
                details={"cause_code": error.code},
            ) from error
        wrapper = _object(decoded, role="snapshot")
        required = {"protocol", "engine_version", "state_hash", "authority"}
        if self._binding is not None:
            required.add("composition")
        _exact_fields(wrapper, required=required, role="snapshot")
        if _text(wrapper["protocol"], field="protocol") != SNAPSHOT_PROTOCOL:
            raise _incompatible_snapshot("snapshot protocol is incompatible", field="protocol")
        if _text(wrapper["engine_version"], field="engine_version") != __version__:
            raise _incompatible_snapshot(
                "snapshot engine version is incompatible", field="engine_version"
            )
        if self._binding is not None:
            composition = _object(wrapper["composition"], role="composition")
            _exact_fields(
                composition,
                required={"project_schema", "dependency_lock_hash", "platform_profile"},
                role="composition",
            )
            expected = self._binding.as_dict()
            for field in ("project_schema", "dependency_lock_hash", "platform_profile"):
                actual = _text(composition[field], field=f"composition.{field}")
                if actual != expected[field]:
                    raise _incompatible_snapshot(
                        "snapshot composition is incompatible with this codec",
                        field=f"composition.{field}",
                    )
        declared_hash = _text(wrapper["state_hash"], field="state_hash")
        authority = _object(wrapper["authority"], role="authority")
        computed_hash = authority_hash(authority)
        if declared_hash != computed_hash:
            raise SnapshotHashMismatchError(
                "snapshot authoritative state hash does not match its payload",
                code="world.snapshot.hash_mismatch",
                subsystem="world",
                phase="verify",
                details={"declared_hash": declared_hash, "computed_hash": computed_hash},
            )
        session, migrated = self._decode_authority(authority, tick_executor=tick_executor)
        if not migrated and session.state_hash != declared_hash:
            raise SnapshotHashMismatchError(
                "decoded snapshot does not reproduce its authoritative state hash",
                code="world.snapshot.hash_mismatch",
                subsystem="world",
                phase="restore",
                details={"declared_hash": declared_hash, "computed_hash": session.state_hash},
            )
        return session

    def load_into(self, session: WorldSession, document: str | bytes) -> None:
        """Atomically adopt a decoded snapshot into an existing compatible session."""

        self._require_compatible_session(session)
        candidate = self.decode(document)
        try:
            session._adopt_snapshot(candidate)
        except LudoWeaveError as error:
            raise _snapshot_error(
                "snapshot could not be adopted at the current safe point",
                phase="restore",
                details={"cause_code": error.code},
            ) from error

    def _decode_authority(
        self,
        authority: dict[str, JsonValue],
        *,
        tick_executor: TickExecutor | None,
    ) -> tuple[WorldSession, bool]:
        _exact_fields(
            authority,
            required={
                "protocol",
                "world_id",
                "completed_ticks",
                "component_schemas",
                "resource_schemas",
                "allocator",
                "epochs",
                "components",
                "resources",
                "random",
            },
            role="authority",
        )
        if _text(authority["protocol"], field="authority.protocol") != AUTHORITY_PROTOCOL:
            raise _incompatible_snapshot(
                "snapshot authority protocol is incompatible", field="authority.protocol"
            )
        world_id = _text(authority["world_id"], field="world_id")
        completed_ticks = _non_negative_int(authority["completed_ticks"], field="completed_ticks")
        component_versions = self._validate_component_manifest(authority["component_schemas"])
        resource_versions = self._validate_resource_manifest(authority["resource_schemas"])
        allocator = self._decode_allocator(authority["allocator"])
        if len(allocator.generations) > self._limits.max_entities:
            raise _snapshot_limit(
                "allocator_slots",
                len(allocator.generations),
                self._limits.max_entities,
            )
        epochs = _object(authority["epochs"], role="epochs")
        _exact_fields(epochs, required={"world", "structural"}, role="epochs")
        world_epoch = _non_negative_int(epochs["world"], field="epochs.world")
        structural_epoch = _non_negative_int(epochs["structural"], field="epochs.structural")
        tables, component_count, component_migrated = self._decode_components(
            authority["components"], component_versions
        )
        if component_count > self._limits.max_components:
            raise _snapshot_limit("components", component_count, self._limits.max_components)
        checkpoint = EcsCheckpoint(allocator, world_epoch, structural_epoch, tables)
        world = World(self._component_registry)
        try:
            world._restore_checkpoint(checkpoint)
        except LudoWeaveError as error:
            raise _snapshot_error(
                "snapshot world checkpoint violates canonical invariants",
                phase="restore",
                details={"cause_code": error.code},
            ) from error

        resource_initial, resources_migrated = self._decode_resources(
            authority["resources"], resource_versions
        )
        random_streams = self._decode_random(authority["random"])
        try:
            resources = ResourceStore(self._resource_registry, resource_initial)
            session = WorldSession(
                world_id,
                world,
                resources,
                authority_resources=self._authority_resources,
                completed_ticks=completed_ticks,
                random_streams=random_streams,
                tick_executor=tick_executor,
            )
        except LudoWeaveError as error:
            raise _snapshot_error(
                "snapshot session composition violates canonical invariants",
                phase="restore",
                details={"cause_code": error.code},
            ) from error
        return session, component_migrated or resources_migrated

    def _validate_component_manifest(self, value: JsonValue) -> dict[UUID, int]:
        entries = _array(value, role="component_schemas")
        versions: dict[UUID, int] = {}
        for entry_value in entries:
            entry = _object(entry_value, role="component_schema")
            _exact_fields(
                entry,
                required={"type_id", "version", "determinism", "fields"},
                role="component_schema",
            )
            type_id = _uuid(entry["type_id"], field="component_schema.type_id")
            if type_id in versions:
                raise _snapshot_error(
                    "snapshot repeats a component schema",
                    phase="validate",
                    details={"type_id": str(type_id)},
                )
            try:
                schema = self._component_registry.schema_for_id(type_id)
            except LudoWeaveError as error:
                raise _incompatible_snapshot(
                    "snapshot contains an unknown component schema",
                    field="component_schema.type_id",
                ) from error
            version = _positive_int(entry["version"], field="component_schema.version")
            # ``fields`` is the registered current decode-target contract. The
            # historical row shape is consumed only by the named migration
            # chain and is never inferred from untrusted manifest metadata.
            expected_fields: list[JsonValue] = [
                {
                    "name": field.name,
                    "type": field.value_type.value,
                    "optional": field.allow_none,
                }
                for field in schema.fields
            ]
            if (
                version > schema.version
                or _text(entry["determinism"], field="component_schema.determinism")
                != schema.determinism.value
                or canonical_dumps(entry["fields"]) != canonical_dumps(expected_fields)
            ):
                raise _incompatible_snapshot(
                    "snapshot component schema contract is incompatible",
                    field="component_schema",
                )
            versions[type_id] = version
        if set(versions) != {schema.type_id for schema in self._component_registry.schemas}:
            raise _incompatible_snapshot(
                "snapshot component schema set is incompatible", field="component_schemas"
            )
        return versions

    def _validate_resource_manifest(self, value: JsonValue) -> dict[UUID, int]:
        entries = _array(value, role="resource_schemas")
        expected = {
            str(schema.type_id): (
                schema.version,
                schema.codec_id,
                schema.role.value,
                schema.spec.name,
            )
            for schema in self._authority_resources.state_schemas
        }
        actual: dict[str, tuple[int, str, str, str]] = {}
        for entry_value in entries:
            entry = _object(entry_value, role="resource_schema")
            _exact_fields(
                entry,
                required={"type_id", "version", "codec", "role", "resource"},
                role="resource_schema",
            )
            type_id = str(_uuid(entry["type_id"], field="resource_schema.type_id"))
            if type_id in actual:
                raise _snapshot_error(
                    "snapshot repeats a resource schema",
                    phase="validate",
                    details={"type_id": type_id},
                )
            actual[type_id] = (
                _positive_int(entry["version"], field="resource_schema.version"),
                _text(entry["codec"], field="resource_schema.codec"),
                _text(entry["role"], field="resource_schema.role"),
                _text(entry["resource"], field="resource_schema.resource"),
            )
        # Historical resource versions are allowed only when identity, role,
        # and codec remain explicit and a registered migration chain exists.
        if set(actual) != set(expected):
            raise _incompatible_snapshot(
                "snapshot resource schema set is incompatible", field="resource_schemas"
            )
        for type_id, actual_record in actual.items():
            expected_record = expected[type_id]
            if actual_record[0] > expected_record[0] or actual_record[1:] != expected_record[1:]:
                raise _incompatible_snapshot(
                    "snapshot resource schema is incompatible", field="resource_schema"
                )
        return {UUID(type_id): record[0] for type_id, record in actual.items()}

    def _decode_allocator(self, value: JsonValue) -> AllocatorCheckpoint:
        allocator = _object(value, role="allocator")
        _exact_fields(allocator, required={"generations", "alive", "free"}, role="allocator")
        generation_values = _array(allocator["generations"], role="allocator.generations")
        alive_values = _array(allocator["alive"], role="allocator.alive")
        free_values = _array(allocator["free"], role="allocator.free")
        for field, items in (
            ("allocator.generations", generation_values),
            ("allocator.alive", alive_values),
            ("allocator.free", free_values),
        ):
            if len(items) > self._limits.max_entities:
                raise _snapshot_limit(field, len(items), self._limits.max_entities)
        generations = tuple(
            _non_negative_int(item, field="allocator.generations") for item in generation_values
        )
        alive = tuple(_boolean(item, field="allocator.alive") for item in alive_values)
        free = tuple(_non_negative_int(item, field="allocator.free") for item in free_values)
        try:
            return AllocatorCheckpoint(generations, alive, free)
        except LudoWeaveError as error:
            raise _snapshot_error(
                "snapshot allocator state is invalid",
                phase="validate",
                details={"cause_code": error.code},
            ) from error

    def _decode_components(
        self,
        value: JsonValue,
        manifest_versions: Mapping[UUID, int],
    ) -> tuple[tuple[ComponentTableCheckpoint, ...], int, bool]:
        table_values = _array(value, role="components")
        tables: dict[UUID, ComponentTableCheckpoint] = {}
        component_count = 0
        migrated = False
        for table_value in table_values:
            table = _object(table_value, role="component_table")
            _exact_fields(
                table,
                required={"type_id", "version", "structural_epoch", "rows"},
                role="component_table",
            )
            type_id = _uuid(table["type_id"], field="component_table.type_id")
            if type_id in tables or type_id not in manifest_versions:
                raise _snapshot_error(
                    "snapshot component table identity is duplicate or undeclared",
                    phase="validate",
                    details={"type_id": str(type_id)},
                )
            version = _positive_int(table["version"], field="component_table.version")
            if version != manifest_versions[type_id]:
                raise _snapshot_error(
                    "snapshot component table version differs from its manifest",
                    phase="validate",
                    details={"type_id": str(type_id)},
                )
            component_type = self._component_registry.component_type_for_id(type_id)
            rows: list[ComponentRowCheckpoint] = []
            seen: set[EntityId] = set()
            row_values = _array(table["rows"], role="component_rows")
            if component_count + len(row_values) > self._limits.max_components:
                raise _snapshot_limit(
                    "components",
                    component_count + len(row_values),
                    self._limits.max_components,
                )
            for row_value in row_values:
                row = _object(row_value, role="component_row")
                _exact_fields(
                    row,
                    required={"entity", "changed_epoch", "values"},
                    role="component_row",
                )
                entity_fields = _array(row["entity"], role="component_row.entity")
                if len(entity_fields) != 2:
                    raise _snapshot_error(
                        "snapshot entity ID must have two fields",
                        phase="validate",
                        details={"field": "entity"},
                    )
                entity_id = EntityId(
                    _non_negative_int(entity_fields[0], field="entity.index"),
                    _non_negative_int(entity_fields[1], field="entity.generation"),
                )
                if entity_id in seen:
                    raise _snapshot_error(
                        "snapshot component table repeats an entity",
                        phase="validate",
                        details={"type_id": str(type_id)},
                    )
                seen.add(entity_id)
                raw_values = _object(row["values"], role="component_values")
                try:
                    current_values = self._component_registry.migrate(
                        type_id,
                        from_version=version,
                        values=cast(dict[str, object], raw_values),
                    )
                    component = component_type(**current_values)
                except Exception as error:
                    cause_code = (
                        error.code if isinstance(error, LudoWeaveError) else type(error).__name__
                    )
                    raise _snapshot_error(
                        "snapshot component could not migrate or construct",
                        phase="migrate",
                        details={"type_id": str(type_id), "cause_code": cause_code},
                    ) from error
                rows.append(
                    ComponentRowCheckpoint(
                        entity_id,
                        component,
                        _non_negative_int(row["changed_epoch"], field="changed_epoch"),
                    )
                )
            component_count += len(rows)
            schema = self._component_registry.schema_for_id(type_id)
            migrated = migrated or version != schema.version
            tables[type_id] = ComponentTableCheckpoint(
                component_type,
                _non_negative_int(table["structural_epoch"], field="structural_epoch"),
                tuple(rows),
            )
        expected = {schema.type_id for schema in self._component_registry.schemas}
        if set(tables) != expected:
            raise _snapshot_error(
                "snapshot component table set is incomplete",
                phase="validate",
                details={"field": "components"},
            )
        return (
            tuple(tables[type_id] for type_id in sorted(tables, key=lambda item: item.bytes)),
            component_count,
            migrated,
        )

    def _decode_resources(
        self,
        value: JsonValue,
        manifest_versions: Mapping[UUID, int],
    ) -> tuple[tuple[tuple[object, object], ...], bool]:
        records = _array(value, role="resources")
        if len(records) > self._limits.max_resources:
            raise _snapshot_limit("resources", len(records), self._limits.max_resources)
        values: dict[UUID, tuple[object, object, bool]] = {}
        migrated = False
        for record_value in records:
            record = _object(record_value, role="resource")
            _exact_fields(
                record,
                required={"type_id", "version", "codec", "present", "value"},
                role="resource",
            )
            type_id = _uuid(record["type_id"], field="resource.type_id")
            if type_id in values:
                raise _snapshot_error(
                    "snapshot repeats a resource record",
                    phase="validate",
                    details={"type_id": str(type_id)},
                )
            try:
                schema = self._authority_resources.schema_for_id(type_id)
            except LudoWeaveError as error:
                raise _incompatible_snapshot(
                    "snapshot resource type is not registered", field="resource.type_id"
                ) from error
            version = _positive_int(record["version"], field="resource.version")
            if version != manifest_versions.get(type_id):
                raise _snapshot_error(
                    "snapshot resource version differs from its manifest",
                    phase="validate",
                    details={"type_id": str(type_id)},
                )
            if _text(record["codec"], field="resource.codec") != schema.codec_id:
                raise _incompatible_snapshot(
                    "snapshot resource codec is incompatible", field="resource.codec"
                )
            present = _boolean(record["present"], field="resource.present")
            if present:
                try:
                    decoded = schema.decode_versioned(version, record["value"])
                except LudoWeaveError as error:
                    raise _snapshot_error(
                        "snapshot resource could not migrate or decode",
                        phase="migrate",
                        details={"type_id": str(type_id), "cause_code": error.code},
                    ) from error
                values[type_id] = (schema.spec, decoded, True)
            elif record["value"] is not None:
                raise _snapshot_error(
                    "absent snapshot resources must contain null",
                    phase="validate",
                    details={"type_id": str(type_id)},
                )
            else:
                values[type_id] = (schema.spec, None, False)
            migrated = migrated or version != schema.version
        expected = {schema.type_id for schema in self._authority_resources.state_schemas}
        if set(values) != expected:
            raise _snapshot_error(
                "snapshot resource record set is incomplete",
                phase="validate",
                details={"field": "resources"},
            )
        initial = tuple(
            (values[type_id][0], values[type_id][1])
            for type_id in sorted(values, key=lambda item: item.bytes)
            if values[type_id][2]
        )
        return initial, migrated

    def _decode_random(self, value: JsonValue) -> RandomStreams:
        random = _object(value, role="random")
        _exact_fields(random, required={"algorithm", "seed", "streams"}, role="random")
        algorithm = _text(random["algorithm"], field="random.algorithm")
        if algorithm != RANDOM_ALGORITHM:
            raise _incompatible_snapshot(
                "snapshot random algorithm is incompatible", field="random.algorithm"
            )
        streams: list[RandomStreamState] = []
        stream_values = _array(random["streams"], role="random.streams")
        if len(stream_values) > self._limits.max_random_streams:
            raise _snapshot_limit(
                "random.streams",
                len(stream_values),
                self._limits.max_random_streams,
            )
        for stream_value in stream_values:
            stream = _object(stream_value, role="random_stream")
            _exact_fields(
                stream,
                required={"name", "state", "increment"},
                role="random_stream",
            )
            streams.append(
                RandomStreamState(
                    _text(stream["name"], field="random.name"),
                    _hex_u64(stream["state"], field="random.state"),
                    _hex_u64(stream["increment"], field="random.increment"),
                )
            )
        try:
            checkpoint = RandomStreamsSnapshot(
                seed=_hex_u64(random["seed"], field="random.seed"),
                streams=tuple(streams),
                algorithm=algorithm,
            )
            return RandomStreams.from_checkpoint(checkpoint)
        except LudoWeaveError as error:
            raise _snapshot_error(
                "snapshot random state is invalid",
                phase="validate",
                details={"cause_code": error.code},
            ) from error

    def _require_compatible_session(self, session: WorldSession) -> None:
        if session.component_registry.schemas != self._component_registry.schemas:
            raise _incompatible_snapshot(
                "session component registry is incompatible with snapshot codec",
                field="component_registry",
            )
        if session.resource_registry.specs != self._resource_registry.specs:
            raise _incompatible_snapshot(
                "session resource registry is incompatible with snapshot codec",
                field="resource_registry",
            )
        if session.authority_resources.schemas != self._authority_resources.schemas:
            raise _incompatible_snapshot(
                "session authority registry is incompatible with snapshot codec",
                field="authority_resources",
            )


def _exact_fields(value: Mapping[str, JsonValue], *, required: set[str], role: str) -> None:
    missing = sorted(required - value.keys())
    unexpected = sorted(value.keys() - required)
    if missing or unexpected:
        raise _snapshot_error(
            "snapshot object fields do not match its schema",
            phase="validate",
            details={
                "role": role,
                "missing": ",".join(missing),
                "unexpected": ",".join(unexpected),
            },
        )


def _object(value: object, *, role: str) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise _snapshot_error(
            "snapshot value must be an object",
            phase="validate",
            details={"role": role, "actual_type": type(value).__name__},
        )
    return cast(dict[str, JsonValue], value)


def _array(value: object, *, role: str) -> list[JsonValue]:
    if not isinstance(value, list):
        raise _snapshot_error(
            "snapshot value must be an array",
            phase="validate",
            details={"role": role, "actual_type": type(value).__name__},
        )
    return cast(list[JsonValue], value)


def _text(value: object, *, field: str) -> str:
    if type(value) is not str:
        raise _snapshot_type_error(field, value, "string")
    return value


def _positive_int(value: object, *, field: str) -> int:
    checked = _non_negative_int(value, field=field)
    if checked == 0:
        raise _snapshot_type_error(field, value, "positive integer")
    return checked


def _non_negative_int(value: object, *, field: str) -> int:
    if type(value) is not int or value < 0:
        raise _snapshot_type_error(field, value, "non-negative integer")
    return value


def _boolean(value: object, *, field: str) -> bool:
    if type(value) is not bool:
        raise _snapshot_type_error(field, value, "boolean")
    return value


def _uuid(value: object, *, field: str) -> UUID:
    text = _text(value, field=field)
    try:
        result = UUID(text)
    except ValueError as error:
        raise _snapshot_type_error(field, value, "canonical UUID") from error
    if result.int == 0 or str(result) != text:
        raise _snapshot_type_error(field, value, "canonical nonzero UUID")
    return result


def _hex_u64(value: object, *, field: str) -> int:
    text = _text(value, field=field)
    if len(text) != 16 or any(character not in "0123456789abcdef" for character in text):
        raise _snapshot_type_error(field, value, "16-digit lowercase hexadecimal")
    return int(text, 16)


def _snapshot_type_error(field: str, value: object, expected: str) -> SnapshotDecodeError:
    return _snapshot_error(
        "snapshot field has an invalid value",
        phase="validate",
        details={"field": field, "expected": expected, "actual_type": type(value).__name__},
    )


def _snapshot_limit(field: str, actual: int, limit: int) -> SnapshotDecodeError:
    return SnapshotDecodeError(
        "snapshot exceeds a configured deterministic limit",
        code="world.snapshot.oversized",
        subsystem="world",
        phase="validate",
        details={"field": field, "actual": actual, "limit": limit},
    )


def _snapshot_error(
    message: str,
    *,
    phase: str,
    details: dict[str, str | int | float | bool | None],
) -> SnapshotDecodeError:
    return SnapshotDecodeError(
        message,
        code="world.snapshot.malformed",
        subsystem="world",
        phase=phase,
        details=details,
    )


def _incompatible_snapshot(message: str, *, field: str) -> IncompatibleSnapshotError:
    return IncompatibleSnapshotError(
        message,
        code="world.snapshot.incompatible",
        subsystem="world",
        phase="compatibility",
        details={"field": field},
    )
