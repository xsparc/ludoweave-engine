# RFC-0126: Add a path-free unreferenced-blob preview

- **Status:** Accepted
- **Date:** 2026-08-27
- **Decision owners:** LudoWeave maintainers

## Context

M137 identifies blobs with no action-metadata reference during one bounded,
verified, sequential cache observation. M138 binds that complete observation by
digest. Operators can inspect the larger inventory or fingerprint documents,
but there is no small contract explicitly framed as a read-only preview rather
than deletion eligibility.

Current cache-management systems require materially more authority before
mutation. [Bazel](https://bazel.build/remote/caching) supports disk-cache age
and size bounds. [Gradle 9.7.1](https://docs.gradle.org/current/userguide/directory_layout.html)
uses category-specific last-use retention. [BuildKit](https://docs.docker.com/build/cache/garbage-collection/)
orders policies by resource type, age, sharing, and storage thresholds. These
inputs do not exist in the LudoWeave cache format.

[CNCF Distribution](https://distribution.github.io/distribution/about/garbage-collection/)
describes mark-and-sweep, provides a dry run, and requires read-only or stopped
writers to avoid deleting newly uploaded content. [Git](https://git-scm.com/docs/git-gc.html)
retains reference roots and a grace period while warning that concurrent
immediate pruning can corrupt a repository. LudoWeave has no cross-process
quiescence, retention-root registry, grace policy, leases, pins, or generations.

The safe incremental capability is therefore a minimized observation report,
not cleanup. OpenTelemetry's
[data-minimization guidance](https://opentelemetry.io/docs/security/handling-sensitive-data/)
supports publishing aggregates when they serve the diagnostic purpose. M143
can reuse existing M137 aggregates and M138 observation identity without
listing candidate objects.

## Decision

Add frozen
`ludoweave.asset-cache-unreferenced-preview/1` and a pure function:

```python
preview_asset_cache_unreferenced_blobs(plan, fingerprint)
```

The function requires exact `AssetBuildPlan` and `AssetCacheFingerprint`
values, recomputes the exact plan digest, requires the fingerprint's nested
inventory to bind that plan, and copies only existing verified evidence into a
new immutable value.

The canonical report contains:

- `status: "observed"`;
- inventory and fingerprint protocol identifiers;
- exact plan and complete-observation SHA-256 values; and
- `unreferenced_blobs` plus `unreferenced_blob_bytes`.

It contains no candidate digest, action/cache key, URI, artifact identity,
filename, path, payload, timestamp, age, or policy. The observation digest
binds the complete already-public M138 cache observation; it is not a candidate
list or an authenticity statement.

## CLI composition

Add:

```console
ludoweave source asset-cache-unreferenced-preview PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE --cache CACHE
```

The command verifies current source identities, the saved source lock, and the
exact regenerated plan before resolving or observing the cache. It then invokes
the unchanged M138 bounded read-only fingerprint operation exactly once and
passes the frozen result to the pure M143 function.

An absent cache produces a zero preview without creating it. A valid preview
with a nonzero count still exits 0: the count is an observation, not a warning,
failure, deletion candidate approval, or mutation request. Invalid processing
remains structured standard error with exit 2.

## Safety and ownership boundary

“Unreferenced” means only that no admitted action metadata in one sequential
verified observation names the blob. A writer might have published the CAS
blob before publishing its action entry. Another project, process, generation,
or future plan might still require it. M143 does not determine last use,
importance, regenerability, sharing, retention, or deletion eligibility.

The pure function has no filesystem, cache, source, environment, clock,
process, thread, or network access and mutates no input. The CLI owns one
read-only observation. It does not create, lock, write, rename, repair, delete,
evict, sweep, compact, or otherwise mutate cache or project state.

## Determinism and failure

The unchanged M138 operation verifies canonical action metadata, action/blob
references, CAS content digests, bounded collection sizes and bytes, sorted
observation order, and no-follow filesystem rules. Exact plan binding completes
before a preview is constructed. Any mismatch or corrupt observation fails
without partial success.

Identical admitted plan and fingerprint values produce identical canonical
preview bytes on every supported platform. This remains evidence for one
sequential observation, not an atomic snapshot or concurrency guarantee.

## Compatibility and CI

M137 inventory, M138 fingerprint, M139 verification, M140 comparison, M141
offline comparison, and M142 saved-comparison verification protocols and bytes
remain unchanged. Cache layout, dependencies, package version, workflows,
permissions, release authority, and engine-root APIs remain unchanged.

The existing quota-conscious trusted-base CI already qualifies substantive
Python and installed-wheel changes. M143 adds no workflow job or allocation.
There is no CI change.

## Non-scope

M143 adds no candidate list, object identity disclosure, detailed diff, saved
preview decoder, record store, filename, write-back, last-access tracking,
timestamp, age/grace policy, quota or size policy, retained-root registry,
lease, pin, generation, quiescence, lock, atomic snapshot, cleanup, garbage
collection, prune, repair, deletion, eviction, compaction, rollback, remote
cache, authentication, signature, attestation, provenance, network, watcher,
scheduler, worker, process, thread, parallelism, plugin, renderer upload,
project/world mutation, command receipt, dependency, native/backend surface,
version, workflow allocation, permission, credential, release, publication, or
remote change.

## Consequences

- Operators receive a stable small report for existing path-free
  unreferenced-blob aggregates.
- The report can detect an exact observation substitution through M138 identity
  without exposing individual candidates.
- Nonzero counts do not confer deletion authority.
- Future cleanup work still requires explicit roots, grace/age policy,
  quiescence or locking, rescan semantics, crash recovery, and adversarial
  concurrency evidence.
- Hosted CI allocation remains unchanged.

## Revisit triggers

- A cleanup preview with concrete candidates requires a separate disclosure
  review and a retained-root design.
- Any mutation requires quiescence/locking, grace/age, crash-recovery, and
  revalidation semantics.
- Remote-cache work requires an authenticated transport and server lifecycle
  design independent of this local report.
