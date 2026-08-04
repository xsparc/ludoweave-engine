"""Generational entity identifiers and deterministic slot allocation."""

from __future__ import annotations

from dataclasses import dataclass

from ludoweave.ecs.errors import InvalidEntityIdError, StaleEntityError


@dataclass(frozen=True, slots=True)
class AllocatorCheckpoint:
    """Complete deterministic allocator state for engine-owned checkpoints."""

    generations: tuple[int, ...]
    alive: tuple[bool, ...]
    free: tuple[int, ...]

    def __post_init__(self) -> None:
        if len(self.generations) != len(self.alive):
            raise InvalidEntityIdError(
                "allocator checkpoint arrays must have equal lengths",
                code="ecs.invalid_allocator_checkpoint",
                subsystem="ecs",
                phase="checkpoint",
                details={"reason": "length_mismatch"},
            )
        if any(type(is_alive) is not bool for is_alive in self.alive):
            raise InvalidEntityIdError(
                "allocator checkpoint alive flags must be booleans",
                code="ecs.invalid_allocator_checkpoint",
                subsystem="ecs",
                phase="checkpoint",
                details={"reason": "invalid_alive_flag"},
            )
        for index, generation in enumerate(self.generations):
            _validate_id_field("generation", generation)
            if not self.alive[index] and generation == 0:
                raise InvalidEntityIdError(
                    "retired allocator slots must have an advanced generation",
                    code="ecs.invalid_allocator_checkpoint",
                    subsystem="ecs",
                    phase="checkpoint",
                    details={"reason": "retired_generation_not_advanced", "index": index},
                )
        expected_free = {index for index, is_alive in enumerate(self.alive) if not is_alive}
        if (
            any(type(index) is not int for index in self.free)
            or len(set(self.free)) != len(self.free)
            or set(self.free) != expected_free
        ):
            raise InvalidEntityIdError(
                "allocator checkpoint free list must exactly name retired slots",
                code="ecs.invalid_allocator_checkpoint",
                subsystem="ecs",
                phase="checkpoint",
                details={"reason": "invalid_free_list"},
            )


@dataclass(frozen=True, slots=True)
class EntityId:
    """Stable two-field identity for one allocation generation.

    ``index`` is an allocator-owned slot and is never accepted on its own by a
    public allocator operation. ``generation`` changes before a destroyed slot
    can be reused, keeping every earlier handle stale.
    """

    index: int
    generation: int

    def __post_init__(self) -> None:
        _validate_id_field("index", self.index)
        _validate_id_field("generation", self.generation)

    def as_tuple(self) -> tuple[int, int]:
        """Return the canonical serialization-friendly field pair."""

        return (self.index, self.generation)


class EntityAllocator:
    """Allocate and retire generational IDs in deterministic operation order.

    Freed slots are reused last-in, first-out. Generations are unbounded Python
    integers, so allocator churn cannot wrap an old handle back into validity.
    The allocator is intended for single-owner simulation use and is not
    concurrently safe.
    """

    __slots__ = ("_alive", "_free", "_generations")

    def __init__(self) -> None:
        self._generations: list[int] = []
        self._alive: list[bool] = []
        self._free: list[int] = []

    @property
    def alive_count(self) -> int:
        """Return the number of IDs that currently identify live entities."""

        return len(self._generations) - len(self._free)

    @property
    def capacity(self) -> int:
        """Return the number of slots created by this allocator."""

        return len(self._generations)

    def create(self) -> EntityId:
        """Create one live entity ID, reusing a retired slot when available."""

        if self._free:
            index = self._free.pop()
            self._alive[index] = True
        else:
            index = len(self._generations)
            self._generations.append(0)
            self._alive.append(True)
        return EntityId(index=index, generation=self._generations[index])

    def destroy(self, entity_id: EntityId) -> None:
        """Retire a live ID and advance its generation before future reuse."""

        index = self._require_alive(entity_id, operation="destroy")
        self._alive[index] = False
        self._generations[index] += 1
        self._free.append(index)

    def is_alive(self, entity_id: EntityId) -> bool:
        """Return whether ``entity_id`` names a live allocation generation."""

        checked = _require_entity_id(entity_id, operation="is_alive")
        return (
            checked.index < len(self._generations)
            and self._alive[checked.index]
            and self._generations[checked.index] == checked.generation
        )

    def validate(self, entity_id: EntityId, *, operation: str = "validate") -> None:
        """Raise :class:`StaleEntityError` unless ``entity_id`` is live."""

        self._require_alive(entity_id, operation=operation)

    def clone(self) -> EntityAllocator:
        """Return an independent allocator with identical future allocation order."""

        duplicate = EntityAllocator()
        duplicate._generations = list(self._generations)
        duplicate._alive = list(self._alive)
        duplicate._free = list(self._free)
        return duplicate

    def checkpoint(self) -> AllocatorCheckpoint:
        """Capture complete future-allocation state without exposing mutable arrays."""

        return AllocatorCheckpoint(
            generations=tuple(self._generations),
            alive=tuple(self._alive),
            free=tuple(self._free),
        )

    @classmethod
    def from_checkpoint(cls, checkpoint: AllocatorCheckpoint) -> EntityAllocator:
        """Construct an allocator after checkpoint invariants have been validated."""

        restored = cls()
        restored._generations = list(checkpoint.generations)
        restored._alive = list(checkpoint.alive)
        restored._free = list(checkpoint.free)
        return restored

    def _require_alive(self, entity_id: EntityId, *, operation: str) -> int:
        checked = _require_entity_id(entity_id, operation=operation)
        if checked.index >= len(self._generations):
            raise _stale_entity_error(
                checked,
                operation=operation,
                reason="unknown_index",
                current_generation=None,
            )

        current_generation = self._generations[checked.index]
        if not self._alive[checked.index]:
            raise _stale_entity_error(
                checked,
                operation=operation,
                reason="not_alive",
                current_generation=current_generation,
            )
        if current_generation != checked.generation:
            raise _stale_entity_error(
                checked,
                operation=operation,
                reason="generation_mismatch",
                current_generation=current_generation,
            )
        return checked.index


def _validate_id_field(field: str, value: object) -> None:
    if type(value) is not int:
        raise InvalidEntityIdError(
            "entity ID fields must be integers",
            code="ecs.invalid_entity_id",
            subsystem="ecs",
            phase="construct",
            details={"field": field, "actual_type": type(value).__name__},
        )
    if value < 0:
        raise InvalidEntityIdError(
            "entity ID fields must be non-negative",
            code="ecs.invalid_entity_id",
            subsystem="ecs",
            phase="construct",
            details={"field": field, "value": value},
        )


def _require_entity_id(entity_id: object, *, operation: str) -> EntityId:
    if isinstance(entity_id, EntityId):
        return entity_id
    raise InvalidEntityIdError(
        "public entity operations require an EntityId",
        code="ecs.invalid_entity_id",
        subsystem="ecs",
        phase=operation,
        details={"actual_type": type(entity_id).__name__},
    )


def _stale_entity_error(
    entity_id: EntityId,
    *,
    operation: str,
    reason: str,
    current_generation: int | None,
) -> StaleEntityError:
    return StaleEntityError(
        "entity ID does not identify a live entity",
        code="ecs.stale_entity",
        subsystem="ecs",
        phase=operation,
        details={
            "index": entity_id.index,
            "generation": entity_id.generation,
            "current_generation": current_generation,
            "reason": reason,
        },
    )
