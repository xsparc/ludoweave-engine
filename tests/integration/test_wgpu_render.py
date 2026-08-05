"""GPU-backed M3 acceptance tests, skipped when the graphics extra is absent."""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from collections.abc import Iterator
from pathlib import Path

import pytest

pytest.importorskip("wgpu")
pytest.importorskip("rendercanvas")

from ludoweave.core.errors import RenderError
from ludoweave.presentation import (
    BitmapFont,
    BitmapGlyph,
    ParticleEmitter,
    ParticleState,
    SpriteAnimationClip,
    SpriteAnimationFrame,
    TileChunk,
    TileDefinition,
    TileLayer,
    TileMap,
    animation_sprite,
    extract_tile_groups,
    glyph_sprites,
    layout_text,
    particle_sprites,
    sample_animation,
    step_particles,
)
from ludoweave.render import (
    Camera2D,
    ClearCommand,
    Color,
    CommandList,
    DebugLineCommand,
    PipelineDescriptor,
    PresentationFrame,
    RenderExtractor,
    SpriteBatchCommand,
    SpriteInstance,
    SurfaceDescriptor,
    SurfaceKind,
    TextureData,
    TextureDescriptor,
    TextureFormat,
    TextureUsage,
    TileBatchCommand,
    TileInstance,
    run_render_device_conformance,
)
from ludoweave.render.backends.wgpu import WgpuRenderDevice


@pytest.fixture
def device() -> Iterator[WgpuRenderDevice]:
    selected = WgpuRenderDevice()
    try:
        yield selected
    finally:
        selected.close()


def _pixel(pixels: bytes, width: int, x: int, y: int) -> tuple[int, int, int, int]:
    offset = (y * width + x) * 4
    return tuple(pixels[offset : offset + 4])  # type: ignore[return-value]


def _camera(width: int, height: int) -> tuple[float, ...]:
    return Camera2D(
        viewport_width=float(width), viewport_height=float(height)
    ).orthographic_matrix()


def test_gamepad_poll_without_window_is_empty(device: WgpuRenderDevice) -> None:
    assert device.poll_gamepads() == ()


def test_real_wgpu_adapter_passes_installed_baseline_conformance() -> None:
    report = run_render_device_conformance(
        "org.ludoweave.wgpu",
        WgpuRenderDevice,
    )

    assert report.passed
    assert report.adapter_name == "wgpu"


def test_real_glfw_null_platform_gamepad_poll_is_bounded() -> None:
    script = textwrap.dedent(
        """
        import json
        import glfw

        from ludoweave.render.backends.wgpu import _GlfwGamepadPoller

        glfw.init_hint(glfw.PLATFORM, glfw.PLATFORM_NULL)
        assert glfw.init()
        try:
            events = _GlfwGamepadPoller(glfw).poll()
            assert len(events) <= 16 * 20
            print(json.dumps({"events": len(events), "status": "ok"}, sort_keys=True))
        finally:
            glfw.terminate()
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["status"] == "ok"


def test_clear_and_two_region_texture_atlas_use_one_instanced_draw(
    device: WgpuRenderDevice,
) -> None:
    surface = device.create_surface(
        SurfaceDescriptor(
            16,
            8,
            TextureFormat.RGBA8_UNORM,
            SurfaceKind.OFFSCREEN,
            "atlas-fixture",
        )
    )
    texture = device.create_texture(
        TextureDescriptor(
            2,
            1,
            TextureFormat.RGBA8_UNORM,
            TextureUsage.SAMPLED | TextureUsage.COPY_DESTINATION,
            label="red-green-atlas",
        ),
        TextureData(b"\xff\x00\x00\xff\x00\xff\x00\xff", 8),
    )
    pipeline = device.create_pipeline(PipelineDescriptor(TextureFormat.RGBA8_UNORM))
    instances = (
        SpriteInstance(-4.0, 0.0, 8.0, 8.0, 0.0, 0.0, 0.0, 0.5, 1.0),
        SpriteInstance(4.0, 0.0, 8.0, 8.0, 0.0, 0.5, 0.0, 1.0, 1.0, entity_index=1),
    )
    submission = device.submit(
        (
            CommandList(
                "atlas-frame",
                (
                    ClearCommand(surface, Color()),
                    SpriteBatchCommand(pipeline, texture, instances),
                ),
                surface,
                _camera(16, 8),
            ),
        )
    )
    device.poll()
    capture = device.capture_surface(surface)

    assert submission.draw_calls == 1
    assert submission.sprite_instances == 2
    assert device.is_fence_complete(submission.fence)
    assert _pixel(capture.pixels, 16, 3, 4) == (255, 0, 0, 255)
    assert _pixel(capture.pixels, 16, 12, 4) == (0, 255, 0, 255)


def test_tile_batch_and_debug_primitives_are_batched_semantically(
    device: WgpuRenderDevice,
) -> None:
    surface = device.create_surface(
        SurfaceDescriptor(
            8,
            8,
            TextureFormat.RGBA8_UNORM,
            SurfaceKind.OFFSCREEN,
            "tile-debug-fixture",
        )
    )
    texture = device.create_texture(
        TextureDescriptor(
            1,
            1,
            TextureFormat.RGBA8_UNORM,
            TextureUsage.SAMPLED | TextureUsage.COPY_DESTINATION,
            label="blue-tile",
        ),
        TextureData(b"\x00\x00\xff\xff", 4),
    )
    pipeline = device.create_pipeline(PipelineDescriptor(TextureFormat.RGBA8_UNORM))
    commands = CommandList(
        "tile-debug-frame",
        (
            ClearCommand(surface, Color()),
            TileBatchCommand(
                pipeline,
                texture,
                (TileInstance(0, 0, 0.0, 0.0, 1.0, 1.0),),
                4.0,
                4.0,
            ),
            DebugLineCommand(-4.0, 0.0, 4.0, 0.0, Color(1.0, 1.0, 1.0, 1.0)),
        ),
        surface,
        _camera(8, 8),
    )
    submission = device.submit((commands,))
    device.poll()
    capture = device.capture_surface(surface)

    assert submission.draw_calls == 2
    assert submission.tile_instances == 1
    assert submission.debug_primitives == 1
    pixels = tuple(_pixel(capture.pixels, 8, x, y) for y in range(8) for x in range(8))
    assert (255, 255, 255, 255) in pixels
    assert (0, 0, 255, 255) in pixels


def test_rich_2d_authoring_records_render_through_real_backend(
    device: WgpuRenderDevice,
) -> None:
    surface = device.create_surface(
        SurfaceDescriptor(16, 8, TextureFormat.RGBA8_UNORM, SurfaceKind.OFFSCREEN, "rich-2d")
    )
    texture = device.create_texture(
        TextureDescriptor(
            2,
            1,
            TextureFormat.RGBA8_UNORM,
            TextureUsage.SAMPLED | TextureUsage.COPY_DESTINATION,
            label="rich-2d-atlas",
        ),
        TextureData(b"\xff\x00\x00\xff\x00\xff\x00\xff", 8),
    )
    pipeline = device.create_pipeline(PipelineDescriptor(TextureFormat.RGBA8_UNORM))
    animation = SpriteAnimationClip("gpu.animation", (SpriteAnimationFrame(1, 0.0, 0.0, 0.5, 1.0),))
    font = BitmapFont(
        "gpu.font",
        4,
        (BitmapGlyph("A", 4, 4, 4, 0, 0, 0.5, 0.0, 1.0, 1.0),),
        "A",
    )
    particles = step_particles(ParticleEmitter("gpu.particles", 1, 1, 1, 2), ParticleState())
    sources = (
        animation_sprite(
            texture,
            sample_animation(animation, 0),
            entity_index=0,
            previous_x=-4.0,
            previous_y=0.0,
            current_x=-4.0,
            current_y=0.0,
            width=4.0,
            height=4.0,
        ),
        *glyph_sprites(texture, layout_text(font, "A"), base_entity_index=10),
        *particle_sprites(texture, particles, base_entity_index=20, width=2.0, height=2.0),
    )
    tilemap = TileMap(
        "gpu.map",
        4,
        4,
        (TileDefinition(1, 0.5, 0.0, 1.0, 1.0),),
        (TileLayer("ground", 0, (TileChunk(1, 0, 1, 1, (1,)),)),),
    )
    extractor = RenderExtractor()
    sprites = extractor.extract_sprites(
        sources,
        completed_ticks=1,
        interpolation_alpha=0.0,
        camera=Camera2D(viewport_width=16.0, viewport_height=8.0),
    )
    frame = PresentationFrame(
        sprites.completed_ticks,
        sprites.source_tick,
        sprites.interpolation_alpha,
        sprites.camera,
        sprite_groups=sprites.sprite_groups,
        tile_groups=extract_tile_groups(tilemap, texture, min_x=0, min_y=0, max_x=2, max_y=1),
    )

    submission = device.submit(
        (extractor.build_command_list(frame, target=surface, pipeline=pipeline),)
    )
    device.poll()
    capture = device.capture_surface(surface)

    assert submission.draw_calls == 2
    assert submission.sprite_instances == 3
    assert submission.tile_instances == 1
    assert len(capture.pixels) == 16 * 8 * 4


def test_surface_resize_minimize_restore_destroy_and_capture_lifecycle(
    device: WgpuRenderDevice,
) -> None:
    surface = device.create_surface(
        SurfaceDescriptor(
            4,
            4,
            TextureFormat.RGBA8_UNORM,
            SurfaceKind.OFFSCREEN,
            "resize-fixture",
        )
    )
    device.resize_surface(surface, 8, 2)
    device.submit(
        (
            CommandList(
                "resized",
                (ClearCommand(surface, Color(0.25, 0.5, 0.75, 1.0)),),
                surface,
            ),
        )
    )
    device.poll()
    capture = device.capture_surface(surface)
    assert (capture.width, capture.height, len(capture.pixels)) == (8, 2, 64)

    device.resize_surface(surface, 0, 0)
    with pytest.raises(RenderError) as minimized:
        device.capture_surface(surface)
    assert minimized.value.code == "render.capture_unavailable"
    with pytest.raises(RenderError):
        device.resize_surface(surface, 1, 0)

    device.resize_surface(surface, 2, 2)
    device.destroy(surface)
    with pytest.raises(RenderError) as stale:
        device.capture_surface(surface)
    assert stale.value.code == "render.stale_handle"


def test_simulated_device_loss_has_typed_non_secret_diagnostics(
    device: WgpuRenderDevice,
) -> None:
    device.simulate_device_loss()
    with pytest.raises(RenderError) as lost:
        _ = device.capabilities
    assert lost.value.code == "render.device_lost"
    assert dict(lost.value.details) == {
        "backend": "wgpu",
        "reason": "simulated",
        "recoverable": False,
    }


def test_hello_sprite_example_emits_versioned_capture_summary() -> None:
    example = Path(__file__).parents[2] / "examples" / "hello_sprite.py"
    result = subprocess.run(
        (sys.executable, str(example), "--width", "16", "--height", "8"),
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    document = json.loads(result.stdout)
    assert document["schema"] == "ludoweave.example.hello_sprite/1"
    assert document["backend"] == "wgpu"
    assert document["capture_bytes"] == 512
    assert len(document["capture_sha256"]) == 64
    assert document["draw_calls"] == 1
    assert document["sprite_instances"] == 2
    assert document["fence_complete"] is True


def test_agent_world_builder_example_completes_real_capture_and_typed_loop() -> None:
    example = Path(__file__).parents[2] / "examples" / "agent_world_builder.py"
    result = subprocess.run(
        (sys.executable, str(example)),
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    document = json.loads(result.stdout)
    assert document["protocol"] == "ludoweave.sample.agent_world_builder/1"
    assert document["validation_status"] == "dry_run"
    assert document["apply_status"] == document["adjust_status"] == "committed"
    assert document["ticks"] == 3
    assert document["query_matches"] == 6
    assert document["capture_width"] == 320
    assert document["capture_height"] == 180
    assert document["capture_sha256"].startswith("sha256:")
    assert document["tests_passed"] is True
    assert document["replay_batches"] == 5
