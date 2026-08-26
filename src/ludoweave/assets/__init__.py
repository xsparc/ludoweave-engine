"""Validated logical asset identities and content-addressed build artifacts."""

from ludoweave.assets.execution import (
    ASSET_BUILD_RESULT_PROTOCOL,
    AssetBuildExecutionLimits,
    AssetBuildInput,
    AssetBuildResult,
    AssetBuildResultEntry,
    execute_asset_build_plan,
)
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
    "ASSET_BUILD_RESULT_PROTOCOL",
    "ASSET_LOADER_PROTOCOL",
    "ASSET_MANIFEST_PROTOCOL",
    "ASSET_SOURCE_LOCK_PROTOCOL",
    "ASSET_SOURCE_MAX_BYTES",
    "ASSET_SOURCE_TOTAL_MAX_BYTES",
    "AssetArtifact",
    "AssetBuildExecutionLimits",
    "AssetBuildInput",
    "AssetBuildPlan",
    "AssetBuildPlanEntry",
    "AssetBuildPlanLimits",
    "AssetBuildResult",
    "AssetBuildResultEntry",
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
    "execute_asset_build_plan",
]
__stability__ = {name: "experimental" for name in __all__}
