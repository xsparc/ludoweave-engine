"""Explicit persistent metadata and codecs for authoritative resources."""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import cast
from uuid import UUID

from ludoweave.ecs import ResourceSpec
from ludoweave.world.canonical import JsonValue, validate_json_value
from ludoweave.world.errors import ResourceSchemaError

_CODEC_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}\Z")
_MAX_CANONICAL_INT = 2**63 - 1


class ResourceRole(StrEnum):
    """Persistence role for one application resource."""

    STATE = "state"
    INPUT = "input"
    RUNTIME_EXCLUDED = "runtime_excluded"


@dataclass(frozen=True, slots=True)
class AuthorityResourceMigration:
    """One trusted adjacent forward migration for canonical resource values."""

    from_version: int
    to_version: int
    function: Callable[[JsonValue], object] = field(repr=False, compare=False)

    def __post_init__(self) -> None:
        if (
            type(self.from_version) is not int
            or self.from_version <= 0
            or self.from_version > _MAX_CANONICAL_INT
            or type(self.to_version) is not int
            or self.to_version != self.from_version + 1
            or self.to_version > _MAX_CANONICAL_INT
        ):
            raise _resource_schema_error(
                "resource migrations must connect adjacent positive versions",
                phase="define",
                details={
                    "from_version": self.from_version,
                    "to_version": self.to_version,
                },
            )
        if not callable(self.function):
            raise _resource_schema_error(
                "resource migration function must be callable",
                phase="define",
                details={"field": "function"},
            )


@dataclass(frozen=True, slots=True, eq=False)
class AuthorityResourceSchema[ResourceT]:
    """Stable resource identity plus trusted canonical value codec."""

    type_id: UUID
    version: int
    spec: ResourceSpec[ResourceT]
    codec_id: str
    encoder: Callable[[ResourceT], object] = field(repr=False)
    decoder: Callable[[JsonValue], ResourceT] = field(repr=False)
    role: ResourceRole = ResourceRole.STATE
    migrations: tuple[AuthorityResourceMigration, ...] = ()

    def __post_init__(self) -> None:
        type_id = cast(object, self.type_id)
        if not isinstance(type_id, UUID) or type_id.int == 0:
            raise _resource_schema_error(
                "resource type ID must be a nonzero UUID",
                phase="define",
                details={"field": "type_id", "actual_type": type(self.type_id).__name__},
            )
        if type(self.version) is not int or self.version <= 0 or self.version > _MAX_CANONICAL_INT:
            raise _resource_schema_error(
                "resource schema version must be a positive signed 64-bit integer",
                phase="define",
                details={"field": "version"},
            )
        if type(self.codec_id) is not str or _CODEC_ID.fullmatch(self.codec_id) is None:
            raise _resource_schema_error(
                "resource codec ID must use bounded stable text",
                phase="define",
                details={"field": "codec_id"},
            )
        spec = cast(object, self.spec)
        if not isinstance(spec, ResourceSpec):
            raise _resource_schema_error(
                "resource schema spec must be a ResourceSpec",
                phase="define",
                details={"field": "spec", "actual_type": type(self.spec).__name__},
            )
        if type(self.role) is not ResourceRole:
            raise _resource_schema_error(
                "resource role must be an exact ResourceRole",
                phase="define",
                details={"field": "role", "actual_type": type(self.role).__name__},
            )
        if not callable(self.encoder) or not callable(self.decoder):
            raise _resource_schema_error(
                "resource encoder and decoder must be callable",
                phase="define",
                details={"field": "codec"},
            )
        if self.role is ResourceRole.STATE and not self.spec.deterministic:
            raise _resource_schema_error(
                "authoritative state resources must be deterministic-eligible",
                phase="define",
                details={"resource": self.spec.name},
            )
        try:
            migrations = tuple(cast(Iterable[object], cast(object, self.migrations)))
        except Exception as error:
            raise _resource_schema_error(
                "resource migrations must be an iterable of migration records",
                phase="define",
                details={"field": "migrations", "actual_type": type(self.migrations).__name__},
            ) from error
        if any(not isinstance(migration, AuthorityResourceMigration) for migration in migrations):
            raise _resource_schema_error(
                "resource migrations must contain migration records",
                phase="define",
                details={"field": "migrations"},
            )
        checked_migrations = cast(tuple[AuthorityResourceMigration, ...], migrations)
        object.__setattr__(self, "migrations", checked_migrations)
        expected = tuple(range(1, self.version))
        actual = tuple(migration.from_version for migration in checked_migrations)
        if actual != expected or any(
            migration.to_version != migration.from_version + 1 for migration in checked_migrations
        ):
            raise _resource_schema_error(
                "resource schema must retain one complete adjacent migration chain",
                phase="define",
                details={"resource": self.spec.name, "version": self.version},
            )

    def encode(self, value: ResourceT) -> JsonValue:
        """Run the trusted encoder and validate its detached JSON result."""

        if type(value) is not self.spec.value_type:
            raise _resource_schema_error(
                "resource encoder received the wrong exact value type",
                phase="encode",
                details={"resource": self.spec.name, "actual_type": type(value).__name__},
            )
        try:
            encoded = self.encoder(value)
        except Exception as error:
            raise _resource_schema_error(
                "resource encoder raised an exception",
                phase="encode",
                details={"resource": self.spec.name, "cause_type": type(error).__name__},
            ) from error
        return validate_json_value(encoded)

    def decode(self, value: object) -> ResourceT:
        """Run the trusted decoder and require the schema's exact resource type."""

        checked = validate_json_value(value)
        try:
            decoded = self.decoder(checked)
        except Exception as error:
            raise _resource_schema_error(
                "resource decoder raised an exception",
                phase="decode",
                details={"resource": self.spec.name, "cause_type": type(error).__name__},
            ) from error
        if type(decoded) is not self.spec.value_type:
            raise _resource_schema_error(
                "resource decoder returned the wrong exact value type",
                phase="decode",
                details={"resource": self.spec.name, "actual_type": type(decoded).__name__},
            )
        return decoded

    def decode_versioned(self, version: int, value: object) -> ResourceT:
        """Migrate a historical canonical value and decode the current type."""

        if type(version) is not int or version <= 0 or version > self.version:
            raise _resource_schema_error(
                "resource value version is incompatible",
                phase="migrate",
                details={"resource": self.spec.name, "version": version},
            )
        current = validate_json_value(value)
        for migration in self.migrations:
            if migration.from_version < version:
                continue
            try:
                current = validate_json_value(migration.function(current))
            except Exception as error:
                raise _resource_schema_error(
                    "resource migration failed",
                    phase="migrate",
                    details={
                        "resource": self.spec.name,
                        "from_version": migration.from_version,
                        "cause_type": type(error).__name__,
                    },
                ) from error
        return self.decode(current)


class AuthorityResourceRegistry:
    """Immutable explicit indexes for persistent resource schemas."""

    __slots__ = ("_by_id", "_by_spec", "_schemas", "_state_schemas")

    def __init__(self, schemas: Iterable[object] = ()) -> None:
        by_id: dict[UUID, AuthorityResourceSchema[object]] = {}
        by_spec: dict[ResourceSpec[object], AuthorityResourceSchema[object]] = {}
        for candidate in schemas:
            if not isinstance(candidate, AuthorityResourceSchema):
                raise _resource_schema_error(
                    "authority registry entries must be resource schemas",
                    phase="register",
                    details={"actual_type": type(candidate).__name__},
                )
            schema = cast(AuthorityResourceSchema[object], candidate)
            if schema.type_id in by_id or schema.spec in by_spec:
                raise _resource_schema_error(
                    "resource authority identity is already registered",
                    phase="register",
                    details={"resource": schema.spec.name, "type_id": str(schema.type_id)},
                )
            by_id[schema.type_id] = schema
            by_spec[schema.spec] = schema
        self._by_id = MappingProxyType(by_id)
        self._by_spec = MappingProxyType(by_spec)
        self._schemas = tuple(
            by_id[type_id] for type_id in sorted(by_id, key=lambda item: item.bytes)
        )
        self._state_schemas = tuple(
            schema for schema in self._schemas if schema.role is ResourceRole.STATE
        )

    @property
    def schemas(self) -> tuple[AuthorityResourceSchema[object], ...]:
        return self._schemas

    @property
    def state_schemas(self) -> tuple[AuthorityResourceSchema[object], ...]:
        return self._state_schemas

    def schema_for_id(self, type_id: UUID) -> AuthorityResourceSchema[object]:
        schema = self._by_id.get(type_id)
        if schema is None:
            raise _resource_schema_error(
                "resource type ID is not registered",
                phase="lookup",
                details={"type_id": str(type_id)},
            )
        return schema

    def schema_for_spec(self, spec: ResourceSpec[object]) -> AuthorityResourceSchema[object]:
        schema = self._by_spec.get(spec)
        if schema is None:
            raise _resource_schema_error(
                "resource specification is not classified",
                phase="lookup",
                details={"resource": spec.name},
            )
        return schema


def _resource_schema_error(
    message: str,
    *,
    phase: str,
    details: dict[str, str | int | float | bool | None],
) -> ResourceSchemaError:
    return ResourceSchemaError(
        message,
        code="world.invalid_resource_schema",
        subsystem="world",
        phase=phase,
        details=details,
    )
