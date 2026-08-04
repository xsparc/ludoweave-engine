# ADR-0010: Canonical snapshots, state hashes, and random streams

- **Status:** Accepted
- **Date:** 2026-08-05

## Context

Replay, save/load, optimistic commands, and deterministic debugging need one
portable representation of complete authoritative state. Entity/component
values alone are insufficient: allocator free-list order, generations, change
epochs, persistent resources, tick position, schema compatibility, and random
generator state all affect future behavior. Private dense-storage layout and
Python object identity must not become persistent contracts.

Restoring untrusted bytes directly into a live session would risk partial
mutation. Python's process-global `random` module also has implicit state and
does not provide composition-owned named streams with an engine-controlled
wire contract.

## Decision

Snapshots use the versioned `ludoweave.snapshot/1` wrapper and embed one
`ludoweave.authority/1` logical image. The wrapper records the exact engine
version and a `sha256:` digest over canonical authority bytes. Decode is
bounded before domain construction, rejects unknown wrapper/authority fields,
verifies the source digest, validates schema identities and versions, applies
only registered adjacent forward migrations, and reconstructs a new complete
session. Loading into an existing session adopts the candidate record only at
an ECS safe point after all decode, migration, validation, and reconstruction
work succeeds.

A codec may require an exact composition binding containing project-schema,
dependency-lock, and platform-profile identities. The data-only CLI always
uses this binding, so snapshots cannot cross selected project compositions even
when their world/seed and empty registries happen to match. Component manifest
`fields` describe the registered current decode-target contract; historical
row shapes are interpreted only by trusted registered migration chains.

The logical image preserves allocator slot generations, alive flags and exact
free-list order; world/table/row epochs; components; explicit `STATE`
resources; completed ticks; and deterministic random state. Runtime resources,
paths, clocks, presentation state, storage indexes, and backend/native objects
are excluded. Loading into an existing session preserves its classified
`INPUT` and `RUNTIME_EXCLUDED` values while replacing `STATE` values; decoding
into a new session leaves excluded values absent. Current-version round trips must reproduce the declared hash;
successful migrations intentionally produce a new current-version hash.

Engine-owned random state uses explicit unsigned 64-bit seeds and independently
derived named PCG32/1 streams. Stream names are stable bounded identifiers.
Seed, internal state, and increments are encoded as fixed-width lowercase
hexadecimal text so the unsigned 64-bit domain does not conflict with the
canonical JSON signed-integer domain. Named stream creation order cannot alter
another stream's sequence.

## Consequences

- Snapshot bytes are deterministic for one authority image and composition.
- Restore preserves future entity allocation, changed-query filtering, tick
  position, and future random outputs.
- A failed decode, compatibility check, migration, limit check, or active-query
  safe-point check leaves a destination session unchanged.
- Component migrations, resource migrations, and codecs are trusted local code;
  their external side effects cannot be rolled back.
- Exact engine-version compatibility is deliberately conservative in the
  pre-alpha protocol. Future compatibility widening requires a new decision.
- Snapshot size/count limits and correctness-first reconstruction may be
  expensive. Benchmark evidence may justify internal optimization without
  changing the public format.

## Alternatives considered

Pickle was rejected because it executes Python object reconstruction and is not
a safe, portable public protocol. Serializing dense/sparse tables directly was
rejected because private storage layout is not authority. Using the global
`random` module was rejected because its ownership and named-stream behavior
are implicit. Mutating a destination while decoding was rejected because a
late failure could expose partial state.
