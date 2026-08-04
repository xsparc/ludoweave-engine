"""Production world-storage behavior and failure atomicity tests."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast
from uuid import UUID

import pytest

from ludoweave import __all__ as root_exports
from ludoweave.ecs import (
    ComponentAlreadyPresentError,
    ComponentRegistry,
    EntityId,
    InvalidComponentValueError,
    MissingComponentError,
    StaleEntityError,
    StorageHint,
    UnknownComponentError,
    World,
    component,
)


@component(type_id=UUID("dddddddd-0000-0000-0000-000000000001"))
@dataclass(slots=True)
class Position:
    x: int = 0
    y: int = 0


@component(type_id=UUID("dddddddd-0000-0000-0000-000000000002"))
@dataclass(frozen=True, slots=True, kw_only=True)
class Name:
    value: str


@component(type_id=UUID("dddddddd-0000-0000-0000-000000000003"))
@dataclass(slots=True)
class Motion:
    speed: float = 0.0
    enabled: bool = True


@component(type_id=UUID("dddddddd-0000-0000-0000-000000000004"))
@dataclass(slots=True)
class Tag:
    pass


@component(type_id=UUID("dddddddd-0000-0000-0000-000000000005"))
@dataclass(slots=True)
class HostileGetter:
    value: int = 0

    def __getattribute__(self, name: str) -> object:
        current = object.__getattribute__(self, name)
        if name == "value":
            object.__setattr__(self, name, "corrupted")
        return current


@component(type_id=UUID("dddddddd-0000-0000-0000-000000000006"), storage_hint=StorageHint.ROW)
@dataclass(slots=True)
class RowHinted:
    value: int = 0


@component(type_id=UUID("dddddddd-0000-0000-0000-000000000007"), storage_hint=StorageHint.COLUMN)
@dataclass(slots=True)
class ColumnHinted:
    value: int = 0


REGISTRY = ComponentRegistry((Motion, Name, Tag, Position))


def test_empty_world_and_multi_component_spawn_have_canonical_epochs() -> None:
    world = World(REGISTRY)

    assert world.registry is REGISTRY
    assert world.entities() == ()
    assert world.components(Position) == ()
    assert world.epoch == 0
    assert world.structural_epoch == 0
    assert world.component_structural_epoch(Position) == 0

    entity_id = world.spawn(Position(1, 2), Name(value="hero"))

    assert entity_id == EntityId(0, 0)
    assert world.entities() == (entity_id,)
    assert world.get(entity_id, Position) == Position(1, 2)
    assert world.get(entity_id, Name) == Name(value="hero")
    assert world.component_epoch(entity_id, Position) == 1
    assert world.component_epoch(entity_id, Name) == 1
    assert world.component_structural_epoch(Position) == 1
    assert world.component_structural_epoch(Name) == 1
    assert world.component_structural_epoch(Motion) == 0
    assert world.epoch == world.structural_epoch == 1


def test_swap_remove_middle_repairs_sparse_location_and_preserves_moved_epoch() -> None:
    world = World(REGISTRY)
    first = world.spawn(Position(1, 0))
    middle = world.spawn(Position(2, 0))
    moved = world.spawn(Position(3, 0))
    moved_epoch = world.component_epoch(moved, Position)

    assert world.remove(middle, Position) == Position(2, 0)

    assert world.components(Position) == (
        (first, Position(1, 0)),
        (moved, Position(3, 0)),
    )
    assert world.component_epoch(moved, Position) == moved_epoch
    assert world.patch(moved, Position, y=7) == Position(3, 7)
    assert world.remove(moved, Position) == Position(3, 7)
    world._check_invariants()  # pyright: ignore[reportPrivateUsage]


def test_destroy_cleans_multiple_middle_rows_and_reuse_inherits_nothing() -> None:
    world = World(REGISTRY)
    first = world.spawn(Position(1, 1), Motion(1.0))
    retired = world.spawn(Position(2, 2), Motion(2.0), Tag())
    last = world.spawn(Position(3, 3), Motion(3.0))
    before = world.epoch

    world.destroy(retired)

    assert world.epoch == before + 1
    assert world.entities() == (first, last)
    assert world.components(Position) == (
        (first, Position(1, 1)),
        (last, Position(3, 3)),
    )
    assert world.components(Motion) == (
        (first, Motion(1.0)),
        (last, Motion(3.0)),
    )
    replacement = world.spawn()
    assert replacement == EntityId(retired.index, retired.generation + 1)
    assert not world.has(replacement, Position)
    assert not world.has(replacement, Tag)
    with pytest.raises(StaleEntityError):
        world.get(retired, Position)
    world._check_invariants()  # pyright: ignore[reportPrivateUsage]


def test_every_entity_scoped_operation_rejects_stale_handles_atomically() -> None:
    world = World(REGISTRY)
    stale = world.spawn(Position(1, 1))
    world.destroy(stale)
    replacement = world.spawn(Position(2, 2))
    assert replacement.index == stale.index
    before = _fingerprint(world)
    operations: tuple[Callable[[], object], ...] = (
        lambda: world.destroy(stale),
        lambda: world.add(stale, Motion(1.0)),
        lambda: world.replace(stale, Position(3, 3)),
        lambda: world.patch(stale, Position, x=3),
        lambda: world.remove(stale, Position),
        lambda: world.has(stale, Position),
        lambda: world.get(stale, Position),
        lambda: world.component_epoch(stale, Position),
    )

    for operation in operations:
        with pytest.raises(StaleEntityError):
            operation()
        assert _fingerprint(world) == before

    for forged in (EntityId(99, 0), EntityId(replacement.index, replacement.generation + 1)):
        with pytest.raises(StaleEntityError):
            world.has(forged, Position)
        assert _fingerprint(world) == before


def test_canonical_state_isolated_from_input_and_output_aliases() -> None:
    world = World(REGISTRY)
    source = Position(4, 5)
    first = world.spawn(source)
    second = world.spawn(source)
    epoch = world.epoch

    source.x = 99
    retrieved = world.get(first, Position)
    retrieved.y = 88
    enumerated = world.components(Position)
    enumerated[0][1].x = 77

    assert world.get(first, Position) == Position(4, 5)
    assert world.get(second, Position) == Position(4, 5)
    assert world.get(first, Position) is not world.get(first, Position)
    assert world.epoch == epoch


def test_add_replace_patch_remove_and_epoch_contract() -> None:
    world = World(REGISTRY)
    entity_id = world.spawn()

    returned = world.add(entity_id, Position(1, 2))
    assert returned == Position(1, 2)
    returned.x = 10
    add_epoch = world.epoch
    assert world.component_epoch(entity_id, Position) == add_epoch
    assert world.structural_epoch == add_epoch

    replaced = world.replace(entity_id, Position(1, 2))
    assert replaced == Position(1, 2)
    replace_epoch = world.epoch
    assert replace_epoch == add_epoch + 1
    assert world.component_epoch(entity_id, Position) == replace_epoch
    assert world.structural_epoch == add_epoch

    patched = world.patch(entity_id, Position, x=1)
    assert patched == Position(1, 2)
    assert world.epoch == replace_epoch + 1
    assert world.component_epoch(entity_id, Position) == world.epoch
    assert world.structural_epoch == add_epoch

    removed = world.remove(entity_id, Position)
    assert removed == Position(1, 2)
    assert not world.has(entity_id, Position)
    assert world.structural_epoch == world.epoch
    assert world.component_structural_epoch(Position) == world.epoch


def test_frozen_keyword_only_and_empty_components_support_storage_and_patch() -> None:
    world = World(REGISTRY)
    entity_id = world.spawn(Name(value="before"), Tag())

    assert world.patch(entity_id, Name, value="after") == Name(value="after")
    assert world.get(entity_id, Name) == Name(value="after")
    assert world.get(entity_id, Tag) == Tag()


@pytest.mark.parametrize("world_operation", ["duplicate", "missing", "empty", "unknown"])
def test_expected_failures_are_atomic(world_operation: str) -> None:
    world = World(REGISTRY)
    entity_id = world.spawn(Position(2, 3))
    before = _fingerprint(world)

    if world_operation == "duplicate":
        with pytest.raises(ComponentAlreadyPresentError):
            world.add(entity_id, Position(9, 9))
    elif world_operation == "missing":
        with pytest.raises(MissingComponentError):
            world.remove(entity_id, Motion)
    elif world_operation == "empty":
        with pytest.raises(InvalidComponentValueError):
            world.patch(entity_id, Position)
    else:

        @dataclass(slots=True)
        class Undeclared:
            value: int = 0

        with pytest.raises(UnknownComponentError):
            world.add(entity_id, Undeclared())

    assert _fingerprint(world) == before


def test_duplicate_spawn_is_preflighted_before_entity_allocation() -> None:
    world = World(REGISTRY)

    with pytest.raises(ComponentAlreadyPresentError):
        world.spawn(Position(1, 1), Position(2, 2))

    assert world.epoch == 0
    assert world.entities() == ()
    assert world.spawn() == EntityId(0, 0)


def test_uninitialized_component_slots_raise_structured_errors_atomically() -> None:
    world = World(REGISTRY)
    malformed = object.__new__(Position)

    with pytest.raises(InvalidComponentValueError) as caught:
        world.spawn(malformed)

    assert caught.value.phase == "spawn"
    assert dict(caught.value.details)["reason"] == "unreadable_field"
    assert isinstance(caught.value.__cause__, AttributeError)
    assert world.epoch == 0
    assert world.entities() == ()
    assert world.spawn() == EntityId(0, 0)


def test_component_getters_cannot_change_validated_or_canonical_values() -> None:
    registry = ComponentRegistry((HostileGetter,))
    world = World(registry)
    source = HostileGetter(7)

    entity_id = world.spawn(source)
    first = world.get(entity_id, HostileGetter)
    second = world.get(entity_id, HostileGetter)

    assert object.__getattribute__(source, "value") == 7
    assert object.__getattribute__(first, "value") == 7
    assert object.__getattribute__(second, "value") == 7
    assert world.component_epoch(entity_id, HostileGetter) == 1


def test_storage_hints_are_advisory_with_identical_public_behavior() -> None:
    registry = ComponentRegistry((Position, RowHinted, ColumnHinted))
    world = World(registry)
    entity_id = world.spawn(Position(1, 0), RowHinted(2), ColumnHinted(3))

    assert world.patch(entity_id, Position, x=4) == Position(4, 0)
    assert world.patch(entity_id, RowHinted, value=5) == RowHinted(5)
    assert world.patch(entity_id, ColumnHinted, value=6) == ColumnHinted(6)
    assert world.component_epoch(entity_id, Position) == 2
    assert world.component_epoch(entity_id, RowHinted) == 3
    assert world.component_epoch(entity_id, ColumnHinted) == 4


@pytest.mark.parametrize("invalid", [True, None, "wrong", float("nan"), float("inf")])
def test_invalid_patch_values_are_atomic(invalid: object) -> None:
    world = World(REGISTRY)
    entity_id = world.spawn(Motion(2.0, True))
    before = _fingerprint(world)

    with pytest.raises(InvalidComponentValueError):
        world.patch(entity_id, Motion, speed=invalid)

    assert _fingerprint(world) == before


@pytest.mark.parametrize("invalid", [True, None, float("nan"), float("inf")])
def test_tampered_component_values_are_rejected_without_mutation(invalid: object) -> None:
    world = World(REGISTRY)
    entity_id = world.spawn(Position(1, 2))
    tampered = Motion(1.0)
    tampered.speed = cast(float, invalid)
    before = _fingerprint(world)

    with pytest.raises(InvalidComponentValueError) as caught:
        world.add(entity_id, tampered)

    assert caught.value.code == "ecs.invalid_component_value"
    assert _fingerprint(world) == before


def test_mixed_invalid_patch_is_atomic_and_does_not_leak_values_in_errors() -> None:
    world = World(REGISTRY)
    entity_id = world.spawn(Position(1, 2))
    before = _fingerprint(world)

    with pytest.raises(InvalidComponentValueError) as caught:
        world.patch(entity_id, Position, x=5, secret_unknown="credential-value")

    assert _fingerprint(world) == before
    assert "credential-value" not in str(caught.value.as_dict())


def test_clone_is_independent_and_preserves_future_allocation_order() -> None:
    world = World(REGISTRY)
    first = world.spawn(Position(1, 1))
    retired = world.spawn(Name(value="retire"))
    world.destroy(retired)
    duplicate = world.clone()

    expected = EntityId(retired.index, retired.generation + 1)
    assert world.spawn() == expected
    assert duplicate.spawn() == expected
    duplicate.patch(first, Position, x=9)

    assert world.get(first, Position) == Position(1, 1)
    assert duplicate.get(first, Position) == Position(9, 1)


def test_worlds_are_isolated_even_when_the_registry_is_shared() -> None:
    first_world = World(REGISTRY)
    second_world = World(REGISTRY)

    first = first_world.spawn(Position(1, 1))
    second = second_world.spawn(Position(2, 2))

    assert first == second == EntityId(0, 0)
    assert first_world.get(first, Position) == Position(1, 1)
    assert second_world.get(second, Position) == Position(2, 2)
    assert first_world.epoch == second_world.epoch == 1


def test_stable_inspection_order_does_not_expose_dense_history() -> None:
    world = World(REGISTRY)
    first = world.spawn(Position(1, 0))
    middle = world.spawn(Position(2, 0))
    last = world.spawn(Position(3, 0))
    world.remove(first, Position)
    world.add(first, Position(4, 0))
    world.destroy(middle)

    assert world.entities() == tuple(sorted((first, last), key=EntityId.as_tuple))
    assert world.components(Position) == (
        (first, Position(4, 0)),
        (last, Position(3, 0)),
    )


def test_world_contract_does_not_expand_root_api() -> None:
    assert "World" not in root_exports
    assert "ReferenceWorld" not in root_exports


def _fingerprint(world: World) -> tuple[object, ...]:
    component_state = tuple(
        (
            component_type,
            world.component_structural_epoch(component_type),
            tuple(
                (
                    entity_id,
                    value,
                    world.component_epoch(entity_id, component_type),
                )
                for entity_id, value in world.components(component_type)
            ),
        )
        for component_type in REGISTRY.component_types
    )
    return (
        world.entities(),
        world.epoch,
        world.structural_epoch,
        component_state,
    )
