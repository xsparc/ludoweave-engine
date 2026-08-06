# Current Task

- **Task:** M20 - command/receipt preview-readiness decision
- **Status:** Complete. Implementation, local validation, findings-first
  review, ready PR #28, the single unchanged essential hosted run, and exact
  squash integration into `main` are complete. PR #28 produced GitHub-verified
  main commit `d166ef86bf25526d9d7715f63263d3cac6db78d4`; the milestone branch
  remains for audit history.
- **Started:** 2026-08-06
- **Outcome:** Decide whether the central installed command, transaction, and
  receipt contracts can honestly move from experimental to preview stability,
  using deterministic evidence rather than inferring compatibility from their
  same-version quality.
- **Acceptance gate:**
  - One dependency-free installed example emits exact versioned schema
    `ludoweave.evaluation.command-receipt-stability/1` with a deterministic
    decision and no arguments, ambient inputs, paths, timing, state hashes,
    world values, captures, or provider diagnostics.
  - Evidence confirms exact command/transaction/receipt protocol IDs, built-in
    operations, public stability labels, canonical decode/round trip, dry-run
    non-mutation, committed hash continuity, stale-hash and unsupported-hash
    rejection, and failed-middle-operation atomicity.
  - The existing installed twelve-check M18 agent-tool profile passes against
    a fresh explicitly composed built-in authority, proving transport-
    independent same-version command/receipt behavior without adding another
    conformance runner.
  - The preview promotion gate explicitly covers a cross-version fixture
    corpus, external consumer feedback, operation-argument evolution rules, a
    bounded public receipt reader, receipt-diff/diagnostic evolution rules, and
    a supported deprecation-capable feature-release channel.
  - RFC-0003 records the evidence-based decision. No stability label or wire
    contract changes unless every gate is actually met.
  - The evidence runs from source, an isolated dependency-free wheel, and the
    deterministic release sample bundle with a strict exact-type validator.
  - Architecture tests reject ambient/discovery/backend/tool imports, prove the
    scanner with nested invalid fixtures, preserve root exports and dependency
    metadata, and verify the command/receipt exports remain focused.
  - The existing eight essential CI jobs remain unchanged and only one hosted
    implementation run may be created.
- **Non-scope:** A new command or operation, receipt reader, schema migration,
  field reinterpretation, stability promotion, source runtime module, package-
  root export, plugin field, provider discovery/loading, transport/listener,
  storage backend, networking, editor, 3D, WASM, Box2D, native code, dependency,
  lock, package version, CI job, tag, release, or publication.
- **SemVer:** Evidence/documentation only. All existing command/receipt Python
  exports and persistent protocols retain their current experimental status;
  package version remains `0.1.0a1`.
- **Baseline evidence:** On exact base
  `2fdeccd697f09f3e165130eb8564a6c585d472d2`, `uv lock --check` resolved 46
  packages; 91 focused canonical-command/transaction/receipt/agent/API tests
  passed in 1.52 seconds; and the full suite passed 955 tests with the existing
  Windows symlink-capability skip in 72.22 seconds. The initial sandboxed lock
  check exited 1 before project execution because uv's existing user cache was
  inaccessible; the approved cache-access rerun exited 0.
- **Current local evidence:** The final Windows/uv-managed CPython 3.12.13 gate
  passes 972 tests with one existing symlink-capability skip in 73.99 seconds,
  205-file formatting, Ruff, strict Pyright, strict MkDocs, source and installed
  evidence, pure-wheel build/smoke, a fresh complete 10-artifact release smoke,
  211 expanded focused tests, and ten real-wgpu tests. Every inherited
  benchmark/profile artifact validates; the M1 simulation and both M3 targets
  remain observed misses. Findings-first review hardened forbidden-import
  matching for submodules and found no remaining issue. Ready PR #28 is
  mergeable and clean; GitHub Actions run `31095009029` passed all eight
  unchanged essential jobs on DCO-signed implementation commit
  `d96d132da5ee847d6e86645be5e87a1e4aa5e89e`. PR #28 squash-integrated exact
  final evidence head `d04561184996fac507071ad9e7dd0ef9c5e3cb7c` as verified
  `main` commit `d166ef86bf25526d9d7715f63263d3cac6db78d4`; both trees are
  `c3e2dc1224f530fb483d1b9684ff55329bf9557b`. No tag, release, package
  publication, stability promotion, cross-version compatibility, or external
  adoption is claimed.
