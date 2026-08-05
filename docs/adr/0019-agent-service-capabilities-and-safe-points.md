# ADR-0019: Agent service capabilities and mutation safe points

- Status: Accepted
- Date: 2026-08-05

## Context

M5 needs one surface through which Python callers, a local CLI, and an MCP
adapter can inspect and operate a live world. Giving each transport its own
mutation implementation would split authority, weaken receipt equivalence, and
make safety policy inconsistent. Agent-facing calls also require explicit
capabilities, bounded work, caller attribution, redaction, and predictable
concurrency behavior.

## Decision

Add a transport-independent `AgentCommandService` in `ludoweave.agent`. It owns
tool schemas and safety policy while delegating all authority changes to the
existing `WorldSession` and `TransactionService`. Transactions keep their
canonical command protocol and receipts. A convenience tick call constructs
one ordinary transaction per tick so every committed tick remains an atomic
replay and branch safe point.

Read is always enabled. Write, capture, and registered-test capabilities are
separate, immutable, and disabled by default. Limits bound requests, results,
queries, transactions, ticks, snapshots, captures, tests, and call rate.
Diagnostics and telemetry redact credential-shaped values. Capture, telemetry,
and tests are injected provider protocols; only the capture provider is owned
and closed by the service.

The service is owned by its constructing thread. Mutations use a non-blocking
single-owner gate and reject wrong-thread, concurrent, or reentrant mutation.
Reads return detached documents. The service does not expose ECS storage,
render-provider objects, paths, environment values, arbitrary imports, Python
evaluation, or shell execution.

## Consequences

- Direct Python, CLI, and MCP calls share the same validation, capability,
  atomicity, receipt, replay, and error behavior.
- Read-only composition is safe by default; authorization is explicit at the
  trusted composition root rather than hidden in request data.
- A multi-tick convenience request may have a committed prefix because each
  tick is intentionally its own atomic receipt. Callers can resume from the
  last returned hash without inventing a larger unbranchable transaction.
- The initial model serializes mutations and is not a distributed transaction
  system. Remote authentication, multi-writer scheduling, and networking remain
  deferred.

## Alternatives considered

Transport-specific world adapters were rejected because they would duplicate
authority rules. Embedding provider callables or module names in request data
was rejected as arbitrary execution. Blocking a concurrent mutation was
rejected because an unbounded wait is less predictable than a structured busy
failure. Treating a requested tick count as one atomic batch was rejected
because it would erase the per-tick receipt and branch boundary established by
M2.
