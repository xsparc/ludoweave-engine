"""Validation-only audio adapter with no device or provider dependency."""

from __future__ import annotations

from enum import StrEnum
from uuid import UUID, uuid4

from ludoweave.audio.api import (
    AudioBusDescriptor,
    AudioClipDescriptor,
    AudioClipHandle,
    AudioError,
    AudioMixGraph,
    AudioPlaybackHandle,
    audio_error,
    validate_audio_name,
    validate_volume,
)


class _State(StrEnum):
    CREATED = "created"
    READY = "ready"
    CLOSED = "closed"


class NullAudioBackend:
    """Own clip/playback lifetimes while intentionally producing no sound."""

    __slots__ = (
        "_category_volumes",
        "_clips",
        "_master_volume",
        "_mix_graph",
        "_next_clip",
        "_next_playback",
        "_playbacks",
        "_scope",
        "_state",
    )

    def __init__(self, *, scope: UUID | None = None) -> None:
        selected_scope = uuid4() if scope is None else scope
        scope_value: object = selected_scope
        if type(scope_value) is not UUID or scope_value.int == 0:
            raise audio_error(
                "null audio scope must be a nonzero UUID",
                phase="compose",
                details={"field": "scope"},
            )
        self._scope = selected_scope
        self._state = _State.CREATED
        self._clips: dict[AudioClipHandle, AudioClipDescriptor] = {}
        self._playbacks: dict[AudioPlaybackHandle, tuple[AudioClipHandle, float, bool]] = {}
        self._category_volumes: dict[str, float] = {}
        self._master_volume = 1.0
        self._mix_graph = _default_mix_graph()
        self._next_clip = 0
        self._next_playback = 0

    @property
    def name(self) -> str:
        return "null-audio"

    @property
    def master_volume(self) -> float:
        return self._master_volume

    @property
    def active_playback_count(self) -> int:
        return len(self._playbacks)

    @property
    def clip_count(self) -> int:
        return len(self._clips)

    def initialize(self) -> None:
        if self._state is not _State.CREATED:
            raise _state_error("initialize", self._state)
        self._state = _State.READY

    def configure_mix(self, graph: AudioMixGraph) -> None:
        self._ready("configure_mix")
        if type(graph) is not AudioMixGraph:
            raise audio_error(
                "null audio requires an exact mix graph",
                phase="configure_mix",
                details={"actual_type": type(graph).__name__},
            )
        if self._clips or self._playbacks:
            raise audio_error(
                "audio mix graph must be configured before clips or playbacks exist",
                phase="configure_mix",
                details={"clip_count": len(self._clips), "playback_count": len(self._playbacks)},
                code="audio.invalid_state",
            )
        self._mix_graph = graph
        self._category_volumes.clear()

    def load_clip(self, descriptor: AudioClipDescriptor, data: bytes) -> AudioClipHandle:
        self._ready("load_clip")
        if type(descriptor) is not AudioClipDescriptor:
            raise audio_error(
                "null audio requires an exact clip descriptor",
                phase="load",
                details={"actual_type": type(descriptor).__name__},
            )
        if type(data) is not bytes or not data:
            raise audio_error(
                "audio clip data must be non-empty immutable bytes",
                phase="load",
                details={"actual_type": type(data).__name__},
            )
        self._mix_graph.gain_for(descriptor.category)
        handle = AudioClipHandle(self._scope, self._next_clip)
        self._next_clip += 1
        self._clips[handle] = descriptor
        return handle

    def play(
        self,
        clip: AudioClipHandle,
        *,
        volume: float = 1.0,
        loop: bool = False,
    ) -> AudioPlaybackHandle:
        self._ready("play")
        checked_volume = validate_volume(volume, phase="play")
        if type(loop) is not bool:
            raise audio_error(
                "audio loop state must be an exact boolean",
                phase="play",
                details={"actual_type": type(loop).__name__},
            )
        if (
            type(clip) is not AudioClipHandle
            or clip.scope != self._scope
            or clip not in self._clips
        ):
            raise audio_error(
                "audio clip handle is not live in this backend",
                phase="play",
                details={"field": "clip"},
                code="audio.invalid_handle",
            )
        handle = AudioPlaybackHandle(self._scope, self._next_playback)
        self._next_playback += 1
        self._playbacks[handle] = (clip, checked_volume, loop)
        return handle

    def stop(self, playback: AudioPlaybackHandle) -> None:
        self._ready("stop")
        if (
            type(playback) is not AudioPlaybackHandle
            or playback.scope != self._scope
            or playback not in self._playbacks
        ):
            raise audio_error(
                "audio playback handle is not active in this backend",
                phase="stop",
                details={"field": "playback"},
                code="audio.invalid_handle",
            )
        del self._playbacks[playback]

    def set_master_volume(self, volume: float) -> None:
        self._ready("set_master_volume")
        self._master_volume = validate_volume(volume, phase="volume")

    def set_category_volume(self, category: str, volume: float) -> None:
        self._ready("set_category_volume")
        checked_category = validate_audio_name(category, field="category")
        self._mix_graph.gain_for(checked_category)
        self._category_volumes[checked_category] = validate_volume(volume, phase="volume")

    def category_volume(self, category: str) -> float:
        checked_category = validate_audio_name(category, field="category")
        self._mix_graph.gain_for(checked_category)
        return self._category_volumes.get(checked_category, 1.0)

    def playback_gain(self, playback: AudioPlaybackHandle) -> float:
        """Return the current deterministic effective gain for a live playback."""

        self._ready("playback_gain")
        if type(playback) is not AudioPlaybackHandle or playback.scope != self._scope:
            raise audio_error(
                "audio playback handle is not active in this backend",
                phase="playback_gain",
                details={"field": "playback"},
                code="audio.invalid_handle",
            )
        record = self._playbacks.get(playback)
        if record is None:
            raise audio_error(
                "audio playback handle is not active in this backend",
                phase="playback_gain",
                details={"field": "playback"},
                code="audio.invalid_handle",
            )
        clip, volume, _loop = record
        category = self._clips[clip].category
        runtime_bus_gain = 1.0
        for bus in self._mix_graph.lineage_for(category):
            runtime_bus_gain *= self._category_volumes.get(bus, 1.0)
        return self._master_volume * self._mix_graph.gain_for(category) * runtime_bus_gain * volume

    def close(self) -> None:
        if self._state is _State.CLOSED:
            return
        self._playbacks.clear()
        self._clips.clear()
        self._state = _State.CLOSED

    def _ready(self, operation: str) -> None:
        if self._state is not _State.READY:
            raise _state_error(operation, self._state)


def _state_error(operation: str, state: _State) -> AudioError:
    return audio_error(
        "audio operation is invalid in the current lifecycle state",
        phase=operation,
        details={"operation": operation, "state": state.value},
        code="audio.invalid_state",
    )


def _default_mix_graph() -> AudioMixGraph:
    return AudioMixGraph(
        (
            AudioBusDescriptor("master", None),
            AudioBusDescriptor("effects", "master"),
            AudioBusDescriptor("music", "master"),
        )
    )
