"""Structured failures for versioned scene documents and plans."""

from ludoweave.core.errors import LudoWeaveError


class SceneError(LudoWeaveError):
    """Raised before mutation when scene data or planning is invalid."""


class PrefabError(SceneError):
    """Raised before mutation when prefab data or planning is invalid."""
