"""Collision primitive, spatial-grid, and kinematic acceptance tests."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.collision import (
    Aabb,
    Circle,
    Collider,
    SpatialGrid,
    Vec2,
    brute_force_overlaps,
    overlaps,
    resolve_kinematic_aabb,
)


def test_aabb_circle_and_cross_shape_overlap_contract() -> None:
    origin = Aabb(Vec2(0.0, 0.0), 1.0, 1.0)
    assert overlaps(origin, Aabb(Vec2(1.5, 0.0), 1.0, 1.0))
    assert not overlaps(origin, Aabb(Vec2(2.0, 0.0), 1.0, 1.0))
    assert overlaps(Circle(Vec2(0.0, 0.0), 1.0), Circle(Vec2(1.5, 0.0), 1.0))
    assert overlaps(origin, Circle(Vec2(0.5, 0.5), 0.25))
    assert not overlaps(origin, Circle(Vec2(2.0, 0.0), 1.0))


@given(
    query_x=st.integers(-20, 20),
    query_y=st.integers(-20, 20),
    raw=st.lists(
        st.tuples(
            st.integers(-20, 20),
            st.integers(-20, 20),
            st.integers(1, 5),
            st.integers(1, 5),
        ),
        max_size=60,
    ),
)
def test_spatial_grid_matches_brute_force(
    query_x: int,
    query_y: int,
    raw: list[tuple[int, int, int, int]],
) -> None:
    colliders = tuple(
        Collider(
            index,
            Aabb(Vec2(float(x), float(y)), float(width), float(height)),
        )
        for index, (x, y, width, height) in enumerate(raw)
    )
    query = Aabb(Vec2(float(query_x), float(query_y)), 2.0, 2.0)
    grid = SpatialGrid(4.0)
    grid.rebuild(colliders)

    assert grid.query(query) == brute_force_overlaps(query, colliders)


def test_kinematic_resolution_is_axis_ordered_and_stable() -> None:
    moving = Aabb(Vec2(0.0, 0.0), 0.5, 0.5)
    obstacles = (
        Collider(9, Aabb(Vec2(2.0, 0.0), 0.5, 3.0)),
        Collider(3, Aabb(Vec2(1.0, 2.0), 3.0, 0.5)),
    )

    result = resolve_kinematic_aabb(moving, Vec2(3.0, 3.0), obstacles)

    assert result.shape.center == Vec2(1.0, 1.0)
    assert result.applied == Vec2(1.0, 1.0)
    assert result.collided_ids == (3, 9)


@pytest.mark.parametrize("bad", [0.0, -1.0, float("inf"), float("nan")])
def test_collision_dimensions_reject_nonpositive_or_nonfinite_values(bad: float) -> None:
    with pytest.raises(Exception, match="collision"):
        Aabb(Vec2(0.0, 0.0), bad, 1.0)
