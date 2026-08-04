"""Backend-neutral generational render-resource handles."""

from dataclasses import dataclass
from typing import cast
from uuid import UUID

from ludoweave.core.errors import RenderError

_MAX_HANDLE_VALUE = 2**63 - 1


def _validate_handle(scope: object, index: object, generation: object) -> None:
    if not isinstance(scope, UUID) or scope.int == 0:
        raise RenderError(
            "render handle scope must be a nonzero UUID",
            code="render.invalid_handle",
            subsystem="render",
            phase="handle",
            details={"field": "scope", "actual_type": type(scope).__name__},
        )
    for field, value in (("index", index), ("generation", generation)):
        if type(value) is not int or value < 0 or value > _MAX_HANDLE_VALUE:
            raise RenderError(
                "render handle fields must be non-negative signed 64-bit integers",
                code="render.invalid_handle",
                subsystem="render",
                phase="handle",
                details={"field": field, "actual_type": type(value).__name__},
            )


@dataclass(frozen=True, slots=True, order=True)
class BufferHandle:
    """Opaque identity for an engine-owned GPU-style buffer."""

    scope: UUID
    index: int
    generation: int

    def __post_init__(self) -> None:
        _validate_handle(self.scope, self.index, self.generation)


@dataclass(frozen=True, slots=True, order=True)
class TextureHandle:
    """Opaque identity for an engine-owned texture."""

    scope: UUID
    index: int
    generation: int

    def __post_init__(self) -> None:
        _validate_handle(self.scope, self.index, self.generation)


@dataclass(frozen=True, slots=True, order=True)
class PipelineHandle:
    """Opaque identity for an engine-owned render pipeline."""

    scope: UUID
    index: int
    generation: int

    def __post_init__(self) -> None:
        _validate_handle(self.scope, self.index, self.generation)


@dataclass(frozen=True, slots=True, order=True)
class SurfaceHandle:
    """Opaque identity for an onscreen or offscreen render target."""

    scope: UUID
    index: int
    generation: int

    def __post_init__(self) -> None:
        _validate_handle(self.scope, self.index, self.generation)


@dataclass(frozen=True, slots=True, order=True)
class FenceHandle:
    """Opaque identity for one submitted unit of backend work."""

    scope: UUID
    submission: int

    def __post_init__(self) -> None:
        scope = cast(object, self.scope)
        if not isinstance(scope, UUID) or scope.int == 0:
            raise RenderError(
                "render fence scope must be a nonzero UUID",
                code="render.invalid_fence",
                subsystem="render",
                phase="fence",
                details={"field": "scope", "actual_type": type(self.scope).__name__},
            )
        if (
            type(self.submission) is not int
            or self.submission <= 0
            or self.submission > _MAX_HANDLE_VALUE
        ):
            raise RenderError(
                "render fence submission must be a positive signed 64-bit integer",
                code="render.invalid_fence",
                subsystem="render",
                phase="fence",
                details={"field": "submission", "actual_type": type(self.submission).__name__},
            )


type RenderResourceHandle = BufferHandle | TextureHandle | PipelineHandle | SurfaceHandle
