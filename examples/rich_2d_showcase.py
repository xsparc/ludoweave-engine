"""Exercise M11 audio, text, animation, tilemap, and particles headlessly."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from uuid import UUID

from ludoweave import __version__
from ludoweave.audio import (
    AudioBusDescriptor,
    AudioClipDescriptor,
    AudioMixGraph,
    NullAudioBackend,
)
from ludoweave.presentation import (
    BitmapFont,
    BitmapGlyph,
    ParticleEmitter,
    ParticleState,
    PlaybackMode,
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
    particle_state_digest,
    sample_animation,
    step_particles,
)
from ludoweave.render import (
    Camera2D,
    PipelineDescriptor,
    PresentationFrame,
    RenderExtractor,
    SurfaceDescriptor,
    SurfaceKind,
    TextureData,
    TextureDescriptor,
    TextureFormat,
    TextureUsage,
)
from ludoweave.render.backends import NullRenderDevice

_SCOPE = UUID("a80b87c8-aee5-4be3-9caf-df42159c1a71")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticks", type=int, default=6)
    return parser


def _font() -> BitmapFont:
    characters = "? ADELOWUV"
    glyphs = tuple(
        BitmapGlyph(
            character,
            6 if character != " " else 4,
            5 if character != " " else 0,
            8 if character != " " else 0,
            0,
            0,
            float(index) / float(len(characters)),
            0.0,
            float(index + 1) / float(len(characters)),
            1.0,
        )
        for index, character in enumerate(characters)
    )
    return BitmapFont("showcase.font", 10, glyphs, "?")


def _tilemap() -> TileMap:
    return TileMap(
        "showcase.map",
        8,
        8,
        (
            TileDefinition(1, 0.0, 0.0, 0.5, 1.0),
            TileDefinition(2, 0.5, 0.0, 1.0, 1.0),
        ),
        (
            TileLayer(
                "ground",
                0,
                (TileChunk(-2, -1, 4, 2, (1, 2, 1, 2, 2, 1, 2, 1)),),
            ),
        ),
    )


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    if not 0 <= arguments.ticks <= 10_000:
        _parser().error("--ticks must be between zero and 10000")

    audio = NullAudioBackend(scope=_SCOPE)
    device = NullRenderDevice(scope=_SCOPE)
    try:
        audio.initialize()
        audio.configure_mix(
            AudioMixGraph(
                (
                    AudioBusDescriptor("master", None, 0.8),
                    AudioBusDescriptor("effects", "master", 0.5),
                )
            )
        )
        clip = audio.load_clip(AudioClipDescriptor("showcase.tick", 0.1), b"pcm-fixture")
        playback = audio.play(clip, volume=0.5)

        surface = device.create_surface(
            SurfaceDescriptor(128, 72, TextureFormat.RGBA8_UNORM, SurfaceKind.OFFSCREEN)
        )
        texture = device.create_texture(
            TextureDescriptor(
                4,
                1,
                TextureFormat.RGBA8_UNORM,
                TextureUsage.SAMPLED | TextureUsage.COPY_DESTINATION,
                label="showcase-atlas",
            ),
            TextureData(b"\xff\xff\xff\xff" * 4, 16),
        )
        pipeline = device.create_pipeline(PipelineDescriptor(TextureFormat.RGBA8_UNORM))

        animation = SpriteAnimationClip(
            "showcase.pulse",
            (
                SpriteAnimationFrame(2, 0.0, 0.0, 0.5, 1.0),
                SpriteAnimationFrame(1, 0.5, 0.0, 1.0, 1.0),
            ),
            PlaybackMode.PING_PONG,
        )
        animation_sample = sample_animation(animation, arguments.ticks)
        text_layout = layout_text(_font(), "LUDOWEAVE", max_width=64)
        particle_state = step_particles(
            ParticleEmitter(
                "showcase.spark",
                seed=11,
                capacity=16,
                spawn_per_tick=2,
                lifetime_ticks=5,
                velocity_x_min=-24,
                velocity_x_max=24,
                velocity_y_min=16,
                velocity_y_max=32,
                acceleration_y=-4,
            ),
            ParticleState(),
            ticks=arguments.ticks,
        )
        sprites = (
            animation_sprite(
                texture,
                animation_sample,
                entity_index=0,
                previous_x=0.0,
                previous_y=0.0,
                current_x=1.0,
                current_y=0.0,
                width=12.0,
                height=12.0,
                layer=1,
            ),
            *glyph_sprites(
                texture,
                text_layout,
                base_entity_index=100,
                origin_x=-30.0,
                origin_y=-24.0,
                layer=2,
            ),
            *particle_sprites(
                texture,
                particle_state,
                base_entity_index=1_000,
                width=2.0,
                height=2.0,
                layer=3,
            ),
        )
        extractor = RenderExtractor()
        sprite_frame = extractor.extract_sprites(
            sprites,
            completed_ticks=arguments.ticks,
            interpolation_alpha=0.5,
            camera=Camera2D(viewport_width=128.0, viewport_height=72.0),
        )
        frame = PresentationFrame(
            sprite_frame.completed_ticks,
            sprite_frame.source_tick,
            sprite_frame.interpolation_alpha,
            sprite_frame.camera,
            sprite_groups=sprite_frame.sprite_groups,
            tile_groups=extract_tile_groups(
                _tilemap(), texture, min_x=-2, min_y=-1, max_x=2, max_y=1
            ),
        )
        submission = device.submit(
            (extractor.build_command_list(frame, target=surface, pipeline=pipeline),)
        )
        device.poll()
        summary = {
            "schema": "ludoweave.example.rich_2d/1",
            "version": __version__,
            "ticks": arguments.ticks,
            "animation_frame": animation_sample.frame_index,
            "audio_gain": audio.playback_gain(playback),
            "glyphs": len(text_layout.placements),
            "particles": len(particle_state.particles),
            "particle_sha256": particle_state_digest(particle_state),
            "tile_instances": submission.tile_instances,
            "sprite_instances": submission.sprite_instances,
            "draw_calls": submission.draw_calls,
            "renderer": device.name,
        }
        print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
    finally:
        audio.close()
        device.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
