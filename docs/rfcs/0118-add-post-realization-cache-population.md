# RFC-0118: Add explicit post-realization cache population

- **Status:** Accepted
- **Date:** 2026-08-27
- **Decision owners:** LudoWeave maintainers

## Context

M132 can publish a complete uncached materialization, M133 can inspect verified
cache entries without write authority, and M134 can combine verified hits with
decoded misses into one complete in-memory materialization. M134 deliberately
does not publish. The next narrow step is an explicit operation that reuses
M134 and obtains write authority only after complete realization succeeds.

Current [Bazel remote-cache documentation](https://bazel.build/remote/caching)
describes a sequence of declared actions, local/cache lookup, local execution
for misses, and upload of new outputs. It also provides a read-only mode by
disabling upload. Current [Gradle build-cache documentation](https://docs.gradle.org/current/userguide/build_cache.html)
separates cache enablement from its `push` authority, disables remote pushing
by default, and requires a complete picture of task inputs and outputs for safe
reuse. These sources support a deliberate boundary between lookup/realization
and publication. They do not establish an all-plan transaction, rollback,
remote transport, hostile-concurrency safety, repair, or eviction.

## Decision

Add `populate_asset_build_cache(plan, inputs, cache_root, *, project_root=None,
limits=...)`. The caller supplies the exact current plan, detached inputs, an
explicit local cache path, optional project confinement, and optionally
tightened M131 limits.

The operation performs these phases in order:

1. Open the explicit cache root through `AssetCacheStore(..., writable=False)`.
   A missing root remains absent. Existing root and project-separation rules
   are checked without granting write authority.
2. Complete M134 realization. The whole source tuple is preflighted, every
   current-plan cache candidate is verified, exact misses are decoded, and all
   active bounds pass before the operation continues.
3. Only after complete realization, open that resolved explicit root through
   `AssetCacheStore(..., writable=True)` and pass the complete materialization
   to the unchanged M132 `publish()` implementation.
4. Return immutable combined evidence only after publication returns a
   complete summary.

Add frozen `AssetCachePopulationEntry` and `AssetCachePopulation` values under
`ludoweave.asset-cache-population/1`. Each plan-ordered entry records the
existing logical result identity, `hit` or `decoded` realization status, and
`published` or `reused` publication status. Aggregate counts and byte totals
are path-free. Payloads, cache paths, timestamps, environment values, and
unrelated cache history are excluded.

## CLI composition

Add:

```console
ludoweave source asset-cache-populate PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE --cache DIRECTORY
```

The command verifies the saved source lock against current sources, regenerates
and verifies the exact saved plan, and acquires every project-confined detached
source before calling the population operation. The command does not hold or
duplicate cache-write mechanics. Success writes one canonical population
report to stdout; failure writes no success document.

The existing `source asset-cache` command remains the explicit all-decode then
publish path. The existing `source asset-realize` command remains read-only.
Neither changes behavior.

## Ownership, failure, and atomicity

The caller owns selection of the external cache root. Project composition owns
bounded source acquisition. The population operation owns only its temporary
read-only and writable store values and immutable in-memory realization; those
stores own no persistent descriptor, worker, thread, or background lifecycle.

Source, plan, lookup, corruption, decoder, or limit failure occurs before
write authority is acquired. An absent cache therefore remains absent on those
paths. A cache can change between the read-only and write phases because the
store retains a resolved path, not a pinned directory descriptor or snapshot.
The unchanged M132 publisher re-verifies an existing entry and fails closed on
corruption.

Publication is atomic per entry, not transactional across the entire plan. A
later storage failure returns the original structured M132 error and no M135
success report, but earlier valid action entries or valid unreferenced CAS
blobs may remain. M135 provides no rollback and makes no all-or-nothing cache-
root claim.

## Determinism and trust

Stable plan, source bytes, initial cache contents, limits, and supported local
filesystem behavior produce the same artifacts and canonical population
report. Cache state intentionally affects the hit/decoded and published/reused
evidence; the materialized artifact identities remain those of M131/M134.

Digest verification establishes integrity of the observed local mapping, not
origin or authenticity of malicious self-consistent cache content. Sequential
single-caller use remains the supported model. Hostile concurrent replacement,
shared-writer coordination, filesystem snapshots, and cross-filesystem
transactionality are not claimed.

## Compatibility

M131 execution, M132 publication, M133 lookup, and M134 read-only realization
remain unchanged and independently protected. The new focused-package exports
and CLI subcommand are experimental and additive. The engine root, loader and
cache-key identities, dependencies, version, workflows, permissions, and
release authority remain unchanged. There is no CI change.

## Non-scope

M135 has no automatic write during `asset-realize`, cache repair/deletion/
eviction/garbage collection/quota/migration, remote cache, networking,
authentication, authorization, discovery, enumeration, watcher, reimport,
worker, scheduler, process, thread, parallelism, plugin or decoder
registration, renderer upload, source/project write-back, world/session,
command, transaction, mutation, or receipt. It adds no dependency, native
code, backend object, engine-root API, version, workflow job/allocation,
permission, credential, release authority, or remote change.

## Consequences

- A cold explicit population decodes all required artifacts before creating
  the cache root, then publishes them through the existing per-entry protocol.
- A warm explicit population verifies and reuses all hits without decoder work.
- Mixed populations decode only misses while preserving exact plan order.
- Failures before publication cannot leave cache writes; publication failures
  retain M132's documented valid-prefix/orphan possibility.
- Read and write authority are visible as separate construction points and are
  guarded by an architecture test.

## Revisit triggers

- All-plan atomic publication requires a separate generation/index/commit
  protocol and recovery semantics.
- Concurrent writers require supported-filesystem evidence and a precise
  synchronization or immutable-generation policy.
- Remote use requires separate credentials, authentication, authorization,
  poisoning defenses, transport bounds, retry semantics, and observability.
- Repair, eviction, quota, and garbage collection require explicit ownership
  and protection against deleting entries used by other callers.

## Rejected alternatives

- Make M134 publish misses automatically. Rejected because a read-only command
  must not gain an implicit filesystem effect.
- Open the cache writable before realization. Rejected because decoder, source,
  cache-integrity, or limit failure would acquire unnecessary write authority
  and could create an empty cache root.
- Republish each decoded miss immediately. Rejected because later corruption
  or decoder failure would create avoidable partial effects before complete
  realization.
- Add an all-plan rollback claim around M132. Rejected because the existing
  content-addressed per-entry publisher intentionally does not provide that
  transaction.
