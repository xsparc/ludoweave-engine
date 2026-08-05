"""Immutable backend-neutral rendering descriptors and command records."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from enum import IntFlag, StrEnum
from math import isfinite
from typing import cast

from ludoweave.core.errors import RenderError
from ludoweave.render.handles import (
    FenceHandle,
    PipelineHandle,
    RenderResourceHandle,
    SurfaceHandle,
    TextureHandle,
)

_LABEL = re.compile(r"[^\x00-\x1f\x7f]{1,128}\Z")
_MAX_SIZE = 2**31 - 1
_IDENTITY_MATRIX = (
    1.0,
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
    0.0,
    0.0,
    0.0,
    0.0,
    1.0,
)


class BufferUsage(IntFlag):
    """Backend-neutral intended buffer use."""

    VERTEX = 1
    INDEX = 2
    UNIFORM = 4
    COPY_SOURCE = 8
    COPY_DESTINATION = 16


class TextureUsage(IntFlag):
    """Backend-neutral intended texture use."""

    SAMPLED = 1
    RENDER_ATTACHMENT = 2
    COPY_SOURCE = 4
    COPY_DESTINATION = 8


class TextureFormat(StrEnum):
    """Small portable color-format surface for the M3 renderer."""

    RGBA8_UNORM = "rgba8_unorm"
    RGBA8_UNORM_SRGB = "rgba8_unorm_srgb"
    BGRA8_UNORM = "bgra8_unorm"
    BGRA8_UNORM_SRGB = "bgra8_unorm_srgb"


class PrimitiveTopology(StrEnum):
    TRIANGLE_LIST = "triangle_list"
    LINE_LIST = "line_list"


class BlendMode(StrEnum):
    OPAQUE = "opaque"
    ALPHA = "alpha"
    ADDITIVE = "additive"


class SurfaceKind(StrEnum):
    WINDOW = "window"
    OFFSCREEN = "offscreen"


@dataclass(frozen=True, slots=True)
class Color:
    """Linear RGBA color with finite normalized channels."""

    red: float = 0.0
    green: float = 0.0
    blue: float = 0.0
    alpha: float = 1.0

    def __post_init__(self) -> None:
        for field in ("red", "green", "blue", "alpha"):
            value = getattr(self, field)
            if type(value) is not float or not isfinite(value) or not 0.0 <= value <= 1.0:
                raise _descriptor_error(
                    "color channels must be finite floats between zero and one",
                    field=field,
                    actual_type=type(value).__name__,
                )


@dataclass(frozen=True, slots=True)
class BufferDescriptor:
    size: int
    usage: BufferUsage
    label: str = "buffer"

    def __post_init__(self) -> None:
        _positive_size(self.size, field="size")
        _exact_flag(self.usage, BufferUsage, field="usage")
        _label(self.label)


@dataclass(frozen=True, slots=True)
class BufferData:
    value: bytes

    def __post_init__(self) -> None:
        if type(self.value) is not bytes:
            raise _descriptor_error(
                "buffer data must be immutable bytes",
                field="value",
                actual_type=type(self.value).__name__,
            )


@dataclass(frozen=True, slots=True)
class TextureDescriptor:
    width: int
    height: int
    format: TextureFormat
    usage: TextureUsage
    layers: int = 1
    label: str = "texture"

    def __post_init__(self) -> None:
        _positive_size(self.width, field="width")
        _positive_size(self.height, field="height")
        _positive_size(self.layers, field="layers")
        _exact_enum(self.format, TextureFormat, field="format")
        _exact_flag(self.usage, TextureUsage, field="usage")
        _label(self.label)


@dataclass(frozen=True, slots=True)
class TextureData:
    value: bytes
    bytes_per_row: int

    def __post_init__(self) -> None:
        if type(self.value) is not bytes or not self.value:
            raise _descriptor_error(
                "texture data must be non-empty immutable bytes",
                field="value",
                actual_type=type(self.value).__name__,
            )
        _positive_size(self.bytes_per_row, field="bytes_per_row")


@dataclass(frozen=True, slots=True)
class PipelineDescriptor:
    color_format: TextureFormat
    topology: PrimitiveTopology = PrimitiveTopology.TRIANGLE_LIST
    blend: BlendMode = BlendMode.ALPHA
    label: str = "pipeline"

    def __post_init__(self) -> None:
        _exact_enum(self.color_format, TextureFormat, field="color_format")
        _exact_enum(self.topology, PrimitiveTopology, field="topology")
        _exact_enum(self.blend, BlendMode, field="blend")
        _label(self.label)


@dataclass(frozen=True, slots=True)
class SurfaceDescriptor:
    width: int
    height: int
    format: TextureFormat = TextureFormat.BGRA8_UNORM_SRGB
    kind: SurfaceKind = SurfaceKind.WINDOW
    label: str = "surface"

    def __post_init__(self) -> None:
        _positive_size(self.width, field="width")
        _positive_size(self.height, field="height")
        _exact_enum(self.format, TextureFormat, field="format")
        _exact_enum(self.kind, SurfaceKind, field="kind")
        _label(self.label)


@dataclass(frozen=True, slots=True)
class RenderCapabilities:
    backend: str
    max_texture_dimension_2d: int
    offscreen_capture: bool
    timestamp_queries: bool
    surface_formats: tuple[TextureFormat, ...]

    def __post_init__(self) -> None:
        _label(self.backend, field="backend")
        _positive_size(self.max_texture_dimension_2d, field="max_texture_dimension_2d")
        if type(self.offscreen_capture) is not bool or type(self.timestamp_queries) is not bool:
            raise _descriptor_error(
                "render capability flags must be exact booleans",
                field="capability",
                actual_type="non_bool",
            )
        formats = tuple(self.surface_formats)
        if not formats or any(type(item) is not TextureFormat for item in formats):
            raise _descriptor_error(
                "render capabilities require exact supported texture formats",
                field="surface_formats",
                actual_type=type(self.surface_formats).__name__,
            )
        object.__setattr__(self, "surface_formats", formats)


@dataclass(frozen=True, slots=True)
class CaptureImage:
    """Immutable normalized RGBA8 capture with no array/backend exposure."""

    width: int
    height: int
    pixels: bytes
    format: TextureFormat = TextureFormat.RGBA8_UNORM

    def __post_init__(self) -> None:
        _positive_size(self.width, field="width")
        _positive_size(self.height, field="height")
        if type(self.pixels) is not bytes or len(self.pixels) != self.width * self.height * 4:
            raise _descriptor_error(
                "capture pixels must be exact tightly packed immutable RGBA8 bytes",
                field="pixels",
                actual_type=type(self.pixels).__name__,
            )
        if self.format is not TextureFormat.RGBA8_UNORM:
            raise _descriptor_error(
                "capture format must be normalized RGBA8 unorm",
                field="format",
                actual_type=type(self.format).__name__,
            )


@dataclass(frozen=True, slots=True)
class ClearCommand:
    target: TextureHandle | SurfaceHandle
    color: Color

    def __post_init__(self) -> None:
        if type(self.target) not in (TextureHandle, SurfaceHandle) or type(self.color) is not Color:
            raise _command_error("clear command contains an invalid target or color")


@dataclass(frozen=True, slots=True)
class SpriteInstance:
    """One packed, immutable sprite presentation instance."""

    x: float
    y: float
    width: float
    height: float
    rotation_radians: float
    uv_left: float
    uv_top: float
    uv_right: float
    uv_bottom: float
    tint: Color = dataclass_field(default_factory=lambda: Color(1.0, 1.0, 1.0, 1.0))
    layer: int = 0
    z: float = 0.0
    entity_index: int = 0
    entity_generation: int = 0

    def __post_init__(self) -> None:
        for field in (
            "x",
            "y",
            "width",
            "height",
            "rotation_radians",
            "uv_left",
            "uv_top",
            "uv_right",
            "uv_bottom",
            "z",
        ):
            value = getattr(self, field)
            if type(value) is not float or not isfinite(value):
                raise _command_error("sprite values must be finite exact floats", field=field)
        if self.width <= 0.0 or self.height <= 0.0:
            raise _command_error("sprite dimensions must be positive", field="size")
        if not (
            0.0 <= self.uv_left < self.uv_right <= 1.0
            and 0.0 <= self.uv_top < self.uv_bottom <= 1.0
        ):
            raise _command_error("sprite UV rectangle must be normalized and non-empty", field="uv")
        if type(self.tint) is not Color:
            raise _command_error("sprite tint must be a Color", field="tint")
        for field in ("layer", "entity_index", "entity_generation"):
            value = getattr(self, field)
            if type(value) is not int or value < 0 or value > 2**63 - 1:
                raise _command_error(
                    "sprite identity fields must be non-negative signed 64-bit integers",
                    field=field,
                )

    @property
    def sort_key(self) -> tuple[int, float, int, int]:
        return (self.layer, self.z, self.entity_index, self.entity_generation)


@dataclass(frozen=True, slots=True)
class SpriteBatchCommand:
    pipeline: PipelineHandle
    texture: TextureHandle
    instances: tuple[SpriteInstance, ...]

    def __post_init__(self) -> None:
        if type(self.pipeline) is not PipelineHandle or type(self.texture) is not TextureHandle:
            raise _command_error("sprite batch requires pipeline and texture handles")
        instances = _freeze_exact(self.instances, SpriteInstance, field="instances")
        if not instances:
            raise _command_error("sprite batch cannot be empty", field="instances")
        if tuple(sorted(instances, key=lambda item: item.sort_key)) != instances:
            raise _command_error("sprite batch instances must use canonical layer/z/entity order")
        object.__setattr__(self, "instances", instances)


@dataclass(frozen=True, slots=True)
class TileInstance:
    x: int
    y: int
    uv_left: float
    uv_top: float
    uv_right: float
    uv_bottom: float

    def __post_init__(self) -> None:
        if (
            type(self.x) is not int
            or type(self.y) is not int
            or not -(2**31) <= self.x < 2**31
            or not -(2**31) <= self.y < 2**31
        ):
            raise _command_error("tile coordinates must be exact integers")
        for field in ("uv_left", "uv_top", "uv_right", "uv_bottom"):
            value = getattr(self, field)
            if type(value) is not float or not isfinite(value):
                raise _command_error("tile UV values must be finite floats", field=field)
        if not (
            0.0 <= self.uv_left < self.uv_right <= 1.0
            and 0.0 <= self.uv_top < self.uv_bottom <= 1.0
        ):
            raise _command_error("tile UV rectangle must be normalized and non-empty", field="uv")


@dataclass(frozen=True, slots=True)
class TileBatchCommand:
    pipeline: PipelineHandle
    texture: TextureHandle
    tiles: tuple[TileInstance, ...]
    tile_width: float
    tile_height: float
    layer: int = 0

    def __post_init__(self) -> None:
        if type(self.pipeline) is not PipelineHandle or type(self.texture) is not TextureHandle:
            raise _command_error("tile batch requires pipeline and texture handles")
        tiles = _freeze_exact(self.tiles, TileInstance, field="tiles")
        if not tiles:
            raise _command_error("tile batch cannot be empty", field="tiles")
        object.__setattr__(self, "tiles", tiles)
        for field in ("tile_width", "tile_height"):
            value = getattr(self, field)
            if type(value) is not float or not isfinite(value) or value <= 0.0:
                raise _command_error("tile dimensions must be positive finite floats", field=field)
        if type(self.layer) is not int or self.layer < 0:
            raise _command_error("tile layer must be a non-negative integer", field="layer")


@dataclass(frozen=True, slots=True)
class DebugLineCommand:
    x1: float
    y1: float
    x2: float
    y2: float
    color: Color
    width: float = 1.0

    def __post_init__(self) -> None:
        for field in ("x1", "y1", "x2", "y2", "width"):
            value = getattr(self, field)
            if type(value) is not float or not isfinite(value):
                raise _command_error("debug-line values must be finite floats", field=field)
        if self.width <= 0.0 or type(self.color) is not Color:
            raise _command_error("debug line requires positive width and a Color")


@dataclass(frozen=True, slots=True)
class DiagnosticTextCommand:
    text: str
    x: float
    y: float
    color: Color = dataclass_field(default_factory=lambda: Color(1.0, 1.0, 1.0, 1.0))

    def __post_init__(self) -> None:
        if type(self.text) is not str or not self.text or len(self.text) > 1024:
            raise _command_error("diagnostic text must be bounded non-empty text", field="text")
        for field in ("x", "y"):
            value = getattr(self, field)
            if type(value) is not float or not isfinite(value):
                raise _command_error(
                    "diagnostic text coordinates must be finite floats", field=field
                )
        if type(self.color) is not Color:
            raise _command_error("diagnostic text color must be a Color", field="color")


type RenderCommand = (
    ClearCommand | SpriteBatchCommand | TileBatchCommand | DebugLineCommand | DiagnosticTextCommand
)


@dataclass(frozen=True, slots=True)
class CommandList:
    label: str
    commands: tuple[RenderCommand, ...]
    target: TextureHandle | SurfaceHandle | None = None
    camera_matrix: tuple[float, ...] = _IDENTITY_MATRIX

    def __post_init__(self) -> None:
        _label(self.label)
        commands = tuple(self.commands)
        allowed = (
            ClearCommand,
            SpriteBatchCommand,
            TileBatchCommand,
            DebugLineCommand,
            DiagnosticTextCommand,
        )
        if any(type(command) not in allowed for command in commands):
            raise _command_error("command list contains an unsupported command")
        object.__setattr__(self, "commands", commands)
        clears = tuple(
            index for index, command in enumerate(commands) if type(command) is ClearCommand
        )
        if len(clears) > 1 or (clears and clears[0] != 0):
            raise _command_error(
                "a command list may begin with at most one clear",
                field="commands",
            )
        if self.target is not None and type(self.target) not in (TextureHandle, SurfaceHandle):
            raise _command_error(
                "command-list target must be an exact render target", field="target"
            )
        matrix = tuple(self.camera_matrix)
        if len(matrix) != 16 or any(
            type(value) is not float or not isfinite(value) for value in matrix
        ):
            raise _command_error(
                "camera matrix must contain sixteen finite exact floats",
                field="camera_matrix",
            )
        object.__setattr__(self, "camera_matrix", matrix)
        draws = (SpriteBatchCommand, TileBatchCommand, DebugLineCommand, DiagnosticTextCommand)
        if any(type(command) in draws for command in commands) and self.target is None:
            raise _command_error("draw command lists require an explicit target", field="target")
        for command in commands:
            if (
                type(command) is ClearCommand
                and self.target is not None
                and command.target != self.target
            ):
                raise _command_error(
                    "clear target must match the command-list target",
                    field="target",
                )


@dataclass(frozen=True, slots=True)
class Submission:
    fence: FenceHandle
    command_lists: tuple[CommandList, ...]
    draw_calls: int
    sprite_instances: int
    tile_instances: int = 0
    debug_primitives: int = 0

    def __post_init__(self) -> None:
        if type(self.fence) is not FenceHandle:
            raise _command_error("submission requires a fence handle", field="fence")
        command_lists = _freeze_exact(self.command_lists, CommandList, field="command_lists")
        object.__setattr__(self, "command_lists", command_lists)
        for field in ("draw_calls", "sprite_instances", "tile_instances", "debug_primitives"):
            value = getattr(self, field)
            if type(value) is not int or value < 0:
                raise _command_error(
                    "submission counters must be non-negative integers", field=field
                )


def referenced_resources(command: RenderCommand) -> tuple[RenderResourceHandle, ...]:
    """Return backend-neutral resource references in one command."""

    if type(command) is ClearCommand:
        return (command.target,)
    if type(command) in (SpriteBatchCommand, TileBatchCommand):
        batch = cast(SpriteBatchCommand | TileBatchCommand, command)
        return (batch.pipeline, batch.texture)
    return ()


def _freeze_exact[ValueT](
    values: Iterable[ValueT], expected: type[ValueT], *, field: str
) -> tuple[ValueT, ...]:
    try:
        frozen = tuple(values)
    except Exception as error:
        raise _command_error("render record collection could not be frozen", field=field) from error
    if any(type(value) is not expected for value in frozen):
        raise _command_error("render record collection has an invalid item", field=field)
    return frozen


def _positive_size(value: object, *, field: str) -> int:
    if type(value) is not int or value <= 0 or value > _MAX_SIZE:
        raise _descriptor_error(
            "render sizes must be positive bounded integers",
            field=field,
            actual_type=type(value).__name__,
        )
    return value


def _label(value: object, *, field: str = "label") -> str:
    if type(value) is not str or _LABEL.fullmatch(value) is None or not value.strip():
        raise _descriptor_error(
            "render labels must be bounded printable non-whitespace text",
            field=field,
            actual_type=type(value).__name__,
        )
    return value


def _exact_enum[EnumT](value: object, enum_type: type[EnumT], *, field: str) -> EnumT:
    if type(value) is not enum_type:
        raise _descriptor_error(
            "render descriptor enum has the wrong exact type",
            field=field,
            actual_type=type(value).__name__,
        )
    return cast(EnumT, value)


def _exact_flag[FlagT](value: object, flag_type: type[FlagT], *, field: str) -> FlagT:
    allowed = 0
    for member in flag_type:  # type: ignore[union-attr]
        allowed |= int(member)  # type: ignore[arg-type]
    if type(value) is not flag_type or not bool(value) or int(value) & ~allowed:  # type: ignore[arg-type]
        raise _descriptor_error(
            "render descriptor usage must be a non-empty exact flag value",
            field=field,
            actual_type=type(value).__name__,
        )
    return cast(FlagT, value)


def _descriptor_error(message: str, *, field: str, actual_type: str) -> RenderError:
    return RenderError(
        message,
        code="render.invalid_descriptor",
        subsystem="render",
        phase="descriptor",
        details={"field": field, "actual_type": actual_type},
    )


def _command_error(message: str, *, field: str = "command") -> RenderError:
    return RenderError(
        message,
        code="render.invalid_command",
        subsystem="render",
        phase="command",
        details={"field": field},
    )
