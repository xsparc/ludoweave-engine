# RFC-0129: defer asset-cache cleanup

- **Status:** Accepted
- **Milestone:** M146
- **Date:** 2026-08-27

## Summary

Do not add cache cleanup, garbage collection, prune, deletion, or eviction in
M146. Record the evidence and safety gates that must be satisfied before a
future mutation proposal can be considered.

## Context

M137-M145 provide bounded read-only cache inventory, deterministic path-free
fingerprints and comparisons, minimized unreferenced-blob aggregates, strict
saved-record admission, and offline verification. These are useful integrity
records, but the preview deliberately reports only a count and byte total.

Aggregate equality does not prove object identity: two observations may contain
different blobs with the same count and total bytes. “Unreferenced” also means
only that one admitted sequential observation found no action reference. It
does not prove that no concurrent writer, retained generation, lease, pin, or
external policy needs the object when deletion occurs.

## Decision

Asset-cache cleanup remains deferred. A future proposal must jointly define and
validate:

1. exact content identities for every candidate, bound to an admitted complete
   observation and exact cache layout;
2. every retained root, including action metadata, generations, leases, pins,
   in-flight readers/writers, and recovery state;
3. atomic-snapshot or generation-bound quiescence semantics that close the
   observation-to-deletion race;
4. explicit grace, age, and quota policy with a documented trusted-time source;
5. bounded dry-run output and a separate typed mutation command with receipts;
6. concurrent-writer exclusion, partial-failure recovery, idempotence, and
   interruption behavior;
7. cross-platform no-follow and reparse/link safety; and
8. restore or rollback behavior plus adversarial tests for every failure phase.

No single gate is sufficient. In particular, aggregate stability, digest
agreement, record age, local integrity, or cache idleness alone grants no
deletion authority.

## Consequences

M146 adds no runtime module, value, protocol, decoder, CLI command, cache read
or write, candidate disclosure, retention policy, mutation, dependency,
package-version change, workflow, runner allocation, permission, credential,
release authority, or CI change. M137-M145 protocols and bytes remain exact.
There is no CI change.

The next cleanup-related milestone must begin with a separate accepted RFC and
threat model. Until then, callers may inspect and verify aggregate evidence but
must not interpret it as safe-to-delete output.

## Alternatives considered

- Compare two aggregate previews. Rejected as a new API because M140 already
  reports the relevant deltas, while aggregate comparison cannot prove
  candidate identity or mutation safety.
- List candidates now and defer deletion. Rejected because identity disclosure
  without retained-root and quiescence semantics risks encouraging unsafe
  external deletion.
- Delete after a time threshold. Rejected because age requires trusted-time,
  retention, concurrency, and recovery policy that does not yet exist.
- Reuse implementation-specific cache idleness. Rejected because backend
  internals are not a public engine contract and idle alone does not establish
  reachability.

## Validation

An architecture test must prove that workflows, dependencies, cache runtime,
M143-M145 evidence contracts, CLI composition, and release surfaces remain
byte-exact; that the decision and non-goals are public; and that no cleanup or
mutation implementation was introduced. Strict docs, the complete established
test matrix, reproducible distributions, installed consumers, release rehearsal,
and findings-first review remain required before closeout.

## References

- [Bazel remote caching](https://bazel.build/remote/caching)
- [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html)
- [SLSA artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts)
