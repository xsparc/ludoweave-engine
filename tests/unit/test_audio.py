"""Audio contract and null-adapter lifecycle tests."""

from uuid import UUID

import pytest

from ludoweave.audio import AudioClipDescriptor, AudioError, NullAudioBackend


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
