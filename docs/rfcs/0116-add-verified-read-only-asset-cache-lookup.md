# RFC-0116: Add verified read-only asset cache lookup

- **Status:** Accepted
- **Date:** 2026-08-26
- **Decision owners:** LudoWeave maintainers

## Context

M132 can publish and revalidate a result only when the caller already holds its
exact decoded result identity. Cache-assisted execution will eventually need a
different lookup boundary: start with the stable action key in a current
verified plan, decode untrusted action metadata, and decide whether the
referenced payload is a verified hit or an exact miss.

Current [Bazel remote-cache documentation](https://bazel.build/remote/caching)
describes the action cache as a map from action hashes to result metadata and
the CAS as separate output storage. It looks up outputs after constructing the
required action graph and treats absent outputs as misses. Current
[Gradle build-cache documentation](https://docs.gradle.org/current/userguide/build_cache.html)
similarly derives a key from complete task inputs, uses it to request prior
outputs, and permits read and write behavior to be controlled independently.
Python's [`json` documentation](https://docs.python.org/3/library/json.html)
warns that untrusted JSON should be size-bounded and that duplicate object
names are otherwise accepted by default.

These sources support a bounded read-only lookup keyed only by exact current
plan entries. They do not establish cache authenticity, authorize a decode
shortcut, justify enumeration of unrelated cache entries, or justify remote
transport, repair, deletion, eviction, or parallel access.

## Decision

Extend `AssetCacheStore` with explicit authority:

- `writable=True` retains M132's creating and publishing behavior;
- `writable=False` never creates the root and rejects `publish()` as
  `asset_cache.read_only`; and
- both modes reject cache roots equal to, inside, or containing the project.

Add `load_action(AssetBuildPlanEntry)`. Lookup derives only the existing action
path from the exact M129 cache key. An absent action directory is a miss even
if an unreferenced CAS blob exists. A present action must have exactly one
ordinary `entry.json` file within the M132 byte bound.

Metadata parsing uses strict UTF-8, rejects duplicate object names and
non-finite constants, requires exactly the M132 field set, and reconstructs a
validated `AssetBuildResultEntry`. The original bytes must equal the canonical
encoding. URI, kind, cache key, and source byte count must match the current
plan entry; source hash, settings, dependencies, and loader protocol are
already inputs to that plan-validated cache key. The referenced ordinary CAS
file must then match its declared bounded byte count and SHA-256. Any present
malformed, aliased, mismatched, unreadable, or incomplete entry fails closed as
`asset_cache.corrupt_entry`; corruption is never downgraded to a miss.

Add `inspect(AssetBuildPlan)` and immutable
`ludoweave.asset-cache-lookup/1` summaries. Entries remain in canonical plan
order and report logical URI, action key, `hit` or `miss`, and artifact identity
only for verified hits. Counts and bytes are path-free and deterministic for a
stable plan and cache state.

## CLI composition

Add:

```console
ludoweave source asset-cache-check PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE --cache DIRECTORY
```

The command loads and verifies the saved lock, recomputes current source
identities, regenerates and verifies the current plan, then opens the explicit
cache with `writable=False` and inspects only that plan. A missing cache root
produces plan-ordered misses without creating it. Success writes one canonical
lookup document to stdout; failure writes no success bytes.

## Trust, ownership, and determinism

The caller owns the local cache-root authority. Digest verification proves
internal content integrity, not provenance, authenticity, authorization, or
freedom from a malicious self-consistent action mapping. M133 is intended for
a caller-controlled local cache under the exact loader/action-key contract.

The store retains a resolved path but no open descriptor or background
lifecycle. Inspection writes neither cache nor project data and does not update
access times intentionally; filesystem-level read access-time behavior is not
part of the protocol. Concurrent hostile replacement is outside this local
single-caller boundary and would require a separately designed snapshot or
descriptor-pinning policy.

## Compatibility

M132 construction remains source-compatible because write authority defaults
to `True`. Existing `load()` and `publish()` protocols and behavior are
unchanged. New focused-package exports are experimental and additive. The
engine root, loader/cache-key identity, plan/result/publication protocols,
dependencies, version, and workflows remain unchanged.

## Non-scope

M133 has no cache-assisted execution, decoder bypass, materialization from
mixed hits, cache publication through the new command, remote cache, network,
authentication, shared service, eviction, deletion, repair, quota, discovery,
enumeration, watcher, reimport, scheduler, worker, process, thread, plugin,
renderer upload, project write, world/session, mutation, or receipt. It adds no
dependency, native code, engine-root API, version, workflow, permission,
credential, release authority, or CI change. There is no CI change.

## Consequences

- Current plans can now obtain independent verified hit/miss evidence without
  creating or changing a cache.
- Present corruption is visible and actionable instead of silently causing
  expensive re-execution or repair.
- The verified `AssetBuildArtifact` returned by `load_action()` is a bounded
  foundation for a later separately reviewed cache-assisted execution slice.

## Revisit triggers

- Cache-assisted execution must define all-hit, mixed-hit, decoder-failure,
  result-order, and publication behavior without weakening current preflight.
- Concurrent readers/writers require supported-filesystem evidence and a
  precise snapshot or descriptor lifetime.
- Remote use requires authentication, authorization, poisoning defenses,
  transport bounds, retry policy, and separate read/write authority.

## Rejected alternatives

- Treat corrupt entries as misses. Rejected because it hides integrity faults
  and makes evidence dependent on an implicit repair/re-execution policy.
- Trust decoded metadata without matching plan-known fields. Rejected because
  a path collision must not redefine the requested action.
- Enumerate the cache to produce a report. Rejected because unrelated entries,
  directory order, and cache history are outside the explicit current plan.
- Add cache-assisted execution in the same slice. Rejected because strict
  lookup needs independent behavior and installed-artifact evidence first.
