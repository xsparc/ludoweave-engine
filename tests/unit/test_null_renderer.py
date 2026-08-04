"""Null-render descriptor and lifecycle validation tests."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.core.errors import RenderError
from ludoweave.render import NullRenderBackend, RenderDescriptor


def test_null_renderer_valid_lifecycle() -> None:
    backend = NullRenderBackend()
    descriptor = RenderDescriptor(width=320, height=180, label="test")
    backend.initialize(descriptor)
    backend.render(tick=0)
    backend.render(tick=1)
    backend.close()
    backend.close()

    assert backend.descriptor == descriptor
    assert backend.frame_count == 2
    assert backend.is_closed


@given(st.integers(max_value=0))
def test_descriptor_rejects_non_positive_width(width: int) -> None:
    with pytest.raises(RenderError, match="positive integer"):
        RenderDescriptor(width=width)


@given(st.integers(max_value=0))
def test_descriptor_rejects_non_positive_height(height: int) -> None:
    with pytest.raises(RenderError, match="positive integer"):
        RenderDescriptor(height=height)


@pytest.mark.parametrize("label", ["", " ", "\t"])
def test_descriptor_rejects_blank_label(label: str) -> None:
    with pytest.raises(RenderError, match="non-whitespace"):
        RenderDescriptor(label=label)


def test_null_renderer_rejects_render_before_initialize() -> None:
    backend = NullRenderBackend()
    with pytest.raises(RenderError, match="created state"):
        backend.render(tick=0)


def test_null_renderer_rejects_double_initialize() -> None:
    backend = NullRenderBackend()
    backend.initialize(RenderDescriptor())
    with pytest.raises(RenderError, match="ready state"):
        backend.initialize(RenderDescriptor())


def test_null_renderer_rejects_render_after_close() -> None:
    backend = NullRenderBackend()
    backend.initialize(RenderDescriptor())
    backend.close()
    with pytest.raises(RenderError, match="closed state"):
        backend.render(tick=0)
