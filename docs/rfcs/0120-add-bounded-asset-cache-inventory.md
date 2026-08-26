# RFC-0120: Add bounded read-only asset-cache inventory

- **Status:** Accepted
- **Date:** 2026-08-27
- **Decision owners:** LudoWeave maintainers

## Context

M132-M136 can publish, look up, realize, populate, and verify exact current-plan
cache entries. None describes the complete engine-owned `actions/` and `cas/`
storage at an explicit local cache root. Operators need deterministic bounded
integrity evidence before any future cache-maintenance proposal can be judged.

Current [Bazel remote-cache documentation](https://bazel.build/remote/caching)
separates action metadata from CAS outputs and treats disk-cache garbage
collection as a separate size/age policy. Current [Gradle cache-directory
documentation](https://docs.gradle.org/current/userguide/directory_layout.html#dir:gradle_user_home)
likewise separates versioned cache storage from managed cleanup policy. Python
3.12's [`os.scandir()` documentation](https://docs.python.org/3.12/library/os.html#os.scandir)
defines no-follow classification, filesystem errors, and Windows junction
behavior. These sources support a separate read-only inventory with explicit
bounds and no cleanup authority.

## Decision

Add `inspect_asset_cache_inventory(plan, cache_root, *, project_root=None,
limits=...)`. It opens the existing store with `writable=False` and scans only
the engine-owned top-level `actions/` and `cas/` namespaces.

The tightening-only hard maxima are 16,384 actions, 16,384 CAS blobs, 64 MiB of
canonical action metadata, and 1,073,741,832 CAS bytes (the existing maximum
valid single artifact). Enumeration is incremental; entries are never collected
without a small fixed bound or running action/blob limit. Aggregate byte budgets
are checked from no-follow metadata before file open and again while reading.

Every namespace, shard, action directory, metadata file, and CAS file must be
ordinary and non-reparse. Shard/digest names must be lowercase hexadecimal and
prefix-consistent. Every action record must be strict duplicate-free exact-
field canonical JSON reconstructing `AssetBuildResultEntry`; its cache key must
equal its location. Every CAS blob is streamed and SHA-256 checked against its
name once. Every action reference must resolve to a same-sized blob.

The exact current plan classifies action keys and their unique CAS identities.
A current action must also match URI, kind, and source byte count. Other valid
actions and blobs are exposed only as aggregate counts and bytes.

## Result contract

Frozen path-free `ludoweave.asset-cache-inventory/1` evidence contains the plan
SHA-256; current/missing/other action counts and metadata bytes; total/current/
other CAS counts and bytes; and counts/bytes for CAS blobs with no action
reference observed by this scan. It emits no URI, cache key, artifact hash,
filename, absolute path, payload, access time, or age.

## CLI composition

Add:

```console
ludoweave source asset-cache-inventory PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE --cache DIRECTORY
```

The command recomputes current source identities, verifies the saved lock and
exact regenerated plan, then inventories the explicit external cache. It does
not reacquire source payloads for decoding, construct a writable store, or
invoke a decoder.

## Ownership, failure, and determinism

The caller owns the explicit cache location. The inventory owns only temporary
read descriptors and closes each before continuing. It creates no root,
directory, file, worker, thread, or background lifecycle.

An absent cache is a valid empty observation and remains absent. Unexpected
layout, reparse objects, ambiguous/noncanonical metadata, digest mismatch,
missing referenced blobs, current-plan mismatch, limit excess, and observed
size changes fail with path/content-silent structured errors. Nothing is
repaired or deleted.

Stable plan and cache bytes produce the same canonical result regardless of
enumeration order. The scan is sequential, not an atomic filesystem snapshot.
Detected size drift fails, but hostile concurrent replacement can still race
no-follow checks and reads; snapshot consistency is not claimed.

## Observation is not deletion eligibility

`unreferenced_blobs` means only that no decoded action record in this bounded
scan referenced those CAS identities. It is not deletion eligibility: a
concurrent or future publisher may need a blob, another process may hold an
older observation, and the scan has no lease, generation, last-use time,
retention policy, or transaction. M137 adds no deletion recommendation.

## Compatibility

M132 publication, M133 lookup, M134 realization, M135 population, and M136
saved-population verification remain unchanged and protected. Focused exports
and the CLI subcommand are experimental and additive. The engine root, cache
layout/protocols, dependencies, version, workflows, permissions, and release
authority remain unchanged. There is no CI change.

## Non-scope

M137 has no write, publication, repair, deletion, eviction, garbage collection,
quota enforcement, age/access-time policy, lease, pin, generation, atomic
snapshot, migration, remote cache, network, authentication, signature,
attestation, provenance, watcher, decoder, worker, process, thread, parallelism,
plugin, renderer upload, project write-back, world/session, command,
transaction, mutation, or receipt. It adds no dependency, native/backend
surface, engine-root API, version, workflow allocation, permission, credential,
release authority, or remote change.

## Consequences

- Operators gain bounded whole-cache integrity and storage classification
  without mutation.
- Corrupt data outside the current plan now fails complete inventory.
- Every admitted CAS byte is read and hashed, so inventory may be deliberately
  more expensive than current-plan lookup.
- Blobs with no observed action reference are diagnostic evidence only, not
  deletion candidates.
- CI remains unchanged; existing local validation exercises the new boundary.

## Revisit triggers

- Deletion requires leases or immutable generations, retention policy,
  concurrent-reader/writer guarantees, crash recovery, and rollback evidence.
- Larger caches require benchmark evidence and a separately reviewed way to
  raise budgets without weakening denial-of-service bounds.
- Atomic inventory requires supported-filesystem snapshot or descriptor-pinning
  evidence across Windows, macOS, and Linux.
- Remote inventory requires authenticated transport and server-defined
  pagination, integrity, authorization, and retry contracts.

## Rejected alternatives

- Delete unreferenced blobs during inventory. Rejected because one sequential
  observation supplies no safe deletion authority.
- Trust filenames without reading content. Rejected because that would be
  layout enumeration rather than integrity evidence.
- Emit per-entry keys or hashes. Rejected because aggregate path-free evidence
  is sufficient and avoids exposing cache contents.
- Follow symlinks or junctions. Rejected because the cache root must not grant
  authority outside the engine-owned ordinary layout.
