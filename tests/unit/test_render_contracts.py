"""Backend-neutral M3 descriptors, handles, extraction, and Null device tests."""

import gc
import math
import threading
from dataclasses import FrozenInstanceError
from uuid import UUID

import pytest

from ludoweave.core.errors import RenderError
from ludoweave.ecs import ComponentRegistry, ResourceRegistry, ResourceStore, World
from ludoweave.render import (
    BlendMode,
    BufferData,
    BufferDescriptor,
    BufferHandle,
    BufferUsage,
    Camera2D,
    ClearCommand,
    Color,
    CommandList,
    NullRenderBackend,
    NullRenderDevice,
    PipelineDescriptor,
    PipelineHandle,
    PrimitiveTopology,
    RenderDescriptor,
    RenderExtractor,
    SpriteBatchCommand,
    SpriteExtractionSource,
    SurfaceDescriptor,
    SurfaceHandle,
    TextureData,
    TextureDescriptor,
    TextureFormat,
    TextureHandle,
    TextureUsage,
)
from ludoweave.world import CanonicalJsonError, WorldSession, canonical_dumps

SCOPE = UUID("602f8176-58cd-4c15-b011-f5787a646887")
OTHER_SCOPE = UUID("4502b1a5-ef88-4bb8-aa2a-b46825cf94dc")


def _texture_descriptor() -> TextureDescriptor:
    return TextureDescriptor(
        2,
        2,
        TextureFormat.RGBA8_UNORM,
        TextureUsage.SAMPLED | TextureUsage.COPY_DESTINATION,
    )


def test_render_descriptors_are_frozen_slotted_and_exactly_validated() -> None:
    descriptor = BufferDescriptor(16, BufferUsage.VERTEX | BufferUsage.COPY_DESTINATION)
    with pytest.raises(FrozenInstanceError):
        descriptor.size = 8  # type: ignore[misc]
    assert not hasattr(descriptor, "__dict__")

    for invalid in (0, -1, True, 1.0, "1", None, 2**31):
        with pytest.raises(RenderError) as raised:
            BufferDescriptor(invalid, BufferUsage.VERTEX)  # type: ignore[arg-type]
        assert raised.value.code == "render.invalid_descriptor"
        assert raised.value.phase == "descriptor"

    for invalid in (0, True, 1, "sampled", None):
        with pytest.raises(RenderError):
            TextureDescriptor(
                1,
                1,
                TextureFormat.RGBA8_UNORM,
                invalid,  # type: ignore[arg-type]
            )


def test_descriptor_error_does_not_call_hostile_repr_and_null_requires_exact_type() -> None:
    class Hostile:
        def __repr__(self) -> str:
            raise RuntimeError("boom")

    with pytest.raises(RenderError) as raised:
        RenderDescriptor(width=Hostile())  # type: ignore[arg-type]
    assert raised.value.__cause__ is None

    backend = NullRenderBackend()
    with pytest.raises(RenderError):
        backend.initialize(object())  # type: ignore[arg-type]
    assert backend.descriptor is None


def test_buffer_and_texture_initial_data_are_detached_and_bounded() -> None:
    device = NullRenderDevice(scope=SCOPE)
    raw = bytearray(b"abcd")
    data = BufferData(bytes(raw))
    raw[:] = b"zzzz"
    handle = device.create_buffer(BufferDescriptor(4, BufferUsage.VERTEX), data)
    assert handle == BufferHandle(SCOPE, 0, 0)

    texture_data = TextureData(bytes(range(16)), bytes_per_row=8)
    texture = device.create_texture(_texture_descriptor(), texture_data)
    assert texture == TextureHandle(SCOPE, 1, 0)
    with pytest.raises(RenderError):
        device.create_buffer(BufferDescriptor(2, BufferUsage.VERTEX), BufferData(b"abc"))
    assert device.live_resource_count == 2


def test_handle_retirement_is_immediate_and_physical_reuse_waits_for_fence() -> None:
    device = NullRenderDevice(scope=SCOPE)
    texture = device.create_texture(_texture_descriptor())
    pipeline = device.create_pipeline(
        PipelineDescriptor(TextureFormat.RGBA8_UNORM, blend=BlendMode.ALPHA)
    )
    surface = device.create_surface(SurfaceDescriptor(64, 64, TextureFormat.RGBA8_UNORM))
    sprite = SpriteExtractionSource(
        texture,
        1,
        0,
        0.0,
        0.0,
        1.0,
        1.0,
        0.0,
        0.0,
        1.0,
        1.0,
    )
    frame = RenderExtractor().extract_sprites(
        (sprite,), completed_ticks=1, interpolation_alpha=0.5, camera=Camera2D()
    )
    submission = device.submit(
        (
            CommandList(
                "frame",
                (
                    ClearCommand(surface, Color()),
                    SpriteBatchCommand(pipeline, texture, frame.sprite_groups[0].instances),
                ),
                surface,
            ),
        )
    )
    assert submission.draw_calls == 1
    assert submission.sprite_instances == 1
    assert not device.is_fence_complete(submission.fence)

    device.destroy(texture)
    assert device.live_resource_count == 2
    assert device.pending_destruction_count == 1
    with pytest.raises(RenderError) as stale:
        device.destroy(texture)
    assert stale.value.code == "render.stale_handle"

    replacement_before_completion = device.create_texture(_texture_descriptor())
    assert replacement_before_completion.index != texture.index
    device.complete_through(submission.fence.submission)
    assert device.pending_destruction_count == 0
    replacement_after_completion = device.create_texture(_texture_descriptor())
    assert replacement_after_completion.index == texture.index
    assert replacement_after_completion.generation == texture.generation + 1


def test_foreign_wrong_kind_stale_closed_and_thread_failures_are_structured() -> None:
    device = NullRenderDevice(scope=SCOPE)
    texture = device.create_texture(_texture_descriptor())
    with pytest.raises(RenderError) as foreign:
        device.destroy(TextureHandle(OTHER_SCOPE, texture.index, texture.generation))
    assert foreign.value.code == "render.foreign_handle"
    with pytest.raises(RenderError) as wrong_kind:
        device.destroy(BufferHandle(SCOPE, texture.index, texture.generation))
    assert wrong_kind.value.code == "render.wrong_handle_kind"

    errors: list[RenderError] = []

    def use_from_thread() -> None:
        try:
            device.destroy(texture)
        except RenderError as error:
            errors.append(error)

    worker = threading.Thread(target=use_from_thread)
    worker.start()
    worker.join()
    assert [error.code for error in errors] == ["render.thread_violation"]
    assert device.live_resource_count == 1

    device.close()
    device.close()
    with pytest.raises(RenderError) as closed:
        device.create_texture(_texture_descriptor())
    assert closed.value.code == "render.device_closed"
    with pytest.raises(RenderError) as closed_gamepads:
        device.poll_gamepads()
    assert closed_gamepads.value.code == "render.device_closed"


def test_python_handle_gc_does_not_release_resources() -> None:
    device = NullRenderDevice(scope=SCOPE)
    handle = device.create_texture(_texture_descriptor())
    del handle
    gc.collect()
    assert device.live_resource_count == 1
    device.close()
    assert device.physical_resource_count == 0


def test_extraction_is_immutable_sorted_grouped_and_non_authoritative() -> None:
    device = NullRenderDevice(scope=SCOPE)
    texture_b = device.create_texture(_texture_descriptor())
    texture_a = device.create_texture(_texture_descriptor())
    sources = [
        SpriteExtractionSource(
            texture_a,
            2,
            0,
            0.0,
            0.0,
            4.0,
            2.0,
            0.0,
            1.0,
            2.0,
            2.0,
            layer=1,
            z=0.5,
        ),
        SpriteExtractionSource(
            texture_b,
            1,
            0,
            0.0,
            0.0,
            2.0,
            4.0,
            0.0,
            0.0,
            1.0,
            1.0,
        ),
    ]
    extractor = RenderExtractor()
    frame = extractor.extract_sprites(
        reversed(sources), completed_ticks=0, interpolation_alpha=0.5, camera=Camera2D()
    )
    repeated = extractor.extract_sprites(
        reversed(sources), completed_ticks=0, interpolation_alpha=0.5, camera=Camera2D()
    )
    assert frame == repeated
    assert frame.source_tick is None
    assert frame.visible_sprite_count == 2
    assert tuple(group.texture.index for group in frame.sprite_groups) == (0, 1)
    assert frame.sprite_groups[1].instances[0].x == 2.0
    sources.clear()
    assert frame.visible_sprite_count == 2

    session = WorldSession(
        "render-authority",
        World(ComponentRegistry()),
        ResourceStore(ResourceRegistry()),
    )
    before = session.state_hash
    extractor.extract_sprites(
        (), completed_ticks=1, interpolation_alpha=0.25, camera=Camera2D(zoom=2.0)
    )
    assert session.state_hash == before
    with pytest.raises(CanonicalJsonError):
        canonical_dumps(frame)


@pytest.mark.parametrize("alpha", [True, -0.1, 1.1, float("nan"), float("inf")])
def test_extraction_rejects_invalid_interpolation_without_state(alpha: object) -> None:
    with pytest.raises(RenderError):
        RenderExtractor().extract_sprites(
            (),
            completed_ticks=0,
            interpolation_alpha=alpha,  # type: ignore[arg-type]
            camera=Camera2D(),
        )


def test_extraction_rejects_forged_unvalidated_source_record() -> None:
    forged = object.__new__(SpriteExtractionSource)
    with pytest.raises(RenderError) as raised:
        RenderExtractor().extract_sprites(
            (forged,), completed_ticks=0, interpolation_alpha=0.5, camera=Camera2D()
        )
    assert raised.value.code == "render.invalid_extraction"
    assert dict(raised.value.details)["field"] == "sources"


def test_extraction_rejects_finite_endpoints_whose_interpolation_overflows() -> None:
    source = SpriteExtractionSource(
        TextureHandle(SCOPE, 0, 0),
        0,
        0,
        -1e308,
        0.0,
        1e308,
        0.0,
        0.0,
        0.0,
        1.0,
        1.0,
    )
    with pytest.raises(RenderError) as raised:
        RenderExtractor().extract_sprites(
            (source,), completed_ticks=0, interpolation_alpha=0.5, camera=Camera2D()
        )
    assert raised.value.code == "render.invalid_extraction"
    assert dict(raised.value.details)["field"] == "interpolation"


def test_camera_matrix_includes_translation_zoom_and_rotation() -> None:
    matrix = Camera2D(
        x=2.0,
        y=3.0,
        viewport_width=4.0,
        viewport_height=2.0,
        rotation_radians=math.pi / 2.0,
        zoom=2.0,
    ).orthographic_matrix()
    assert matrix[0] == pytest.approx(0.0, abs=1e-12)
    assert matrix[1] == pytest.approx(-2.0)
    assert matrix[4] == pytest.approx(1.0)
    assert matrix[5] == pytest.approx(0.0, abs=1e-12)
    assert matrix[12] == pytest.approx(-3.0)
    assert matrix[13] == pytest.approx(4.0)


def test_draw_command_lists_require_explicit_target_and_valid_camera() -> None:
    pipeline = PipelineHandle(SCOPE, 0, 0)
    texture = TextureHandle(SCOPE, 1, 0)
    surface = SurfaceHandle(SCOPE, 2, 0)
    instance = SpriteExtractionSource(
        texture,
        0,
        0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        1.0,
    )
    frame = RenderExtractor().extract_sprites(
        (instance,), completed_ticks=1, interpolation_alpha=0.0, camera=Camera2D()
    )
    command = SpriteBatchCommand(pipeline, texture, frame.sprite_groups[0].instances)
    with pytest.raises(RenderError):
        CommandList("missing-target", (command,))
    with pytest.raises(RenderError):
        CommandList("bad-camera", (command,), surface, (1.0,) * 15)

    extracted = RenderExtractor().build_command_list(frame, target=surface, pipeline=pipeline)
    assert extracted.target == surface
    assert extracted.camera_matrix == frame.camera.orthographic_matrix()
    assert extracted.commands == (command,)


def test_unknown_usage_bits_and_non_triangle_sprite_pipeline_are_rejected() -> None:
    with pytest.raises(RenderError):
        BufferDescriptor(4, BufferUsage(128))

    device = NullRenderDevice(scope=SCOPE)
    texture = device.create_texture(_texture_descriptor())
    pipeline = device.create_pipeline(
        PipelineDescriptor(
            TextureFormat.RGBA8_UNORM,
            topology=PrimitiveTopology.LINE_LIST,
        )
    )
    surface = device.create_surface(SurfaceDescriptor(4, 4, TextureFormat.RGBA8_UNORM))
    source = SpriteExtractionSource(texture, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0)
    frame = RenderExtractor().extract_sprites(
        (source,), completed_ticks=1, interpolation_alpha=0.0, camera=Camera2D()
    )
    commands = RenderExtractor().build_command_list(frame, target=surface, pipeline=pipeline)
    with pytest.raises(RenderError) as raised:
        device.submit((commands,))
    assert raised.value.code == "render.invalid_usage"


def test_null_surface_event_drain_is_empty_and_rejects_wrong_handle_kind() -> None:
    device = NullRenderDevice(scope=SCOPE)
    surface = device.create_surface(SurfaceDescriptor(4, 4, TextureFormat.RGBA8_UNORM))
    texture = device.create_texture(_texture_descriptor())

    assert device.drain_surface_events(surface) == ()
    assert device.poll_gamepads() == ()
    with pytest.raises(RenderError) as raised:
        device.drain_surface_events(texture)  # type: ignore[arg-type]
    assert raised.value.code == "render.wrong_handle_kind"
