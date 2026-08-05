"""Structured failures for data-only plugin contracts."""

from ludoweave.core.errors import LudoWeaveError


class PluginError(LudoWeaveError):
    """Base class for plugin manifest and compatibility failures."""


class PluginManifestError(PluginError):
    """Raised when a plugin manifest violates its bounded wire schema."""


class PluginCompatibilityError(PluginError):
    """Raised when a compatibility request itself is malformed."""
