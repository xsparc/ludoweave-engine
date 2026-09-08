"""Optional, explicitly pumped PCM output; no Python audio callbacks.

The constructing thread owns every operation. ``pump`` performs a blocking
device write and must be called regularly by the presentation loop. It is not
a simulation clock and makes no hard real-time or bounded driver-latency promise.
"""

from array import array
from threading import get_ident
from typing import Protocol, cast

from ludoweave.audio.api import (
    AudioClipDescriptor,
    AudioClipHandle,
    AudioMixGraph,
    AudioPlaybackHandle,
    audio_error,
)
from ludoweave.audio.null import NullAudioBackend

__all__ = ["BlockingAudioBackend"]
__stability__ = {name: "experimental" for name in __all__}

_RATE = 44_100
_MAX_CLIP_BYTES = _RATE * 2 * 10
_MAX_TOTAL_BYTES = 16 * 1024 * 1024


class _Stream(Protocol):
    def start(self) -> None: ...
    def write(self, data: bytes) -> bool: ...
    def abort(self) -> None: ...
    def close(self) -> None: ...


def _open_stream() -> _Stream:
    # The dependency and its native objects are confined to this adapter.
    import sounddevice  # pyright: ignore[reportMissingTypeStubs]

    return cast(
        _Stream,
        sounddevice.RawOutputStream(  # pyright: ignore[reportUnknownMemberType]
            samplerate=_RATE,
            channels=1,
            dtype="int16",
            blocksize=735,
            callback=None,
            finished_callback=None,
        ),
    )


class BlockingAudioBackend:
    """Owned mono 44.1-kHz signed little-endian PCM16 output.

    At most 64 clips, 16 MiB of source PCM, and 16 simultaneous voices are
    admitted. Each clip is at most ten seconds. No resampling or file decoding
    is performed. Natural completion invalidates a playback handle after pump.
    """

    __slots__ = (
        "_clips",
        "_model",
        "_owner",
        "_state",
        "_stream",
        "_total_bytes",
        "_underflows",
        "_voices",
    )

    def __init__(self) -> None:
        self._owner = get_ident()
        self._state = "created"
        self._model = NullAudioBackend()
        self._stream: _Stream | None = None
        self._clips: dict[AudioClipHandle, array[int]] = {}
        self._voices: dict[AudioPlaybackHandle, tuple[AudioClipHandle, int, bool]] = {}
        self._total_bytes = 0
        self._underflows = 0

    @property
    def name(self) -> str:
        return "blocking-audio"

    @property
    def underflow_count(self) -> int:
        """Diagnostic device-write underflows; never canonical world state."""
        return self._underflows

    @property
    def active_playback_count(self) -> int:
        return len(self._voices)

    def _check(self, phase: str, state: str = "ready") -> None:
        if get_ident() != self._owner:
            raise audio_error(
                "audio operations require the owner thread",
                phase=phase,
                details={},
                code="audio.wrong_thread",
            )
        if self._state != state:
            raise audio_error(
                "audio lifecycle transition is invalid",
                phase=phase,
                details={"state": self._state},
                code="audio.invalid_state",
            )

    def initialize(self) -> None:
        self._check("initialize", "created")
        try:
            self._stream = _open_stream()
            self._stream.start()
        except Exception as exc:
            self._state = "failed"
            self._dispose(exc)
            raise audio_error(
                "audio output could not be initialized",
                phase="initialize",
                details={},
                code="audio.provider_failure",
            ) from exc
        self._model.initialize()
        self._state = "ready"

    def configure_mix(self, graph: AudioMixGraph) -> None:
        self._check("configure_mix")
        self._model.configure_mix(graph)

    def load_clip(self, descriptor: AudioClipDescriptor, data: bytes) -> AudioClipHandle:
        self._check("load_clip")
        if (
            type(descriptor) is not AudioClipDescriptor
            or type(data) is not bytes
            or not data
            or len(data) % 2
            or len(data) > _MAX_CLIP_BYTES
        ):
            raise audio_error(
                "clip requires bounded mono PCM16 bytes",
                phase="load_clip",
                details={},
                code="audio.invalid_value",
            )
        if abs(descriptor.duration_seconds * _RATE - len(data) // 2) > 0.5:
            raise audio_error(
                "clip duration does not match PCM sample count",
                phase="load_clip",
                details={},
                code="audio.invalid_value",
            )
        if len(self._clips) >= 64 or self._total_bytes + len(data) > _MAX_TOTAL_BYTES:
            raise audio_error(
                "audio clip capacity is exhausted",
                phase="load_clip",
                details={},
                code="audio.capacity_exceeded",
            )
        samples = array("h")
        samples.frombytes(data)
        import sys

        if sys.byteorder != "little":
            samples.byteswap()
        handle = self._model.load_clip(descriptor, data)
        self._clips[handle] = samples
        self._total_bytes += len(data)
        return handle

    def play(
        self, clip: AudioClipHandle, *, volume: float = 1.0, loop: bool = False
    ) -> AudioPlaybackHandle:
        self._check("play")
        if len(self._voices) >= 16:
            raise audio_error(
                "audio voice capacity is exhausted",
                phase="play",
                details={},
                code="audio.capacity_exceeded",
            )
        playback = self._model.play(clip, volume=volume, loop=loop)
        self._voices[playback] = (clip, 0, loop)
        return playback

    def stop(self, playback: AudioPlaybackHandle) -> None:
        self._check("stop")
        self._model.stop(playback)
        del self._voices[playback]

    def set_master_volume(self, volume: float) -> None:
        self._check("set_master_volume")
        self._model.set_master_volume(volume)

    def set_category_volume(self, category: str, volume: float) -> None:
        self._check("set_category_volume")
        self._model.set_category_volume(category, volume)

    def pump(self, frames: int = 735) -> None:
        """Mix and write 1..4096 frames, including silence when no voice is live.

        The write uses native-endian PCM; clip input is always little-endian.
        Device buffering makes presentation timing nondeterministic. Do not
        derive simulation progress from playback completion or this call's time.
        """
        self._check("pump")
        if type(frames) is not int or not 1 <= frames <= 4096:
            raise audio_error("pump requires 1..4096 frames", phase="pump", details={})
        mixed = [0.0] * frames
        next_voices: dict[AudioPlaybackHandle, tuple[AudioClipHandle, int, bool]] = {}
        for handle, (clip, offset, loop) in self._voices.items():
            samples = self._clips[clip]
            gain = self._model.playback_gain(handle)
            for index in range(frames):
                if offset == len(samples):
                    if not loop:
                        break
                    offset = 0
                mixed[index] += samples[offset] * gain
                offset += 1
            if loop or offset < len(samples):
                next_voices[handle] = (clip, offset, loop)
        output = array("h", (max(-32768, min(32767, round(value))) for value in mixed))
        stream = self._stream
        assert stream is not None
        try:
            underflow = stream.write(output.tobytes())
        except Exception as exc:
            self._state = "failed"
            self._dispose(exc)
            raise audio_error(
                "audio output write failed", phase="pump", details={}, code="audio.provider_failure"
            ) from exc
        self._underflows += int(underflow)
        for handle in self._voices.keys() - next_voices.keys():
            self._model.stop(handle)
        self._voices = next_voices

    def _dispose(self, cause: Exception | None = None) -> None:
        stream, self._stream = self._stream, None
        self._model.close()
        self._voices.clear()
        self._clips.clear()
        self._total_bytes = 0
        if stream is not None:
            try:
                try:
                    stream.abort()
                finally:
                    stream.close()
            except Exception as exc:
                if cause is not None:
                    cause.add_note("audio resource cleanup also failed")
                else:
                    raise audio_error(
                        "audio output cleanup failed",
                        phase="close",
                        details={},
                        code="audio.provider_failure",
                    ) from exc

    def close(self) -> None:
        """Abort buffered output and close once, including after failed initialization."""
        self._check("close", self._state)
        if self._state == "closed":
            return
        self._state = "closed"
        self._dispose()
