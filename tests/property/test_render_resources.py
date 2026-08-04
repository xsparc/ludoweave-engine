"""Property checks for M3 render resource identities and extraction ordering."""

from __future__ import annotations

from uuid import UUID

from hypothesis import given
from hypothesis import strategies as st

from ludoweave.render import (
    Camera2D,
    NullRenderDevice,
    RenderExtractor,
    SpriteExtractionSource,
    TextureDescriptor,
    TextureFormat,
    TextureUsage,
)

_SCOPE = UUID("47ddc1bf-22e7-4b26-bad7-51ccfd6f2105")


def _descriptor(size: int) -> TextureDescriptor:
    return TextureDescriptor(
        size,
        size,
        TextureFormat.RGBA8_UNORM,
        TextureUsage.SAMPLED | TextureUsage.COPY_DESTINATION,
    )


@given(st.lists(st.integers(min_value=1, max_value=16), min_size=1, max_size=64))
def test_immediately_retired_slots_reuse_index_and_increment_generation(
    dimensions: list[int],
) -> None:
    device = NullRenderDevice(scope=_SCOPE)
    handle = device.create_texture(_descriptor(dimensions[0]))
    for expected_generation, dimension in enumerate(dimensions[1:], start=1):
        device.destroy(handle)
        handle = device.create_texture(_descriptor(dimension))
        assert handle.index == 0
        assert handle.generation == expected_generation


@given(st.permutations(tuple(range(8))), st.floats(min_value=0.0, max_value=1.0))
def test_extraction_is_permutation_invariant_with_canonical_entity_order(
    order: list[int], alpha: float
) -> None:
    device = NullRenderDevice(scope=_SCOPE)
    texture = device.create_texture(_descriptor(1))
    sources = tuple(
        SpriteExtractionSource(
            texture,
            index,
            0,
            0.0,
            0.0,
            float(index),
            float(index),
            0.0,
            0.0,
            1.0,
            1.0,
        )
        for index in range(8)
    )
    extractor = RenderExtractor()
    frame = extractor.extract_sprites(
        (sources[index] for index in order),
        completed_ticks=1,
        interpolation_alpha=alpha,
        camera=Camera2D(),
    )
    assert tuple(item.entity_index for item in frame.sprite_groups[0].instances) == tuple(range(8))
