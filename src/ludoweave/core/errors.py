"""Structured error types shared by engine-owned contracts.

Errors carry stable machine fields without depending on a logging or transport
framework. Callers decide how and where diagnostics are displayed.
"""

from collections.abc import Mapping

type ErrorValue = str | int | float | bool | None


class LudoWeaveError(Exception):
    """Base class for expected engine failures with immutable context."""

    code: str
    subsystem: str
    phase: str | None
    message: str
    details: tuple[tuple[str, ErrorValue], ...]

    def __init__(
        self,
        message: str,
        *,
        code: str,
        subsystem: str,
        phase: str | None = None,
        details: Mapping[str, ErrorValue] | None = None,
    ) -> None:
        self.message = message
        self.code = code
        self.subsystem = subsystem
        self.phase = phase
        self.details = tuple(sorted((details or {}).items()))
        super().__init__(message)

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation for diagnostic adapters."""

        return {
            "code": self.code,
            "subsystem": self.subsystem,
            "phase": self.phase,
            "message": self.message,
            "details": dict(self.details),
        }

    def __str__(self) -> str:
        location = self.subsystem if self.phase is None else f"{self.subsystem}/{self.phase}"
        context = ", ".join(f"{key}={value!r}" for key, value in self.details)
        suffix = "" if not context else f" ({context})"
        return f"[{self.code}] {location}: {self.message}{suffix}"


class ConfigurationError(LudoWeaveError):
    """Raised when engine configuration violates a declared invariant."""


class ClockError(LudoWeaveError):
    """Raised when a clock receives an invalid or backward time operation."""


class LifecycleError(LudoWeaveError):
    """Raised for invalid transitions or lifecycle subsystem failures."""


class RenderError(LudoWeaveError):
    """Raised for render descriptors, ordering, or backend failures."""
