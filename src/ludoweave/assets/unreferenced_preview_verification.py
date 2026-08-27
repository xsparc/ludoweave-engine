"""Strict saved unreferenced-blob previews and offline verification."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from typing import cast

from ludoweave.assets.cache import AssetCacheError
from ludoweave.assets.inventory import (
    ASSET_CACHE_FINGERPRINT_PROTOCOL,
    ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS,
    ASSET_CACHE_INVENTORY_MAX_CAS_BYTES,
    ASSET_CACHE_INVENTORY_PROTOCOL,
    AssetCacheFingerprint,
)
from ludoweave.assets.plans import AssetBuildPlan
from ludoweave.assets.unreferenced_preview import (
    ASSET_CACHE_UNREFERENCED_PREVIEW_PROTOCOL,
    AssetCacheUnreferencedPreview,
    preview_asset_cache_unreferenced_blobs,
)

ASSET_CACHE_UNREFERENCED_PREVIEW_RECORD_MAX_BYTES = 2_048
ASSET_CACHE_UNREFERENCED_PREVIEW_VERIFICATION_PROTOCOL = (
    "ludoweave.asset-cache-unreferenced-preview-verification/1"
)

_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")


@dataclass(frozen=True, slots=True)
class AssetCacheUnreferencedPreviewRecordLimits:
    """Tightening-only bounds for one untrusted saved preview."""

    max_bytes: int = ASSET_CACHE_UNREFERENCED_PREVIEW_RECORD_MAX_BYTES

    def __post_init__(self) -> None:
        if type(self.max_bytes) is not int or self.max_bytes <= 0:
            raise _record_error(
                "asset cache unreferenced preview limits require an exact positive integer",
                code="asset_cache.invalid_unreferenced_preview_limits",
                phase="configure",
                details={"field": "max_bytes", "actual_type": type(self.max_bytes).__name__},
            )
        if self.max_bytes > ASSET_CACHE_UNREFERENCED_PREVIEW_RECORD_MAX_BYTES:
            raise _record_error(
                "asset cache unreferenced preview limits may only tighten the hard maximum",
                code="asset_cache.invalid_unreferenced_preview_limits",
                phase="configure",
                details={
                    "field": "max_bytes",
                    "actual": self.max_bytes,
                    "maximum": ASSET_CACHE_UNREFERENCED_PREVIEW_RECORD_MAX_BYTES,
                },
            )


DEFAULT_ASSET_CACHE_UNREFERENCED_PREVIEW_RECORD_LIMITS = AssetCacheUnreferencedPreviewRecordLimits()


@dataclass(frozen=True, slots=True)
class AssetCacheUnreferencedPreviewVerification:
    """Path-free proof that one saved preview matches its supplied evidence."""

    plan_sha256: str
    observation_sha256: str
    preview_sha256: str
    fingerprint_protocol: str = ASSET_CACHE_FINGERPRINT_PROTOCOL
    preview_protocol: str = ASSET_CACHE_UNREFERENCED_PREVIEW_PROTOCOL
    protocol: str = ASSET_CACHE_UNREFERENCED_PREVIEW_VERIFICATION_PROTOCOL

    def __post_init__(self) -> None:
        if (
            type(self.protocol) is not str
            or self.protocol != ASSET_CACHE_UNREFERENCED_PREVIEW_VERIFICATION_PROTOCOL
            or type(self.preview_protocol) is not str
            or self.preview_protocol != ASSET_CACHE_UNREFERENCED_PREVIEW_PROTOCOL
            or type(self.fingerprint_protocol) is not str
            or self.fingerprint_protocol != ASSET_CACHE_FINGERPRINT_PROTOCOL
            or type(self.plan_sha256) is not str
            or _SHA256.fullmatch(self.plan_sha256) is None
            or type(self.observation_sha256) is not str
            or _SHA256.fullmatch(self.observation_sha256) is None
            or type(self.preview_sha256) is not str
            or _SHA256.fullmatch(self.preview_sha256) is None
        ):
            raise _record_error(
                "asset cache unreferenced preview verification is invalid",
                code="asset_cache.invalid_unreferenced_preview_verification",
                phase="report",
                details={"field": "verification"},
            )

    def as_dict(self) -> dict[str, object]:
        return {
            "$schema": self.protocol,
            "status": "valid",
            "fingerprint_protocol": self.fingerprint_protocol,
            "preview_protocol": self.preview_protocol,
            "plan_sha256": self.plan_sha256,
            "observation_sha256": self.observation_sha256,
            "preview_sha256": self.preview_sha256,
        }

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.as_dict(),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")


def decode_asset_cache_unreferenced_preview(
    document: str | bytes,
    *,
    limits: AssetCacheUnreferencedPreviewRecordLimits = (
        DEFAULT_ASSET_CACHE_UNREFERENCED_PREVIEW_RECORD_LIMITS
    ),
) -> AssetCacheUnreferencedPreview:
    """Decode one bounded, canonical, exact-schema unreferenced preview."""

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
            "asset cache unreferenced preview JSON could not be decoded",
            code="asset_cache.invalid_unreferenced_preview_json",
            phase="decode",
            details={"cause_type": type(error).__name__},
        ) from error
    root = _object(decoded, field="preview")
    _exact_fields(
        root,
        required={
            "$schema",
            "status",
            "fingerprint_protocol",
            "inventory_protocol",
            "plan_sha256",
            "observation_sha256",
            "unreferenced_blobs",
            "unreferenced_blob_bytes",
        },
        field="preview",
    )
    if _text(root["status"], field="status") != "observed":
        raise _invalid_document(field="status")
    try:
        preview = AssetCacheUnreferencedPreview(
            plan_sha256=_digest(root["plan_sha256"], field="plan_sha256"),
            observation_sha256=_digest(root["observation_sha256"], field="observation_sha256"),
            unreferenced_blobs=_bounded_integer(
                root["unreferenced_blobs"],
                field="unreferenced_blobs",
                maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS,
            ),
            unreferenced_blob_bytes=_bounded_integer(
                root["unreferenced_blob_bytes"],
                field="unreferenced_blob_bytes",
                maximum=ASSET_CACHE_INVENTORY_MAX_CAS_BYTES,
            ),
            inventory_protocol=_protocol(
                root["inventory_protocol"],
                field="inventory_protocol",
                expected=ASSET_CACHE_INVENTORY_PROTOCOL,
            ),
            fingerprint_protocol=_protocol(
                root["fingerprint_protocol"],
                field="fingerprint_protocol",
                expected=ASSET_CACHE_FINGERPRINT_PROTOCOL,
            ),
            protocol=_protocol(
                root["$schema"],
                field="$schema",
                expected=ASSET_CACHE_UNREFERENCED_PREVIEW_PROTOCOL,
            ),
        )
    except AssetCacheError as error:
        if error.code == "asset_cache.invalid_unreferenced_preview_record":
            raise
        raise _invalid_document(field="preview") from error
    if raw != preview.canonical_bytes():
        raise _record_error(
            "asset cache unreferenced preview must use canonical JSON",
            code="asset_cache.noncanonical_unreferenced_preview_record",
            phase="decode",
            details={"field": "document"},
        )
    return preview


def verify_asset_cache_unreferenced_preview(
    plan: AssetBuildPlan,
    fingerprint: AssetCacheFingerprint,
    preview: AssetCacheUnreferencedPreview,
) -> AssetCacheUnreferencedPreviewVerification:
    """Verify one saved preview against one admitted fingerprint offline."""

    for field, value, expected_type in (
        ("plan", plan, AssetBuildPlan),
        ("fingerprint", fingerprint, AssetCacheFingerprint),
        ("preview", preview, AssetCacheUnreferencedPreview),
    ):
        if type(value) is not expected_type:
            raise _record_error(
                "asset cache unreferenced preview verification requires exact values",
                code="asset_cache.invalid_unreferenced_preview_verify",
                phase="configure",
                details={"field": field},
            )
    recomputed = preview_asset_cache_unreferenced_blobs(plan, fingerprint)
    if preview != recomputed:
        for field in (
            "protocol",
            "fingerprint_protocol",
            "inventory_protocol",
            "plan_sha256",
            "observation_sha256",
            "unreferenced_blobs",
            "unreferenced_blob_bytes",
        ):
            if getattr(preview, field) != getattr(recomputed, field):
                raise _mismatch(field=field)
        raise _mismatch(field="preview")
    preview_bytes = preview.canonical_bytes()
    return AssetCacheUnreferencedPreviewVerification(
        plan_sha256=preview.plan_sha256,
        observation_sha256=preview.observation_sha256,
        preview_sha256=f"sha256:{sha256(preview_bytes).hexdigest()}",
    )


def _document_bytes(document: str | bytes, *, maximum: int) -> bytes:
    if type(document) is str:
        try:
            raw = document.encode("utf-8")
        except UnicodeEncodeError as error:
            raise _record_error(
                "asset cache unreferenced preview JSON could not be decoded",
                code="asset_cache.invalid_unreferenced_preview_json",
                phase="decode",
                details={"cause_type": type(error).__name__},
            ) from error
    elif type(document) is bytes:
        raw = document
    else:
        raise _invalid_document(field="document")
    if len(raw) > maximum:
        raise _record_error(
            "asset cache unreferenced preview exceeds an active limit",
            code="asset_cache.unreferenced_preview_limit_exceeded",
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
    protocol = _text(value, field=field)
    if protocol != expected:
        raise _invalid_document(field=field)
    return protocol


def _digest(value: object, *, field: str) -> str:
    digest = _text(value, field=field)
    if _SHA256.fullmatch(digest) is None:
        raise _invalid_document(field=field)
    return digest


def _bounded_integer(value: object, *, field: str, maximum: int) -> int:
    if type(value) is not int or not 0 <= value <= maximum:
        raise _invalid_document(field=field)
    return value


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    document: dict[str, object] = {}
    for key, value in pairs:
        if key in document:
            raise ValueError("duplicate unreferenced preview field")
        document[key] = value
    return document


def _reject_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant: {value}")


def _require_limits(
    limits: AssetCacheUnreferencedPreviewRecordLimits,
) -> AssetCacheUnreferencedPreviewRecordLimits:
    if type(limits) is not AssetCacheUnreferencedPreviewRecordLimits:
        raise _record_error(
            "asset cache unreferenced preview requires exact limits",
            code="asset_cache.invalid_unreferenced_preview_limits",
            phase="configure",
            details={"actual_type": type(limits).__name__},
        )
    return limits


def _invalid_document(*, field: str) -> AssetCacheError:
    return _record_error(
        "asset cache unreferenced preview record is invalid",
        code="asset_cache.invalid_unreferenced_preview_record",
        phase="decode",
        details={"field": field},
    )


def _mismatch(*, field: str) -> AssetCacheError:
    return _record_error(
        "saved asset cache unreferenced preview does not match supplied evidence",
        code="asset_cache.unreferenced_preview_verification_mismatch",
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
