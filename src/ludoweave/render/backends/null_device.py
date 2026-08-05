"""Deterministic validation-only render device with no graphics dependencies."""

from __future__ import annotations

import threading
from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import cast
from uuid import UUID, uuid4

from ludoweave.core.errors import RenderError
from ludoweave.platform import PlatformEvent
from ludoweave.render.contracts import (
    BufferData,
    BufferDescriptor,
    CaptureImage,
    ClearCommand,
    CommandList,
    PipelineDescriptor,
    PrimitiveTopology,
    RenderCapabilities,
    SpriteBatchCommand,
    Submission,
    SurfaceDescriptor,
    SurfaceKind,
    TextureData,
    TextureDescriptor,
    TextureFormat,
    TextureUsage,
    TileBatchCommand,
    referenced_resources,
)
from ludoweave.render.graph import CompiledRenderGraph, RenderGraph
from ludoweave.render.handles import (
    BufferHandle,
    FenceHandle,
    PipelineHandle,
    RenderResourceHandle,
    SurfaceHandle,
    TextureHandle,
)

_MAX_GENERATION = 2**63 - 1


class _Kind(StrEnum):
    BUFFER = "buffer"
    TEXTURE = "texture"
    PIPELINE = "pipeline"
    SURFACE = "surface"


@dataclass(slots=True)
class _Slot:
    kind: _Kind
    generation: int
    descriptor: object
    data: bytes | None
    live: bool = True
    last_submission: int = 0
    retire_after: int | None = None


class NullRenderDevice:
    """Reference resource-lifetime and command validator for all backends."""

    __slots__ = (
        "_closed",
        "_completed_submission",
        "_free",
        "_next_submission",
        "_owner_thread",
        "_scope",
        "_slots",
        "_submissions",
    )

    def __init__(self, *, scope: UUID | None = None) -> None:
        selected_scope = uuid4() if scope is None else scope
        checked_scope = cast(object, selected_scope)
        if not isinstance(checked_scope, UUID) or checked_scope.int == 0:
            raise _device_error(
                "null render device scope must be a nonzero UUID",
                code="render.invalid_device",
                phase="configure",
                details={"field": "scope"},
            )
        self._scope = selected_scope
        self._slots: list[_Slot] = []
        self._free: list[int] = []
        self._next_submission = 1
        self._completed_submission = 0
        self._submissions: dict[int, Submission] = {}
        self._closed = False
        self._owner_thread = threading.get_ident()

    @property
    def name(self) -> str:
        return "null-device"

    @property
    def scope(self) -> UUID:
        return self._scope

    @property
    def capabilities(self) -> RenderCapabilities:
        return RenderCapabilities(
            backend="null-device",
            max_texture_dimension_2d=16_384,
            offscreen_capture=False,
            timestamp_queries=False,
            surface_formats=(
                TextureFormat.RGBA8_UNORM,
                TextureFormat.RGBA8_UNORM_SRGB,
                TextureFormat.BGRA8_UNORM,
                TextureFormat.BGRA8_UNORM_SRGB,
            ),
        )

    @property
    def live_resource_count(self) -> int:
        return sum(slot.live for slot in self._slots)

    @property
    def pending_destruction_count(self) -> int:
        return sum(slot.retire_after is not None for slot in self._slots)

    @property
    def physical_resource_count(self) -> int:
        return sum(slot.live or slot.retire_after is not None for slot in self._slots)

    @property
    def completed_submission(self) -> int:
        return self._completed_submission

    @property
    def latest_submission(self) -> int:
        return self._next_submission - 1

    def create_buffer(
        self, descriptor: BufferDescriptor, data: BufferData | None = None
    ) -> BufferHandle:
        self._guard("create_buffer")
        if type(descriptor) is not BufferDescriptor or (
            data is not None and type(data) is not BufferData
        ):
            raise _invalid_descriptor("buffer")
        if data is not None and len(data.value) > descriptor.size:
            raise _invalid_descriptor("buffer_data")
        return cast(
            BufferHandle,
            self._allocate(_Kind.BUFFER, descriptor, None if data is None else bytes(data.value)),
        )

    def create_texture(
        self, descriptor: TextureDescriptor, data: TextureData | None = None
    ) -> TextureHandle:
        self._guard("create_texture")
        if type(descriptor) is not TextureDescriptor or (
            data is not None and type(data) is not TextureData
        ):
            raise _invalid_descriptor("texture")
        if descriptor.width > self.capabilities.max_texture_dimension_2d or descriptor.height > (
            self.capabilities.max_texture_dimension_2d
        ):
            raise _device_error(
                "texture exceeds device capabilities",
                code="render.unsupported_descriptor",
                phase="create",
                details={"resource": "texture"},
            )
        if data is not None:
            expected = data.bytes_per_row * descriptor.height * descriptor.layers
            if data.bytes_per_row < descriptor.width * 4 or len(data.value) != expected:
                raise _invalid_descriptor("texture_data")
        return cast(
            TextureHandle,
            self._allocate(_Kind.TEXTURE, descriptor, None if data is None else bytes(data.value)),
        )

    def create_pipeline(self, descriptor: PipelineDescriptor) -> PipelineHandle:
        self._guard("create_pipeline")
        if type(descriptor) is not PipelineDescriptor:
            raise _invalid_descriptor("pipeline")
        return cast(PipelineHandle, self._allocate(_Kind.PIPELINE, descriptor, None))

    def create_surface(self, descriptor: SurfaceDescriptor) -> SurfaceHandle:
        self._guard("create_surface")
        if type(descriptor) is not SurfaceDescriptor:
            raise _invalid_descriptor("surface")
        if descriptor.kind is SurfaceKind.WINDOW:
            # Null validates the same descriptor but owns no native window.
            pass
        return cast(SurfaceHandle, self._allocate(_Kind.SURFACE, descriptor, None))

    def submit(self, command_lists: Sequence[CommandList]) -> Submission:
        self._guard("submit")
        try:
            frozen_lists = tuple(command_lists)
        except Exception as error:
            raise _device_error(
                "render command lists could not be frozen",
                code="render.invalid_submission",
                phase="submit",
                details={"field": "command_lists"},
            ) from error
        if not frozen_lists or any(type(item) is not CommandList for item in frozen_lists):
            raise _device_error(
                "render submission requires exact non-empty command lists",
                code="render.invalid_submission",
                phase="submit",
                details={"field": "command_lists"},
            )
        referenced: list[RenderResourceHandle] = []
        draw_calls = 0
        sprite_instances = 0
        tile_instances = 0
        debug_primitives = 0
        for command_list in frozen_lists:
            target_format: TextureFormat | None = None
            has_debug_draw = False
            if command_list.target is not None:
                target_slot = self._slot_for(command_list.target)
                referenced.append(command_list.target)
                target_format = self._target_format(target_slot)
            for command in command_list.commands:
                handles = referenced_resources(command)
                for handle in handles:
                    self._slot_for(handle)
                    referenced.append(handle)
                if type(command) is ClearCommand:
                    target_slot = self._slot_for(command.target)
                    if target_slot.kind is _Kind.TEXTURE:
                        descriptor = cast(TextureDescriptor, target_slot.descriptor)
                        if not descriptor.usage & TextureUsage.RENDER_ATTACHMENT:
                            raise _invalid_usage("clear_target")
                elif type(command) is SpriteBatchCommand:
                    self._validate_batch(command.pipeline, command.texture, target_format)
                    draw_calls += 1
                    sprite_instances += len(command.instances)
                elif type(command) is TileBatchCommand:
                    self._validate_batch(command.pipeline, command.texture, target_format)
                    draw_calls += 1
                    tile_instances += len(command.tiles)
                else:
                    has_debug_draw = True
                    debug_primitives += 1
            if has_debug_draw:
                draw_calls += 1

        submission_number = self._next_submission
        if submission_number > _MAX_GENERATION:
            raise _device_error(
                "render submission sequence is exhausted",
                code="render.fence_exhausted",
                phase="submit",
                details={},
            )
        fence = FenceHandle(self._scope, submission_number)
        report = Submission(
            fence,
            frozen_lists,
            draw_calls,
            sprite_instances,
            tile_instances,
            debug_primitives,
        )
        for handle in referenced:
            self._slot_for(handle).last_submission = submission_number
        self._submissions[submission_number] = report
        self._next_submission += 1
        return report

    def submit_graph(self, graph: RenderGraph | CompiledRenderGraph) -> Submission:
        self._guard("submit_graph")
        compiled = graph.compile() if type(graph) is RenderGraph else graph
        if type(compiled) is not CompiledRenderGraph:
            raise _device_error(
                "render graph submission requires a graph or compiled graph",
                code="render.invalid_graph",
                phase="submit",
                details={"field": "graph"},
            )
        return self.submit(compiled.command_lists)

    def is_fence_complete(self, fence: FenceHandle) -> bool:
        self._guard("is_fence_complete")
        self._validate_fence(fence)
        return fence.submission <= self._completed_submission

    def capture_surface(self, handle: SurfaceHandle) -> CaptureImage:
        self._guard("capture_surface")
        self._slot_for(handle)
        raise _device_error(
            "null rendering has no presentation pixels",
            code="render.capability_missing",
            phase="capture",
            details={"feature": "offscreen_capture"},
        )

    def resize_surface(self, handle: SurfaceHandle, width: int, height: int) -> None:
        self._guard("resize_surface")
        slot = self._slot_for(handle)
        if (
            type(width) is not int
            or type(height) is not int
            or width < 0
            or height < 0
            or (width == 0) != (height == 0)
        ):
            raise _device_error(
                "surface extent must be positive or use the minimized zero extent",
                code="render.invalid_descriptor",
                phase="resize",
                details={"field": "extent"},
            )
        if width == 0:
            return
        descriptor = cast(SurfaceDescriptor, slot.descriptor)
        slot.descriptor = SurfaceDescriptor(
            width,
            height,
            descriptor.format,
            descriptor.kind,
            descriptor.label,
        )

    def drain_surface_events(self, handle: SurfaceHandle) -> tuple[PlatformEvent, ...]:
        """Validate the surface and return no events for the headless device."""

        self._guard("drain_surface_events")
        if type(handle) is not SurfaceHandle:
            raise _device_error(
                "surface event drain requires an exact surface handle",
                code="render.wrong_handle_kind",
                phase="events",
                details={"actual_type": type(handle).__name__},
            )
        self._slot_for(handle)
        return ()

    def poll(self) -> None:
        self._guard("poll")
        self.complete_through(self._next_submission - 1)

    def complete_through(self, submission: int) -> None:
        """Deterministically advance Null completion without sleeps."""

        self._guard("complete_through")
        if (
            type(submission) is not int
            or submission < self._completed_submission
            or submission >= self._next_submission
        ):
            raise _device_error(
                "completion must advance through an existing submission",
                code="render.invalid_fence",
                phase="complete",
                details={"field": "submission"},
            )
        self._completed_submission = submission
        for index, slot in enumerate(self._slots):
            if slot.retire_after is not None and slot.retire_after <= submission:
                slot.retire_after = None
                slot.descriptor = None
                slot.data = None
                if slot.generation < _MAX_GENERATION:
                    self._free.append(index)

    def destroy(self, handle: RenderResourceHandle) -> None:
        self._guard("destroy")
        slot = self._slot_for(handle)
        slot.live = False
        if slot.generation == _MAX_GENERATION:
            slot.descriptor = None
            slot.data = None
            slot.retire_after = None
            return
        slot.generation += 1
        if slot.last_submission > self._completed_submission:
            slot.retire_after = slot.last_submission
        else:
            slot.descriptor = None
            slot.data = None
            self._free.append(handle.index)

    def validate_handle(self, handle: RenderResourceHandle) -> None:
        """Validate owner, kind, and live generation without changing state."""

        self._guard("validate_handle")
        self._slot_for(handle)

    def last_submission_for(self, handle: RenderResourceHandle) -> int:
        """Return the latest submission that referenced a live handle."""

        self._guard("last_submission_for")
        return self._slot_for(handle).last_submission

    def close(self) -> None:
        self._assert_owner_thread()
        if self._closed:
            return
        if self._next_submission > 1:
            self._completed_submission = self._next_submission - 1
        self._free.clear()
        for slot in self._slots:
            slot.live = False
            slot.retire_after = None
            slot.descriptor = None
            slot.data = None
        self._submissions.clear()
        self._closed = True

    def _allocate(
        self, kind: _Kind, descriptor: object, data: bytes | None
    ) -> RenderResourceHandle:
        if self._free:
            index = self._free.pop()
            slot = self._slots[index]
            if slot.live or slot.retire_after is not None or slot.generation >= _MAX_GENERATION:
                raise AssertionError("null render free-list invariant violated")
            slot.kind = kind
            slot.descriptor = descriptor
            slot.data = data
            slot.live = True
            slot.last_submission = 0
        else:
            index = len(self._slots)
            slot = _Slot(kind, 0, descriptor, data)
            self._slots.append(slot)
        handle_type = {
            _Kind.BUFFER: BufferHandle,
            _Kind.TEXTURE: TextureHandle,
            _Kind.PIPELINE: PipelineHandle,
            _Kind.SURFACE: SurfaceHandle,
        }[kind]
        return handle_type(self._scope, index, slot.generation)

    def _slot_for(self, handle: RenderResourceHandle) -> _Slot:
        if type(handle) not in (BufferHandle, TextureHandle, PipelineHandle, SurfaceHandle):
            raise _device_error(
                "render operation requires an exact resource handle",
                code="render.invalid_handle",
                phase="handle",
                details={"actual_type": type(handle).__name__},
            )
        if handle.scope != self._scope:
            raise _device_error(
                "render handle belongs to a different device",
                code="render.foreign_handle",
                phase="handle",
                details={"resource": type(handle).__name__},
            )
        if handle.index >= len(self._slots):
            raise _device_error(
                "render handle slot does not exist",
                code="render.invalid_handle",
                phase="handle",
                details={"resource": type(handle).__name__},
            )
        slot = self._slots[handle.index]
        expected_type = {
            _Kind.BUFFER: BufferHandle,
            _Kind.TEXTURE: TextureHandle,
            _Kind.PIPELINE: PipelineHandle,
            _Kind.SURFACE: SurfaceHandle,
        }[slot.kind]
        if type(handle) is not expected_type:
            raise _device_error(
                "render handle kind does not match the resource",
                code="render.wrong_handle_kind",
                phase="handle",
                details={"resource": slot.kind.value},
            )
        if not slot.live or handle.generation != slot.generation:
            raise _device_error(
                "render handle is stale or retired",
                code="render.stale_handle",
                phase="handle",
                details={"resource": slot.kind.value},
            )
        return slot

    def _validate_batch(
        self,
        pipeline: PipelineHandle,
        texture: TextureHandle,
        target_format: TextureFormat | None,
    ) -> None:
        pipeline_slot = self._slot_for(pipeline)
        texture_slot = self._slot_for(texture)
        descriptor = cast(TextureDescriptor, texture_slot.descriptor)
        if not descriptor.usage & TextureUsage.SAMPLED:
            raise _invalid_usage("sampled_texture")
        pipeline_descriptor = cast(PipelineDescriptor, pipeline_slot.descriptor)
        if (
            target_format is None
            or pipeline_descriptor.color_format is not target_format
            or pipeline_descriptor.topology is not PrimitiveTopology.TRIANGLE_LIST
        ):
            raise _invalid_usage("pipeline_target_format")

    def _target_format(self, slot: _Slot) -> TextureFormat:
        if slot.kind is _Kind.TEXTURE:
            descriptor = cast(TextureDescriptor, slot.descriptor)
            if not descriptor.usage & TextureUsage.RENDER_ATTACHMENT:
                raise _invalid_usage("command_list_target")
            return descriptor.format
        if slot.kind is _Kind.SURFACE:
            return cast(SurfaceDescriptor, slot.descriptor).format
        raise _invalid_usage("command_list_target")

    def _validate_fence(self, fence: FenceHandle) -> None:
        if type(fence) is not FenceHandle:
            raise _device_error(
                "fence operation requires an exact fence handle",
                code="render.invalid_fence",
                phase="fence",
                details={"actual_type": type(fence).__name__},
            )
        if fence.scope != self._scope:
            raise _device_error(
                "render fence belongs to another device",
                code="render.foreign_fence",
                phase="fence",
                details={},
            )
        if fence.submission not in self._submissions:
            raise _device_error(
                "render fence does not identify an existing submission",
                code="render.invalid_fence",
                phase="fence",
                details={},
            )

    def _guard(self, operation: str) -> None:
        self._assert_owner_thread()
        if self._closed:
            raise _device_error(
                "render device is closed",
                code="render.device_closed",
                phase=operation,
                details={"operation": operation},
            )

    def _assert_owner_thread(self) -> None:
        if threading.get_ident() != self._owner_thread:
            raise _device_error(
                "render device operations must run on the constructing thread",
                code="render.thread_violation",
                phase="ownership",
                details={"owner": "constructing_thread", "caller": "different_thread"},
            )


def _invalid_descriptor(resource: str) -> RenderError:
    return _device_error(
        "render resource descriptor or initial data is invalid",
        code="render.invalid_descriptor",
        phase="create",
        details={"resource": resource},
    )


def _invalid_usage(resource: str) -> RenderError:
    return _device_error(
        "render resource usage is incompatible with the command",
        code="render.invalid_usage",
        phase="submit",
        details={"resource": resource},
    )


def _device_error(
    message: str,
    *,
    code: str,
    phase: str,
    details: dict[str, str | int | float | bool | None],
) -> RenderError:
    return RenderError(
        message,
        code=code,
        subsystem="render",
        phase=phase,
        details=details,
    )
