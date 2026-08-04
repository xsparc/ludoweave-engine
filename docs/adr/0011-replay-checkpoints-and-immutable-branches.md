# ADR-0011: Replay checkpoints and immutable timeline branches

- **Status:** Accepted
- **Date:** 2026-08-05

## Context

A command log is only useful for deterministic verification when it identifies
the exact starting authority state, composition, tick boundaries, and expected
hashes. A list of commands without this context can silently run against a
different schema, dependency set, random seed, operation registry, or platform
profile. Tick counts also cannot be inferred from batch position because
non-tick transactions may share a completed-tick boundary.

Branches must preserve history. Editing a parent log in place would make audit
references and earlier checkpoint evidence ambiguous.

## Decision

Replays use canonical `ludoweave.replay/1` documents containing:

- a compatibility header with engine version, D1 profile, project-schema hash,
  dependency-lock hash, explicit platform profile, operation-registry
  fingerprint, random seed, world identity, and initial tick/hash;
- one embedded immutable canonical snapshot;
- ordered committed transaction batches with contiguous indexes, exact
  start/end completed ticks, and pre/post authority hashes;
- optional checkpoints naming an exact `after_batch` boundary, tick, and hash.

Replay decode is bounded and schema-exact. The runner reconstructs a fresh
session from the embedded snapshot, applies the same typed
`CommandTransaction` values through `TransactionService`, and verifies reached
ticks and hashes. Rejected transactions or divergences identify the exact batch
without exposing environment or path data. The initial snapshot/header identity
is always verified; callers may disable subsequent batch/checkpoint hash
verification only for diagnostic execution.

`ReplayRecorder` is the sole append owner for its timeline. It does not append
dry-run or failed transactions, returns a failed transaction's rejected
receipt, detects authority changes performed outside the recorder, preflights
deterministic replay limits before commit, and records only committed receipts.
Transaction IDs are unique within one timeline.

A branch is a new self-contained timeline whose initial snapshot is the parent
state after all recorded work at an exact completed-tick boundary. Its header
contains the parent timeline ID, SHA-256 digest of the complete immutable parent
document, parent batch boundary, tick, and state hash. Parent bytes are never
rewritten. Persistent `world.tick` commands advance exactly one tick, so every
completed recorded tick is an exact batch and branch boundary.
Branch replay can additionally require the immutable parent document, verify
its ID and complete timeline digest, reproduce the referenced parent
batch/tick/hash boundary, and only then execute child batches.

## Consequences

- Repeated replay from the same header/snapshot reaches every recorded
  checkpoint or reports the first exact divergence.
- Zero-tick command batches remain ordered without inventing tick gaps.
- Multi-tick persistent batches are rejected; callers record one command batch
  per tick so snapshots and branches never hide an intermediate tick.
- Branches can be replayed independently while retaining a verifiable parent
  reference and branch-state hash.
- The embedded initial snapshot makes M2 replay files self-contained. External
  content-addressed snapshot references may be added later under a separately
  versioned format.
- Platform profiles are explicit caller-supplied compatibility identities, not
  ambient path, hostname, or environment capture.
- Trusted tick executors, migrations, codecs, and resource adapters retain the
  deterministic/no-external-side-effect obligations recorded in earlier ADRs.

## Alternatives considered

JSON Lines without a header was rejected because composition and initial-state
compatibility would be implicit. Using tick number as the only checkpoint
position was rejected because multiple ordered transactions can occur at the
same completed tick. Rewriting a replay prefix for a branch was rejected
because it destroys immutable-history identity. Path-based snapshot references
were deferred because transport/path policy belongs to CLI and artifact
adapters, not the world-domain replay contract.
