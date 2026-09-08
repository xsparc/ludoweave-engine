"""Deterministic PCM and ownership regressions without an audio device."""

from array import array
from concurrent.futures import ThreadPoolExecutor

import pytest

from ludoweave.audio import AudioClipDescriptor, AudioError
from ludoweave.audio import sounddevice as adapter


class FakeStream:
    def __init__(self) -> None:
        self.blocks: list[bytes] = []
        self.calls: list[str] = []
        self.failure: str | None = None

    def start(self) -> None:
        self.calls.append("start")
        if self.failure == "start":
            raise RuntimeError("synthetic start")

    def write(self, data: bytes) -> bool:
        if self.failure == "write":
            raise RuntimeError("synthetic write")
        self.blocks.append(data)
        return False

    def abort(self) -> None:
        self.calls.append("abort")
        if self.failure == "abort":
            raise RuntimeError("synthetic abort")

    def close(self) -> None:
        self.calls.append("close")


@pytest.fixture
def output(monkeypatch: pytest.MonkeyPatch) -> FakeStream:
    stream = FakeStream()
    monkeypatch.setattr(adapter, "_open_stream", lambda: stream)
    return stream


def _clip(audio: adapter.BlockingAudioBackend, sample: int = 1000) -> adapter.AudioClipHandle:
    return audio.load_clip(
        AudioClipDescriptor("tone", 2 / 44100), sample.to_bytes(2, "little", signed=True) * 2
    )


def test_mix_loop_gain_completion_and_close(output: FakeStream) -> None:
    audio = adapter.BlockingAudioBackend()
    audio.initialize()
    clip = _clip(audio)
    audio.set_master_volume(0.5)
    audio.set_category_volume("effects", 0.5)
    audio.play(clip, volume=0.5)
    looping = audio.play(clip, loop=True)
    audio.pump(3)
    samples = array("h")
    samples.frombytes(output.blocks[0])
    assert list(samples) == [375, 375, 250]
    assert audio.active_playback_count == 1
    audio.stop(looping)
    audio.pump(1)
    assert output.blocks[-1] == b"\0\0"
    audio.close()
    audio.close()
    assert output.calls == ["start", "abort", "close"]


@pytest.mark.parametrize("phase", ["start", "write", "abort"])
def test_provider_failure_closes_owned_stream(output: FakeStream, phase: str) -> None:
    audio = adapter.BlockingAudioBackend()
    output.failure = phase
    with pytest.raises(AudioError) as error:
        audio.initialize()
        audio.pump(1)
        audio.close()
    assert error.value.code == "audio.provider_failure"
    assert isinstance(error.value.__cause__, RuntimeError)
    audio.close()
    assert output.calls.count("close") == 1


@pytest.mark.parametrize("frames", [0, -1, 4097, True])
def test_invalid_pump_has_no_write(output: FakeStream, frames: int) -> None:
    audio = adapter.BlockingAudioBackend()
    audio.initialize()
    with pytest.raises(AudioError):
        audio.pump(frames)
    assert not output.blocks
    audio.close()


@pytest.mark.parametrize(
    "data", [b"", b"x", b"xxxxxx", b"x" * 882002], ids=["empty", "odd", "duration", "oversized"]
)
def test_pcm_shape_and_duration(output: FakeStream, data: bytes) -> None:
    audio = adapter.BlockingAudioBackend()
    audio.initialize()
    with pytest.raises(AudioError):
        audio.load_clip(AudioClipDescriptor("tone", 2 / 44100), data)
    audio.close()


def test_capacities_and_saturating_mix(output: FakeStream) -> None:
    audio = adapter.BlockingAudioBackend()
    audio.initialize()
    clip = _clip(audio, 32000)
    for _ in range(16):
        audio.play(clip)
    with pytest.raises(AudioError, match="capacity"):
        audio.play(clip)
    audio.pump(2)
    values = array("h")
    values.frombytes(output.blocks[0])
    assert list(values) == [32767, 32767]
    assert audio.active_playback_count == 0
    for _ in range(63):
        _clip(audio)
    with pytest.raises(AudioError, match="capacity"):
        _clip(audio)
    audio.close()


def test_lifecycle_and_foreign_handles(output: FakeStream) -> None:
    audio = adapter.BlockingAudioBackend()
    with pytest.raises(AudioError):
        audio.pump()
    audio.initialize()
    with pytest.raises(AudioError):
        audio.initialize()
    other = adapter.BlockingAudioBackend()
    other.initialize()
    with pytest.raises(AudioError):
        audio.play(_clip(other))
    with ThreadPoolExecutor(max_workers=1) as pool, pytest.raises(AudioError) as error:
        pool.submit(audio.close).result()
    assert error.value.code == "audio.wrong_thread"
    other.close()
    audio.close()
    with pytest.raises(AudioError):
        audio.pump()


def test_missing_provider_is_structured(monkeypatch: pytest.MonkeyPatch) -> None:
    def missing() -> FakeStream:
        raise ImportError("synthetic missing provider")

    monkeypatch.setattr(adapter, "_open_stream", missing)
    audio = adapter.BlockingAudioBackend()
    with pytest.raises(AudioError) as error:
        audio.initialize()
    assert isinstance(error.value.__cause__, ImportError)
    audio.close()


def test_aggregate_pcm_capacity(output: FakeStream) -> None:
    audio = adapter.BlockingAudioBackend()
    audio.initialize()
    pcm = bytes(882000)
    for _ in range(19):
        audio.load_clip(AudioClipDescriptor("long", 10.0), pcm)
    with pytest.raises(AudioError, match="capacity"):
        audio.load_clip(AudioClipDescriptor("long", 10.0), pcm)
    audio.close()
