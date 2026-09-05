"""Bounded content-identity locks for explicit source manifests."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, cast

from ludoweave.core.errors import LudoWeaveError
from ludoweave.scene.document import SCENE_PROTOCOL
from ludoweave.scene.errors import SceneError
from ludoweave.scene.prefab import PREFAB_INSTANCE_PROTOCOL, PREFAB_PROTOCOL
from ludoweave.world.canonical import JsonLimits, JsonValue, canonical_dumps, canonical_loads

SOURCE_LOCK_PROTOCOL = "ludoweave.source-lock/1"

_STABLE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")
_MAX_BYTES = 65_536
_MAX_ENTRIES = 256
_MAX_DEPTH = 8
_MAX_NODES = 4_096
_MAX_COLLECTION_ITEMS = 1_024
_MAX_STRING_BYTES = 4_096


@dataclass(frozen=True, slots=True)
class SourceLockLimits:
    """Hard limits for one explicit source-integrity lock."""

    max_bytes: int = _MAX_BYTES
    max_entries: int = _MAX_ENTRIES

    def __post_init__(self) -> None:
        for field, maximum in (("max_bytes", _MAX_BYTES), ("max_entries", _MAX_ENTRIES)):
            value = getattr(self, field)
            if type(value) is not int or value <= 0:
                raise _lock_error(
                    "source lock limits must be exact positive integers",
                    code="source_lock.invalid_limits",
                    phase="configure",
                    details={"field": field, "actual_type": type(value).__name__},
                )
            if value > maximum:
                raise _lock_error(
                    "source lock limits may tighten but not exceed hard maxima",
                    code="source_lock.invalid_limits",
                    phase="configure",
                    details={"field": field, "actual": value, "maximum": maximum},
                )

    def json_limits(self) -> JsonLimits:
        """Return shared canonical-JSON limits for this lock."""

        return JsonLimits(
            max_bytes=self.max_bytes,
            max_depth=_MAX_DEPTH,
            max_nodes=_MAX_NODES,
            max_collection_items=_MAX_COLLECTION_ITEMS,
            max_string_bytes=_MAX_STRING_BYTES,
        )


DEFAULT_SOURCE_LOCK_LIMITS = SourceLockLimits()


@dataclass(frozen=True, slots=True)
class SourceLockEntry:
    """One path-independent locked scene or prefab source identity."""

    entry_id: str
    kind: Literal["scene", "prefab"]
    source_protocol: str
    source_id: str
    source_sha256: str
    instance_protocol: str | None = None
    instance_id: str | None = None
    instance_sha256: str | None = None

    def __post_init__(self) -> None:
        _stable_id(self.entry_id, field="entry_id", phase="construct")
        _stable_id(self.source_id, field="source_id", phase="construct")
        _sha256(self.source_sha256, field="source_sha256", phase="construct")
        if self.kind == "scene":
            if self.source_protocol != SCENE_PROTOCOL:
                raise _lock_error(
                    "source lock scene protocol is unsupported",
                    code="source_lock.invalid_entry",
                    phase="construct",
                    details={"entry_id": self.entry_id, "field": "source_protocol"},
                )
            if any(
                value is not None
                for value in (self.instance_protocol, self.instance_id, self.instance_sha256)
            ):
                raise _lock_error(
                    "source lock scene entries cannot contain instance identity",
                    code="source_lock.invalid_entry",
                    phase="construct",
                    details={"entry_id": self.entry_id, "field": "instance"},
                )
            return
        if self.kind != "prefab":
            raise _lock_error(
                "source lock entry kind is unsupported",
                code="source_lock.invalid_entry",
                phase="construct",
                details={"entry_id": self.entry_id, "field": "kind"},
            )
        if self.source_protocol != PREFAB_PROTOCOL:
            raise _lock_error(
                "source lock prefab protocol is unsupported",
                code="source_lock.invalid_entry",
                phase="construct",
                details={"entry_id": self.entry_id, "field": "source_protocol"},
            )
        if self.instance_protocol != PREFAB_INSTANCE_PROTOCOL:
            raise _lock_error(
                "source lock prefab instance protocol is unsupported",
                code="source_lock.invalid_entry",
                phase="construct",
                details={"entry_id": self.entry_id, "field": "instance_protocol"},
            )
        _stable_id(self.instance_id, field="instance_id", phase="construct")
        _sha256(self.instance_sha256, field="instance_sha256", phase="construct")

    def as_dict(self) -> dict[str, JsonValue]:
        """Return a detached ordinary JSON representation."""

        value: dict[str, JsonValue] = {
            "entry_id": self.entry_id,
            "kind": self.kind,
            "source_protocol": self.source_protocol,
            "source_id": self.source_id,
            "source_sha256": self.source_sha256,
        }
        if self.kind == "prefab":
            assert self.instance_protocol is not None
            assert self.instance_id is not None
            assert self.instance_sha256 is not None
            value.update(
                {
                    "instance_protocol": self.instance_protocol,
                    "instance_id": self.instance_id,
                    "instance_sha256": self.instance_sha256,
                }
            )
        return value


@dataclass(frozen=True, slots=True)
class SourceLock:
    """A normalized path-independent identity lock for one source manifest."""

    manifest_id: str
    manifest_sha256: str
    entries: tuple[SourceLockEntry, ...]
    protocol: str = SOURCE_LOCK_PROTOCOL

    def __post_init__(self) -> None:
        if type(self.protocol) is not str or self.protocol != SOURCE_LOCK_PROTOCOL:
            raise _lock_error(
                "source lock protocol is unsupported",
                code="source_lock.incompatible_protocol",
                phase="construct",
                details={"field": "$schema"},
            )
        _stable_id(self.manifest_id, field="manifest_id", phase="construct")
        _sha256(self.manifest_sha256, field="manifest_sha256", phase="construct")
        if (
            type(self.entries) is not tuple
            or not self.entries
            or any(type(entry) is not SourceLockEntry for entry in self.entries)
        ):
            raise _lock_error(
                "source lock entries must be a nonempty tuple of exact entries",
                code="source_lock.invalid_document",
                phase="construct",
                details={"field": "entries"},
            )
        if len(self.entries) > _MAX_ENTRIES:
            raise _lock_error(
                "source lock entry count is outside its bounds",
                code="source_lock.limit_exceeded",
                phase="construct",
                details={"field": "entries", "actual": len(self.entries), "limit": _MAX_ENTRIES},
            )
        entry_ids = tuple(entry.entry_id for entry in self.entries)
        if len(set(entry_ids)) != len(entry_ids):
            raise _lock_error(
                "source lock entry IDs must be unique",
                code="source_lock.duplicate_entry_id",
                phase="construct",
                details={"field": "entry_id"},
            )
        object.__setattr__(
            self, "entries", tuple(sorted(self.entries, key=lambda item: item.entry_id))
        )

    @classmethod
    def from_json(
        cls,
        document: str | bytes,
        *,
        limits: SourceLockLimits = DEFAULT_SOURCE_LOCK_LIMITS,
    ) -> SourceLock:
        """Decode one bounded canonical-JSON source lock."""

        checked_limits = _require_limits(limits)
        try:
            value = canonical_loads(document, limits=checked_limits.json_limits())
        except LudoWeaveError as error:
            raise _lock_error(
                "source lock JSON could not be decoded canonically",
                code="source_lock.invalid_json",
                phase="decode",
                details={"cause_code": error.code},
            ) from error
        root = _object(value, role="lock")
        _exact_fields(
            root,
            required={"$schema", "manifest_id", "manifest_sha256", "entries"},
            role="lock",
        )
        protocol = _text(root["$schema"], field="$schema")
        if protocol != SOURCE_LOCK_PROTOCOL:
            raise _lock_error(
                "source lock protocol is unsupported",
                code="source_lock.incompatible_protocol",
                phase="decode",
                details={"field": "$schema"},
            )
        manifest_id = _stable_id(root["manifest_id"], field="manifest_id", phase="decode")
        manifest_sha256 = _sha256(root["manifest_sha256"], field="manifest_sha256", phase="decode")
        raw_entries = root["entries"]
        if not isinstance(raw_entries, list):
            raise _field_error("entries", raw_entries, "array")
        items = cast(list[object], raw_entries)
        if not items or len(items) > checked_limits.max_entries:
            raise _lock_error(
                "source lock entry count is outside its bounds",
                code="source_lock.limit_exceeded",
                phase="decode",
                details={
                    "field": "entries",
                    "actual": len(items),
                    "limit": checked_limits.max_entries,
                },
            )
        entries = tuple(_entry(item) for item in items)
        return cls(manifest_id, manifest_sha256, entries, protocol)

    def as_dict(self) -> dict[str, JsonValue]:
        """Return a detached ordinary JSON representation."""

        return {
            "$schema": self.protocol,
            "manifest_id": self.manifest_id,
            "manifest_sha256": self.manifest_sha256,
            "entries": [entry.as_dict() for entry in self.entries],
        }

    def canonical_bytes(self) -> bytes:
        """Return deterministic canonical bytes for persistence or comparison."""

        try:
            return canonical_dumps(self.as_dict(), limits=DEFAULT_SOURCE_LOCK_LIMITS.json_limits())
        except LudoWeaveError as error:
            raise _lock_error(
                "source lock could not be encoded within canonical limits",
                code="source_lock.invalid_document",
                phase="encode",
                details={"cause_code": error.code},
            ) from error

    def verify(self, actual: SourceLock) -> None:
        """Require an exact current lock without disclosing content identities."""

        if type(actual) is not SourceLock:
            raise _lock_error(
                "source lock verification requires an exact SourceLock value",
                code="source_lock.invalid_verify",
                phase="verify",
                details={"actual_type": type(actual).__name__},
            )
        for field in ("manifest_id", "manifest_sha256"):
            if getattr(self, field) != getattr(actual, field):
                raise _mismatch(field=field)
        expected_ids = tuple(entry.entry_id for entry in self.entries)
        actual_ids = tuple(entry.entry_id for entry in actual.entries)
        if expected_ids != actual_ids:
            raise _mismatch(field="entries")
        for expected, observed in zip(self.entries, actual.entries, strict=True):
            for field in (
                "kind",
                "source_protocol",
                "source_id",
                "source_sha256",
                "instance_protocol",
                "instance_id",
                "instance_sha256",
            ):
                if getattr(expected, field) != getattr(observed, field):
                    raise _mismatch(field=field, entry_id=expected.entry_id)


def _entry(value: object) -> SourceLockEntry:
    document = _object(value, role="entry")
    kind = _text(document.get("kind"), field="kind")
    common = {"entry_id", "kind", "source_protocol", "source_id", "source_sha256"}
    if kind == "scene":
        required = common
    elif kind == "prefab":
        required = common | {"instance_protocol", "instance_id", "instance_sha256"}
    else:
        raise _lock_error(
            "source lock entry kind is unsupported",
            code="source_lock.invalid_entry",
            phase="decode",
            details={"field": "kind"},
        )
    _exact_fields(document, required=required, role="entry")
    entry_id = _stable_id(document["entry_id"], field="entry_id", phase="decode")
    return SourceLockEntry(
        entry_id=entry_id,
        kind=kind,
        source_protocol=_text(document["source_protocol"], field="source_protocol"),
        source_id=_stable_id(document["source_id"], field="source_id", phase="decode"),
        source_sha256=_sha256(document["source_sha256"], field="source_sha256", phase="decode"),
        instance_protocol=(
            None
            if kind == "scene"
            else _text(document["instance_protocol"], field="instance_protocol")
        ),
        instance_id=(
            None
            if kind == "scene"
            else _stable_id(document["instance_id"], field="instance_id", phase="decode")
        ),
        instance_sha256=(
            None
            if kind == "scene"
            else _sha256(document["instance_sha256"], field="instance_sha256", phase="decode")
        ),
    )


def _require_limits(value: object) -> SourceLockLimits:
    if type(value) is not SourceLockLimits:
        raise _lock_error(
            "source lock limits must be an exact SourceLockLimits value",
            code="source_lock.invalid_limits",
            phase="configure",
            details={"actual_type": type(value).__name__},
        )
    return value


def _object(value: object, *, role: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise _lock_error(
            "source lock value must be an object",
            code="source_lock.invalid_document",
            phase="decode",
            details={"role": role, "actual_type": type(value).__name__},
        )
    return cast(dict[str, object], value)


def _exact_fields(value: Mapping[str, object], *, required: set[str], role: str) -> None:
    missing = sorted(required - value.keys())
    unexpected = sorted(value.keys() - required)
    if missing or unexpected:
        raise _lock_error(
            "source lock fields do not match the schema",
            code="source_lock.invalid_document",
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
        raise _lock_error(
            "source lock identity must use bounded stable text",
            code="source_lock.invalid_identity",
            phase=phase,
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _sha256(value: object, *, field: str, phase: str) -> str:
    if type(value) is not str or _SHA256.fullmatch(value) is None:
        raise _lock_error(
            "source lock hash must use lowercase SHA-256 identity text",
            code="source_lock.invalid_hash",
            phase=phase,
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _field_error(field: str, value: object, expected: str) -> SceneError:
    return _lock_error(
        "source lock field has an invalid type",
        code="source_lock.invalid_document",
        phase="decode",
        details={"field": field, "expected": expected, "actual_type": type(value).__name__},
    )


def _mismatch(*, field: str, entry_id: str | None = None) -> SceneError:
    details: dict[str, str | int | float | bool | None] = {"field": field}
    if entry_id is not None:
        details["entry_id"] = entry_id
    return _lock_error(
        "current source identities do not match the expected lock",
        code="source_lock.mismatch",
        phase="verify",
        details=details,
    )


def _lock_error(
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
