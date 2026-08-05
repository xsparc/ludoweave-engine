"""Pure-Python sprite packing reference and failure tests."""

from struct import pack

import pytest

from ludoweave.core.errors import RenderError
from ludoweave.render import Color, SpriteInstance
from ludoweave.render._sprite import SPRITE_INSTANCE_STRIDE, pack_sprite_instances


def test_sprite_packing_matches_the_provider_neutral_float32_layout() -> None:
    first = SpriteInstance(
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        0.1,
        0.2,
        0.8,
        0.9,
        tint=Color(0.3, 0.4, 0.5, 0.6),
        z=7.0,
    )
    second = SpriteInstance(8.0, 9.0, 10.0, 11.0, 12.0, 0.0, 0.0, 1.0, 1.0)

    packed = pack_sprite_instances((first, second))

    expected = pack(
        "<32f",
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        0.1,
        0.2,
        0.0,
        0.8,
        0.9,
        0.3,
        0.4,
        0.5,
        0.6,
        7.0,
        0.0,
        8.0,
        9.0,
        10.0,
        11.0,
        12.0,
        0.0,
        0.0,
        0.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        0.0,
        0.0,
    )
    assert packed == expected
    assert len(packed) == 2 * SPRITE_INSTANCE_STRIDE
    assert pack_sprite_instances(()) == b""


def test_sprite_packing_wraps_float32_overflow_with_context() -> None:
    instance = SpriteInstance(1e100, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0)

    with pytest.raises(RenderError) as raised:
        pack_sprite_instances((instance,))

    assert raised.value.code == "render.instance_pack_failed"
    assert dict(raised.value.details) == {"instances": 1}
    assert isinstance(raised.value.__cause__, OverflowError)
