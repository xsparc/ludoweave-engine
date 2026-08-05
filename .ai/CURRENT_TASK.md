# Current Task

- **Task:** M18 - installed agent-tool conformance
- **Status:** Locally complete and validated on
  `codex/m18-agent-tool-conformance`; publication and hosted validation remain
  pending.
- **Started:** 2026-08-06
- **Base:** Exact clean synchronized `main` commit
  `ed65b12fa02f672113eac5939a0f616079fee44a`.
- **Outcome:** Give authors of local agent/tool adapters one small installed,
  versioned behavioral profile over the existing transport-independent
  `AgentCommandService` boundary without copying repository-private tests.
- **Acceptance gate:**
  - The public experimental runner accepts a bounded adapter ID and an
    explicitly supplied trusted factory. It performs no discovery, dynamic
    import, install, filesystem scan, subprocess launch, network request, or
    global registration.
  - One fixed baseline exercises factory ownership, the exact 12-tool
    discovery contract, clean read isolation, canonical snapshot, transaction
    dry-run, atomic apply receipt, stale-hash rejection without mutation,
    entity query/get, per-tick receipts, semantic diff, capture/test/telemetry,
    idempotent close, and structured use-after-close rejection.
  - Frozen reports use protocol `ludoweave.agent-tool-conformance/1` and
    profile `agent-tool-baseline/1`, with stable ordered statuses and
    runner-owned codes. Reports contain no provider exception text/error code,
    path, environment, timing, snapshot/capture bytes, entity data, or native
    object.
  - The built-in direct agent service passes from source, an isolated
    dependency-free wheel, and the deterministic release sample bundle.
  - Negative fixtures prove capability/tool/result mismatches, read mutation,
    malformed receipts, stale-hash mutation, cleanup failure, control-flow
    cleanup, immutability, and no-discovery behavior.
  - ADR-0032 and public guides record trust, ownership, limitations, evidence
    meaning, and the fact that accepted independent adapter adoption remains
    zero.
  - The existing eight essential CI jobs remain unchanged and only one hosted
    implementation run may be created.
- **Non-scope:** Adapter discovery/loading/installation, MCP/network transport,
  remote authentication, plugin fields or execution, sandboxing, security or
  provider certification, a new command/world implementation, external
  telemetry collection, GUI/editor, 3D, WASM, native code, dependency/lock/
  version changes, release tag, GitHub release, or package publication.
- **SemVer:** Additive experimental `ludoweave.agent` exports and a versioned
  report/profile. No stable API, persistent command/snapshot/replay format,
  runtime dependency, or package version change.
- **Baseline evidence:** On the exact clean base, `uv lock --check` resolved 46
  packages; the focused agent/CLI/import suite passed 111 tests in 1.70
  seconds; and `uv run --frozen pytest -q` passed 895 tests with the existing
  Windows symlink-capability skip in 65.00 seconds.
- **Current local evidence:** The final gate passes 925 tests with the existing
  skip, 145 focused tests, ten real-wgpu tests, strict Ruff/Pyright/docs, a pure
  93-entry isolated wheel, and a complete ten-artifact release smoke. All
  inherited benchmark/profile validators pass while the existing M1/M3 target
  misses remain explicit. No hosted M18 result is claimed yet.
