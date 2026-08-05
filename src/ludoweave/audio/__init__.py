"""Engine-owned audio contracts and deterministic null adapter."""

from ludoweave.audio.api import (
    AudioBackend,
    AudioBusDescriptor,
    AudioClipDescriptor,
    AudioClipHandle,
    AudioError,
    AudioMixGraph,
    AudioPlaybackHandle,
)
from ludoweave.audio.null import NullAudioBackend

__all__ = [
    "AudioBackend",
    "AudioBusDescriptor",
    "AudioClipDescriptor",
    "AudioClipHandle",
    "AudioError",
    "AudioMixGraph",
    "AudioPlaybackHandle",
    "NullAudioBackend",
]
__stability__ = {name: "experimental" for name in __all__}
