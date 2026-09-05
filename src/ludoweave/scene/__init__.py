"""Versioned data-only scene documents and transaction planning."""

from ludoweave.scene.document import SCENE_PROTOCOL, SceneDocument, SceneLimits
from ludoweave.scene.errors import PrefabError, SceneError
from ludoweave.scene.locks import (
    SOURCE_LOCK_PROTOCOL,
    SourceLock,
    SourceLockEntry,
    SourceLockLimits,
)
from ludoweave.scene.planning import SceneInstantiationPlan, SceneNode, compile_scene
from ludoweave.scene.prefab import (
    PREFAB_INSTANCE_PROTOCOL,
    PREFAB_PROTOCOL,
    PrefabDocument,
    PrefabInstance,
    PrefabInstantiationPlan,
    PrefabLimits,
    PrefabNode,
    compile_prefab,
)
from ludoweave.scene.sources import (
    SOURCE_MANIFEST_PROTOCOL,
    SourceManifest,
    SourceManifestEntry,
    SourceManifestLimits,
)

__all__ = [
    "PREFAB_INSTANCE_PROTOCOL",
    "PREFAB_PROTOCOL",
    "SCENE_PROTOCOL",
    "SOURCE_LOCK_PROTOCOL",
    "SOURCE_MANIFEST_PROTOCOL",
    "PrefabDocument",
    "PrefabError",
    "PrefabInstance",
    "PrefabInstantiationPlan",
    "PrefabLimits",
    "PrefabNode",
    "SceneDocument",
    "SceneError",
    "SceneInstantiationPlan",
    "SceneLimits",
    "SceneNode",
    "SourceLock",
    "SourceLockEntry",
    "SourceLockLimits",
    "SourceManifest",
    "SourceManifestEntry",
    "SourceManifestLimits",
    "compile_prefab",
    "compile_scene",
]
__stability__ = {name: "experimental" for name in __all__}
