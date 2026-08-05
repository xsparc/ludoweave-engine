"""Strict expected document for M14 installed-surface artifact smoke."""

from typing import cast

_RENDER_EXPORTS = [
    "RENDER_DEVICE_CONFORMANCE_PROFILE",
    "RENDER_DEVICE_CONFORMANCE_PROTOCOL",
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
    "ConformanceStatus",
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
    "RenderDeviceConformanceCheck",
    "RenderDeviceConformanceReport",
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
    "run_render_device_conformance",
]
_FACTS: dict[str, object] = {
    "builtin_operations": [
        "component.add",
        "component.patch",
        "component.remove",
        "entity.destroy",
        "entity.spawn",
        "resource.patch",
        "world.tick",
    ],
    "pipeline_fields": ["color_format", "topology", "blend", "label"],
    "render_capability_fields": [
        "backend",
        "max_texture_dimension_2d",
        "offscreen_capture",
        "timestamp_queries",
        "surface_formats",
    ],
    "render_export_count": 53,
    "render_exports": _RENDER_EXPORTS,
    "texture_descriptor_fields": [
        "width",
        "height",
        "format",
        "usage",
        "layers",
        "label",
    ],
    "texture_formats": [
        "rgba8_unorm",
        "rgba8_unorm_srgb",
        "bgra8_unorm",
        "bgra8_unorm_srgb",
    ],
}
_GATES: dict[str, object] = {
    "agent_semantic_contract": False,
    "cross_platform_budget": False,
    "depth_stencil_contract": False,
    "headless_null_conformance": False,
    "material_lighting_contract": False,
    "mesh_geometry_contract": False,
    "perspective_camera_contract": False,
    "product_vertical_slice": False,
    "three_dimensional_texture_contract": False,
}
_LAYERED_2D: dict[str, object] = {
    "camera_exported": True,
    "camera_fields": [
        "x",
        "y",
        "viewport_width",
        "viewport_height",
        "rotation_radians",
        "zoom",
    ],
    "camera_projection": "orthographic",
    "default_camera_matrix": [
        2.0,
        0.0,
        0.0,
        0.0,
        0.0,
        2.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
    ],
    "sprite_sort_fields": ["layer", "z", "entity_index", "entity_generation"],
    "sprite_sort_keys": [[0, -1.0, 9, 0], [0, 2.0, 5, 2], [1, -10.0, 1, 0]],
    "tile_layer_field": True,
}


def validate_constrained_3d_evidence(document: dict[str, object], *, version: str) -> None:
    """Reject any installed-surface evidence drift with exact JSON types."""

    expected: dict[str, object] = {
        "admission_ready": False,
        "decision": "retain-layered-2d",
        "facts": _FACTS,
        "gates": _GATES,
        "layered_2d": _LAYERED_2D,
        "layered_2d_confirmed": True,
        "ludoweave_version": version,
        "schema": "ludoweave.evaluation.constrained-3d/1",
        "status": "deferred",
    }
    if not _exact_json(document, expected):
        raise RuntimeError("constrained 3D installed-surface evidence drifted")


def _exact_json(actual: object, expected: object) -> bool:
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        actual_mapping = cast(dict[object, object], actual)
        expected_mapping = cast(dict[object, object], expected)
        return actual_mapping.keys() == expected_mapping.keys() and all(
            _exact_json(actual_mapping[key], value) for key, value in expected_mapping.items()
        )
    if isinstance(expected, list):
        actual_items = cast(list[object], actual)
        expected_items = cast(list[object], expected)
        return len(actual_items) == len(expected_items) and all(
            _exact_json(actual_item, expected_item)
            for actual_item, expected_item in zip(actual_items, expected_items, strict=True)
        )
    return actual == expected
