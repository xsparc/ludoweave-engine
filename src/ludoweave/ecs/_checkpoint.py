"""Private storage-neutral checkpoints for engine-owned transaction services.

These records contain detached Python component values. They are an internal
bridge, not the persistent M2 snapshot wire format or a public ``WorldStore``
obligation.
"""

from dataclasses import dataclass

from ludoweave.ecs.entity import AllocatorCheckpoint, EntityId


@dataclass(frozen=True, slots=True)
class ComponentRowCheckpoint:
    entity_id: EntityId
    value: object
    changed_epoch: int


@dataclass(frozen=True, slots=True)
class ComponentTableCheckpoint:
    component_type: type[object]
    structural_epoch: int
    rows: tuple[ComponentRowCheckpoint, ...]


@dataclass(frozen=True, slots=True)
class EcsCheckpoint:
    allocator: AllocatorCheckpoint
    epoch: int
    structural_epoch: int
    tables: tuple[ComponentTableCheckpoint, ...]
