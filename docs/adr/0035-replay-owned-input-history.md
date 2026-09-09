# ADR-0035: replay-owned input history

- Status: Accepted for M239; locally qualified, hosted qualification pending
- Date: 2026-09-09
- Design: [RFC-0221](../rfcs/0221-replay-owned-input-history.md)
- Supersedes: ADR-0027's prohibition on adding persistent input history only

## Decision

Add an application-level versioned envelope combining an unchanged replay-v1
timeline and its complete immutable input snapshots. Reject missing ticks rather
than silently supplying empty input. Preserve exact digital, analog and edge
values with the existing input validator and canonical JSON policy.

The world layer remains independent of application input. Replay still requires
trusted game composition code, but not the original input generator or ambient
input history. An explicitly supplied factory receives the envelope as its input
source after composition checks; all state/checkpoint verification remains enabled.

## Consequences

The envelope hash includes inputs; the embedded timeline hash does not change.
A digest proves identity, not authenticity. Factory-created resources remain the
caller's responsibility and replay is synchronous, single-owner and offline.
Old replay-v1 artifacts retain their existing input-injection requirements.
The historical M13 evaluator continues to describe that old format correctly.
No network authority, live rollback, transport, native code or new CI job is added.
