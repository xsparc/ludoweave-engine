"""Audio contract and null-adapter lifecycle tests."""

from itertools import chain, repeat
from uuid import UUID

import pytest

from ludoweave.audio import (
    AudioBusDescriptor,
    AudioClipDescriptor,
    AudioError,
    AudioMixGraph,
    NullAudioBackend,
)


def _backend() -> NullAudioBackend:
    return NullAudioBackend(scope=UUID("3eb097a0-a26e-4602-b097-ff6e42384a40"))


def test_null_audio_load_play_volume_stop_and_close_lifecycle() -> None:
    backend = _backend()
    backend.initialize()
    clip = backend.load_clip(AudioClipDescriptor("laser", 0.25), b"decoded-pcm-fixture")
    backend.set_master_volume(0.75)
    backend.set_category_volume("effects", 0.5)
    playback = backend.play(clip, volume=0.25, loop=True)

    assert backend.clip_count == 1
    assert backend.active_playback_count == 1
    assert backend.master_volume == 0.75
    assert backend.category_volume("effects") == 0.5

    backend.stop(playback)
    assert backend.active_playback_count == 0
    backend.close()
    backend.close()
    assert backend.clip_count == 0


def test_null_audio_rejects_invalid_order_handles_and_values() -> None:
    backend = _backend()
    with pytest.raises(AudioError, match="invalid_state"):
        backend.load_clip(AudioClipDescriptor("laser", 0.25), b"pcm")
    backend.initialize()
    clip = backend.load_clip(AudioClipDescriptor("laser", 0.25), b"pcm")
    with pytest.raises(AudioError):
        backend.play(clip, volume=1.1)
    with pytest.raises(AudioError):
        backend.set_master_volume(1)  # type: ignore[arg-type]
    backend.close()
    with pytest.raises(AudioError, match="invalid_state"):
        backend.play(clip)


def test_null_audio_applies_bounded_mix_graph_gains() -> None:
    graph = AudioMixGraph(
        (
            AudioBusDescriptor("music", "master", 0.25),
            AudioBusDescriptor("master", None, 0.5),
            AudioBusDescriptor("effects", "master", 0.4),
            AudioBusDescriptor("dialogue", "effects", 0.5),
        )
    )
    backend = _backend()
    backend.initialize()
    backend.configure_mix(graph)
    clip = backend.load_clip(AudioClipDescriptor("laser", 0.25), b"pcm")
    backend.set_master_volume(0.8)
    backend.set_category_volume("effects", 0.25)
    playback = backend.play(clip, volume=0.5)

    assert graph.gain_for("effects") == pytest.approx(0.2)
    assert backend.playback_gain(playback) == pytest.approx(0.02)
    voice = backend.load_clip(AudioClipDescriptor("voice", 0.25, "dialogue"), b"pcm")
    backend.set_category_volume("dialogue", 0.5)
    voice_playback = backend.play(voice, volume=0.5)
    assert graph.lineage_for("dialogue") == ("master", "effects", "dialogue")
    assert backend.playback_gain(voice_playback) == pytest.approx(0.005)


def test_audio_mix_graph_rejects_cycles_missing_buses_and_late_reconfiguration() -> None:
    with pytest.raises(AudioError, match="acyclic"):
        AudioMixGraph(
            (
                AudioBusDescriptor("master", None),
                AudioBusDescriptor("a", "b"),
                AudioBusDescriptor("b", "a"),
            )
        )
    backend = _backend()
    backend.initialize()
    with pytest.raises(AudioError, match="invalid_bus"):
        backend.load_clip(AudioClipDescriptor("voice", 0.25, "dialogue"), b"pcm")
    backend.load_clip(AudioClipDescriptor("laser", 0.25), b"pcm")
    with pytest.raises(AudioError, match="invalid_state"):
        backend.configure_mix(AudioMixGraph((AudioBusDescriptor("master", None),)))


def test_audio_mix_graph_bounds_an_infinite_bus_iterator() -> None:
    buses = chain(
        (AudioBusDescriptor("master", None),),
        repeat(AudioBusDescriptor("overflow", "master")),
    )
    with pytest.raises(AudioError, match="one to 64"):
        AudioMixGraph(buses)  # type: ignore[arg-type]
