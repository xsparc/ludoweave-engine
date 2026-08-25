"""Validated logical asset identities and content-addressed build artifacts."""

from ludoweave.assets.locks import (
    ASSET_SOURCE_LOCK_PROTOCOL,
    ASSET_SOURCE_MAX_BYTES,
    ASSET_SOURCE_TOTAL_MAX_BYTES,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetSourceLockLimits,
)
from ludoweave.assets.pipeline import (
    ASSET_LOADER_PROTOCOL,
    ASSET_MANIFEST_PROTOCOL,
    AssetArtifact,
    AssetEntry,
    AssetError,
    AssetKind,
    AssetManifest,
    AssetManifestLimits,
    AssetPipeline,
    AssetUri,
    PngTexture,
    TextureAsset,
    TextureSlot,
    decode_png,
)
from ludoweave.assets.plans import (
    ASSET_BUILD_PLAN_PROTOCOL,
    AssetBuildPlan,
    AssetBuildPlanEntry,
    AssetBuildPlanLimits,
)

__all__ = [
    "ASSET_BUILD_PLAN_PROTOCOL",
    "ASSET_LOADER_PROTOCOL",
    "ASSET_MANIFEST_PROTOCOL",
    "ASSET_SOURCE_LOCK_PROTOCOL",
    "ASSET_SOURCE_MAX_BYTES",
    "ASSET_SOURCE_TOTAL_MAX_BYTES",
    "AssetArtifact",
    "AssetBuildPlan",
    "AssetBuildPlanEntry",
    "AssetBuildPlanLimits",
    "AssetEntry",
    "AssetError",
    "AssetKind",
    "AssetManifest",
    "AssetManifestLimits",
    "AssetPipeline",
    "AssetSourceLock",
    "AssetSourceLockEntry",
    "AssetSourceLockLimits",
    "AssetUri",
    "PngTexture",
    "TextureAsset",
    "TextureSlot",
    "decode_png",
]
__stability__ = {name: "experimental" for name in __all__}
