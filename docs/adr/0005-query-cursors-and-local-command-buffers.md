# ADR-0005: Query cursors and local structural command buffers

- **Status:** Accepted
- **Date:** 2026-08-05

## Context

M1-04 needs useful world traversal without exposing dense rows or sparse indexes. Mutable query results can bypass validation unless their ownership and writeback boundaries are explicit. Structural mutation during iteration can also invalidate candidates, while an abandoned iterator can leave ambiguous ownership unless it has an explicit close operation.

Gameplay systems also need to defer entity and component membership changes until a safe boundary. These local operations are not the persistent, versioned commands and receipts planned for M2: they have no serialization format, authority metadata, stable command ID, transaction identity, or replay contract.

## Decision

`Query` is an immutable, storage-neutral builder. Included types form a conjunction, excluded types form a disjunction, and changed filtering matches when any watched included component has a change epoch strictly greater than the supplied epoch. Callers may request stable ascending `EntityId` order; native order has no compatibility guarantee. Production plans select a smallest included table with a UUID tie-break and cache only private layout choices. Structural epochs invalidate those plans.

Query rows contain detached component copies in caller-specified include order. Read-only row mutation is discarded. A caller must declare writable included types with `writes()` and use the resulting cursor as a context manager. Writeback occurs one row at a time: every changed writable component in that row is validated before any is stored, shares one new world epoch, and is copied again into canonical state. An invalid row commits none of that row, releases the cursor, and preserves earlier completed rows. Queries are therefore not transactions.

Read-only cursors may overlap other read-only cursors. Any overlap involving a writable cursor fails. Direct structural and value mutation, cloning, and command-buffer flushes fail while any cursor is active. Early exit retains the guard until `close()` or context exit; correctness does not depend on finalizers. A context exception discards the current row, preserves earlier writeback, releases the guard, and propagates.

`Commands` is a reusable, world-bound local buffer. Components are validated and copied when enqueued. A deferred spawn returns an opaque token bound to that exact buffer generation; it can target later operations in the same generation but cannot cross buffers or worlds. `clear()` discards queued operations and invalidates outstanding tokens.

`World.flush()` applies a non-empty buffer to a private clone in enqueue order, then adopts the staged state only after complete success. Epoch and allocation behavior therefore matches the equivalent direct operations. Failure chains the original structured cause, retains the queue for identical retry or explicit clear, and leaves the world unchanged. Success clears the buffer and returns a local `FlushResult`; an empty flush is a no-op. This result is explicitly not an M2 receipt.

`ReferenceWorld` shares public query, cursor, buffer, immutable record, token, result, schema, entity, and error contracts. It independently chooses query candidates, evaluates filters, copies and validates rows, writes back values, stages command application, resolves targets, and adopts successful state. Architecture tests prohibit imports from the production world, allocator, storage, or private planner/executor details.

## Consequences

- Storage layout and dense row order remain private and replaceable.
- Ordinary query values cannot escape as aliases to canonical component instances.
- Cursor lifetime is explicit; callers that break early must close the cursor.
- Row writeback is deterministic and locally atomic, but a query is not an all-rows transaction.
- Clone-staged flush prioritizes correctness and rollback over throughput; M1 benchmarks measure its cost before optimization.
- Local buffers solve structural safety inside one live process without pre-empting versioned M2 commands, receipts, snapshots, hashes, or replay.
- Cross-world equality of independently created `EntityId` values cannot be detected from the ID alone; persistent world identity is deferred.
