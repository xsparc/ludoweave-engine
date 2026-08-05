"""Shared exact-value validation for presentation modules."""

from __future__ import annotations

import re
from collections.abc import Iterable
from itertools import islice
from math import isfinite
from typing import cast

from ludoweave.presentation.errors import presentation_error

_NAME = re.compile(r"[A-Za-z][A-Za-z0-9_.:-]{0,127}\Z")
_MAX_SIGNED_64 = 2**63 - 1


def stable_name(value: object, *, phase: str, field: str = "name") -> str:
    if type(value) is not str or _NAME.fullmatch(value) is None:
        raise presentation_error(
            "presentation names must be bounded stable identifiers",
            phase=phase,
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def bounded_int(
    value: object,
    *,
    phase: str,
    field: str,
    minimum: int = 0,
    maximum: int = _MAX_SIGNED_64,
) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        raise presentation_error(
            "presentation integer is outside its declared bounds",
            phase=phase,
            details={"field": field, "minimum": minimum, "maximum": maximum},
        )
    return value


def finite_float(
    value: object,
    *,
    phase: str,
    field: str,
    positive: bool = False,
) -> float:
    if type(value) is not float or not isfinite(value) or (positive and value <= 0.0):
        raise presentation_error(
            "presentation value must be an exact finite float",
            phase=phase,
            details={"field": field, "positive": positive},
        )
    return value


def normalized_uv(
    left: object,
    top: object,
    right: object,
    bottom: object,
    *,
    phase: str,
) -> tuple[float, float, float, float]:
    checked_left = finite_float(left, phase=phase, field="uv_left")
    checked_top = finite_float(top, phase=phase, field="uv_top")
    checked_right = finite_float(right, phase=phase, field="uv_right")
    checked_bottom = finite_float(bottom, phase=phase, field="uv_bottom")
    if not (
        0.0 <= checked_left < checked_right <= 1.0 and 0.0 <= checked_top < checked_bottom <= 1.0
    ):
        raise presentation_error(
            "presentation UV rectangle must be normalized and non-empty",
            phase=phase,
            details={"field": "uv"},
        )
    return checked_left, checked_top, checked_right, checked_bottom


def freeze_bounded(
    values: object,
    *,
    maximum: int,
    phase: str,
    field: str,
    allow_empty: bool = False,
) -> tuple[object, ...]:
    """Freeze at most ``maximum + 1`` items before rejecting oversized input."""

    try:
        iterator = iter(cast(Iterable[object], values))
        frozen = tuple(islice(iterator, maximum + 1))
    except Exception as error:
        raise presentation_error(
            "presentation sequence could not be bounded and frozen",
            phase=phase,
            details={"field": field, "actual_type": type(values).__name__},
        ) from error
    if len(frozen) > maximum or (not allow_empty and not frozen):
        raise presentation_error(
            "presentation sequence is outside its declared item bound",
            phase=phase,
            details={"field": field, "maximum": maximum},
        )
    return frozen


def freeze_bounded_exact[T](
    values: object,
    expected: type[T],
    *,
    maximum: int,
    phase: str,
    field: str,
    allow_empty: bool = False,
) -> tuple[T, ...]:
    frozen = freeze_bounded(
        values,
        maximum=maximum,
        phase=phase,
        field=field,
        allow_empty=allow_empty,
    )
    if any(type(item) is not expected for item in frozen):
        raise presentation_error(
            "presentation sequence requires exact item records",
            phase=phase,
            details={"field": field, "expected": expected.__name__},
        )
    return cast(tuple[T, ...], frozen)
