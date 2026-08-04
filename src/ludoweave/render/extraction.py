"""Immutable presentation extraction outside authoritative world state."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from math import cos, isfinite, sin

from ludoweave.core.errors import RenderError
from ludoweave.render.contracts import (
    Color,
    CommandList,
    DebugLineCommand,
    DiagnosticTextCommand,
    RenderCommand,
    SpriteBatchCommand,
    SpriteInstance,
    TileBatchCommand,
    TileInstance,
)
from ludoweave.render.handles import PipelineHandle, SurfaceHandle, TextureHandle


@dataclass(frozen=True, slots=True)
class Camera2D:
    """Backend-neutral orthographic presentation camera."""

    x: float = 0.0
    y: float = 0.0
    viewport_width: float = 1.0
    viewport_height: float = 1.0
    rotation_radians: float = 0.0
    zoom: float = 1.0

    def __post_init__(self) -> None:
        for field in (
            "x",
            "y",
            "viewport_width",
            "viewport_height",
            "rotation_radians",
            "zoom",
        ):
            value = getattr(self, field)
            if type(value) is not float or not isfinite(value):
                raise _extraction_error("camera values must be finite exact floats", field=field)
        if self.viewport_width <= 0.0 or self.viewport_height <= 0.0 or self.zoom <= 0.0:
            raise _extraction_error(
                "camera viewport dimensions and zoom must be positive", field="camera"
            )

    def orthographic_matrix(self) -> tuple[float, ...]:
        """Return a stable column-major 4x4 projection without backend objects."""

        scale_x = 2.0 * self.zoom / self.viewport_width
        scale_y = 2.0 * self.zoom / self.viewport_height
        cosine = cos(self.rotation_radians)
        sine = sin(self.rotation_radians)
        matrix = (
            scale_x * cosine,
            -scale_y * sine,
            0.0,
            0.0,
            scale_x * sine,
            scale_y * cosine,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            -scale_x * (cosine * self.x + sine * self.y),
            scale_y * (sine * self.x - cosine * self.y),
            0.0,
            1.0,
        )
        if any(not isfinite(value) for value in matrix):
            raise _extraction_error(
                "camera matrix cannot be represented with finite values", field="camera"
            )
        return matrix


@dataclass(frozen=True, slots=True)
class SpriteExtractionSource:
    """Previous/current simulation values copied into the presentation boundary."""

    texture: TextureHandle
    entity_index: int
    entity_generation: int
    previous_x: float
    previous_y: float
    current_x: float
    current_y: float
    previous_rotation: float
    current_rotation: float
    width: float
    height: float
    uv_left: float = 0.0
    uv_top: float = 0.0
    uv_right: float = 1.0
    uv_bottom: float = 1.0
    tint: Color = dataclass_field(default_factory=lambda: Color(1.0, 1.0, 1.0, 1.0))
    layer: int = 0
    z: float = 0.0

    def __post_init__(self) -> None:
        if type(self.texture) is not TextureHandle:
            raise _extraction_error("sprite extraction requires a texture handle", field="texture")
        for field in ("entity_index", "entity_generation", "layer"):
            value = getattr(self, field)
            if type(value) is not int or value < 0 or value > 2**63 - 1:
                raise _extraction_error(
                    "sprite extraction identity must be a non-negative signed 64-bit integer",
                    field=field,
                )
        for field in (
            "previous_x",
            "previous_y",
            "current_x",
            "current_y",
            "previous_rotation",
            "current_rotation",
            "width",
            "height",
            "uv_left",
            "uv_top",
            "uv_right",
            "uv_bottom",
            "z",
        ):
            value = getattr(self, field)
            if type(value) is not float or not isfinite(value):
                raise _extraction_error(
                    "sprite extraction values must be finite exact floats", field=field
                )
        if self.width <= 0.0 or self.height <= 0.0:
            raise _extraction_error("sprite extraction dimensions must be positive", field="size")
        if type(self.tint) is not Color:
            raise _extraction_error("sprite extraction tint must be a Color", field="tint")


@dataclass(frozen=True, slots=True)
class SpriteDrawGroup:
    """Canonical instances sharing one texture and therefore one normal draw."""

    texture: TextureHandle
    instances: tuple[SpriteInstance, ...]

    def __post_init__(self) -> None:
        if type(self.texture) is not TextureHandle:
            raise _extraction_error("sprite draw group requires a texture handle", field="texture")
        instances = tuple(self.instances)
        if not instances or any(type(item) is not SpriteInstance for item in instances):
            raise _extraction_error(
                "sprite draw group requires exact sprite instances", field="instances"
            )
        if tuple(sorted(instances, key=lambda item: item.sort_key)) != instances:
            raise _extraction_error("sprite draw group order is not canonical", field="instances")
        object.__setattr__(self, "instances", instances)


@dataclass(frozen=True, slots=True)
class TileDrawGroup:
    texture: TextureHandle
    tiles: tuple[TileInstance, ...]
    tile_width: float
    tile_height: float
    layer: int = 0

    def __post_init__(self) -> None:
        if type(self.texture) is not TextureHandle:
            raise _extraction_error("tile draw group requires a texture handle", field="texture")
        tiles = tuple(self.tiles)
        if any(type(tile) is not TileInstance for tile in tiles):
            raise _extraction_error("tile draw group requires exact tile instances", field="tiles")
        object.__setattr__(self, "tiles", tiles)
        for field in ("tile_width", "tile_height"):
            value = getattr(self, field)
            if type(value) is not float or not isfinite(value) or value <= 0.0:
                raise _extraction_error(
                    "tile draw group dimensions must be positive finite floats", field=field
                )
        if type(self.layer) is not int or self.layer < 0:
            raise _extraction_error("tile draw group layer must be non-negative", field="layer")


@dataclass(frozen=True, slots=True)
class PresentationFrame:
    """Complete immutable non-authoritative input consumed by every renderer."""

    completed_ticks: int
    source_tick: int | None
    interpolation_alpha: float
    camera: Camera2D
    sprite_groups: tuple[SpriteDrawGroup, ...] = ()
    tile_groups: tuple[TileDrawGroup, ...] = ()
    debug_lines: tuple[DebugLineCommand, ...] = ()
    diagnostic_text: tuple[DiagnosticTextCommand, ...] = ()

    def __post_init__(self) -> None:
        if (
            type(self.completed_ticks) is not int
            or self.completed_ticks < 0
            or self.completed_ticks > 2**63 - 1
        ):
            raise _extraction_error(
                "completed tick count must be a non-negative signed 64-bit integer",
                field="completed_ticks",
            )
        expected_source_tick = self.completed_ticks - 1 if self.completed_ticks else None
        if self.source_tick != expected_source_tick or (
            self.source_tick is not None and type(self.source_tick) is not int
        ):
            raise _extraction_error(
                "presentation source tick must identify the latest completed tick",
                field="source_tick",
            )
        if (
            type(self.interpolation_alpha) is not float
            or not isfinite(self.interpolation_alpha)
            or not 0.0 <= self.interpolation_alpha <= 1.0
        ):
            raise _extraction_error(
                "presentation interpolation alpha must be a normalized finite float",
                field="interpolation_alpha",
            )
        if type(self.camera) is not Camera2D:
            raise _extraction_error("presentation frame requires a Camera2D", field="camera")
        for field, expected in (
            ("sprite_groups", SpriteDrawGroup),
            ("tile_groups", TileDrawGroup),
            ("debug_lines", DebugLineCommand),
            ("diagnostic_text", DiagnosticTextCommand),
        ):
            values = tuple(getattr(self, field))
            if any(type(value) is not expected for value in values):
                raise _extraction_error(
                    "presentation frame collection contains an invalid record", field=field
                )
            object.__setattr__(self, field, values)

    @property
    def visible_sprite_count(self) -> int:
        return sum(len(group.instances) for group in self.sprite_groups)

    @property
    def normal_sprite_draw_count(self) -> int:
        return len(self.sprite_groups)


class RenderExtractor:
    """Pure presentation extraction with deterministic grouping and sorting."""

    __slots__ = ()

    def extract_sprites(
        self,
        sources: Iterable[SpriteExtractionSource],
        *,
        completed_ticks: int,
        interpolation_alpha: float,
        camera: Camera2D,
    ) -> PresentationFrame:
        if type(completed_ticks) is not int or completed_ticks < 0 or completed_ticks > 2**63 - 1:
            raise _extraction_error(
                "completed tick count must be a non-negative signed 64-bit integer",
                field="completed_ticks",
            )
        if (
            type(interpolation_alpha) is not float
            or not isfinite(interpolation_alpha)
            or not 0.0 <= interpolation_alpha <= 1.0
        ):
            raise _extraction_error(
                "presentation interpolation alpha must be a normalized finite float",
                field="interpolation_alpha",
            )
        if type(camera) is not Camera2D:
            raise _extraction_error("extraction requires a Camera2D", field="camera")
        try:
            frozen_sources = tuple(sources)
        except Exception as error:
            raise _extraction_error(
                "sprite extraction source iteration failed", field="sources"
            ) from error
        if any(type(source) is not SpriteExtractionSource for source in frozen_sources):
            raise _extraction_error(
                "sprite extraction requires exact source records", field="sources"
            )

        grouped: dict[TextureHandle, list[SpriteInstance]] = {}
        alpha = interpolation_alpha
        for source in frozen_sources:
            instance = SpriteInstance(
                x=source.previous_x + (source.current_x - source.previous_x) * alpha,
                y=source.previous_y + (source.current_y - source.previous_y) * alpha,
                width=source.width,
                height=source.height,
                rotation_radians=source.previous_rotation
                + (source.current_rotation - source.previous_rotation) * alpha,
                uv_left=source.uv_left,
                uv_top=source.uv_top,
                uv_right=source.uv_right,
                uv_bottom=source.uv_bottom,
                tint=source.tint,
                layer=source.layer,
                z=source.z,
                entity_index=source.entity_index,
                entity_generation=source.entity_generation,
            )
            grouped.setdefault(source.texture, []).append(instance)

        groups = tuple(
            SpriteDrawGroup(
                texture,
                tuple(sorted(instances, key=lambda item: item.sort_key)),
            )
            for texture, instances in sorted(
                grouped.items(),
                key=lambda item: (item[0].scope.bytes, item[0].index, item[0].generation),
            )
        )
        return PresentationFrame(
            completed_ticks,
            completed_ticks - 1 if completed_ticks else None,
            alpha,
            camera,
            sprite_groups=groups,
        )

    def build_command_list(
        self,
        frame: PresentationFrame,
        *,
        target: SurfaceHandle | TextureHandle,
        pipeline: PipelineHandle,
        label: str = "presentation-frame",
    ) -> CommandList:
        """Translate one immutable frame into equivalent backend input."""

        if type(frame) is not PresentationFrame:
            raise _extraction_error(
                "command extraction requires a presentation frame", field="frame"
            )
        if type(target) not in (SurfaceHandle, TextureHandle):
            raise _extraction_error("command extraction requires a render target", field="target")
        if type(pipeline) is not PipelineHandle:
            raise _extraction_error(
                "command extraction requires a pipeline handle", field="pipeline"
            )
        commands: list[RenderCommand] = [
            SpriteBatchCommand(pipeline, group.texture, group.instances)
            for group in frame.sprite_groups
        ]
        commands.extend(
            TileBatchCommand(
                pipeline,
                group.texture,
                group.tiles,
                group.tile_width,
                group.tile_height,
                group.layer,
            )
            for group in frame.tile_groups
        )
        commands.extend(frame.debug_lines)
        commands.extend(frame.diagnostic_text)
        return CommandList(label, tuple(commands), target, frame.camera.orthographic_matrix())


def _extraction_error(message: str, *, field: str) -> RenderError:
    return RenderError(
        message,
        code="render.invalid_extraction",
        subsystem="render",
        phase="extract",
        details={"field": field},
    )
