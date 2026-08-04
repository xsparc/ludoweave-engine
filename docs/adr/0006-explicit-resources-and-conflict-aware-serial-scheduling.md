# ADR-0006: Explicit resources and conflict-aware serial scheduling

- **Status:** Accepted
- **Date:** 2026-08-05

## Context

M1-05 needs typed world-level singleton data and a deterministic way to order gameplay systems before M1-06 invokes them. A process-global registry, implicit copying, or scheduler tie-breaking based on registration order would make world composition and replay behavior difficult to inspect. Running arbitrary Python systems concurrently would also make access declarations a weak hint instead of an enforceable ownership contract.

Resource values can contain mutable application objects. An unqualified `deepcopy` is not a safe engine policy because application hooks may execute arbitrary code, retain aliases, consult external state, or simply be unsupported. System conflicts likewise must not be silently resolved by incidental input order: a write/read or write/write relationship represents a design decision that must be explicit.

## Decision

`ResourceSpec[T]` is an explicit, identity-owned key with a stable name, exact Python value type, deterministic-eligibility flag, and caller-supplied copy adapter. `ResourceRegistry` is immutable, name-sorted, and accepts multiple named keys for the same value type. It recognizes the exact registered key object rather than a value-equal reconstruction. There is no global registry.

`ResourceStore` holds at most one value for each registered key. Values are copied on insertion and again when returned, replaced, removed, or cloned. A mutable adapter must return a distinct exact-type instance. Exact immutable scalar values may preserve Python identity because they cannot expose a mutable alias. Copy failures are structured and chained.

The adapter is trusted application code and receives the submitted or stored object as read-only input. A compliant adapter must not mutate that object or any nested state, perform I/O, consult time or randomness, retain aliases, or return a mutable alias. For compliant adapters, a failed copy leaves an existing store value unchanged. Python cannot enforce or roll back mutation performed inside arbitrary adapter code without introducing another trusted serialization boundary; violating this rule invalidates the store ownership guarantee.

Module-level synchronous Python functions declare systems with `@system`. The decorator returns the same function and attaches immutable metadata without registering it globally. A declaration names one fixed phase (`pre_simulate`, `simulate`, or `post_simulate`), component and resource reads/writes, explicit same-phase `before` and `after` constraints, deterministic eligibility, and an execution class.

`Scheduler.build()` is a planner only in M1-05; it never invokes systems. Fixed phase order resolves cross-phase access conflicts. Within one phase, every component or resource relationship containing a writer must have an explicit direct or transitive precedence path. An ambiguous conflict fails rather than acquiring order from input. Explicit dependencies form a same-phase DAG; unknown, duplicate, self, and cross-phase edges fail. Cycles report a canonical closed path and edge sources.

The resulting plan is a total serial order. Kahn topological planning uses lexical system name as the tie-break among currently ready systems, making the result independent of declaration input order. Python is the only accepted execution class in M1. Vectorized, native, process, and arbitrary concurrent execution remain declared future classes and are rejected by the planner.

## Consequences

- Resource identity and copy behavior are reviewable at composition time.
- Mutable resource values cannot enter or escape canonical storage through an ordinary public alias.
- Copy ownership depends on a narrow, explicit trusted-adapter contract; arbitrary service objects that cannot honor it are excluded.
- An explicit adapter is additional authoring work but prevents hidden serialization or copying behavior.
- Conflicting same-phase systems require an intentional ordering decision.
- Independent systems receive a stable serial order without promising parallel execution.
- System declarations cannot use wall clock, randomness, backend objects, or external state when marked deterministic; M1 validates declarations and eligibility but cannot prove function purity.
- M1-06 may execute the immutable plan through the declared `SystemContext` seam, but must preserve the same access and ordering contract.
