"""Small backend-neutral audio interface for owned clip and playback lifetimes."""

from __future__ import annotations

import re
from dataclasses import dataclass
from math import isfinite
from typing import Protocol
from uuid import UUID

from ludoweave.core.errors import LudoWeaveError

_NAME = re.compile(r"[A-Za-z][A-Za-z0-9_.:-]{0,127}\Z")


class AudioError(LudoWeaveError):
    """Raised for audio descriptors, ordering, or backend failures."""


@dataclass(frozen=True, slots=True)
class AudioClipDescriptor:
    """Provider-neutral immutable metadata for one decoded clip."""

    name: str
    duration_seconds: float
    category: str = "effects"

    def __post_init__(self) -> None:
        validate_audio_name(self.name, field="name")
        validate_audio_name(self.category, field="category")
        if (
            type(self.duration_seconds) is not float
            or not isfinite(self.duration_seconds)
            or self.duration_seconds <= 0.0
        ):
            raise audio_error(
                "audio duration must be a positive finite exact float",
                phase="descriptor",
                details={"field": "duration_seconds"},
            )


@dataclass(frozen=True, slots=True)
class AudioClipHandle:
    scope: UUID
    index: int
    generation: int = 0

    def __post_init__(self) -> None:
        _handle(self.scope, self.index, self.generation, kind="clip")


@dataclass(frozen=True, slots=True)
class AudioPlaybackHandle:
    scope: UUID
    index: int
    generation: int = 0

    def __post_init__(self) -> None:
        _handle(self.scope, self.index, self.generation, kind="playback")


class AudioBackend(Protocol):
    """Engine-owned minimal audio adapter; callers close the injected backend."""

    @property
    def name(self) -> str: ...

    def initialize(self) -> None: ...

    def load_clip(self, descriptor: AudioClipDescriptor, data: bytes) -> AudioClipHandle: ...

    def play(
        self,
        clip: AudioClipHandle,
        *,
        volume: float = 1.0,
        loop: bool = False,
    ) -> AudioPlaybackHandle: ...

    def stop(self, playback: AudioPlaybackHandle) -> None: ...

    def set_master_volume(self, volume: float) -> None: ...

    def set_category_volume(self, category: str, volume: float) -> None: ...

    def close(self) -> None: ...


def validate_audio_name(value: object, *, field: str) -> str:
    if type(value) is not str or _NAME.fullmatch(value) is None:
        raise audio_error(
            "audio names must be bounded stable identifiers",
            phase="descriptor",
            details={"field": field, "actual_type": type(value).__name__},
        )
    return value


def validate_volume(value: object, *, phase: str) -> float:
    if type(value) is not float or not isfinite(value) or not 0.0 <= value <= 1.0:
        raise audio_error(
            "audio volume must be a finite exact float between zero and one",
            phase=phase,
            details={"field": "volume", "actual_type": type(value).__name__},
        )
    return value


def _handle(scope: object, index: object, generation: object, *, kind: str) -> None:
    if not isinstance(scope, UUID) or scope.int == 0:
        raise audio_error(
            "audio handle requires a nonzero UUID scope",
            phase="handle",
            details={"kind": kind, "field": "scope"},
        )
    if type(index) is not int or type(generation) is not int or index < 0 or generation < 0:
        raise audio_error(
            "audio handle indices must be non-negative integers",
            phase="handle",
            details={"kind": kind, "field": "index"},
        )


def audio_error(
    message: str,
    *,
    phase: str,
    details: dict[str, str | int | float | bool | None],
    code: str = "audio.invalid_value",
) -> AudioError:
    return AudioError(
        message,
        code=code,
        subsystem="audio",
        phase=phase,
        details=details,
    )
