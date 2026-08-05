"""M14 installed-surface evidence remains deterministic and 3D-deferred."""

import json
import subprocess
import sys
from pathlib import Path

from ludoweave import __version__

_ROOT = Path(__file__).parents[2]
_EXAMPLE = _ROOT / "examples" / "constrained_3d_decision.py"


def _run() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE)),
        check=False,
        capture_output=True,
        text=True,
    )


def test_installed_surface_evidence_is_repeatable_and_defers_3d() -> None:
    first = _run()
    second = _run()

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = json.loads(first.stdout)
    assert document["schema"] == "ludoweave.evaluation.constrained-3d/1"
    assert document["status"] == "deferred"
    assert document["decision"] == "retain-layered-2d"
    assert document["admission_ready"] is False
    assert set(document) == {
        "admission_ready",
        "decision",
        "facts",
        "gates",
        "layered_2d",
        "layered_2d_confirmed",
        "ludoweave_version",
        "schema",
        "status",
    }
    assert document["gates"] == {
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
    facts = document["facts"]
    assert set(facts) == {
        "builtin_operations",
        "pipeline_fields",
        "render_capability_fields",
        "render_export_count",
        "render_exports",
        "texture_descriptor_fields",
        "texture_formats",
    }
    assert facts["builtin_operations"] == [
        "component.add",
        "component.patch",
        "component.remove",
        "entity.destroy",
        "entity.spawn",
        "resource.patch",
        "world.tick",
    ]
    assert facts["render_export_count"] == 47
    assert document["ludoweave_version"] == __version__
    assert facts["pipeline_fields"] == ["color_format", "topology", "blend", "label"]
    assert facts["render_capability_fields"] == [
        "backend",
        "max_texture_dimension_2d",
        "offscreen_capture",
        "timestamp_queries",
        "surface_formats",
    ]
    assert facts["texture_descriptor_fields"] == [
        "width",
        "height",
        "format",
        "usage",
        "layers",
        "label",
    ]
    assert facts["texture_formats"] == [
        "rgba8_unorm",
        "rgba8_unorm_srgb",
        "bgra8_unorm",
        "bgra8_unorm_srgb",
    ]
    assert document["layered_2d_confirmed"] is True
    assert document["layered_2d"] == {
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
    for forbidden in ("credential", "environment", "host", "path", "provider", "timing"):
        assert forbidden not in first.stdout.casefold()


def test_decision_example_rejects_arguments() -> None:
    result = subprocess.run(
        (sys.executable, str(_EXAMPLE), "--enable-3d"),
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "accepts no arguments" in result.stderr
