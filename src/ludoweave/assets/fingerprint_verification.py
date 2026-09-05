"""Strict saved cache fingerprints and read-only observation verification."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import cast

from ludoweave.assets.cache import AssetCacheError
from ludoweave.assets.inventory import (
    ASSET_CACHE_FINGERPRINT_PROTOCOL,
    ASSET_CACHE_INVENTORY_MAX_ACTIONS,
    ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS,
    ASSET_CACHE_INVENTORY_MAX_CAS_BYTES,
    ASSET_CACHE_INVENTORY_MAX_METADATA_BYTES,
    DEFAULT_ASSET_CACHE_INVENTORY_LIMITS,
    AssetCacheFingerprint,
    AssetCacheInventory,
    AssetCacheInventoryLimits,
    fingerprint_asset_cache_observation,
)
from ludoweave.assets.plans import AssetBuildPlan

ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES = 65_536
ASSET_CACHE_FINGERPRINT_VERIFICATION_PROTOCOL = "ludoweave.asset-cache-fingerprint-verification/1"

_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")
_INVENTORY_FIELDS = {
    "$schema",
    "plan_sha256",
    "current_actions",
    "missing_actions",
    "other_actions",
    "current_action_metadata_bytes",
    "other_action_metadata_bytes",
    "cas_blobs",
    "current_blobs",
    "other_blobs",
    "current_blob_bytes",
    "other_blob_bytes",
    "unreferenced_blobs",
    "unreferenced_blob_bytes",
}


@dataclass(frozen=True, slots=True)
class AssetCacheFingerprintRecordLimits:
    """Tightening-only bounds for one untrusted saved fingerprint."""

    max_bytes: int = ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES

    def __post_init__(self) -> None:
        if type(self.max_bytes) is not int or self.max_bytes <= 0:
            raise _record_error(
                "asset cache fingerprint record limits require an exact positive integer",
                code="asset_cache.invalid_fingerprint_limits",
                phase="configure",
                details={"field": "max_bytes", "actual_type": type(self.max_bytes).__name__},
            )
        if self.max_bytes > ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES:
            raise _record_error(
                "asset cache fingerprint record limits may only tighten the hard maximum",
                code="asset_cache.invalid_fingerprint_limits",
                phase="configure",
                details={
                    "field": "max_bytes",
                    "actual": self.max_bytes,
                    "maximum": ASSET_CACHE_FINGERPRINT_RECORD_MAX_BYTES,
                },
            )


DEFAULT_ASSET_CACHE_FINGERPRINT_RECORD_LIMITS = AssetCacheFingerprintRecordLimits()


@dataclass(frozen=True, slots=True)
class AssetCacheFingerprintVerification:
    """Path-free equality proof for one saved and one current observation."""

    plan_sha256: str
    observation_sha256: str
    fingerprint_protocol: str = ASSET_CACHE_FINGERPRINT_PROTOCOL
    protocol: str = ASSET_CACHE_FINGERPRINT_VERIFICATION_PROTOCOL

    def __post_init__(self) -> None:
        if (
            type(self.protocol) is not str
            or self.protocol != ASSET_CACHE_FINGERPRINT_VERIFICATION_PROTOCOL
            or type(self.fingerprint_protocol) is not str
            or self.fingerprint_protocol != ASSET_CACHE_FINGERPRINT_PROTOCOL
            or type(self.plan_sha256) is not str
            or _SHA256.fullmatch(self.plan_sha256) is None
            or type(self.observation_sha256) is not str
            or _SHA256.fullmatch(self.observation_sha256) is None
        ):
            raise _record_error(
                "asset cache fingerprint verification is invalid",
                code="asset_cache.invalid_fingerprint_verification",
                phase="report",
                details={"field": "verification"},
            )

    def as_dict(self) -> dict[str, object]:
        return {
            "$schema": self.protocol,
            "status": "valid",
            "fingerprint_protocol": self.fingerprint_protocol,
            "plan_sha256": self.plan_sha256,
            "observation_sha256": self.observation_sha256,
        }

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.as_dict(),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")


def decode_asset_cache_fingerprint(
    document: str | bytes,
    *,
    limits: AssetCacheFingerprintRecordLimits = DEFAULT_ASSET_CACHE_FINGERPRINT_RECORD_LIMITS,
) -> AssetCacheFingerprint:
    """Decode one bounded, canonical, exact-schema fingerprint record."""

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
            "asset cache fingerprint record JSON could not be decoded",
            code="asset_cache.invalid_fingerprint_json",
            phase="decode",
            details={"cause_type": type(error).__name__},
        ) from error
    root = _object(decoded, field="fingerprint")
    _exact_fields(
        root,
        required={"$schema", "inventory", "observation_sha256"},
        field="fingerprint",
    )
    inventory_document = _object(root["inventory"], field="inventory")
    _exact_fields(inventory_document, required=_INVENTORY_FIELDS, field="inventory")
    try:
        inventory = AssetCacheInventory(
            plan_sha256=_text(inventory_document["plan_sha256"], field="plan_sha256"),
            current_actions=_bounded_integer(
                inventory_document["current_actions"],
                field="current_actions",
                maximum=ASSET_CACHE_INVENTORY_MAX_ACTIONS,
            ),
            missing_actions=_bounded_integer(
                inventory_document["missing_actions"],
                field="missing_actions",
                maximum=ASSET_CACHE_INVENTORY_MAX_ACTIONS,
            ),
            other_actions=_bounded_integer(
                inventory_document["other_actions"],
                field="other_actions",
                maximum=ASSET_CACHE_INVENTORY_MAX_ACTIONS,
            ),
            current_action_metadata_bytes=_bounded_integer(
                inventory_document["current_action_metadata_bytes"],
                field="current_action_metadata_bytes",
                maximum=ASSET_CACHE_INVENTORY_MAX_METADATA_BYTES,
            ),
            other_action_metadata_bytes=_bounded_integer(
                inventory_document["other_action_metadata_bytes"],
                field="other_action_metadata_bytes",
                maximum=ASSET_CACHE_INVENTORY_MAX_METADATA_BYTES,
            ),
            cas_blobs=_bounded_integer(
                inventory_document["cas_blobs"],
                field="cas_blobs",
                maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS,
            ),
            current_blobs=_bounded_integer(
                inventory_document["current_blobs"],
                field="current_blobs",
                maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS,
            ),
            other_blobs=_bounded_integer(
                inventory_document["other_blobs"],
                field="other_blobs",
                maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS,
            ),
            current_blob_bytes=_bounded_integer(
                inventory_document["current_blob_bytes"],
                field="current_blob_bytes",
                maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BYTES,
            ),
            other_blob_bytes=_bounded_integer(
                inventory_document["other_blob_bytes"],
                field="other_blob_bytes",
                maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BYTES,
            ),
            unreferenced_blobs=_bounded_integer(
                inventory_document["unreferenced_blobs"],
                field="unreferenced_blobs",
                maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS,
            ),
            unreferenced_blob_bytes=_bounded_integer(
                inventory_document["unreferenced_blob_bytes"],
                field="unreferenced_blob_bytes",
                maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BYTES,
            ),
            protocol=_text(inventory_document["$schema"], field="inventory_schema"),
        )
        fingerprint = AssetCacheFingerprint(
            inventory,
            _text(root["observation_sha256"], field="observation_sha256"),
            protocol=_text(root["$schema"], field="$schema"),
        )
    except AssetCacheError as error:
        raise _invalid_document(field="fingerprint") from error
    if raw != fingerprint.canonical_bytes():
        raise _record_error(
            "asset cache fingerprint record must use canonical JSON",
            code="asset_cache.noncanonical_fingerprint_record",
            phase="decode",
            details={"field": "document"},
        )
    return fingerprint


def verify_asset_cache_fingerprint(
    plan: AssetBuildPlan,
    fingerprint: AssetCacheFingerprint,
    cache_root: Path,
    *,
    project_root: Path | None = None,
    limits: AssetCacheInventoryLimits = DEFAULT_ASSET_CACHE_INVENTORY_LIMITS,
) -> AssetCacheFingerprintVerification:
    """Compare one saved fingerprint with one fresh bounded cache observation."""

    _preflight_fingerprint(plan, fingerprint)
    current = fingerprint_asset_cache_observation(
        plan,
        cache_root,
        project_root=project_root,
        limits=limits,
    )
    if current.inventory != fingerprint.inventory:
        raise _mismatch(field="inventory")
    if current.observation_sha256 != fingerprint.observation_sha256:
        raise _mismatch(field="observation_sha256")
    return AssetCacheFingerprintVerification(
        fingerprint.inventory.plan_sha256,
        fingerprint.observation_sha256,
    )


def _preflight_fingerprint(
    plan: AssetBuildPlan,
    fingerprint: AssetCacheFingerprint,
) -> None:
    if type(plan) is not AssetBuildPlan or type(fingerprint) is not AssetCacheFingerprint:
        raise _record_error(
            "asset cache fingerprint verification requires exact values",
            code="asset_cache.invalid_fingerprint_verify",
            phase="configure",
            details={"field": "plan_or_fingerprint"},
        )
    plan_sha256 = f"sha256:{sha256(plan.canonical_bytes()).hexdigest()}"
    if fingerprint.inventory.plan_sha256 != plan_sha256:
        raise _mismatch(field="plan_sha256")


def _document_bytes(document: str | bytes, *, maximum: int) -> bytes:
    if type(document) is str:
        try:
            raw = document.encode("utf-8")
        except UnicodeEncodeError as error:
            raise _record_error(
                "asset cache fingerprint record JSON could not be decoded",
                code="asset_cache.invalid_fingerprint_json",
                phase="decode",
                details={"cause_type": type(error).__name__},
            ) from error
    elif type(document) is bytes:
        raw = document
    else:
        raise _invalid_document(field="document")
    if len(raw) > maximum:
        raise _record_error(
            "asset cache fingerprint record exceeds an active limit",
            code="asset_cache.fingerprint_limit_exceeded",
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


def _bounded_integer(value: object, *, field: str, maximum: int) -> int:
    if type(value) is not int or not 0 <= value <= maximum:
        raise _invalid_document(field=field)
    return value


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    document: dict[str, object] = {}
    for key, value in pairs:
        if key in document:
            raise ValueError("duplicate fingerprint record field")
        document[key] = value
    return document


def _reject_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant: {value}")


def _require_limits(
    limits: AssetCacheFingerprintRecordLimits,
) -> AssetCacheFingerprintRecordLimits:
    if type(limits) is not AssetCacheFingerprintRecordLimits:
        raise _record_error(
            "asset cache fingerprint record requires exact limits",
            code="asset_cache.invalid_fingerprint_limits",
            phase="configure",
            details={"actual_type": type(limits).__name__},
        )
    return limits


def _invalid_document(*, field: str) -> AssetCacheError:
    return _record_error(
        "asset cache fingerprint record is invalid",
        code="asset_cache.invalid_fingerprint_record",
        phase="decode",
        details={"field": field},
    )


def _mismatch(*, field: str) -> AssetCacheError:
    return _record_error(
        "saved asset cache fingerprint does not match current verified state",
        code="asset_cache.fingerprint_mismatch",
        phase="verify",
        details={"field": field},
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
