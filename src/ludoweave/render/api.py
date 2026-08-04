"""Backend-neutral render descriptors and protocol."""

from dataclasses import dataclass
from typing import Protocol

from ludoweave.core.errors import RenderError


@dataclass(frozen=True, slots=True)
class RenderDescriptor:
    """Minimal backend-neutral render target description for M0."""

    width: int = 1
    height: int = 1
    label: str = "headless"

    def __post_init__(self) -> None:
        dimensions = (
            ("width", self.width),
            ("height", self.height),
        )
        for field, value in dimensions:
            if type(value) is not int or value <= 0:
                raise RenderError(
                    f"{field} must be a positive integer",
                    code="render.invalid_descriptor",
                    subsystem="render",
                    phase="descriptor",
                    details={"field": field, "value": repr(value)},
                )
        label = self.label
        if type(label) is not str or not label.strip():
            raise RenderError(
                "label must contain non-whitespace text",
                code="render.invalid_descriptor",
                subsystem="render",
                phase="descriptor",
                details={"field": "label"},
            )


class RenderBackend(Protocol):
    """Engine-owned lifecycle boundary implemented by render adapters.

    After injection the engine owns the backend and is responsible for closing
    it. Implementations are used by one engine thread in M0.
    """

    @property
    def name(self) -> str:
        """Stable diagnostic backend name."""

        ...

    def initialize(self, descriptor: RenderDescriptor) -> None:
        """Initialize resources for the supplied engine descriptor."""

        ...

    def render(self, *, tick: int) -> None:
        """Validate or present one frame for a completed tick."""

        ...

    def close(self) -> None:
        """Release owned resources; repeated calls must be safe."""

        ...
