"""Bounded path-independent identities for selected asset source files."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast

from ludoweave.assets.pipeline import AssetError, AssetKind, AssetUri

ASSET_SOURCE_LOCK_PROTOCOL = "ludoweave.asset-source-lock/1"
ASSET_SOURCE_MAX_BYTES = 256 * 1024 * 1024
ASSET_SOURCE_TOTAL_MAX_BYTES = 1024 * 1024 * 1024

_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")
_MAX_LOCK_BYTES = 1024 * 1024
_MAX_ENTRIES = 4_096
_MAX_ROOTS = 4_096


@dataclass(frozen=True, slots=True)
class AssetSourceLockLimits:
    """Tightening-only decode limits for one asset-source lock."""

    max_bytes: int = _MAX_LOCK_BYTES
    max_entries: int = _MAX_ENTRIES
    max_roots: int = _MAX_ROOTS

    def __post_init__(self) -> None:
        for field, maximum in (
            ("max_bytes", _MAX_LOCK_BYTES),
            ("max_entries", _MAX_ENTRIES),
            ("max_roots", _MAX_ROOTS),
        ):
            value = getattr(self, field)
            if type(value) is not int or value <= 0:
                raise _lock_error(
                    "asset-source lock limits must be exact positive integers",
                    code="asset_source_lock.invalid_limits",
                    phase="configure",
                    details={"field": field, "actual_type": type(value).__name__},
                )
            if value > maximum:
                raise _lock_error(
                    "asset-source lock limits may tighten but not exceed hard maxima",
                    code="asset_source_lock.invalid_limits",
                    phase="configure",
                    details={"field": field, "actual": value, "maximum": maximum},
                )


DEFAULT_ASSET_SOURCE_LOCK_LIMITS = AssetSourceLockLimits()


@dataclass(frozen=True, slots=True)
class AssetSourceLockEntry:
    """One locked logical asset and its exact source-byte identity."""

    uri: AssetUri
    kind: AssetKind
    source_sha256: str
    source_bytes: int

    def __post_init__(self) -> None:
        if (
            type(self.uri) is not AssetUri
            or type(self.kind) is not AssetKind
            or type(self.source_sha256) is not str
            or _SHA256.fullmatch(self.source_sha256) is None
            or type(self.source_bytes) is not int
            or not 0 <= self.source_bytes <= ASSET_SOURCE_MAX_BYTES
        ):
            raise _lock_error(
                "asset-source lock entry contains invalid immutable identity",
                code="asset_source_lock.invalid_entry",
                phase="construct",
                details={"field": "entry"},
            )

    def as_dict(self) -> dict[str, object]:
        """Return a detached ordinary JSON representation."""

        return {
            "uri": self.uri.value,
            "kind": self.kind.value,
            "source_sha256": self.source_sha256,
            "source_bytes": self.source_bytes,
        }


@dataclass(frozen=True, slots=True)
class AssetSourceLock:
    """Normalized input identity for one selected asset dependency closure."""

    source_lock_sha256: str
    asset_manifest_sha256: str
    roots: tuple[AssetUri, ...]
    entries: tuple[AssetSourceLockEntry, ...]
    protocol: str = ASSET_SOURCE_LOCK_PROTOCOL

    def __post_init__(self) -> None:
        if type(self.protocol) is not str or self.protocol != ASSET_SOURCE_LOCK_PROTOCOL:
            raise _lock_error(
                "asset-source lock protocol is unsupported",
                code="asset_source_lock.incompatible_protocol",
                phase="construct",
                details={"field": "$schema"},
            )
        _require_sha256(self.source_lock_sha256, field="source_lock_sha256", phase="construct")
        _require_sha256(
            self.asset_manifest_sha256,
            field="asset_manifest_sha256",
            phase="construct",
        )
        if (
            type(self.roots) is not tuple
            or len(self.roots) > _MAX_ROOTS
            or any(type(root) is not AssetUri for root in self.roots)
            or len(set(self.roots)) != len(self.roots)
        ):
            raise _lock_error(
                "asset-source lock roots must be distinct exact logical URIs",
                code="asset_source_lock.invalid_roots",
                phase="construct",
                details={"field": "roots"},
            )
        if (
            type(self.entries) is not tuple
            or len(self.entries) > _MAX_ENTRIES
            or any(type(entry) is not AssetSourceLockEntry for entry in self.entries)
        ):
            raise _lock_error(
                "asset-source lock entries must be an exact bounded tuple",
                code="asset_source_lock.invalid_entries",
                phase="construct",
                details={"field": "entries"},
            )
        entry_uris = tuple(entry.uri for entry in self.entries)
        if len(set(entry_uris)) != len(entry_uris):
            raise _lock_error(
                "asset-source lock repeats a logical URI",
                code="asset_source_lock.duplicate_uri",
                phase="construct",
                details={"field": "uri"},
            )
        missing = tuple(sorted(root for root in self.roots if root not in entry_uris))
        if missing:
            raise _lock_error(
                "asset-source lock root is absent from locked entries",
                code="asset_source_lock.unknown_root",
                phase="construct",
                details={"uri": missing[0].value},
            )
        if not self.roots and self.entries:
            raise _lock_error(
                "asset-source lock without roots cannot contain entries",
                code="asset_source_lock.invalid_entries",
                phase="construct",
                details={"field": "entries"},
            )
        object.__setattr__(self, "roots", tuple(sorted(self.roots)))
        object.__setattr__(self, "entries", tuple(sorted(self.entries, key=lambda item: item.uri)))

    @classmethod
    def from_json(
        cls,
        document: str | bytes,
        *,
        limits: AssetSourceLockLimits = DEFAULT_ASSET_SOURCE_LOCK_LIMITS,
    ) -> AssetSourceLock:
        """Decode one bounded exact asset-source lock document."""

        checked_limits = _require_limits(limits)
        raw = _document_bytes(document, max_bytes=checked_limits.max_bytes)
        try:
            decoded: object = json.loads(
                raw.decode("utf-8"),
                object_pairs_hook=_unique_object,
                parse_float=_finite_float,
                parse_constant=_reject_constant,
            )
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError) as error:
            raise _lock_error(
                "asset-source lock JSON could not be decoded",
                code="asset_source_lock.invalid_json",
                phase="decode",
                details={"cause_type": type(error).__name__},
            ) from error
        root = _object(decoded, role="lock")
        _exact_fields(
            root,
            required={
                "$schema",
                "source_lock_sha256",
                "asset_manifest_sha256",
                "roots",
                "entries",
            },
            role="lock",
        )
        protocol = _text(root["$schema"], field="$schema")
        if protocol != ASSET_SOURCE_LOCK_PROTOCOL:
            raise _lock_error(
                "asset-source lock protocol is unsupported",
                code="asset_source_lock.incompatible_protocol",
                phase="decode",
                details={"field": "$schema"},
            )
        raw_roots = root["roots"]
        raw_entries = root["entries"]
        if type(raw_roots) is not list or type(raw_entries) is not list:
            raise _document_error(field="roots_or_entries")
        roots_list = cast(list[object], raw_roots)
        entries_list = cast(list[object], raw_entries)
        if len(roots_list) > checked_limits.max_roots:
            raise _limit_error(
                field="roots", actual=len(roots_list), limit=checked_limits.max_roots
            )
        if len(entries_list) > checked_limits.max_entries:
            raise _limit_error(
                field="entries", actual=len(entries_list), limit=checked_limits.max_entries
            )
        roots = tuple(AssetUri(_text(value, field="root")) for value in roots_list)
        entries = tuple(_entry(value) for value in entries_list)
        return cls(
            source_lock_sha256=_require_sha256(
                root["source_lock_sha256"], field="source_lock_sha256", phase="decode"
            ),
            asset_manifest_sha256=_require_sha256(
                root["asset_manifest_sha256"],
                field="asset_manifest_sha256",
                phase="decode",
            ),
            roots=roots,
            entries=entries,
            protocol=protocol,
        )

    def as_dict(self) -> dict[str, object]:
        """Return a detached normalized JSON-compatible representation."""

        return {
            "$schema": self.protocol,
            "source_lock_sha256": self.source_lock_sha256,
            "asset_manifest_sha256": self.asset_manifest_sha256,
            "roots": [root.value for root in self.roots],
            "entries": [entry.as_dict() for entry in self.entries],
        }

    def canonical_bytes(self) -> bytes:
        """Return deterministic normalized bytes for persistence or comparison."""

        encoded = json.dumps(
            self.as_dict(),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        if len(encoded) > _MAX_LOCK_BYTES:
            raise _limit_error(field="document", actual=len(encoded), limit=_MAX_LOCK_BYTES)
        return encoded

    def verify(self, actual: AssetSourceLock) -> None:
        """Require exact current identities without disclosing compared values."""

        if type(actual) is not AssetSourceLock:
            raise _lock_error(
                "asset-source lock verification requires an exact lock value",
                code="asset_source_lock.invalid_verify",
                phase="verify",
                details={"actual_type": type(actual).__name__},
            )
        for field in ("source_lock_sha256", "asset_manifest_sha256", "roots"):
            if getattr(self, field) != getattr(actual, field):
                raise _mismatch(field=field)
        expected_uris = tuple(entry.uri for entry in self.entries)
        actual_uris = tuple(entry.uri for entry in actual.entries)
        if expected_uris != actual_uris:
            raise _mismatch(field="entries")
        for expected, observed in zip(self.entries, actual.entries, strict=True):
            for field in ("kind", "source_sha256", "source_bytes"):
                if getattr(expected, field) != getattr(observed, field):
                    raise _mismatch(field=field, uri=expected.uri)


def _entry(value: object) -> AssetSourceLockEntry:
    document = _object(value, role="entry")
    _exact_fields(
        document,
        required={"uri", "kind", "source_sha256", "source_bytes"},
        role="entry",
    )
    try:
        kind = AssetKind(_text(document["kind"], field="kind"))
    except ValueError as error:
        raise _document_error(field="kind") from error
    return AssetSourceLockEntry(
        uri=AssetUri(_text(document["uri"], field="uri")),
        kind=kind,
        source_sha256=_require_sha256(
            document["source_sha256"], field="source_sha256", phase="decode"
        ),
        source_bytes=_integer(document["source_bytes"], field="source_bytes"),
    )


def _document_bytes(document: str | bytes, *, max_bytes: int) -> bytes:
    try:
        if type(document) is bytes:
            raw = document
        elif type(document) is str:
            raw = document.encode("utf-8")
        else:
            raise TypeError
    except (TypeError, UnicodeEncodeError) as error:
        raise _lock_error(
            "asset-source lock document must be UTF-8 text or bytes",
            code="asset_source_lock.invalid_json",
            phase="decode",
            details={"actual_type": type(document).__name__},
        ) from error
    if len(raw) > max_bytes:
        raise _limit_error(field="document", actual=len(raw), limit=max_bytes)
    return raw


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate object key")
        value[key] = item
    return value


def _finite_float(value: str) -> float:
    parsed = float(value)
    if not (-float("inf") < parsed < float("inf")):
        raise ValueError("non-finite number")
    return parsed


def _reject_constant(value: str) -> object:
    raise ValueError(f"unsupported JSON constant: {value}")


def _require_limits(value: object) -> AssetSourceLockLimits:
    if type(value) is not AssetSourceLockLimits:
        raise _lock_error(
            "asset-source lock limits must be an exact limits value",
            code="asset_source_lock.invalid_limits",
            phase="configure",
            details={"actual_type": type(value).__name__},
        )
    return value


def _object(value: object, *, role: str) -> dict[str, object]:
    if type(value) is not dict:
        raise _document_error(field=role)
    return cast(dict[str, object], value)


def _exact_fields(value: Mapping[str, object], *, required: set[str], role: str) -> None:
    if set(value) != required:
        raise _lock_error(
            "asset-source lock fields do not match the exact schema",
            code="asset_source_lock.invalid_document",
            phase="decode",
            details={"role": role},
        )


def _text(value: object, *, field: str) -> str:
    if type(value) is not str:
        raise _document_error(field=field)
    try:
        if len(value.encode("utf-8")) > 4_096:
            raise UnicodeEncodeError("utf-8", value, 0, len(value), "text is oversized")
    except UnicodeEncodeError as error:
        raise _document_error(field=field) from error
    return value


def _integer(value: object, *, field: str) -> int:
    if type(value) is not int:
        raise _document_error(field=field)
    return value


def _require_sha256(value: object, *, field: str, phase: str) -> str:
    if type(value) is not str or _SHA256.fullmatch(value) is None:
        raise _lock_error(
            "asset-source lock hash must use lowercase SHA-256 identity text",
            code="asset_source_lock.invalid_hash",
            phase=phase,
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def _limit_error(*, field: str, actual: int, limit: int) -> AssetError:
    return _lock_error(
        "asset-source lock exceeds its configured limit",
        code="asset_source_lock.limit_exceeded",
        phase="decode",
        details={"field": field, "actual": actual, "limit": limit},
    )


def _document_error(*, field: str) -> AssetError:
    return _lock_error(
        "asset-source lock document contains an invalid field",
        code="asset_source_lock.invalid_document",
        phase="decode",
        details={"field": field},
    )


def _mismatch(*, field: str, uri: AssetUri | None = None) -> AssetError:
    details: dict[str, str | int | float | bool | None] = {"field": field}
    if uri is not None:
        details["uri"] = uri.value
    return _lock_error(
        "current asset source identities do not match the expected lock",
        code="asset_source_lock.mismatch",
        phase="verify",
        details=details,
    )


def _lock_error(
    message: str,
    *,
    code: str,
    phase: str,
    details: Mapping[str, str | int | float | bool | None],
) -> AssetError:
    return AssetError(
        message,
        code=code,
        subsystem="assets",
        phase=phase,
        details=details,
    )
