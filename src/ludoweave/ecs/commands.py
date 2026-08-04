# pyright: reportPrivateUsage=false
"""World-bound local buffers for deferred structural ECS mutations.

Protected protocol hooks are intentionally called by their command-buffer
collaborator without becoming part of the public ``World`` API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from ludoweave.ecs.entity import EntityId
from ludoweave.ecs.errors import (
    CommandBufferStateError,
    InvalidDeferredEntityError,
)


class CommandBackend(Protocol):
    """Internal copy/validation hooks supplied independently by each world."""

    @property
    def _command_owner_token(self) -> object: ...

    def _copy_command_component(self, component: object, *, operation: str) -> object: ...

    def _validate_command_component_type(self, component_type: type[object]) -> None: ...


@dataclass(frozen=True, slots=True, eq=False)
class DeferredEntity:
    """Opaque reference to one spawn earlier in the same buffer generation."""

    _owner_token: object = field(repr=False)
    _generation: int = field(repr=False)
    ordinal: int

    def _is_valid_for(self, owner_token: object, generation: int) -> bool:
        """Return whether this opaque token belongs to one buffer generation."""

        return self._owner_token is owner_token and self._generation == generation


type EntityTarget = EntityId | DeferredEntity


@dataclass(frozen=True, slots=True)
class SpawnCommand:
    token: DeferredEntity
    components: tuple[object, ...]


@dataclass(frozen=True, slots=True)
class DestroyCommand:
    target: EntityTarget


@dataclass(frozen=True, slots=True)
class AddCommand:
    target: EntityTarget
    component: object


@dataclass(frozen=True, slots=True)
class RemoveCommand:
    target: EntityTarget
    component_type: type[object]


type DeferredCommand = SpawnCommand | DestroyCommand | AddCommand | RemoveCommand


@dataclass(frozen=True, slots=True)
class FlushResult:
    """Local flush outcome; deliberately not an M2 command receipt."""

    command_count: int
    start_epoch: int
    end_epoch: int
    resolutions: tuple[tuple[DeferredEntity, EntityId], ...]

    def resolve(self, token: object) -> EntityId:
        """Resolve a spawn token recorded by this successful flush."""

        if not isinstance(token, DeferredEntity):
            raise _invalid_deferred_error(
                "flush resolution requires a DeferredEntity",
                phase="resolve",
                details={"actual_type": type(token).__name__},
            )
        for recorded, entity_id in self.resolutions:
            if recorded == token:
                return entity_id
        raise _invalid_deferred_error(
            "deferred entity was not created by this flush",
            phase="resolve",
            details={"ordinal": token.ordinal},
        )


class Commands:
    """Reusable world-bound queue of copied local structural commands."""

    __slots__ = (
        "_backend",
        "_buffer_token",
        "_generation",
        "_records",
        "_tokens",
        "_world_token",
    )

    def __init__(self, backend: CommandBackend) -> None:
        self._backend = backend
        self._buffer_token = object()
        self._world_token = backend._command_owner_token
        self._generation = 0
        self._records: list[DeferredCommand] = []
        self._tokens: set[DeferredEntity] = set()

    def __len__(self) -> int:
        return len(self._records)

    def spawn(self, *components: object) -> DeferredEntity:
        """Queue a spawn and return an opaque same-generation target token."""

        copied: list[object] = []
        seen: set[type[object]] = set()
        for component in components:
            component_type = type(component)
            if component_type in seen:
                raise CommandBufferStateError(
                    "deferred spawn repeats a component type",
                    code="ecs.invalid_command_buffer",
                    subsystem="ecs",
                    phase="enqueue_spawn",
                    details={"component_type": component_type.__name__},
                )
            seen.add(component_type)
            copied.append(
                self._backend._copy_command_component(component, operation="enqueue_spawn")
            )
        token = DeferredEntity(
            self._buffer_token,
            self._generation,
            sum(isinstance(record, SpawnCommand) for record in self._records),
        )
        self._records.append(SpawnCommand(token, tuple(copied)))
        self._tokens.add(token)
        return token

    def destroy(self, target: EntityTarget) -> None:
        """Queue destruction of an existing or earlier deferred entity."""

        self._records.append(DestroyCommand(self._validate_target(target, phase="enqueue_destroy")))

    def add(self, target: EntityTarget, component: object) -> None:
        """Queue addition of one copied component value."""

        checked_target = self._validate_target(target, phase="enqueue_add")
        copied = self._backend._copy_command_component(component, operation="enqueue_add")
        self._records.append(AddCommand(checked_target, copied))

    def remove(self, target: EntityTarget, component_type: type[object]) -> None:
        """Queue removal of one registered component type."""

        checked_target = self._validate_target(target, phase="enqueue_remove")
        self._backend._validate_command_component_type(component_type)
        self._records.append(RemoveCommand(checked_target, component_type))

    def clear(self) -> None:
        """Discard queued operations and invalidate their deferred tokens."""

        self._records.clear()
        self._tokens.clear()
        self._generation += 1

    def _records_for(self, owner_token: object) -> tuple[DeferredCommand, ...]:
        """Return an immutable internal flush view after checking ownership."""

        if owner_token is not self._world_token:
            raise CommandBufferStateError(
                "command buffer is bound to a different world",
                code="ecs.command_buffer_wrong_world",
                subsystem="ecs",
                phase="flush",
            )
        return tuple(self._records)

    def _complete_flush(self) -> None:
        """Clear a successfully flushed generation and prepare the next one."""

        self.clear()

    def _validate_target(self, target: object, *, phase: str) -> EntityTarget:
        if isinstance(target, EntityId):
            return target
        if not isinstance(target, DeferredEntity):
            raise _invalid_deferred_error(
                "deferred command target must be EntityId or DeferredEntity",
                phase=phase,
                details={"actual_type": type(target).__name__},
            )
        if (
            not target._is_valid_for(self._buffer_token, self._generation)
            or target not in self._tokens
        ):
            raise _invalid_deferred_error(
                "deferred entity is forged, stale, or belongs to another buffer",
                phase=phase,
                details={"ordinal": target.ordinal},
            )
        return target


def _invalid_deferred_error(
    message: str,
    *,
    phase: str,
    details: dict[str, str | int | float | bool | None],
) -> InvalidDeferredEntityError:
    return InvalidDeferredEntityError(
        message,
        code="ecs.invalid_deferred_entity",
        subsystem="ecs",
        phase=phase,
        details=details,
    )
