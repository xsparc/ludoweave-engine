# Current Task

- **Task:** M1 — deterministic world core milestone closure
- **Status:** Complete locally; ready for commit, push, pull request, and hosted CI
- **Started:** 2026-08-05
- **Completed locally:** 2026-08-05
- **Outcome:** The pure-Python deterministic world core now includes generational entities, explicit component schemas, canonical/reference worlds, typed queries and local structural commands, typed resources and deterministic scheduling, plus a fixed-step headless application runner with immutable input.
- **Acceptance gate:** All M0/M1 correctness, architecture, formatting, lint, type, test, documentation, package, installed-wheel, benchmark-validation, and audit gates pass locally; raw benchmark evidence records both observed and missed local engineering targets.
- **Decisions:** ADR-0003 through ADR-0007 record component identity, canonical storage, queries/commands, resources/scheduling, and fixed-step/input/system-context semantics.
- **Non-scope retained:** Persistent M2 commands/receipts/transactions, snapshots/replay/state hashes, random streams, WebGPU, MCP, physics, audio, networking, editor work, arbitrary concurrent Python systems, and native code.
- **Next assigned slice:** M2-01 persistent typed command envelopes and schema registry, after the M1 branch is committed, pushed, and opened for review.
- **SemVer:** Additive experimental `0.1.0.dev0` APIs; no compatibility promise or version bump in M1.
