# RFC-0121: Add deterministic cache-observation fingerprint

- **Status:** Accepted
- **Date:** 2026-08-27
- **Decision owners:** LudoWeave maintainers

## Context

M137 verifies and classifies one complete engine-owned local cache, but its
public report intentionally exposes only aggregate counts and bytes. Equal
aggregate reports do not establish that the observed action metadata and CAS
identities were equal. Operators need a compact equality signal before any
future comparison, retention-root, or maintenance proposal can be judged.

Current [Bazel remote-cache documentation](https://bazel.build/remote/caching)
separates action metadata from CAS content and applies disk-cache garbage
collection through explicit size/age policy while idle. Current [Gradle cache
documentation](https://docs.gradle.org/current/userguide/directory_layout.html#dir:gradle_user_home)
uses managed unused-entry retention periods. Git's current [`git gc`
documentation](https://git-scm.com/docs/git-gc) protects referenced/recent
objects and still warns that concurrent writers can race pruning. These models
do not justify deletion from M137's sequential observation. They do support a
separate deterministic read-only identity over the already verified action/CAS
observation.

## Decision

Add `fingerprint_asset_cache_observation(plan, cache_root, *,
project_root=None, limits=...)`. It reuses exactly one M137 bounded verification
pass. No second enumeration, store, or content read occurs.

The function returns frozen path-free
`ludoweave.asset-cache-fingerprint/1` evidence containing:

- the complete nested M137 inventory for plan-relative aggregate context; and
- `observation_sha256`, a digest binding every verified action metadata record
  and CAS identity/size in the complete observed storage.

The observation digest is independent of the current plan. The nested
inventory remains plan-relative. Therefore two calls over equal cache storage
can have equal observation digests while reporting different current/missing/
other classifications for different plans.

## Fingerprint framing

The SHA-256 input starts with the ASCII fingerprint protocol followed by one
NUL byte. Verified action records are processed by cache key order. Each action
frame contains byte tag `A`, an unsigned eight-byte big-endian payload length,
and the exact canonical `ludoweave.asset-cache-entry/1` metadata bytes already
validated by M137.

Verified CAS records follow in artifact-digest order. Each CAS payload is the
32 raw SHA-256 bytes followed by its unsigned eight-byte big-endian content
length; it is framed with byte tag `C` and the same eight-byte length field.
Domain, record type, length, order, canonical metadata, digest, and byte count
are all bound without constructing an unbounded aggregate document.

## CLI composition

Add:

```console
ludoweave source asset-cache-fingerprint PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE --cache DIRECTORY
```

The command recomputes current source identities, verifies the saved lock and
exact regenerated plan, then runs the single read-only observation. It does not
acquire source payloads for decoding, construct a writable store, or invoke a
decoder.

## Ownership, failure, and determinism

M137 retains all authority, bounds, no-follow classification, canonical
metadata checks, streamed CAS verification, descriptor ownership, and failure
behavior. An absent cache remains absent and has the stable digest of the
domain prefix alone. Corruption or limits fail before a fingerprint report is
returned.

Stable verified storage produces the same observation digest regardless of
filesystem enumeration order, cache root path, or current plan. Any action
metadata identity, action membership, CAS digest, CAS size, or CAS membership
change alters the framed input. The report contains no URI, key, artifact
digest, filename, absolute path, payload, access time, age, or environment
value.

The pass is still a sequential observation, not an atomic filesystem snapshot.
It can bind exactly what the bounded verifier observed, but cannot prove that
all entries coexisted at one instant under a hostile concurrent writer.

## Observation is not deletion eligibility

Fingerprint equality is integrity evidence for two observed streams only. It
does not establish ownership, last use, leases, generations, retention roots,
quiescence, age, authorization, or deletion safety. A changed fingerprint does
not identify which object changed. An unchanged fingerprint is not deletion
eligibility for any unreferenced blob.

## Compatibility

The M137 inventory protocol and aggregate canonical bytes remain unchanged.
M132-M137 cache behavior stays protected. The focused export and CLI subcommand
are experimental and additive. The cache layout, engine root, dependencies,
version, workflows, permissions, and release authority remain unchanged. There
is no CI change.

## Non-scope

M138 has no write, publication, repair, deletion, eviction, garbage collection,
quota/age policy, retention root, lease, pin, generation, atomic snapshot,
diff, saved-fingerprint verifier, migration, remote cache, network,
authentication, signature, attestation, provenance, watcher, decoder, worker,
process, thread, parallelism, plugin, renderer upload, project write-back,
world/session, command, transaction, mutation, or receipt. It adds no
dependency, native/backend surface, engine-root API, version, workflow
allocation, permission, credential, release authority, or remote change.

## Consequences

- Operators gain compact exact equality evidence for complete verified cache
  observations without exposing cache identities.
- Fingerprint production retains M137's full-cache read cost and hard bounds.
- Plan-relative counts and plan-independent storage identity remain explicit
  rather than conflated.
- Cleanup policy and deletion authority remain deliberately deferred.
- CI remains unchanged; existing local validation exercises the new boundary.

## Revisit triggers

- Saved fingerprint verification requires a bounded strict decoder and an
  explicit statement of what equality does and does not prove.
- Retention planning requires explicit roots from every relevant project or
  generation, not inference from unreferenced counts.
- Deletion requires quiescence/lease guarantees, grace/age policy, crash
  recovery, rollback evidence, and cross-platform filesystem semantics.
- Remote fingerprints require authenticated transport, server-defined
  pagination/snapshot semantics, authorization, and retry contracts.

## Rejected alternatives

- Treat equal M137 counts as equal storage. Rejected because equal-size content
  substitution can preserve every aggregate.
- Emit the complete action and CAS identity list. Rejected because a compact
  digest supplies equality evidence without exposing cache contents.
- Add timestamps or use file modification time. Rejected because they are not
  deterministic identity and do not prove last use.
- Delete objects after fingerprinting. Rejected because exact observation
  identity grants no retention or mutation authority.
