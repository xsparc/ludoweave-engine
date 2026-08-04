"""Engine-owned render-device protocol isolated from concrete backends."""

from collections.abc import Sequence
from typing import Protocol

from ludoweave.render.contracts import (
    BufferData,
    BufferDescriptor,
    CaptureImage,
    CommandList,
    PipelineDescriptor,
    RenderCapabilities,
    Submission,
    SurfaceDescriptor,
    TextureData,
    TextureDescriptor,
)
from ludoweave.render.handles import (
    BufferHandle,
    FenceHandle,
    PipelineHandle,
    RenderResourceHandle,
    SurfaceHandle,
    TextureHandle,
)


class RenderDevice(Protocol):
    """Single-owner backend-neutral resource and submission boundary."""

    @property
    def name(self) -> str: ...

    @property
    def capabilities(self) -> RenderCapabilities: ...

    def create_buffer(
        self, descriptor: BufferDescriptor, data: BufferData | None = None
    ) -> BufferHandle: ...

    def create_texture(
        self, descriptor: TextureDescriptor, data: TextureData | None = None
    ) -> TextureHandle: ...

    def create_pipeline(self, descriptor: PipelineDescriptor) -> PipelineHandle: ...

    def create_surface(self, descriptor: SurfaceDescriptor) -> SurfaceHandle: ...

    def submit(self, command_lists: Sequence[CommandList]) -> Submission: ...

    def is_fence_complete(self, fence: FenceHandle) -> bool: ...

    def capture_surface(self, handle: SurfaceHandle) -> CaptureImage: ...

    def resize_surface(self, handle: SurfaceHandle, width: int, height: int) -> None: ...

    def poll(self) -> None: ...

    def destroy(self, handle: RenderResourceHandle) -> None: ...

    def close(self) -> None: ...
