"""Property coverage for deterministic component registration and migrations."""

from collections.abc import Mapping
from dataclasses import dataclass
from uuid import UUID

from hypothesis import given
from hypothesis import strategies as st

from ludoweave.ecs import ComponentMigration, ComponentRegistry, component, component_schema


def _counter_v1_to_v2(values: Mapping[str, object]) -> Mapping[str, object]:
    value = values["value"]
    if type(value) is not int:
        raise TypeError("value must be int")
    return {"value": value + 7}


@component(
    type_id=UUID("bbbbbbbb-0000-0000-0000-000000000001"),
    version=2,
    migrations=(ComponentMigration(1, 2, _counter_v1_to_v2),),
)
@dataclass(slots=True)
class Counter:
    value: int


@component(type_id=UUID("bbbbbbbb-0000-0000-0000-000000000002"))
@dataclass(slots=True)
class Alpha:
    value: int = 0


@component(type_id=UUID("bbbbbbbb-0000-0000-0000-000000000003"))
@dataclass(slots=True)
class Beta:
    value: int = 0


@given(value=st.integers(min_value=-(2**63), max_value=2**63 - 1))
def test_migration_matches_model_and_preserves_source(value: int) -> None:
    registry = ComponentRegistry((Counter,))
    source: dict[str, object] = {"value": value}

    migrated = registry.migrate(component_schema(Counter).type_id, from_version=1, values=source)

    assert migrated == {"value": value + 7}
    assert source == {"value": value}


@given(order=st.permutations((Counter, Alpha, Beta)))
def test_registry_enumeration_is_independent_of_input_order(order: list[type[object]]) -> None:
    registry = ComponentRegistry(order)

    assert tuple(schema.type_id for schema in registry.schemas) == tuple(
        sorted(
            (component_schema(item).type_id for item in (Counter, Alpha, Beta)),
            key=lambda item: item.bytes,
        )
    )
