"""Structured failures for the transport-independent agent service."""

from ludoweave.core.errors import LudoWeaveError


class AgentError(LudoWeaveError):
    """Base class for expected agent-service failures."""


class AgentRequestError(AgentError):
    """Raised when a tool request does not match its typed contract."""


class AgentCapabilityError(AgentError):
    """Raised when a disabled capability is requested."""


class AgentLimitError(AgentError):
    """Raised before bounded agent work would exceed a configured quota."""


class AgentConcurrencyError(AgentError):
    """Raised when a call cannot enter the single-owner safe point."""


class AgentProviderError(AgentError):
    """Raised when an injected capture, test, or telemetry provider fails."""
