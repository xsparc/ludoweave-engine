# ADR-0014: Explicit render-graph dependencies and lifetimes

- **Status:** Accepted
- **Date:** 2026-08-05

## Context

Render-pass declaration order is not a sufficient dependency model. Transient
resources can otherwise be read before they are produced, used outside their
lifetime, or written concurrently without an explicit ordering path. These
failures must be reproducible without a GPU.

## Decision

Render graphs use named immutable resources and passes. Resources are external
or transient. Every transient declares its first and last pass, and its first
pass must write it. Passes declare reads, writes, and named dependencies.

Compilation validates names, unknown references, cycles, read-before-write,
access outside transient lifetimes, and unordered hazards where either access
writes. A stable name-sorted topological algorithm makes the compiled order
independent of declaration order. Compiled passes expose the same
`CommandList` records accepted by both devices.

## Consequences

- Invalid dependency and lifetime behavior fails deterministically in the
  Null backend and unit tests.
- Independent reads may remain unordered; any writer relationship needs an
  explicit dependency path.
- M3 does not allocate transient physical resources or optimize aliasing. The
  graph is a correctness boundary first.

## Alternatives considered

Implicit list order was rejected because refactors silently change hazards.
Provider-native render graphs were rejected because they cannot be validated
headlessly and would leak backend concepts. Automatic dependency inference was
rejected because it hides ownership mistakes and makes ambiguous writer order
look valid.
