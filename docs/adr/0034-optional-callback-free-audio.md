# ADR-0034: optional callback-free audio output

- Status: Accepted; locally qualified, hosted qualification pending
- Date: 2026-09-09
- Supersedes: the Null-only audio-provider restriction in ADR-0018
- Design: [RFC-0220](../rfcs/0220-optional-blocking-audio.md)

## Decision

Admit sounddevice 0.5.6 through an optional `audio` extra and isolated
`BlockingAudioBackend`. Retain AudioBackend and Null. The adapter passes no
stream or completion callback. The owning application calls `pump` to mix
bounded PCM and write through the blocking raw-output API. No Python work runs
in a PortAudio callback.

Device latency, completion and underruns never control canonical state or
replay. Clockwork Arena derives effects from committed counters; only opt-in
device mode is paced by output.

## Consequences

No worker or process-global mixer ownership is added. Writes can block and
underrun; there is no hard real-time guarantee. Linux requires system PortAudio.
Devices/providers remain optional and their objects never enter public
contracts. Null stays dependency-free and unpaced. Richer formats, resampling,
spatial audio and background mixing remain deferred.
