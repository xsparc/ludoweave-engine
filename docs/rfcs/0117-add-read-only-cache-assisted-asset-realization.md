# RFC-0117: Add read-only cache-assisted asset realization

- **Status:** Accepted
- **Date:** 2026-08-27
- **Decision owners:** LudoWeave maintainers

## Context

M131 can materialize every planned artifact with bounded built-in decoders.
M132 can explicitly publish that complete materialization. M133 can obtain
verified current-plan cache hits and exact misses without decoder or write
authority. The next narrow step is to reuse those verified hits while retaining
M131's complete detached-input validation, deterministic output, and limits.

Current [Bazel remote-cache documentation](https://bazel.build/remote/caching)
describes building the required action list, checking caches, executing missing
actions, and optionally uploading new outputs as distinct phases. Current
[Gradle build-cache documentation](https://docs.gradle.org/current/userguide/build_cache.html)
requires a complete picture of stable task inputs for safe output reuse and
allows cache reading to be enabled while writing is disabled. These sources
support a read-only hit/decode-miss composition. They do not justify trusting a
cache hit without verification, publishing misses automatically, remote
transport, concurrency, eviction, repair, discovery, or a new decoder/plugin
surface.

## Decision

Add `realize_asset_build_plan(plan, inputs, cache, *, limits=...)`. The caller
supplies an exact current `AssetBuildPlan`, its exact detached input tuple, one
explicit `AssetCacheStore`, and optionally tightened M131 execution limits.

The operation has three ordered phases:

1. Validate the complete input tuple for exact plan order, source byte counts,
   source SHA-256 values, and per-entry and aggregate source limits. Failure
   occurs before any action lookup or decoder call.
2. Resolve every plan entry through M133 `load_action()`. Every present entry
   must pass canonical action metadata, plan-field, CAS byte-count, and payload
   SHA-256 verification. Every verified hit must also pass the active per-entry
   and aggregate artifact limits. Failure occurs before any miss decoder call.
3. Decode only exact misses with the unchanged built-in decoder kernel. Apply
   the same artifact limits, merge hits and decoded artifacts in exact plan
   order, and return one immutable materialization.

Add frozen `AssetBuildRealizationEntry` and `AssetBuildRealization` values under
`ludoweave.asset-build-realization/1`. Each entry contains the existing logical
result identity plus exact `hit` or `decoded` status. The report includes
aggregate hit/decoded counts, source and artifact byte counts, loader protocol,
and plan hash. It excludes payloads, filesystem paths, timestamps, environment
values, and unrelated cache history.

## CLI composition

Add:

```console
ludoweave source asset-realize PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE --cache DIRECTORY
```

The command verifies the saved lock against current sources, recomputes and
verifies the saved plan, acquires all project-confined detached inputs, opens
the caller-selected cache with `writable=False`, realizes the plan, and writes
one canonical report to stdout. A missing cache is an all-miss view and remains
absent. Failure writes no success bytes.

## Trust, ownership, failure, and determinism

The caller owns cache-root authority and the project composition root owns
source acquisition. The realizer retains only immutable source and artifact
bytes for the call result. It owns no descriptor, subprocess, thread, worker,
clock, random source, global registry, or background lifecycle.

M133 digest verification establishes internal content integrity, not origin or
authenticity of a malicious self-consistent local mapping. M134 does not widen
that trust boundary. Sequential lookup observes entries as read; hostile
concurrent replacement remains outside the supported local single-caller
model. Once returned, every selected payload is immutable and fully verified.

A source, cache, limit, or decoder failure discards all in-memory candidates.
No project or cache write is attempted. Decoder execution can begin only after
the complete source and cache phases succeed. Stable plan, source, cache, and
limits produce the same materialization and canonical report bytes.

## Compatibility

M131 execution/materialization, M132 publication, and M133 lookup remain
unchanged. The new focused-package exports and CLI subcommand are experimental
and additive. The engine root, loader/cache-key identity, earlier protocols,
dependencies, version, workflows, and permissions remain unchanged.

## Non-scope

M134 has no automatic cache publication, cache creation/write/repair/deletion/
eviction, remote cache, networking, authentication, discovery, enumeration,
watcher, import/reimport, worker, scheduler, process, thread, plugin or decoder
registration, renderer upload, project write, world/session, mutation, or
receipt. It adds no dependency, native code, backend object, engine-root API,
version, workflow job/allocation, hosted allocation, permission, credential,
release authority, or CI change. There is no CI change.

## Consequences

- Verified local hits now bypass built-in decoder work without bypassing input,
  cache, or resource-bound validation.
- Missing actions remain ordinary local decoder work and are not published as
  a side effect.
- A corrupt later action prevents every decoder call, making failure ordering
  independent of which earlier entries were misses.
- The unchanged M131 execution implementation remains independently protected;
  parity tests bind realization output to its materialization result.

## Revisit triggers

- Automatic publication requires an explicit write policy, complete-success
  transaction semantics, and separately reviewed failure behavior.
- Concurrent cache readers/writers require supported-filesystem evidence and a
  precise snapshot or descriptor-pinning policy.
- Remote use requires authentication, authorization, poisoning defenses,
  transport bounds, retries, and distinct read/write credentials.
- Additional decoders or plugins require a deterministic registration and
  compatibility contract outside this slice.

## Rejected alternatives

- Publish decoded misses automatically. Rejected because cache write authority
  must remain explicit and independently auditable.
- Decode each miss immediately during lookup. Rejected because corruption in a
  later action would make decoder side effects and cost depend on cache order.
- Treat present corruption as a miss. Rejected because it hides integrity
  faults and introduces an implicit repair path.
- Skip source validation for cache hits. Rejected because the action key is
  valid only for the exact declared current inputs.
