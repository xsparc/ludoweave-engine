# RFC-0115: Add verified local asset cache publication

- **Status:** Accepted
- **Date:** 2026-08-26
- **Decision owners:** LudoWeave maintainers

## Context

M131 verifies and executes a complete asset plan but deliberately releases
decoded payloads without persistent side effects. Reuse now requires an
explicit storage authority, a durable format, independent action and payload
identities, verified reads, and failure behavior that cannot expose a partial
entry as a cache hit.

Current [Bazel remote-cache documentation](https://bazel.build/remote/caching)
separates an action cache from a content-addressable store (CAS), publishes new
outputs only after action execution, and warns that modified inputs can poison
a shared cache. The [Remote Execution API](https://github.com/bazelbuild/remote-apis/blob/main/build/bazel/remote/execution/v2/remote_execution.proto)
addresses CAS blobs by their own content, requires digest verification, and
requires referenced blobs to be available when an action result is returned.
Current [Gradle build-cache concepts](https://docs.gradle.org/current/userguide/build_cache_concepts.html)
require repeatable outputs and discrete non-overlapping ownership. Python
3.14 documents [`os.replace()`](https://docs.python.org/3.14/library/os.html#os.replace)
as the cross-platform replacement primitive when source and destination use
the same filesystem.

These sources support a local-only verified cache whose staging paths are
inside the destination filesystem. They do not justify remote cache transport,
shared write authority, automatic eviction, background maintenance, or
parallel execution.

## Decision

Add bounded materialization values to the focused asset execution contract:

- `AssetBuildArtifact` pairs one exact immutable decoded payload with its M131
  result entry;
- `AssetBuildMaterialization` pairs the complete M131 result with an exact
  plan-ordered artifact tuple; and
- `materialize_asset_build_plan()` retains payloads only after the same
  complete source preflight, decoder behavior, and aggregate limits as M131.

`execute_asset_build_plan()` retains its M131 behavior and result: it uses the
shared execution kernel without retaining payloads. Materialization is an
explicit separate authority boundary.

Add `AssetCacheStore` for one caller-selected local root. When a project root
is supplied, the cache root must be distinct and may be neither inside nor an
ancestor of the project. Existing cache roots and observed layout components
must be ordinary directories rather than symbolic links or reparse points.

The cache has two namespaces:

- `cas/HH/HASH` stores a decoded payload by its exact artifact SHA-256; and
- `actions/HH/CACHE_KEY/entry.json` stores canonical
  `ludoweave.asset-cache-entry/1` metadata by the existing M4/M129 action cache
  key and references the CAS identity, byte count, URI, kind, loader protocol,
  and source byte count.

Reads require the exact expected M131 result entry. Metadata bytes must be the
exact canonical document, the referenced blob must be a bounded ordinary
file, and both its length and SHA-256 must match. An absent action is a miss.
Any observed malformed, incomplete, aliased, or mismatched entry fails closed
as `asset_cache.corrupt_entry`; cache reads never repair or delete content.

## Atomic publication

Publication first writes and flushes a uniquely staged CAS blob beside its
final destination, then replaces the final blob name. It next writes and
flushes canonical action metadata inside a uniquely staged sibling directory;
atomic per-entry action-directory replacement is the visibility point. On
platforms that support directory synchronization, the relevant destination
directory is synchronized after replacement.

If an equivalent CAS blob or action entry already exists, it is completely
verified and reused without rewrite. A corrupt collision is never overwritten.
Every still-owned staging path is removed on success or failure. A filesystem
failure may leave an unreferenced but valid CAS blob after blob publication and
before action publication; a later retry reuses it. It cannot produce a cache
hit because the action entry is absent. Successfully published earlier entries
from a multi-entry plan also remain valid if a later independent entry fails.
M132 promises atomic entries, not an atomic all-plan transaction or crash-proof
filesystem durability beyond the documented flush/replacement sequence.

## CLI composition

Add:

```console
ludoweave source asset-cache PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE --cache DIRECTORY
```

The command completes the exact M130 verification chain, acquires and
revalidates detached sources, materializes every bounded M131 payload, and only
then constructs the explicit cache store and publishes. No cache path comes
from project data. Success is canonical
`ludoweave.asset-cache-publish/1`, containing plan identity, ordered logical
artifact identities, and `published` or `reused` status without cache paths.

## Ownership, failure, and determinism

The caller owns the cache-root authority. `AssetCacheStore` retains only the
resolved root and owns no open descriptor or background lifecycle. Individual
file and directory descriptors are lexical and closed before return. The
project remains read-only, and decoder or verification failure occurs before
cache-root creation in the CLI composition.

Stable inputs and an initially equivalent cache state produce the same payload
and metadata bytes. Publication status legitimately depends on prior cache
state; paths, timestamps, staging names, process identity, and environment
values never enter protocols or cache identities.

## Compatibility

All new focused-package exports and protocols are experimental and additive.
The engine root, package version, existing loader/cache-key identity, M128 lock,
M129 plan, M131 result, legacy M4 pipeline, dependencies, and workflows remain
unchanged.

## Non-scope

M132 has no remote cache, network transport, authentication, shared service,
download/upload protocol, cache eviction, garbage collection, deletion API,
repair, overwrite-on-corruption, size quota, watcher, discovery, automatic
reimport, scheduler, worker, process, thread, plugin, decoder registration,
renderer upload, world/session, command, transaction, world mutation, or
receipt. There is no project write, dependency, native code, engine-root API,
version, permission, credential, release authority, or CI change.
There is no CI change in this milestone.

## Consequences

- A verified plan can now materialize once and populate a reusable local
  action index plus deduplicated payload CAS.
- Cache hits are accepted only against an exact current expected result entry;
  existing legacy cache files do not become trusted automatically.
- Unreferenced valid CAS blobs are possible after interrupted publication and
  remain inert until a matching action entry exists.

## Revisit triggers

- Eviction or garbage collection requires explicit ownership, reachability,
  quotas, concurrent-reader behavior, and recoverable deletion policy.
- Remote caching requires authentication, authorization, transport bounds,
  poisoning defenses, trust domains, retry behavior, and separate opt-in
  write authority.
- Parallel publication requires deterministic error selection and evidence
  for collision behavior across supported filesystems.

## Rejected alternatives

- Store payload and metadata together under the action cache key. Rejected
  because it conflates output content identity with action identity and blocks
  CAS deduplication.
- Publish metadata before the payload. Rejected because a visible action could
  reference a missing blob.
- Rewrite corrupt collisions. Rejected because observed corruption may signal
  a collision, concurrent fault, or untrusted cache and must fail closed.
- Place the cache inside the project. Rejected because generated cache effects
  must not mutate source-controlled project state.
- Add remote cache support now. Rejected because transport and shared-writer
  trust are independent decisions.
