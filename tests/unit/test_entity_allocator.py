"""Generational entity allocator tests."""

from typing import cast

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.ecs import EntityAllocator, EntityId, InvalidEntityIdError, StaleEntityError
from ludoweave.ecs.entity import AllocatorCheckpoint


def test_allocator_creates_distinct_live_ids() -> None:
    allocator = EntityAllocator()

    first = allocator.create()
    second = allocator.create()

    assert first == EntityId(index=0, generation=0)
    assert second == EntityId(index=1, generation=0)
    assert allocator.is_alive(first)
    assert allocator.is_alive(second)
    assert allocator.alive_count == 2
    assert allocator.capacity == 2


def test_destroy_advances_generation_before_lifo_reuse() -> None:
    allocator = EntityAllocator()
    first = allocator.create()
    second = allocator.create()

    allocator.destroy(first)
    allocator.destroy(second)
    replacement = allocator.create()

    assert replacement == EntityId(index=second.index, generation=second.generation + 1)
    assert not allocator.is_alive(second)
    assert allocator.alive_count == 1
    assert allocator.capacity == 2


def test_destroying_twice_fails_without_corrupting_allocator() -> None:
    allocator = EntityAllocator()
    stale = allocator.create()
    allocator.destroy(stale)

    with pytest.raises(StaleEntityError):
        allocator.destroy(stale)

    assert allocator.alive_count == 0
    assert allocator.create() == EntityId(index=stale.index, generation=stale.generation + 1)


def test_stale_access_has_structured_context() -> None:
    allocator = EntityAllocator()
    stale = allocator.create()
    allocator.destroy(stale)

    with pytest.raises(StaleEntityError) as caught:
        allocator.validate(stale)

    assert caught.value.as_dict() == {
        "code": "ecs.stale_entity",
        "subsystem": "ecs",
        "phase": "validate",
        "message": "entity ID does not identify a live entity",
        "details": {
            "current_generation": 1,
            "generation": 0,
            "index": 0,
            "reason": "not_alive",
        },
    }


def test_unknown_and_forged_generations_are_stale() -> None:
    allocator = EntityAllocator()
    live = allocator.create()

    with pytest.raises(StaleEntityError, match=r"ecs\.stale_entity"):
        allocator.validate(EntityId(index=99, generation=0))
    with pytest.raises(StaleEntityError, match=r"ecs\.stale_entity"):
        allocator.validate(EntityId(index=live.index, generation=live.generation + 1))


@pytest.mark.parametrize(
    ("index", "generation"),
    [(-1, 0), (0, -1), (True, 0), (0, False), ("0", 0), (0, "0")],
)
def test_entity_id_rejects_invalid_fields(index: object, generation: object) -> None:
    with pytest.raises(InvalidEntityIdError, match=r"ecs\.invalid_entity_id"):
        EntityId(index=cast(int, index), generation=cast(int, generation))


def test_public_operations_reject_raw_indexes() -> None:
    allocator = EntityAllocator()
    allocator.create()

    with pytest.raises(InvalidEntityIdError, match="require an EntityId"):
        allocator.is_alive(cast(EntityId, 0))


def test_checkpoint_rejects_retired_generation_zero_that_could_revive_a_handle() -> None:
    with pytest.raises(InvalidEntityIdError) as raised:
        AllocatorCheckpoint(generations=(0,), alive=(False,), free=(0,))

    assert raised.value.code == "ecs.invalid_allocator_checkpoint"
    assert raised.value.details == (
        ("index", 0),
        ("reason", "retired_generation_not_advanced"),
    )


@pytest.mark.parametrize("flag", [0, 1, "", "alive", None])
def test_checkpoint_rejects_non_boolean_alive_flags(flag: object) -> None:
    with pytest.raises(InvalidEntityIdError) as raised:
        AllocatorCheckpoint(generations=(0,), alive=cast(tuple[bool, ...], (flag,)), free=())

    assert raised.value.code == "ecs.invalid_allocator_checkpoint"
    assert raised.value.details == (("reason", "invalid_alive_flag"),)


@given(cycles=st.integers(min_value=1, max_value=500))
def test_destroyed_handles_never_revive(cycles: int) -> None:
    allocator = EntityAllocator()
    stale_handles: list[EntityId] = []

    current = allocator.create()
    for _ in range(cycles):
        allocator.destroy(current)
        stale_handles.append(current)
        current = allocator.create()

        assert all(not allocator.is_alive(stale) for stale in stale_handles)
        assert current.index == 0
        assert current.generation == len(stale_handles)


@given(
    actions=st.lists(st.tuples(st.booleans(), st.integers(min_value=0)), min_size=1, max_size=200)
)
def test_stale_handles_remain_invalid_across_random_allocator_churn(
    actions: list[tuple[bool, int]],
) -> None:
    allocator = EntityAllocator()
    live: list[EntityId] = []
    stale: list[EntityId] = []

    for should_create, selector in actions:
        if should_create or not live:
            live.append(allocator.create())
        else:
            retired = live.pop(selector % len(live))
            allocator.destroy(retired)
            stale.append(retired)

        assert all(allocator.is_alive(entity_id) for entity_id in live)
        assert all(not allocator.is_alive(entity_id) for entity_id in stale)
        assert allocator.alive_count == len(live)


@given(index=st.integers(min_value=0), generation=st.integers(min_value=0))
def test_entity_id_has_stable_two_field_representation(index: int, generation: int) -> None:
    entity_id = EntityId(index=index, generation=generation)

    assert entity_id.as_tuple() == (index, generation)
