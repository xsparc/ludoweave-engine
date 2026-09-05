"""Path-free preview of unreferenced blobs in one verified cache fingerprint."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256

from ludoweave.assets.cache import AssetCacheError
from ludoweave.assets.inventory import (
    ASSET_CACHE_FINGERPRINT_PROTOCOL,
    ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS,
    ASSET_CACHE_INVENTORY_MAX_CAS_BYTES,
    ASSET_CACHE_INVENTORY_PROTOCOL,
    AssetCacheFingerprint,
)
from ludoweave.assets.plans import AssetBuildPlan

ASSET_CACHE_UNREFERENCED_PREVIEW_PROTOCOL = "ludoweave.asset-cache-unreferenced-preview/1"

_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")


@dataclass(frozen=True, slots=True)
class AssetCacheUnreferencedPreview:
    """Path-free observation of blobs with no admitted action reference."""

    plan_sha256: str
    observation_sha256: str
    unreferenced_blobs: int
    unreferenced_blob_bytes: int
    inventory_protocol: str = ASSET_CACHE_INVENTORY_PROTOCOL
    fingerprint_protocol: str = ASSET_CACHE_FINGERPRINT_PROTOCOL
    protocol: str = ASSET_CACHE_UNREFERENCED_PREVIEW_PROTOCOL

    def __post_init__(self) -> None:
        if (
            type(self.protocol) is not str
            or self.protocol != ASSET_CACHE_UNREFERENCED_PREVIEW_PROTOCOL
            or type(self.fingerprint_protocol) is not str
            or self.fingerprint_protocol != ASSET_CACHE_FINGERPRINT_PROTOCOL
            or type(self.inventory_protocol) is not str
            or self.inventory_protocol != ASSET_CACHE_INVENTORY_PROTOCOL
            or type(self.plan_sha256) is not str
            or _SHA256.fullmatch(self.plan_sha256) is None
            or type(self.observation_sha256) is not str
            or _SHA256.fullmatch(self.observation_sha256) is None
            or type(self.unreferenced_blobs) is not int
            or not 0 <= self.unreferenced_blobs <= ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS
            or type(self.unreferenced_blob_bytes) is not int
            or not 0 <= self.unreferenced_blob_bytes <= ASSET_CACHE_INVENTORY_MAX_CAS_BYTES
            or (self.unreferenced_blobs == 0 and self.unreferenced_blob_bytes != 0)
        ):
            raise _preview_error(
                "asset cache unreferenced preview is invalid",
                code="asset_cache.invalid_unreferenced_preview",
                phase="report",
                details={"field": "preview"},
            )

    def as_dict(self) -> dict[str, object]:
        return {
            "$schema": self.protocol,
            "status": "observed",
            "fingerprint_protocol": self.fingerprint_protocol,
            "inventory_protocol": self.inventory_protocol,
            "plan_sha256": self.plan_sha256,
            "observation_sha256": self.observation_sha256,
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


def preview_asset_cache_unreferenced_blobs(
    plan: AssetBuildPlan,
    fingerprint: AssetCacheFingerprint,
) -> AssetCacheUnreferencedPreview:
    """Summarize existing path-free evidence without cache access or mutation."""

    if type(plan) is not AssetBuildPlan:
        raise _preview_error(
            "asset cache unreferenced preview requires an exact build plan",
            code="asset_cache.invalid_unreferenced_preview",
            phase="configure",
            details={"field": "plan"},
        )
    if type(fingerprint) is not AssetCacheFingerprint:
        raise _preview_error(
            "asset cache unreferenced preview requires an exact fingerprint",
            code="asset_cache.invalid_unreferenced_preview",
            phase="configure",
            details={"field": "fingerprint"},
        )
    plan_sha256 = f"sha256:{sha256(plan.canonical_bytes()).hexdigest()}"
    inventory = fingerprint.inventory
    if inventory.plan_sha256 != plan_sha256:
        raise _preview_error(
            "asset cache fingerprint does not match the preview plan",
            code="asset_cache.unreferenced_preview_mismatch",
            phase="preview",
            details={"field": "plan_sha256"},
        )
    return AssetCacheUnreferencedPreview(
        plan_sha256=plan_sha256,
        observation_sha256=fingerprint.observation_sha256,
        unreferenced_blobs=inventory.unreferenced_blobs,
        unreferenced_blob_bytes=inventory.unreferenced_blob_bytes,
    )


def _preview_error(
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
