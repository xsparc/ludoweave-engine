"""Deterministic overlap tests, spatial hashing, and kinematic resolution."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from math import floor, isfinite

from ludoweave.core.errors import LudoWeaveError

_MAX_GRID_CELLS_PER_SHAPE = 1_000_000


class CollisionError(LudoWeaveError):
    """Raised when collision values exceed the deterministic contract."""


@dataclass(frozen=True, slots=True)
class Vec2:
    x: float
    y: float

    def __post_init__(self) -> None:
        _finite(self.x, field="x")
        _finite(self.y, field="y")


@dataclass(frozen=True, slots=True)
class Aabb:
    """Axis-aligned box represented by center and positive half-extents."""

    center: Vec2
    half_width: float
    half_height: float

    def __post_init__(self) -> None:
        if type(self.center) is not Vec2:
            raise _collision_error("AABB center must be an exact Vec2", field="center")
        _positive(self.half_width, field="half_width")
        _positive(self.half_height, field="half_height")

    @property
    def bounds(self) -> tuple[float, float, float, float]:
        return (
            self.center.x - self.half_width,
            self.center.y - self.half_height,
            self.center.x + self.half_width,
            self.center.y + self.half_height,
        )

    def moved(self, displacement: Vec2) -> Aabb:
        if type(displacement) is not Vec2:
            raise _collision_error("AABB displacement must be an exact Vec2", field="displacement")
        return Aabb(
            Vec2(self.center.x + displacement.x, self.center.y + displacement.y),
            self.half_width,
            self.half_height,
        )


@dataclass(frozen=True, slots=True)
class Circle:
    center: Vec2
    radius: float

    def __post_init__(self) -> None:
        if type(self.center) is not Vec2:
            raise _collision_error("circle center must be an exact Vec2", field="center")
        _positive(self.radius, field="radius")

    @property
    def bounds(self) -> tuple[float, float, float, float]:
        return (
            self.center.x - self.radius,
            self.center.y - self.radius,
            self.center.x + self.radius,
            self.center.y + self.radius,
        )


type Shape = Aabb | Circle


@dataclass(frozen=True, slots=True)
class Collider:
    collider_id: int
    shape: Shape

    def __post_init__(self) -> None:
        if type(self.collider_id) is not int or self.collider_id < 0:
            raise _collision_error(
                "collider ID must be a non-negative integer", field="collider_id"
            )
        if type(self.shape) not in (Aabb, Circle):
            raise _collision_error("collider shape must be an Aabb or Circle", field="shape")


def overlaps(left: Shape, right: Shape) -> bool:
    """Return strict-area overlap; edge touching alone is not overlap."""

    if type(left) is Aabb and type(right) is Aabb:
        return (
            abs(left.center.x - right.center.x) < left.half_width + right.half_width
            and abs(left.center.y - right.center.y) < left.half_height + right.half_height
        )
    if type(left) is Circle and type(right) is Circle:
        dx = left.center.x - right.center.x
        dy = left.center.y - right.center.y
        radii = left.radius + right.radius
        return dx * dx + dy * dy < radii * radii
    if type(left) is Circle and type(right) is Aabb:
        return _circle_aabb(left, right)
    if type(left) is Aabb and type(right) is Circle:
        return _circle_aabb(right, left)
    raise _collision_error("overlap requires exact supported shapes", field="shape")


def brute_force_overlaps(shape: Shape, colliders: Iterable[Collider]) -> tuple[int, ...]:
    """Reference candidate scan used to validate spatial-grid results."""

    _require_shape(shape)
    values = _colliders(colliders)
    return tuple(item.collider_id for item in values if overlaps(shape, item.shape))


class SpatialGrid:
    """Deterministic broad phase with exact overlap filtering and sorted output."""

    __slots__ = ("_by_cell", "_by_id", "_cell_size")

    def __init__(self, cell_size: float) -> None:
        _positive(cell_size, field="cell_size")
        self._cell_size = cell_size
        self._by_cell: dict[tuple[int, int], tuple[int, ...]] = {}
        self._by_id: dict[int, Shape] = {}

    @property
    def cell_size(self) -> float:
        return self._cell_size

    def rebuild(self, colliders: Iterable[Collider]) -> None:
        """Atomically replace the index from a copied collider sequence."""

        values = _colliders(colliders)
        by_id = {item.collider_id: item.shape for item in values}
        if len(by_id) != len(values):
            raise _collision_error("spatial grid repeats a collider ID", field="collider_id")
        mutable: dict[tuple[int, int], list[int]] = {}
        for item in values:
            for cell in self._cells(item.shape):
                mutable.setdefault(cell, []).append(item.collider_id)
        self._by_id = by_id
        self._by_cell = {cell: tuple(sorted(ids)) for cell, ids in sorted(mutable.items())}

    def query(self, shape: Shape) -> tuple[int, ...]:
        """Return sorted collider IDs that exactly overlap ``shape``."""

        _require_shape(shape)
        candidates: set[int] = set()
        for cell in self._cells(shape):
            candidates.update(self._by_cell.get(cell, ()))
        return tuple(
            collider_id
            for collider_id in sorted(candidates)
            if overlaps(shape, self._by_id[collider_id])
        )

    def _cells(self, shape: Shape) -> tuple[tuple[int, int], ...]:
        minimum_x, minimum_y, maximum_x, maximum_y = shape.bounds
        left = floor(minimum_x / self._cell_size)
        bottom = floor(minimum_y / self._cell_size)
        right = floor(maximum_x / self._cell_size)
        top = floor(maximum_y / self._cell_size)
        count = (right - left + 1) * (top - bottom + 1)
        if count > _MAX_GRID_CELLS_PER_SHAPE:
            raise _collision_error(
                "shape covers too many spatial-grid cells", field="shape", count=count
            )
        return tuple((x, y) for x in range(left, right + 1) for y in range(bottom, top + 1))


@dataclass(frozen=True, slots=True)
class KinematicResult:
    shape: Aabb
    applied: Vec2
    collided_ids: tuple[int, ...]


def resolve_kinematic_aabb(
    moving: Aabb,
    displacement: Vec2,
    obstacles: Iterable[Collider],
) -> KinematicResult:
    """Resolve X then Y against sorted static AABBs, clamping at first contact.

    This deliberately simple policy is deterministic and suitable for the M4
    arena. It does not provide continuous collision detection or rigid-body
    response.
    """

    if type(moving) is not Aabb or type(displacement) is not Vec2:
        raise _collision_error("kinematic resolution requires Aabb and Vec2", field="shape")
    walls = tuple(item for item in _colliders(obstacles) if type(item.shape) is Aabb)
    current = moving
    collided: set[int] = set()
    applied_x = displacement.x
    if displacement.x != 0.0:
        candidate = current.moved(Vec2(displacement.x, 0.0))
        for wall in walls:
            assert type(wall.shape) is Aabb
            current_left, current_bottom, current_right, current_top = current.bounds
            wall_left, wall_bottom, wall_right, wall_top = wall.shape.bounds
            vertical_overlap = current_bottom < wall_top and current_top > wall_bottom
            crossed = vertical_overlap and (
                (
                    displacement.x > 0.0
                    and current_right <= wall_left
                    and candidate.bounds[2] > wall_left
                )
                or (
                    displacement.x < 0.0
                    and current_left >= wall_right
                    and candidate.bounds[0] < wall_right
                )
            )
            if crossed or overlaps(candidate, wall.shape):
                collided.add(wall.collider_id)
                if displacement.x > 0.0:
                    applied_x = min(
                        applied_x,
                        wall.shape.center.x
                        - wall.shape.half_width
                        - current.center.x
                        - current.half_width,
                    )
                else:
                    applied_x = max(
                        applied_x,
                        wall.shape.center.x
                        + wall.shape.half_width
                        - current.center.x
                        + current.half_width,
                    )
                candidate = current.moved(Vec2(applied_x, 0.0))
        current = candidate
    applied_y = displacement.y
    if displacement.y != 0.0:
        candidate = current.moved(Vec2(0.0, displacement.y))
        for wall in walls:
            assert type(wall.shape) is Aabb
            current_left, current_bottom, current_right, current_top = current.bounds
            wall_left, wall_bottom, wall_right, wall_top = wall.shape.bounds
            horizontal_overlap = current_left < wall_right and current_right > wall_left
            crossed = horizontal_overlap and (
                (
                    displacement.y > 0.0
                    and current_top <= wall_bottom
                    and candidate.bounds[3] > wall_bottom
                )
                or (
                    displacement.y < 0.0
                    and current_bottom >= wall_top
                    and candidate.bounds[1] < wall_top
                )
            )
            if crossed or overlaps(candidate, wall.shape):
                collided.add(wall.collider_id)
                if displacement.y > 0.0:
                    applied_y = min(
                        applied_y,
                        wall.shape.center.y
                        - wall.shape.half_height
                        - current.center.y
                        - current.half_height,
                    )
                else:
                    applied_y = max(
                        applied_y,
                        wall.shape.center.y
                        + wall.shape.half_height
                        - current.center.y
                        + current.half_height,
                    )
                candidate = current.moved(Vec2(0.0, applied_y))
        current = candidate
    return KinematicResult(current, Vec2(applied_x, applied_y), tuple(sorted(collided)))


def _circle_aabb(circle: Circle, box: Aabb) -> bool:
    minimum_x, minimum_y, maximum_x, maximum_y = box.bounds
    closest_x = min(maximum_x, max(minimum_x, circle.center.x))
    closest_y = min(maximum_y, max(minimum_y, circle.center.y))
    dx = circle.center.x - closest_x
    dy = circle.center.y - closest_y
    return dx * dx + dy * dy < circle.radius * circle.radius


def _colliders(values: Iterable[Collider]) -> tuple[Collider, ...]:
    try:
        checked = tuple(values)
    except Exception as error:
        raise _collision_error(
            "colliders could not be materialized",
            field="colliders",
            cause_type=type(error).__name__,
        ) from error
    if any(type(item) is not Collider for item in checked):
        raise _collision_error("colliders must be exact Collider values", field="colliders")
    return tuple(sorted(checked, key=lambda item: item.collider_id))


def _require_shape(value: object) -> Shape:
    if type(value) not in (Aabb, Circle):
        raise _collision_error("value must be an exact supported shape", field="shape")
    assert isinstance(value, (Aabb, Circle))
    return value


def _finite(value: object, *, field: str) -> float:
    if type(value) is not float or not isfinite(value):
        raise _collision_error("collision values must be finite exact floats", field=field)
    return value


def _positive(value: object, *, field: str) -> float:
    checked = _finite(value, field=field)
    if checked <= 0.0:
        raise _collision_error("collision dimensions must be positive", field=field)
    return checked


def _collision_error(
    message: str,
    *,
    field: str,
    count: int | None = None,
    cause_type: str | None = None,
) -> CollisionError:
    details: dict[str, str | int | None] = {"field": field}
    if count is not None:
        details["count"] = count
    if cause_type is not None:
        details["cause_type"] = cause_type
    return CollisionError(
        message,
        code="collision.invalid_value",
        subsystem="collision",
        phase="validate",
        details=details,
    )
