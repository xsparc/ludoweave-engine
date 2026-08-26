"""Strict saved cache-fingerprint comparisons and offline verification."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from typing import cast

from ludoweave.assets.cache import AssetCacheError
from ludoweave.assets.fingerprint_comparison import (
    ASSET_CACHE_FINGERPRINT_COMPARISON_PROTOCOL,
    AssetCacheFingerprintComparison,
    AssetCacheInventoryDelta,
    compare_asset_cache_fingerprint_records,
)
from ludoweave.assets.inventory import (
    ASSET_CACHE_FINGERPRINT_PROTOCOL,
    ASSET_CACHE_INVENTORY_MAX_ACTIONS,
    ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS,
    ASSET_CACHE_INVENTORY_MAX_CAS_BYTES,
    ASSET_CACHE_INVENTORY_MAX_METADATA_BYTES,
    AssetCacheFingerprint,
)
from ludoweave.assets.plans import AssetBuildPlan

ASSET_CACHE_FINGERPRINT_COMPARISON_RECORD_MAX_BYTES = 4_096
ASSET_CACHE_FINGERPRINT_COMPARISON_VERIFICATION_PROTOCOL = (
    "ludoweave.asset-cache-fingerprint-comparison-verification/1"
)

_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")
_DELTA_FIELDS = set(AssetCacheInventoryDelta.field_names())


@dataclass(frozen=True, slots=True)
class AssetCacheFingerprintComparisonRecordLimits:
    """Tightening-only bounds for one untrusted saved comparison."""

    max_bytes: int = ASSET_CACHE_FINGERPRINT_COMPARISON_RECORD_MAX_BYTES

    def __post_init__(self) -> None:
        if type(self.max_bytes) is not int or self.max_bytes <= 0:
            raise _comparison_record_error(
                "asset cache fingerprint comparison limits require an exact positive integer",
                code="asset_cache.invalid_fingerprint_comparison_limits",
                phase="configure",
                details={"field": "max_bytes", "actual_type": type(self.max_bytes).__name__},
            )
        if self.max_bytes > ASSET_CACHE_FINGERPRINT_COMPARISON_RECORD_MAX_BYTES:
            raise _comparison_record_error(
                "asset cache fingerprint comparison limits may only tighten the hard maximum",
                code="asset_cache.invalid_fingerprint_comparison_limits",
                phase="configure",
                details={
                    "field": "max_bytes",
                    "actual": self.max_bytes,
                    "maximum": ASSET_CACHE_FINGERPRINT_COMPARISON_RECORD_MAX_BYTES,
                },
            )


DEFAULT_ASSET_CACHE_FINGERPRINT_COMPARISON_RECORD_LIMITS = (
    AssetCacheFingerprintComparisonRecordLimits()
)


@dataclass(frozen=True, slots=True)
class AssetCacheFingerprintComparisonVerification:
    """Path-free proof that one saved comparison matches its supplied records."""

    plan_sha256: str
    comparison_sha256: str
    comparison_status: str
    fingerprint_protocol: str = ASSET_CACHE_FINGERPRINT_PROTOCOL
    comparison_protocol: str = ASSET_CACHE_FINGERPRINT_COMPARISON_PROTOCOL
    protocol: str = ASSET_CACHE_FINGERPRINT_COMPARISON_VERIFICATION_PROTOCOL

    def __post_init__(self) -> None:
        if (
            type(self.protocol) is not str
            or self.protocol != ASSET_CACHE_FINGERPRINT_COMPARISON_VERIFICATION_PROTOCOL
            or type(self.comparison_protocol) is not str
            or self.comparison_protocol != ASSET_CACHE_FINGERPRINT_COMPARISON_PROTOCOL
            or type(self.fingerprint_protocol) is not str
            or self.fingerprint_protocol != ASSET_CACHE_FINGERPRINT_PROTOCOL
            or type(self.plan_sha256) is not str
            or _SHA256.fullmatch(self.plan_sha256) is None
            or type(self.comparison_sha256) is not str
            or _SHA256.fullmatch(self.comparison_sha256) is None
            or type(self.comparison_status) is not str
            or self.comparison_status not in {"equal", "different"}
        ):
            raise _comparison_record_error(
                "asset cache fingerprint comparison verification is invalid",
                code="asset_cache.invalid_fingerprint_comparison_verification",
                phase="report",
                details={"field": "verification"},
            )

    def as_dict(self) -> dict[str, object]:
        return {
            "$schema": self.protocol,
            "status": "valid",
            "fingerprint_protocol": self.fingerprint_protocol,
            "comparison_protocol": self.comparison_protocol,
            "plan_sha256": self.plan_sha256,
            "comparison_status": self.comparison_status,
            "comparison_sha256": self.comparison_sha256,
        }

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.as_dict(),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")


def decode_asset_cache_fingerprint_comparison(
    document: str | bytes,
    *,
    limits: AssetCacheFingerprintComparisonRecordLimits = (
        DEFAULT_ASSET_CACHE_FINGERPRINT_COMPARISON_RECORD_LIMITS
    ),
) -> AssetCacheFingerprintComparison:
    """Decode one bounded, canonical, exact-schema comparison record."""

    checked_limits = _require_limits(limits)
    raw = _document_bytes(document, maximum=checked_limits.max_bytes)
    try:
        decoded: object = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
            parse_int=_parse_integer,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError) as error:
        raise _comparison_record_error(
            "asset cache fingerprint comparison JSON could not be decoded",
            code="asset_cache.invalid_fingerprint_comparison_json",
            phase="decode",
            details={"cause_type": type(error).__name__},
        ) from error
    root = _object(decoded, field="comparison")
    _exact_fields(
        root,
        required={
            "$schema",
            "status",
            "fingerprint_protocol",
            "plan_sha256",
            "observation_equal",
            "deltas",
        },
        field="comparison",
    )
    deltas = _object(root["deltas"], field="deltas")
    _exact_fields(deltas, required=_DELTA_FIELDS, field="deltas")
    try:
        comparison = AssetCacheFingerprintComparison(
            plan_sha256=_digest(root["plan_sha256"], field="plan_sha256"),
            observation_equal=_boolean(root["observation_equal"], field="observation_equal"),
            deltas=AssetCacheInventoryDelta(
                current_actions=_signed_integer(
                    deltas["current_actions"],
                    field="current_actions",
                    maximum=ASSET_CACHE_INVENTORY_MAX_ACTIONS,
                ),
                missing_actions=_signed_integer(
                    deltas["missing_actions"],
                    field="missing_actions",
                    maximum=ASSET_CACHE_INVENTORY_MAX_ACTIONS,
                ),
                other_actions=_signed_integer(
                    deltas["other_actions"],
                    field="other_actions",
                    maximum=ASSET_CACHE_INVENTORY_MAX_ACTIONS,
                ),
                current_action_metadata_bytes=_signed_integer(
                    deltas["current_action_metadata_bytes"],
                    field="current_action_metadata_bytes",
                    maximum=ASSET_CACHE_INVENTORY_MAX_METADATA_BYTES,
                ),
                other_action_metadata_bytes=_signed_integer(
                    deltas["other_action_metadata_bytes"],
                    field="other_action_metadata_bytes",
                    maximum=ASSET_CACHE_INVENTORY_MAX_METADATA_BYTES,
                ),
                cas_blobs=_signed_integer(
                    deltas["cas_blobs"],
                    field="cas_blobs",
                    maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS,
                ),
                current_blobs=_signed_integer(
                    deltas["current_blobs"],
                    field="current_blobs",
                    maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS,
                ),
                other_blobs=_signed_integer(
                    deltas["other_blobs"],
                    field="other_blobs",
                    maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS,
                ),
                current_blob_bytes=_signed_integer(
                    deltas["current_blob_bytes"],
                    field="current_blob_bytes",
                    maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BYTES,
                ),
                other_blob_bytes=_signed_integer(
                    deltas["other_blob_bytes"],
                    field="other_blob_bytes",
                    maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BYTES,
                ),
                unreferenced_blobs=_signed_integer(
                    deltas["unreferenced_blobs"],
                    field="unreferenced_blobs",
                    maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS,
                ),
                unreferenced_blob_bytes=_signed_integer(
                    deltas["unreferenced_blob_bytes"],
                    field="unreferenced_blob_bytes",
                    maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BYTES,
                ),
            ),
            fingerprint_protocol=_protocol(
                root["fingerprint_protocol"],
                field="fingerprint_protocol",
                expected=ASSET_CACHE_FINGERPRINT_PROTOCOL,
            ),
            protocol=_protocol(
                root["$schema"],
                field="$schema",
                expected=ASSET_CACHE_FINGERPRINT_COMPARISON_PROTOCOL,
            ),
        )
    except AssetCacheError as error:
        if error.code == "asset_cache.invalid_fingerprint_comparison_record":
            raise
        raise _invalid_document(field="comparison") from error
    status = _text(root["status"], field="status")
    if status != ("equal" if comparison.equal else "different"):
        raise _invalid_document(field="status")
    if raw != comparison.canonical_bytes():
        raise _comparison_record_error(
            "asset cache fingerprint comparison must use canonical JSON",
            code="asset_cache.noncanonical_fingerprint_comparison_record",
            phase="decode",
            details={"field": "document"},
        )
    return comparison


def verify_asset_cache_fingerprint_comparison(
    plan: AssetBuildPlan,
    expected: AssetCacheFingerprint,
    current: AssetCacheFingerprint,
    comparison: AssetCacheFingerprintComparison,
) -> AssetCacheFingerprintComparisonVerification:
    """Verify one saved comparison against two admitted fingerprints offline."""

    for field, value, expected_type in (
        ("plan", plan, AssetBuildPlan),
        ("expected", expected, AssetCacheFingerprint),
        ("current", current, AssetCacheFingerprint),
        ("comparison", comparison, AssetCacheFingerprintComparison),
    ):
        if type(value) is not expected_type:
            raise _comparison_record_error(
                "asset cache fingerprint comparison verification requires exact values",
                code="asset_cache.invalid_fingerprint_comparison_verify",
                phase="configure",
                details={"field": field},
            )
    recomputed = compare_asset_cache_fingerprint_records(plan, expected, current)
    if comparison != recomputed:
        for field in (
            "protocol",
            "fingerprint_protocol",
            "plan_sha256",
            "observation_equal",
            "deltas",
        ):
            if getattr(comparison, field) != getattr(recomputed, field):
                raise _mismatch(field=field)
        raise _mismatch(field="comparison")
    comparison_bytes = comparison.canonical_bytes()
    return AssetCacheFingerprintComparisonVerification(
        plan_sha256=comparison.plan_sha256,
        comparison_sha256=f"sha256:{sha256(comparison_bytes).hexdigest()}",
        comparison_status="equal" if comparison.equal else "different",
    )


def _document_bytes(document: str | bytes, *, maximum: int) -> bytes:
    if type(document) is str:
        try:
            raw = document.encode("utf-8")
        except UnicodeEncodeError as error:
            raise _comparison_record_error(
                "asset cache fingerprint comparison JSON could not be decoded",
                code="asset_cache.invalid_fingerprint_comparison_json",
                phase="decode",
                details={"cause_type": type(error).__name__},
            ) from error
    elif type(document) is bytes:
        raw = document
    else:
        raise _invalid_document(field="document")
    if len(raw) > maximum:
        raise _comparison_record_error(
            "asset cache fingerprint comparison exceeds an active limit",
            code="asset_cache.fingerprint_comparison_limit_exceeded",
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


def _protocol(value: object, *, field: str, expected: str) -> str:
    text = _text(value, field=field)
    if text != expected:
        raise _invalid_document(field=field)
    return text


def _digest(value: object, *, field: str) -> str:
    text = _text(value, field=field)
    if _SHA256.fullmatch(text) is None:
        raise _invalid_document(field=field)
    return text


def _boolean(value: object, *, field: str) -> bool:
    if type(value) is not bool:
        raise _invalid_document(field=field)
    return value


def _signed_integer(value: object, *, field: str, maximum: int) -> int:
    if type(value) is not int or not -maximum <= value <= maximum:
        raise _invalid_document(field=field)
    return value


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    document: dict[str, object] = {}
    for key, value in pairs:
        if key in document:
            raise ValueError("duplicate comparison record field")
        document[key] = value
    return document


def _reject_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant: {value}")


def _parse_integer(value: str) -> int:
    if len(value.removeprefix("-")) > 20:
        raise ValueError("comparison integer is too long")
    return int(value)


def _require_limits(
    limits: AssetCacheFingerprintComparisonRecordLimits,
) -> AssetCacheFingerprintComparisonRecordLimits:
    if type(limits) is not AssetCacheFingerprintComparisonRecordLimits:
        raise _comparison_record_error(
            "asset cache fingerprint comparison requires exact limits",
            code="asset_cache.invalid_fingerprint_comparison_limits",
            phase="configure",
            details={"actual_type": type(limits).__name__},
        )
    return limits


def _invalid_document(*, field: str) -> AssetCacheError:
    return _comparison_record_error(
        "asset cache fingerprint comparison record is invalid",
        code="asset_cache.invalid_fingerprint_comparison_record",
        phase="decode",
        details={"field": field},
    )


def _mismatch(*, field: str) -> AssetCacheError:
    return _comparison_record_error(
        "saved asset cache fingerprint comparison does not match supplied records",
        code="asset_cache.fingerprint_comparison_mismatch",
        phase="verify",
        details={"field": field},
    )


def _comparison_record_error(
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
