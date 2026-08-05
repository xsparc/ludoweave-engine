"""Deterministic pure-Python 2D collision contracts and spatial grid."""

from ludoweave.collision.geometry import (
    Aabb,
    Circle,
    Collider,
    CollisionError,
    KinematicResult,
    Shape,
    SpatialGrid,
    Vec2,
    brute_force_overlaps,
    overlaps,
    resolve_kinematic_aabb,
)

__all__ = [
    "Aabb",
    "Circle",
    "Collider",
    "CollisionError",
    "KinematicResult",
    "Shape",
    "SpatialGrid",
    "Vec2",
    "brute_force_overlaps",
    "overlaps",
    "resolve_kinematic_aabb",
]
