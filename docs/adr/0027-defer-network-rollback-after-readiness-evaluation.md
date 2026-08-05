# ADR-0027: defer network rollback after readiness evaluation

- Status: Accepted
- Date: 2026-08-06

## Context

The post-alpha sequence permits exploring rollback/network snapshots only
after deterministic replay is mature. LudoWeave already has canonical complete
authority snapshots, exact state hashes, self-contained transaction timelines,
verified checkpoints, exact composition bindings, and immutable
parent-referenced replay branches. Those contracts justify a bounded readiness
evaluation, not an assumption that multiplayer or live rollback is ready.

Clockwork Arena exposes the decisive gap. Each replay batch records a
`world.tick` transaction, but the action snapshot used by its application-owned
tick executor is not embedded in the transaction or replay. Reproduction works
only when the caller separately injects an equivalent `RecordedInputSource`.
That ambient dependency is unsuitable as the canonical correction history for
peers.

The repository also has no authority/peer model, full/delta snapshot protocol,
correction window, acknowledgement and reorder semantics, transport security,
abuse limits, simulated network conformance, or rollback resource budget.
Existing local stdio MCP is explicitly not a network transport and must not be
repurposed as one.

## Decision

Admit one dependency-free, offline readiness proof and defer network rollback.
`examples/rollback_readiness.py` records and verifies a bounded Clockwork Arena
parent, branches at an exact tick with corrected future inputs, replays the
child twice, proves its final state differs without changing parent lineage,
and demonstrates that omitting external input rehydration causes replay
divergence. It emits sanitized `ludoweave.evaluation.rollback-readiness/1`
evidence; repository tooling strictly validates that evidence and cannot
report a transport as implemented.

Do not add sockets, listeners, remote attach, peer identities, a replication
store, a live rollback service, background mutation, transport dependencies,
or public network types. The ECS/world session remains the sole canonical
authority. Existing snapshot and replay formats remain unchanged.

A future assigned networking proposal must satisfy every gate below:

1. replay-owned canonical tick input history rather than ambient executor
   state;
2. explicit authority, peer, prediction, correction, and reconciliation
   ownership;
3. bounded versioned full/delta snapshot and input envelopes with chunk
   integrity and compatibility negotiation;
4. exact tick windows, sequencing, acknowledgements, duplicates, loss,
   reordering, and late-input behavior;
5. authentication, encryption, replay protection, rate/work/size quotas, and
   sanitized failures before a listener exists;
6. same-build cross-platform determinism and repeatable loss/latency/reorder/
   malicious-input simulations;
7. measured worst-case rollback CPU, memory, and catch-up targets across the
   supported matrix; and
8. explicit single-owner lifecycle/thread/close/recovery rules, installed
   artifact conformance, and a named maintainer.

## Consequences

- The existing immutable branch API gains source, wheel, and release-bundle
  evidence without a new runtime abstraction or compatibility promise.
- The evidence records canonical byte sizes as informational counts, not
  bandwidth or performance claims.
- M13 identifies canonical input history as the first technical prerequisite
  for rollback while leaving the persistent formats unchanged.
- Networking, multiplayer replication, live rollback, and remote agent
  transports remain unimplemented.
- Future work must supersede this ADR rather than interpreting a successful
  local branch proof as transport authorization.
