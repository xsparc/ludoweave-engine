# Current Task

- **Task:** M33 - benchmark-regression-rate admission readiness
- **Status:** Implementation, findings-first review, and complete local
  validation are complete on neutral branch
  `evidence/m33-benchmark-regression-rate`; commit, hosted validation, PR,
  integration, and cleanup remain pending.
- **Started:** 2026-08-08
- **Base:** M32 implementation PR #52 and factual record PR #53 are
  squash-integrated. Exact clean synchronized `main`, `origin/main`, and
  `origin/HEAD` commit before branching was
  `60ddf57216d1054ac44df8d834756312c3864e3e`; only `main` existed locally and
  remotely.
- **Outcome:** Make the design plan's next ordered longer-term metric—benchmark
  regression rate—mechanically reportable from a complete reviewed controlled
  paired-comparison cohort without changing benchmarks/CI, querying GitHub,
  collecting telemetry, or inferring a zero rate from local timings, profiles,
  or passing smokes.
- **Acceptance gate:**
  - Add one strict reviewed manifest whose current evaluation-window set is
    empty and whose exact 199 bytes and SHA-256 are pinned.
  - Admit only registered M1-M4 `time.perf_counter_ns` workloads and exact
    `p95_ns`; exclude M7 cProfile diagnostics from timing comparison.
  - Require bounded chronological non-overlapping windows, a strictly later
    observation cutoff, and a complete reviewed controlled-runner census.
  - Bind each comparison to canonical run/job, distinct base/head revisions,
    exact benchmark/workflow sources, frozen runner profile, environment
    profile, result artifacts, and SHA-256 identities.
  - Require reviewed eligibility, comparability, tolerance predeclaration,
    outcome, provenance, validation, and cohort completeness.
  - Classify exact integer p95 evidence with predeclared basis-point tolerance;
    equality is stable and one unit above is regressed.
  - Preserve stable, regressed, and not-executed outcomes; non-execution remains
    counted and blocks rate publication.
  - Preserve complete accepted history through an executable mandatory prefix
    and exact whole-manifest digest.
  - Emit only sanitized aggregate evidence and an exact rational rate after
    complete admission; define no project-wide target, quality verdict, release
    gate, guarantee, native decision, SLA, or support promise.
  - Exercise source, isolated-wheel, and release-sample paths, accept RFC-0016,
    and preserve runtime, benchmark, dependency, lock, version, and workflow
    surfaces.
- **Non-scope:** New benchmark targets/runners/workflows; runtime optimization;
  Rust, PyO3, WASM, or other native code; GitHub discovery; telemetry;
  benchmark or CI mutation; public API/export; persistent format/protocol;
  dependencies/lock/version; providers; tags/releases/publication; performance
  certification, guarantees, SLAs, or support policy.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1` and
  stability labels remain unchanged.
- **Baseline evidence:** Repository/history audit was clean at exact base. The
  sandbox blocked the GitHub API open-PR query; it will be repeated with network
  access before publication. `uv lock --check` resolved the unchanged
  46-package lock. A first focused command used stale benchmark-test filenames
  and collected no tests; the corrected baseline passed 86 inherited
  M32/benchmark/release tests with one graphics-capability skip in 5.10 seconds.
- **Current evidence:** The exact empty manifest has SHA-256
  `720ae794e2a4ba76303196cd43d6ba0f3b21f81cffd4fa8584f526e2a0d48dca`.
  Its evaluator emits deterministic path-free `not-ready` evidence with zero
  windows/comparisons and no rate. All 44 adversarial evaluator tests pass.
  Packaging wiring plus strict Pyright, Ruff, and 59 focused tests pass. Strict
  docs and whitespace pass. The first complete suite found one inherited M32
  wording regression after 1,555 passes; the exact phrase was restored, 70
  M32/M33 contract tests passed, and the corrected complete suite passed 1,556
  tests with nine skips in 95.10 seconds. Pure build, isolated-wheel smoke, a
  fresh ten-artifact release smoke, all documented M1-M4 benchmark validators,
  both M7 profile validators, ten real-wgpu tests, and both graphics vertical
  slices pass. Protected surfaces are unchanged and artifact/security audits
  pass. The local benchmark/profile outputs are not admitted rate evidence.
