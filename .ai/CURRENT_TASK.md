# Current Task

- **Task:** M11 - Bounded headless rich 2D authoring modules
- **Status:** Complete, independently accepted, DCO-signed, published as ready
  stacked PR #12, and validated by all eight essential hosted CI jobs
- **Started:** 2026-08-06
- **Base:** Exact final M10 evidence head
  `bae799900671481cfd6f03fe502dea95b2c7f96c`; M11 stacks against
  `codex/m10-live-semantic-inspector`.
- **Outcome:** Implement the fifth authoritative post-alpha item as one
  dependency-free headless slice spanning richer audio mixing, bitmap text,
  exact-tick animation, immutable tilemaps, and fixed-point particles.
- **Acceptance gate:**
  - `ludoweave.presentation` exports typed frozen records and pure operations
    for bounded animation, bitmap text layout, tilemap culling, particle
    stepping, and existing render-record extraction.
  - Animation samples `once`, `loop`, and `ping_pong` from exact elapsed ticks
    without wall-clock or mutable player state.
  - Bitmap text validates caller-loaded glyph metrics, fallback, wrapping,
    alignment, and visible glyph sprites without font/provider objects.
  - Tilemaps validate unique IDs/layers, non-overlapping bounded chunks,
    declared cell IDs, half-open culling, and canonical tile order.
  - Particles use bounded immutable state, fixed-point integer motion, stable
    IDs, seeded repeatable velocity sampling, exact ticks, state digests, and
    interpolation-ready sprites.
  - Audio uses a maximum-64-bus immutable acyclic graph rooted at `master`;
    the Null adapter validates categories, configuration order, handles, and
    effective gain without opening a device.
  - Architecture tests prevent presentation from importing authority,
    application/tool, sample, concrete-backend, native, or provider modules.
  - A repeatable headless example exercises all five areas through Null audio
    and render devices; the isolated wheel and release sample bundle run it.
  - Full local quality, package, release, graphics, example, and independent
    review gates pass before signed commit, PR, or hosted-success claims.
  - The existing eight-job essential CI topology remains unchanged.
- **Architecture:** Presentation authoring may depend only on core and exact
  backend-neutral render contracts/extraction/opaque handles. It owns no world,
  provider, renderer resource, thread, clock, or mutable singleton. Gameplay-
  relevant cursors/edits/state remain ECS/world authority and must use commands.
- **Non-scope:** Real audio devices/callbacks, streaming/spatial/effects DSP,
  font parsing, kerning/shaping/bidirectional layout, rich markup, Tiled or
  general scene import, editor-scale streaming, particle DSL/editor, GPU
  particles, another world store, GUI/editor, networking, rollback, plugin
  manifests, 3D, SDL3, Box2D, native code, tags, releases, or publication.
- **SemVer:** Additive experimental Python/sample surface; runtime version
  remains `0.1.0a1` and no mandatory dependency is added.
- **Current evidence:** The final reviewed local gate reports 663 passing tests
  and one existing Windows symlink-capability skip, 164 formatted Python files,
  zero Ruff/Pyright findings, strict docs, pure wheel/sdist, isolated-wheel and
  complete ten-artifact release smoke, nine real-wgpu tests, valid inherited
  base/graphics profiling contracts, and successful Clockwork Arena, Agent
  World Builder, alpha acceptance, and rich-2D showcase execution. Independent
  findings-first re-review reports no remaining finding. GitHub Actions run
  `31024155710` passed the unchanged eight-job essential topology on signed
  implementation commit `aca6d93165a52d88451e8e06d5f1aa8d2e323f1d`.
