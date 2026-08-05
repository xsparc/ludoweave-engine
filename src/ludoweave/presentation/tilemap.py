"""Bounded immutable tilemaps with deterministic culling and render extraction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from ludoweave.presentation._validation import (
    bounded_int,
    freeze_bounded,
    freeze_bounded_exact,
    normalized_uv,
    stable_name,
)
from ludoweave.presentation.errors import presentation_error
from ludoweave.render.contracts import TileInstance
from ludoweave.render.extraction import TileDrawGroup
from ludoweave.render.handles import TextureHandle

_COORD_MIN = -(2**31)
_COORD_MAX = 2**31 - 1
_REGION_MAX_EXCLUSIVE = 2**31
_MAX_CHUNK_CELLS = 65_536
_MAX_MAP_CELLS = 1_000_000
_MAX_CHUNKS_PER_LAYER = 4096
_MAX_LAYERS = 256
_MAX_TILES = 65_536


@dataclass(frozen=True, slots=True)
class TileDefinition:
    tile_id: int
    uv_left: float
    uv_top: float
    uv_right: float
    uv_bottom: float

    def __post_init__(self) -> None:
        bounded_int(
            self.tile_id,
            phase="tile_definition",
            field="tile_id",
            maximum=2**31 - 1,
        )
        normalized_uv(
            self.uv_left,
            self.uv_top,
            self.uv_right,
            self.uv_bottom,
            phase="tile_definition",
        )


@dataclass(frozen=True, slots=True)
class TileChunk:
    """Dense row-major cells for one bounded, non-overlapping region."""

    origin_x: int
    origin_y: int
    width: int
    height: int
    cells: tuple[int | None, ...]

    def __post_init__(self) -> None:
        bounded_int(
            self.origin_x,
            phase="tile_chunk",
            field="origin_x",
            minimum=_COORD_MIN,
            maximum=_COORD_MAX,
        )
        bounded_int(
            self.origin_y,
            phase="tile_chunk",
            field="origin_y",
            minimum=_COORD_MIN,
            maximum=_COORD_MAX,
        )
        bounded_int(
            self.width,
            phase="tile_chunk",
            field="width",
            minimum=1,
            maximum=_MAX_CHUNK_CELLS,
        )
        bounded_int(
            self.height,
            phase="tile_chunk",
            field="height",
            minimum=1,
            maximum=_MAX_CHUNK_CELLS,
        )
        cell_count = self.width * self.height
        if cell_count > _MAX_CHUNK_CELLS:
            raise presentation_error(
                "tile chunk exceeds the bounded cell count",
                phase="tile_chunk",
                details={"field": "cells", "maximum": _MAX_CHUNK_CELLS},
            )
        if (
            self.origin_x + self.width - 1 > _COORD_MAX
            or self.origin_y + self.height - 1 > _COORD_MAX
        ):
            raise presentation_error(
                "tile chunk coordinates exceed signed 32-bit bounds",
                phase="tile_chunk",
                details={"field": "bounds"},
            )
        frozen_cells = freeze_bounded(
            self.cells,
            maximum=cell_count,
            phase="tile_chunk",
            field="cells",
        )
        cells = cast(tuple[int | None, ...], frozen_cells)
        if len(cells) != cell_count or any(
            value is not None and (type(value) is not int or not 0 <= value <= 2**31 - 1)
            for value in cells
        ):
            raise presentation_error(
                "tile chunk cells must match dimensions and contain bounded tile IDs or None",
                phase="tile_chunk",
                details={"field": "cells", "expected": cell_count},
            )
        object.__setattr__(self, "cells", cells)

    def tile_at(self, x: int, y: int) -> int | None:
        bounded_int(
            x,
            phase="tile_query",
            field="x",
            minimum=_COORD_MIN,
            maximum=_COORD_MAX,
        )
        bounded_int(
            y,
            phase="tile_query",
            field="y",
            minimum=_COORD_MIN,
            maximum=_COORD_MAX,
        )
        if not (
            self.origin_x <= x < self.origin_x + self.width
            and self.origin_y <= y < self.origin_y + self.height
        ):
            return None
        index = (y - self.origin_y) * self.width + (x - self.origin_x)
        return self.cells[index]


@dataclass(frozen=True, slots=True)
class TileLayer:
    name: str
    layer: int
    chunks: tuple[TileChunk, ...]
    visible: bool = True

    def __post_init__(self) -> None:
        stable_name(self.name, phase="tile_layer")
        bounded_int(self.layer, phase="tile_layer", field="layer", maximum=2**31 - 1)
        chunks = freeze_bounded_exact(
            self.chunks,
            TileChunk,
            maximum=_MAX_CHUNKS_PER_LAYER,
            phase="tile_layer",
            field="chunks",
        )
        if type(self.visible) is not bool:
            raise presentation_error(
                "tile layer visibility must be an exact boolean",
                phase="tile_layer",
                details={"field": "visible"},
            )
        ordered = tuple(sorted(chunks, key=lambda chunk: (chunk.origin_y, chunk.origin_x)))
        cell_count = sum(chunk.width * chunk.height for chunk in ordered)
        if cell_count > _MAX_MAP_CELLS:
            raise presentation_error(
                "tile layer exceeds the bounded authored cell count",
                phase="tile_layer",
                details={"field": "chunks", "maximum": _MAX_MAP_CELLS},
            )
        intervals_by_row: dict[int, list[tuple[int, int]]] = {}
        for chunk in ordered:
            interval = (chunk.origin_x, chunk.origin_x + chunk.width)
            for y in range(chunk.origin_y, chunk.origin_y + chunk.height):
                intervals_by_row.setdefault(y, []).append(interval)
        for intervals in intervals_by_row.values():
            previous_end: int | None = None
            for start, end in sorted(intervals):
                if previous_end is not None and start < previous_end:
                    raise presentation_error(
                        "tile chunks in one layer may not overlap",
                        phase="tile_layer",
                        details={"field": "chunks", "layer": self.name},
                    )
                previous_end = end
        object.__setattr__(self, "chunks", ordered)


@dataclass(frozen=True, slots=True)
class TileMap:
    """Immutable authored map; renderer handles remain outside the data model."""

    name: str
    tile_width: int
    tile_height: int
    tiles: tuple[TileDefinition, ...]
    layers: tuple[TileLayer, ...]

    def __post_init__(self) -> None:
        stable_name(self.name, phase="tilemap")
        bounded_int(
            self.tile_width,
            phase="tilemap",
            field="tile_width",
            minimum=1,
            maximum=2**16 - 1,
        )
        bounded_int(
            self.tile_height,
            phase="tilemap",
            field="tile_height",
            minimum=1,
            maximum=2**16 - 1,
        )
        tiles = freeze_bounded_exact(
            self.tiles,
            TileDefinition,
            maximum=_MAX_TILES,
            phase="tilemap",
            field="tiles",
        )
        layers = freeze_bounded_exact(
            self.layers,
            TileLayer,
            maximum=_MAX_LAYERS,
            phase="tilemap",
            field="layers",
        )
        tile_ids = tuple(tile.tile_id for tile in tiles)
        layer_ids = tuple(layer.layer for layer in layers)
        layer_names = tuple(layer.name for layer in layers)
        if len(set(tile_ids)) != len(tile_ids):
            raise presentation_error(
                "tile definition IDs must be unique",
                phase="tilemap",
                details={"field": "tiles"},
            )
        if len(set(layer_ids)) != len(layer_ids) or len(set(layer_names)) != len(layer_names):
            raise presentation_error(
                "tile layer names and numeric layers must be unique",
                phase="tilemap",
                details={"field": "layers"},
            )
        total_cells = sum(chunk.width * chunk.height for layer in layers for chunk in layer.chunks)
        if total_cells > _MAX_MAP_CELLS:
            raise presentation_error(
                "tilemap exceeds the bounded authored cell count",
                phase="tilemap",
                details={"field": "cells", "maximum": _MAX_MAP_CELLS},
            )
        declared = set(tile_ids)
        if any(
            cell is not None and cell not in declared
            for layer in layers
            for chunk in layer.chunks
            for cell in chunk.cells
        ):
            raise presentation_error(
                "tilemap cell references an undeclared tile ID",
                phase="tilemap",
                details={"field": "cells"},
            )
        object.__setattr__(self, "tiles", tuple(sorted(tiles, key=lambda tile: tile.tile_id)))
        object.__setattr__(self, "layers", tuple(sorted(layers, key=lambda layer: layer.layer)))


def extract_tile_groups(
    tilemap: TileMap,
    texture: TextureHandle,
    *,
    min_x: int,
    min_y: int,
    max_x: int,
    max_y: int,
) -> tuple[TileDrawGroup, ...]:
    """Cull a half-open cell region and produce canonical per-layer batches."""

    if type(tilemap) is not TileMap:
        raise presentation_error(
            "tile extraction requires an exact TileMap",
            phase="tile_extract",
            details={"field": "tilemap", "actual_type": type(tilemap).__name__},
        )
    if type(texture) is not TextureHandle:
        raise presentation_error(
            "tile extraction requires an exact texture handle",
            phase="tile_extract",
            details={"field": "texture", "actual_type": type(texture).__name__},
        )
    for field, value, maximum in (
        ("min_x", min_x, _COORD_MAX),
        ("min_y", min_y, _COORD_MAX),
        ("max_x", max_x, _REGION_MAX_EXCLUSIVE),
        ("max_y", max_y, _REGION_MAX_EXCLUSIVE),
    ):
        bounded_int(
            value,
            phase="tile_extract",
            field=field,
            minimum=_COORD_MIN,
            maximum=maximum,
        )
    if min_x >= max_x or min_y >= max_y:
        raise presentation_error(
            "tile extraction region must be a non-empty half-open rectangle",
            phase="tile_extract",
            details={"field": "region"},
        )
    tile_by_id = {tile.tile_id: tile for tile in tilemap.tiles}
    groups: list[TileDrawGroup] = []
    for layer in tilemap.layers:
        if not layer.visible:
            continue
        instances: list[TileInstance] = []
        for chunk in layer.chunks:
            start_x = max(min_x, chunk.origin_x)
            start_y = max(min_y, chunk.origin_y)
            end_x = min(max_x, chunk.origin_x + chunk.width)
            end_y = min(max_y, chunk.origin_y + chunk.height)
            for y in range(start_y, end_y):
                for x in range(start_x, end_x):
                    tile_id = chunk.tile_at(x, y)
                    if tile_id is None:
                        continue
                    tile = tile_by_id[tile_id]
                    instances.append(
                        TileInstance(
                            x,
                            y,
                            tile.uv_left,
                            tile.uv_top,
                            tile.uv_right,
                            tile.uv_bottom,
                        )
                    )
        if instances:
            instances.sort(key=lambda item: (item.y, item.x))
            groups.append(
                TileDrawGroup(
                    texture,
                    tuple(instances),
                    float(tilemap.tile_width),
                    float(tilemap.tile_height),
                    layer.layer,
                )
            )
    return tuple(groups)
