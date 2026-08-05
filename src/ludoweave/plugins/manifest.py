"""Strict data-only plugin manifests with no discovery or executable hooks."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from itertools import islice
from typing import cast

from ludoweave.core.errors import LudoWeaveError
from ludoweave.world.canonical import JsonLimits, JsonValue, canonical_dumps, canonical_loads

from .errors import PluginManifestError

PLUGIN_MANIFEST_PROTOCOL = "ludoweave.plugin-manifest/1"
PLUGIN_MANIFEST_LIMITS = JsonLimits(
    max_bytes=65_536,
    max_depth=8,
    max_nodes=4_096,
    max_collection_items=256,
    max_string_bytes=512,
)

_MAX_DEPENDENCIES = 64
_MAX_CAPABILITIES = 16
_MAX_PLATFORMS = 3
_PLUGIN_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,62}(?:\.[a-z0-9][a-z0-9-]{0,62})+\Z")
_VERSION = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:(a|b|rc)(0|[1-9][0-9]*))?\Z"
)
_PYTHON_VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")
_MAX_VERSION_PART = 2**31 - 1


class PluginPlatform(StrEnum):
    """Desktop platform families represented by manifest v1."""

    LINUX = "linux"
    MACOS = "macos"
    WINDOWS = "windows"


class PluginCapability(StrEnum):
    """Engine-owned extension boundaries available to manifest v1."""

    AGENT_CAPTURE = "agent.capture"
    AGENT_TELEMETRY = "agent.telemetry"
    AGENT_TEST = "agent.test"
    AUDIO_BACKEND = "audio.backend"
    RENDER_BACKEND = "render.backend"
    RENDER_DEVICE = "render.device"
    RESOURCE_ADAPTER = "resource.adapter"
    TICK_EXECUTOR = "simulation.tick_executor"


class PluginDeterminism(StrEnum):
    """Highest determinism tier a plugin claims for its own behavior."""

    D0 = "d0"
    D1 = "d1"
    D2 = "d2"


@dataclass(frozen=True, slots=True, order=True)
class _ParsedVersion:
    major: int
    minor: int
    patch: int
    phase: int
    serial: int


@dataclass(frozen=True, slots=True)
class VersionRange:
    """Half-open range over the manifest protocol's bounded release syntax."""

    minimum: str
    maximum_exclusive: str

    def __post_init__(self) -> None:
        minimum = _parse_release(self.minimum, field="minimum")
        maximum = _parse_release(self.maximum_exclusive, field="maximum_exclusive")
        if minimum >= maximum:
            raise _manifest_error(
                "version range must be non-empty and increasing",
                phase="construct",
                details={"field": "version_range"},
            )

    def contains(self, version: str) -> bool:
        candidate = _parse_release(version, field="version")
        return (
            _parse_release(self.minimum, field="minimum")
            <= candidate
            < _parse_release(
                self.maximum_exclusive,
                field="maximum_exclusive",
            )
        )

    def as_dict(self) -> dict[str, str]:
        return {
            "minimum": self.minimum,
            "maximum_exclusive": self.maximum_exclusive,
        }


@dataclass(frozen=True, slots=True)
class PythonVersionRange:
    """Half-open CPython major/minor range."""

    minimum: str
    maximum_exclusive: str

    def __post_init__(self) -> None:
        minimum = _parse_python_version(self.minimum, field="minimum")
        maximum = _parse_python_version(self.maximum_exclusive, field="maximum_exclusive")
        if minimum >= maximum:
            raise _manifest_error(
                "Python range must be non-empty and increasing",
                phase="construct",
                details={"field": "python_range"},
            )

    def contains(self, version: str) -> bool:
        candidate = _parse_python_version(version, field="python_version")
        return (
            _parse_python_version(self.minimum, field="minimum")
            <= candidate
            < (_parse_python_version(self.maximum_exclusive, field="maximum_exclusive"))
        )

    def as_dict(self) -> dict[str, str]:
        return {
            "minimum": self.minimum,
            "maximum_exclusive": self.maximum_exclusive,
        }


@dataclass(frozen=True, slots=True)
class PluginRequirement:
    """One required plugin identity and compatible release range."""

    plugin_id: str
    versions: VersionRange

    def __post_init__(self) -> None:
        _require_plugin_id(self.plugin_id, field="requires.plugin_id")
        if type(self.versions) is not VersionRange:
            raise _manifest_error(
                "plugin dependency versions must be an exact VersionRange",
                phase="construct",
                details={"field": "requires.versions"},
            )

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "plugin_id": self.plugin_id,
            "versions": cast(dict[str, JsonValue], self.versions.as_dict()),
        }


@dataclass(frozen=True, slots=True)
class PluginManifest:
    """One immutable, canonical declaration of plugin compatibility metadata."""

    plugin_id: str
    plugin_version: str
    engine: VersionRange
    python: PythonVersionRange
    platforms: tuple[PluginPlatform, ...]
    capabilities: tuple[PluginCapability, ...]
    determinism: PluginDeterminism
    native: bool
    requires: tuple[PluginRequirement, ...] = ()
    protocol: str = PLUGIN_MANIFEST_PROTOCOL

    def __post_init__(self) -> None:
        if type(self.protocol) is not str or self.protocol != PLUGIN_MANIFEST_PROTOCOL:
            raise _manifest_error(
                "plugin manifest protocol is incompatible",
                phase="construct",
                details={"field": "protocol"},
            )
        _require_plugin_id(self.plugin_id, field="plugin_id")
        _parse_release(self.plugin_version, field="plugin_version")
        if type(self.engine) is not VersionRange:
            raise _manifest_error(
                "engine compatibility must be an exact VersionRange",
                phase="construct",
                details={"field": "engine"},
            )
        if type(self.python) is not PythonVersionRange:
            raise _manifest_error(
                "Python compatibility must be an exact PythonVersionRange",
                phase="construct",
                details={"field": "python"},
            )
        platforms = _freeze_enum_values(
            self.platforms,
            PluginPlatform,
            maximum=_MAX_PLATFORMS,
            field="platforms",
        )
        if not platforms:
            raise _manifest_error(
                "plugin manifest must support at least one platform",
                phase="construct",
                details={"field": "platforms"},
            )
        capabilities = _freeze_enum_values(
            self.capabilities,
            PluginCapability,
            maximum=_MAX_CAPABILITIES,
            field="capabilities",
        )
        if not capabilities:
            raise _manifest_error(
                "plugin manifest must declare at least one capability",
                phase="construct",
                details={"field": "capabilities"},
            )
        if type(self.determinism) is not PluginDeterminism:
            raise _manifest_error(
                "plugin determinism must be an exact PluginDeterminism",
                phase="construct",
                details={"field": "determinism"},
            )
        if type(self.native) is not bool:
            raise _manifest_error(
                "plugin native marker must be an exact boolean",
                phase="construct",
                details={"field": "native"},
            )
        requirements = _freeze_requirements(self.requires)
        if any(requirement.plugin_id == self.plugin_id for requirement in requirements):
            raise _manifest_error(
                "plugin manifest cannot require itself",
                phase="construct",
                details={"field": "requires", "plugin_id": self.plugin_id},
            )
        object.__setattr__(self, "platforms", platforms)
        object.__setattr__(self, "capabilities", capabilities)
        object.__setattr__(self, "requires", requirements)

    @classmethod
    def from_mapping(cls, value: object) -> PluginManifest:
        """Decode one already-parsed exact manifest object."""

        document = _require_object(value, role="plugin_manifest")
        _require_exact_fields(
            document,
            required={
                "protocol",
                "plugin_id",
                "plugin_version",
                "engine",
                "python",
                "platforms",
                "capabilities",
                "determinism",
                "native",
                "requires",
            },
            role="plugin_manifest",
        )
        engine = _decode_version_range(document["engine"], role="engine")
        python = _decode_python_range(document["python"])
        platforms = tuple(
            _enum_value(PluginPlatform, item, field="platforms")
            for item in _require_array(
                document["platforms"], role="platforms", maximum=_MAX_PLATFORMS
            )
        )
        capabilities = tuple(
            _enum_value(PluginCapability, item, field="capabilities")
            for item in _require_array(
                document["capabilities"], role="capabilities", maximum=_MAX_CAPABILITIES
            )
        )
        requirements = tuple(
            _decode_requirement(item)
            for item in _require_array(
                document["requires"], role="requires", maximum=_MAX_DEPENDENCIES
            )
        )
        return cls(
            protocol=_require_text(document["protocol"], field="protocol"),
            plugin_id=_require_text(document["plugin_id"], field="plugin_id"),
            plugin_version=_require_text(document["plugin_version"], field="plugin_version"),
            engine=engine,
            python=python,
            platforms=platforms,
            capabilities=capabilities,
            determinism=_enum_value(
                PluginDeterminism,
                document["determinism"],
                field="determinism",
            ),
            native=_require_bool(document["native"], field="native"),
            requires=requirements,
        )

    @classmethod
    def from_json(cls, document: str | bytes) -> PluginManifest:
        """Decode one bounded canonical-JSON-domain manifest."""

        try:
            decoded = canonical_loads(document, limits=PLUGIN_MANIFEST_LIMITS)
        except LudoWeaveError as error:
            raise _manifest_error(
                "plugin manifest JSON is malformed or outside its limits",
                phase="decode",
                details={"cause_code": error.code},
            ) from error
        return cls.from_mapping(decoded)

    @property
    def fingerprint(self) -> str:
        return f"sha256:{sha256(self.canonical_bytes()).hexdigest()}"

    def as_dict(self) -> dict[str, JsonValue]:
        return {
            "protocol": self.protocol,
            "plugin_id": self.plugin_id,
            "plugin_version": self.plugin_version,
            "engine": cast(dict[str, JsonValue], self.engine.as_dict()),
            "python": cast(dict[str, JsonValue], self.python.as_dict()),
            "platforms": [platform.value for platform in self.platforms],
            "capabilities": [capability.value for capability in self.capabilities],
            "determinism": self.determinism.value,
            "native": self.native,
            "requires": [requirement.as_dict() for requirement in self.requires],
        }

    def canonical_bytes(self) -> bytes:
        return canonical_dumps(self.as_dict(), limits=PLUGIN_MANIFEST_LIMITS)


def _decode_version_range(value: object, *, role: str) -> VersionRange:
    document = _require_object(value, role=role)
    _require_exact_fields(document, required={"minimum", "maximum_exclusive"}, role=role)
    return VersionRange(
        minimum=_require_text(document["minimum"], field=f"{role}.minimum"),
        maximum_exclusive=_require_text(
            document["maximum_exclusive"],
            field=f"{role}.maximum_exclusive",
        ),
    )


def _decode_python_range(value: object) -> PythonVersionRange:
    document = _require_object(value, role="python")
    _require_exact_fields(
        document,
        required={"minimum", "maximum_exclusive"},
        role="python",
    )
    return PythonVersionRange(
        minimum=_require_text(document["minimum"], field="python.minimum"),
        maximum_exclusive=_require_text(
            document["maximum_exclusive"],
            field="python.maximum_exclusive",
        ),
    )


def _decode_requirement(value: object) -> PluginRequirement:
    document = _require_object(value, role="requirement")
    _require_exact_fields(document, required={"plugin_id", "versions"}, role="requirement")
    return PluginRequirement(
        plugin_id=_require_text(document["plugin_id"], field="requires.plugin_id"),
        versions=_decode_version_range(document["versions"], role="requires.versions"),
    )


def _freeze_requirements(values: Iterable[PluginRequirement]) -> tuple[PluginRequirement, ...]:
    materialized = _bounded_tuple(values, maximum=_MAX_DEPENDENCIES, field="requires")
    if any(type(item) is not PluginRequirement for item in materialized):
        raise _manifest_error(
            "plugin requirements must contain exact PluginRequirement values",
            phase="construct",
            details={"field": "requires"},
        )
    requirements = cast(tuple[PluginRequirement, ...], materialized)
    identities = [requirement.plugin_id for requirement in requirements]
    if len(identities) != len(set(identities)):
        raise _manifest_error(
            "plugin requirements must have unique identities",
            phase="construct",
            details={"field": "requires"},
        )
    return tuple(sorted(requirements, key=lambda item: item.plugin_id))


def _freeze_enum_values[EnumT: StrEnum](
    values: Iterable[EnumT],
    enum_type: type[EnumT],
    *,
    maximum: int,
    field: str,
) -> tuple[EnumT, ...]:
    materialized = _bounded_tuple(values, maximum=maximum, field=field)
    if any(type(item) is not enum_type for item in materialized):
        raise _manifest_error(
            f"{field} must contain exact {enum_type.__name__} values",
            phase="construct",
            details={"field": field},
        )
    checked = cast(tuple[EnumT, ...], materialized)
    if len(checked) != len(set(checked)):
        raise _manifest_error(
            f"{field} must not contain duplicates",
            phase="construct",
            details={"field": field},
        )
    return tuple(sorted(checked, key=lambda item: item.value))


def _bounded_tuple(values: Iterable[object], *, maximum: int, field: str) -> tuple[object, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise _manifest_error(
            "plugin manifest collections must be iterables of records",
            phase="construct",
            details={"field": field, "actual_type": type(values).__name__},
        )
    try:
        materialized = tuple(islice(iter(values), maximum + 1))
    except Exception as error:
        raise _manifest_error(
            "plugin manifest collection could not be materialized",
            phase="construct",
            details={"field": field, "actual_type": type(values).__name__},
        ) from error
    if len(materialized) > maximum:
        raise _manifest_error(
            "plugin manifest collection exceeds its item limit",
            phase="construct",
            details={"field": field, "limit": maximum},
        )
    return materialized


def _enum_value[EnumT: StrEnum](
    enum_type: type[EnumT],
    value: object,
    *,
    field: str,
) -> EnumT:
    text = _require_text(value, field=field)
    try:
        return enum_type(text)
    except ValueError as error:
        raise _manifest_error(
            "plugin manifest enum value is unsupported",
            phase="decode",
            details={"field": field},
        ) from error


def _parse_release(value: object, *, field: str) -> _ParsedVersion:
    if type(value) is not str or len(value) > 64:
        raise _manifest_error(
            "release version must use bounded text",
            phase="construct",
            details={"field": field, "actual_type": type(value).__name__},
        )
    match = _VERSION.fullmatch(value)
    if match is None:
        raise _manifest_error(
            "release version must use MAJOR.MINOR.PATCH with optional a, b, or rc suffix",
            phase="construct",
            details={"field": field},
        )
    major, minor, patch = (int(match.group(index)) for index in range(1, 4))
    serial_text = match.group(5)
    serial = 0 if serial_text is None else int(serial_text)
    if any(part > _MAX_VERSION_PART for part in (major, minor, patch, serial)):
        raise _manifest_error(
            "release version component exceeds its integer limit",
            phase="construct",
            details={"field": field},
        )
    phase_text = match.group(4)
    phase = {"a": 0, "b": 1, "rc": 2, None: 3}[phase_text]
    return _ParsedVersion(major, minor, patch, phase, serial)


def _parse_python_version(value: object, *, field: str) -> tuple[int, int]:
    if type(value) is not str or len(value) > 32:
        raise _manifest_error(
            "Python version must use bounded MAJOR.MINOR text",
            phase="construct",
            details={"field": field, "actual_type": type(value).__name__},
        )
    match = _PYTHON_VERSION.fullmatch(value)
    if match is None:
        raise _manifest_error(
            "Python version must use MAJOR.MINOR text",
            phase="construct",
            details={"field": field},
        )
    result = (int(match.group(1)), int(match.group(2)))
    if any(part > _MAX_VERSION_PART for part in result):
        raise _manifest_error(
            "Python version component exceeds its integer limit",
            phase="construct",
            details={"field": field},
        )
    return result


def _require_plugin_id(value: object, *, field: str) -> str:
    if type(value) is not str or len(value) > 128 or _PLUGIN_ID.fullmatch(value) is None:
        raise _manifest_error(
            "plugin identity must be a bounded lowercase dotted identifier",
            phase="construct",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _require_object(value: object, *, role: str) -> dict[str, object]:
    if type(value) is not dict:
        raise _manifest_error(
            "plugin manifest record must be an object",
            phase="decode",
            details={"role": role, "actual_type": type(value).__name__},
        )
    return cast(dict[str, object], value)


def _require_array(value: object, *, role: str, maximum: int) -> list[object]:
    if type(value) is not list:
        raise _manifest_error(
            "plugin manifest collection must be an array",
            phase="decode",
            details={"role": role, "actual_type": type(value).__name__},
        )
    checked = cast(list[object], value)
    if len(checked) > maximum:
        raise _manifest_error(
            "plugin manifest collection exceeds its item limit",
            phase="decode",
            details={"role": role, "limit": maximum, "actual": len(checked)},
        )
    return checked


def _require_exact_fields(
    value: Mapping[str, object],
    *,
    required: set[str],
    role: str,
) -> None:
    actual_count = len(value)
    if actual_count > len(required):
        raise _manifest_error(
            "plugin manifest record fields do not match its schema",
            phase="decode",
            details={
                "role": role,
                "expected_count": len(required),
                "actual_count": actual_count,
            },
        )
    keys = tuple(value.keys())
    invalid_key_count = sum(type(key) is not str for key in keys)
    if invalid_key_count:
        raise _manifest_error(
            "plugin manifest record keys must be exact strings",
            phase="decode",
            details={"role": role, "invalid_key_count": invalid_key_count},
        )
    checked_keys = set(keys)
    missing = required - checked_keys
    unexpected = checked_keys - required
    if missing or unexpected:
        raise _manifest_error(
            "plugin manifest record fields do not match its schema",
            phase="decode",
            details={
                "role": role,
                "missing_count": len(missing),
                "unexpected_count": len(unexpected),
            },
        )


def _require_text(value: object, *, field: str) -> str:
    if type(value) is not str:
        raise _manifest_error(
            "plugin manifest field must contain text",
            phase="decode",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _require_bool(value: object, *, field: str) -> bool:
    if type(value) is not bool:
        raise _manifest_error(
            "plugin manifest field must contain a boolean",
            phase="decode",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _manifest_error(
    message: str,
    *,
    phase: str,
    details: Mapping[str, str | int | float | bool | None],
) -> PluginManifestError:
    return PluginManifestError(
        message,
        code="plugins.invalid_manifest",
        subsystem="plugins",
        phase=phase,
        details=details,
    )
