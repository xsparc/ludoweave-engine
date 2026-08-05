"""Richer headless 2D presentation module tests."""

from itertools import repeat
from uuid import UUID

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.presentation import (
    BitmapFont,
    BitmapGlyph,
    Particle,
    ParticleEmitter,
    ParticleState,
    PlaybackMode,
    PresentationError,
    SpriteAnimationClip,
    SpriteAnimationFrame,
    TextAlign,
    TextLayout,
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
from ludoweave.render import TextureHandle

_TEXTURE = TextureHandle(UUID("8754815d-6c63-44a2-8889-57b34e937340"), 4, 0)


def _frame(left: float, right: float, duration: int = 1) -> SpriteAnimationFrame:
    return SpriteAnimationFrame(duration, left, 0.0, right, 1.0)


def _font() -> BitmapFont:
    return BitmapFont(
        "fixture.font",
        10,
        (
            BitmapGlyph("?", 5, 4, 8, 0, 1, 0.0, 0.0, 0.25, 0.5),
            BitmapGlyph("A", 6, 5, 8, 0, 1, 0.25, 0.0, 0.5, 0.5),
            BitmapGlyph("B", 6, 5, 8, 0, 1, 0.5, 0.0, 0.75, 0.5),
            BitmapGlyph(" ", 4, 0, 0, 0, 0, 0.75, 0.0, 1.0, 0.5),
        ),
        "?",
    )


def _tilemap() -> TileMap:
    return TileMap(
        "fixture.map",
        16,
        8,
        (
            TileDefinition(1, 0.0, 0.0, 0.5, 1.0),
            TileDefinition(2, 0.5, 0.0, 1.0, 1.0),
        ),
        (TileLayer("ground", 2, (TileChunk(-1, 0, 3, 2, (1, 2, None, None, 2, 1)),)),),
    )


def _emitter(seed: int = 7) -> ParticleEmitter:
    return ParticleEmitter(
        "fixture.emitter",
        seed,
        capacity=5,
        spawn_per_tick=2,
        lifetime_ticks=3,
        velocity_x_min=-16,
        velocity_x_max=16,
        velocity_y_min=8,
        velocity_y_max=24,
        acceleration_y=-2,
    )


def test_animation_modes_use_exact_tick_boundaries() -> None:
    loop = SpriteAnimationClip("walk", (_frame(0.0, 0.5, 2), _frame(0.5, 1.0)), PlaybackMode.LOOP)
    assert [sample_animation(loop, tick).frame_index for tick in range(6)] == [0, 0, 1, 0, 0, 1]
    assert sample_animation(loop, 3).completed_cycles == 1

    once = SpriteAnimationClip("once", loop.frames, PlaybackMode.ONCE)
    final = sample_animation(once, 99)
    assert final.frame_index == 1
    assert final.frame_tick == 0
    assert final.finished is True

    ping_pong = SpriteAnimationClip(
        "ping.pong",
        (_frame(0.0, 0.25), _frame(0.25, 0.5), _frame(0.5, 0.75)),
        PlaybackMode.PING_PONG,
    )
    assert [sample_animation(ping_pong, tick).frame_index for tick in range(8)] == [
        0,
        1,
        2,
        1,
        0,
        1,
        2,
        1,
    ]


def test_animation_extracts_through_existing_sprite_contract() -> None:
    clip = SpriteAnimationClip("idle", (_frame(0.25, 0.5),))
    source = animation_sprite(
        _TEXTURE,
        sample_animation(clip, 0),
        entity_index=9,
        previous_x=1.0,
        previous_y=2.0,
        current_x=3.0,
        current_y=4.0,
        width=8.0,
        height=8.0,
    )
    assert (source.uv_left, source.uv_right) == (0.25, 0.5)
    assert (source.previous_x, source.current_x) == (1.0, 3.0)


def test_animation_rejects_invalid_frames_and_elapsed_ticks() -> None:
    with pytest.raises(PresentationError):
        _frame(0.0, 1.0, 0)
    clip = SpriteAnimationClip("idle", (_frame(0.0, 1.0),))
    with pytest.raises(PresentationError):
        sample_animation(clip, -1)
    with pytest.raises(PresentationError, match="item bound"):
        SpriteAnimationClip("too.long", repeat(_frame(0.0, 1.0)))  # type: ignore[arg-type]


def test_bitmap_text_wrap_alignment_fallback_and_sprite_extraction() -> None:
    font = _font()
    layout = layout_text(font, "ABX", max_width=12, max_lines=2, align=TextAlign.RIGHT)
    assert layout.line_widths == (12, 5)
    assert layout.width == 12
    assert layout.height == 20
    assert [placement.glyph.character for placement in layout.placements] == ["A", "B", "?"]
    assert layout.placements[-1].x == 7

    sources = glyph_sprites(_TEXTURE, layout, base_entity_index=100, origin_x=1.0)
    assert len(sources) == 3
    assert [source.entity_index for source in sources] == [100, 101, 102]
    assert sources[0].width == 5.0


def test_bitmap_text_explicit_lines_tabs_spaces_and_bounds() -> None:
    font = _font()
    layout = layout_text(font, "A\nA B\tA")
    assert layout.line_widths == (6, 38)
    assert len(glyph_sprites(_TEXTURE, layout, base_entity_index=0)) == 4
    with pytest.raises(PresentationError, match="line bound"):
        layout_text(font, "A\nB", max_lines=1)
    with pytest.raises(PresentationError, match="control"):
        layout_text(font, "A\rB")
    tabs = layout_text(font, "\t" * 1_100)
    assert len(tabs.placements) == 4_400
    valid = layout_text(font, "AB")
    with pytest.raises(PresentationError, match="smaller"):
        TextLayout(valid.placements, valid.line_widths, valid.width - 1, valid.height)


def test_tilemap_culls_half_open_region_in_canonical_order() -> None:
    tilemap = _tilemap()
    groups = extract_tile_groups(tilemap, _TEXTURE, min_x=0, min_y=0, max_x=2, max_y=2)
    assert len(groups) == 1
    assert groups[0].layer == 2
    assert [(tile.x, tile.y) for tile in groups[0].tiles] == [(0, 0), (0, 1), (1, 1)]
    assert (groups[0].tile_width, groups[0].tile_height) == (16.0, 8.0)


def test_tilemap_rejects_overlap_unknown_tiles_and_invalid_regions() -> None:
    left = TileChunk(0, 0, 2, 1, (1, 1))
    right = TileChunk(1, 0, 1, 1, (1,))
    with pytest.raises(PresentationError, match="overlap"):
        TileLayer("bad", 0, (left, right))
    with pytest.raises(PresentationError, match="undeclared"):
        TileMap(
            "bad.map",
            1,
            1,
            (TileDefinition(1, 0.0, 0.0, 1.0, 1.0),),
            (TileLayer("bad", 0, (TileChunk(0, 0, 1, 1, (2,)),)),),
        )
    with pytest.raises(PresentationError, match="half-open"):
        extract_tile_groups(_tilemap(), _TEXTURE, min_x=0, min_y=0, max_x=0, max_y=1)
    with pytest.raises(PresentationError, match="item bound"):
        TileLayer("too.many", 0, repeat(TileChunk(0, 0, 1, 1, (1,))))  # type: ignore[arg-type]


def test_tilemap_orders_cells_globally_across_different_chunk_heights() -> None:
    tilemap = TileMap(
        "ordered.map",
        1,
        1,
        (TileDefinition(1, 0.0, 0.0, 1.0, 1.0),),
        (
            TileLayer(
                "ordered",
                0,
                (
                    TileChunk(10, 0, 1, 3, (1, 1, 1)),
                    TileChunk(0, 1, 1, 1, (1,)),
                ),
            ),
        ),
    )
    groups = extract_tile_groups(tilemap, _TEXTURE, min_x=0, min_y=0, max_x=11, max_y=3)
    assert [(tile.x, tile.y) for tile in groups[0].tiles] == [
        (10, 0),
        (0, 1),
        (10, 1),
        (10, 2),
    ]


def test_tilemap_can_extract_the_maximum_signed_32_bit_cell() -> None:
    tilemap = TileMap(
        "edge.map",
        1,
        1,
        (TileDefinition(1, 0.0, 0.0, 1.0, 1.0),),
        (
            TileLayer(
                "edge",
                0,
                (TileChunk(2**31 - 1, 2**31 - 1, 1, 1, (1,)),),
            ),
        ),
    )
    groups = extract_tile_groups(
        tilemap,
        _TEXTURE,
        min_x=2**31 - 1,
        min_y=2**31 - 1,
        max_x=2**31,
        max_y=2**31,
    )
    assert [(tile.x, tile.y) for tile in groups[0].tiles] == [(2**31 - 1, 2**31 - 1)]


def test_particles_are_bounded_repeatable_and_extractable() -> None:
    emitter = _emitter()
    first = step_particles(emitter, ParticleState(), ticks=4)
    second = step_particles(emitter, ParticleState(), ticks=4)
    assert first == second
    assert len(first.particles) <= emitter.capacity
    assert first.completed_ticks == 4
    assert particle_state_digest(first) == particle_state_digest(second)
    assert (
        particle_state_digest(first)
        == "5d01c1805a7b85ab6ab30b1afaeaf0e1b9283b6982c6e05ebff99ba2798cd138"
    )

    sources = particle_sprites(
        _TEXTURE,
        first,
        base_entity_index=200,
        width=2.0,
        height=3.0,
    )
    assert len(sources) == len(first.particles)
    assert all(source.width == 2.0 for source in sources)


@given(seed=st.integers(min_value=0, max_value=2**64 - 1), ticks=st.integers(0, 12))
def test_particle_repeatability_property(seed: int, ticks: int) -> None:
    emitter = _emitter(seed)
    first = step_particles(emitter, ParticleState(), ticks=ticks)
    second = step_particles(emitter, ParticleState(), ticks=ticks)
    assert first == second
    assert len(first.particles) <= emitter.capacity
    assert all(particle.age_ticks < particle.lifetime_ticks for particle in first.particles)


def test_particles_reject_invalid_state_and_tick_bounds() -> None:
    with pytest.raises(PresentationError):
        ParticleEmitter("bad", 0, 1, 2, 1)
    with pytest.raises(PresentationError):
        step_particles(_emitter(), ParticleState(), ticks=-1)
    mismatched = ParticleState(
        0,
        1,
        (Particle(0, 0, 2, 0, 0, 0, 0, 0, 0),),
    )
    with pytest.raises(PresentationError, match="lifetime"):
        step_particles(_emitter(), mismatched)
    expensive = ParticleEmitter("expensive", 0, 100_000, 0, 3)
    with pytest.raises(PresentationError, match="work budget"):
        step_particles(expensive, ParticleState(), ticks=101)
