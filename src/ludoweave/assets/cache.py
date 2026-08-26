"""Verified atomic local cache storage for materialized asset artifacts."""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import cast

from ludoweave.assets.execution import (
    ASSET_BUILD_ARTIFACT_MAX_BYTES,
    AssetBuildArtifact,
    AssetBuildMaterialization,
    AssetBuildResultEntry,
)
from ludoweave.assets.pipeline import (
    ASSET_LOADER_PROTOCOL,
    AssetError,
    AssetKind,
    AssetUri,
)
from ludoweave.assets.plans import AssetBuildPlan, AssetBuildPlanEntry

ASSET_CACHE_ENTRY_PROTOCOL = "ludoweave.asset-cache-entry/1"
ASSET_CACHE_LOOKUP_PROTOCOL = "ludoweave.asset-cache-lookup/1"
ASSET_CACHE_PUBLISH_PROTOCOL = "ludoweave.asset-cache-publish/1"

_METADATA_FILE = "entry.json"
_METADATA_MAX_BYTES = 65_536
_REPORT_MAX_BYTES = 8 * 1024 * 1024
_ENTRY_FILES = frozenset((_METADATA_FILE,))
_STAT_REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")


class AssetCacheError(AssetError):
    """Raised when local cache authority, integrity, or publication fails."""


@dataclass(frozen=True, slots=True)
class AssetCachePublishEntry:
    """Path-free publication status for one content-addressed artifact."""

    uri: AssetUri
    cache_key: str
    artifact_sha256: str
    artifact_bytes: int
    status: str

    def __post_init__(self) -> None:
        if (
            type(self.uri) is not AssetUri
            or type(self.cache_key) is not str
            or _SHA256.fullmatch(self.cache_key) is None
            or type(self.artifact_sha256) is not str
            or _SHA256.fullmatch(self.artifact_sha256) is None
            or type(self.artifact_bytes) is not int
            or not 0 <= self.artifact_bytes <= ASSET_BUILD_ARTIFACT_MAX_BYTES
            or type(self.status) is not str
            or self.status not in {"published", "reused"}
        ):
            raise _cache_error(
                "asset cache publication entry is invalid",
                code="asset_cache.invalid_summary",
                phase="report",
                details={"field": "entry"},
            )

    def as_dict(self) -> dict[str, object]:
        return {
            "uri": self.uri.value,
            "cache_key": self.cache_key,
            "artifact_sha256": self.artifact_sha256,
            "artifact_bytes": self.artifact_bytes,
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class AssetCachePublishSummary:
    """Deterministic result of complete local cache publication."""

    plan_sha256: str
    entries: tuple[AssetCachePublishEntry, ...]
    protocol: str = ASSET_CACHE_PUBLISH_PROTOCOL

    def __post_init__(self) -> None:
        if (
            type(self.protocol) is not str
            or self.protocol != ASSET_CACHE_PUBLISH_PROTOCOL
            or type(self.plan_sha256) is not str
            or _SHA256.fullmatch(self.plan_sha256) is None
            or type(self.entries) is not tuple
            or any(type(entry) is not AssetCachePublishEntry for entry in self.entries)
            or len({entry.uri for entry in self.entries}) != len(self.entries)
        ):
            raise _cache_error(
                "asset cache publication summary is invalid",
                code="asset_cache.invalid_summary",
                phase="report",
                details={"field": "summary"},
            )

    @property
    def published(self) -> int:
        return sum(entry.status == "published" for entry in self.entries)

    @property
    def reused(self) -> int:
        return sum(entry.status == "reused" for entry in self.entries)

    def as_dict(self) -> dict[str, object]:
        return {
            "$schema": self.protocol,
            "plan_sha256": self.plan_sha256,
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
        if len(encoded) > _REPORT_MAX_BYTES:
            raise _cache_error(
                "asset cache publication report exceeds its byte bound",
                code="asset_cache.invalid_summary",
                phase="report",
                details={"field": "report_bytes"},
            )
        return encoded


@dataclass(frozen=True, slots=True)
class AssetCacheLookupEntry:
    """Path-free verified hit or exact miss for one planned action."""

    uri: AssetUri
    cache_key: str
    status: str
    artifact_sha256: str | None = None
    artifact_bytes: int | None = None

    def __post_init__(self) -> None:
        hit = self.status == "hit"
        if (
            type(self.uri) is not AssetUri
            or type(self.cache_key) is not str
            or _SHA256.fullmatch(self.cache_key) is None
            or type(self.status) is not str
            or self.status not in {"hit", "miss"}
            or (
                hit
                and (
                    type(self.artifact_sha256) is not str
                    or _SHA256.fullmatch(self.artifact_sha256) is None
                    or type(self.artifact_bytes) is not int
                    or not 0 <= self.artifact_bytes <= ASSET_BUILD_ARTIFACT_MAX_BYTES
                )
            )
            or (not hit and (self.artifact_sha256 is not None or self.artifact_bytes is not None))
        ):
            raise _cache_error(
                "asset cache lookup entry is invalid",
                code="asset_cache.invalid_summary",
                phase="report",
                details={"field": "entry"},
            )

    def as_dict(self) -> dict[str, object]:
        return {
            "uri": self.uri.value,
            "cache_key": self.cache_key,
            "status": self.status,
            "artifact_sha256": self.artifact_sha256,
            "artifact_bytes": self.artifact_bytes,
        }


@dataclass(frozen=True, slots=True)
class AssetCacheLookupSummary:
    """Deterministic read-only cache evidence for one exact current plan."""

    plan_sha256: str
    entries: tuple[AssetCacheLookupEntry, ...]
    protocol: str = ASSET_CACHE_LOOKUP_PROTOCOL

    def __post_init__(self) -> None:
        if (
            type(self.protocol) is not str
            or self.protocol != ASSET_CACHE_LOOKUP_PROTOCOL
            or type(self.plan_sha256) is not str
            or _SHA256.fullmatch(self.plan_sha256) is None
            or type(self.entries) is not tuple
            or any(type(entry) is not AssetCacheLookupEntry for entry in self.entries)
            or len({entry.uri for entry in self.entries}) != len(self.entries)
        ):
            raise _cache_error(
                "asset cache lookup summary is invalid",
                code="asset_cache.invalid_summary",
                phase="report",
                details={"field": "summary"},
            )

    @property
    def hits(self) -> int:
        return sum(entry.status == "hit" for entry in self.entries)

    @property
    def misses(self) -> int:
        return sum(entry.status == "miss" for entry in self.entries)

    def as_dict(self) -> dict[str, object]:
        return {
            "$schema": self.protocol,
            "plan_sha256": self.plan_sha256,
            "hits": self.hits,
            "misses": self.misses,
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
        if len(encoded) > _REPORT_MAX_BYTES:
            raise _cache_error(
                "asset cache lookup report exceeds its byte bound",
                code="asset_cache.invalid_summary",
                phase="report",
                details={"field": "report_bytes"},
            )
        return encoded


class AssetCacheStore:
    """Explicit local CAS root with verified reads and atomic entry publication."""

    __slots__ = ("_root", "_writable")

    def __init__(
        self,
        root: Path,
        *,
        project_root: Path | None = None,
        writable: bool = True,
    ) -> None:
        if type(writable) is not bool:
            raise _cache_error(
                "asset cache authority requires an exact boolean",
                code="asset_cache.invalid_authority",
                phase="configure",
                details={"field": "writable"},
            )
        root_value = _path(root)
        project_value = None if project_root is None else _path(project_root)
        try:
            root_info = root_value.lstat()
        except FileNotFoundError:
            root_info = None
        except OSError as error:
            raise _invalid_root() from error
        if root_info is not None and _is_reparse(root_info):
            raise _invalid_root()
        resolved = root_value.resolve(strict=False)
        if project_value is not None:
            project = project_value.resolve(strict=False)
            if (
                resolved == project
                or resolved.is_relative_to(project)
                or project.is_relative_to(resolved)
            ):
                raise _invalid_root()
        try:
            if writable:
                resolved.mkdir(parents=True, exist_ok=True)
            if resolved.exists():
                _require_directory(resolved, field="cache_root")
        except AssetCacheError:
            raise
        except OSError as error:
            raise _invalid_root() from error
        self._root = resolved
        self._writable = writable

    @property
    def root(self) -> Path:
        return self._root

    def load(self, entry: AssetBuildResultEntry) -> bytes | None:
        """Return one verified payload, or ``None`` for an exact cache miss."""

        if type(entry) is not AssetBuildResultEntry:
            raise _cache_error(
                "asset cache lookup requires an exact result entry",
                code="asset_cache.invalid_entry",
                phase="read",
                details={"field": "entry"},
            )
        location = self._entry_location(entry.cache_key)
        if location is None:
            return None
        return self._load_from_location(entry, location)

    def load_action(self, entry: AssetBuildPlanEntry) -> AssetBuildArtifact | None:
        """Load one verified action result for an exact current plan entry."""

        if type(entry) is not AssetBuildPlanEntry:
            raise _cache_error(
                "asset cache action lookup requires an exact plan entry",
                code="asset_cache.invalid_entry",
                phase="read",
                details={"field": "entry"},
            )
        location = self._entry_location(entry.cache_key)
        if location is None:
            return None
        _require_entry_files(location)
        metadata = _read_regular(location / _METADATA_FILE, maximum=_METADATA_MAX_BYTES)
        result_entry = _decode_metadata(metadata)
        if (
            result_entry.uri != entry.uri
            or result_entry.kind is not entry.kind
            or result_entry.cache_key != entry.cache_key
            or result_entry.source_bytes != entry.source_bytes
        ):
            raise _corrupt(field="metadata")
        payload = self._load_from_location(result_entry, location, metadata=metadata)
        return AssetBuildArtifact(result_entry, payload)

    def inspect(self, plan: AssetBuildPlan) -> AssetCacheLookupSummary:
        """Return plan-ordered verified hit/miss evidence without cache mutation."""

        if type(plan) is not AssetBuildPlan:
            raise _cache_error(
                "asset cache inspection requires an exact build plan",
                code="asset_cache.invalid_plan",
                phase="read",
                details={"field": "plan"},
            )
        entries: list[AssetCacheLookupEntry] = []
        for plan_entry in plan.entries:
            artifact = self.load_action(plan_entry)
            entries.append(
                AssetCacheLookupEntry(
                    uri=plan_entry.uri,
                    cache_key=plan_entry.cache_key,
                    status="miss" if artifact is None else "hit",
                    artifact_sha256=None if artifact is None else artifact.entry.artifact_sha256,
                    artifact_bytes=None if artifact is None else artifact.entry.artifact_bytes,
                )
            )
        return AssetCacheLookupSummary(
            f"sha256:{sha256(plan.canonical_bytes()).hexdigest()}",
            tuple(entries),
        )

    def _load_from_location(
        self,
        entry: AssetBuildResultEntry,
        location: Path,
        *,
        metadata: bytes | None = None,
    ) -> bytes:
        _require_entry_files(location)
        observed = (
            _read_regular(location / _METADATA_FILE, maximum=_METADATA_MAX_BYTES)
            if metadata is None
            else metadata
        )
        if observed != _metadata_bytes(entry):
            raise _corrupt(field="metadata")
        blob = self._blob_location(entry)
        if blob is None:
            raise _corrupt(field="blob")
        payload = _read_regular(blob, maximum=entry.artifact_bytes)
        if (
            len(payload) != entry.artifact_bytes
            or f"sha256:{sha256(payload).hexdigest()}" != entry.artifact_sha256
        ):
            raise _corrupt(field="payload")
        return payload

    def publish(self, materialized: AssetBuildMaterialization) -> AssetCachePublishSummary:
        """Verify or atomically publish every complete materialized entry."""

        if not self._writable:
            raise _cache_error(
                "asset cache was opened without write authority",
                code="asset_cache.read_only",
                phase="publish",
                details={"field": "writable"},
            )
        if type(materialized) is not AssetBuildMaterialization:
            raise _cache_error(
                "asset cache publication requires an exact materialization",
                code="asset_cache.invalid_materialization",
                phase="publish",
                details={"field": "materialization"},
            )
        published: list[AssetCachePublishEntry] = []
        for artifact in materialized.artifacts:
            status = self._publish_one(artifact.entry, artifact.payload)
            published.append(
                AssetCachePublishEntry(
                    uri=artifact.entry.uri,
                    cache_key=artifact.entry.cache_key,
                    artifact_sha256=artifact.entry.artifact_sha256,
                    artifact_bytes=artifact.entry.artifact_bytes,
                    status=status,
                )
            )
        return AssetCachePublishSummary(materialized.result.plan_sha256, tuple(published))

    def _publish_one(self, entry: AssetBuildResultEntry, payload: bytes) -> str:
        if self.load(entry) is not None:
            return "reused"
        self._publish_blob(entry, payload)
        self._publish_action(entry)
        if self.load(entry) is None:
            raise _corrupt(field="entry")
        return "published"

    def _publish_blob(self, entry: AssetBuildResultEntry, payload: bytes) -> None:
        digest = entry.artifact_sha256.removeprefix("sha256:")
        cas = _ensure_directory(self._root / "cas")
        shard = _ensure_directory(cas / digest[:2])
        final = shard / digest
        existing = _optional_regular(final)
        if existing is not None:
            if _read_regular(existing, maximum=entry.artifact_bytes) != payload:
                raise _corrupt(field="blob")
            return
        descriptor, temporary_name = tempfile.mkstemp(prefix=".staging-", dir=shard)
        staging = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            existing = _optional_regular(final)
            if existing is not None:
                if _read_regular(existing, maximum=entry.artifact_bytes) != payload:
                    raise _corrupt(field="blob")
                return
            try:
                os.replace(staging, final)
            except OSError as error:
                existing = _optional_regular(final)
                if existing is not None:
                    if _read_regular(existing, maximum=entry.artifact_bytes) != payload:
                        raise _corrupt(field="blob") from error
                    return
                raise _publish_failed(error) from error
            _fsync_directory(shard)
        except AssetCacheError:
            raise
        except OSError as error:
            raise _publish_failed(error) from error
        finally:
            if staging.exists():
                try:
                    staging.unlink()
                except OSError as error:
                    raise _publish_failed(error) from error

    def _publish_action(self, entry: AssetBuildResultEntry) -> None:
        digest = entry.cache_key.removeprefix("sha256:")
        actions = _ensure_directory(self._root / "actions")
        shard = _ensure_directory(actions / digest[:2])
        final = shard / digest
        staging = Path(tempfile.mkdtemp(prefix=".staging-", dir=shard))
        try:
            _write_durable(staging / _METADATA_FILE, _metadata_bytes(entry))
            _fsync_directory(staging)
            if final.exists():
                if self.load(entry) is None:
                    raise _corrupt(field="entry")
                return
            try:
                os.replace(staging, final)
            except OSError as error:
                if final.exists():
                    if self.load(entry) is None:
                        raise _corrupt(field="entry") from error
                    return
                raise _publish_failed(error) from error
            _fsync_directory(shard)
        except AssetCacheError:
            raise
        except OSError as error:
            raise _publish_failed(error) from error
        finally:
            if staging.exists():
                try:
                    shutil.rmtree(staging)
                except OSError as error:
                    raise _publish_failed(error) from error

    def _entry_location(self, cache_key: str) -> Path | None:
        digest = cache_key.removeprefix("sha256:")
        actions = _optional_directory(self._root / "actions")
        if actions is None:
            return None
        shard = _optional_directory(actions / digest[:2])
        if shard is None:
            return None
        return _optional_directory(shard / digest)

    def _blob_location(self, entry: AssetBuildResultEntry) -> Path | None:
        digest = entry.artifact_sha256.removeprefix("sha256:")
        cas = _optional_directory(self._root / "cas")
        if cas is None:
            return None
        shard = _optional_directory(cas / digest[:2])
        if shard is None:
            return None
        return _optional_regular(shard / digest)


def _metadata_bytes(entry: AssetBuildResultEntry) -> bytes:
    return json.dumps(
        {
            "$schema": ASSET_CACHE_ENTRY_PROTOCOL,
            "loader_protocol": ASSET_LOADER_PROTOCOL,
            **entry.as_dict(),
        },
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _decode_metadata(payload: bytes) -> AssetBuildResultEntry:
    try:
        decoded: object = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
        if type(decoded) is not dict:
            raise ValueError("metadata must be an object")
        untyped_document = cast(dict[object, object], decoded)
        if any(type(key) is not str for key in untyped_document):
            raise ValueError("metadata keys must be strings")
        document = cast(dict[str, object], decoded)
        expected_fields = {
            "$schema",
            "loader_protocol",
            "uri",
            "kind",
            "cache_key",
            "source_bytes",
            "artifact_sha256",
            "artifact_bytes",
        }
        if set(document) != expected_fields:
            raise ValueError("metadata fields differ")
        if document["$schema"] != ASSET_CACHE_ENTRY_PROTOCOL:
            raise ValueError("metadata protocol differs")
        if document["loader_protocol"] != ASSET_LOADER_PROTOCOL:
            raise ValueError("loader protocol differs")
        uri_value = document["uri"]
        kind_value = document["kind"]
        cache_key = document["cache_key"]
        source_bytes = document["source_bytes"]
        artifact_sha256 = document["artifact_sha256"]
        artifact_bytes = document["artifact_bytes"]
        if (
            type(uri_value) is not str
            or type(kind_value) is not str
            or type(cache_key) is not str
            or type(source_bytes) is not int
            or type(artifact_sha256) is not str
            or type(artifact_bytes) is not int
        ):
            raise ValueError("metadata identity type differs")
        entry = AssetBuildResultEntry(
            uri=AssetUri(uri_value),
            kind=AssetKind(kind_value),
            cache_key=cache_key,
            source_bytes=source_bytes,
            artifact_sha256=artifact_sha256,
            artifact_bytes=artifact_bytes,
        )
    except (AssetError, UnicodeDecodeError, ValueError) as error:
        raise _corrupt(field="metadata") from error
    if payload != _metadata_bytes(entry):
        raise _corrupt(field="metadata")
    return entry


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    document: dict[str, object] = {}
    for key, value in pairs:
        if key in document:
            raise ValueError("duplicate metadata field")
        document[key] = value
    return document


def _reject_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant: {value}")


def _path(value: object) -> Path:
    if not isinstance(value, Path):
        raise _invalid_root()
    return value


def _optional_directory(path: Path) -> Path | None:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    except OSError as error:
        raise _corrupt(field="layout") from error
    if not stat.S_ISDIR(info.st_mode) or _is_reparse(info):
        raise _corrupt(field="layout")
    return path


def _optional_regular(path: Path) -> Path | None:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    except OSError as error:
        raise _corrupt(field="layout") from error
    if not stat.S_ISREG(info.st_mode) or _is_reparse(info):
        raise _corrupt(field="layout")
    return path


def _ensure_directory(path: Path) -> Path:
    try:
        path.mkdir(exist_ok=True)
        _require_directory(path, field="layout")
    except AssetCacheError:
        raise
    except OSError as error:
        raise _publish_failed(error) from error
    return path


def _require_directory(path: Path, *, field: str) -> None:
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or _is_reparse(info):
        if field == "cache_root":
            raise _invalid_root()
        raise _corrupt(field=field)


def _read_regular(path: Path, *, maximum: int) -> bytes:
    try:
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or _is_reparse(info):
            raise _corrupt(field="files")
        with path.open("rb") as stream:
            payload = stream.read(maximum + 1)
    except AssetCacheError:
        raise
    except OSError as error:
        raise _corrupt(field="files") from error
    if len(payload) > maximum:
        raise _corrupt(field="bytes")
    return payload


def _require_entry_files(location: Path) -> None:
    try:
        names = frozenset(path.name for path in location.iterdir())
    except OSError as error:
        raise _corrupt(field="files") from error
    if names != _ENTRY_FILES:
        raise _corrupt(field="files")


def _write_durable(path: Path, payload: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


def _fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _is_reparse(info: os.stat_result) -> bool:
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & _STAT_REPARSE_POINT
    )


def _invalid_root() -> AssetCacheError:
    return _cache_error(
        "asset cache root must be a distinct ordinary directory",
        code="asset_cache.invalid_root",
        phase="configure",
        details={"field": "cache_root"},
    )


def _corrupt(*, field: str) -> AssetCacheError:
    return _cache_error(
        "asset cache entry failed integrity verification",
        code="asset_cache.corrupt_entry",
        phase="read",
        details={"field": field},
    )


def _publish_failed(error: OSError) -> AssetCacheError:
    return _cache_error(
        "asset cache entry could not be published atomically",
        code="asset_cache.publish_failed",
        phase="publish",
        details={"field": "entry", "cause_type": type(error).__name__},
    )


def _cache_error(
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
