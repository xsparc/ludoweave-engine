"""Report the installed engine surface behind the constrained-3D decision."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from dataclasses import fields

from ludoweave import __version__
from ludoweave.render import (
    Camera2D,
    PipelineDescriptor,
    RenderCapabilities,
    SpriteInstance,
    TextureDescriptor,
    TextureFormat,
    TileBatchCommand,
)
from ludoweave.render import (
    __all__ as render_exports,
)
from ludoweave.world import BUILTIN_OPERATION_SPECS

_SCHEMA = "ludoweave.evaluation.constrained-3d/1"
_CAMERA_EXPORTS = frozenset({"Camera3D", "PerspectiveCamera"})
_MESH_EXPORTS = frozenset({"IndexBuffer", "Mesh", "MeshDescriptor", "MeshInstance", "VertexBuffer"})
_MATERIAL_EXPORTS = frozenset(
    {"DirectionalLight", "Light", "Material", "MaterialDescriptor", "PointLight"}
)
_THREE_D_TOKENS = ("3d", "mesh", "model", "perspective")
_CAMERA_FIELDS = (
    "x",
    "y",
    "viewport_width",
    "viewport_height",
    "rotation_radians",
    "zoom",
)
_SPRITE_SORT_FIELDS = ("layer", "z", "entity_index", "entity_generation")


def main(argv: Sequence[str] | None = None) -> int:
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    if arguments:
        raise SystemExit("constrained_3d_decision accepts no arguments")
    print(json.dumps(evaluate(), ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0


def evaluate() -> dict[str, object]:
    """Return exact installed facts and the resulting admission decision."""

    exports = frozenset(render_exports)
    pipeline_fields = tuple(field.name for field in fields(PipelineDescriptor))
    capability_fields = tuple(field.name for field in fields(RenderCapabilities))
    texture_fields = tuple(field.name for field in fields(TextureDescriptor))
    texture_formats = tuple(item.value for item in TextureFormat)
    operations = tuple(spec.operation for spec in BUILTIN_OPERATION_SPECS)
    camera_fields = tuple(field.name for field in fields(Camera2D))
    camera_matrix = tuple(
        0.0 if value == 0.0 else value for value in Camera2D().orthographic_matrix()
    )
    sprite_sort_fields = tuple(field.name for field in fields(SpriteInstance))[-4:]
    sprite_sort_keys = tuple(
        item.sort_key
        for item in sorted(
            (
                _sprite(layer=1, z=-10.0, entity_index=1, entity_generation=0),
                _sprite(layer=0, z=2.0, entity_index=5, entity_generation=2),
                _sprite(layer=0, z=-1.0, entity_index=9, entity_generation=0),
            ),
            key=lambda item: item.sort_key,
        )
    )
    tile_fields = tuple(field.name for field in fields(TileBatchCommand))
    layered_2d = {
        "camera_exported": "Camera2D" in exports,
        "camera_fields": camera_fields,
        "camera_projection": Camera2D.orthographic_matrix.__name__.removesuffix("_matrix"),
        "default_camera_matrix": camera_matrix,
        "sprite_sort_fields": sprite_sort_fields,
        "sprite_sort_keys": sprite_sort_keys,
        "tile_layer_field": "layer" in tile_fields,
    }
    layered_2d_confirmed = layered_2d == {
        "camera_exported": True,
        "camera_fields": _CAMERA_FIELDS,
        "camera_projection": "orthographic",
        "default_camera_matrix": (
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
        ),
        "sprite_sort_fields": _SPRITE_SORT_FIELDS,
        "sprite_sort_keys": ((0, -1.0, 9, 0), (0, 2.0, 5, 2), (1, -10.0, 1, 0)),
        "tile_layer_field": True,
    }

    perspective_camera = not exports.isdisjoint(_CAMERA_EXPORTS)
    mesh_geometry = not exports.isdisjoint(_MESH_EXPORTS)
    depth_stencil = any(
        token in value.casefold()
        for value in (*pipeline_fields, *texture_fields, *texture_formats)
        for token in ("depth", "stencil")
    )
    texture_3d = "max_texture_dimension_3d" in capability_fields or "depth" in texture_fields
    material_lighting = not exports.isdisjoint(_MATERIAL_EXPORTS)
    agent_semantics = any(
        token in operation.casefold() for operation in operations for token in _THREE_D_TOKENS
    )
    gates = {
        "agent_semantic_contract": agent_semantics,
        "cross_platform_budget": False,
        "depth_stencil_contract": depth_stencil,
        "headless_null_conformance": False,
        "material_lighting_contract": material_lighting,
        "mesh_geometry_contract": mesh_geometry,
        "perspective_camera_contract": perspective_camera,
        "product_vertical_slice": False,
        "three_dimensional_texture_contract": texture_3d,
    }
    admission_ready = all(gates.values())
    if admission_ready:
        raise AssertionError("M14 evidence unexpectedly satisfies every 3D admission gate")
    return {
        "admission_ready": admission_ready,
        "decision": "retain-layered-2d",
        "facts": {
            "builtin_operations": operations,
            "pipeline_fields": pipeline_fields,
            "render_capability_fields": capability_fields,
            "render_export_count": len(exports),
            "render_exports": tuple(render_exports),
            "texture_descriptor_fields": texture_fields,
            "texture_formats": texture_formats,
        },
        "gates": gates,
        "layered_2d": layered_2d,
        "layered_2d_confirmed": layered_2d_confirmed,
        "ludoweave_version": __version__,
        "schema": _SCHEMA,
        "status": "deferred",
    }


def _sprite(*, layer: int, z: float, entity_index: int, entity_generation: int) -> SpriteInstance:
    return SpriteInstance(
        x=0.0,
        y=0.0,
        width=1.0,
        height=1.0,
        rotation_radians=0.0,
        uv_left=0.0,
        uv_top=0.0,
        uv_right=1.0,
        uv_bottom=1.0,
        layer=layer,
        z=z,
        entity_index=entity_index,
        entity_generation=entity_generation,
    )


if __name__ == "__main__":
    raise SystemExit(main())
