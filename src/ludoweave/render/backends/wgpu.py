# pyright: reportMissingTypeStubs=false, reportPossiblyUnboundVariable=false
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
# pyright: reportArgumentType=false, reportAttributeAccessIssue=false
"""Private wgpu-py/rendercanvas adapter behind engine-owned render contracts."""

from __future__ import annotations

import struct
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Never, Protocol, cast
from uuid import UUID, uuid4

from ludoweave.core.errors import RenderError
from ludoweave.render._sprite import (
    SPRITE_INSTANCE_STRIDE,
    SPRITE_SHADER,
    debug_instances,
    pack_sprite_instances,
    tile_instances,
)
from ludoweave.render.backends.null_device import NullRenderDevice
from ludoweave.render.contracts import (
    BlendMode,
    BufferData,
    BufferDescriptor,
    BufferUsage,
    CaptureImage,
    ClearCommand,
    Color,
    CommandList,
    DebugLineCommand,
    DiagnosticTextCommand,
    PipelineDescriptor,
    PrimitiveTopology,
    RenderCapabilities,
    SpriteBatchCommand,
    SpriteInstance,
    Submission,
    SurfaceDescriptor,
    SurfaceKind,
    TextureData,
    TextureDescriptor,
    TextureFormat,
    TextureUsage,
    TileBatchCommand,
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

try:
    import wgpu
    from rendercanvas.glfw import RenderCanvas as GlfwRenderCanvas
    from rendercanvas.offscreen import OffscreenRenderCanvas
except ImportError as dependency_error:
    _dependency_import_error: ImportError | None = dependency_error
else:
    _dependency_import_error = None


class _NativeTexture(Protocol):
    def create_view(self) -> object: ...


class _CanvasContext(Protocol):
    def configure(self, **kwargs: object) -> None: ...

    def get_current_texture(self) -> _NativeTexture: ...


class _CaptureArray(Protocol):
    def tobytes(self) -> bytes: ...


class _Canvas(Protocol):
    def get_wgpu_context(self) -> _CanvasContext: ...

    def request_draw(self, draw_function: Callable[[], None]) -> None: ...

    def draw(self) -> _CaptureArray: ...

    def force_draw(self) -> None: ...

    def set_logical_size(self, width: float, height: float) -> None: ...

    def close(self) -> None: ...


@dataclass(slots=True)
class _Surface:
    descriptor: SurfaceDescriptor
    canvas: _Canvas
    context: _CanvasContext
    capture: CaptureImage | None = None
    width: int = 0
    height: int = 0
    suspended: bool = False


@dataclass(slots=True)
class _Texture:
    descriptor: TextureDescriptor
    texture: _NativeTexture


@dataclass(slots=True)
class _Pipeline:
    descriptor: PipelineDescriptor
    pipeline: object
    bind_group_layout: object


@dataclass(slots=True)
class _RetiredNative:
    value: object
    retire_after: int


class _RenderPass(Protocol):
    def set_pipeline(self, pipeline: object) -> None: ...

    def set_bind_group(self, index: int, bind_group: object) -> None: ...

    def set_vertex_buffer(
        self, slot: int, buffer: object, offset: int = 0, size: int | None = None
    ) -> None: ...

    def draw(
        self,
        vertex_count: int,
        instance_count: int = 1,
        first_vertex: int = 0,
        first_instance: int = 0,
    ) -> None: ...

    def end(self) -> None: ...


class _Encoder(Protocol):
    def begin_render_pass(self, **descriptor: object) -> _RenderPass: ...

    def finish(self) -> object: ...


class WgpuRenderDevice:
    """Optional production device; no native object crosses its public methods."""

    __slots__ = (
        "_adapter",
        "_closed",
        "_debug_pipelines",
        "_device",
        "_loss_reason",
        "_lost",
        "_native",
        "_queue",
        "_retired",
        "_sampler",
        "_surfaces",
        "_validator",
        "_white_texture",
    )

    def __init__(
        self,
        *,
        power_preference: str = "low-power",
        force_fallback_adapter: bool = False,
        scope: UUID | None = None,
    ) -> None:
        if _dependency_import_error is not None:
            raise _backend_error(
                "optional graphics dependencies are not installed",
                code="render.backend_dependency_missing",
                phase="initialize",
                details={"install": "pip install ludoweave[graphics]"},
            ) from _dependency_import_error
        if type(power_preference) is not str or power_preference not in (
            "low-power",
            "high-performance",
        ):
            raise _backend_error(
                "power preference is unsupported",
                code="render.invalid_descriptor",
                phase="initialize",
                details={"field": "power_preference"},
            )
        if type(force_fallback_adapter) is not bool:
            raise _backend_error(
                "fallback-adapter preference must be a boolean",
                code="render.invalid_descriptor",
                phase="initialize",
                details={"field": "force_fallback_adapter"},
            )
        selected_scope = uuid4() if scope is None else scope
        self._validator = NullRenderDevice(scope=selected_scope)
        try:
            adapter = wgpu.gpu.request_adapter_sync(
                power_preference=power_preference,
                force_fallback_adapter=force_fallback_adapter,
            )
        except Exception as error:
            self._validator.close()
            raise _backend_error(
                "wgpu adapter request failed",
                code="render.adapter_unavailable",
                phase="initialize",
                details={"backend": "wgpu", "fallback": force_fallback_adapter},
            ) from error
        try:
            device = adapter.request_device_sync(label="ludoweave-render-device")
        except Exception as error:
            self._validator.close()
            raise _backend_error(
                "wgpu device request failed",
                code="render.device_request_failed",
                phase="initialize",
                details={"backend": "wgpu"},
            ) from error
        try:
            queue = device.queue
            sampler = device.create_sampler(
                label="ludoweave-nearest-sampler",
                mag_filter="nearest",
                min_filter="nearest",
            )
            white_texture = device.create_texture(
                label="ludoweave-white-texture",
                size=(1, 1, 1),
                format="rgba8unorm",
                usage=wgpu.TextureUsage.TEXTURE_BINDING | wgpu.TextureUsage.COPY_DST,
            )
            queue.write_texture(
                {"texture": white_texture},
                b"\xff\xff\xff\xff",
                {"bytes_per_row": 4, "rows_per_image": 1},
                (1, 1, 1),
            )
        except Exception as error:
            self._validator.close()
            _close_native(device)
            raise _backend_error(
                "wgpu built-in resources could not be initialized",
                code="render.device_initialization_failed",
                phase="initialize",
                details={"backend": "wgpu"},
            ) from error
        self._adapter = adapter
        self._device = device
        self._queue = queue
        self._sampler = sampler
        self._white_texture = cast(_NativeTexture, white_texture)
        self._debug_pipelines: dict[TextureFormat, _Pipeline] = {}
        self._native: dict[tuple[type[object], int, int], object] = {}
        self._surfaces: dict[tuple[int, int], _Surface] = {}
        self._retired: list[_RetiredNative] = []
        self._closed = False
        self._lost = False
        self._loss_reason = "none"

    @property
    def name(self) -> str:
        return "wgpu"

    @property
    def scope(self) -> UUID:
        return self._validator.scope

    @property
    def capabilities(self) -> RenderCapabilities:
        self._guard("capabilities")
        limits = cast(Mapping[str, int], self._adapter.limits)
        maximum = min(
            16_384,
            int(
                limits.get(
                    "max-texture-dimension-2d",
                    limits.get("max_texture_dimension_2d", 8192),
                )
            ),
        )
        return RenderCapabilities(
            backend="wgpu",
            max_texture_dimension_2d=maximum,
            offscreen_capture=True,
            # M3 exposes CPU submission evidence. Timestamp-query collection
            # is not advertised until an engine-owned result contract exists.
            timestamp_queries=False,
            surface_formats=(
                TextureFormat.RGBA8_UNORM,
                TextureFormat.RGBA8_UNORM_SRGB,
                TextureFormat.BGRA8_UNORM,
                TextureFormat.BGRA8_UNORM_SRGB,
            ),
        )

    def create_buffer(
        self, descriptor: BufferDescriptor, data: BufferData | None = None
    ) -> BufferHandle:
        self._guard("create_buffer")
        handle = self._validator.create_buffer(descriptor, data)
        native: object
        try:
            native = self._device.create_buffer(
                label=descriptor.label,
                size=descriptor.size,
                usage=_buffer_usage(descriptor.usage),
            )
            if data is not None and data.value:
                self._queue.write_buffer(native, 0, data.value)
        except Exception as error:
            self._lose(error, operation="create_buffer")
        self._native[_key(handle)] = native
        return handle

    def create_texture(
        self, descriptor: TextureDescriptor, data: TextureData | None = None
    ) -> TextureHandle:
        self._guard("create_texture")
        handle = self._validator.create_texture(descriptor, data)
        if descriptor.width > self.capabilities.max_texture_dimension_2d or (
            descriptor.height > self.capabilities.max_texture_dimension_2d
        ):
            self._validator.destroy(handle)
            raise _backend_error(
                "texture exceeds the selected adapter limits",
                code="render.unsupported_descriptor",
                phase="create_texture",
                details={"resource": "texture"},
            )
        native: object
        try:
            native = self._device.create_texture(
                label=descriptor.label,
                size=(descriptor.width, descriptor.height, descriptor.layers),
                format=_texture_format(descriptor.format),
                usage=_texture_usage(descriptor.usage),
            )
            if data is not None:
                self._queue.write_texture(
                    {"texture": native},
                    data.value,
                    {"bytes_per_row": data.bytes_per_row, "rows_per_image": descriptor.height},
                    (descriptor.width, descriptor.height, descriptor.layers),
                )
        except Exception as error:
            self._lose(error, operation="create_texture")
        self._native[_key(handle)] = _Texture(descriptor, cast(_NativeTexture, native))
        return handle

    def create_pipeline(self, descriptor: PipelineDescriptor) -> PipelineHandle:
        self._guard("create_pipeline")
        handle = self._validator.create_pipeline(descriptor)
        try:
            self._native[_key(handle)] = self._make_pipeline(descriptor)
        except Exception as error:
            self._validator.destroy(handle)
            self._lose(error, operation="create_pipeline")
        return handle

    def create_surface(self, descriptor: SurfaceDescriptor) -> SurfaceHandle:
        self._guard("create_surface")
        handle = self._validator.create_surface(descriptor)
        if descriptor.width > self.capabilities.max_texture_dimension_2d or (
            descriptor.height > self.capabilities.max_texture_dimension_2d
        ):
            self._validator.destroy(handle)
            raise _backend_error(
                "surface exceeds the selected adapter limits",
                code="render.unsupported_descriptor",
                phase="create_surface",
                details={"resource": "surface"},
            )
        canvas: _Canvas | None = None
        try:
            if descriptor.kind is SurfaceKind.OFFSCREEN:
                canvas = cast(
                    _Canvas,
                    OffscreenRenderCanvas(
                        size=(descriptor.width, descriptor.height), format="rgba-u8"
                    ),
                )
            else:
                canvas = cast(
                    _Canvas,
                    GlfwRenderCanvas(
                        size=(descriptor.width, descriptor.height), title=descriptor.label
                    ),
                )
            context = canvas.get_wgpu_context()
            context.configure(
                device=self._device,
                format=_texture_format(descriptor.format),
                usage=wgpu.TextureUsage.RENDER_ATTACHMENT | wgpu.TextureUsage.COPY_SRC,
            )
        except Exception as error:
            if canvas is not None:
                _close_native(canvas)
            self._validator.destroy(handle)
            raise _backend_error(
                "render surface could not be created",
                code="render.surface_unavailable",
                phase="create_surface",
                details={"kind": descriptor.kind.value},
            ) from error
        self._surfaces[(handle.index, handle.generation)] = _Surface(
            descriptor,
            canvas,
            context,
            width=descriptor.width,
            height=descriptor.height,
        )
        self._native[_key(handle)] = canvas
        return handle

    def submit(self, command_lists: Sequence[CommandList]) -> Submission:
        self._guard("submit")
        report = self._validator.submit(command_lists)
        try:
            for command_list in report.command_lists:
                self._render_command_list(command_list, report.fence.submission)
        except RenderError:
            raise
        except Exception as error:
            self._lose(error, operation="submit")
        return report

    def submit_graph(self, graph: RenderGraph | CompiledRenderGraph) -> Submission:
        compiled = graph.compile() if type(graph) is RenderGraph else graph
        if type(compiled) is not CompiledRenderGraph:
            raise _backend_error(
                "render graph submission requires an exact graph",
                code="render.invalid_graph",
                phase="submit",
                details={"field": "graph"},
            )
        return self.submit(compiled.command_lists)

    def is_fence_complete(self, fence: FenceHandle) -> bool:
        self._guard("is_fence_complete")
        return self._validator.is_fence_complete(fence)

    def poll(self) -> None:
        self._guard("poll")
        try:
            # wgpu-py 0.32's native queue callback has an ABI mismatch on
            # Windows. Polling the native device to idle is the provider's
            # equivalent completion primitive and keeps that workaround
            # isolated inside this exact adapter.
            self._device._poll_wait()
        except Exception as error:
            self._lose(error, operation="poll")
        self._validator.poll()
        completed = self._validator.completed_submission
        remaining: list[_RetiredNative] = []
        for retired in self._retired:
            if retired.retire_after <= completed:
                _close_native(retired.value)
            else:
                remaining.append(retired)
        self._retired = remaining

    def destroy(self, handle: RenderResourceHandle) -> None:
        self._guard("destroy")
        key = _key(handle)
        last_submission = self._validator.last_submission_for(handle)
        native = self._native.get(key)
        surface = (
            self._surfaces.get((handle.index, handle.generation))
            if type(handle) is SurfaceHandle
            else None
        )
        # Validator performs all owner/kind/generation checks before native state
        # changes and immediately retires the logical handle.
        self._validator.destroy(handle)
        self._native.pop(key, None)
        if surface is not None:
            self._surfaces.pop((handle.index, handle.generation), None)
        if native is None:
            return
        if last_submission > self._validator.completed_submission:
            self._retired.append(_RetiredNative(native, last_submission))
        else:
            _close_native(native)

    def capture_surface(self, handle: SurfaceHandle) -> CaptureImage:
        self._guard("capture_surface")
        self._validator.validate_handle(handle)
        surface = self._surfaces.get((handle.index, handle.generation))
        if surface is None or surface.descriptor.kind is not SurfaceKind.OFFSCREEN:
            raise _backend_error(
                "surface does not support offscreen capture",
                code="render.capability_missing",
                phase="capture",
                details={"feature": "offscreen_capture"},
            )
        if surface.capture is None:
            raise _backend_error(
                "surface has not produced a frame",
                code="render.capture_unavailable",
                phase="capture",
                details={},
            )
        return surface.capture

    def resize_surface(self, handle: SurfaceHandle, width: int, height: int) -> None:
        self._guard("resize_surface")
        self._validator.resize_surface(handle, width, height)
        surface = self._surfaces[(handle.index, handle.generation)]
        if width == 0:
            surface.suspended = True
            surface.capture = None
            return
        try:
            surface.canvas.set_logical_size(float(width), float(height))
        except Exception as error:
            self._lose(error, operation="resize_surface")
        surface.descriptor = SurfaceDescriptor(
            width,
            height,
            surface.descriptor.format,
            surface.descriptor.kind,
            surface.descriptor.label,
        )
        surface.width = width
        surface.height = height
        surface.suspended = False
        surface.capture = None

    def simulate_device_loss(self) -> None:
        """Inject a deterministic fatal loss for adapter conformance tests."""

        self._guard("simulate_device_loss")
        self._lost = True
        self._loss_reason = "simulated"

    def close(self) -> None:
        if self._closed:
            return
        try:
            if not self._lost and self._validator.completed_submission < (
                self._validator.latest_submission
            ):
                self.poll()
        finally:
            for native in tuple(self._native.values()):
                _close_native(native)
            for retired in self._retired:
                _close_native(retired.value)
            self._native.clear()
            self._surfaces.clear()
            self._retired.clear()
            for pipeline in self._debug_pipelines.values():
                _close_native(pipeline)
            self._debug_pipelines.clear()
            _close_native(self._white_texture)
            _close_native(self._sampler)
            self._validator.close()
            _close_native(self._device)
            self._closed = True

    def _render_command_list(self, command_list: CommandList, retire_after: int) -> None:
        target = command_list.target
        if target is None:
            target = next(
                (
                    command.target
                    for command in command_list.commands
                    if type(command) is ClearCommand
                ),
                None,
            )
        if target is None or not command_list.commands:
            return
        if type(target) is TextureHandle:
            texture = cast(_Texture, self._native[_key(target)])
            encoder = self._device.create_command_encoder(label=command_list.label)
            self._encode_commands(
                encoder,
                texture.texture.create_view(),
                texture.descriptor.format,
                command_list,
                retire_after,
            )
            self._queue.submit((encoder.finish(),))
            return

        surface = self._surfaces[(target.index, target.generation)]
        if surface.suspended:
            return

        def draw_frame() -> None:
            current = surface.context.get_current_texture()
            encoder = self._device.create_command_encoder(label=command_list.label)
            self._encode_commands(
                encoder,
                current.create_view(),
                surface.descriptor.format,
                command_list,
                retire_after,
            )
            self._queue.submit((encoder.finish(),))

        surface.canvas.request_draw(draw_frame)
        if surface.descriptor.kind is SurfaceKind.OFFSCREEN:
            image = surface.canvas.draw()
            surface.capture = CaptureImage(
                surface.width,
                surface.height,
                image.tobytes(),
                TextureFormat.RGBA8_UNORM,
            )
        else:
            surface.canvas.force_draw()

    def _encode_commands(
        self,
        encoder: _Encoder,
        target_view: object,
        target_format: TextureFormat,
        command_list: CommandList,
        retire_after: int,
    ) -> None:
        clear = next(
            (command for command in command_list.commands if type(command) is ClearCommand),
            None,
        )
        clear_color = Color() if clear is None else clear.color
        render_pass = encoder.begin_render_pass(
            color_attachments=(
                {
                    "view": target_view,
                    "resolve_target": None,
                    "clear_value": (
                        clear_color.red,
                        clear_color.green,
                        clear_color.blue,
                        clear_color.alpha,
                    ),
                    "load_op": "load" if clear is None else "clear",
                    "store_op": "store",
                },
            )
        )
        debug_commands: list[DebugLineCommand | DiagnosticTextCommand] = []
        for command in command_list.commands:
            if type(command) is SpriteBatchCommand:
                pipeline = cast(_Pipeline, self._native[_key(command.pipeline)])
                texture = cast(_Texture, self._native[_key(command.texture)])
                self._encode_batch(
                    render_pass,
                    pipeline,
                    texture.texture,
                    command.instances,
                    command_list.camera_matrix,
                    retire_after,
                )
            elif type(command) is TileBatchCommand:
                pipeline = cast(_Pipeline, self._native[_key(command.pipeline)])
                texture = cast(_Texture, self._native[_key(command.texture)])
                self._encode_batch(
                    render_pass,
                    pipeline,
                    texture.texture,
                    tile_instances(command),
                    command_list.camera_matrix,
                    retire_after,
                )
            elif type(command) in (DebugLineCommand, DiagnosticTextCommand):
                debug_commands.append(cast(DebugLineCommand | DiagnosticTextCommand, command))
        if debug_commands:
            pipeline = self._debug_pipelines.get(target_format)
            if pipeline is None:
                pipeline = self._make_pipeline(PipelineDescriptor(target_format))
                self._debug_pipelines[target_format] = pipeline
            self._encode_batch(
                render_pass,
                pipeline,
                self._white_texture,
                debug_instances(debug_commands),
                command_list.camera_matrix,
                retire_after,
            )
        render_pass.end()

    def _encode_batch(
        self,
        render_pass: _RenderPass,
        pipeline: _Pipeline,
        texture: _NativeTexture,
        instances: Sequence[SpriteInstance],
        camera_matrix: tuple[float, ...],
        retire_after: int,
    ) -> None:
        packed_instances = pack_sprite_instances(instances)
        instance_buffer = self._device.create_buffer(
            label="ludoweave-sprite-instances",
            size=len(packed_instances),
            usage=wgpu.BufferUsage.VERTEX | wgpu.BufferUsage.COPY_DST,
        )
        camera_data = struct.pack("<16f", *camera_matrix)
        camera_buffer = self._device.create_buffer(
            label="ludoweave-camera",
            size=len(camera_data),
            usage=wgpu.BufferUsage.UNIFORM | wgpu.BufferUsage.COPY_DST,
        )
        self._queue.write_buffer(instance_buffer, 0, packed_instances)
        self._queue.write_buffer(camera_buffer, 0, camera_data)
        bind_group = self._device.create_bind_group(
            label="ludoweave-sprite-bindings",
            layout=pipeline.bind_group_layout,
            entries=(
                {
                    "binding": 0,
                    "resource": {"buffer": camera_buffer, "offset": 0, "size": len(camera_data)},
                },
                {"binding": 1, "resource": texture.create_view()},
                {"binding": 2, "resource": self._sampler},
            ),
        )
        render_pass.set_pipeline(pipeline.pipeline)
        render_pass.set_bind_group(0, bind_group)
        render_pass.set_vertex_buffer(0, instance_buffer, 0, len(packed_instances))
        render_pass.draw(6, len(instances), 0, 0)
        self._retired.extend(
            (
                _RetiredNative(instance_buffer, retire_after),
                _RetiredNative(camera_buffer, retire_after),
            )
        )

    def _make_pipeline(self, descriptor: PipelineDescriptor) -> _Pipeline:
        shader = self._device.create_shader_module(
            label="ludoweave-sprite-shader",
            code=SPRITE_SHADER,
        )
        bind_group_layout = self._device.create_bind_group_layout(
            label="ludoweave-sprite-bind-group-layout",
            entries=(
                {
                    "binding": 0,
                    "visibility": wgpu.ShaderStage.VERTEX,
                    "buffer": {"type": "uniform"},
                },
                {
                    "binding": 1,
                    "visibility": wgpu.ShaderStage.FRAGMENT,
                    "texture": {"sample_type": "float", "view_dimension": "2d"},
                },
                {
                    "binding": 2,
                    "visibility": wgpu.ShaderStage.FRAGMENT,
                    "sampler": {"type": "filtering"},
                },
            ),
        )
        layout = self._device.create_pipeline_layout(
            label="ludoweave-sprite-pipeline-layout",
            bind_group_layouts=(bind_group_layout,),
        )
        pipeline = self._device.create_render_pipeline(
            label=descriptor.label,
            layout=layout,
            vertex={
                "module": shader,
                "entry_point": "vs_main",
                "buffers": (
                    {
                        "array_stride": SPRITE_INSTANCE_STRIDE,
                        "step_mode": "instance",
                        "attributes": tuple(
                            {
                                "format": "float32x4",
                                "offset": offset,
                                "shader_location": location,
                            }
                            for location, offset in enumerate((0, 16, 32, 48))
                        ),
                    },
                ),
            },
            primitive={
                "topology": _primitive_topology(descriptor.topology),
                "front_face": "ccw",
                "cull_mode": "none",
            },
            fragment={
                "module": shader,
                "entry_point": "fs_main",
                "targets": (
                    {
                        "format": _texture_format(descriptor.color_format),
                        "blend": _blend_state(descriptor.blend),
                        "write_mask": wgpu.ColorWrite.ALL,
                    },
                ),
            },
        )
        return _Pipeline(descriptor, pipeline, bind_group_layout)

    def _lose(self, error: Exception, *, operation: str) -> Never:
        self._lost = True
        self._loss_reason = "provider_error"
        raise _backend_error(
            "wgpu device operation failed and the backend was marked lost",
            code="render.device_lost",
            phase=operation,
            details={"backend": "wgpu", "recoverable": False, "reason": self._loss_reason},
        ) from error

    def _guard(self, operation: str) -> None:
        if self._closed:
            raise _backend_error(
                "wgpu render device is closed",
                code="render.device_closed",
                phase=operation,
                details={"operation": operation},
            )
        if self._lost:
            raise _backend_error(
                "wgpu render device is lost",
                code="render.device_lost",
                phase=operation,
                details={"backend": "wgpu", "recoverable": False, "reason": self._loss_reason},
            )


def _key(
    handle: BufferHandle | TextureHandle | PipelineHandle | SurfaceHandle,
) -> tuple[type[object], int, int]:
    return (type(handle), handle.index, handle.generation)


def _buffer_usage(value: BufferUsage) -> int:
    result = 0
    mapping = (
        (BufferUsage.VERTEX, wgpu.BufferUsage.VERTEX),
        (BufferUsage.INDEX, wgpu.BufferUsage.INDEX),
        (BufferUsage.UNIFORM, wgpu.BufferUsage.UNIFORM),
        (BufferUsage.COPY_SOURCE, wgpu.BufferUsage.COPY_SRC),
        (BufferUsage.COPY_DESTINATION, wgpu.BufferUsage.COPY_DST),
    )
    for engine_flag, native_flag in mapping:
        if value & engine_flag:
            result |= native_flag
    return result


def _texture_usage(value: TextureUsage) -> int:
    result = 0
    mapping = (
        (TextureUsage.SAMPLED, wgpu.TextureUsage.TEXTURE_BINDING),
        (TextureUsage.RENDER_ATTACHMENT, wgpu.TextureUsage.RENDER_ATTACHMENT),
        (TextureUsage.COPY_SOURCE, wgpu.TextureUsage.COPY_SRC),
        (TextureUsage.COPY_DESTINATION, wgpu.TextureUsage.COPY_DST),
    )
    for engine_flag, native_flag in mapping:
        if value & engine_flag:
            result |= native_flag
    return result


def _texture_format(value: TextureFormat) -> str:
    return {
        TextureFormat.RGBA8_UNORM: "rgba8unorm",
        TextureFormat.RGBA8_UNORM_SRGB: "rgba8unorm-srgb",
        TextureFormat.BGRA8_UNORM: "bgra8unorm",
        TextureFormat.BGRA8_UNORM_SRGB: "bgra8unorm-srgb",
    }[value]


def _primitive_topology(value: PrimitiveTopology) -> str:
    return {
        PrimitiveTopology.TRIANGLE_LIST: "triangle-list",
        PrimitiveTopology.LINE_LIST: "line-list",
    }[value]


def _blend_state(value: BlendMode) -> dict[str, dict[str, str]] | None:
    if value is BlendMode.OPAQUE:
        return None
    destination = "one" if value is BlendMode.ADDITIVE else "one-minus-src-alpha"
    return {
        "color": {
            "operation": "add",
            "src_factor": "src-alpha",
            "dst_factor": destination,
        },
        "alpha": {
            "operation": "add",
            "src_factor": "one",
            "dst_factor": destination,
        },
    }


def _close_native(value: object) -> None:
    if type(value) is _Texture:
        _close_native(value.texture)
        return
    if type(value) is _Pipeline:
        _close_native(value.pipeline)
        _close_native(value.bind_group_layout)
        return
    close = getattr(value, "close", None)
    destroy = getattr(value, "destroy", None)
    if callable(close):
        close()
    elif callable(destroy):
        destroy()


def _backend_error(
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
