"""Render a two-sprite texture-atlas fixture through the optional wgpu backend."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Sequence

from ludoweave import __version__
from ludoweave.render import (
    Camera2D,
    ClearCommand,
    Color,
    CommandList,
    PipelineDescriptor,
    SpriteBatchCommand,
    SpriteInstance,
    SurfaceDescriptor,
    SurfaceKind,
    TextureData,
    TextureDescriptor,
    TextureFormat,
    TextureUsage,
)
from ludoweave.render.backends.wgpu import WgpuRenderDevice


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=64)
    parser.add_argument("--height", type=int, default=32)
    parser.add_argument(
        "--window",
        action="store_true",
        help="open a GLFW window instead of producing a headless capture",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.width <= 0 or arguments.height <= 0:
        _parser().error("--width and --height must be positive")
    kind = SurfaceKind.WINDOW if arguments.window else SurfaceKind.OFFSCREEN
    device = WgpuRenderDevice()
    try:
        surface = device.create_surface(
            SurfaceDescriptor(
                arguments.width,
                arguments.height,
                TextureFormat.RGBA8_UNORM,
                kind,
                "LudoWeave sprite example",
            )
        )
        texture = device.create_texture(
            TextureDescriptor(
                2,
                1,
                TextureFormat.RGBA8_UNORM,
                TextureUsage.SAMPLED | TextureUsage.COPY_DESTINATION,
                label="example-atlas",
            ),
            TextureData(b"\xff\x40\x20\xff\x20\x80\xff\xff", 8),
        )
        pipeline = device.create_pipeline(PipelineDescriptor(TextureFormat.RGBA8_UNORM))
        sprite_width = float(arguments.width) / 2.0
        instances = (
            SpriteInstance(
                -sprite_width / 2.0,
                0.0,
                sprite_width,
                float(arguments.height),
                0.0,
                0.0,
                0.0,
                0.5,
                1.0,
            ),
            SpriteInstance(
                sprite_width / 2.0,
                0.0,
                sprite_width,
                float(arguments.height),
                0.0,
                0.5,
                0.0,
                1.0,
                1.0,
                entity_index=1,
            ),
        )
        commands = CommandList(
            "example-frame",
            (
                ClearCommand(surface, Color(0.02, 0.02, 0.04, 1.0)),
                SpriteBatchCommand(pipeline, texture, instances),
            ),
            surface,
            Camera2D(
                viewport_width=float(arguments.width),
                viewport_height=float(arguments.height),
            ).orthographic_matrix(),
        )
        submission = device.submit((commands,))
        device.poll()
        result: dict[str, object] = {
            "schema": "ludoweave.example.hello_sprite/1",
            "version": __version__,
            "backend": device.name,
            "surface": kind.value,
            "width": arguments.width,
            "height": arguments.height,
            "draw_calls": submission.draw_calls,
            "sprite_instances": submission.sprite_instances,
            "fence_complete": device.is_fence_complete(submission.fence),
        }
        if kind is SurfaceKind.OFFSCREEN:
            capture = device.capture_surface(surface)
            result["capture_sha256"] = hashlib.sha256(capture.pixels).hexdigest()
            result["capture_bytes"] = len(capture.pixels)
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    finally:
        device.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
