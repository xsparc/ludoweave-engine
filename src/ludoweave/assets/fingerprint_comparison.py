"""Path-free aggregate diagnosis for saved cache-fingerprint differences."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

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

ASSET_CACHE_FINGERPRINT_COMPARISON_PROTOCOL = "ludoweave.asset-cache-fingerprint-comparison/1"

_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")


@dataclass(frozen=True, slots=True)
class AssetCacheInventoryDelta:
    """Signed changes for the fixed path-free M137 aggregate fields."""

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

    def __post_init__(self) -> None:
        for field, maximum in (
            ("current_actions", ASSET_CACHE_INVENTORY_MAX_ACTIONS),
            ("missing_actions", ASSET_CACHE_INVENTORY_MAX_ACTIONS),
            ("other_actions", ASSET_CACHE_INVENTORY_MAX_ACTIONS),
            ("current_action_metadata_bytes", ASSET_CACHE_INVENTORY_MAX_METADATA_BYTES),
            ("other_action_metadata_bytes", ASSET_CACHE_INVENTORY_MAX_METADATA_BYTES),
            ("cas_blobs", ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS),
            ("current_blobs", ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS),
            ("other_blobs", ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS),
            ("current_blob_bytes", ASSET_CACHE_INVENTORY_MAX_CAS_BYTES),
            ("other_blob_bytes", ASSET_CACHE_INVENTORY_MAX_CAS_BYTES),
            ("unreferenced_blobs", ASSET_CACHE_INVENTORY_MAX_CAS_BLOBS),
            ("unreferenced_blob_bytes", ASSET_CACHE_INVENTORY_MAX_CAS_BYTES),
        ):
            value = getattr(self, field)
            if type(value) is not int or not -maximum <= value <= maximum:
                raise _comparison_error(
                    "asset cache inventory delta is invalid",
                    code="asset_cache.invalid_fingerprint_comparison",
                    phase="report",
                    details={"field": field},
                )

    @classmethod
    def between(
        cls,
        expected: AssetCacheInventory,
        current: AssetCacheInventory,
    ) -> AssetCacheInventoryDelta:
        """Subtract one exact saved inventory from one current inventory."""

        if type(expected) is not AssetCacheInventory or type(current) is not AssetCacheInventory:
            raise _comparison_error(
                "asset cache inventory delta requires exact inventory values",
                code="asset_cache.invalid_fingerprint_comparison",
                phase="configure",
                details={"field": "inventory"},
            )
        if expected.plan_sha256 != current.plan_sha256:
            raise _comparison_error(
                "asset cache inventory delta requires one exact plan",
                code="asset_cache.fingerprint_mismatch",
                phase="compare",
                details={"field": "plan_sha256"},
            )
        return cls(
            current_actions=current.current_actions - expected.current_actions,
            missing_actions=current.missing_actions - expected.missing_actions,
            other_actions=current.other_actions - expected.other_actions,
            current_action_metadata_bytes=(
                current.current_action_metadata_bytes - expected.current_action_metadata_bytes
            ),
            other_action_metadata_bytes=(
                current.other_action_metadata_bytes - expected.other_action_metadata_bytes
            ),
            cas_blobs=current.cas_blobs - expected.cas_blobs,
            current_blobs=current.current_blobs - expected.current_blobs,
            other_blobs=current.other_blobs - expected.other_blobs,
            current_blob_bytes=current.current_blob_bytes - expected.current_blob_bytes,
            other_blob_bytes=current.other_blob_bytes - expected.other_blob_bytes,
            unreferenced_blobs=current.unreferenced_blobs - expected.unreferenced_blobs,
            unreferenced_blob_bytes=(
                current.unreferenced_blob_bytes - expected.unreferenced_blob_bytes
            ),
        )

    @staticmethod
    def field_names() -> tuple[str, ...]:
        return (
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
        )

    @property
    def changed(self) -> bool:
        return any(getattr(self, field) != 0 for field in self.field_names())

    def as_dict(self) -> dict[str, int]:
        return {field: getattr(self, field) for field in self.field_names()}


@dataclass(frozen=True, slots=True)
class AssetCacheFingerprintComparison:
    """Path-free aggregate comparison of saved and current cache evidence."""

    plan_sha256: str
    observation_equal: bool
    deltas: AssetCacheInventoryDelta
    fingerprint_protocol: str = ASSET_CACHE_FINGERPRINT_PROTOCOL
    protocol: str = ASSET_CACHE_FINGERPRINT_COMPARISON_PROTOCOL

    def __post_init__(self) -> None:
        if (
            type(self.protocol) is not str
            or self.protocol != ASSET_CACHE_FINGERPRINT_COMPARISON_PROTOCOL
            or type(self.fingerprint_protocol) is not str
            or self.fingerprint_protocol != ASSET_CACHE_FINGERPRINT_PROTOCOL
            or type(self.plan_sha256) is not str
            or _SHA256.fullmatch(self.plan_sha256) is None
            or type(self.observation_equal) is not bool
            or type(self.deltas) is not AssetCacheInventoryDelta
        ):
            raise _comparison_error(
                "asset cache fingerprint comparison is invalid",
                code="asset_cache.invalid_fingerprint_comparison",
                phase="report",
                details={"field": "comparison"},
            )

    @property
    def equal(self) -> bool:
        return self.observation_equal and not self.deltas.changed

    def as_dict(self) -> dict[str, object]:
        return {
            "$schema": self.protocol,
            "status": "equal" if self.equal else "different",
            "fingerprint_protocol": self.fingerprint_protocol,
            "plan_sha256": self.plan_sha256,
            "observation_equal": self.observation_equal,
            "deltas": self.deltas.as_dict(),
        }

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.as_dict(),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")


def compare_asset_cache_fingerprint(
    plan: AssetBuildPlan,
    fingerprint: AssetCacheFingerprint,
    cache_root: Path,
    *,
    project_root: Path | None = None,
    limits: AssetCacheInventoryLimits = DEFAULT_ASSET_CACHE_INVENTORY_LIMITS,
) -> AssetCacheFingerprintComparison:
    """Diagnose fixed aggregate differences after exact-plan preflight."""

    _preflight(plan, fingerprint)
    current = fingerprint_asset_cache_observation(
        plan,
        cache_root,
        project_root=project_root,
        limits=limits,
    )
    return AssetCacheFingerprintComparison(
        plan_sha256=fingerprint.inventory.plan_sha256,
        observation_equal=current.observation_sha256 == fingerprint.observation_sha256,
        deltas=AssetCacheInventoryDelta.between(fingerprint.inventory, current.inventory),
    )


def _preflight(plan: AssetBuildPlan, fingerprint: AssetCacheFingerprint) -> None:
    if type(plan) is not AssetBuildPlan or type(fingerprint) is not AssetCacheFingerprint:
        raise _comparison_error(
            "asset cache fingerprint comparison requires exact values",
            code="asset_cache.invalid_fingerprint_comparison",
            phase="configure",
            details={"field": "plan_or_fingerprint"},
        )
    plan_sha256 = f"sha256:{sha256(plan.canonical_bytes()).hexdigest()}"
    if fingerprint.inventory.plan_sha256 != plan_sha256:
        raise _comparison_error(
            "saved asset cache fingerprint does not match the comparison plan",
            code="asset_cache.fingerprint_mismatch",
            phase="compare",
            details={"field": "plan_sha256"},
        )


def _comparison_error(
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
