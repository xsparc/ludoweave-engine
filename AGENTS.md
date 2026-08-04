# AGENTS.md

This file is the operating contract for human and automated contributors to LudoWeave Engine.

## Read first

1. The assigned issue or milestone acceptance criteria.
2. `docs/architecture.md` and relevant accepted ADRs.
3. `.ai/PROJECT_STATE.md`, `.ai/CURRENT_TASK.md`, and `.ai/TEST_EVIDENCE.md`.
4. Current code, tests, CI, and `git status`.

## Authoritative rules

1. Canonical runtime state belongs to the ECS/world store as it is introduced through M1.
2. Headless execution is first-class.
3. Every externally initiated world mutation must eventually be a versioned command that produces a receipt.
4. Public APIs must not expose wgpu, GLFW, NumPy storage, or native extension objects.
5. No arbitrary Python evaluation or unauthenticated remote control.
6. Normal CPython 3.12-3.14 is the baseline; free-threaded builds are optional experiments.
7. Apache-2.0 and DCO sign-off govern contributions.
8. Never claim a check passed unless it was executed and its result was recorded.
9. Do not create empty speculative packages or abstractions without an exercised test or example.
10. Stop at the assigned milestone; do not opportunistically implement adjacent roadmap items.

## Dependency direction

Contracts and core code do not import application, tool, or concrete-backend modules. Application code depends on engine-owned protocols. Concrete adapters implement those protocols. CLI and examples are composition roots and may choose a concrete adapter. See ADR-0002 and the architecture tests.

## Working method

- Keep one task in progress and map changes to acceptance criteria.
- Preserve unrelated user changes and never use destructive Git commands to discard work.
- Add focused tests and public documentation with behavior changes.
- Run focused checks first, then every command in the README quality suite.
- Review the diff for scope growth, secrets, dependency violations, backend leakage, nondeterminism, packaging effects, and stale documentation.
- Update `.ai/PROJECT_STATE.md` and `.ai/TEST_EVIDENCE.md` with reproducible facts only.

## Current boundary

M0 and M1 are complete locally. The user has authorized milestone work through M6, but each milestone must still be implemented and fully validated on its own task-scoped branch before automatic commit, push, and pull-request creation. M2-01 persistent typed command envelopes and schema registry is next; snapshots, WebGPU, MCP, physics, audio, networking, editor work, and native code remain out of scope until their assigned roadmap slices. The complete-M1 benchmark records a substantial local 10,000-entity tick target miss; it does not authorize native acceleration.
