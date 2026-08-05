# pyright: reportPrivateUsage=false
"""Deterministic compatibility evaluation for explicit plugin manifests."""

from __future__ import annotations

import re
import sys
from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from hashlib import sha256
from itertools import islice
from math import isfinite
from typing import cast

from ludoweave.core.errors import LudoWeaveError
from ludoweave.core.version import __version__
from ludoweave.world.canonical import JsonLimits, JsonValue, canonical_dumps

from .errors import PluginCompatibilityError, PluginManifestError
from .manifest import (
    PluginCapability,
    PluginDeterminism,
    PluginManifest,
    PluginPlatform,
    _parse_python_version,
    _parse_release,
    _require_plugin_id,
)

PLUGIN_CHECK_PROTOCOL = "ludoweave.plugin-check/1"
_PLUGIN_CHECK_LIMITS = JsonLimits(
    max_bytes=4_194_304,
    max_depth=8,
    max_nodes=100_000,
    max_collection_items=10_000,
    max_string_bytes=512,
)
_MAX_PLUGINS = 64
_MAX_ISSUES = 6_000
_ISSUE_CODE = re.compile(r"plugins\.[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+\Z")
_DETAIL_KEY = re.compile(r"[a-z][a-z0-9_]{0,63}\Z")
type CompatibilityValue = str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class PluginCompatibilityContext:
    """Explicit environment and policy used for one compatibility decision."""

    engine_version: str
    python_version: str
    python_implementation: str
    platform: PluginPlatform
    minimum_determinism: PluginDeterminism = PluginDeterminism.D0
    allow_native: bool = False
    supported_capabilities: tuple[PluginCapability, ...] = tuple(PluginCapability)

    def __post_init__(self) -> None:
        try:
            _parse_release(self.engine_version, field="context.engine_version")
        except PluginManifestError as error:
            raise _compatibility_error(
                "engine compatibility context version is invalid",
                phase="configure",
                details={"field": "engine_version"},
            ) from error
        try:
            _parse_python_version(self.python_version, field="context.python_version")
        except PluginManifestError as error:
            raise _compatibility_error(
                "Python compatibility context version is invalid",
                phase="configure",
                details={"field": "python_version"},
            ) from error
        if (
            type(self.python_implementation) is not str
            or not self.python_implementation
            or len(self.python_implementation) > 32
            or not self.python_implementation.isascii()
        ):
            raise _compatibility_error(
                "Python implementation must be bounded ASCII text",
                phase="configure",
                details={"field": "python_implementation"},
            )
        if type(self.platform) is not PluginPlatform:
            raise _compatibility_error(
                "platform must be an exact PluginPlatform",
                phase="configure",
                details={"field": "platform"},
            )
        if type(self.minimum_determinism) is not PluginDeterminism:
            raise _compatibility_error(
                "minimum determinism must be an exact PluginDeterminism",
                phase="configure",
                details={"field": "minimum_determinism"},
            )
        if type(self.allow_native) is not bool:
            raise _compatibility_error(
                "native policy must be an exact boolean",
                phase="configure",
                details={"field": "allow_native"},
            )
        capabilities = _freeze_capabilities(self.supported_capabilities)
        object.__setattr__(self, "supported_capabilities", capabilities)

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "engine_version": self.engine_version,
            "python_version": self.python_version,
            "python_implementation": self.python_implementation,
            "platform": self.platform.value,
            "minimum_determinism": self.minimum_determinism.value,
            "allow_native": self.allow_native,
            "supported_capabilities": [item.value for item in self.supported_capabilities],
        }


@dataclass(frozen=True, slots=True)
class PluginCompatibilityIssue:
    """One stable incompatibility code with bounded detached context."""

    code: str
    plugin_id: str
    details: tuple[tuple[str, CompatibilityValue], ...] = ()

    def __post_init__(self) -> None:
        if type(self.code) is not str or _ISSUE_CODE.fullmatch(self.code) is None:
            raise _compatibility_error(
                "compatibility issue code is invalid",
                phase="report",
                details={"field": "code"},
            )
        _validate_report_plugin_id(self.plugin_id, field="plugin_id")
        if isinstance(self.details, (str, bytes, bytearray)):
            raise _compatibility_error(
                "compatibility issue details must be a collection of key-value pairs",
                phase="report",
                details={"field": "details"},
            )
        try:
            details = tuple(islice(iter(self.details), 17))
        except Exception as error:
            raise _compatibility_error(
                "compatibility issue details could not be materialized",
                phase="report",
                details={"field": "details"},
            ) from error
        if len(details) > 16:
            raise _compatibility_error(
                "compatibility issue details exceed their limit",
                phase="report",
                details={"field": "details", "limit": 16},
            )
        checked: list[tuple[str, CompatibilityValue]] = []
        for entry in details:
            if type(entry) is not tuple or len(entry) != 2:
                raise _compatibility_error(
                    "compatibility issue detail must be a two-item tuple",
                    phase="report",
                    details={"field": "details"},
                )
            key, value = entry
            if type(key) is not str or _DETAIL_KEY.fullmatch(key) is None:
                raise _compatibility_error(
                    "compatibility issue detail key is invalid",
                    phase="report",
                    details={"field": "details"},
                )
            if value is not None and type(value) not in (str, int, float, bool):
                raise _compatibility_error(
                    "compatibility issue detail value is invalid",
                    phase="report",
                    details={"field": key},
                )
            if type(value) is float and not isfinite(value):
                raise _compatibility_error(
                    "compatibility issue detail number must be finite",
                    phase="report",
                    details={"field": key},
                )
            if type(value) is int and not -(2**63) <= value <= 2**63 - 1:
                raise _compatibility_error(
                    "compatibility issue detail integer is outside its range",
                    phase="report",
                    details={"field": key},
                )
            if type(value) is str:
                try:
                    encoded_length = len(value.encode("utf-8"))
                except UnicodeEncodeError as error:
                    raise _compatibility_error(
                        "compatibility issue detail text is not valid Unicode",
                        phase="report",
                        details={"field": key},
                    ) from error
                if encoded_length > 512:
                    raise _compatibility_error(
                        "compatibility issue detail text exceeds its limit",
                        phase="report",
                        details={"field": key, "limit": 512},
                    )
            checked.append((key, value))
        if len({key for key, _value in checked}) != len(checked):
            raise _compatibility_error(
                "compatibility issue detail keys must be unique",
                phase="report",
                details={"field": "details"},
            )
        object.__setattr__(self, "details", tuple(sorted(checked)))

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "code": self.code,
            "plugin_id": self.plugin_id,
            "details": cast(dict[str, JsonValue], dict(self.details)),
        }


@dataclass(frozen=True, slots=True)
class PluginCompatibilityReport:
    """Canonical compatibility result for one explicit manifest set."""

    context: PluginCompatibilityContext
    plugin_ids: tuple[str, ...]
    manifest_fingerprint: str
    issues: tuple[PluginCompatibilityIssue, ...]
    protocol: str = PLUGIN_CHECK_PROTOCOL

    def __post_init__(self) -> None:
        if type(self.protocol) is not str or self.protocol != PLUGIN_CHECK_PROTOCOL:
            raise _compatibility_error(
                "plugin check protocol is incompatible",
                phase="report",
                details={"field": "protocol"},
            )
        if type(self.context) is not PluginCompatibilityContext:
            raise _compatibility_error(
                "plugin check context has the wrong type",
                phase="report",
                details={"field": "context"},
            )
        if isinstance(self.plugin_ids, (str, bytes, bytearray)):
            raise _compatibility_error(
                "plugin report identities must be a collection of plugin identities",
                phase="report",
                details={"field": "plugin_ids"},
            )
        try:
            plugin_ids = tuple(islice(iter(self.plugin_ids), _MAX_PLUGINS + 1))
        except Exception as error:
            raise _compatibility_error(
                "plugin report identities could not be materialized",
                phase="report",
                details={"field": "plugin_ids"},
            ) from error
        if len(plugin_ids) > _MAX_PLUGINS:
            raise _compatibility_error(
                "plugin report identities are invalid or exceed their limit",
                phase="report",
                details={"field": "plugin_ids", "limit": _MAX_PLUGINS},
            )
        for plugin_id in plugin_ids:
            _validate_report_plugin_id(plugin_id, field="plugin_ids")
        if tuple(sorted(plugin_ids)) != plugin_ids:
            raise _compatibility_error(
                "plugin report identities must be canonically ordered",
                phase="report",
                details={"field": "plugin_ids"},
            )
        if type(self.manifest_fingerprint) is not str or not re.fullmatch(
            r"sha256:[0-9a-f]{64}", self.manifest_fingerprint
        ):
            raise _compatibility_error(
                "plugin manifest fingerprint is invalid",
                phase="report",
                details={"field": "manifest_fingerprint"},
            )
        if isinstance(self.issues, (str, bytes, bytearray)):
            raise _compatibility_error(
                "plugin report issues must be a collection of compatibility issues",
                phase="report",
                details={"field": "issues"},
            )
        try:
            issues = tuple(islice(iter(self.issues), _MAX_ISSUES + 1))
        except Exception as error:
            raise _compatibility_error(
                "plugin report issues could not be materialized",
                phase="report",
                details={"field": "issues"},
            ) from error
        if len(issues) > _MAX_ISSUES or any(
            type(issue) is not PluginCompatibilityIssue for issue in issues
        ):
            raise _compatibility_error(
                "plugin report issues are invalid or exceed their limit",
                phase="report",
                details={"field": "issues", "limit": _MAX_ISSUES},
            )
        checked_issues = issues
        expected_issues = tuple(sorted(checked_issues, key=_issue_sort_key))
        if expected_issues != checked_issues:
            raise _compatibility_error(
                "plugin report issues must be canonically ordered",
                phase="report",
                details={"field": "issues"},
            )
        object.__setattr__(self, "plugin_ids", plugin_ids)
        object.__setattr__(self, "issues", checked_issues)
        try:
            canonical_dumps(self.as_dict(), limits=_PLUGIN_CHECK_LIMITS)
        except LudoWeaveError as error:
            raise _compatibility_error(
                "plugin compatibility report is not canonically serializable",
                phase="report",
                details={"field": "report"},
            ) from error

    @property
    def compatible(self) -> bool:
        return not self.issues

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "protocol": self.protocol,
            "compatible": self.compatible,
            "plugin_count": len(self.plugin_ids),
            "plugin_ids": list(self.plugin_ids),
            "manifest_fingerprint": self.manifest_fingerprint,
            "context": self.context.as_dict(),
            "issues": [issue.as_dict() for issue in self.issues],
        }

    def canonical_bytes(self) -> bytes:
        return canonical_dumps(self.as_dict(), limits=_PLUGIN_CHECK_LIMITS)


def current_plugin_context(
    *,
    minimum_determinism: PluginDeterminism = PluginDeterminism.D0,
    allow_native: bool = False,
    supported_capabilities: Iterable[PluginCapability] = tuple(PluginCapability),
) -> PluginCompatibilityContext:
    """Describe the current supported CPython/desktop process without paths."""

    platform = _current_platform(sys.platform)
    return PluginCompatibilityContext(
        engine_version=__version__,
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}",
        python_implementation=sys.implementation.name,
        platform=platform,
        minimum_determinism=minimum_determinism,
        allow_native=allow_native,
        supported_capabilities=cast(tuple[PluginCapability, ...], supported_capabilities),
    )


def check_plugin_compatibility(
    manifests: Iterable[PluginManifest],
    context: PluginCompatibilityContext,
) -> PluginCompatibilityReport:
    """Evaluate a bounded explicit manifest set without loading plugin code."""

    if type(context) is not PluginCompatibilityContext:
        raise _compatibility_error(
            "plugin check requires an exact compatibility context",
            phase="check",
            details={"field": "context"},
        )
    checked = _freeze_manifests(manifests)
    ordered = tuple(sorted(checked, key=lambda item: item.canonical_bytes()))
    issues: list[PluginCompatibilityIssue] = []
    counts = Counter(manifest.plugin_id for manifest in ordered)
    for plugin_id, count in sorted(counts.items()):
        if count > 1:
            issues.append(_issue("plugins.compatibility.duplicate_id", plugin_id, count=count))

    unique = {
        manifest.plugin_id: manifest for manifest in ordered if counts[manifest.plugin_id] == 1
    }
    supported = frozenset(context.supported_capabilities)
    for manifest in ordered:
        issues.extend(_check_manifest(manifest, context=context, supported=supported))
        if counts[manifest.plugin_id] != 1:
            continue
        for requirement in manifest.requires:
            if counts.get(requirement.plugin_id, 0) > 1:
                issues.append(
                    _issue(
                        "plugins.compatibility.dependency_ambiguous",
                        manifest.plugin_id,
                        dependency=requirement.plugin_id,
                    )
                )
                continue
            dependency = unique.get(requirement.plugin_id)
            if dependency is None:
                issues.append(
                    _issue(
                        "plugins.compatibility.dependency_missing",
                        manifest.plugin_id,
                        dependency=requirement.plugin_id,
                    )
                )
                continue
            if not requirement.versions.contains(dependency.plugin_version):
                issues.append(
                    _issue(
                        "plugins.compatibility.dependency_version",
                        manifest.plugin_id,
                        dependency=requirement.plugin_id,
                        actual=dependency.plugin_version,
                        minimum=requirement.versions.minimum,
                        maximum_exclusive=requirement.versions.maximum_exclusive,
                    )
                )

    issues.extend(_dependency_cycle_issues(unique))
    sorted_issues = tuple(sorted(issues, key=_issue_sort_key))
    digest = sha256()
    for manifest in ordered:
        encoded = manifest.canonical_bytes()
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    fingerprint = f"sha256:{digest.hexdigest()}"
    return PluginCompatibilityReport(
        context=context,
        plugin_ids=tuple(sorted(manifest.plugin_id for manifest in ordered)),
        manifest_fingerprint=fingerprint,
        issues=sorted_issues,
    )


def _check_manifest(
    manifest: PluginManifest,
    *,
    context: PluginCompatibilityContext,
    supported: frozenset[PluginCapability],
) -> list[PluginCompatibilityIssue]:
    issues: list[PluginCompatibilityIssue] = []
    if not manifest.engine.contains(context.engine_version):
        issues.append(
            _issue(
                "plugins.compatibility.engine_version",
                manifest.plugin_id,
                actual=context.engine_version,
                minimum=manifest.engine.minimum,
                maximum_exclusive=manifest.engine.maximum_exclusive,
            )
        )
    if context.python_implementation != "cpython":
        issues.append(
            _issue(
                "plugins.compatibility.python_implementation",
                manifest.plugin_id,
                actual=context.python_implementation,
                required="cpython",
            )
        )
    if not manifest.python.contains(context.python_version):
        issues.append(
            _issue(
                "plugins.compatibility.python_version",
                manifest.plugin_id,
                actual=context.python_version,
                minimum=manifest.python.minimum,
                maximum_exclusive=manifest.python.maximum_exclusive,
            )
        )
    if context.platform not in manifest.platforms:
        issues.append(
            _issue(
                "plugins.compatibility.platform",
                manifest.plugin_id,
                actual=context.platform.value,
                supported=",".join(platform.value for platform in manifest.platforms),
            )
        )
    if manifest.native and not context.allow_native:
        issues.append(
            _issue(
                "plugins.compatibility.native_forbidden",
                manifest.plugin_id,
            )
        )
    if _determinism_rank(manifest.determinism) < _determinism_rank(context.minimum_determinism):
        issues.append(
            _issue(
                "plugins.compatibility.determinism",
                manifest.plugin_id,
                actual=manifest.determinism.value,
                minimum=context.minimum_determinism.value,
            )
        )
    for capability in manifest.capabilities:
        if capability not in supported:
            issues.append(
                _issue(
                    "plugins.compatibility.capability",
                    manifest.plugin_id,
                    capability=capability.value,
                )
            )
    return issues


def _dependency_cycle_issues(
    manifests: Mapping[str, PluginManifest],
) -> list[PluginCompatibilityIssue]:
    graph = {
        plugin_id: tuple(
            sorted(
                requirement.plugin_id
                for requirement in manifest.requires
                if requirement.plugin_id in manifests
            )
        )
        for plugin_id, manifest in manifests.items()
    }
    index = 0
    indices: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    components: list[tuple[str, ...]] = []

    def strong_connect(node: str) -> None:
        nonlocal index
        indices[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for target in graph[node]:
            if target not in indices:
                strong_connect(target)
                lowlinks[node] = min(lowlinks[node], lowlinks[target])
            elif target in on_stack:
                lowlinks[node] = min(lowlinks[node], indices[target])
        if lowlinks[node] != indices[node]:
            return
        component: list[str] = []
        while stack:
            member = stack.pop()
            on_stack.remove(member)
            component.append(member)
            if member == node:
                break
        components.append(tuple(sorted(component)))

    for plugin_id in sorted(graph):
        if plugin_id not in indices:
            strong_connect(plugin_id)

    issues: list[PluginCompatibilityIssue] = []
    for component in sorted(components):
        if len(component) < 2:
            continue
        cycle_fingerprint = f"sha256:{sha256(canonical_dumps(list(component))).hexdigest()}"
        issues.extend(
            _issue(
                "plugins.compatibility.dependency_cycle",
                plugin_id,
                cycle_fingerprint=cycle_fingerprint,
                cycle_size=len(component),
            )
            for plugin_id in component
        )
    return issues


def _determinism_rank(value: PluginDeterminism) -> int:
    if value is PluginDeterminism.D0:
        return 0
    if value is PluginDeterminism.D1:
        return 1
    return 2


def _freeze_manifests(values: Iterable[PluginManifest]) -> tuple[PluginManifest, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise _compatibility_error(
            "plugin manifests must be an iterable of records",
            phase="check",
            details={"field": "manifests", "actual_type": type(values).__name__},
        )
    try:
        manifests = tuple(islice(iter(values), _MAX_PLUGINS + 1))
    except Exception as error:
        raise _compatibility_error(
            "plugin manifests could not be materialized",
            phase="check",
            details={"field": "manifests", "actual_type": type(values).__name__},
        ) from error
    if len(manifests) > _MAX_PLUGINS:
        raise _compatibility_error(
            "plugin manifest set exceeds its item limit",
            phase="check",
            details={"field": "manifests", "limit": _MAX_PLUGINS},
        )
    if any(type(manifest) is not PluginManifest for manifest in manifests):
        raise _compatibility_error(
            "plugin manifest set contains the wrong value type",
            phase="check",
            details={"field": "manifests"},
        )
    return manifests


def _freeze_capabilities(values: Iterable[PluginCapability]) -> tuple[PluginCapability, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise _compatibility_error(
            "supported capabilities must be an iterable",
            phase="configure",
            details={"field": "supported_capabilities"},
        )
    try:
        capabilities = tuple(islice(iter(values), len(PluginCapability) + 1))
    except Exception as error:
        raise _compatibility_error(
            "supported capabilities could not be materialized",
            phase="configure",
            details={"field": "supported_capabilities"},
        ) from error
    if len(capabilities) > len(PluginCapability):
        raise _compatibility_error(
            "supported capabilities exceed their item limit",
            phase="configure",
            details={"field": "supported_capabilities", "limit": len(PluginCapability)},
        )
    if any(type(capability) is not PluginCapability for capability in capabilities):
        raise _compatibility_error(
            "supported capabilities contain the wrong value type",
            phase="configure",
            details={"field": "supported_capabilities"},
        )
    checked = capabilities
    if len(checked) != len(set(checked)):
        raise _compatibility_error(
            "supported capabilities must be unique",
            phase="configure",
            details={"field": "supported_capabilities"},
        )
    return tuple(sorted(checked, key=lambda item: item.value))


def _current_platform(value: str) -> PluginPlatform:
    if value.startswith("linux"):
        return PluginPlatform.LINUX
    if value == "darwin":
        return PluginPlatform.MACOS
    if value in {"win32", "cygwin"}:
        return PluginPlatform.WINDOWS
    raise _compatibility_error(
        "current platform is outside the supported desktop families",
        phase="configure",
        details={"field": "platform"},
    )


def _issue(
    code: str,
    plugin_id: str,
    **details: CompatibilityValue,
) -> PluginCompatibilityIssue:
    return PluginCompatibilityIssue(code, plugin_id, tuple(details.items()))


def _issue_sort_key(
    issue: PluginCompatibilityIssue,
) -> tuple[str, str, bytes]:
    return (issue.plugin_id, issue.code, canonical_dumps(issue.as_dict()))


def _compatibility_error(
    message: str,
    *,
    phase: str,
    details: Mapping[str, CompatibilityValue],
) -> PluginCompatibilityError:
    return PluginCompatibilityError(
        message,
        code="plugins.invalid_compatibility_request",
        subsystem="plugins",
        phase=phase,
        details=details,
    )


def _validate_report_plugin_id(value: object, *, field: str) -> str:
    try:
        return _require_plugin_id(value, field=field)
    except PluginManifestError as error:
        raise _compatibility_error(
            "plugin compatibility report identity is invalid",
            phase="report",
            details={"field": field},
        ) from error
