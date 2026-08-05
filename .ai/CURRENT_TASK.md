# Current Task

- **Task:** M10 - Headless live semantic inspector
- **Status:** Complete; published as ready stacked PR #11 and validated by all
  eight essential hosted CI jobs
- **Started:** 2026-08-06
- **Base:** Exact final-head hosted-validated M9 commit
  `22bc2de9f8450f60fe483bd4fea10a86702d2f0f`; M10 will stack against
  `codex/m9-box2d-plugin-evaluation`.
- **Outcome:** Add a headless inspector process that observes a live world
  exclusively through the existing local stdio MCP command/query protocol and
  emits a bounded, versioned stream of detached semantic observations.
- **Acceptance gate:**
  - `ludoweave inspect` starts only the built-in `python -I -m ludoweave mcp`
    child; it accepts no shell, executable, URL, host, port, or dynamic module.
  - Initial and post-transition observations include world description,
    bounded stable query results, telemetry, exact authority hashes, and
    semantic diffs without exposing snapshots, paths, environment values,
    process IDs, provider values, or mutable aliases.
  - The default inspector is read-only. Bootstrap/tick mutations require an
    explicit write flag and use existing versioned transactions/tick commands,
    receipts, optimistic hash chaining, and mutation safe points.
  - The inspector verifies the MCP lifecycle, required typed tools, response
    IDs/shapes, transition status, snapshot/diff hash continuity, message
    bounds, and child exit status.
  - The parent owns the child and closes it after success, protocol/domain
    failure, partial output, or exception; no background listener or orphan is
    created.
  - Source-tree and installed-wheel tests cover read-only, write/bootstrap,
    invalid capability/bounds, malformed/early child failure, and architecture
    bans on networking and arbitrary evaluation.
  - Full local quality/package/release/graphics gates and independent review
    pass before signed commit, stacked PR, or hosted-success claims.
  - Pull-request CI retains one complete baseline gate, all supported Python
    versions and operating systems, and real graphics coverage without
    repeating universal-wheel/release smoke on every platform.
- **Architecture:** The child world remains canonical. The inspector holds only
  detached JSON observations and an ephemeral prior snapshot used internally
  for `world_diff`; it cannot mutate outside versioned service tools.
- **Non-scope:** GUI/TUI/editor widgets, remote attach, sockets/HTTP/WebSocket,
  process discovery, arbitrary executables, shell commands, filesystem export,
  watch polling by wall clock, multiple targets, Box2D, richer media modules,
  plugin manifests, rollback/networking, 3D, WASM, native code, tags, releases,
  or package publication.
- **SemVer:** Additive experimental CLI/tooling only; runtime version remains
  `0.1.0a1`.
- **Review:** The first independent review found child import shadowing,
  dash-prefixed project-option injection, incomplete tick receipt validation,
  and unstructured stream-read failures. Isolated child resolution, option
  termination, exact receipt/hash/tick checks, structured reads, and
  adversarial regressions resolved all four; repeat review approved
  publication with no remaining blocker. A final CI review then found the
  consolidated baseline duplicated real graphics without installing its Linux
  runtime; the baseline now excludes that separately gated file and the
  architecture test locks the eight-job quota/security contract.
- **Hosted gate:** GitHub Actions run `31020096463` passed the complete Ubuntu
  3.12 quality/test/distribution gate; Ubuntu 3.13/3.14, Windows 3.14, and macOS
  3.14 compatibility; and real graphics on Linux, Windows, and macOS. PR #11 is
  open, ready, mergeable, and clean against
  `codex/m9-box2d-plugin-evaluation`.
