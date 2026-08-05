# ADR-0026: Bounded headless-first rich 2D authoring modules

- **Status:** Accepted
- **Date:** 2026-08-06

## Context

The post-alpha sequence next calls for richer audio, text, animation, tilemap,
and particle modules. M3 already owns backend-neutral sprite/tile extraction,
and M4 has only a minimal audio protocol and Null adapter. Adding provider
objects, wall-clock animation, unbounded maps/effects, or a second presentation
store would violate the existing determinism, headless, and ownership rules.

## Decision

Add one public `ludoweave.presentation` authoring layer. It may import core and
the engine-owned render contracts, extraction records, and opaque handles. It
may not import ECS/world implementations, application/tool composition,
concrete render backends, or third-party providers.

- Sprite animation is sampled from exact non-negative elapsed ticks. `once`,
  `loop`, and `ping_pong` timelines use bounded immutable atlas frames and never
  read a wall clock.
- Text uses caller-supplied bounded bitmap glyph metrics, deterministic
  code-point wrapping/alignment, and sprite extraction. M11 does not parse font
  files, shape scripts, apply bidirectional layout, or expose provider objects.
- Tilemaps use bounded immutable row-major chunks, unique layers and tile IDs,
  non-overlap validation, half-open integer culling, and existing tile batches.
- Particles use bounded immutable state, stable identities, integer fixed-point
  motion, a specified counter-derived SplitMix64 sampler, exact tick stepping,
  and sprite extraction. No module-global RNG or mutable singleton exists.
- Audio gains use a bounded immutable acyclic bus graph rooted at `master`.
  The Null adapter validates configuration, clip categories, lifecycle, and
  effective gains; M11 adds no real audio device or callback.

All authored records and failures are typed and validated. Presentation
extraction remains non-authoritative. If elapsed animation, tile edits, or
particle state affects gameplay or replay, the composition must store that
state in the ECS/world authority and mutate it through the existing versioned
command boundary. M11 adds no world mutation command.

The headless showcase and isolated-wheel/release smoke must exercise all five
areas without a display, audio device, network, native compiler, or new runtime
dependency.

## Consequences

- Headless tests and agents can build and inspect the same authored 2D records
  before any real provider is involved.
- Tick animation and fixed-point particles are reproducible for identical
  validated inputs; GPU pixels and real audio timing still have no bit-exact
  cross-platform guarantee.
- Bitmap layout is useful for atlases and UI fixtures but is intentionally not
  international text shaping.
- Dense chunks and immutable particle replacement favor a small auditable
  contract over editor-scale throughput. Performance admission requires later
  evidence, not speculative native code.
- Public additions remain experimental under `0.1.0a1`.

## Alternatives considered

- A new scene graph or presentation world was rejected because canonical state
  already belongs to ECS/world storage.
- Free-running mutable animation and particle managers were rejected because
  ownership, replay, and tick provenance would be ambiguous.
- HarfBuzz/FreeType, a production audio provider, Tiled parsing, and a particle
  DSL were rejected because each adds dependency, format, security, and
  cross-platform work beyond this bounded milestone.
- Implementing the modules directly in the wgpu adapter was rejected because
  it would make headless execution secondary and leak provider direction into
  authoring contracts.
