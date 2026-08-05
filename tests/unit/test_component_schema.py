"""Component schema, registry, and migration contract tests."""

import json
from collections.abc import Callable, Mapping, MutableMapping
from dataclasses import Field, FrozenInstanceError, dataclass, field, make_dataclass
from typing import Any, cast
from uuid import UUID

import pytest

import ludoweave
from ludoweave.ecs import (
    ComponentMigration,
    ComponentMigrationError,
    ComponentRegistry,
    ComponentSchemaError,
    ComponentValueType,
    DeterminismTier,
    DuplicateComponentError,
    IncompatibleComponentVersionError,
    SerializationPolicy,
    StorageHint,
    UnknownComponentError,
    component,
    component_schema,
)

POSITION_ID = UUID("2be41765-9132-4ef7-a220-186f76807f41")
STATS_ID = UUID("ce1afed7-ecca-4773-b757-c473aafaf65c")


def _stats_v1_to_v2(values: Mapping[str, object]) -> Mapping[str, object]:
    count = values["count"]
    if type(count) is not int:
        raise TypeError("count must be int")
    return {"count": count + 1, "migration_step": "v2"}


def _stats_v2_to_v3(values: Mapping[str, object]) -> Mapping[str, object]:
    count = values["count"]
    if type(count) is not int or values.get("migration_step") != "v2":
        raise TypeError("invalid version 2 values")
    return {"count": count * 2, "label": "migrated"}


def _failing_migration(values: Mapping[str, object]) -> Mapping[str, object]:
    del values
    raise ValueError("intentional migration failure")


def _non_mapping_migration(values: Mapping[str, object]) -> Mapping[str, object]:
    del values
    return cast(Mapping[str, object], ["not", "a", "mapping"])


def _missing_field_migration(values: Mapping[str, object]) -> Mapping[str, object]:
    del values
    return {"count": 1}


def _wrong_type_migration(values: Mapping[str, object]) -> Mapping[str, object]:
    del values
    return {"count": True, "label": "invalid"}


def _mutating_migration(values: Mapping[str, object]) -> Mapping[str, object]:
    mutable = cast(MutableMapping[str, object], values)
    mutable["value"] = 99
    return mutable


@component(
    type_id=POSITION_ID,
    version=1,
    authoritative=True,
    serialization=SerializationPolicy.CANONICAL,
    determinism=DeterminismTier.D2,
    storage_hint=StorageHint.COLUMN,
    inspection_metadata={"category": "spatial", "order": 10},
)
@dataclass(slots=True)
class Position:
    x: float = field(default=0.0, metadata={"units": "pixels"})
    y: float = 0.0


@component(
    type_id=STATS_ID,
    version=3,
    migrations=(
        ComponentMigration(1, 2, _stats_v1_to_v2),
        ComponentMigration(2, 3, _stats_v2_to_v3),
    ),
)
@dataclass(slots=True)
class CurrentStats:
    count: int
    label: str | None = None


def _make_component(
    name: str,
    type_id: UUID,
    *,
    qualified_name: str | None = None,
) -> type[object]:
    component_type = make_dataclass(name, [("value", int, field(default=0))], slots=True)
    component_type.__module__ = __name__
    component_type.__qualname__ = qualified_name or name
    return cast(type[object], component(type_id=type_id)(component_type))


def test_schema_preserves_identity_fields_defaults_and_metadata() -> None:
    schema = component_schema(Position)

    assert schema.type_id == POSITION_ID
    assert schema.qualified_name == f"{__name__}.Position"
    assert schema.version == 1
    assert schema.authoritative
    assert schema.serialization is SerializationPolicy.CANONICAL
    assert schema.determinism is DeterminismTier.D2
    assert schema.storage_hint is StorageHint.COLUMN
    assert schema.inspection_metadata == (("category", "spatial"), ("order", 10))
    assert [item.name for item in schema.fields] == ["x", "y"]
    assert schema.fields[0].annotation == "float"
    assert schema.fields[0].value_type is ComponentValueType.FLOAT
    assert schema.fields[0].default == 0.0
    assert schema.fields[0].inspection_metadata == (("units", "pixels"),)


def test_optional_none_is_distinct_from_a_required_field() -> None:
    schema = component_schema(CurrentStats)

    assert schema.fields[0].required
    assert schema.fields[0].default is None
    assert not schema.fields[1].required
    assert schema.fields[1].allow_none
    assert schema.fields[1].default is None


def test_schema_value_objects_are_frozen_and_slotted() -> None:
    schema = component_schema(Position)

    with pytest.raises(FrozenInstanceError):
        schema.version = 2  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        schema.fields[0].name = "changed"  # type: ignore[misc]
    assert not hasattr(schema, "__dict__")
    assert not hasattr(schema.fields[0], "__dict__")


def test_registry_is_explicit_immutable_and_deterministically_sorted() -> None:
    registry = ComponentRegistry((CurrentStats, Position))
    another = ComponentRegistry()

    assert registry.schemas == tuple(
        sorted(
            (component_schema(CurrentStats), component_schema(Position)),
            key=lambda s: s.type_id.bytes,
        )
    )
    assert registry.component_types == tuple(
        sorted((CurrentStats, Position), key=lambda item: component_schema(item).type_id.bytes)
    )
    assert registry.schema_for_id(POSITION_ID) is component_schema(Position)
    assert registry.schema_for_name(f"{__name__}.CurrentStats") is component_schema(CurrentStats)
    assert registry.schema_for_type(Position) is component_schema(Position)
    assert len(registry) == 2
    assert len(another) == 0


def test_duplicate_type_id_fails_without_changing_an_existing_registry() -> None:
    first = _make_component("FirstId", UUID("aaaaaaaa-0000-0000-0000-000000000001"))
    duplicate = _make_component("SecondId", component_schema(first).type_id)
    existing = ComponentRegistry((first,))

    with pytest.raises(DuplicateComponentError) as caught:
        ComponentRegistry((first, duplicate))

    assert dict(caught.value.details)["identity"] == "type_id"
    assert existing.schemas == (component_schema(first),)


def test_duplicate_qualified_name_and_python_type_fail() -> None:
    shared_name = "tests.synthetic.Shared"
    first = _make_component(
        "FirstName", UUID("aaaaaaaa-0000-0000-0000-000000000002"), qualified_name=shared_name
    )
    duplicate_name = _make_component(
        "SecondName", UUID("aaaaaaaa-0000-0000-0000-000000000003"), qualified_name=shared_name
    )

    with pytest.raises(DuplicateComponentError) as name_error:
        ComponentRegistry((first, duplicate_name))
    with pytest.raises(DuplicateComponentError) as type_error:
        ComponentRegistry((first, first))

    assert dict(name_error.value.details)["identity"] == "qualified_name"
    assert dict(type_error.value.details)["identity"] == "component_type"


def test_unknown_registry_lookups_are_structured() -> None:
    registry = ComponentRegistry((Position,))
    unknown_type = _make_component("Unknown", UUID("aaaaaaaa-0000-0000-0000-000000000004"))

    with pytest.raises(UnknownComponentError, match=r"ecs\.unknown_component") as caught:
        registry.schema_for_id(UUID("ffffffff-ffff-ffff-ffff-ffffffffffff"))
    with pytest.raises(UnknownComponentError):
        registry.schema_for_name("missing.Component")
    with pytest.raises(UnknownComponentError):
        registry.schema_for_type(unknown_type)
    assert json.loads(json.dumps(caught.value.as_dict()))["code"] == "ecs.unknown_component"


def test_migration_chain_is_ordered_and_does_not_mutate_input() -> None:
    registry = ComponentRegistry((CurrentStats,))
    source: dict[str, object] = {"count": 4}

    migrated = registry.migrate(STATS_ID, from_version=1, values=source)

    assert migrated == {"count": 10, "label": "migrated"}
    assert source == {"count": 4}


def test_current_version_values_are_copied_and_validated() -> None:
    registry = ComponentRegistry((CurrentStats,))
    source: dict[str, object] = {"count": 3, "label": None}

    current = registry.migrate(STATS_ID, from_version=3, values=source)

    assert current == source
    assert current is not source


@pytest.mark.parametrize("from_version", [0, -1, True, 4])
def test_incompatible_source_versions_fail(from_version: object) -> None:
    registry = ComponentRegistry((CurrentStats,))

    with pytest.raises((ComponentSchemaError, IncompatibleComponentVersionError)):
        registry.migrate(
            STATS_ID,
            from_version=cast(int, from_version),
            values={"count": 1},
        )


def test_migration_exception_is_chained_with_edge_context() -> None:
    component_type = _make_migrating_component(
        "FailingMigration",
        UUID("aaaaaaaa-0000-0000-0000-000000000005"),
        _failing_migration,
    )
    registry = ComponentRegistry((component_type,))

    with pytest.raises(ComponentMigrationError) as caught:
        registry.migrate(
            component_schema(component_type).type_id, from_version=1, values={"value": 1}
        )

    assert isinstance(caught.value.__cause__, ValueError)
    assert dict(caught.value.details)["from_version"] == 1
    assert dict(caught.value.details)["to_version"] == 2


def test_migration_receives_read_only_values_and_preserves_source() -> None:
    component_type = _make_migrating_component(
        "MutatingMigration",
        UUID("aaaaaaaa-0000-0000-0000-000000000015"),
        _mutating_migration,
    )
    registry = ComponentRegistry((component_type,))
    source: dict[str, object] = {"value": 1}

    with pytest.raises(ComponentMigrationError) as caught:
        registry.migrate(component_schema(component_type).type_id, from_version=1, values=source)

    assert isinstance(caught.value.__cause__, TypeError)
    assert source == {"value": 1}


@pytest.mark.parametrize(
    "migration",
    [_non_mapping_migration, _missing_field_migration, _wrong_type_migration],
)
def test_invalid_migration_outputs_fail(migration: object) -> None:
    function = cast("CallableMigration", migration)
    component_type = _make_migrating_component(
        "InvalidOutput",
        UUID("aaaaaaaa-0000-0000-0000-000000000006"),
        function,
    )
    registry = ComponentRegistry((component_type,))

    with pytest.raises(ComponentMigrationError, match=r"ecs\.invalid_component_data"):
        registry.migrate(
            component_schema(component_type).type_id, from_version=1, values={"value": 1}
        )


def test_incomplete_or_unordered_migration_chains_fail_before_execution() -> None:
    with pytest.raises(ComponentSchemaError, match="complete adjacent chain"):
        component(
            type_id=UUID("aaaaaaaa-0000-0000-0000-000000000007"),
            version=3,
            migrations=(ComponentMigration(2, 3, _stats_v2_to_v3),),
        )
    with pytest.raises(ComponentSchemaError, match="ascending version order"):
        component(
            type_id=UUID("aaaaaaaa-0000-0000-0000-000000000008"),
            version=3,
            migrations=(
                ComponentMigration(2, 3, _stats_v2_to_v3),
                ComponentMigration(1, 2, _stats_v1_to_v2),
            ),
        )


@pytest.mark.parametrize(("from_version", "to_version"), [(1, 1), (2, 1), (1, 3)])
def test_migration_edges_must_be_adjacent_and_forward(from_version: int, to_version: int) -> None:
    with pytest.raises(ComponentSchemaError, match="adjacent forward versions"):
        ComponentMigration(from_version, to_version, _stats_v1_to_v2)


def test_migration_callable_must_be_named_and_module_level() -> None:
    with pytest.raises(ComponentSchemaError, match="named module-level"):
        ComponentMigration(1, 2, lambda values: values)


@pytest.mark.parametrize("version", [0, -1, True, 1.0, "1", None])
def test_component_version_must_be_a_positive_exact_integer(version: object) -> None:
    with pytest.raises(ComponentSchemaError, match="positive integers"):
        component(
            type_id=UUID("aaaaaaaa-0000-0000-0000-000000000009"),
            version=cast(int, version),
        )


def test_component_requires_nonzero_uuid_and_enum_instances() -> None:
    with pytest.raises(ComponentSchemaError, match="nonzero UUID"):
        component(type_id=UUID(int=0))
    with pytest.raises(ComponentSchemaError, match="wrong type"):
        component(
            type_id=UUID("aaaaaaaa-0000-0000-0000-00000000000a"),
            determinism=cast(DeterminismTier, "d1"),
        )


def test_authoritative_metadata_combinations_are_validated() -> None:
    with pytest.raises(ComponentSchemaError, match="canonical serialization"):
        component(
            type_id=UUID("aaaaaaaa-0000-0000-0000-00000000000b"),
            serialization=SerializationPolicy.EXCLUDED,
        )
    with pytest.raises(ComponentSchemaError, match="D1 or D2"):
        component(
            type_id=UUID("aaaaaaaa-0000-0000-0000-00000000000c"),
            determinism=DeterminismTier.D0,
        )

    presentation = _make_presentation_component()
    schema = component_schema(presentation)
    assert not schema.authoritative
    assert schema.serialization is SerializationPolicy.EXCLUDED
    assert schema.determinism is DeterminismTier.D0


def test_component_class_shape_and_decorator_order_are_validated() -> None:
    class Ordinary:
        pass

    @dataclass
    class Unslotted:
        value: int = 0

    @dataclass(slots=True)
    class SlottedInstance:
        value: int = 0

    @dataclass(slots=True)
    class SlottedBase:
        value: int = 0

    @dataclass(slots=True)
    class Inherited(SlottedBase):
        other: int = 0

    with pytest.raises(ComponentSchemaError, match="requires a dataclass"):
        component(type_id=UUID("aaaaaaaa-0000-0000-0000-00000000000d"))(Ordinary)
    with pytest.raises(ComponentSchemaError, match="must use slots"):
        component(type_id=UUID("aaaaaaaa-0000-0000-0000-00000000000e"))(Unslotted)
    with pytest.raises(ComponentSchemaError, match="requires a dataclass class"):
        component(type_id=UUID("aaaaaaaa-0000-0000-0000-000000000014"))(
            cast(type[object], SlottedInstance())
        )
    with pytest.raises(ComponentSchemaError, match="inheritance is not supported"):
        component(type_id=UUID("aaaaaaaa-0000-0000-0000-000000000016"))(Inherited)

    @dataclass(slots=True)
    class Local:
        value: int = 0

    with pytest.raises(ComponentSchemaError, match="stable module-qualified name"):
        component(type_id=UUID("aaaaaaaa-0000-0000-0000-00000000000f"))(Local)


@pytest.mark.parametrize(
    ("annotation", "field_definition", "message"),
    [
        (list[int], field(default=None), "must use bool, int, float, str"),
        ("int", field(default=0), "must use bool, int, float, str"),
        (str, field(default_factory=str), "default_factory"),
        (int, field(default=0, init=False), "participate in dataclass initialization"),
        (int, field(default=True), "does not match"),
        (float, field(default=float("nan")), "must be finite"),
    ],
)
def test_invalid_component_fields_fail(
    annotation: object,
    field_definition: Field[Any],
    message: str,
) -> None:
    component_type = make_dataclass(
        "InvalidField",
        [("value", cast(Any, annotation), field_definition)],
        slots=True,
    )
    component_type.__module__ = __name__
    component_type.__qualname__ = f"InvalidField_{message}"

    with pytest.raises(ComponentSchemaError, match=message):
        component(type_id=UUID("aaaaaaaa-0000-0000-0000-000000000010"))(component_type)


def test_invalid_inspection_metadata_is_rejected_and_valid_input_is_copied() -> None:
    metadata: dict[str, object] = {"order": 1}
    decorator = component(
        type_id=UUID("aaaaaaaa-0000-0000-0000-000000000011"),
        inspection_metadata=cast("Metadata", metadata),
    )
    metadata["order"] = 2
    component_type = make_dataclass("MetadataCopy", [("value", int, field(default=0))], slots=True)
    component_type.__module__ = __name__
    component_type.__qualname__ = "MetadataCopy"
    decorated = cast(type[object], decorator(component_type))
    schema = component_schema(decorated)

    assert schema.inspection_metadata == (("order", 1),)
    with pytest.raises(ComponentSchemaError, match="must be scalar"):
        component(
            type_id=UUID("aaaaaaaa-0000-0000-0000-000000000012"),
            inspection_metadata=cast("Metadata", {"invalid": []}),
        )
    with pytest.raises(ComponentSchemaError, match="keys must be non-empty strings"):
        component(
            type_id=UUID("aaaaaaaa-0000-0000-0000-000000000017"),
            inspection_metadata=cast("Metadata", {cast(str, 1): "invalid"}),
        )


def test_root_public_api_remains_deliberately_small() -> None:
    assert "component" not in ludoweave.__all__
    assert "ComponentRegistry" not in ludoweave.__all__


type CallableMigration = Callable[[Mapping[str, object]], Mapping[str, object]]
type Metadata = Mapping[str, str | int | float | bool | None]


def _make_migrating_component(
    name: str,
    type_id: UUID,
    migration: CallableMigration,
) -> type[object]:
    component_type = make_dataclass(name, [("value", int)], slots=True)
    component_type.__module__ = __name__
    component_type.__qualname__ = name
    return cast(
        type[object],
        component(
            type_id=type_id,
            version=2,
            migrations=(ComponentMigration(1, 2, migration),),
        )(component_type),
    )


def _make_presentation_component() -> type[object]:
    component_type = make_dataclass(
        "PresentationOnly",
        [("text", str, field(default=""))],
        slots=True,
    )
    component_type.__module__ = __name__
    component_type.__qualname__ = "PresentationOnly"
    return cast(
        type[object],
        component(
            type_id=UUID("aaaaaaaa-0000-0000-0000-000000000013"),
            authoritative=False,
            serialization=SerializationPolicy.EXCLUDED,
            determinism=DeterminismTier.D0,
            storage_hint=StorageHint.ROW,
        )(component_type),
    )
