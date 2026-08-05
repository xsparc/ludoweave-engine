# Current Task

- **Task:** M8 — Gamepad input and SDL3 adapter-maturity decision
- **Status:** Complete; published as ready PR #9 and validated by hosted CI
- **Started:** 2026-08-05
- **Outcome:** Add provider-neutral, typed gamepad input that maps into the
  existing immutable per-tick action snapshots, and record an evidence-based
  decision on whether an SDL3 adapter is ready for the supported baseline.
- **Acceptance gate:**
  - Immutable bounded connection, button, and axis events use engine-owned
    identities and never expose provider objects.
  - Action maps support standardized gamepad buttons and axes with explicit
    deterministic ordering, finite normalization, deadzones, scaling,
    hotplug cleanup, and focus-loss behavior.
  - The already-pinned optional GLFW provider supplies standardized buttons
    and four unambiguous stick axes on Windows, macOS, and Linux without a new
    mandatory dependency. Its indistinguishable unavailable/half-pressed
    trigger values are omitted rather than synthesized.
  - Virtual/headless behavior, malformed input, provider failure, and
    installed-wheel use are exercised; real-provider smoke remains tolerant of
    machines with no attached gamepad.
  - SDL3/Python binding maturity is evaluated from current primary sources and
    accepted or deferred in an ADR with a measurable revisit gate.
  - The full documented quality, package, release-candidate, graphics, and
    repository review gates pass before publication.
- **Architecture:** Gamepad state remains non-canonical platform input until an
  application deliberately maps it into a tick-indexed `InputSnapshot`.
  Provider polling is single-thread owned, globally ordered by player slot,
  and isolated behind engine contracts. No SDL/GLFW/native value enters public
  APIs, world state, snapshots, commands, receipts, or replays.
- **Decision outcome:** Accepted ADR-0023 uses the existing pinned GLFW
  provider and defers SDL3 until its Python binding, offline binary delivery,
  lifecycle ownership, cross-platform conformance, and maintenance gates are
  satisfied. No dependency changed.
- **Local gate:** Windows, uv-managed CPython 3.12.13 reports 594 passed and one
  existing symlink-capability skip, 149 formatted files, zero Ruff/Pyright
  findings, strict docs success, a pure 79-entry wheel with no native entries,
  installed-wheel and complete release-candidate smoke, eight real wgpu/GLFW
  integration passes, and successful Clockwork Arena, Agent World Builder, and
  alpha-acceptance runs. Repeat independent review found no blockers and
  recommends PR publication. The superseded 589-pass run remains recorded.
- **Hosted gate:** GitHub Actions run `31012696753` passed all 14 jobs on PR #9:
  quality/docs; Ubuntu CPython 3.12/3.13/3.14; Windows and macOS CPython
  3.12/3.14; installed-wheel smoke on all three systems; and real graphics/
  GLFW gamepad smoke on Ubuntu, Windows, and macOS.
- **Non-scope:** Haptics, LEDs, sensors, touchpads, raw joysticks, controller
  remapping UI/database downloads, background input, multiple windows, IME,
  clipboard, real audio, networking, editor work, 3D, Box2D, Rust/PyO3, release
  tags, GitHub releases, or package publication.
- **SemVer:** Additive experimental Python surface only; version remains
  `0.1.0a1` unless implementation evidence requires a different decision.
