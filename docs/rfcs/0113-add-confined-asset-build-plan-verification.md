# RFC-0113: Add confined asset build-plan verification

- **Status:** Accepted
- **Date:** 2026-08-26
- **Decision owners:** LudoWeave maintainers

## Context

M129 can construct and strictly decode deterministic prospective work, but a
saved plan has no composition-root loader and no operation that establishes it
still matches current verified inputs. Executing a caller-supplied stale plan
later would undermine the input identity that its cache keys describe.

Current [Bazel remote-caching documentation](https://bazel.build/remote/caching)
describes declared inputs and required actions before cache lookup and
execution. Current [Gradle build-cache documentation](https://docs.gradle.org/current/userguide/build_cache.html)
requires complete task inputs for safe reuse, while its
[configuration-cache documentation](https://docs.gradle.org/current/userguide/configuration_cache.html)
revalidates recorded input fingerprints before restoring a saved graph. Stable
[Godot import documentation](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html)
separates committed import configuration from generated imported assets.

These sources support a verification prerequisite, not immediate execution or
cache integration. LudoWeave already owns confined readers, strict plan
decoding, M128 current-input verification, and deterministic M129 planning.

## Decision

Add `HeadlessProject.load_asset_build_plan(relative, *, limits=...)`. It uses
the existing project-relative path policy, regular-file/no-follow descriptor,
8 MiB plan limit, exact limits type, and owned close path. It delegates detached
bytes to `AssetBuildPlan.from_json()` and retains no descriptor.

Add `AssetBuildPlan.verify(actual)`. Both operands must be exact constructed
plans. Verification compares, in order:

1. asset-source-lock SHA-256 identity;
2. asset-manifest SHA-256 identity;
3. sorted direct roots;
4. exact entry URI sequence; and
5. kind, normalized settings, source SHA-256, source byte count, dependencies,
   and cache key for each URI.

Failure is stable `asset_build_plan.mismatch` in phase `verify`, with only the
first field and optional logical URI. An inexact operand uses
`asset_build_plan.invalid_verify`. No compared hash, size, settings value,
cache key, or path enters details or messages.

Add:

```console
ludoweave source asset-plan-verify PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE
```

The command loads the saved plan and expected M128 lock, recomputes the current
lock, verifies it, reloads the asset manifest, regenerates the M129 plan, and
compares it with the saved plan. Only after complete success it emits canonical
`ludoweave.cli.asset-build-plan-verify/1` containing status, plan/loader
protocols, and root/entry counts.

## Ownership, failure, and determinism

The project composition owns every opened descriptor and closes it before a
plan is returned or an error escapes. Returned plans are frozen, slotted, and
detached. The CLI writes no project file and retains no handle.

Invalid paths/files/documents fail before source hashing. Current M128 mismatch
fails before current-plan construction. Saved-plan mismatch fails before any
success byte. Existing structured exception chaining remains authoritative;
diagnostics are content-silent.

Stable saved bytes and stable current project inputs produce the same success
bytes. M128 reads remain sequential rather than an atomic filesystem snapshot;
concurrent source modification is not admitted by this result.

## Boundary and compatibility

M130 changes no M129 schema or cache-key byte. The method added to the focused
experimental plan class and the versioned CLI result remain experimental. The
engine root, dependencies, metadata, version, workflows, and release authority
are unchanged.

This is verification only. There is no plan execution, asset payload decoder,
asset build, import, cache read, cache write, artifact creation, scheduler,
worker, parallel execution, discovery, watcher, reimport, live update,
source/project write, world/session, command, transaction, mutation, receipt,
provenance, authenticity, or signature. There is no workflow allocation.

## Consequences

- A saved M129 plan can be safely loaded and proven current before a later
  execution design is considered.
- Mismatch evidence stays stable and does not disclose compared content.
- Verification rereads current selected sources and inherits the documented
  sequential-snapshot limitation.
- A future execution milestone must separately define decoder registration,
  cache ownership, artifact integrity, atomic publication, failure receipts,
  and interruption behavior.

## Rejected alternatives

- Execute the plan during verification. Rejected because verification must be
  side-effect-free and execution ownership is undefined.
- Trust only the saved cache keys. Rejected because keys do not establish that
  the current project still has the recorded inputs.
- Compare only canonical plan hashes. Rejected because a stable first-field
  mismatch is more useful while remaining content-silent.
- Discover a default plan. Rejected because project composition stays explicit
  and directory-discovery-free.

## Evidence required

- exact and mismatching unit verification cases with content-silent details;
- confined loading, limit, traversal, and descriptor-close evidence;
- CLI success, stale-plan, current-source mismatch, and no-success-byte cases;
- isolated no-dependency wheel generation plus saved-plan verification;
- architecture, docs, full supported-runtime, graphics, package, release,
  scope, credential, history, cleanup, and DCO evidence.
