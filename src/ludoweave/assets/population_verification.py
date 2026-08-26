"""Bounded saved population records and read-only current-cache verification."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import cast

from ludoweave.assets.cache import AssetCacheError, AssetCacheStore
from ludoweave.assets.execution import (
    ASSET_BUILD_ARTIFACT_TOTAL_MAX_BYTES,
    AssetBuildResultEntry,
)
from ludoweave.assets.locks import ASSET_SOURCE_TOTAL_MAX_BYTES
from ludoweave.assets.pipeline import ASSET_LOADER_PROTOCOL, AssetError, AssetKind, AssetUri
from ludoweave.assets.plans import AssetBuildPlan
from ludoweave.assets.population import ASSET_CACHE_POPULATION_PROTOCOL

ASSET_CACHE_POPULATION_RECORD_MAX_BYTES = 8 * 1024 * 1024
ASSET_CACHE_POPULATION_VERIFICATION_PROTOCOL = "ludoweave.asset-cache-population-verification/1"

_MAX_ENTRIES = 4_096
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")


@dataclass(frozen=True, slots=True)
class AssetCachePopulationRecordLimits:
    """Tightening-only bounds for one untrusted population report."""

    max_bytes: int = ASSET_CACHE_POPULATION_RECORD_MAX_BYTES
    max_entries: int = _MAX_ENTRIES

    def __post_init__(self) -> None:
        for field, maximum in (
            ("max_bytes", ASSET_CACHE_POPULATION_RECORD_MAX_BYTES),
            ("max_entries", _MAX_ENTRIES),
        ):
            value = getattr(self, field)
            if type(value) is not int or value <= 0:
                raise _record_error(
                    "asset cache population record limits require exact positive integers",
                    code="asset_cache.invalid_population_limits",
                    phase="configure",
                    details={"field": field, "actual_type": type(value).__name__},
                )
            if value > maximum:
                raise _record_error(
                    "asset cache population record limits may only tighten hard maxima",
                    code="asset_cache.invalid_population_limits",
                    phase="configure",
                    details={"field": field, "actual": value, "maximum": maximum},
                )


_DEFAULT_RECORD_LIMITS = AssetCachePopulationRecordLimits()


@dataclass(frozen=True, slots=True)
class AssetCachePopulationRecordEntry:
    """One detached result identity with historical population statuses."""

    result: AssetBuildResultEntry
    realization_status: str
    publication_status: str

    def __post_init__(self) -> None:
        if (
            type(self.result) is not AssetBuildResultEntry
            or type(self.realization_status) is not str
            or self.realization_status not in {"hit", "decoded"}
            or type(self.publication_status) is not str
            or self.publication_status not in {"published", "reused"}
        ):
            raise _record_error(
                "asset cache population record entry is invalid",
                code="asset_cache.invalid_population_record",
                phase="decode",
                details={"field": "entry"},
            )

    @property
    def uri(self) -> AssetUri:
        return self.result.uri

    def as_dict(self) -> dict[str, object]:
        return {
            **self.result.as_dict(),
            "realization_status": self.realization_status,
            "publication_status": self.publication_status,
        }


@dataclass(frozen=True, slots=True)
class AssetCachePopulationRecord:
    """Strict detached form of one saved M135 population report."""

    plan_sha256: str
    source_bytes: int
    artifact_bytes: int
    entries: tuple[AssetCachePopulationRecordEntry, ...]
    loader_protocol: str = ASSET_LOADER_PROTOCOL
    protocol: str = ASSET_CACHE_POPULATION_PROTOCOL

    def __post_init__(self) -> None:
        if (
            type(self.protocol) is not str
            or self.protocol != ASSET_CACHE_POPULATION_PROTOCOL
            or type(self.loader_protocol) is not str
            or self.loader_protocol != ASSET_LOADER_PROTOCOL
            or type(self.plan_sha256) is not str
            or _SHA256.fullmatch(self.plan_sha256) is None
            or type(self.source_bytes) is not int
            or not 0 <= self.source_bytes <= ASSET_SOURCE_TOTAL_MAX_BYTES
            or type(self.artifact_bytes) is not int
            or not 0 <= self.artifact_bytes <= ASSET_BUILD_ARTIFACT_TOTAL_MAX_BYTES
            or type(self.entries) is not tuple
            or len(self.entries) > _MAX_ENTRIES
            or any(type(entry) is not AssetCachePopulationRecordEntry for entry in self.entries)
            or len({entry.uri for entry in self.entries}) != len(self.entries)
            or sum(entry.result.source_bytes for entry in self.entries) != self.source_bytes
            or sum(entry.result.artifact_bytes for entry in self.entries) != self.artifact_bytes
        ):
            raise _record_error(
                "asset cache population record is invalid",
                code="asset_cache.invalid_population_record",
                phase="decode",
                details={"field": "population"},
            )

    @property
    def hits(self) -> int:
        return sum(entry.realization_status == "hit" for entry in self.entries)

    @property
    def decoded(self) -> int:
        return sum(entry.realization_status == "decoded" for entry in self.entries)

    @property
    def published(self) -> int:
        return sum(entry.publication_status == "published" for entry in self.entries)

    @property
    def reused(self) -> int:
        return sum(entry.publication_status == "reused" for entry in self.entries)

    @classmethod
    def from_json(
        cls,
        document: str | bytes,
        *,
        limits: AssetCachePopulationRecordLimits = _DEFAULT_RECORD_LIMITS,
    ) -> AssetCachePopulationRecord:
        """Decode one bounded exact-schema population report."""

        checked_limits = _require_limits(limits)
        raw = _document_bytes(document, maximum=checked_limits.max_bytes)
        try:
            decoded: object = json.loads(
                raw.decode("utf-8"),
                object_pairs_hook=_unique_object,
                parse_constant=_reject_constant,
            )
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError) as error:
            raise _record_error(
                "asset cache population record JSON could not be decoded",
                code="asset_cache.invalid_population_json",
                phase="decode",
                details={"cause_type": type(error).__name__},
            ) from error
        root = _object(decoded, field="population")
        _exact_fields(
            root,
            required={
                "$schema",
                "loader_protocol",
                "plan_sha256",
                "source_bytes",
                "artifact_bytes",
                "hits",
                "decoded",
                "published",
                "reused",
                "entries",
            },
            field="population",
        )
        raw_entries = root["entries"]
        if type(raw_entries) is not list:
            raise _invalid_document(field="entries")
        entry_values = cast(list[object], raw_entries)
        if len(entry_values) > checked_limits.max_entries:
            raise _record_error(
                "asset cache population record exceeds an active limit",
                code="asset_cache.population_limit_exceeded",
                phase="decode",
                details={
                    "field": "entries",
                    "actual": len(entry_values),
                    "limit": checked_limits.max_entries,
                },
            )
        try:
            entries = tuple(_entry(value) for value in entry_values)
        except AssetError as error:
            if error.code.startswith("asset_cache."):
                raise
            raise _invalid_document(field="entry") from error
        record = cls(
            plan_sha256=_text(root["plan_sha256"], field="plan_sha256"),
            source_bytes=_integer(root["source_bytes"], field="source_bytes"),
            artifact_bytes=_integer(root["artifact_bytes"], field="artifact_bytes"),
            entries=entries,
            loader_protocol=_text(root["loader_protocol"], field="loader_protocol"),
            protocol=_text(root["$schema"], field="$schema"),
        )
        for field, observed in (
            ("hits", record.hits),
            ("decoded", record.decoded),
            ("published", record.published),
            ("reused", record.reused),
        ):
            if _integer(root[field], field=field) != observed:
                raise _invalid_document(field=field)
        return record

    def as_dict(self) -> dict[str, object]:
        return {
            "$schema": self.protocol,
            "loader_protocol": self.loader_protocol,
            "plan_sha256": self.plan_sha256,
            "source_bytes": self.source_bytes,
            "artifact_bytes": self.artifact_bytes,
            "hits": self.hits,
            "decoded": self.decoded,
            "published": self.published,
            "reused": self.reused,
            "entries": [entry.as_dict() for entry in self.entries],
        }

    def canonical_bytes(self) -> bytes:
        encoded = json.dumps(
            self.as_dict(),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        if len(encoded) > ASSET_CACHE_POPULATION_RECORD_MAX_BYTES:
            raise _record_error(
                "asset cache population record exceeds its hard byte bound",
                code="asset_cache.population_limit_exceeded",
                phase="report",
                details={
                    "field": "document",
                    "actual": len(encoded),
                    "limit": ASSET_CACHE_POPULATION_RECORD_MAX_BYTES,
                },
            )
        return encoded


@dataclass(frozen=True, slots=True)
class AssetCachePopulationVerification:
    """Path-free proof that a saved population matches the current local cache."""

    plan_sha256: str
    entry_count: int
    population_protocol: str = ASSET_CACHE_POPULATION_PROTOCOL
    protocol: str = ASSET_CACHE_POPULATION_VERIFICATION_PROTOCOL

    def __post_init__(self) -> None:
        if (
            type(self.protocol) is not str
            or self.protocol != ASSET_CACHE_POPULATION_VERIFICATION_PROTOCOL
            or type(self.population_protocol) is not str
            or self.population_protocol != ASSET_CACHE_POPULATION_PROTOCOL
            or type(self.plan_sha256) is not str
            or _SHA256.fullmatch(self.plan_sha256) is None
            or type(self.entry_count) is not int
            or not 0 <= self.entry_count <= _MAX_ENTRIES
        ):
            raise _record_error(
                "asset cache population verification is invalid",
                code="asset_cache.invalid_population_verification",
                phase="report",
                details={"field": "verification"},
            )

    def as_dict(self) -> dict[str, object]:
        return {
            "$schema": self.protocol,
            "status": "valid",
            "population_protocol": self.population_protocol,
            "plan_sha256": self.plan_sha256,
            "entry_count": self.entry_count,
        }

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.as_dict(),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")


def verify_asset_cache_population(
    plan: AssetBuildPlan,
    population: AssetCachePopulationRecord,
    cache_root: Path,
    *,
    project_root: Path | None = None,
) -> AssetCachePopulationVerification:
    """Verify one saved population against the exact plan and current cache."""

    _preflight_population(plan, population)
    cache = AssetCacheStore(
        cache_root,
        project_root=project_root,
        writable=False,
    )
    for plan_entry, recorded in zip(plan.entries, population.entries, strict=True):
        artifact = cache.load_action(plan_entry)
        if artifact is None:
            raise _record_error(
                "saved asset cache population has no current cache action",
                code="asset_cache.population_miss",
                phase="verify",
                details={"uri": plan_entry.uri.value},
            )
        if artifact.entry != recorded.result:
            raise _mismatch(field="artifact", uri=plan_entry.uri)
    return AssetCachePopulationVerification(population.plan_sha256, len(population.entries))


def _preflight_population(
    plan: AssetBuildPlan,
    population: AssetCachePopulationRecord,
) -> None:
    if type(plan) is not AssetBuildPlan or type(population) is not AssetCachePopulationRecord:
        raise _record_error(
            "asset cache population verification requires exact values",
            code="asset_cache.invalid_population_verify",
            phase="configure",
            details={"field": "plan_or_population"},
        )
    plan_sha256 = f"sha256:{sha256(plan.canonical_bytes()).hexdigest()}"
    if population.plan_sha256 != plan_sha256:
        raise _mismatch(field="plan_sha256")
    if len(population.entries) != len(plan.entries):
        raise _mismatch(field="entries")
    for plan_entry, recorded in zip(plan.entries, population.entries, strict=True):
        result = recorded.result
        for field in ("uri", "kind", "cache_key", "source_bytes"):
            if getattr(result, field) != getattr(plan_entry, field):
                raise _mismatch(field=field, uri=plan_entry.uri)


def _entry(value: object) -> AssetCachePopulationRecordEntry:
    document = _object(value, field="entry")
    _exact_fields(
        document,
        required={
            "uri",
            "kind",
            "cache_key",
            "source_bytes",
            "artifact_sha256",
            "artifact_bytes",
            "realization_status",
            "publication_status",
        },
        field="entry",
    )
    try:
        result = AssetBuildResultEntry(
            uri=AssetUri(_text(document["uri"], field="uri")),
            kind=AssetKind(_text(document["kind"], field="kind")),
            cache_key=_text(document["cache_key"], field="cache_key"),
            source_bytes=_integer(document["source_bytes"], field="source_bytes"),
            artifact_sha256=_text(document["artifact_sha256"], field="artifact_sha256"),
            artifact_bytes=_integer(document["artifact_bytes"], field="artifact_bytes"),
        )
    except (AssetError, ValueError) as error:
        raise _invalid_document(field="entry") from error
    return AssetCachePopulationRecordEntry(
        result,
        _text(document["realization_status"], field="realization_status"),
        _text(document["publication_status"], field="publication_status"),
    )


def _document_bytes(document: str | bytes, *, maximum: int) -> bytes:
    if type(document) is str:
        raw = document.encode("utf-8")
    elif type(document) is bytes:
        raw = document
    else:
        raise _invalid_document(field="document")
    if len(raw) > maximum:
        raise _record_error(
            "asset cache population record exceeds an active limit",
            code="asset_cache.population_limit_exceeded",
            phase="decode",
            details={"field": "document", "actual": len(raw), "limit": maximum},
        )
    return raw


def _object(value: object, *, field: str) -> dict[str, object]:
    if type(value) is not dict:
        raise _invalid_document(field=field)
    untyped = cast(dict[object, object], value)
    if any(type(key) is not str for key in untyped):
        raise _invalid_document(field=field)
    return cast(dict[str, object], value)


def _exact_fields(
    value: dict[str, object],
    *,
    required: set[str],
    field: str,
) -> None:
    if set(value) != required:
        raise _invalid_document(field=field)


def _text(value: object, *, field: str) -> str:
    if type(value) is not str:
        raise _invalid_document(field=field)
    return value


def _integer(value: object, *, field: str) -> int:
    if type(value) is not int:
        raise _invalid_document(field=field)
    return value


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    document: dict[str, object] = {}
    for key, value in pairs:
        if key in document:
            raise ValueError("duplicate population record field")
        document[key] = value
    return document


def _reject_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant: {value}")


def _require_limits(
    limits: AssetCachePopulationRecordLimits,
) -> AssetCachePopulationRecordLimits:
    if type(limits) is not AssetCachePopulationRecordLimits:
        raise _record_error(
            "asset cache population record requires exact limits",
            code="asset_cache.invalid_population_limits",
            phase="configure",
            details={"actual_type": type(limits).__name__},
        )
    return limits


def _invalid_document(*, field: str) -> AssetCacheError:
    return _record_error(
        "asset cache population record is invalid",
        code="asset_cache.invalid_population_record",
        phase="decode",
        details={"field": field},
    )


def _mismatch(*, field: str, uri: AssetUri | None = None) -> AssetCacheError:
    details: dict[str, str | int | float | bool | None] = {"field": field}
    if uri is not None:
        details["uri"] = uri.value
    return _record_error(
        "saved asset cache population does not match current verified state",
        code="asset_cache.population_mismatch",
        phase="verify",
        details=details,
    )


def _record_error(
    message: str,
    *,
    code: str,
    phase: str,
    details: Mapping[str, str | int | float | bool | None],
) -> AssetCacheError:
    return AssetCacheError(
        message,
        code=code,
        subsystem="asset_cache",
        phase=phase,
        details=details,
    )
