"""Small backend-neutral audio interface for owned clip and playback lifetimes."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import islice
from math import isfinite
from typing import Protocol, cast
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
class AudioBusDescriptor:
    """One provider-neutral mix bus and its immutable authored gain."""

    name: str
    parent: str | None
    volume: float = 1.0

    def __post_init__(self) -> None:
        validate_audio_name(self.name, field="name")
        if self.parent is not None:
            validate_audio_name(self.parent, field="parent")
        validate_volume(self.volume, phase="mix_graph")


@dataclass(frozen=True, slots=True)
class AudioMixGraph:
    """Bounded acyclic bus graph rooted at the required ``master`` bus."""

    buses: tuple[AudioBusDescriptor, ...]

    def __post_init__(self) -> None:
        try:
            buses = tuple(islice(iter(cast(Iterable[object], self.buses)), 65))
        except Exception as error:
            raise audio_error(
                "audio mix graph bus sequence could not be bounded and frozen",
                phase="mix_graph",
                details={"field": "buses", "actual_type": type(self.buses).__name__},
            ) from error
        if (
            not buses
            or len(buses) > 64
            or any(type(bus) is not AudioBusDescriptor for bus in buses)
        ):
            raise audio_error(
                "audio mix graph requires one to 64 exact bus descriptors",
                phase="mix_graph",
                details={"field": "buses", "maximum": 64},
            )
        checked_buses = cast(tuple[AudioBusDescriptor, ...], buses)
        by_name = {bus.name: bus for bus in checked_buses}
        if len(by_name) != len(buses):
            raise audio_error(
                "audio mix bus names must be unique",
                phase="mix_graph",
                details={"field": "buses"},
            )
        master = by_name.get("master")
        if master is None or master.parent is not None:
            raise audio_error(
                "audio mix graph requires a parentless master bus",
                phase="mix_graph",
                details={"field": "master"},
            )
        for bus in checked_buses:
            if bus.name != "master" and bus.parent is None:
                raise audio_error(
                    "every non-master audio bus requires a parent",
                    phase="mix_graph",
                    details={"field": "parent", "bus": bus.name},
                )
            if bus.parent is not None and bus.parent not in by_name:
                raise audio_error(
                    "audio bus parent must identify a declared bus",
                    phase="mix_graph",
                    details={"field": "parent", "bus": bus.name},
                )
            _validate_bus_path(bus.name, by_name)
        object.__setattr__(
            self,
            "buses",
            tuple(sorted(checked_buses, key=lambda bus: bus.name)),
        )

    def gain_for(self, name: str) -> float:
        """Resolve immutable authored gain through the parent chain."""

        by_name = {bus.name: bus for bus in self.buses}
        return _product(by_name[item].volume for item in self.lineage_for(name))

    def lineage_for(self, name: str) -> tuple[str, ...]:
        """Return the declared root-to-selected bus path."""

        checked_name = validate_audio_name(name, field="name")
        by_name = {bus.name: bus for bus in self.buses}
        current = by_name.get(checked_name)
        if current is None:
            raise audio_error(
                "audio bus is not declared by the active mix graph",
                phase="mix_graph",
                details={"field": "name", "bus": checked_name},
                code="audio.invalid_bus",
            )
        reverse_path: list[str] = []
        while current is not None:
            reverse_path.append(current.name)
            current = None if current.parent is None else by_name[current.parent]
        return tuple(reversed(reverse_path))


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

    def configure_mix(self, graph: AudioMixGraph) -> None: ...

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


def _validate_bus_path(
    start: str,
    buses: dict[str, AudioBusDescriptor],
) -> None:
    seen: set[str] = set()
    current: str | None = start
    while current is not None:
        if current in seen:
            raise audio_error(
                "audio mix graph must be acyclic",
                phase="mix_graph",
                details={"field": "parent", "bus": start},
            )
        seen.add(current)
        current = buses[current].parent


def _product(values: Iterable[float]) -> float:
    result = 1.0
    for value in values:
        result *= value
    return result
