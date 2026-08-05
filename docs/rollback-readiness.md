# Rollback and network-snapshot readiness

M13 evaluates the existing snapshot/replay machinery; it does not implement
multiplayer, rollback netcode, remote authority, or a network transport.

The dependency-free proof records a Clockwork Arena parent replay, branches at
an exact completed-tick boundary, applies a different future input stream, and
replays the corrected child twice while verifying the immutable parent
timeline hash and boundary state hash:

```console
python examples/rollback_readiness.py --ticks 120 --branch-tick 60
python examples/rollback_readiness.py --ticks 120 --branch-tick 60 --output rollback-readiness.json
python scripts/validate_rollback_readiness.py rollback-readiness.json
```

The example is bounded to 600 ticks. Its versioned JSON contains only work
counts, canonical byte sizes, hashes, Boolean admission gates, the engine
version, and a deferred decision. It has no timing, path, host, environment,
peer, socket, credential, or provider fields. The validator requires the exact
schema, rejects unknown fields and false local-proof claims, and specifically
rejects any claim that a transport was implemented.

## What the proof establishes

- Complete authority snapshots reproduce the exact branch boundary.
- Parent and child timelines have canonical hashes and immutable lineage.
- A corrected future input stream can be resimulated locally and repeatedly.
- A correction changes the final authority hash without mutating the parent.
- Source, isolated-wheel, and release-bundle compositions can run the proof
  headlessly with no additional dependency.

This is offline evidence over one single-owner composition. It is not a
runtime rollback service, performance target, cross-machine compatibility
claim, or network protocol.

## Why admission is deferred

`world.tick` replay batches do not contain the action snapshot consumed by the
application-owned tick executor. Replaying Clockwork Arena therefore requires
the caller to inject an equivalent `RecordedInputSource`; using an empty input
source produces verified replay divergence. A network correction protocol
cannot rely on ambient caller state for canonical input history.

No current contract defines full-versus-delta snapshot cadence, correction
windows, peer/authority ownership, tick sequence and acknowledgement rules,
loss/reordering behavior, chunk integrity, compatibility negotiation,
authentication, encryption, replay-attack resistance, abuse quotas, or
rollback CPU/memory limits. Full snapshots also retain exact composition
compatibility requirements. These omissions are deliberate and are recorded
in [ADR-0027](adr/0027-defer-network-rollback-after-readiness-evaluation.md).

## Revisit gate

A future assigned proposal must provide all of the following before any
network listener or supported live-rollback API is admitted:

1. canonical tick input embedded in or content-addressed by the replay format;
2. an explicit single authority/peer ownership and reconciliation model;
3. bounded versioned full/delta snapshot and correction envelopes with chunk
   integrity and compatibility rules;
4. exact tick window, sequence, acknowledgement, duplicate, reorder, drop, and
   late-input semantics;
5. authenticated and encrypted transport, replay protection, rate/work/size
   quotas, and sanitized failure behavior;
6. same-build cross-platform determinism plus repeatable loss, latency,
   reordering, and malicious-input simulations;
7. measured worst-case rollback CPU, memory, and catch-up targets on the
   supported matrix; and
8. explicit lifecycle, thread, close, failure recovery, maintenance ownership,
   and installed-artifact conformance.

Until a proposal satisfies every gate, networking and remote authority remain
out of scope.
