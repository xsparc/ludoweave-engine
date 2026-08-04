"""Pure-Python packing and built-in shader data for the M3 sprite pipeline."""

from __future__ import annotations

import math
import struct
from collections.abc import Iterable, Sequence
from typing import cast

from ludoweave.core.errors import RenderError
from ludoweave.render.contracts import (
    Color,
    DebugLineCommand,
    DiagnosticTextCommand,
    SpriteInstance,
    TileBatchCommand,
)

SPRITE_INSTANCE_FLOATS = 16
SPRITE_INSTANCE_STRIDE = SPRITE_INSTANCE_FLOATS * 4

SPRITE_SHADER = """
struct Camera {
    matrix: mat4x4<f32>,
};

@group(0) @binding(0) var<uniform> camera: Camera;
@group(0) @binding(1) var sprite_texture: texture_2d<f32>;
@group(0) @binding(2) var sprite_sampler: sampler;

struct VertexInput {
    @builtin(vertex_index) vertex_index: u32,
    @location(0) position_size: vec4<f32>,
    @location(1) rotation_uv0: vec4<f32>,
    @location(2) uv1_tint_rg: vec4<f32>,
    @location(3) tint_ba_z_pad: vec4<f32>,
};

struct VertexOutput {
    @builtin(position) position: vec4<f32>,
    @location(0) uv: vec2<f32>,
    @location(1) tint: vec4<f32>,
};

@vertex
fn vs_main(input: VertexInput) -> VertexOutput {
    let corners = array<vec2<f32>, 6>(
        vec2<f32>(-0.5, -0.5), vec2<f32>(0.5, -0.5), vec2<f32>(0.5, 0.5),
        vec2<f32>(-0.5, -0.5), vec2<f32>(0.5, 0.5), vec2<f32>(-0.5, 0.5),
    );
    let unit_uv = array<vec2<f32>, 6>(
        vec2<f32>(0.0, 1.0), vec2<f32>(1.0, 1.0), vec2<f32>(1.0, 0.0),
        vec2<f32>(0.0, 1.0), vec2<f32>(1.0, 0.0), vec2<f32>(0.0, 0.0),
    );
    let local = corners[input.vertex_index] * input.position_size.zw;
    let sine = sin(input.rotation_uv0.x);
    let cosine = cos(input.rotation_uv0.x);
    let rotated = vec2<f32>(
        local.x * cosine - local.y * sine,
        local.x * sine + local.y * cosine,
    );
    let world = input.position_size.xy + rotated;
    let uv0 = input.rotation_uv0.yz;
    let uv1 = input.uv1_tint_rg.xy;
    var output: VertexOutput;
    output.position = camera.matrix * vec4<f32>(world, 0.0, 1.0);
    output.uv = mix(uv0, uv1, unit_uv[input.vertex_index]);
    output.tint = vec4<f32>(input.uv1_tint_rg.zw, input.tint_ba_z_pad.xy);
    return output;
}

@fragment
fn fs_main(input: VertexOutput) -> @location(0) vec4<f32> {
    return textureSample(sprite_texture, sprite_sampler, input.uv) * input.tint;
}
"""

_GLYPHS: dict[str, tuple[str, ...]] = {
    "?": ("11110", "00001", "00110", "00100", "00000", "00100", "00000"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "10000", "11110", "00001", "00001", "11110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01111", "10000", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00001", "00001", "00001", "00001", "10001", "10001", "01110"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "00110", "00110"),
    ":": ("00000", "00110", "00110", "00000", "00110", "00110", "00000"),
}


def pack_sprite_instances(instances: Sequence[SpriteInstance]) -> bytes:
    """Pack records into the provider-independent 64-byte instance layout."""

    values: list[float] = []
    for instance in instances:
        values.extend(
            (
                instance.x,
                instance.y,
                instance.width,
                instance.height,
                instance.rotation_radians,
                instance.uv_left,
                instance.uv_top,
                0.0,
                instance.uv_right,
                instance.uv_bottom,
                instance.tint.red,
                instance.tint.green,
                instance.tint.blue,
                instance.tint.alpha,
                instance.z,
                0.0,
            )
        )
    try:
        return struct.pack(f"<{len(values)}f", *values)
    except (OverflowError, struct.error) as error:
        raise RenderError(
            "sprite instance values cannot be represented as float32",
            code="render.instance_pack_failed",
            subsystem="render",
            phase="pack",
            details={"instances": len(instances)},
        ) from error


def tile_instances(command: TileBatchCommand) -> tuple[SpriteInstance, ...]:
    """Expand a tile batch into one instanced sprite draw, never per-tile draws."""

    return tuple(
        SpriteInstance(
            x=float(tile.x) * command.tile_width + command.tile_width * 0.5,
            y=float(tile.y) * command.tile_height + command.tile_height * 0.5,
            width=command.tile_width,
            height=command.tile_height,
            rotation_radians=0.0,
            uv_left=tile.uv_left,
            uv_top=tile.uv_top,
            uv_right=tile.uv_right,
            uv_bottom=tile.uv_bottom,
            layer=command.layer,
            entity_index=index,
        )
        for index, tile in enumerate(command.tiles)
    )


def debug_instances(
    commands: Iterable[DebugLineCommand | DiagnosticTextCommand],
) -> tuple[SpriteInstance, ...]:
    """Convert built-in debug lines and 5x7 diagnostic glyphs to white quads."""

    result: list[SpriteInstance] = []
    sequence = 0
    for command in commands:
        if type(command) is DebugLineCommand:
            delta_x = command.x2 - command.x1
            delta_y = command.y2 - command.y1
            length = math.hypot(delta_x, delta_y)
            if length == 0.0:
                length = command.width
            result.append(
                _white_instance(
                    x=(command.x1 + command.x2) * 0.5,
                    y=(command.y1 + command.y2) * 0.5,
                    width=length,
                    height=command.width,
                    rotation=math.atan2(delta_y, delta_x),
                    color=command.color,
                    sequence=sequence,
                )
            )
            sequence += 1
            continue
        diagnostic = cast(DiagnosticTextCommand, command)
        cursor_x = diagnostic.x
        cursor_y = diagnostic.y
        for character in diagnostic.text.upper():
            if character == "\n":
                cursor_x = diagnostic.x
                cursor_y -= 8.0
                continue
            if character != " ":
                glyph = _GLYPHS.get(character, _GLYPHS["?"])
                for row, pixels in enumerate(glyph):
                    for column, enabled in enumerate(pixels):
                        if enabled == "1":
                            result.append(
                                _white_instance(
                                    x=cursor_x + float(column) + 0.5,
                                    y=cursor_y - float(row) - 0.5,
                                    width=1.0,
                                    height=1.0,
                                    rotation=0.0,
                                    color=diagnostic.color,
                                    sequence=sequence,
                                )
                            )
                            sequence += 1
            cursor_x += 6.0
    return tuple(result)


def _white_instance(
    *,
    x: float,
    y: float,
    width: float,
    height: float,
    rotation: float,
    color: Color,
    sequence: int,
) -> SpriteInstance:
    return SpriteInstance(
        x=x,
        y=y,
        width=width,
        height=height,
        rotation_radians=rotation,
        uv_left=0.0,
        uv_top=0.0,
        uv_right=1.0,
        uv_bottom=1.0,
        tint=color,
        entity_index=sequence,
    )
