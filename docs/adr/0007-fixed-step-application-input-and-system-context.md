# ADR-0007: Fixed-step application, immutable input, and system context

- **Status:** Accepted
- **Date:** 2026-08-05

## Context

M1-06 must invoke M1 systems without changing the established M0 `Engine.run(ticks)` contract or coupling ECS code upward to application and rendering modules. Interactive-style frame pumps may observe irregular monotonic time and must bound catch-up work without allowing frame grouping, rounded tick durations, or presentation values to change authoritative tick outcomes.

Systems need useful world access, but returning raw `World`, `ResourceStore`, `Query`, or `Commands` objects would make M1-05 read/write declarations unenforceable. Structural commands also need one unambiguous visibility boundary. Full tick transactions, persistent input/replay files, state hashes, and rollback remain M2 scope.

## Decision

`FixedStepApplication` is an additive application-layer runner exported from `ludoweave.app`; the root API and M0 `Engine` remain unchanged. The application layer may depend on public ECS, core clock, and render protocol contracts. ECS and core do not depend on application implementations, and application code never imports concrete render backends.

The runner owns and closes its injected `RenderBackend`. It is the single mutation owner of its injected `WorldStore` and `ResourceStore` while active. It shares an immutable `Schedule`, and does not close the clock or input source. Lifecycle and constructing-thread rules mirror M0.

`ApplicationConfig` contains exact positive `fixed_hz` and `catch_up_limit` integers. A pump adds `elapsed_ns × fixed_hz` integer accumulator units; one tick consumes exactly 1,000,000,000 units. A pump executes at most the catch-up limit and retains all excess backlog. Zero-elapsed pumps may drain it. Absolute exact-tick deadlines use `start + floor((tick + 1) × 1,000,000,000 / fixed_hz)`. No rounded delta accumulates. Systems receive the constant float `1.0 / fixed_hz`, which is a D1 convenience and not a D2 cross-platform float guarantee.

`pump()` renders once after zero or more catch-up ticks. `run_ticks()` is a separate, non-mixable deterministic convenience mode that waits or advances to exact deadlines and renders once per tick. Frames, interpolation alpha, and renderer diagnostics are presentation state and never feed input, scheduling, or world mutation.

Input uses frozen, slotted `InputSnapshot` values indexed by exact zero-based tick. Actions have unique stable names, canonical lexical order, and exact bool or finite-float values. Exact equality and hashing use a value-kind tag plus `float.hex()` so bool/float and signed-zero values cannot collapse. `NullInputSource`, `VirtualInputSource`, and `RecordedInputSource` return an empty snapshot for missing ticks and copy construction data. The recorded source is an in-memory M1 timeline, not a replay format. The exact global `INPUT_SNAPSHOT_RESOURCE` key must be present in the explicit application resource registry; the runner publishes the current snapshot before PRE_SIMULATE and rejects schedules that declare it writable.

Every system receives a synchronous invocation-scoped context. Its query wrapper defaults to stable entity ordering and validates include, exclude, changed, and explicit `.writes()` requests against declared component access. Its resource API returns detached values, stages write-declared values, and batch-commits them in canonical declaration order only after successful system return. Its commands facade validates component-bearing spawn/add/remove operations against declared writes. M1 has no entity-set/structural access declaration, so zero-component queries, empty spawn, and entity destruction are rejected inside scheduled systems rather than being invisible to scheduler conflicts. Retained contexts and facades expire after the call. Read cursors are aborted during cleanup; returning with an open writable cursor fails and discards its current row. Cleanup also runs for unwrapped `BaseException` control flow. These controls detect ordinary undeclared access but are not a Python sandbox: trusted system code can still reference globals or deliberately reach private objects.

Each tick has one new shared command buffer:

1. Acquire and publish immutable input.
2. Run PRE_SIMULATE systems.
3. Run SIMULATE systems.
4. Flush the buffer once.
5. Run POST_SIMULATE systems.
6. Count the tick complete.

PRE and SIMULATE structural changes are invisible until the flush and visible to POST. POST cannot enqueue structural commands because no second implicit flush exists. Enqueue order is stable schedule order. Flush failure uses the existing clone-staged atomicity and is attributed to the system whose command range contains the failing operation.

Before initialization succeeds, the application rebuilds the supplied systems with the scheduler and requires the injected immutable schedule to equal that canonical plan. Directly forged system order, edges, conflicts, eligibility, or registry access therefore cannot bypass planning rules.

M1 tick failure is explicitly nontransactional. An incomplete tick is not counted and unflushed commands are cleared, but committed query/resource writes from earlier systems and already-flushed structural changes remain. Errors chain the original cause and report available tick, phase, system, stage, and operation context. No placeholder world ID, command ID, receipt, hash, rollback, or replay claim is introduced.

## Consequences

- Irregular frame partitions and catch-up grouping cannot change the fully drained tick outcome for the same elapsed time and input timeline.
- Retained backlog is observable and deterministic but may remain high under sustained overload.
- System access declarations now constrain normal context operations without pretending arbitrary Python is pure or sandboxed.
- Resource adapters and system bodies remain trusted deterministic application code under ADR-0006.
- Presentation may render tick zero before any simulation tick; render frame counts are not authoritative.
- Platform event polling, device adapters, persistent replay input, random streams, physics, audio, extraction/interpolation state, concurrent execution, and M2 transactions remain deferred.
