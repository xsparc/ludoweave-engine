"""Local deferred structural command-buffer behavior and atomicity tests."""

from dataclasses import dataclass, replace
from uuid import UUID

import pytest

from ludoweave.core import LudoWeaveError
from ludoweave.ecs import (
    CommandBufferStateError,
    ComponentRegistry,
    DeferredCommandError,
    DeferredEntity,
    InvalidComponentValueError,
    InvalidDeferredEntityError,
    StaleEntityError,
    UnknownComponentError,
    World,
    component,
)


@component(type_id=UUID("f2000000-0000-0000-0000-000000000001"))
@dataclass(slots=True)
class Position:
    x: int = 0
    y: int = 0


@component(type_id=UUID("f2000000-0000-0000-0000-000000000002"))
@dataclass(slots=True)
class Velocity:
    x: int = 0
    y: int = 0


@component(type_id=UUID("f2000000-0000-0000-0000-000000000003"))
@dataclass(slots=True)
class HostileCommandValue:
    value: int = 0

    def __getattribute__(self, name: str) -> object:
        current = object.__getattribute__(self, name)
        if name == "value":
            object.__setattr__(self, name, "corrupted")
        return current


REGISTRY = ComponentRegistry((Velocity, Position, HostileCommandValue))


def test_buffer_is_invisible_until_flush_and_copies_enqueue_values() -> None:
    world = World(REGISTRY)
    commands = world.commands()
    source = Position(1, 2)
    token = commands.spawn(source)
    source.x = 99

    assert world.entities() == ()
    assert world.epoch == 0

    result = world.flush(commands)
    entity_id = result.resolve(token)
    assert result.command_count == 1
    assert result.start_epoch == 0
    assert result.end_epoch == 1
    assert result.resolutions == ((token, entity_id),)
    assert world.get(entity_id, Position) == Position(1, 2)
    assert len(commands) == 0


def test_enqueue_copy_bypasses_hostile_author_getters() -> None:
    world = World(REGISTRY)
    commands = world.commands()
    source = HostileCommandValue(7)
    token = commands.spawn(source)

    assert object.__getattribute__(source, "value") == 7
    result = world.flush(commands)
    stored = world.get(result.resolve(token), HostileCommandValue)
    assert object.__getattribute__(stored, "value") == 7


def test_spawn_token_chains_apply_in_enqueue_order() -> None:
    world = World(REGISTRY)
    commands = world.commands()
    token = commands.spawn(Position(1, 2))
    velocity = Velocity(3, 4)
    commands.add(token, velocity)
    velocity.y = 99
    commands.remove(token, Position)

    result = world.flush(commands)
    entity_id = result.resolve(token)
    assert not world.has(entity_id, Position)
    assert world.get(entity_id, Velocity) == Velocity(3, 4)
    assert result.command_count == 3
    assert result.end_epoch == 3


def test_multiple_spawn_tokens_allocate_and_resolve_in_enqueue_order() -> None:
    world = World(REGISTRY)
    commands = world.commands()
    first = commands.spawn(Position(1, 1))
    second = commands.spawn(Position(2, 2))

    result = world.flush(commands)

    assert result.resolutions == (
        (first, result.resolve(first)),
        (second, result.resolve(second)),
    )
    assert result.resolve(first).index == 0
    assert result.resolve(second).index == 1


def test_successful_flush_matches_direct_mutation_epochs_and_state() -> None:
    direct = World(REGISTRY)
    expected_id = direct.spawn(Position(1, 2))
    direct.add(expected_id, Velocity(3, 4))
    direct.remove(expected_id, Position)

    deferred = World(REGISTRY)
    commands = deferred.commands()
    token = commands.spawn(Position(1, 2))
    commands.add(token, Velocity(3, 4))
    commands.remove(token, Position)
    result = deferred.flush(commands)

    assert result.resolve(token) == expected_id
    assert deferred.entities() == direct.entities()
    assert deferred.components(Position) == direct.components(Position)
    assert deferred.components(Velocity) == direct.components(Velocity)
    assert deferred.epoch == direct.epoch
    assert deferred.structural_epoch == direct.structural_epoch


def test_failed_flush_rolls_back_state_allocator_and_retains_queue_for_retry() -> None:
    world = World(REGISTRY)
    retained = world.spawn(Position(1, 1))
    commands = world.commands()
    token = commands.spawn(Position(2, 2))
    commands.add(token, Position(3, 3))
    before = _fingerprint(world)
    list(world.query(Position).rows())
    cached_plan = next(
        iter(world._query_plans.values())  # pyright: ignore[reportPrivateUsage]
    )

    with pytest.raises(DeferredCommandError) as first_failure:
        world.flush(commands)
    assert _fingerprint(world) == before
    assert len(commands) == 2
    list(world.query(Position).rows())
    assert (
        next(iter(world._query_plans.values()))  # pyright: ignore[reportPrivateUsage]
        is cached_plan
    )
    assert isinstance(first_failure.value.__cause__, LudoWeaveError)
    assert dict(first_failure.value.details) == {
        "cause_code": "ecs.component_already_present",
        "operation_index": 1,
        "operation_kind": "add",
    }

    with pytest.raises(DeferredCommandError) as retry_failure:
        world.flush(commands)
    assert retry_failure.value.as_dict() == first_failure.value.as_dict()
    assert _fingerprint(world) == before
    assert len(commands) == 2

    commands.clear()
    with pytest.raises(InvalidDeferredEntityError):
        commands.destroy(token)
    replacement = world.spawn()
    assert replacement.index == retained.index + 1


def test_clear_reuses_buffer_and_invalidates_old_tokens() -> None:
    world = World(REGISTRY)
    commands = world.commands()
    discarded = commands.spawn(Position(1, 1))
    commands.clear()

    assert len(commands) == 0
    with pytest.raises(InvalidDeferredEntityError):
        commands.add(discarded, Velocity())

    current = commands.spawn(Position(2, 2))
    result = world.flush(commands)
    assert world.get(result.resolve(current), Position) == Position(2, 2)
    assert len(commands) == 0
    with pytest.raises(InvalidDeferredEntityError):
        commands.destroy(current)

    next_token = commands.spawn(Position(3, 3))
    next_result = world.flush(commands)
    assert world.get(next_result.resolve(next_token), Position) == Position(3, 3)

    empty = world.flush(commands)
    assert empty.command_count == 0
    assert empty.start_epoch == empty.end_epoch == world.epoch


def test_foreign_forged_and_cross_buffer_tokens_are_rejected_at_enqueue() -> None:
    first_world = World(REGISTRY)
    second_world = World(REGISTRY)
    first_buffer = first_world.commands()
    sibling_buffer = first_world.commands()
    foreign_buffer = second_world.commands()
    first_token = first_buffer.spawn()
    foreign_token = foreign_buffer.spawn()
    forged = DeferredEntity(object(), 0, first_token.ordinal)
    copied = replace(first_token)

    for token in (first_token, foreign_token, forged, copied):
        with pytest.raises(InvalidDeferredEntityError):
            sibling_buffer.destroy(token)
    with pytest.raises(InvalidDeferredEntityError):
        first_buffer.destroy(copied)
    with pytest.raises(CommandBufferStateError):
        second_world.flush(first_buffer)


def test_spawn_then_destroy_returns_a_resolved_stale_handle() -> None:
    world = World(REGISTRY)
    commands = world.commands()
    token = commands.spawn(Position())
    commands.destroy(token)

    result = world.flush(commands)
    stale = result.resolve(token)
    with pytest.raises(StaleEntityError):
        world.get(stale, Position)


def test_stale_existing_target_in_middle_rolls_back_prior_spawn_and_allocator() -> None:
    world = World(REGISTRY)
    stale = world.spawn(Position(1, 1))
    world.destroy(stale)
    commands = world.commands()
    commands.spawn(Position(2, 2))
    commands.destroy(stale)
    before = _fingerprint(world)

    with pytest.raises(DeferredCommandError) as failure:
        world.flush(commands)

    assert dict(failure.value.details)["operation_index"] == 1
    assert _fingerprint(world) == before
    assert len(commands) == 2
    commands.clear()
    replacement = world.spawn()
    assert replacement.index == stale.index
    assert replacement.generation == stale.generation + 1


def test_original_and_clone_reject_each_others_command_buffers() -> None:
    world = World(REGISTRY)
    duplicate = world.clone()
    commands = world.commands()
    token = commands.spawn(Position(1, 2))

    with pytest.raises(CommandBufferStateError):
        duplicate.flush(commands)
    result = world.flush(commands)
    assert world.get(result.resolve(token), Position) == Position(1, 2)
    assert duplicate.entities() == ()


def test_enqueue_validation_is_atomic_and_resolution_rejects_unknown_token() -> None:
    world = World(REGISTRY)
    commands = world.commands()
    malformed = Position(1, 2)
    object.__setattr__(malformed, "x", "invalid")

    with pytest.raises(InvalidComponentValueError):
        commands.spawn(malformed)
    assert len(commands) == 0

    valid = commands.spawn(Position())
    result = world.flush(commands)
    assert result.resolve(valid) in world.entities()
    other = world.commands().spawn()
    with pytest.raises(InvalidDeferredEntityError):
        result.resolve(other)


def test_invalid_enqueue_operations_never_append_partial_records() -> None:
    world = World(REGISTRY)
    entity_id = world.spawn()
    commands = world.commands()

    with pytest.raises(CommandBufferStateError):
        commands.spawn(Position(), Position())
    assert len(commands) == 0

    with pytest.raises(UnknownComponentError):
        commands.remove(entity_id, str)
    assert len(commands) == 0

    with pytest.raises(InvalidDeferredEntityError):
        commands.destroy(object())  # type: ignore[arg-type]
    assert len(commands) == 0


def _fingerprint(world: World) -> tuple[object, ...]:
    return (
        world.entities(),
        world.components(Position),
        world.components(Velocity),
        world.epoch,
        world.structural_epoch,
        world.component_structural_epoch(Position),
        world.component_structural_epoch(Velocity),
    )
