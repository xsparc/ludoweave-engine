# API status

The normative compatibility policy is
[`API_COMPATIBILITY.md`](https://github.com/xsparc/ludoweave-engine/blob/main/API_COMPATIBILITY.md). LudoWeave defines official
Python exports through `__all__`; the adjacent `__stability__` mapping gives
every exported symbol its status.

The `0.1.0a1` surfaces are:

| Module | Role | Status |
| --- | --- | --- |
| `ludoweave` | Deliberately small engine root | Experimental |
| `ludoweave.core` | Clock/error contracts | Experimental |
| `ludoweave.ecs` | Entity, component, query, resource, schedule, world, and installed conformance contracts | Experimental |
| `ludoweave.app` | Lifecycle, fixed-step application, and input contracts | Experimental |
| `ludoweave.world` | Persistent commands, bounded receipt decoding, snapshots, replay, and authority; command/receipt preview remains deferred under RFC-0003/RFC-0004 | Experimental |
| `ludoweave.render` | Backend-neutral 2D rendering contracts and installed conformance evidence | Experimental |
| `ludoweave.render.backends` | Null validation adapters | Experimental |
| `ludoweave.render.backends.wgpu` | Optional concrete WebGPU device entry point | Experimental |
| `ludoweave.platform` | Provider-neutral events and gamepad-provider protocol | Experimental |
| `ludoweave.assets` | Project-confined asset manifests, loading, and pipeline contracts | Experimental |
| `ludoweave.scene` | Versioned data-only scene/prefab/source-manifest/source-lock documents and world-transaction planning | Experimental |
| `ludoweave.audio` | Audio protocol, mix graph, and Null adapter | Experimental |
| `ludoweave.collision` | Deterministic bounded collision | Experimental |
| `ludoweave.presentation` | Tick animation, bitmap text, tilemap, particle, and extraction contracts | Experimental |
| `ludoweave.plugins` | Data-only plugin manifests and compatibility evaluation | Preview |
| `ludoweave.agent` | Typed agent-control service and installed conformance evidence | Experimental |
| `ludoweave.samples` | Exercised reference compositions | Experimental |

Names from `ludoweave.tools` are composition-root internals unless a future
decision exports them. CLI commands and persistent protocols have separately
documented versioned contracts; a Python stability label does not override a
wire-format revision. M121 extends the internal `HeadlessProject` composition
with project-confined scene file loading without exporting a new public symbol.
M122 similarly adds explicit project-confined prefab source and instance file
loading only to that internal composition root; the public exports are
unchanged. M123 adds a versioned CLI output protocol and no Python export.
M124 adds experimental `SourceManifest`, `SourceManifestEntry`,
`SourceManifestLimits`, and `SOURCE_MANIFEST_PROTOCOL` exports through the
focused `ludoweave.scene` package plus a versioned CLI result; the engine root
remains unchanged. M125 adds experimental `SourceLock`, `SourceLockEntry`,
`SourceLockLimits`, and `SOURCE_LOCK_PROTOCOL` through the same focused package
plus a versioned verification result; the engine root remains unchanged.
M126 adds experimental `ASSET_MANIFEST_PROTOCOL` and `AssetManifestLimits`
through the focused `ludoweave.assets` package plus internal project-confined
loading and canonical methods on the existing `AssetManifest`; the engine root
remains unchanged. M127 adds experimental `dependency_closure()` behavior to
that existing class plus a versioned read-only CLI result. It adds no Python
export and the engine root remains unchanged.
M128 adds experimental `ASSET_SOURCE_LOCK_PROTOCOL`,
`ASSET_SOURCE_MAX_BYTES`, `ASSET_SOURCE_TOTAL_MAX_BYTES`,
`AssetSourceLockLimits`, `AssetSourceLockEntry`, and `AssetSourceLock` through
the focused `ludoweave.assets` package plus a versioned verification result.
The engine root remains unchanged.
M129 adds experimental `ASSET_BUILD_PLAN_PROTOCOL`, `ASSET_LOADER_PROTOCOL`,
`AssetBuildPlanLimits`, `AssetBuildPlanEntry`, and `AssetBuildPlan` through the
focused `ludoweave.assets` package. The new loader constant names the exact
existing M4 cache-key identity and does not change its bytes. Planning adds a
versioned CLI document; the engine root remains unchanged.
M130 adds experimental exact verification behavior to `AssetBuildPlan`, an
internal project-confined plan loader, and a versioned CLI verification result.
It adds no Python export and the engine root remains unchanged.
M131 adds experimental `ASSET_BUILD_RESULT_PROTOCOL`,
`AssetBuildExecutionLimits`, `AssetBuildInput`, `AssetBuildResultEntry`,
`AssetBuildResult`, and `execute_asset_build_plan` through the focused
`ludoweave.assets` package. The versioned result retains output identities but
not payloads; the engine root remains unchanged.
M132 adds experimental `AssetBuildArtifact`, `AssetBuildMaterialization`,
`materialize_asset_build_plan()`, `ASSET_CACHE_ENTRY_PROTOCOL`,
`ASSET_CACHE_PUBLISH_PROTOCOL`, `AssetCacheError`, `AssetCachePublishEntry`,
`AssetCachePublishSummary`, and `AssetCacheStore` through
`ludoweave.assets`. Cache protocols and storage remain local-only; the engine
root remains unchanged.

M20 confirms that the installed command/transaction/receipt path is canonical,
atomic, and transport-independent within one version. It remains experimental:
there is no cross-version fixture result, external consumer evidence, complete
field-evolution policy, or supported feature-release channel for the preview
deprecation promise. M21 adds the bounded reader and a frozen single-version
fixture baseline; those new exports also remain experimental under RFC-0004.
M22 adds no export. RFC-0005 separately fixes the exact built-in v1 operation
argument evolution policy and satisfies that one RFC-0003 gate. M23 also adds
no export; RFC-0006 fixes receipt-v1 semantic-diff and diagnostic-code
evolution and satisfies that policy gate. Cross-version history, external
feedback, and a supported feature-release channel remain incomplete.
M24 adds no export; RFC-0007 makes cross-version admission mechanically
auditable but records the current single-version/no-release-evidence result as
not ready.
M25 adds no export; RFC-0008 makes external-consumer-feedback admission
mechanically auditable but records the reviewed empty manifest as not ready.
M26 adds no export; RFC-0009 makes supported feature-release-channel admission
mechanically auditable but records the reviewed empty manifest as not ready.
M27 adds no export; RFC-0010 makes external-contributor rehearsal admission
mechanically auditable but records the reviewed empty manifest as not ready.
M28 adds no export; RFC-0011 makes external sample-game adoption admission
mechanically auditable but records the reviewed empty manifest and zero count
as not ready.
M29 adds no export; RFC-0012 makes external contributor-retention admission
mechanically auditable but records the reviewed empty manifest and zero count
as not ready.
M30 adds no export; RFC-0013 makes published-wheel installation-matrix
admission mechanically auditable but records the reviewed empty manifest and
zero successful environments as not ready.
M31 adds no export; RFC-0014 makes issue-response and pull-request-review
latency admission mechanically auditable but records the reviewed empty
manifest, zero measurements, and no SLA as not ready.
M32 adds no export; RFC-0015 makes CI replay-divergence-rate admission
mechanically auditable but records the reviewed empty execution manifest and no
measured divergence rate as not ready.
M33 adds no export; RFC-0016 makes controlled benchmark-regression-rate
admission mechanically auditable but records the reviewed empty comparison
manifest and no measured regression rate as not ready.
M34 adds no export; RFC-0017 makes task-directed agent-tool recovery-rate
admission mechanically auditable but records the reviewed empty call manifest
and no measured completion-without-manual-recovery rate as not ready.
M35 adds no export; RFC-0018 makes third-party conformance adoption
mechanically auditable but records the reviewed empty submission manifest and
zero passing external implementations as not ready.

Inspect metadata directly when evaluating an alpha dependency:

```python
import ludoweave.ecs as ecs

assert set(ecs.__all__) == set(ecs.__stability__)
assert ecs.__stability__["World"] == "experimental"

import ludoweave.plugins as plugins

assert plugins.__stability__["PluginManifest"] == "preview"
```
