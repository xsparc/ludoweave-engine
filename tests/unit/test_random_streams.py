"""Engine-owned deterministic random stream behavior."""

from typing import cast

import pytest

from ludoweave.world import (
    AuthorityError,
    RandomStreams,
    RandomStreamsSnapshot,
    RandomStreamState,
)


def test_named_streams_are_repeatable_independent_and_checkpointable() -> None:
    left = RandomStreams(42)
    right = RandomStreams(42)

    left_a = [left.next_u32("waves") for _ in range(5)]
    left_b = [left.next_u32("loot") for _ in range(3)]
    right_a = [right.next_u32("waves") for _ in range(5)]
    right_b = [right.next_u32("loot") for _ in range(3)]

    assert left_a == right_a
    assert left_b == right_b
    assert left_a[:3] != left_b

    restored = RandomStreams.from_checkpoint(left.checkpoint())
    assert restored.next_u32("waves") == left.next_u32("waves")
    assert restored.next_u32("loot") == left.next_u32("loot")


def test_stream_order_does_not_change_each_named_sequence() -> None:
    first = RandomStreams(7)
    second = RandomStreams(7)
    expected_a = [first.next_u32("a") for _ in range(10)]
    expected_b = [first.next_u32("b") for _ in range(10)]

    actual_b = [second.next_u32("b") for _ in range(10)]
    actual_a = [second.next_u32("a") for _ in range(10)]

    assert actual_a == expected_a
    assert actual_b == expected_b


def test_randbelow_is_bounded_and_invalid_inputs_are_structured() -> None:
    streams = RandomStreams(1)
    assert all(0 <= streams.randbelow("dice", 6) < 6 for _ in range(100))

    for value in (0, -1, 2**32 + 1, True):
        with pytest.raises(AuthorityError):
            streams.randbelow("dice", value)
    with pytest.raises(AuthorityError):
        streams.next_u32("invalid stream")


def test_random_snapshot_freezes_and_validates_its_stream_collection() -> None:
    source = [RandomStreamState("waves", 1, 3)]
    snapshot = RandomStreamsSnapshot(
        7,
        cast(tuple[RandomStreamState, ...], source),
    )
    source.clear()
    assert len(snapshot.streams) == 1

    with pytest.raises(AuthorityError):
        RandomStreamsSnapshot(
            7,
            cast(tuple[RandomStreamState, ...], (object(),)),
        )
