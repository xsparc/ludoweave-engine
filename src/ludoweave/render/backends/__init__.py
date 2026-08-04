"""Concrete rendering adapters exercised by the current milestone."""

from ludoweave.render.backends.null import NullRenderBackend
from ludoweave.render.backends.null_device import NullRenderDevice

__all__ = ["NullRenderBackend", "NullRenderDevice"]
