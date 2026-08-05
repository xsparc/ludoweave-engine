"""Tick-indexed sprite animation with no wall-clock or backend state."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ludoweave.presentation._validation import (
    bounded_int,
    freeze_bounded_exact,
    normalized_uv,
    stable_name,
)
from ludoweave.presentation.errors import presentation_error
from ludoweave.render.contracts import Color
from ludoweave.render.extraction import SpriteExtractionSource
from ludoweave.render.handles import TextureHandle

_MAX_FRAMES = 4096
_WHITE = Color(1.0, 1.0, 1.0, 1.0)


class PlaybackMode(StrEnum):
    """Finite deterministic playback policies."""

    ONCE = "once"
    LOOP = "loop"
    PING_PONG = "ping_pong"


@dataclass(frozen=True, slots=True)
class SpriteAnimationFrame:
    """One atlas region retained for an exact positive number of ticks."""

    duration_ticks: int
    uv_left: float
    uv_top: float
    uv_right: float
    uv_bottom: float

    def __post_init__(self) -> None:
        bounded_int(
            self.duration_ticks,
            phase="animation_frame",
            field="duration_ticks",
            minimum=1,
            maximum=2**31 - 1,
        )
        normalized_uv(
            self.uv_left,
            self.uv_top,
            self.uv_right,
            self.uv_bottom,
            phase="animation_frame",
        )


@dataclass(frozen=True, slots=True)
class SpriteAnimationClip:
    """Immutable tick timeline suitable for ECS-owned elapsed-tick state."""

    name: str
    frames: tuple[SpriteAnimationFrame, ...]
    mode: PlaybackMode = PlaybackMode.LOOP

    def __post_init__(self) -> None:
        stable_name(self.name, phase="animation_clip")
        frames = freeze_bounded_exact(
            self.frames,
            SpriteAnimationFrame,
            maximum=_MAX_FRAMES,
            phase="animation_clip",
            field="frames",
        )
        if type(self.mode) is not PlaybackMode:
            raise presentation_error(
                "animation playback mode must be an exact PlaybackMode",
                phase="animation_clip",
                details={"field": "mode", "actual_type": type(self.mode).__name__},
            )
        object.__setattr__(self, "frames", frames)

    @property
    def cycle_ticks(self) -> int:
        indices = _cycle_indices(self)
        return sum(self.frames[index].duration_ticks for index in indices)


@dataclass(frozen=True, slots=True)
class AnimationSample:
    """Detached result for one exact elapsed-tick value."""

    frame_index: int
    frame: SpriteAnimationFrame
    frame_tick: int
    completed_cycles: int
    finished: bool

    def __post_init__(self) -> None:
        bounded_int(self.frame_index, phase="animation_sample", field="frame_index")
        if type(self.frame) is not SpriteAnimationFrame:
            raise presentation_error(
                "animation sample requires an exact frame",
                phase="animation_sample",
                details={"field": "frame"},
            )
        bounded_int(
            self.frame_tick,
            phase="animation_sample",
            field="frame_tick",
            maximum=self.frame.duration_ticks - 1,
        )
        bounded_int(
            self.completed_cycles,
            phase="animation_sample",
            field="completed_cycles",
        )
        if type(self.finished) is not bool:
            raise presentation_error(
                "animation completion state must be an exact boolean",
                phase="animation_sample",
                details={"field": "finished"},
            )


def sample_animation(clip: SpriteAnimationClip, elapsed_ticks: int) -> AnimationSample:
    """Sample without mutable player state or accumulated fractional time."""

    if type(clip) is not SpriteAnimationClip:
        raise presentation_error(
            "animation sampling requires an exact clip",
            phase="animation_sample",
            details={"field": "clip", "actual_type": type(clip).__name__},
        )
    checked_elapsed = bounded_int(
        elapsed_ticks,
        phase="animation_sample",
        field="elapsed_ticks",
    )
    indices = _cycle_indices(clip)
    cycle_ticks = sum(clip.frames[index].duration_ticks for index in indices)
    if clip.mode is PlaybackMode.ONCE:
        finished = checked_elapsed >= cycle_ticks
        cycle_tick = min(checked_elapsed, cycle_ticks - 1)
        completed_cycles = int(finished)
    else:
        finished = False
        completed_cycles, cycle_tick = divmod(checked_elapsed, cycle_ticks)

    cursor = 0
    for frame_index in indices:
        frame = clip.frames[frame_index]
        end = cursor + frame.duration_ticks
        if cycle_tick < end:
            return AnimationSample(
                frame_index,
                frame,
                cycle_tick - cursor,
                completed_cycles,
                finished,
            )
        cursor = end
    raise AssertionError("validated animation cycle must contain one sampled frame")


def animation_sprite(
    texture: TextureHandle,
    sample: AnimationSample,
    *,
    entity_index: int,
    entity_generation: int = 0,
    previous_x: float,
    previous_y: float,
    current_x: float,
    current_y: float,
    width: float,
    height: float,
    previous_rotation: float = 0.0,
    current_rotation: float = 0.0,
    tint: Color = _WHITE,
    layer: int = 0,
    z: float = 0.0,
) -> SpriteExtractionSource:
    """Translate a sample into the existing backend-neutral sprite boundary."""

    if type(sample) is not AnimationSample:
        raise presentation_error(
            "animation extraction requires an exact sample",
            phase="animation_extract",
            details={"field": "sample", "actual_type": type(sample).__name__},
        )
    frame = sample.frame
    return SpriteExtractionSource(
        texture,
        entity_index,
        entity_generation,
        previous_x,
        previous_y,
        current_x,
        current_y,
        previous_rotation,
        current_rotation,
        width,
        height,
        frame.uv_left,
        frame.uv_top,
        frame.uv_right,
        frame.uv_bottom,
        tint,
        layer,
        z,
    )


def _cycle_indices(clip: SpriteAnimationClip) -> tuple[int, ...]:
    forward = tuple(range(len(clip.frames)))
    if clip.mode is PlaybackMode.PING_PONG and len(forward) > 1:
        return forward + tuple(reversed(forward[1:-1]))
    return forward
