"""Deterministic production/reference world conformance checks."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast
from uuid import UUID

import pytest

from ludoweave.core import LudoWeaveError
from ludoweave.ecs import ComponentRegistry, EntityId, ReferenceWorld, World, component


@component(type_id=UUID("eeeeeeee-0000-0000-0000-000000000001"))
@dataclass(slots=True)
class Counter:
    value: int = 0


@component(type_id=UUID("eeeeeeee-0000-0000-0000-000000000002"))
@dataclass(slots=True)
class Enabled:
    value: bool = True


@component(type_id=UUID("eeeeeeee-0000-0000-0000-000000000003"))
@dataclass(slots=True)
class HostileModel:
    value: int = 0

    def __getattribute__(self, name: str) -> object:
        current = object.__getattribute__(self, name)
        if name == "value":
            object.__setattr__(self, name, "changed-by-getter")
        return current


REGISTRY = ComponentRegistry((Enabled, Counter))


@pytest.mark.parametrize("factory", [World, ReferenceWorld])
def test_each_world_has_the_same_direct_contract(
    factory: Callable[[ComponentRegistry], World | ReferenceWorld],
) -> None:
    world = factory(REGISTRY)
    entity_id = world.spawn(Counter(1))

    world.add(entity_id, Enabled())
    world.patch(entity_id, Counter, value=2)

    assert world.get(entity_id, Counter) == Counter(2)
    assert world.remove(entity_id, Enabled) == Enabled()
    assert not world.has(entity_id, Enabled)


@pytest.mark.parametrize("factory", [World, ReferenceWorld])
def test_each_world_clone_is_independent_and_preserves_allocator_order(
    factory: Callable[[ComponentRegistry], World | ReferenceWorld],
) -> None:
    world = factory(REGISTRY)
    first = world.spawn(Counter(1))
    retained = world.spawn(Counter(2))
    last = world.spawn(Counter(3))
    world.destroy(first)
    world.destroy(last)
    duplicate = world.clone()

    assert duplicate.entities() == world.entities()
    assert duplicate.epoch == world.epoch
    assert duplicate.structural_epoch == world.structural_epoch
    for component_type in REGISTRY.component_types:
        assert duplicate.components(component_type) == world.components(component_type)
        assert duplicate.component_structural_epoch(
            component_type
        ) == world.component_structural_epoch(component_type)
        for entity_id, _ in world.components(component_type):
            assert duplicate.component_epoch(entity_id, component_type) == world.component_epoch(
                entity_id, component_type
            )

    expected_first = EntityId(last.index, last.generation + 1)
    expected_second = EntityId(first.index, first.generation + 1)
    assert (world.spawn(), world.spawn()) == (expected_first, expected_second)
    assert (duplicate.spawn(), duplicate.spawn()) == (expected_first, expected_second)
    duplicate.patch(retained, Counter, value=9)

    assert world.get(retained, Counter) == Counter(2)
    assert duplicate.get(retained, Counter) == Counter(9)


def test_scripted_mutations_and_structured_failures_match_after_every_step() -> None:
    production = World(REGISTRY)
    reference = ReferenceWorld(REGISTRY)

    first = _same_call(production.spawn, reference.spawn, Counter(1))
    second = _same_call(production.spawn, reference.spawn, Counter(2), Enabled(False))
    assert isinstance(first, EntityId)
    assert isinstance(second, EntityId)
    _assert_same_state(production, reference)

    operations: tuple[
        tuple[Callable[..., object], Callable[..., object], tuple[object, ...]], ...
    ] = (
        (production.add, reference.add, (first, Enabled(True))),
        (production.add, reference.add, (first, Enabled(False))),
        (production.patch, reference.patch, (first, Counter)),
        (production.remove, reference.remove, (second, Counter)),
        (production.remove, reference.remove, (second, Counter)),
        (production.replace, reference.replace, (first, Counter(9))),
        (production.destroy, reference.destroy, (second,)),
        (production.get, reference.get, (second, Enabled)),
    )
    for production_call, reference_call, arguments in operations:
        _same_call(production_call, reference_call, *arguments)
        _assert_same_state(production, reference)

    replacement = _same_call(production.spawn, reference.spawn, Counter(10))
    assert replacement == EntityId(second.index, second.generation + 1)
    _same_call(production.get, reference.get, second, Counter)
    _assert_same_state(production, reference)


def test_malformed_required_slots_fail_structurally_without_allocating() -> None:
    production = World(REGISTRY)
    reference = ReferenceWorld(REGISTRY)
    malformed = object.__new__(Counter)

    result = _same_call(production.spawn, reference.spawn, malformed)
    error_result = cast(tuple[str, type[LudoWeaveError], dict[str, object]], result)

    assert error_result[0] == "error"
    assert error_result[1].__name__ == "InvalidComponentValueError"
    _assert_same_state(production, reference)
    assert production.epoch == reference.epoch == 0
    assert _same_call(production.spawn, reference.spawn) == EntityId(0, 0)


def test_hostile_getters_cannot_mutate_either_canonical_world() -> None:
    registry = ComponentRegistry((HostileModel,))
    production = World(registry)
    reference = ReferenceWorld(registry)
    source = HostileModel(4)

    entity_id = _same_call(production.spawn, reference.spawn, source)
    assert isinstance(entity_id, EntityId)
    production_value = production.get(entity_id, HostileModel)
    reference_value = reference.get(entity_id, HostileModel)

    assert object.__getattribute__(source, "value") == 4
    assert object.__getattribute__(production_value, "value") == 4
    assert object.__getattribute__(reference_value, "value") == 4
    assert object.__getattribute__(production.get(entity_id, HostileModel), "value") == 4
    assert object.__getattribute__(reference.get(entity_id, HostileModel), "value") == 4


def _same_call(
    production_call: Callable[..., object],
    reference_call: Callable[..., object],
    *arguments: object,
) -> object:
    production_result = _capture(production_call, arguments)
    reference_result = _capture(reference_call, arguments)
    assert production_result == reference_result
    if production_result[0] == "return":
        return production_result[1]
    return production_result


def _capture(call: Callable[..., object], arguments: tuple[object, ...]) -> tuple[object, ...]:
    try:
        return ("return", call(*arguments))
    except LudoWeaveError as error:
        return ("error", type(error), error.as_dict())


def _assert_same_state(production: World, reference: ReferenceWorld) -> None:
    assert production.entities() == reference.entities()
    assert production.epoch == reference.epoch
    assert production.structural_epoch == reference.structural_epoch
    for component_type in REGISTRY.component_types:
        assert production.components(component_type) == reference.components(component_type)
        assert production.component_structural_epoch(
            component_type
        ) == reference.component_structural_epoch(component_type)
        for entity_id, _ in production.components(component_type):
            assert production.component_epoch(
                entity_id, component_type
            ) == reference.component_epoch(entity_id, component_type)
