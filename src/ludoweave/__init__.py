"""Small experimental root surface for LudoWeave Engine."""

from importlib.metadata import version as distribution_version
from typing import Final

from ludoweave.app import Engine, EngineConfig, LifecycleState

__version__: Final = distribution_version("ludoweave")

__all__ = ["Engine", "EngineConfig", "LifecycleState", "__version__"]
