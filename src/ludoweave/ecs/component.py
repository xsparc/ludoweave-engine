"""Immutable component schemas, explicit registries, and migration paths."""

from collections.abc import Callable, Iterable, Mapping
from dataclasses import (
    MISSING,
    Field,
    dataclass,
    fields,
    is_dataclass,
)
from dataclasses import (
    field as dataclass_field,
)
from enum import StrEnum
from math import isfinite
from types import MappingProxyType, UnionType
from typing import Any, Protocol, TypeVar, Union, cast, get_args, get_origin
from uuid import UUID

from ludoweave.ecs.errors import (
    ComponentMigrationError,
    ComponentSchemaError,
    DuplicateComponentError,
    IncompatibleComponentVersionError,
    UnknownComponentError,
)

type ComponentMigrationFunction = Callable[[Mapping[str, object]], Mapping[str, object]]
type MetadataValue = str | int | float | bool | None

ComponentT = TypeVar("ComponentT")

_SCHEMA_ATTRIBUTE = "__ludoweave_component_schema__"
_SCALAR_TYPES = (bool, int, float, str)


class SerializationPolicy(StrEnum):
    """Whether component values participate in future canonical serialization."""

    CANONICAL = "canonical"
    EXCLUDED = "excluded"


class DeterminismTier(StrEnum):
    """Declared determinism guarantee for one component schema."""

    D0 = "d0"
    D1 = "d1"
    D2 = "d2"


class StorageHint(StrEnum):
    """Backend-neutral preference for a future component storage implementation."""

    AUTO = "auto"
    ROW = "row"
    COLUMN = "column"


class ComponentValueType(StrEnum):
    """Scalar value domain accepted by the M1 schema contract."""

    BOOL = "bool"
    INT = "int"
    FLOAT = "float"
    STRING = "str"


@dataclass(frozen=True, slots=True)
class ComponentField:
    """One ordered, validated field in a component schema."""

    name: str
    annotation: str
    value_type: ComponentValueType
    allow_none: bool
    required: bool
    default: object | None
    inspection_metadata: tuple[tuple[str, MetadataValue], ...]


@dataclass(frozen=True, slots=True)
class ComponentMigration:
    """One named, adjacent, forward-only raw-value migration."""

    from_version: int
    to_version: int
    function: ComponentMigrationFunction = dataclass_field(repr=False, compare=False)
    qualified_name: str = dataclass_field(init=False)

    def __post_init__(self) -> None:
        _require_positive_version(self.from_version, phase="define_migration", field="from_version")
        _require_positive_version(self.to_version, phase="define_migration", field="to_version")
        if self.to_version != self.from_version + 1:
            raise ComponentSchemaError(
                "component migrations must connect adjacent forward versions",
                code="ecs.invalid_component_migration",
                subsystem="ecs",
                phase="define_migration",
                details={
                    "from_version": self.from_version,
                    "to_version": self.to_version,
                },
            )
        qualified_name = _callable_qualified_name(self.function)
        object.__setattr__(self, "qualified_name", qualified_name)


@dataclass(frozen=True, slots=True)
class ComponentSchema:
    """Immutable authoring and compatibility contract for one component type."""

    type_id: UUID
    qualified_name: str
    version: int
    fields: tuple[ComponentField, ...]
    frozen: bool
    authoritative: bool
    serialization: SerializationPolicy
    determinism: DeterminismTier
    storage_hint: StorageHint
    inspection_metadata: tuple[tuple[str, MetadataValue], ...]
    migrations: tuple[ComponentMigration, ...]


def component(
    *,
    type_id: UUID,
    version: int = 1,
    authoritative: bool = True,
    serialization: SerializationPolicy = SerializationPolicy.CANONICAL,
    determinism: DeterminismTier = DeterminismTier.D1,
    storage_hint: StorageHint = StorageHint.AUTO,
    inspection_metadata: Mapping[str, MetadataValue] | None = None,
    migrations: Iterable[ComponentMigration] = (),
) -> Callable[[type[ComponentT]], type[ComponentT]]:
    """Attach a validated schema to a slotted dataclass without global registration."""

    checked_type_id = _require_type_id(type_id, phase="define")
    checked_version = _require_positive_version(version, phase="define", field="version")
    if type(authoritative) is not bool:
        raise _schema_error(
            "authoritative must be a boolean",
            phase="define",
            details={"actual_type": type(authoritative).__name__},
        )
    checked_serialization = _require_enum(serialization, SerializationPolicy, field="serialization")
    checked_determinism = _require_enum(determinism, DeterminismTier, field="determinism")
    checked_storage_hint = _require_enum(storage_hint, StorageHint, field="storage_hint")
    if authoritative and checked_serialization is not SerializationPolicy.CANONICAL:
        raise _schema_error(
            "authoritative components must use canonical serialization",
            phase="define",
            details={"serialization": checked_serialization.value},
        )
    if authoritative and checked_determinism is DeterminismTier.D0:
        raise _schema_error(
            "authoritative components must declare determinism tier D1 or D2",
            phase="define",
            details={"determinism": checked_determinism.value},
        )
    checked_metadata = _freeze_metadata(
        cast(Mapping[object, object] | None, inspection_metadata),
        phase="define",
        location="component",
    )
    checked_migrations = tuple(migrations)
    _validate_migration_chain(checked_version, checked_migrations)

    def decorate(component_type: type[ComponentT]) -> type[ComponentT]:
        checked_component_type, qualified_name = _validate_component_type(component_type)
        if _SCHEMA_ATTRIBUTE in vars(checked_component_type):
            raise _schema_error(
                "component type already has a LudoWeave schema",
                phase="define",
                details={"component_type": _type_name(checked_component_type)},
            )
        schema_fields = tuple(
            _build_component_field(item) for item in fields(cast(Any, checked_component_type))
        )
        schema = ComponentSchema(
            type_id=checked_type_id,
            qualified_name=qualified_name,
            version=checked_version,
            fields=schema_fields,
            frozen=cast(
                _DataclassParams, vars(checked_component_type)["__dataclass_params__"]
            ).frozen,
            authoritative=authoritative,
            serialization=checked_serialization,
            determinism=checked_determinism,
            storage_hint=checked_storage_hint,
            inspection_metadata=checked_metadata,
            migrations=checked_migrations,
        )
        setattr(checked_component_type, _SCHEMA_ATTRIBUTE, schema)
        return component_type

    return decorate


def component_schema(component_type: object) -> ComponentSchema:
    """Return the attached schema or raise a structured declaration error."""

    if not isinstance(component_type, type):
        raise _schema_error(
            "component schema lookup requires a class",
            phase="inspect",
            details={"actual_type": type(component_type).__name__},
        )
    schema = vars(component_type).get(_SCHEMA_ATTRIBUTE)
    if isinstance(schema, ComponentSchema):
        return schema
    raise _schema_error(
        "component class is not decorated with @component",
        phase="inspect",
        details={"component_type": _type_name(component_type)},
    )


class ComponentRegistry:
    """Immutable, deterministic indexes for an explicit set of component types."""

    __slots__ = ("_by_id", "_by_name", "_by_type", "_component_types", "_schemas")

    def __init__(self, component_types: Iterable[type[object]] = ()) -> None:
        by_id: dict[UUID, ComponentSchema] = {}
        by_name: dict[str, ComponentSchema] = {}
        by_type: dict[type[object], ComponentSchema] = {}
        for component_type in component_types:
            schema = component_schema(component_type)
            if component_type in by_type:
                raise _duplicate_error(
                    "component type is registered more than once",
                    identity="component_type",
                    value=schema.qualified_name,
                )
            if schema.type_id in by_id:
                raise _duplicate_error(
                    "component type ID is already registered",
                    identity="type_id",
                    value=str(schema.type_id),
                )
            if schema.qualified_name in by_name:
                raise _duplicate_error(
                    "component qualified name is already registered",
                    identity="qualified_name",
                    value=schema.qualified_name,
                )
            by_type[component_type] = schema
            by_id[schema.type_id] = schema
            by_name[schema.qualified_name] = schema

        self._by_id: Mapping[UUID, ComponentSchema] = MappingProxyType(by_id)
        self._by_name: Mapping[str, ComponentSchema] = MappingProxyType(by_name)
        self._by_type: Mapping[type[object], ComponentSchema] = MappingProxyType(by_type)
        self._component_types = tuple(
            sorted(by_type, key=lambda component_type: by_type[component_type].type_id.bytes)
        )
        self._schemas = tuple(by_type[component_type] for component_type in self._component_types)

    @property
    def schemas(self) -> tuple[ComponentSchema, ...]:
        """Return schemas in deterministic UUID-byte order."""

        return self._schemas

    @property
    def component_types(self) -> tuple[type[object], ...]:
        """Return Python component classes in deterministic UUID-byte order."""

        return self._component_types

    def __len__(self) -> int:
        return len(self._schemas)

    def schema_for_id(self, type_id: UUID) -> ComponentSchema:
        """Resolve a schema by its persistent type ID."""

        checked = _require_type_id(type_id, phase="lookup")
        schema = self._by_id.get(checked)
        if schema is None:
            raise _unknown_error("type_id", str(checked))
        return schema

    def schema_for_name(self, qualified_name: str) -> ComponentSchema:
        """Resolve a schema by its diagnostic qualified name."""

        if type(qualified_name) is not str or not qualified_name.strip():
            raise _schema_error(
                "qualified name lookup must be non-empty text",
                phase="lookup",
                details={"actual_type": type(qualified_name).__name__},
            )
        schema = self._by_name.get(qualified_name)
        if schema is None:
            raise _unknown_error("qualified_name", qualified_name)
        return schema

    def schema_for_type(self, component_type: object) -> ComponentSchema:
        """Resolve a schema by its Python authoring class."""

        if not isinstance(component_type, type):
            raise _schema_error(
                "component type lookup requires a class",
                phase="lookup",
                details={"actual_type": type(component_type).__name__},
            )
        schema = self._by_type.get(component_type)
        if schema is None:
            raise _unknown_error("component_type", _type_name(component_type))
        return schema

    def component_type_for_id(self, type_id: UUID) -> type[object]:
        """Resolve the Python authoring type for a persistent component UUID."""

        schema = self.schema_for_id(type_id)
        return next(
            component_type
            for component_type in self._component_types
            if self._by_type[component_type] is schema
        )

    def migrate(
        self,
        type_id: UUID,
        *,
        from_version: int,
        values: Mapping[str, object],
    ) -> dict[str, object]:
        """Migrate copied raw values forward to the registered current schema."""

        schema = self.schema_for_id(type_id)
        source_version = _require_positive_version(
            from_version, phase="migrate", field="from_version"
        )
        if source_version > schema.version:
            raise _incompatible_version_error(schema, source_version)

        current = _copy_raw_values(values, schema=schema, version=source_version)
        path = tuple(
            migration for migration in schema.migrations if migration.from_version >= source_version
        )
        expected_steps = schema.version - source_version
        if len(path) != expected_steps:
            raise _incompatible_version_error(schema, source_version)

        for migration in path:
            read_only_values = MappingProxyType(dict(current))
            try:
                migrated = migration.function(read_only_values)
            except Exception as error:
                raise ComponentMigrationError(
                    "component migration raised an exception",
                    code="ecs.component_migration_failed",
                    subsystem="ecs",
                    phase="migrate",
                    details={
                        "type_id": str(schema.type_id),
                        "from_version": migration.from_version,
                        "to_version": migration.to_version,
                        "migration": migration.qualified_name,
                        "cause_type": type(error).__name__,
                    },
                ) from error
            current = _copy_raw_values(migrated, schema=schema, version=migration.to_version)

        _validate_current_values(schema, current)
        return current


def _validate_component_type(component_type: object) -> tuple[type[object], str]:
    if not isinstance(component_type, type) or not is_dataclass(component_type):
        raise _schema_error(
            "@component requires a dataclass class",
            phase="define",
            details={"component_type": _type_name(cast(object, component_type))},
        )
    if any("__dict__" in base.__dict__ for base in component_type.__mro__ if base is not object):
        raise _schema_error(
            "component dataclasses must use slots without an instance dictionary",
            phase="define",
            details={"component_type": _type_name(component_type)},
        )
    if any(is_dataclass(base) for base in component_type.__mro__[1:-1]):
        raise _schema_error(
            "component dataclass inheritance is not supported in M1",
            phase="define",
            details={"component_type": _type_name(component_type)},
        )
    module = getattr(component_type, "__module__", "")
    qualified_name = getattr(component_type, "__qualname__", "")
    if not module or not qualified_name or "<locals>" in qualified_name:
        raise _schema_error(
            "component classes must have a stable module-qualified name",
            phase="define",
            details={"component_type": _type_name(component_type)},
        )
    return component_type, f"{module}.{qualified_name}"


class _DataclassParams(Protocol):
    frozen: bool


def _build_component_field(item: Field[Any]) -> ComponentField:
    name = item.name
    init = item.init
    default = item.default
    default_factory = item.default_factory
    metadata = cast(Mapping[object, object], item.metadata)
    annotation = item.type

    if not init:
        raise _field_error(name, "component fields must participate in dataclass initialization")
    if default_factory is not MISSING:
        raise _field_error(name, "component default_factory is not supported in M1")
    value_type, allow_none, rendered_annotation = _parse_field_annotation(name, annotation)
    required = default is MISSING
    checked_default: object | None = None
    if not required:
        checked_default = _validate_field_value(
            name,
            default,
            value_type=value_type,
            allow_none=allow_none,
            phase="define",
        )
    return ComponentField(
        name=name,
        annotation=rendered_annotation,
        value_type=value_type,
        allow_none=allow_none,
        required=required,
        default=checked_default,
        inspection_metadata=_freeze_metadata(metadata, phase="define", location=f"field:{name}"),
    )


def _parse_field_annotation(name: str, annotation: object) -> tuple[ComponentValueType, bool, str]:
    direct = _component_value_type(annotation)
    if direct is not None:
        return direct, False, direct.value

    origin = get_origin(annotation)
    if origin in (Union, UnionType):
        arguments = get_args(annotation)
        non_none = tuple(argument for argument in arguments if argument is not type(None))
        if len(arguments) == 2 and len(non_none) == 1:
            optional_type = _component_value_type(non_none[0])
            if optional_type is not None:
                return optional_type, True, f"{optional_type.value} | None"

    raise _field_error(
        name,
        "component fields must use bool, int, float, str, or an optional form",
        annotation=_type_name(annotation),
    )


def _component_value_type(annotation: object) -> ComponentValueType | None:
    if annotation is bool:
        return ComponentValueType.BOOL
    if annotation is int:
        return ComponentValueType.INT
    if annotation is float:
        return ComponentValueType.FLOAT
    if annotation is str:
        return ComponentValueType.STRING
    return None


def _validate_field_value(
    name: str,
    value: object,
    *,
    value_type: ComponentValueType,
    allow_none: bool,
    phase: str,
) -> object | None:
    if value is None:
        if allow_none:
            return None
        raise _field_error(name, "component field does not allow None", phase=phase)
    expected_type = {
        ComponentValueType.BOOL: bool,
        ComponentValueType.INT: int,
        ComponentValueType.FLOAT: float,
        ComponentValueType.STRING: str,
    }[value_type]
    if type(value) is not expected_type:
        raise _field_error(
            name,
            "component field value does not match its annotation",
            phase=phase,
            expected_type=value_type.value,
            actual_type=type(value).__name__,
        )
    if isinstance(value, float) and not isfinite(value):
        raise _field_error(name, "component float values must be finite", phase=phase)
    return value


def _validate_migration_chain(version: int, migrations: tuple[ComponentMigration, ...]) -> None:
    ordered = tuple(sorted(migrations, key=lambda migration: migration.from_version))
    actual = tuple((item.from_version, item.to_version) for item in ordered)
    expected = tuple((source, source + 1) for source in range(1, version))
    if actual != expected:
        raise ComponentSchemaError(
            "schema migrations must form one complete adjacent chain from version 1",
            code="ecs.incompatible_component_version",
            subsystem="ecs",
            phase="define",
            details={
                "version": version,
                "expected_steps": len(expected),
                "actual_steps": len(actual),
            },
        )
    if migrations != ordered:
        raise ComponentSchemaError(
            "schema migrations must be declared in ascending version order",
            code="ecs.invalid_component_migration",
            subsystem="ecs",
            phase="define",
            details={"version": version},
        )


def _validate_current_values(schema: ComponentSchema, values: Mapping[str, object]) -> None:
    expected_names = tuple(item.name for item in schema.fields)
    actual_names = tuple(values)
    missing = tuple(name for name in expected_names if name not in values)
    unexpected = tuple(name for name in actual_names if name not in expected_names)
    if missing or unexpected:
        raise ComponentMigrationError(
            "migrated component values do not match the current schema",
            code="ecs.invalid_component_data",
            subsystem="ecs",
            phase="migrate",
            details={
                "type_id": str(schema.type_id),
                "missing_fields": ",".join(missing),
                "unexpected_fields": ",".join(unexpected),
            },
        )
    by_name = {item.name: item for item in schema.fields}
    for name, value in values.items():
        schema_field = by_name[name]
        try:
            _validate_field_value(
                name,
                value,
                value_type=schema_field.value_type,
                allow_none=schema_field.allow_none,
                phase="migrate",
            )
        except ComponentSchemaError as error:
            raise ComponentMigrationError(
                "migrated component field value is invalid",
                code="ecs.invalid_component_data",
                subsystem="ecs",
                phase="migrate",
                details={
                    "type_id": str(schema.type_id),
                    "field": name,
                    "reason": error.message,
                },
            ) from error


def _copy_raw_values(values: object, *, schema: ComponentSchema, version: int) -> dict[str, object]:
    if not isinstance(values, Mapping):
        raise ComponentMigrationError(
            "component migration values must be a mapping",
            code="ecs.invalid_component_data",
            subsystem="ecs",
            phase="migrate",
            details={
                "type_id": str(schema.type_id),
                "version": version,
                "actual_type": type(values).__name__,
            },
        )
    copied: dict[str, object] = {}
    checked_values = cast(Mapping[object, object], values)
    for key, value in checked_values.items():
        if type(key) is not str or not key:
            raise ComponentMigrationError(
                "component migration keys must be non-empty strings",
                code="ecs.invalid_component_data",
                subsystem="ecs",
                phase="migrate",
                details={
                    "type_id": str(schema.type_id),
                    "version": version,
                    "actual_key_type": type(key).__name__,
                },
            )
        if value is not None and type(value) not in _SCALAR_TYPES:
            raise ComponentMigrationError(
                "component migration values must use the scalar schema domain",
                code="ecs.invalid_component_data",
                subsystem="ecs",
                phase="migrate",
                details={
                    "type_id": str(schema.type_id),
                    "version": version,
                    "field": key,
                    "actual_type": type(value).__name__,
                },
            )
        if isinstance(value, float) and not isfinite(value):
            raise ComponentMigrationError(
                "component migration float values must be finite",
                code="ecs.invalid_component_data",
                subsystem="ecs",
                phase="migrate",
                details={"type_id": str(schema.type_id), "version": version, "field": key},
            )
        copied[key] = value
    return copied


def _freeze_metadata(
    metadata: Mapping[object, object] | None, *, phase: str, location: str
) -> tuple[tuple[str, MetadataValue], ...]:
    if metadata is None:
        return ()
    frozen: list[tuple[str, MetadataValue]] = []
    for key, value in metadata.items():
        if type(key) is not str or not key.strip():
            raise _schema_error(
                "inspection metadata keys must be non-empty strings",
                phase=phase,
                details={"location": location, "actual_key_type": type(key).__name__},
            )
        if value is not None and type(value) not in _SCALAR_TYPES:
            raise _schema_error(
                "inspection metadata values must be scalar",
                phase=phase,
                details={
                    "location": location,
                    "key": key,
                    "actual_type": type(value).__name__,
                },
            )
        if isinstance(value, float) and not isfinite(value):
            raise _schema_error(
                "inspection metadata float values must be finite",
                phase=phase,
                details={"location": location, "key": key},
            )
        frozen.append((key, cast(MetadataValue, value)))
    return tuple(sorted(frozen))


def _callable_qualified_name(function: object) -> str:
    if not callable(function):
        raise _schema_error(
            "component migration function must be callable",
            phase="define_migration",
            details={"actual_type": type(function).__name__},
        )
    module = getattr(function, "__module__", "")
    qualified_name = getattr(function, "__qualname__", "")
    if (
        type(module) is not str
        or type(qualified_name) is not str
        or not module
        or not qualified_name
        or "<locals>" in qualified_name
        or "<lambda>" in qualified_name
    ):
        raise _schema_error(
            "component migration functions must be named module-level callables",
            phase="define_migration",
            details={"actual_type": type(function).__name__},
        )
    return f"{module}.{qualified_name}"


def _require_type_id(type_id: object, *, phase: str) -> UUID:
    if not isinstance(type_id, UUID) or type_id.int == 0:
        raise _schema_error(
            "component type_id must be a nonzero UUID",
            phase=phase,
            details={"actual_type": type(type_id).__name__},
        )
    return type_id


def _require_positive_version(value: object, *, phase: str, field: str) -> int:
    if type(value) is not int or value < 1 or value > 2**63 - 1:
        raise _schema_error(
            "component versions must be positive integers within the signed 64-bit range",
            phase=phase,
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _require_enum[EnumT](value: object, enum_type: type[EnumT], *, field: str) -> EnumT:
    if not isinstance(value, enum_type):
        raise _schema_error(
            "component schema enum value has the wrong type",
            phase="define",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _field_error(
    field: str,
    message: str,
    *,
    phase: str = "define",
    annotation: str | None = None,
    expected_type: str | None = None,
    actual_type: str | None = None,
) -> ComponentSchemaError:
    details: dict[str, MetadataValue] = {"field": field}
    if annotation is not None:
        details["annotation"] = annotation
    if expected_type is not None:
        details["expected_type"] = expected_type
    if actual_type is not None:
        details["actual_type"] = actual_type
    return _schema_error(message, phase=phase, details=details)


def _schema_error(
    message: str,
    *,
    phase: str,
    details: Mapping[str, MetadataValue] | None = None,
) -> ComponentSchemaError:
    return ComponentSchemaError(
        message,
        code="ecs.invalid_component_schema",
        subsystem="ecs",
        phase=phase,
        details=details,
    )


def _duplicate_error(message: str, *, identity: str, value: str) -> DuplicateComponentError:
    return DuplicateComponentError(
        message,
        code="ecs.duplicate_component",
        subsystem="ecs",
        phase="register",
        details={"identity": identity, "value": value},
    )


def _unknown_error(identity: str, value: str) -> UnknownComponentError:
    return UnknownComponentError(
        "component schema is not registered",
        code="ecs.unknown_component",
        subsystem="ecs",
        phase="lookup",
        details={"identity": identity, "value": value},
    )


def _incompatible_version_error(
    schema: ComponentSchema, from_version: int
) -> IncompatibleComponentVersionError:
    return IncompatibleComponentVersionError(
        "component version cannot migrate to the registered schema",
        code="ecs.incompatible_component_version",
        subsystem="ecs",
        phase="migrate",
        details={
            "type_id": str(schema.type_id),
            "from_version": from_version,
            "current_version": schema.version,
        },
    )


def _type_name(value: object) -> str:
    if isinstance(value, type):
        return f"{value.__module__}.{value.__qualname__}"
    return type(value).__name__
