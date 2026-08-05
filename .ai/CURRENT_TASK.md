# Current Task

- **Task:** M4 — Clockwork Arena playable vertical slice
- **Status:** Implementation and complete local validation are green; DCO-signed publication and hosted validation are pending
- **Started:** 2026-08-05
- **Acceptance gate:** Provider-neutral input, project-confined content-addressed assets, bounded deterministic collision, a minimal engine-owned audio contract, and the Clockwork Arena sample must remain deterministic, headless-first, backend-isolated, packaged, documented, and executable through source and installed-wheel paths.
- **Input outcome:** Immutable keyboard, mouse, pointer, focus, resize, and close events feed action maps and exact-tick snapshots with pressed, just-pressed, and just-released semantics. The interactive wgpu composition root handles movement, aim, fire, restart, resize, and close without provider objects crossing public APIs.
- **Asset outcome:** Strict `asset://` manifests confine sources to a project root, content-address cache keys include transitive dependencies, PNG decoding is bounded and deterministic, and immutable texture revisions support explicit retirement.
- **Collision/audio outcome:** Deterministic AABB/circle overlap, a sorted exact-filter spatial grid, bounded X-then-Y kinematic movement, and a strict lifecycle-validating null audio backend are implemented without Box2D or provider dependencies.
- **Sample outcome:** Clockwork Arena owns canonical gameplay state in the world/resource stores, advances through ordinary versioned transactions and receipts, uses fixed-seed random streams and exact-tick input, extracts immutable presentation, and supports deterministic headless, stress, offscreen wgpu, and interactive window runs.
- **Local gate:** The complete frozen suite reports 516 passed and one existing Windows symlink-capability skip; Ruff, strict Pyright, strict MkDocs, pure wheel build, installed-wheel smoke, architecture checks, real offscreen and GLFW examples, exact 3,600-tick replay/hash evidence, and the 300-sample M4 benchmark artifact/validator all pass.
- **Hosted gate:** Pending publication of `codex/m4-clockwork-arena` as a stacked PR against the validated M3 branch and completion of its 14-job matrix.
- **Known performance result:** The local baseline workload recorded p50/p95/p99 of 1.5228/2.1228/2.5898 ms and observed the 16.666667 ms p95 target. Stress levels 4 and 8 recorded informational p95 values of 3.5029 ms and 4.8371 ms; no targets are assigned to them.
- **Non-scope retained:** MCP/agent control, real audio playback, Box2D, networking, editor tooling, 3D, automatic device recovery, native acceleration, Rust, and PyO3.
- **SemVer:** Additive experimental `0.1.0.dev0` surface; no compatibility promise or version bump.
