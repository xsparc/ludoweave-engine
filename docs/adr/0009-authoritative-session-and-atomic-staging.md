# ADR-0009: Authoritative session ownership and atomic clone staging

- **Status:** Accepted
- **Date:** 2026-08-05

## Context

M1 `World.clone()` and `ResourceStore.clone()` provide independent in-memory
state, but application ownership is split across a world, resources, and tick
counter. Applying persistent operations directly to those live objects would
allow an invalid middle command or system failure to leave a partial commit.
Hashing live entities alone is also insufficient: allocator generations,
free-list order, and change epochs affect future deterministic behavior.

`ResourceSpec.deterministic` describes scheduler eligibility, not persistence.
It provides no stable type ID, schema version, codec identity, or canonical
encoder/decoder. M1 tick execution is explicitly nontransactional and cannot
be called against live state by an M2 transaction.

## Decision

`WorldSession` is the single-owner authority aggregate for persistent
transactions. Construction transfers ownership of its `WorldStore`,
`ResourceStore`, stable world ID, completed-tick count, explicit authoritative
resource registry, and optional staged `TickExecutor`. Public session accessors
return detached world, resource, and random copies. They support inspection
without exposing canonical mutable objects or permitting receipt-less
mutation. Engine-owned services use private session/checkpoint ports to stage
and adopt one complete record.

The session's logical image includes allocator generations, alive flags and
exact free-list order; world, structural, table, and row epochs; canonical
authoritative components; explicit authoritative resource values; completed
ticks; and schema/codec compatibility metadata. Dense rows, sparse indexes,
Python object identities, presentation resources, paths, backend objects, and
wall-clock state are absent. M2 uses standard-library SHA-256 over canonical
logical-image bytes.

Every registered session resource requires exactly one
`AuthorityResourceSchema` with a nonzero
UUID, positive version, stable codec ID, exact M1 `ResourceSpec`, role, and
trusted encoder/decoder. Only `STATE` resources are hashed and eligible for
`resource.patch`. `INPUT` and `RUNTIME_EXCLUDED` roles do not become
authoritative merely because an M1 resource is deterministic-eligible.

Transaction application is serial and constructing-thread-owned:

1. Enforce transaction identity, byte/count limits, world target, and expected
   SHA-256 pre-hash.
2. Decode and schema-validate every operation before cloning.
3. Clone the complete session record.
4. Apply operations only to that staged record in command order.
5. Hash the complete staged result.
6. For dry-run, discard it. For commit, adopt it with one non-raising pointer
   assignment.

No failure path adopts the staged record. `world.tick` advances exactly one
tick, may appear at most once, must be final, and runs only through an injected
executor against staged world and resources. M2 rejects persistent ticks when
the session contains `INPUT` or `RUNTIME_EXCLUDED` resources; recorded input is
assigned to M4. Without the executor seam it fails as nontransactional. The executor is
defined in the lower world layer and implemented by an application adapter;
the world protocol does not import the application runtime.

## Consequences

- A stale hash rejects before resource decoders or staging callbacks run.
- Failed middle operations, tick failures, dry-runs, and even propagated
  `BaseException` control flow do not change the live authority record.
- Public detached views remain independent of later commits and cannot mutate
  the session's current authority record.
- Full clone/diff/hash work is a correctness-first bounded implementation and
  may be expensive; M2 benchmark evidence will guide later optimization.
- Migration functions, resource codecs/copiers, and tick systems are trusted
  deterministic Python code. External I/O, global mutation, retained aliases,
  or other side effects they perform cannot be rolled back by swapping the
  authoritative record and violate their contract.
- M1 local command buffers remain process-local tick internals and never enter
  persistent operation arguments.

## Alternatives considered

Direct mutation plus inverse commands was rejected because inverse behavior is
operation-specific and can fail. Replacing only the world while mutating live
resources/ticks was rejected as a partial transaction. Treating every
deterministic M1 resource as serializable was rejected because copying and
canonical persistence are different contracts.
