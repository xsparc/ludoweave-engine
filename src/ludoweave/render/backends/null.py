"""Validation-only render backend with no graphics dependencies."""

from enum import Enum

from ludoweave.core.errors import RenderError
from ludoweave.render.api import RenderDescriptor


class _NullState(Enum):
    CREATED = "created"
    READY = "ready"
    CLOSED = "closed"


class NullRenderBackend:
    """Headless backend that validates descriptors and lifecycle ordering."""

    __slots__ = ("_descriptor", "_frame_count", "_state")

    def __init__(self) -> None:
        self._state = _NullState.CREATED
        self._descriptor: RenderDescriptor | None = None
        self._frame_count = 0

    @property
    def name(self) -> str:
        return "null"

    @property
    def descriptor(self) -> RenderDescriptor | None:
        """Descriptor accepted during initialization, if any."""

        return self._descriptor

    @property
    def frame_count(self) -> int:
        """Number of frames validated since initialization."""

        return self._frame_count

    @property
    def is_closed(self) -> bool:
        return self._state is _NullState.CLOSED

    def initialize(self, descriptor: RenderDescriptor) -> None:
        if self._state is not _NullState.CREATED:
            self._raise_ordering_error("initialize")
        self._descriptor = descriptor
        self._state = _NullState.READY

    def render(self, *, tick: int) -> None:
        if self._state is not _NullState.READY:
            self._raise_ordering_error("render")
        tick_value = tick
        if type(tick_value) is not int or tick_value < 0:
            raise RenderError(
                "tick must be a non-negative integer",
                code="render.invalid_tick",
                subsystem="render",
                phase="frame",
                details={"tick": repr(tick_value)},
            )
        self._frame_count += 1

    def close(self) -> None:
        if self._state is _NullState.CLOSED:
            return
        self._state = _NullState.CLOSED

    def _raise_ordering_error(self, operation: str) -> None:
        raise RenderError(
            f"cannot {operation} null renderer from {self._state.value} state",
            code="render.invalid_lifecycle",
            subsystem="render",
            phase=operation,
            details={"operation": operation, "state": self._state.value},
        )
