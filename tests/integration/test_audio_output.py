"""Optional provider wiring, distinct from physical audible-output validation."""

from typing import cast

import pytest

from ludoweave.audio import sounddevice as adapter
from tests.unit.test_blocking_audio import FakeStream


def test_real_provider_constructed_without_callbacks(monkeypatch: pytest.MonkeyPatch) -> None:
    provider = pytest.importorskip("sounddevice")
    captured: dict[str, object] = {}
    stream = FakeStream()

    def factory(**kwargs: object) -> FakeStream:
        captured.update(kwargs)
        return stream

    monkeypatch.setattr(provider, "RawOutputStream", factory)
    audio = adapter.BlockingAudioBackend()
    audio.initialize()
    audio.pump()
    audio.close()
    assert captured["callback"] is None
    assert captured["finished_callback"] is None
    assert captured["dtype"] == "int16"
    assert cast(int, captured["channels"]) == 1
    assert len(stream.blocks[0]) == 1470
