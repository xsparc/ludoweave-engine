"""Run Clockwork Arena headlessly or render it through the optional wgpu adapter."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Sequence
from typing import cast

from ludoweave import __version__
from ludoweave.app import ActionBinding, ActionMap, InputSource, MappedInputSource
from ludoweave.platform import (
    CloseEvent,
    FocusEvent,
    InputEvent,
    KeyEvent,
    MouseButtonEvent,
    PointerEvent,
    ResizeEvent,
)
from ludoweave.render import (
    NullRenderDevice,
    PipelineDescriptor,
    RenderDevice,
    RenderExtractor,
    SurfaceDescriptor,
    SurfaceKind,
    TextureData,
    TextureDescriptor,
    TextureFormat,
    TextureUsage,
)
from ludoweave.samples import clockwork_input, create_clockwork_arena


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticks", type=int, default=600)
    parser.add_argument("--stress", type=int, default=1)
    parser.add_argument("--renderer", choices=("null", "wgpu"), default="null")
    parser.add_argument("--window", action="store_true")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="use WASD/arrows, mouse aim/fire, and R to restart in a wgpu window",
    )
    parser.add_argument("--render-every", type=int, default=1)
    return parser


def _device(name: str) -> RenderDevice:
    if name == "null":
        return NullRenderDevice()
    from ludoweave.render.backends.wgpu import WgpuRenderDevice

    return WgpuRenderDevice()


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.ticks < 0:
        _parser().error("--ticks must be non-negative")
    if not 1 <= arguments.stress <= 16:
        _parser().error("--stress must be between 1 and 16")
    if arguments.render_every <= 0:
        _parser().error("--render-every must be positive")
    if arguments.window and arguments.renderer != "wgpu":
        _parser().error("--window requires --renderer wgpu")
    if arguments.interactive and not arguments.window:
        _parser().error("--interactive requires --window")

    mapped = MappedInputSource(
        ActionMap(
            (
                ActionBinding("move.x", "key:a", -1.0),
                ActionBinding("move.x", "key:arrowleft", -1.0),
                ActionBinding("move.x", "key:d", 1.0),
                ActionBinding("move.x", "key:arrowright", 1.0),
                ActionBinding("move.y", "key:s", -1.0),
                ActionBinding("move.y", "key:arrowdown", -1.0),
                ActionBinding("move.y", "key:w", 1.0),
                ActionBinding("move.y", "key:arrowup", 1.0),
                ActionBinding("fire", "mouse:primary"),
                ActionBinding("restart", "key:r"),
                ActionBinding("move.x", "gamepad:0:axis:left_x", 1.0, 0.15),
                ActionBinding("move.y", "gamepad:0:axis:left_y", -1.0, 0.15),
                ActionBinding("aim.x", "gamepad:0:axis:right_x", 1.0, 0.15),
                ActionBinding("aim.y", "gamepad:0:axis:right_y", -1.0, 0.15),
                ActionBinding("fire", "gamepad:0:button:a"),
                ActionBinding("restart", "gamepad:0:button:start"),
            )
        )
    )
    input_source: InputSource = (
        mapped if arguments.interactive else clockwork_input(arguments.ticks)
    )
    arena = create_clockwork_arena(input_source, stress=arguments.stress)
    device = _device(arguments.renderer)
    draw_calls = 0
    sprite_instances = 0
    capture_hash: str | None = None
    kind = SurfaceKind.WINDOW if arguments.window else SurfaceKind.OFFSCREEN
    try:
        surface = device.create_surface(
            SurfaceDescriptor(
                960,
                540,
                TextureFormat.RGBA8_UNORM,
                kind,
                "LudoWeave Clockwork Arena",
            )
        )
        texture = device.create_texture(
            TextureDescriptor(
                1,
                1,
                TextureFormat.RGBA8_UNORM,
                TextureUsage.SAMPLED | TextureUsage.COPY_DESTINATION,
                label="clockwork-white",
            ),
            TextureData(b"\xff\xff\xff\xff", 4),
        )
        pipeline = device.create_pipeline(PipelineDescriptor(TextureFormat.RGBA8_UNORM))
        extractor = RenderExtractor()
        for index in range(arguments.ticks):
            should_close = False
            if arguments.interactive:
                for event in device.drain_surface_events(surface):
                    if type(event) in (KeyEvent, MouseButtonEvent, PointerEvent, FocusEvent):
                        mapped.feed(cast(InputEvent, event))
                    elif type(event) is ResizeEvent:
                        device.resize_surface(surface, event.width, event.height)
                    elif type(event) is CloseEvent:
                        should_close = True
                for event in device.poll_gamepads():
                    mapped.feed(event)
                if should_close:
                    break
            arena.tick()
            if (index + 1) % arguments.render_every != 0 and index + 1 != arguments.ticks:
                continue
            frame = arena.presentation(texture)
            command_list = extractor.build_command_list(
                frame,
                target=surface,
                pipeline=pipeline,
                label=f"clockwork-frame-{index + 1}",
            )
            submission = device.submit((command_list,))
            draw_calls += submission.draw_calls
            sprite_instances += submission.sprite_instances
            device.poll()
        if arguments.renderer == "wgpu" and kind is SurfaceKind.OFFSCREEN:
            capture = device.capture_surface(surface)
            capture_hash = hashlib.sha256(capture.pixels).hexdigest()
    finally:
        device.close()

    payload = {
        "arena": arena.summary().as_dict(),
        "capture_sha256": capture_hash,
        "draw_calls": draw_calls,
        "ludoweave_version": __version__,
        "renderer": arguments.renderer,
        "schema": "ludoweave.example.clockwork_arena/1",
        "sprite_instances": sprite_instances,
        "surface": kind.value,
    }
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
