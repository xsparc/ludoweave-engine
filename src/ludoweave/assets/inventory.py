"""Bounded deterministic read-only inventory of one local asset cache."""

from __future__ import annotations

import json
import os
import re
import stat
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import cast

from ludoweave.assets.cache import (
    ASSET_CACHE_ENTRY_PROTOCOL,
    AssetCacheError,
    AssetCacheStore,
)
from ludoweave.assets.execution import (
    ASSET_BUILD_ARTIFACT_MAX_BYTES,
    AssetBuildResultEntry,
)
from ludoweave.assets.pipeline import ASSET_LOADER_PROTOCOL, AssetError, AssetKind, AssetUri
from ludoweave.assets.plans import AssetBuildPlan

ASSET_CACHE_INVENTORY_PROTOCOL = "ludoweave.asset-cache-inventory/1"
ASSET_CACHE_FINGERPRINT_PROTOCOL = "ludoweave.asset-cache-fingerprint/1"
ASSET_CACHE_INVENTORY_MAX_ACTIONS = 16_384
ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS = 16_384
ASSET_CACHE_INVENTORY_MAX_METADATA_BYTES = 64 * 1024 * 1024
ASSET_CACHE_INVENTORY_MAX_CAS_BYTES = ASSET_BUILD_ARTIFACT_MAX_BYTES

_METADATA_FILE = "entry.json"
_METADATA_MAX_BYTES = 65_536
_READ_CHUNK_BYTES = 1024 * 1024
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
_SHARD = re.compile(r"[0-9a-f]{2}\Z")
_STAT_REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)


@dataclass(frozen=True, slots=True)
class AssetCacheInventoryLimits:
    """Tightening-only limits for one complete local-cache inventory."""

    max_actions: int = ASSET_CACHE_INVENTORY_MAX_ACTIONS
    max_cas_blobs: int = ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS
    max_metadata_bytes: int = ASSET_CACHE_INVENTORY_MAX_METADATA_BYTES
    max_cas_bytes: int = ASSET_CACHE_INVENTORY_MAX_CAS_BYTES

    def __post_init__(self) -> None:
        for field, maximum in (
            ("max_actions", ASSET_CACHE_INVENTORY_MAX_ACTIONS),
            ("max_cas_blobs", ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS),
            ("max_metadata_bytes", ASSET_CACHE_INVENTORY_MAX_METADATA_BYTES),
            ("max_cas_bytes", ASSET_CACHE_INVENTORY_MAX_CAS_BYTES),
        ):
            value = getattr(self, field)
            if type(value) is not int or value <= 0:
                raise _inventory_error(
                    "asset cache inventory limits require exact positive integers",
                    code="asset_cache.invalid_inventory_limits",
                    phase="configure",
                    details={"field": field, "actual_type": type(value).__name__},
                )
            if value > maximum:
                raise _inventory_error(
                    "asset cache inventory limits may only tighten hard maxima",
                    code="asset_cache.invalid_inventory_limits",
                    phase="configure",
                    details={"field": field, "actual": value, "maximum": maximum},
                )


DEFAULT_ASSET_CACHE_INVENTORY_LIMITS = AssetCacheInventoryLimits()


@dataclass(frozen=True, slots=True)
class AssetCacheInventory:
    """Path-free current-plan and whole-cache integrity evidence."""

    plan_sha256: str
    current_actions: int
    missing_actions: int
    other_actions: int
    current_action_metadata_bytes: int
    other_action_metadata_bytes: int
    cas_blobs: int
    current_blobs: int
    other_blobs: int
    current_blob_bytes: int
    other_blob_bytes: int
    unreferenced_blobs: int
    unreferenced_blob_bytes: int
    protocol: str = ASSET_CACHE_INVENTORY_PROTOCOL

    def __post_init__(self) -> None:
        values = (
            self.current_actions,
            self.missing_actions,
            self.other_actions,
            self.current_action_metadata_bytes,
            self.other_action_metadata_bytes,
            self.cas_blobs,
            self.current_blobs,
            self.other_blobs,
            self.current_blob_bytes,
            self.other_blob_bytes,
            self.unreferenced_blobs,
            self.unreferenced_blob_bytes,
        )
        if (
            type(self.protocol) is not str
            or self.protocol != ASSET_CACHE_INVENTORY_PROTOCOL
            or type(self.plan_sha256) is not str
            or _SHA256.fullmatch(self.plan_sha256) is None
            or any(type(value) is not int or value < 0 for value in values)
            or self.current_actions + self.other_actions > ASSET_CACHE_INVENTORY_MAX_ACTIONS
            or self.cas_blobs > ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS
            or self.current_blobs + self.other_blobs != self.cas_blobs
            or self.unreferenced_blobs > self.other_blobs
            or self.current_action_metadata_bytes + self.other_action_metadata_bytes
            > ASSET_CACHE_INVENTORY_MAX_METADATA_BYTES
            or self.current_blob_bytes + self.other_blob_bytes > ASSET_CACHE_INVENTORY_MAX_CAS_BYTES
            or self.unreferenced_blob_bytes > self.other_blob_bytes
        ):
            raise _inventory_error(
                "asset cache inventory report is invalid",
                code="asset_cache.invalid_inventory",
                phase="report",
                details={"field": "inventory"},
            )

    def as_dict(self) -> dict[str, object]:
        return {
            "$schema": self.protocol,
            "plan_sha256": self.plan_sha256,
            "current_actions": self.current_actions,
            "missing_actions": self.missing_actions,
            "other_actions": self.other_actions,
            "current_action_metadata_bytes": self.current_action_metadata_bytes,
            "other_action_metadata_bytes": self.other_action_metadata_bytes,
            "cas_blobs": self.cas_blobs,
            "current_blobs": self.current_blobs,
            "other_blobs": self.other_blobs,
            "current_blob_bytes": self.current_blob_bytes,
            "other_blob_bytes": self.other_blob_bytes,
            "unreferenced_blobs": self.unreferenced_blobs,
            "unreferenced_blob_bytes": self.unreferenced_blob_bytes,
        }

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.as_dict(),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")


@dataclass(frozen=True, slots=True)
class AssetCacheFingerprint:
    """Path-free digest of one verified sequential cache observation."""

    inventory: AssetCacheInventory
    observation_sha256: str
    protocol: str = ASSET_CACHE_FINGERPRINT_PROTOCOL

    def __post_init__(self) -> None:
        if (
            type(self.protocol) is not str
            or self.protocol != ASSET_CACHE_FINGERPRINT_PROTOCOL
            or type(self.inventory) is not AssetCacheInventory
            or type(self.observation_sha256) is not str
            or _SHA256.fullmatch(self.observation_sha256) is None
        ):
            raise _inventory_error(
                "asset cache fingerprint report is invalid",
                code="asset_cache.invalid_fingerprint",
                phase="report",
                details={"field": "fingerprint"},
            )

    def as_dict(self) -> dict[str, object]:
        return {
            "$schema": self.protocol,
            "observation_sha256": self.observation_sha256,
            "inventory": self.inventory.as_dict(),
        }

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.as_dict(),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")


@dataclass(frozen=True, slots=True)
class _StoredAction:
    result: AssetBuildResultEntry
    metadata_bytes: int


def inspect_asset_cache_inventory(
    plan: AssetBuildPlan,
    cache_root: Path,
    *,
    project_root: Path | None = None,
    limits: AssetCacheInventoryLimits = DEFAULT_ASSET_CACHE_INVENTORY_LIMITS,
) -> AssetCacheInventory:
    """Verify and classify one complete engine-owned local cache read-only."""

    current_keys, checked_limits, store, plan_sha256 = _prepare_observation(
        plan,
        cache_root,
        project_root=project_root,
        limits=limits,
    )
    actions, blobs = _observe_storage(store, limits=checked_limits)
    return _inventory_from_storage(
        plan,
        plan_sha256=plan_sha256,
        current_keys=current_keys,
        actions=actions,
        blobs=blobs,
    )


def fingerprint_asset_cache_observation(
    plan: AssetBuildPlan,
    cache_root: Path,
    *,
    project_root: Path | None = None,
    limits: AssetCacheInventoryLimits = DEFAULT_ASSET_CACHE_INVENTORY_LIMITS,
) -> AssetCacheFingerprint:
    """Digest one verified sequential cache observation without mutation."""

    current_keys, checked_limits, store, plan_sha256 = _prepare_observation(
        plan,
        cache_root,
        project_root=project_root,
        limits=limits,
    )
    actions, blobs = _observe_storage(store, limits=checked_limits)
    inventory = _inventory_from_storage(
        plan,
        plan_sha256=plan_sha256,
        current_keys=current_keys,
        actions=actions,
        blobs=blobs,
    )
    return AssetCacheFingerprint(
        inventory,
        observation_sha256=_observation_sha256(actions, blobs),
    )


def _prepare_observation(
    plan: AssetBuildPlan,
    cache_root: Path,
    *,
    project_root: Path | None,
    limits: AssetCacheInventoryLimits,
) -> tuple[set[str], AssetCacheInventoryLimits, AssetCacheStore, str]:

    if type(plan) is not AssetBuildPlan:
        raise _inventory_error(
            "asset cache inventory requires an exact build plan",
            code="asset_cache.invalid_inventory",
            phase="configure",
            details={"field": "plan"},
        )
    current_keys = {entry.cache_key for entry in plan.entries}
    if len(current_keys) != len(plan.entries):
        raise _inventory_error(
            "asset cache inventory requires distinct plan cache keys",
            code="asset_cache.invalid_inventory",
            phase="configure",
            details={"field": "plan_cache_keys"},
        )
    checked_limits = _require_limits(limits)
    store = AssetCacheStore(cache_root, project_root=project_root, writable=False)
    return (
        current_keys,
        checked_limits,
        store,
        f"sha256:{sha256(plan.canonical_bytes()).hexdigest()}",
    )


def _observe_storage(
    store: AssetCacheStore,
    *,
    limits: AssetCacheInventoryLimits,
) -> tuple[dict[str, _StoredAction], dict[str, int]]:
    if not store.root.exists():
        return {}, {}

    _require_root_layout(store.root)
    actions = _scan_actions(store.root / "actions", limits=limits)
    blobs = _scan_cas(store.root / "cas", limits=limits)
    _require_action_blobs(actions, blobs)
    return actions, blobs


def _inventory_from_storage(
    plan: AssetBuildPlan,
    *,
    plan_sha256: str,
    current_keys: set[str],
    actions: Mapping[str, _StoredAction],
    blobs: Mapping[str, int],
) -> AssetCacheInventory:

    current_actions = current_keys.intersection(actions)
    for entry in plan.entries:
        stored = actions.get(entry.cache_key)
        if stored is None:
            continue
        result = stored.result
        if (
            result.uri != entry.uri
            or result.kind is not entry.kind
            or result.source_bytes != entry.source_bytes
        ):
            raise _corrupt_inventory(field="current_action")

    current_digests = {actions[key].result.artifact_sha256 for key in current_actions}
    all_action_digests = {stored.result.artifact_sha256 for stored in actions.values()}
    other_digests = set(blobs).difference(current_digests)
    unreferenced_digests = set(blobs).difference(all_action_digests)
    other_action_keys = set(actions).difference(current_keys)
    return AssetCacheInventory(
        plan_sha256,
        current_actions=len(current_actions),
        missing_actions=len(current_keys.difference(actions)),
        other_actions=len(other_action_keys),
        current_action_metadata_bytes=sum(actions[key].metadata_bytes for key in current_actions),
        other_action_metadata_bytes=sum(actions[key].metadata_bytes for key in other_action_keys),
        cas_blobs=len(blobs),
        current_blobs=len(current_digests),
        other_blobs=len(other_digests),
        current_blob_bytes=sum(blobs[digest] for digest in current_digests),
        other_blob_bytes=sum(blobs[digest] for digest in other_digests),
        unreferenced_blobs=len(unreferenced_digests),
        unreferenced_blob_bytes=sum(blobs[digest] for digest in unreferenced_digests),
    )


def _observation_sha256(
    actions: Mapping[str, _StoredAction],
    blobs: Mapping[str, int],
) -> str:
    observed = sha256()
    observed.update(ASSET_CACHE_FINGERPRINT_PROTOCOL.encode("ascii"))
    observed.update(b"\0")
    for cache_key in sorted(actions):
        payload = _metadata_bytes(actions[cache_key].result)
        observed.update(b"A")
        observed.update(len(payload).to_bytes(8, "big"))
        observed.update(payload)
    for artifact_sha256 in sorted(blobs):
        payload = bytes.fromhex(artifact_sha256.removeprefix("sha256:")) + blobs[
            artifact_sha256
        ].to_bytes(8, "big")
        observed.update(b"C")
        observed.update(len(payload).to_bytes(8, "big"))
        observed.update(payload)
    return f"sha256:{observed.hexdigest()}"


def _require_root_layout(root: Path) -> None:
    _require_directory(root, field="cache_root")
    members = _bounded_members(root, field="cache_root", maximum=3)
    if {item.name for item in members} - {"actions", "cas"}:
        raise _layout_error(field="cache_root")
    for item in members:
        _require_directory(item, field="cache_root")


def _scan_actions(
    root: Path,
    *,
    limits: AssetCacheInventoryLimits,
) -> dict[str, _StoredAction]:
    if not _optional_directory(root, field="actions"):
        return {}
    actions: dict[str, _StoredAction] = {}
    metadata_bytes = 0
    for shard in _bounded_members(root, field="actions", maximum=256):
        if _SHARD.fullmatch(shard.name) is None:
            raise _layout_error(field="action_shard")
        _require_directory(shard, field="action_shard")
        for location in _limited_members(
            shard,
            field="action_shard",
            maximum=limits.max_actions - len(actions),
            total_before=len(actions),
            total_limit=limits.max_actions,
            limit_field="actions",
        ):
            if _DIGEST.fullmatch(location.name) is None or not location.name.startswith(shard.name):
                raise _layout_error(field="action_name")
            _require_directory(location, field="action")
            entry_members = _bounded_members(location, field="action", maximum=2)
            if len(entry_members) != 1 or entry_members[0].name != _METADATA_FILE:
                raise _layout_error(field="action_files")
            metadata = _read_regular(
                entry_members[0],
                maximum=_METADATA_MAX_BYTES,
                field="metadata",
                total_before=metadata_bytes,
                total_limit=limits.max_metadata_bytes,
                total_field="metadata_bytes",
            )
            metadata_bytes += len(metadata)
            result = _decode_metadata(metadata)
            if result.cache_key != f"sha256:{location.name}":
                raise _corrupt_inventory(field="action_key")
            actions[result.cache_key] = _StoredAction(result, len(metadata))
    return actions


def _scan_cas(
    root: Path,
    *,
    limits: AssetCacheInventoryLimits,
) -> dict[str, int]:
    if not _optional_directory(root, field="cas"):
        return {}
    blobs: dict[str, int] = {}
    total_bytes = 0
    for shard in _bounded_members(root, field="cas", maximum=256):
        if _SHARD.fullmatch(shard.name) is None:
            raise _layout_error(field="cas_shard")
        _require_directory(shard, field="cas_shard")
        for blob in _limited_members(
            shard,
            field="cas_shard",
            maximum=limits.max_cas_blobs - len(blobs),
            total_before=len(blobs),
            total_limit=limits.max_cas_blobs,
            limit_field="cas_blobs",
        ):
            if _DIGEST.fullmatch(blob.name) is None or not blob.name.startswith(shard.name):
                raise _layout_error(field="cas_name")
            size, observed = _hash_regular(
                blob,
                maximum=ASSET_BUILD_ARTIFACT_MAX_BYTES,
                total_before=total_bytes,
                total_limit=limits.max_cas_bytes,
            )
            total_bytes += size
            if observed != blob.name:
                raise _corrupt_inventory(field="cas_digest")
            blobs[f"sha256:{blob.name}"] = size
    return blobs


def _require_action_blobs(
    actions: Mapping[str, _StoredAction],
    blobs: Mapping[str, int],
) -> None:
    for stored in actions.values():
        result = stored.result
        if blobs.get(result.artifact_sha256) != result.artifact_bytes:
            raise _corrupt_inventory(field="action_blob")


def _decode_metadata(payload: bytes) -> AssetBuildResultEntry:
    try:
        decoded: object = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
        if type(decoded) is not dict:
            raise ValueError("metadata must be an object")
        document = cast(dict[str, object], decoded)
        if set(document) != {
            "$schema",
            "loader_protocol",
            "uri",
            "kind",
            "cache_key",
            "source_bytes",
            "artifact_sha256",
            "artifact_bytes",
        }:
            raise ValueError("metadata fields are invalid")
        if document["$schema"] != ASSET_CACHE_ENTRY_PROTOCOL:
            raise ValueError("metadata protocol is invalid")
        if document["loader_protocol"] != ASSET_LOADER_PROTOCOL:
            raise ValueError("metadata loader protocol is invalid")
        result = AssetBuildResultEntry(
            AssetUri(_text(document["uri"])),
            AssetKind(_text(document["kind"])),
            _text(document["cache_key"]),
            _integer(document["source_bytes"]),
            _text(document["artifact_sha256"]),
            _integer(document["artifact_bytes"]),
        )
    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
        ValueError,
        RecursionError,
        AssetError,
    ) as error:
        raise _corrupt_inventory(field="metadata") from error
    if payload != _metadata_bytes(result):
        raise _corrupt_inventory(field="metadata")
    return result


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


def _bounded_members(path: Path, *, field: str, maximum: int) -> tuple[Path, ...]:
    members: list[Path] = []
    for item in _iter_members(path, field=field):
        members.append(item)
        if len(members) > maximum:
            raise _layout_error(field=field)
    return tuple(sorted(members, key=lambda item: item.name))


def _limited_members(
    path: Path,
    *,
    field: str,
    maximum: int,
    total_before: int,
    total_limit: int,
    limit_field: str,
) -> tuple[Path, ...]:
    members: list[Path] = []
    for item in _iter_members(path, field=field):
        if len(members) >= maximum:
            raise _limit_error(
                field=limit_field,
                actual=total_before + len(members) + 1,
                limit=total_limit,
            )
        members.append(item)
    return tuple(sorted(members, key=lambda item: item.name))


def _iter_members(path: Path, *, field: str) -> Iterator[Path]:
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                yield Path(entry.path)
    except OSError as error:
        raise _layout_error(field=field, error=error) from error


def _optional_directory(path: Path, *, field: str) -> bool:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return False
    except OSError as error:
        raise _layout_error(field=field, error=error) from error
    if not stat.S_ISDIR(info.st_mode) or _is_reparse(info):
        raise _layout_error(field=field)
    return True


def _require_directory(path: Path, *, field: str) -> None:
    try:
        info = path.lstat()
    except OSError as error:
        raise _layout_error(field=field, error=error) from error
    if not stat.S_ISDIR(info.st_mode) or _is_reparse(info):
        raise _layout_error(field=field)


def _read_regular(
    path: Path,
    *,
    maximum: int,
    field: str,
    total_before: int,
    total_limit: int,
    total_field: str,
) -> bytes:
    try:
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or _is_reparse(info):
            raise _layout_error(field=field)
        if info.st_size > maximum:
            raise _limit_error(field=field, actual=info.st_size, limit=maximum)
        if total_before + info.st_size > total_limit:
            raise _limit_error(
                field=total_field,
                actual=total_before + info.st_size,
                limit=total_limit,
            )
        remaining = min(maximum, total_limit - total_before)
        with path.open("rb") as stream:
            payload = stream.read(remaining + 1)
    except AssetCacheError:
        raise
    except OSError as error:
        raise _layout_error(field=field, error=error) from error
    if len(payload) > maximum:
        raise _limit_error(field=field, actual=len(payload), limit=maximum)
    if total_before + len(payload) > total_limit:
        raise _limit_error(
            field=total_field,
            actual=total_before + len(payload),
            limit=total_limit,
        )
    if len(payload) != info.st_size:
        raise _inventory_changed(field=field)
    return payload


def _hash_regular(
    path: Path,
    *,
    maximum: int,
    total_before: int,
    total_limit: int,
) -> tuple[int, str]:
    try:
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or _is_reparse(info):
            raise _layout_error(field="cas_file")
        if info.st_size > maximum:
            raise _limit_error(field="cas_file", actual=info.st_size, limit=maximum)
        if total_before + info.st_size > total_limit:
            raise _limit_error(
                field="cas_bytes",
                actual=total_before + info.st_size,
                limit=total_limit,
            )
        digest = sha256()
        observed_bytes = 0
        with path.open("rb") as stream:
            while True:
                remaining = min(
                    maximum - observed_bytes,
                    total_limit - total_before - observed_bytes,
                )
                chunk = stream.read(min(_READ_CHUNK_BYTES, remaining + 1))
                if not chunk:
                    break
                observed_bytes += len(chunk)
                if observed_bytes > maximum:
                    raise _limit_error(
                        field="cas_file",
                        actual=observed_bytes,
                        limit=maximum,
                    )
                if total_before + observed_bytes > total_limit:
                    raise _limit_error(
                        field="cas_bytes",
                        actual=total_before + observed_bytes,
                        limit=total_limit,
                    )
                digest.update(chunk)
    except AssetCacheError:
        raise
    except OSError as error:
        raise _layout_error(field="cas_file", error=error) from error
    if observed_bytes != info.st_size:
        raise _inventory_changed(field="cas_file")
    return observed_bytes, digest.hexdigest()


def _is_reparse(info: os.stat_result) -> bool:
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & _STAT_REPARSE_POINT
    )


def _text(value: object) -> str:
    if type(value) is not str:
        raise ValueError("metadata text is invalid")
    return value


def _integer(value: object) -> int:
    if type(value) is not int:
        raise ValueError("metadata integer is invalid")
    return value


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    document: dict[str, object] = {}
    for key, value in pairs:
        if key in document:
            raise ValueError("duplicate cache metadata field")
        document[key] = value
    return document


def _reject_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant: {value}")


def _require_limits(limits: AssetCacheInventoryLimits) -> AssetCacheInventoryLimits:
    if type(limits) is not AssetCacheInventoryLimits:
        raise _inventory_error(
            "asset cache inventory requires exact limits",
            code="asset_cache.invalid_inventory_limits",
            phase="configure",
            details={"actual_type": type(limits).__name__},
        )
    return limits


def _limit_error(*, field: str, actual: int, limit: int) -> AssetCacheError:
    return _inventory_error(
        "asset cache inventory exceeds an active limit",
        code="asset_cache.inventory_limit_exceeded",
        phase="inspect",
        details={"field": field, "actual": actual, "limit": limit},
    )


def _layout_error(*, field: str, error: OSError | None = None) -> AssetCacheError:
    details: dict[str, str | int | float | bool | None] = {"field": field}
    if error is not None:
        details["cause_type"] = type(error).__name__
    return _inventory_error(
        "asset cache inventory layout is invalid",
        code="asset_cache.invalid_inventory_layout",
        phase="inspect",
        details=details,
    )


def _corrupt_inventory(*, field: str) -> AssetCacheError:
    return _inventory_error(
        "asset cache inventory failed content verification",
        code="asset_cache.corrupt_inventory",
        phase="inspect",
        details={"field": field},
    )


def _inventory_changed(*, field: str) -> AssetCacheError:
    return _inventory_error(
        "asset cache inventory changed during observation",
        code="asset_cache.inventory_changed",
        phase="inspect",
        details={"field": field},
    )


def _inventory_error(
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
