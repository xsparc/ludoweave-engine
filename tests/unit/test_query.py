"""Storage-neutral query behavior, writeback, and cursor ownership tests."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, assert_type
from uuid import UUID

import pytest

from ludoweave.ecs import (
    ActiveQueryError,
    ComponentRegistry,
    EntityId,
    InvalidComponentValueError,
    InvalidQueryError,
    Query,
    QueryLifecycleError,
    World,
    component,
)


@component(type_id=UUID("f1000000-0000-0000-0000-000000000001"))
@dataclass(slots=True)
class Position:
    x: int = 0
    y: int = 0


@component(type_id=UUID("f1000000-0000-0000-0000-000000000002"))
@dataclass(slots=True)
class Velocity:
    x: int = 0
    y: int = 0


@component(type_id=UUID("f1000000-0000-0000-0000-000000000003"))
@dataclass(slots=True)
class Hidden:
    value: bool = True


@component(type_id=UUID("f1000000-0000-0000-0000-000000000004"))
@dataclass(frozen=True, slots=True)
class FrozenName:
    value: str = ""


@component(type_id=UUID("f1000000-0000-0000-0000-000000000005"))
@dataclass(slots=True, eq=False)
class HostileBehavior:
    value: int = 0

    def __getattribute__(self, name: str) -> object:
        if name == "value":
            raise AssertionError("query copy must bypass author getters")
        return object.__getattribute__(self, name)

    def __eq__(self, other: object) -> bool:
        del other
        raise AssertionError("query writeback must not invoke component equality")


REGISTRY = ComponentRegistry((Hidden, Velocity, FrozenName, Position, HostileBehavior))


if TYPE_CHECKING:

    def _assert_static_query_shapes(world: World) -> None:
        assert_type(world.query(), Query[()])
        assert_type(world.query(Position), Query[Position])
        assert_type(world.query(Position, Velocity), Query[Position, Velocity])
        assert_type(
            world.query(Position, Velocity, Hidden),
            Query[Position, Velocity, Hidden],
        )
        assert_type(
            world.query(Position, Velocity, Hidden, FrozenName),
            Query[Position, Velocity, Hidden, FrozenName],
        )
        assert_type(
            world.query(Position, Velocity, Hidden, FrozenName, HostileBehavior),
            Query[*tuple[object, ...]],
        )
        assert_type(
            next(world.query(Position, Velocity).rows()),
            tuple[EntityId, Position, Velocity],
        )

    _ = _assert_static_query_shapes


def test_query_include_exclude_zero_include_and_stable_order() -> None:
    world = World(REGISTRY)
    first = world.spawn(Position(1, 1), Velocity(2, 2))
    excluded = world.spawn(Position(3, 3), Velocity(4, 4), Hidden())
    third = world.spawn(Position(5, 5))
    world.destroy(first)
    reused = world.spawn(Position(7, 7), Velocity(8, 8))

    rows = list(world.query(Position, Velocity).without(Hidden).stable().rows())
    assert rows == [(reused, Position(7, 7), Velocity(8, 8))]
    assert excluded not in {row[0] for row in rows}
    assert third not in {row[0] for row in rows}

    all_entities = list(world.query().stable().rows())
    assert all_entities == [(entity_id,) for entity_id in world.entities()]
    without_hidden = list(world.query().without(Hidden).stable().rows())
    assert without_hidden == [
        (entity_id,) for entity_id in world.entities() if entity_id != excluded
    ]


def test_query_builder_rejects_ambiguous_and_unregistered_specs() -> None:
    world = World(REGISTRY)

    with pytest.raises(InvalidQueryError):
        world.query(Position, Position)
    with pytest.raises(InvalidQueryError):
        world.query(Position).without(Hidden, Hidden)
    with pytest.raises(InvalidQueryError):
        world.query(Position).writes(Position).writes(Position)
    with pytest.raises(InvalidQueryError):
        world.query(Position).without(Position)
    with pytest.raises(InvalidQueryError):
        world.query(Position).writes(Velocity)
    with pytest.raises(InvalidQueryError):
        world.query(FrozenName).writes(FrozenName)
    with pytest.raises(InvalidQueryError):
        world.query().changed_since(0)
    with pytest.raises(InvalidQueryError):
        world.query(Position).changed_since(-1)
    with pytest.raises(InvalidQueryError):
        world.query(Position).changed_since(True)
    with pytest.raises(InvalidQueryError):
        world.query(Position).changed_since(0, Velocity)
    with pytest.raises(InvalidQueryError):
        world.query(str)


def test_changed_since_is_strict_uses_or_semantics_and_rejects_future_epoch() -> None:
    world = World(REGISTRY)
    first = world.spawn(Position(1, 1), Velocity(2, 2))
    second = world.spawn(Position(3, 3), Velocity(4, 4))
    baseline = world.epoch
    world.patch(first, Position, x=9)
    world.patch(second, Velocity, y=8)

    assert list(world.query(Position, Velocity).changed_since(baseline).stable().rows()) == [
        (first, Position(9, 1), Velocity(2, 2)),
        (second, Position(3, 3), Velocity(4, 8)),
    ]
    assert list(
        world.query(Position, Velocity).changed_since(baseline, Position).stable().rows()
    ) == [(first, Position(9, 1), Velocity(2, 2))]
    assert list(world.query(Position).changed_since(world.epoch).rows()) == []

    same_value_baseline = world.epoch
    world.patch(first, Position, x=9)
    assert list(world.query(Position).changed_since(same_value_baseline).stable().rows()) == [
        (first, Position(9, 1))
    ]
    with pytest.raises(InvalidQueryError):
        list(world.query(Position).changed_since(world.epoch + 1).rows())

    # A failed activation must release its lease.
    world.spawn(Position(10, 10))


def test_read_only_rows_are_detached_and_nested_readers_block_mutation() -> None:
    world = World(REGISTRY)
    entity_id = world.spawn(Position(1, 2))
    first = world.query(Position).rows()
    second = world.query(Position).rows()
    iter(first)
    iter(second)

    with pytest.raises(ActiveQueryError):
        world.spawn(object())
    first.close()
    with pytest.raises(ActiveQueryError):
        world.destroy(object())  # type: ignore[arg-type]
    second.close()

    cursor = world.query(Position).rows()
    row = next(cursor)
    cursor.close()
    row[1].x = 99
    assert world.get(entity_id, Position) == Position(1, 2)


def test_writable_query_requires_context_and_commits_changed_rows_only() -> None:
    world = World(REGISTRY)
    entity_id = world.spawn(Position(1, 2), Velocity(3, 4))
    before = world.epoch
    cursor = world.query(Position, Velocity).writes(Position, Velocity).rows()

    with pytest.raises(QueryLifecycleError):
        next(cursor)

    with world.query(Position, Velocity).writes(Position, Velocity).rows() as rows:
        current_id, position, velocity = next(rows)
        assert current_id == entity_id
        position.x = 10
        velocity.y = 40

    assert world.get(entity_id, Position) == Position(10, 2)
    assert world.get(entity_id, Velocity) == Velocity(3, 40)
    assert world.epoch == before + 1
    assert world.component_epoch(entity_id, Position) == world.epoch
    assert world.component_epoch(entity_id, Velocity) == world.epoch

    unchanged_epoch = world.epoch
    with world.query(Position).writes(Position).rows() as rows:
        _, unchanged = next(rows)
        unchanged.x = unchanged.x
    assert world.epoch == unchanged_epoch


def test_writable_subset_discards_mutation_to_read_only_included_copy() -> None:
    world = World(REGISTRY)
    entity_id = world.spawn(Position(1, 2), Velocity(3, 4))

    with world.query(Position, Velocity).writes(Position).rows() as rows:
        _, position, velocity = next(rows)
        position.x = 10
        velocity.x = 30

    assert world.get(entity_id, Position) == Position(10, 2)
    assert world.get(entity_id, Velocity) == Velocity(3, 4)


def test_query_copy_and_writeback_bypass_author_getters_and_equality() -> None:
    world = World(REGISTRY)
    entity_id = world.spawn(HostileBehavior(1))

    with world.query(HostileBehavior).writes(HostileBehavior).rows() as rows:
        _, value = next(rows)
        object.__setattr__(value, "value", 2)

    returned = world.get(entity_id, HostileBehavior)
    assert object.__getattribute__(returned, "value") == 2


def test_committed_row_alias_is_inert_after_cursor_close() -> None:
    world = World(REGISTRY)
    entity_id = world.spawn(Position(1, 2))
    retained = Position()

    with world.query(Position).writes(Position).rows() as rows:
        _, retained = next(rows)
        retained.x = 10
    retained.x = 99

    assert world.get(entity_id, Position) == Position(10, 2)


def test_query_plan_cache_reuses_value_only_plans_and_rebuilds_after_structure() -> None:
    world = World(REGISTRY)
    entity_id = world.spawn(Position())
    query = world.query(Position)

    list(query.rows())
    plans = world._query_plans  # pyright: ignore[reportPrivateUsage]
    assert len(plans) == 1
    first_plan = next(iter(plans.values()))

    world.patch(entity_id, Position, x=1)
    list(query.rows())
    assert next(iter(plans.values())) is first_plan

    world.spawn(Position())
    list(query.rows())
    assert next(iter(plans.values())) is not first_plan


def test_plan_keys_preserve_include_order_and_canonicalize_exclusions() -> None:
    world = World(REGISTRY)
    world.spawn(Position(), Velocity())

    list(world.query(Position, Velocity).without(Hidden, FrozenName).rows())
    plans = world._query_plans  # pyright: ignore[reportPrivateUsage]
    assert len(plans) == 1
    list(world.query(Position, Velocity).without(FrozenName, Hidden).rows())
    assert len(plans) == 1
    list(world.query(Velocity, Position).without(Hidden, FrozenName).rows())
    assert len(plans) == 2


def test_query_plan_selects_smallest_table_with_uuid_tie_break() -> None:
    world = World(REGISTRY)
    world.spawn(Position(), Velocity())
    world.spawn(Position())
    list(world.query(Position, Velocity).rows())
    plan = next(
        iter(world._query_plans.values())  # pyright: ignore[reportPrivateUsage]
    )
    assert plan.driver is Velocity

    tied = World(REGISTRY)
    tied.spawn(Position(), Velocity())
    list(tied.query(Velocity, Position).rows())
    tied_plan = next(
        iter(tied._query_plans.values())  # pyright: ignore[reportPrivateUsage]
    )
    assert tied_plan.driver is Position


def test_builder_observes_later_state_and_clone_has_independent_query_guards() -> None:
    world = World(REGISTRY)
    builder = world.query(Position).stable()
    first = world.spawn(Position(1, 1))
    duplicate = world.clone()

    assert list(builder.rows()) == [(first, Position(1, 1))]

    cursor = world.query(Position).rows()
    iter(cursor)
    clone_entity = duplicate.spawn(Position(2, 2))
    assert duplicate.get(clone_entity, Position) == Position(2, 2)
    cursor.close()


def test_writable_row_validation_is_atomic_and_releases_the_guard() -> None:
    world = World(REGISTRY)
    entity_id = world.spawn(Position(1, 2), Velocity(3, 4))
    before = world.epoch

    with (
        pytest.raises(InvalidComponentValueError),
        world.query(Position, Velocity).writes(Position, Velocity).rows() as rows,
    ):
        _, position, velocity = next(rows)
        position.x = 10
        object.__setattr__(velocity, "x", "invalid")

    assert world.get(entity_id, Position) == Position(1, 2)
    assert world.get(entity_id, Velocity) == Velocity(3, 4)
    assert world.epoch == before
    world.spawn()


def test_query_exception_discards_current_row_but_keeps_prior_commits() -> None:
    world = World(REGISTRY)
    first = world.spawn(Position(1, 1))
    second = world.spawn(Position(2, 2))

    with (
        pytest.raises(RuntimeError, match="stop"),
        world.query(Position).writes(Position).stable().rows() as rows,
    ):
        _, first_position = next(rows)
        first_position.x = 10
        _, second_position = next(rows)
        second_position.x = 20
        raise RuntimeError("stop")

    assert world.get(first, Position) == Position(10, 1)
    assert world.get(second, Position) == Position(2, 2)
    world.spawn()


def test_active_cursor_rejects_all_structural_paths_and_overlap() -> None:
    world = World(REGISTRY)
    entity_id = world.spawn(Position())

    reader = world.query(Position).rows()
    iter(reader)
    during_query = world.commands()
    during_query.spawn(Position(9, 9))
    assert world.entities() == (entity_id,)
    operations = (
        lambda: world.spawn(),
        lambda: world.destroy(entity_id),
        lambda: world.add(entity_id, Velocity()),
        lambda: world.remove(entity_id, Position),
        lambda: world.replace(entity_id, Position(1, 1)),
        lambda: world.patch(entity_id, Position, x=1),
        world.clone,
        lambda: world.flush(during_query),
    )
    for operation in operations:
        with pytest.raises(ActiveQueryError):
            operation()

    with (
        pytest.raises(ActiveQueryError),
        world.query(Position).writes(Position).rows(),
    ):
        pass
    assert len(during_query) == 1
    reader.close()

    with world.query(Position).writes(Position).rows() as rows:
        next(rows)
        with pytest.raises(ActiveQueryError):
            iter(world.query(Position).rows())


def test_early_break_retains_guard_until_explicit_close() -> None:
    world = World(REGISTRY)
    world.spawn(Position())
    cursor = world.query(Position).rows()

    for _row in cursor:
        break
    with pytest.raises(ActiveQueryError):
        world.spawn()
    cursor.close()
    world.spawn()


def test_abort_discards_current_writable_row_and_releases_idempotently() -> None:
    world = World(REGISTRY)
    entity_id = world.spawn(Position(1, 2))
    cursor = world.query(Position).writes(Position).rows()
    cursor.__enter__()
    _, position = next(cursor)
    position.x = 99

    assert not cursor.closed
    cursor.abort()
    cursor.abort()

    assert cursor.closed
    assert world.get(entity_id, Position) == Position(1, 2)
    world.spawn()
