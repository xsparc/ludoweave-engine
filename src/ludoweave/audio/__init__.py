"""Engine-owned audio contracts and deterministic null adapter."""

from ludoweave.audio.api import (
    AudioBackend,
    AudioClipDescriptor,
    AudioClipHandle,
    AudioError,
    AudioPlaybackHandle,
)
from ludoweave.audio.null import NullAudioBackend

__all__ = [
    "AudioBackend",
    "AudioClipDescriptor",
    "AudioClipHandle",
    "AudioError",
    "AudioPlaybackHandle",
    "NullAudioBackend",
]
__stability__ = {name: "experimental" for name in __all__}
