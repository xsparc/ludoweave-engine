"""Structured failures for deterministic 2D presentation authoring."""

from __future__ import annotations

from collections.abc import Mapping

from ludoweave.core.errors import ErrorValue, LudoWeaveError


class PresentationError(LudoWeaveError):
    """Raised when presentation data or deterministic sampling is invalid."""


def presentation_error(
    message: str,
    *,
    phase: str,
    details: Mapping[str, ErrorValue],
    code: str = "presentation.invalid_value",
) -> PresentationError:
    return PresentationError(
        message,
        code=code,
        subsystem="presentation",
        phase=phase,
        details=details,
    )
