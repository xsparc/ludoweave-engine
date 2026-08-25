"""Bounded explicit manifests for project-confined scene and prefab sources."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import PurePosixPath, PureWindowsPath
from typing import Literal, cast

from ludoweave.core.errors import LudoWeaveError
from ludoweave.scene.errors import SceneError
from ludoweave.world.canonical import JsonLimits, JsonValue, canonical_dumps, canonical_loads

SOURCE_MANIFEST_PROTOCOL = "ludoweave.source-manifest/1"

_STABLE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_MAX_BYTES = 65_536
_MAX_ENTRIES = 256
_MAX_PATH_BYTES = 1_024
_MAX_DEPTH = 8
_MAX_NODES = 4_096
_MAX_COLLECTION_ITEMS = 1_024
_MAX_STRING_BYTES = 4_096
_WINDOWS_RESERVED = frozenset(
    {
        "AUX",
        "CON",
        "CONIN$",
        "CONOUT$",
        "NUL",
        "PRN",
        *(f"COM{index}" for index in range(1, 10)),
        *(f"LPT{index}" for index in range(1, 10)),
    }
)


@dataclass(frozen=True, slots=True)
class SourceManifestLimits:
    """Hard limits for one explicit source manifest."""

    max_bytes: int = _MAX_BYTES
    max_entries: int = _MAX_ENTRIES
    max_path_bytes: int = _MAX_PATH_BYTES

    def __post_init__(self) -> None:
        for field, maximum in (
            ("max_bytes", _MAX_BYTES),
            ("max_entries", _MAX_ENTRIES),
            ("max_path_bytes", _MAX_PATH_BYTES),
        ):
            value = getattr(self, field)
            if type(value) is not int or value <= 0:
                raise _manifest_error(
                    "source manifest limits must be exact positive integers",
                    code="source_manifest.invalid_limits",
                    phase="configure",
                    details={"field": field, "actual_type": type(value).__name__},
                )
            if value > maximum:
                raise _manifest_error(
                    "source manifest limits may tighten but not exceed hard maxima",
                    code="source_manifest.invalid_limits",
                    phase="configure",
                    details={"field": field, "actual": value, "maximum": maximum},
                )

    def json_limits(self) -> JsonLimits:
        """Return the shared canonical-JSON limits for this manifest."""

        return JsonLimits(
            max_bytes=self.max_bytes,
            max_depth=_MAX_DEPTH,
            max_nodes=_MAX_NODES,
            max_collection_items=_MAX_COLLECTION_ITEMS,
            max_string_bytes=_MAX_STRING_BYTES,
        )


DEFAULT_SOURCE_MANIFEST_LIMITS = SourceManifestLimits()


@dataclass(frozen=True, slots=True)
class SourceManifestEntry:
    """One explicitly named scene or prefab-source/instance pair."""

    entry_id: str
    kind: Literal["scene", "prefab"]
    source: str
    instance: str | None = None

    def __post_init__(self) -> None:
        _stable_id(self.entry_id, field="entry_id", phase="construct")
        if self.kind not in ("scene", "prefab"):
            raise _manifest_error(
                "source manifest entry kind is unsupported",
                code="source_manifest.invalid_entry",
                phase="construct",
                details={"entry_id": self.entry_id, "field": "kind"},
            )
        _portable_relative_path(
            self.source,
            field="source",
            entry_id=self.entry_id,
            max_bytes=_MAX_PATH_BYTES,
            phase="construct",
        )
        if self.kind == "scene":
            if self.instance is not None:
                raise _manifest_error(
                    "scene manifest entries cannot identify a prefab instance",
                    code="source_manifest.invalid_entry",
                    phase="construct",
                    details={"entry_id": self.entry_id, "field": "instance"},
                )
        elif self.instance is None:
            raise _manifest_error(
                "prefab manifest entries require one explicit instance",
                code="source_manifest.invalid_entry",
                phase="construct",
                details={"entry_id": self.entry_id, "field": "instance"},
            )
        else:
            _portable_relative_path(
                self.instance,
                field="instance",
                entry_id=self.entry_id,
                max_bytes=_MAX_PATH_BYTES,
                phase="construct",
            )

    def as_dict(self) -> dict[str, JsonValue]:
        value: dict[str, JsonValue] = {
            "entry_id": self.entry_id,
            "kind": self.kind,
            "source": self.source,
        }
        if self.instance is not None:
            value["instance"] = self.instance
        return value


@dataclass(frozen=True, slots=True)
class SourceManifest:
    """A normalized explicit source list with no discovery or runtime state."""

    manifest_id: str
    entries: tuple[SourceManifestEntry, ...]
    protocol: str = SOURCE_MANIFEST_PROTOCOL

    def __post_init__(self) -> None:
        if type(self.protocol) is not str or self.protocol != SOURCE_MANIFEST_PROTOCOL:
            raise _manifest_error(
                "source manifest protocol is unsupported",
                code="source_manifest.incompatible_protocol",
                phase="construct",
                details={"field": "$schema"},
            )
        _stable_id(self.manifest_id, field="manifest_id", phase="construct")
        if (
            type(self.entries) is not tuple
            or not self.entries
            or any(type(entry) is not SourceManifestEntry for entry in self.entries)
        ):
            raise _manifest_error(
                "source manifest entries must be a nonempty tuple of exact entries",
                code="source_manifest.invalid_document",
                phase="construct",
                details={"field": "entries"},
            )
        if len(self.entries) > _MAX_ENTRIES:
            raise _manifest_error(
                "source manifest entry count is outside its bounds",
                code="source_manifest.limit_exceeded",
                phase="construct",
                details={
                    "field": "entries",
                    "actual": len(self.entries),
                    "limit": _MAX_ENTRIES,
                },
            )
        entry_ids = tuple(entry.entry_id for entry in self.entries)
        if len(set(entry_ids)) != len(entry_ids):
            raise _manifest_error(
                "source manifest entry IDs must be unique",
                code="source_manifest.duplicate_entry_id",
                phase="construct",
                details={"field": "entry_id"},
            )
        references = tuple((entry.kind, entry.source, entry.instance) for entry in self.entries)
        if len(set(references)) != len(references):
            raise _manifest_error(
                "source manifest repeats an exact source reference",
                code="source_manifest.duplicate_source",
                phase="construct",
                details={"field": "entries"},
            )
        object.__setattr__(
            self, "entries", tuple(sorted(self.entries, key=lambda item: item.entry_id))
        )

    @classmethod
    def from_json(
        cls,
        document: str | bytes,
        *,
        limits: SourceManifestLimits = DEFAULT_SOURCE_MANIFEST_LIMITS,
    ) -> SourceManifest:
        """Decode one bounded canonical-JSON source manifest."""

        checked_limits = _require_limits(limits)
        try:
            value = canonical_loads(document, limits=checked_limits.json_limits())
        except LudoWeaveError as error:
            raise _manifest_error(
                "source manifest JSON could not be decoded canonically",
                code="source_manifest.invalid_json",
                phase="decode",
                details={"cause_code": error.code},
            ) from error
        root = _object(value, role="manifest")
        _exact_fields(
            root,
            required={"$schema", "manifest_id", "entries"},
            role="manifest",
        )
        protocol = _text(root["$schema"], field="$schema")
        if protocol != SOURCE_MANIFEST_PROTOCOL:
            raise _manifest_error(
                "source manifest protocol is unsupported",
                code="source_manifest.incompatible_protocol",
                phase="decode",
                details={"field": "$schema"},
            )
        manifest_id = _stable_id(root["manifest_id"], field="manifest_id", phase="decode")
        raw_entries = root["entries"]
        if not isinstance(raw_entries, list):
            raise _field_error("entries", raw_entries, "array")
        items = cast(list[object], raw_entries)
        if not items or len(items) > checked_limits.max_entries:
            raise _manifest_error(
                "source manifest entry count is outside its bounds",
                code="source_manifest.limit_exceeded",
                phase="decode",
                details={
                    "field": "entries",
                    "actual": len(items),
                    "limit": checked_limits.max_entries,
                },
            )
        entries = tuple(_entry(item, limits=checked_limits) for item in items)
        return cls(manifest_id=manifest_id, entries=entries, protocol=protocol)

    def as_dict(self) -> dict[str, JsonValue]:
        """Return a detached ordinary JSON representation."""

        return {
            "$schema": self.protocol,
            "manifest_id": self.manifest_id,
            "entries": [entry.as_dict() for entry in self.entries],
        }

    def canonical_bytes(self) -> bytes:
        """Return deterministic canonical bytes for hashing and persistence."""

        try:
            return canonical_dumps(
                self.as_dict(),
                limits=DEFAULT_SOURCE_MANIFEST_LIMITS.json_limits(),
            )
        except LudoWeaveError as error:
            raise _manifest_error(
                "source manifest could not be encoded within canonical limits",
                code="source_manifest.invalid_document",
                phase="encode",
                details={"cause_code": error.code},
            ) from error


def _entry(value: object, *, limits: SourceManifestLimits) -> SourceManifestEntry:
    document = _object(value, role="entry")
    common = {"entry_id", "kind", "source"}
    kind = _text(document.get("kind"), field="kind")
    if kind not in ("scene", "prefab"):
        raise _manifest_error(
            "source manifest entry kind is unsupported",
            code="source_manifest.invalid_entry",
            phase="decode",
            details={"field": "kind"},
        )
    required = common if kind == "scene" else common | {"instance"}
    _exact_fields(document, required=required, role="entry")
    entry_id = _stable_id(document["entry_id"], field="entry_id", phase="decode")
    source = _portable_relative_path(
        document["source"],
        field="source",
        entry_id=entry_id,
        max_bytes=limits.max_path_bytes,
        phase="decode",
    )
    instance: str | None = None
    if kind == "prefab":
        instance = _portable_relative_path(
            document["instance"],
            field="instance",
            entry_id=entry_id,
            max_bytes=limits.max_path_bytes,
            phase="decode",
        )
    return SourceManifestEntry(
        entry_id=entry_id,
        kind=kind,
        source=source,
        instance=instance,
    )


def _portable_relative_path(
    value: object,
    *,
    field: str,
    entry_id: str,
    max_bytes: int,
    phase: str,
) -> str:
    if type(value) is not str or not value or "\x00" in value or "\\" in value:
        raise _invalid_path(field=field, entry_id=entry_id, phase=phase)
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError as error:
        raise _invalid_path(field=field, entry_id=entry_id, phase=phase) from error
    pure = PurePosixPath(value)
    windows = PureWindowsPath(value)
    parts = value.split("/")
    has_nonportable_part = any(
        ":" in part
        or part.endswith((" ", "."))
        or part.rstrip(" .").partition(".")[0].upper() in _WINDOWS_RESERVED
        for part in parts
    )
    if (
        size > max_bytes
        or pure.is_absolute()
        or windows.is_absolute()
        or windows.drive
        or any(part in ("", ".", "..") for part in parts)
        or has_nonportable_part
        or pure.as_posix() != value
    ):
        raise _invalid_path(field=field, entry_id=entry_id, phase=phase)
    return value


def _require_limits(value: object) -> SourceManifestLimits:
    if type(value) is not SourceManifestLimits:
        raise _manifest_error(
            "source manifest limits must be an exact SourceManifestLimits value",
            code="source_manifest.invalid_limits",
            phase="configure",
            details={"actual_type": type(value).__name__},
        )
    return value


def _object(value: object, *, role: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise _manifest_error(
            "source manifest value must be an object",
            code="source_manifest.invalid_document",
            phase="decode",
            details={"role": role, "actual_type": type(value).__name__},
        )
    return cast(dict[str, object], value)


def _exact_fields(value: Mapping[str, object], *, required: set[str], role: str) -> None:
    missing = sorted(required - value.keys())
    unexpected = sorted(value.keys() - required)
    if missing or unexpected:
        raise _manifest_error(
            "source manifest fields do not match the schema",
            code="source_manifest.invalid_document",
            phase="decode",
            details={
                "role": role,
                "missing": ",".join(missing),
                "unexpected": ",".join(unexpected),
            },
        )


def _text(value: object, *, field: str) -> str:
    if type(value) is not str:
        raise _field_error(field, value, "string")
    return value


def _stable_id(value: object, *, field: str, phase: str) -> str:
    if type(value) is not str or _STABLE_ID.fullmatch(value) is None:
        raise _manifest_error(
            "source manifest identity must use bounded stable text",
            code="source_manifest.invalid_identity",
            phase=phase,
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _invalid_path(*, field: str, entry_id: str, phase: str) -> SceneError:
    return _manifest_error(
        "source manifest path must be normalized project-relative portable text",
        code="source_manifest.invalid_path",
        phase=phase,
        details={"entry_id": entry_id, "field": field},
    )


def _field_error(field: str, value: object, expected: str) -> SceneError:
    return _manifest_error(
        "source manifest field has an invalid type",
        code="source_manifest.invalid_document",
        phase="decode",
        details={
            "field": field,
            "expected": expected,
            "actual_type": type(value).__name__,
        },
    )


def _manifest_error(
    message: str,
    *,
    code: str,
    phase: str,
    details: Mapping[str, str | int | float | bool | None],
) -> SceneError:
    return SceneError(
        message,
        code=code,
        subsystem="scene",
        phase=phase,
        details=details,
    )
