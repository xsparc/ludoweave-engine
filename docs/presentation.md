# Rich 2D presentation authoring

M11 adds dependency-free authoring records for audio mix graphs, bitmap text,
tick animation, chunked tilemaps, and fixed-point particles. They run headlessly
and translate only into existing engine-owned render records.

Run the combined example from a source checkout or sample bundle:

```console
python examples/rich_2d_showcase.py --ticks 6
```

The command prints one versioned JSON summary. It creates no window, audio
device, file watcher, network listener, or background thread.

## Authority and determinism

`ludoweave.presentation` does not own a world. Its values are detached immutable
authoring or presentation values. If an animation cursor, tile edit, or particle
state can influence gameplay, persist it as a registered ECS component/resource
and change it through the versioned world command protocol. Renderer extraction,
interpolation, and audio device state never enter authority hashes.

Animation accepts elapsed ticks, not seconds. Tile coordinates and text layout
metrics are integers. Particle motion uses 1,024 fixed subpixels per authored
unit, stable particle IDs, and a specified seed sampler. Identical validated
inputs therefore produce identical samples and particle state hashes on normal
supported CPython. GPU output and future real-device audio timing are outside
that guarantee.

## Modules

### Animation

`SpriteAnimationClip` contains bounded atlas frames with positive tick
durations. `sample_animation()` supports `once`, `loop`, and `ping_pong`.
`animation_sprite()` converts a detached sample into `SpriteExtractionSource`;
it never owns a texture or player thread.

### Bitmap text

`BitmapFont` contains caller-loaded glyph metrics and atlas UVs.
`layout_text()` applies explicit newlines, four-space tabs, fallback glyphs,
bounded glyph wrapping, and left/center/right alignment using integer units.
`glyph_sprites()` emits one sprite per visible glyph.

This is bitmap atlas layout, not rich-text markup or international shaping.
Font parsing, kerning tables, bidirectional layout, IME, HarfBuzz, and FreeType
remain separate future work.

### Tilemaps

`TileMap` contains unique `TileDefinition` and `TileLayer` records. Layers own
bounded non-overlapping row-major `TileChunk` values. `extract_tile_groups()`
culls a half-open integer cell rectangle and emits stable y/x-ordered tile
batches through an opaque engine texture handle. The model has no project-file
parser or editor state.

### Particles

`ParticleEmitter` declares capacity, spawn rate, lifetime, integer origin,
velocity ranges, acceleration, and seed. `step_particles()` returns a new
`ParticleState`; it never mutates an input or reads global randomness.
`particle_sprites()` converts fixed-point previous/current positions to the
existing interpolation boundary. Work is capped at 100,000 live particles and
10,000 ticks per call, with an additional 10,000,000 particle-tick work budget.

### Audio mix graph

`AudioMixGraph` is a maximum-64-bus acyclic graph rooted at `master`. Authored
gain resolves through parents. `NullAudioBackend.configure_mix()` must run
before clips are loaded, rejects undeclared clip categories, and exposes the
effective gain of live validation-only playbacks. It still produces no sound.

## Ownership, threading, and failure

Authoring records are immutable and have no close operation. Render texture,
surface, and pipeline handles remain owned by their injected render device.
The engine/composition owns and closes the Null audio and render devices.
Provider lifecycles remain single-thread-owned; pure sampling/layout/stepping
functions retain no shared mutable state and may be called independently.

Invalid bounds, types, order, graph cycles, unknown IDs, overflow, or lifecycle
use raises `PresentationError`, `AudioError`, or existing render errors with
stable subsystem, phase, code, and contextual details. Inputs are bounded before
large traversal or allocation.

See [ADR-0026](adr/0026-bounded-headless-rich-2d-authoring.md), the
[rendering contract](rendering.md), and the [runtime authority rules](runtime-contract.md).
