# Current Task

- **Task:** M5 — Agent Command Service and local MCP adapter
- **Status:** Complete; DCO-signed PR #5 is published and hosted run 30999777517 passed all 14 jobs
- **Started:** 2026-08-05
- **Acceptance gate:** One transport-independent typed service must expose the assigned 12-tool surface through direct Python, a project-confined CLI, and a thin local MCP adapter while preserving canonical world ownership, exact receipts, atomicity, safety limits, backend isolation, and read-only defaults.
- **Service outcome:** `AgentCommandService` provides immutable JSON Schema tool discovery, implicit read access, explicit write/capture/test capabilities, bounded requests/results/work, monotonic rate limits, caller binding, redaction, replay recording, and non-blocking single-thread mutation ownership over the existing `WorldSession` and transaction service.
- **Transport outcome:** `ludoweave agent` uses the data-only project confinement boundary. `ludoweave mcp` implements local stdio MCP `2025-11-25` initialize/ping/tools discovery/calls with no socket, HTTP listener, arbitrary evaluation, shell, or new runtime dependency.
- **Acceptance outcome:** Agent World Builder creates six typed ECS entities, validates and commits the layout, advances three individually receipted ticks, captures 320x180 RGBA8 presentation, queries and adjusts the player, diffs snapshots, runs four registered checks, reads telemetry, and records five replay batches.
- **Local gate:** The complete frozen suite reports 545 passed and one existing Windows symlink-capability skip; Ruff, strict Pyright, strict MkDocs, pure-wheel build, installed-wheel smoke, architecture/security scans, direct/CLI/MCP receipt equivalence, actual MCP subprocess coverage, and real offscreen wgpu acceptance all pass.
- **Hosted gate:** PR #5 is published against the validated M4 branch. Run `30999777517` passed quality/docs, seven CPython/OS test jobs, three isolated installed-wheel smokes, and three real graphics smokes including Agent World Builder.
- **Non-scope retained:** Network/HTTP agent transport, remote authentication, arbitrary project code loading, shell/eval tools, editor tooling, production audio, Box2D, 3D, automatic device recovery, native acceleration, Rust, and PyO3.
- **SemVer:** Additive experimental `0.1.0.dev0` surface; no compatibility promise or version bump.
