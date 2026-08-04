"""Engine-owned deterministic PCG32 random streams with snapshot state."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from hashlib import sha256
from typing import cast

from ludoweave.world.errors import AuthorityError

RANDOM_ALGORITHM = "pcg32/1"
_MASK_64 = (1 << 64) - 1
_STREAM_NAME = re.compile(r"[A-Za-z][A-Za-z0-9_.:-]{0,127}\Z")


@dataclass(frozen=True, slots=True)
class RandomStreamState:
    name: str
    state: int
    increment: int

    def __post_init__(self) -> None:
        _validate_name(self.name)
        _validate_u64(self.state, field="state")
        _validate_u64(self.increment, field="increment")
        if self.increment & 1 == 0:
            raise _random_error(
                "random stream increment must be odd",
                details={"stream": self.name, "field": "increment"},
            )


@dataclass(frozen=True, slots=True)
class RandomStreamsSnapshot:
    seed: int
    streams: tuple[RandomStreamState, ...]
    algorithm: str = RANDOM_ALGORITHM

    def __post_init__(self) -> None:
        _validate_u64(self.seed, field="seed")
        if self.algorithm != RANDOM_ALGORITHM:
            raise _random_error(
                "random stream snapshot algorithm is incompatible",
                details={"algorithm": self.algorithm},
            )
        candidate_streams = cast(object, self.streams)
        try:
            streams = tuple(cast(Iterable[object], candidate_streams))
        except Exception as error:
            raise _random_error(
                "random stream snapshots require an iterable of stream states",
                details={"field": "streams", "actual_type": type(self.streams).__name__},
            ) from error
        if any(not isinstance(item, RandomStreamState) for item in streams):
            raise _random_error(
                "random stream snapshots require stream-state records",
                details={"field": "streams"},
            )
        checked_streams = cast(tuple[RandomStreamState, ...], streams)
        object.__setattr__(self, "streams", checked_streams)
        names = tuple(item.name for item in checked_streams)
        if names != tuple(sorted(names)) or len(names) != len(set(names)):
            raise _random_error(
                "random stream snapshots must have unique canonical names",
                details={"field": "streams"},
            )


class RandomStreams:
    """Named deterministic streams derived from one explicit unsigned seed."""

    __slots__ = ("_seed", "_states")

    def __init__(self, seed: int) -> None:
        _validate_u64(seed, field="seed")
        self._seed = seed
        self._states: dict[str, tuple[int, int]] = {}

    @property
    def seed(self) -> int:
        return self._seed

    def next_u32(self, stream: str) -> int:
        """Return the next unsigned 32-bit value for one named stream."""

        name = _validate_name(stream)
        state, increment = self._states.get(name, self._initial_state(name))
        old_state = state
        state = (old_state * 6364136223846793005 + increment) & _MASK_64
        self._states[name] = (state, increment)
        xorshifted = (((old_state >> 18) ^ old_state) >> 27) & 0xFFFFFFFF
        rotation = old_state >> 59
        return ((xorshifted >> rotation) | (xorshifted << ((-rotation) & 31))) & 0xFFFFFFFF

    def randbelow(self, stream: str, upper_bound: int) -> int:
        """Return an unbiased value in ``range(upper_bound)``."""

        if type(upper_bound) is not int or upper_bound <= 0 or upper_bound > 2**32:
            raise _random_error(
                "random upper bound must be in the unsigned 32-bit domain",
                details={"field": "upper_bound", "actual_type": type(upper_bound).__name__},
            )
        threshold = (2**32 - upper_bound) % upper_bound
        while True:
            value = self.next_u32(stream)
            if value >= threshold:
                return value % upper_bound

    def checkpoint(self) -> RandomStreamsSnapshot:
        return RandomStreamsSnapshot(
            seed=self._seed,
            streams=tuple(
                RandomStreamState(name, state, increment)
                for name, (state, increment) in sorted(self._states.items())
            ),
        )

    def clone(self) -> RandomStreams:
        duplicate = RandomStreams(self._seed)
        duplicate._states = dict(self._states)
        return duplicate

    @classmethod
    def from_checkpoint(cls, checkpoint: RandomStreamsSnapshot) -> RandomStreams:
        duplicate = cls(checkpoint.seed)
        duplicate._states = {item.name: (item.state, item.increment) for item in checkpoint.streams}
        return duplicate

    def _initial_state(self, name: str) -> tuple[int, int]:
        seed_bytes = self._seed.to_bytes(8, "big")
        digest = sha256(seed_bytes + b"\0" + name.encode("utf-8")).digest()
        state = int.from_bytes(digest[:8], "big")
        increment = int.from_bytes(digest[8:16], "big") | 1
        return state, increment


def _validate_name(value: object) -> str:
    if type(value) is not str or _STREAM_NAME.fullmatch(value) is None:
        raise _random_error(
            "random stream name must use bounded stable text",
            details={"field": "stream", "actual_type": type(value).__name__},
        )
    return value


def _validate_u64(value: object, *, field: str) -> int:
    if type(value) is not int or value < 0 or value > _MASK_64:
        raise _random_error(
            "random state must be an unsigned 64-bit integer",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _random_error(
    message: str,
    *,
    details: dict[str, str | int | float | bool | None],
) -> AuthorityError:
    return AuthorityError(
        message,
        code="world.invalid_random_state",
        subsystem="world",
        phase="random",
        details=details,
    )
