"""Retain the accepted layered-2D public and provider boundary."""

from dataclasses import fields
from pathlib import Path

import ludoweave.render as render
from ludoweave.render import (
    Camera2D,
    PipelineDescriptor,
    RenderCapabilities,
    SpriteInstance,
    TextureDescriptor,
    TileBatchCommand,
)

_ROOT = Path(__file__).parents[2]
_EXPECTED_RENDER_EXPORTS = (
    "BlendMode",
    "BufferData",
    "BufferDescriptor",
    "BufferHandle",
    "BufferUsage",
    "Camera2D",
    "CaptureImage",
    "ClearCommand",
    "Color",
    "CommandList",
    "CompiledRenderGraph",
    "DebugLineCommand",
    "DiagnosticTextCommand",
    "FenceHandle",
    "GraphResource",
    "GraphResourceKind",
    "GraphResourceLifetime",
    "NullRenderBackend",
    "NullRenderDevice",
    "PipelineDescriptor",
    "PipelineHandle",
    "PresentationFrame",
    "PrimitiveTopology",
    "RenderBackend",
    "RenderCapabilities",
    "RenderDescriptor",
    "RenderDevice",
    "RenderExtractor",
    "RenderGraph",
    "RenderPass",
    "RenderResourceHandle",
    "SpriteBatchCommand",
    "SpriteDrawGroup",
    "SpriteExtractionSource",
    "SpriteInstance",
    "Submission",
    "SurfaceDescriptor",
    "SurfaceHandle",
    "SurfaceKind",
    "TextureData",
    "TextureDescriptor",
    "TextureFormat",
    "TextureHandle",
    "TextureUsage",
    "TileBatchCommand",
    "TileDrawGroup",
    "TileInstance",
)
_FORBIDDEN_EXPORT_TOKENS = (
    "3d",
    "geometry",
    "light",
    "material",
    "mesh",
    "model",
    "perspective",
    "projection",
    "quaternion",
    "vertex",
)


def test_public_render_surface_remains_layered_2d_only() -> None:
    assert tuple(render.__all__) == _EXPECTED_RENDER_EXPORTS
    assert [
        name
        for name in render.__all__
        if any(token in name.casefold() for token in _FORBIDDEN_EXPORT_TOKENS)
    ] == []
    assert tuple(field.name for field in fields(Camera2D)) == (
        "x",
        "y",
        "viewport_width",
        "viewport_height",
        "rotation_radians",
        "zoom",
    )
    assert tuple(field.name for field in fields(SpriteInstance))[-4:] == (
        "layer",
        "z",
        "entity_index",
        "entity_generation",
    )
    assert tuple(field.name for field in fields(TileBatchCommand))[-1] == "layer"
    assert tuple(field.name for field in fields(PipelineDescriptor)) == (
        "color_format",
        "topology",
        "blend",
        "label",
    )
    assert tuple(field.name for field in fields(TextureDescriptor)) == (
        "width",
        "height",
        "format",
        "usage",
        "layers",
        "label",
    )
    assert tuple(field.name for field in fields(RenderCapabilities)) == (
        "backend",
        "max_texture_dimension_2d",
        "offscreen_capture",
        "timestamp_queries",
        "surface_formats",
    )


def test_sprite_shader_uses_fixed_presentation_depth_without_depth_state() -> None:
    shader = (_ROOT / "src" / "ludoweave" / "render" / "_sprite.py").read_text(encoding="utf-8")

    assert "vec4<f32>(world, 0.0, 1.0)" in shader
    assert "depth_stencil" not in shader.casefold()
    assert "texture_depth" not in shader.casefold()


def test_engine_source_contains_no_3d_named_runtime_module() -> None:
    source = _ROOT / "src" / "ludoweave"
    modules = [path.relative_to(source).as_posix() for path in source.rglob("*.py")]

    assert [
        name for name in modules if any("3d" in part.casefold() for part in Path(name).parts)
    ] == []
