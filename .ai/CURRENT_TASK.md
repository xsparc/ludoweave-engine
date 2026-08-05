# Current Task

- **Task:** M9 — Box2D v3 plugin admission evaluation
- **Status:** Complete; published as ready stacked PR #10 and validated by all
  14 hosted CI jobs
- **Started:** 2026-08-06
- **Base:** Exact hosted-validated M8 head `187ad4503a40325a1e334da3cb4078969e2e043b`;
  the M9 PR will stack against `codex/m8-gamepad-sdl3-evaluation`.
- **Outcome:** Evaluate the current `box2d-python` binding against the explicit
  cross-platform wheel, ownership/lifetime, headless, API stability,
  GIL/threading, determinism, and adapter-conformance gates, then admit or
  defer a plugin with an accepted ADR.
- **Acceptance gate:**
  - Current facts come from primary project/package sources and reproducible
    isolated probes; no unexecuted installation or determinism claim is made.
  - The base package and lock remain unchanged, pure Python, and compiler-free.
  - An exercised probe checks available-version identity, bounded lifecycle
    churn, idempotent destruction, headless stepping, and same-binary repeat
    traces without importing LudoWeave or shipping the candidate.
  - Architecture tests prohibit Box2D/native-binding imports from public and
    canonical runtime code.
  - ADR-0024 records each admission gate, evidence, determinism/authority
    classification, decision, and measurable revisit conditions.
  - Full local quality/package/release/graphics gates and independent review
    pass before a signed commit, stacked PR, or hosted-success claim.
- **Architecture:** External rigid-body state cannot become a second canonical
  world. A future plugin must consume and return copied engine-owned values at
  explicit tick/command boundaries, close deterministically, and remain D0
  unless snapshot/replay/hash conformance proves a stronger tier.
- **Non-scope:** A Box2D dependency or adapter, rigid-body gameplay, ECS
  authority changes, plugin discovery/loading, release publication, semantic
  inspector, richer audio/text/animation/tilemap/particles, networking,
  editor, 3D, SDL3, Rust/PyO3, or other native code.
- **SemVer:** Evaluation tooling and documentation only; runtime version remains
  `0.1.0a1`.
- **Hosted gate:** GitHub Actions run `31015885190` passed quality/docs; Ubuntu
  CPython 3.12/3.13/3.14; Windows and macOS CPython 3.12/3.14; complete
  installed release-candidate smoke on all three systems; and real graphics
  smoke on all three systems. PR #10 is open, ready, mergeable, and clean
  against `codex/m8-gamepad-sdl3-evaluation`.
