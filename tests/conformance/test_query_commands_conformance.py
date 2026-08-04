"""Production/reference conformance for queries and local deferred commands."""

from collections.abc import Callable
from dataclasses import dataclass, replace
from math import copysign
from uuid import UUID

import pytest

from ludoweave.core import LudoWeaveError
from ludoweave.ecs import (
    ComponentRegistry,
    InvalidDeferredEntityError,
    ReferenceWorld,
    World,
    component,
)


@component(type_id=UUID("f3000000-0000-0000-0000-000000000001"))
@dataclass(slots=True)
class Counter:
    value: int = 0


@component(type_id=UUID("f3000000-0000-0000-0000-000000000002"))
@dataclass(slots=True)
class Enabled:
    value: bool = True


@component(type_id=UUID("f3000000-0000-0000-0000-000000000003"))
@dataclass(slots=True)
class Excluded:
    value: int = 0


@component(type_id=UUID("f3000000-0000-0000-0000-000000000004"))
@dataclass(slots=True)
class ScalarFloat:
    value: float = 0.0


REGISTRY = ComponentRegistry((Enabled, Excluded, Counter, ScalarFloat))


@pytest.mark.parametrize("factory", [World, ReferenceWorld])
def test_each_world_supports_the_same_query_cursor_contract(
    factory: Callable[[ComponentRegistry], World | ReferenceWorld],
) -> None:
    world = factory(REGISTRY)
    first = world.spawn(Counter(1), Enabled())
    world.spawn(Counter(2), Enabled(False), Excluded())
    baseline = world.epoch
    world.patch(first, Counter, value=3)

    assert list(
        world.query(Counter, Enabled)
        .without(Excluded)
        .changed_since(baseline, Counter)
        .stable()
        .rows()
    ) == [(first, Counter(3), Enabled())]

    with world.query(Counter).writes(Counter).rows() as rows:
        entity_id, counter = next(rows)
        assert entity_id == first
        counter.value = 4
    assert world.get(first, Counter) == Counter(4)


def test_scripted_query_results_epochs_and_failures_match() -> None:
    production = World(REGISTRY)
    reference = ReferenceWorld(REGISTRY)
    for value in range(4):
        components: tuple[object, ...] = (Counter(value), Enabled(value % 2 == 0))
        if value == 2:
            components = (*components, Excluded())
        assert production.spawn(*components) == reference.spawn(*components)

    production_rows = list(production.query(Counter, Enabled).without(Excluded).stable().rows())
    reference_rows = list(reference.query(Counter, Enabled).without(Excluded).stable().rows())
    assert production_rows == reference_rows

    with (
        production.query(Counter, Enabled).writes(Counter, Enabled).stable().rows() as left,
        reference.query(Counter, Enabled).writes(Counter, Enabled).stable().rows() as right,
    ):
        for left_row, right_row in zip(left, right, strict=True):
            assert left_row == right_row
            left_row[1].value += 10
            right_row[1].value += 10
            left_row[2].value = not left_row[2].value
            right_row[2].value = not right_row[2].value

    _assert_same_state(production, reference)
    assert _same_error(
        lambda: list(production.query(Counter).changed_since(production.epoch + 1).rows()),
        lambda: list(reference.query(Counter).changed_since(reference.epoch + 1).rows()),
    )


def test_scripted_command_success_and_resolution_match() -> None:
    production = World(REGISTRY)
    reference = ReferenceWorld(REGISTRY)
    left_existing = production.spawn(Counter(1))
    right_existing = reference.spawn(Counter(1))
    assert left_existing == right_existing
    left = production.commands()
    right = reference.commands()
    left_token = left.spawn(Counter(2))
    right_token = right.spawn(Counter(2))
    left.add(left_token, Enabled(False))
    right.add(right_token, Enabled(False))
    left.remove(left_token, Counter)
    right.remove(right_token, Counter)
    left.destroy(left_existing)
    right.destroy(right_existing)

    left_result = production.flush(left)
    right_result = reference.flush(right)

    assert left_result.command_count == right_result.command_count
    assert left_result.start_epoch == right_result.start_epoch
    assert left_result.end_epoch == right_result.end_epoch
    assert left_result.resolve(left_token) == right_result.resolve(right_token)
    _assert_same_state(production, reference)


def test_scripted_command_failure_and_retry_match_without_mutation() -> None:
    production = World(REGISTRY)
    reference = ReferenceWorld(REGISTRY)
    left = production.commands()
    right = reference.commands()
    left_token = left.spawn(Counter(1))
    right_token = right.spawn(Counter(1))
    left.add(left_token, Counter(2))
    right.add(right_token, Counter(2))

    for _ in range(2):
        assert _same_error(lambda: production.flush(left), lambda: reference.flush(right))
        assert len(left) == len(right) == 2
        _assert_same_state(production, reference)


@pytest.mark.parametrize("factory", [World, ReferenceWorld])
def test_copied_token_cannot_enqueue_or_resolve(
    factory: Callable[[ComponentRegistry], World | ReferenceWorld],
) -> None:
    world = factory(REGISTRY)
    commands = world.commands()
    token = commands.spawn(Counter(1))
    copied = replace(token)

    with pytest.raises(InvalidDeferredEntityError):
        commands.add(copied, Enabled())

    result = world.flush(commands)
    assert result.resolve(token) in world.entities()
    with pytest.raises(InvalidDeferredEntityError):
        result.resolve(copied)


@pytest.mark.parametrize("factory", [World, ReferenceWorld])
def test_writable_query_distinguishes_negative_and_positive_zero(
    factory: Callable[[ComponentRegistry], World | ReferenceWorld],
) -> None:
    world = factory(REGISTRY)
    entity_id = world.spawn(ScalarFloat(-0.0))
    before = world.epoch

    with world.query(ScalarFloat).writes(ScalarFloat).rows() as rows:
        _, value = next(rows)
        value.value = 0.0

    assert world.epoch == before + 1
    stored = world.get(entity_id, ScalarFloat)
    assert copysign(1.0, stored.value) == 1.0


def _same_error(left: Callable[[], object], right: Callable[[], object]) -> bool:
    outcomes: list[tuple[type[LudoWeaveError], dict[str, object]]] = []
    for operation in (left, right):
        try:
            operation()
        except LudoWeaveError as error:
            outcomes.append((type(error), error.as_dict()))
        else:
            pytest.fail("both conformance operations must fail")
    assert outcomes[0][0].__name__ == outcomes[1][0].__name__
    assert outcomes[0][1] == outcomes[1][1]
    return True


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
