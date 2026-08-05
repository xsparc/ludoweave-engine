"""Bounded fixed-point particle simulation and sprite extraction."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from ludoweave.presentation._validation import (
    bounded_int,
    finite_float,
    freeze_bounded_exact,
    normalized_uv,
    stable_name,
)
from ludoweave.presentation.errors import presentation_error
from ludoweave.render.contracts import Color
from ludoweave.render.extraction import SpriteExtractionSource
from ludoweave.render.handles import TextureHandle

SUBPIXELS_PER_UNIT = 1024
_SIGNED_64_MIN = -(2**63)
_SIGNED_64_MAX = 2**63 - 1
_MASK_64 = 2**64 - 1
_MAX_PARTICLES = 100_000
_MAX_ADVANCE_TICKS = 10_000
_MAX_PARTICLE_TICK_WORK = 10_000_000
_WHITE = Color(1.0, 1.0, 1.0, 1.0)


@dataclass(frozen=True, slots=True)
class ParticleEmitter:
    """Finite deterministic emitter using integer simulation units."""

    name: str
    seed: int
    capacity: int
    spawn_per_tick: int
    lifetime_ticks: int
    origin_x: int = 0
    origin_y: int = 0
    velocity_x_min: int = 0
    velocity_x_max: int = 0
    velocity_y_min: int = 0
    velocity_y_max: int = 0
    acceleration_x: int = 0
    acceleration_y: int = 0

    def __post_init__(self) -> None:
        stable_name(self.name, phase="particle_emitter")
        bounded_int(
            self.seed,
            phase="particle_emitter",
            field="seed",
            maximum=_MASK_64,
        )
        bounded_int(
            self.capacity,
            phase="particle_emitter",
            field="capacity",
            minimum=1,
            maximum=_MAX_PARTICLES,
        )
        bounded_int(
            self.spawn_per_tick,
            phase="particle_emitter",
            field="spawn_per_tick",
            maximum=self.capacity,
        )
        bounded_int(
            self.lifetime_ticks,
            phase="particle_emitter",
            field="lifetime_ticks",
            minimum=1,
            maximum=2**31 - 1,
        )
        for field in (
            "origin_x",
            "origin_y",
            "velocity_x_min",
            "velocity_x_max",
            "velocity_y_min",
            "velocity_y_max",
            "acceleration_x",
            "acceleration_y",
        ):
            bounded_int(
                getattr(self, field),
                phase="particle_emitter",
                field=field,
                minimum=-(2**31),
                maximum=2**31 - 1,
            )
        if self.velocity_x_min > self.velocity_x_max or self.velocity_y_min > self.velocity_y_max:
            raise presentation_error(
                "particle velocity ranges must have minimum less than or equal to maximum",
                phase="particle_emitter",
                details={"field": "velocity_range"},
            )


@dataclass(frozen=True, slots=True)
class Particle:
    particle_id: int
    age_ticks: int
    lifetime_ticks: int
    previous_x: int
    previous_y: int
    current_x: int
    current_y: int
    velocity_x: int
    velocity_y: int

    def __post_init__(self) -> None:
        bounded_int(self.particle_id, phase="particle", field="particle_id")
        bounded_int(self.age_ticks, phase="particle", field="age_ticks", maximum=2**31 - 1)
        bounded_int(
            self.lifetime_ticks,
            phase="particle",
            field="lifetime_ticks",
            minimum=1,
            maximum=2**31 - 1,
        )
        if self.age_ticks >= self.lifetime_ticks:
            raise presentation_error(
                "live particle age must be less than its lifetime",
                phase="particle",
                details={"field": "age_ticks"},
            )
        for field in (
            "previous_x",
            "previous_y",
            "current_x",
            "current_y",
            "velocity_x",
            "velocity_y",
        ):
            bounded_int(
                getattr(self, field),
                phase="particle",
                field=field,
                minimum=_SIGNED_64_MIN,
                maximum=_SIGNED_64_MAX,
            )


@dataclass(frozen=True, slots=True)
class ParticleState:
    """Immutable state that may be stored canonically only through ECS/world codecs."""

    completed_ticks: int = 0
    next_particle_id: int = 0
    particles: tuple[Particle, ...] = ()

    def __post_init__(self) -> None:
        bounded_int(
            self.completed_ticks,
            phase="particle_state",
            field="completed_ticks",
        )
        bounded_int(
            self.next_particle_id,
            phase="particle_state",
            field="next_particle_id",
        )
        particles = freeze_bounded_exact(
            self.particles,
            Particle,
            maximum=_MAX_PARTICLES,
            phase="particle_state",
            field="particles",
            allow_empty=True,
        )
        ids = tuple(item.particle_id for item in particles)
        if ids != tuple(sorted(ids)) or len(ids) != len(set(ids)):
            raise presentation_error(
                "particle state must use unique ascending particle identities",
                phase="particle_state",
                details={"field": "particles"},
            )
        if ids and (ids[-1] >= self.next_particle_id):
            raise presentation_error(
                "next particle identity must exceed every live identity",
                phase="particle_state",
                details={"field": "next_particle_id"},
            )
        object.__setattr__(self, "particles", particles)


def step_particles(
    emitter: ParticleEmitter,
    state: ParticleState,
    *,
    ticks: int = 1,
) -> ParticleState:
    """Advance exact integer ticks with stable spawn identities and fixed-point motion."""

    if type(emitter) is not ParticleEmitter or type(state) is not ParticleState:
        raise presentation_error(
            "particle stepping requires exact emitter and state records",
            phase="particle_step",
            details={"field": "input"},
        )
    checked_ticks = bounded_int(
        ticks,
        phase="particle_step",
        field="ticks",
        maximum=_MAX_ADVANCE_TICKS,
    )
    if len(state.particles) > emitter.capacity:
        raise presentation_error(
            "particle state exceeds the selected emitter capacity",
            phase="particle_step",
            details={"field": "particles", "capacity": emitter.capacity},
        )
    if checked_ticks * emitter.capacity > _MAX_PARTICLE_TICK_WORK:
        raise presentation_error(
            "particle step exceeds the bounded particle-tick work budget",
            phase="particle_step",
            details={"field": "ticks", "maximum_work": _MAX_PARTICLE_TICK_WORK},
        )
    if any(item.lifetime_ticks != emitter.lifetime_ticks for item in state.particles):
        raise presentation_error(
            "particle state lifetime does not match the selected emitter",
            phase="particle_step",
            details={"field": "lifetime_ticks"},
        )
    current = state
    for _ in range(checked_ticks):
        live: list[Particle] = []
        for particle in current.particles:
            age = particle.age_ticks + 1
            if age >= particle.lifetime_ticks:
                continue
            velocity_x = _checked_motion(particle.velocity_x, emitter.acceleration_x)
            velocity_y = _checked_motion(particle.velocity_y, emitter.acceleration_y)
            x = _checked_motion(particle.current_x, velocity_x)
            y = _checked_motion(particle.current_y, velocity_y)
            live.append(
                Particle(
                    particle.particle_id,
                    age,
                    particle.lifetime_ticks,
                    particle.current_x,
                    particle.current_y,
                    x,
                    y,
                    velocity_x,
                    velocity_y,
                )
            )
        next_id = current.next_particle_id
        spawn_count = min(emitter.spawn_per_tick, emitter.capacity - len(live))
        if next_id + spawn_count > _SIGNED_64_MAX:
            raise presentation_error(
                "particle identity allocation exceeds signed 64-bit bounds",
                phase="particle_step",
                details={"field": "next_particle_id"},
            )
        for _ in range(spawn_count):
            live.append(
                Particle(
                    next_id,
                    0,
                    emitter.lifetime_ticks,
                    emitter.origin_x,
                    emitter.origin_y,
                    emitter.origin_x,
                    emitter.origin_y,
                    _sample_range(
                        emitter.seed,
                        next_id,
                        0,
                        emitter.velocity_x_min,
                        emitter.velocity_x_max,
                    ),
                    _sample_range(
                        emitter.seed,
                        next_id,
                        1,
                        emitter.velocity_y_min,
                        emitter.velocity_y_max,
                    ),
                )
            )
            next_id += 1
        current = ParticleState(current.completed_ticks + 1, next_id, tuple(live))
    return current


def particle_sprites(
    texture: TextureHandle,
    state: ParticleState,
    *,
    base_entity_index: int,
    width: float,
    height: float,
    uv_left: float = 0.0,
    uv_top: float = 0.0,
    uv_right: float = 1.0,
    uv_bottom: float = 1.0,
    tint: Color = _WHITE,
    layer: int = 0,
    z: float = 0.0,
) -> tuple[SpriteExtractionSource, ...]:
    """Translate fixed-point state into interpolated renderer-neutral sprites."""

    if type(state) is not ParticleState:
        raise presentation_error(
            "particle extraction requires an exact state",
            phase="particle_extract",
            details={"field": "state", "actual_type": type(state).__name__},
        )
    if type(texture) is not TextureHandle:
        raise presentation_error(
            "particle extraction requires an exact texture handle",
            phase="particle_extract",
            details={"field": "texture", "actual_type": type(texture).__name__},
        )
    bounded_int(
        base_entity_index,
        phase="particle_extract",
        field="base_entity_index",
    )
    normalized_uv(uv_left, uv_top, uv_right, uv_bottom, phase="particle_extract")
    finite_float(width, phase="particle_extract", field="width", positive=True)
    finite_float(height, phase="particle_extract", field="height", positive=True)
    finite_float(z, phase="particle_extract", field="z")
    bounded_int(layer, phase="particle_extract", field="layer")
    if type(tint) is not Color:
        raise presentation_error(
            "particle extraction tint must be an exact Color",
            phase="particle_extract",
            details={"field": "tint"},
        )
    if state.particles and base_entity_index + state.particles[-1].particle_id > _SIGNED_64_MAX:
        raise presentation_error(
            "particle entity identity range exceeds signed 64-bit bounds",
            phase="particle_extract",
            details={"field": "base_entity_index"},
        )
    scale = float(SUBPIXELS_PER_UNIT)
    return tuple(
        SpriteExtractionSource(
            texture,
            base_entity_index + particle.particle_id,
            0,
            float(particle.previous_x) / scale,
            float(particle.previous_y) / scale,
            float(particle.current_x) / scale,
            float(particle.current_y) / scale,
            0.0,
            0.0,
            width,
            height,
            uv_left,
            uv_top,
            uv_right,
            uv_bottom,
            tint,
            layer,
            z,
        )
        for particle in state.particles
    )


def particle_state_digest(state: ParticleState) -> str:
    """Return a stable SHA-256 digest of detached integer state."""

    if type(state) is not ParticleState:
        raise presentation_error(
            "particle digest requires an exact state",
            phase="particle_digest",
            details={"field": "state", "actual_type": type(state).__name__},
        )
    document = {
        "completed_ticks": state.completed_ticks,
        "next_particle_id": state.next_particle_id,
        "particles": [
            [
                item.particle_id,
                item.age_ticks,
                item.lifetime_ticks,
                item.previous_x,
                item.previous_y,
                item.current_x,
                item.current_y,
                item.velocity_x,
                item.velocity_y,
            ]
            for item in state.particles
        ],
    }
    payload = json.dumps(document, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def _sample_range(seed: int, particle_id: int, channel: int, minimum: int, maximum: int) -> int:
    value = (seed + 0x9E3779B97F4A7C15 * (particle_id * 2 + channel + 1)) & _MASK_64
    value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & _MASK_64
    value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & _MASK_64
    value ^= value >> 31
    return minimum + value % (maximum - minimum + 1)


def _checked_motion(left: int, right: int) -> int:
    result = left + right
    if not _SIGNED_64_MIN <= result <= _SIGNED_64_MAX:
        raise presentation_error(
            "particle fixed-point motion exceeds signed 64-bit bounds",
            phase="particle_step",
            details={"field": "motion"},
        )
    return result
