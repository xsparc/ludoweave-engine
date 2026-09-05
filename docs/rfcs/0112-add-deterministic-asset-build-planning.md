# RFC-0112: Add deterministic asset build planning

- **Status:** Accepted
- **Date:** 2026-08-26
- **Decision owners:** LudoWeave maintainers

## Context

M126-M128 establish an explicit asset graph, selected closure, and verified raw
source identities. The older M4 `AssetPipeline` can decode selected formats and
write content-addressed artifacts, but source checking currently has no pure
representation of the work that would be attempted before those effects.

Current primary references separate these responsibilities. Bazel first builds
the target graph and required action list, then checks local/remote caches, and
only then executes missing actions. Its action identity includes declared
inputs and execution configuration. Python's `graphlib` defines topological
ordering but documents that equally ready node order depends on insertion.
Unity distinguishes referenced dependencies from assets actually required by a
build. Godot separates source/import configuration from generated imported
files. These support one pure explicit-closure plan with a specified tie-break,
not an automatic import, cache, or scheduler.

## Decision

Add these experimental focused-assets contracts:

```python
ASSET_LOADER_PROTOCOL = "ludoweave.assets/1"
ASSET_BUILD_PLAN_PROTOCOL = "ludoweave.asset-build-plan/1"
AssetBuildPlanLimits
AssetBuildPlanEntry
AssetBuildPlan
```

`ASSET_LOADER_PROTOCOL` names the exact existing M4 loader/cache identity.
`AssetPipeline` and the planner call the same cache-key function. The resulting
key bytes remain unchanged.

The exact plan document is:

```json
{
  "$schema": "ludoweave.asset-build-plan/1",
  "loader_protocol": "ludoweave.assets/1",
  "asset_source_lock_sha256": "sha256:...",
  "asset_manifest_sha256": "sha256:...",
  "roots": ["asset://materials/player.json"],
  "entries": [
    {
      "uri": "asset://textures/player.png",
      "kind": "png",
      "settings": {},
      "source_sha256": "sha256:...",
      "source_bytes": 18,
      "dependencies": [],
      "cache_key": "sha256:..."
    }
  ]
}
```

`AssetBuildPlan.from_inputs()` accepts exact `AssetManifest` and
`AssetSourceLock` values. The lock's canonical manifest identity must match;
its entries must equal the exact manifest closure of its roots; and kinds must
agree. The plan hashes the canonical lock, retains the canonical manifest hash,
and emits only that selected closure.

An iterative topological pass tracks unresolved direct dependencies. It chooses
the lowest logical URI from the current ready set and emits each asset exactly
once. Every dependency therefore precedes its consumers, and manifest insertion
order cannot affect output. Empty roots produce an empty plan.

For each entry, the planner computes the existing M4 cache key over logical URI,
kind, normalized settings, raw source SHA-256, loader protocol, and the direct
dependency cache keys in normalized dependency order. Plan decoding rechecks
exact fields, hashes, root closure, dependency-first order, and all cache keys.
Decode limits may tighten the 8 MiB document, 4,096-root, and 4,096-entry hard
limits.

Add one read-only command:

```console
ludoweave source asset-plan PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json
```

The command loads the expected confined M128 lock, recomputes current M128
identities, requires exact verification, reloads the bounded normalized asset
manifest, and constructs the plan. It writes canonical plan bytes to stdout
only after complete success. It does not persist the plan.

## Ownership, determinism, and failure behavior

Plan values are immutable, detached, and caller-owned. Planning retains no file
descriptor, source payload, decoder result, cache handle, task, worker, or
process. The CLI's M128 verification owns and closes each sequential source
descriptor before planning.

Manifest/lock disagreement produces a typed `asset_build_plan.input_mismatch`
with the first stable field and optional logical URI. Lock verification keeps
its existing content-silent diagnostics. No failure exposes a source path or
compared hash/size value. No success bytes precede full success.

For stable accepted inputs, plan bytes and ready-set selection are
deterministic. The preceding sequential M128 reads are not an atomic filesystem
snapshot; concurrent source change remains outside the contract.

## Boundary and compatibility

M129 is prospective deterministic work identity only. A cache key does not
prove that an entry exists, was produced by a trusted builder, contains the
expected payload, or will decode/build successfully. The plan is not an
artifact manifest, execution log, receipt, signature, provenance statement,
authenticity result, or build-reproducibility proof.

There is no asset payload decode, asset build, import, cache read, cache write,
artifact creation, activation, automatic reimport, watcher, scheduler, worker,
parallel execution, resume, rollback, or discovery. M129 adds no unused-asset
rejection or build-inclusion inference beyond the explicit M127 roots and
closure. It adds no source/project write, world/session, command, transaction,
world mutation, receipt, remote access, dependency, metadata, version, engine-
root export, workflow job, workflow allocation, permission, credential,
release authority, tag, release, publication, push, PR, or remote change. There
is no workflow allocation.

Existing M4 artifact/cache bytes, M126 manifests, M127 reports, M128 locks and
verification results, and all their protocols remain unchanged. Any
incompatible plan or loader-identity change requires a new protocol identity.

## Alternatives considered

- Execute `AssetPipeline.build()` after verification. Rejected because it
  decodes payloads, creates directories, writes partial cache state, and mixes
  planning with effects.
- Use closure URI order as execution order. Rejected because a consumer may
  sort before its dependency.
- Use an unspecified topological sort. Rejected because equally ready ordering
  can depend on insertion.
- Plan every manifest asset. Rejected because M127 deliberately distinguishes
  selected roots/closure from unused or shared catalog entries.
- Inspect or populate a local/remote cache. Rejected because cache ownership,
  trust, artifact verification, concurrency, and failure recovery are separate
  decisions.

## References

- [Bazel build reference](https://bazel.build/concepts/build-ref)
- [Bazel remote caching](https://bazel.build/remote/caching)
- [Python `graphlib`](https://docs.python.org/3/library/graphlib.html)
- [Unity 6.2 `AssetDatabase.GetDependencies`](https://docs.unity3d.com/6000.2/Documentation/ScriptReference/AssetDatabase.GetDependencies.html)
- [Godot stable import process](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html)
- [ADR-0017: content-addressed project-confined assets](../adr/0017-content-addressed-project-confined-assets.md)
- [RFC-0110: source-to-asset dependency checking](0110-add-source-to-asset-dependency-checking.md)
- [RFC-0111: asset-source lock verification](0111-add-asset-source-lock-verification.md)
