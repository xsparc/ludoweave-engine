"""Deterministic headless-first authoring for richer 2D presentation."""

from ludoweave.presentation.animation import (
    AnimationSample,
    PlaybackMode,
    SpriteAnimationClip,
    SpriteAnimationFrame,
    animation_sprite,
    sample_animation,
)
from ludoweave.presentation.errors import PresentationError
from ludoweave.presentation.particles import (
    SUBPIXELS_PER_UNIT,
    Particle,
    ParticleEmitter,
    ParticleState,
    particle_sprites,
    particle_state_digest,
    step_particles,
)
from ludoweave.presentation.text import (
    BitmapFont,
    BitmapGlyph,
    GlyphPlacement,
    TextAlign,
    TextLayout,
    glyph_sprites,
    layout_text,
)
from ludoweave.presentation.tilemap import (
    TileChunk,
    TileDefinition,
    TileLayer,
    TileMap,
    extract_tile_groups,
)

__all__ = [
    "SUBPIXELS_PER_UNIT",
    "AnimationSample",
    "BitmapFont",
    "BitmapGlyph",
    "GlyphPlacement",
    "Particle",
    "ParticleEmitter",
    "ParticleState",
    "PlaybackMode",
    "PresentationError",
    "SpriteAnimationClip",
    "SpriteAnimationFrame",
    "TextAlign",
    "TextLayout",
    "TileChunk",
    "TileDefinition",
    "TileLayer",
    "TileMap",
    "animation_sprite",
    "extract_tile_groups",
    "glyph_sprites",
    "layout_text",
    "particle_sprites",
    "particle_state_digest",
    "sample_animation",
    "step_particles",
]
__stability__ = {name: "experimental" for name in __all__}
