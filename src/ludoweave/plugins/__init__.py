"""Preview data-only plugin manifest and compatibility contracts."""

from .compatibility import (
    PLUGIN_CHECK_PROTOCOL,
    PluginCompatibilityContext,
    PluginCompatibilityIssue,
    PluginCompatibilityReport,
    check_plugin_compatibility,
    current_plugin_context,
)
from .errors import PluginCompatibilityError, PluginError, PluginManifestError
from .manifest import (
    PLUGIN_MANIFEST_PROTOCOL,
    PluginCapability,
    PluginDeterminism,
    PluginManifest,
    PluginPlatform,
    PluginRequirement,
    PythonVersionRange,
    VersionRange,
)

__all__ = [
    "PLUGIN_CHECK_PROTOCOL",
    "PLUGIN_MANIFEST_PROTOCOL",
    "PluginCapability",
    "PluginCompatibilityContext",
    "PluginCompatibilityError",
    "PluginCompatibilityIssue",
    "PluginCompatibilityReport",
    "PluginDeterminism",
    "PluginError",
    "PluginManifest",
    "PluginManifestError",
    "PluginPlatform",
    "PluginRequirement",
    "PythonVersionRange",
    "VersionRange",
    "check_plugin_compatibility",
    "current_plugin_context",
]
__stability__ = {name: "preview" for name in __all__}
