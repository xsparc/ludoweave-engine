# RFC-0114: Add bounded in-memory asset plan execution

- **Status:** Accepted
- **Date:** 2026-08-26
- **Decision owners:** LudoWeave maintainers

## Context

M130 proves that one saved plan still describes the current project inputs,
but it intentionally stops before any decoder runs. The next boundary must
exercise the existing built-in asset transformations without simultaneously
introducing cache lookup, cache publication, filesystem output ownership,
workers, plugins, or automatic reimport.

Current [Bazel remote-cache documentation](https://bazel.build/remote/caching)
separates required-action construction, cache lookup, local action execution,
and later output upload. Current [Gradle build-cache documentation](https://docs.gradle.org/current/userguide/build_cache.html)
keeps cache enablement separate from task execution and requires declared
inputs and repeatable outputs before reuse. Its [build-cache concepts](https://docs.gradle.org/current/userguide/build_cache_concepts.html)
also warn against non-repeatable and overlapping outputs. Stable [Godot import
documentation](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html)
distinguishes committed import configuration from generated imported files.

These sources support a decoder-execution milestone whose result is detached
content identity only. They do not justify a cache, persisted artifacts,
parallel execution, loader plugins, discovery, or automatic reimport.

## Decision

Add the experimental focused-package values:

- `AssetBuildExecutionLimits`;
- `AssetBuildInput`;
- `AssetBuildResultEntry`;
- `AssetBuildResult`; and
- `execute_asset_build_plan()`.

`AssetBuildInput` owns exact immutable bytes and one logical URI. Callers pass
an exact tuple in the M129 plan's dependency-first order. Before any decoder
runs, execution requires exact plan/input URI agreement, exact per-entry source
byte counts and SHA-256 identities, and both per-source and aggregate source
bounds. Empty plans remain valid.

Execution supports only the existing built-in M4 kinds and behavior:

- PNG becomes the existing bounded RGBA8 texture payload with its dimensions;
- JSON becomes the existing sorted compact UTF-8 representation;
- WGSL must be valid UTF-8 and otherwise retains its bytes; and
- audio retains exact bytes.

Settings remain part of the already verified cache key but are not a new
decoder extension point. Each decoded payload is bounded, hashed, counted, and
released after its result entry is constructed. No payload is retained in the
returned result.

`AssetBuildResult` uses protocol `ludoweave.asset-build-result/1`. It binds the
canonical plan SHA-256, unchanged loader protocol, total accepted source and
artifact bytes, and plan-ordered entries containing URI, kind, cache key,
source byte count, artifact SHA-256, and artifact byte count. Canonical result
encoding is capped at 8 MiB. Repeating execution over identical detached
inputs is byte-identical.

Source mismatch uses stable `asset_build.input_mismatch`. Resource failure
uses `asset_build.limit_exceeded`. Built-in decoder rejection is chained and
normalized to `asset_build.decode_failed`. Diagnostics identify only a stable
field, limit, optional logical URI, and stable cause code; source bytes and
expected/actual hashes are absent.

## CLI composition

Add:

```console
ludoweave source asset-build PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE
```

The command loads the saved plan first, recomputes and verifies current M128
inputs, regenerates and verifies the M129 plan, then acquires each source
through the existing project-confined bounded reader. The executor rechecks
those detached bytes before decoding. Only the complete canonical
`ludoweave.asset-build-result/1` document is written to stdout.

Sequential filesystem reads are not an atomic project snapshot. Once read,
the immutable detached byte tuple is the exact execution input. A change
between lock hashing and detached acquisition is rejected by the executor.

## Ownership, failure, and determinism

The project composition owns and closes every source descriptor before
execution. The pure executor owns no descriptor, path, cache root, renderer,
world, process, thread, or background task. Intermediate decoded payloads are
local values and become unreachable on success or failure.

No success bytes are emitted until plan verification, complete detached-input
preflight, every decoder, every bound, and result construction succeed.
Failure cannot leave a partial project or cache output because M131 writes
neither.

Determinism requires stable detached bytes and the exact built-in loader
protocol. M131 makes no cross-implementation decoder promise and no claim that
the sequential pre-read observed one atomic filesystem state.

## Compatibility

All new Python exports are experimental. The engine root, package version,
M4 loader/cache-key identity, M126 manifest, M128 lock, and M129 plan are
unchanged. The CLI command and result protocol are additive.

## Non-scope

M131 has no cache read, no cache write, no persisted artifact, no project write,
no atomic publication, no cache-hit policy, no artifact reader, no
partial execution or resume, no scheduler, worker, process, thread, plugin or
decoder registration, no discovery, watcher, import/reimport, live update,
renderer upload, world/session, command, transaction, world mutation, or
receipt. It adds no dependency, native code, workflow job, workflow
allocation, permission, credential, release authority, push, PR, tag, release,
or publication.

## Consequences

- The complete verified plan can now exercise real built-in decoders and
  produce deterministic output identities without persistent side effects.
- A later cache milestone can define artifact schema, lookup verification,
  atomic publication, collision handling, cleanup, and ownership separately.
- Returning identities instead of payloads keeps this CLI useful for
  reproducibility evidence while avoiding a premature artifact transport.

## Revisit triggers

- A cache milestone must define independent payload/metadata integrity,
  same-filesystem staging, atomic publication, stale/corrupt entry handling,
  and cleanup before using M131 output identities for reuse.
- A decoder extension milestone must define explicit registration authority,
  version identity, determinism class, resource limits, failure normalization,
  and installed conformance before admitting third-party code.
- Parallel execution requires evidence that ready-set scheduling, aggregate
  bounds, cancellation, and error selection remain deterministic.

## Rejected alternatives

- Invoke the existing recursive `AssetPipeline` from the CLI. Rejected because
  it combines source acquisition, decoding, recursion, directory creation, and
  cache persistence before the new verification boundary is established.
- Persist decoded payloads immediately. Rejected because atomic pair
  publication, collision/corruption behavior, cleanup, and reader integrity
  need a separate decision.
- Accept callbacks or discovered decoder plugins. Rejected because execution
  authority, code loading, determinism, and resource ownership are undefined.
- Stream results while executing. Rejected because a late source, decoder, or
  limit failure would expose a partial success document.
