"""Structured failures for fixed-step application composition and execution."""

from ludoweave.core.errors import LudoWeaveError


class ApplicationError(LudoWeaveError):
    """Base class for fixed-step application failures."""


class InputError(ApplicationError):
    """Raised for malformed immutable input declarations and timelines."""


class InputFrameError(ApplicationError):
    """Raised when an input source cannot provide the requested tick."""


class SystemAccessError(ApplicationError):
    """Raised when a system context request exceeds declared access."""


class SystemExecutionError(ApplicationError):
    """Raised when one planned system invocation does not complete."""
