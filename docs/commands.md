# Persistent command protocol

M2 introduces a persistent world-command contract alongside the process-local
`ludoweave.ecs.Commands` buffer. They solve different problems: the ECS buffer
defers trusted system work until one in-process safe point, while persistent
commands are caller-attributed, versioned data intended for transactions,
receipts, snapshots, replay, CLI tools, and later adapters.

## M2-01 envelope

One command uses protocol `ludoweave.command/1` and contains caller-supplied
bounded IDs, an actor, an operation ID and version, an optional optimistic
world hash, and JSON-domain arguments. A transaction uses
`ludoweave.transaction/1`, names its target world, and contains a non-empty
ordered collection of commands. Commands in one transaction must share the
transaction ID, actor, and expected hash; command IDs must be unique.

IDs are data, not engine-generated timestamps or random values. Operation
registries are immutable, explicit composition-owned values. There is no
process-global operation registry and no Python callable/import field in the
wire schema. The initial registry identifies entity spawn/destroy,
component add/remove/patch, authoritative resource patch, and world tick.
Their typed argument validation and atomic behavior are completed by later M2
slices; registration alone is not an application claim.

RFC-0005 makes each built-in operation/version argument shape an exact
persistent identity. Unknown fields are rejected; a breaking change uses a new
operation version rather than reinterpreting v1. See the
[operation-argument compatibility guide](operation-argument-compatibility.md)
for the machine-readable baseline, evolution policy, and same-version evidence.

## Canonical JSON v1

Persistent documents use an engine-owned bounded profile:

- UTF-8, lexically sorted object keys, no insignificant whitespace;
- duplicate keys, trailing documents, BOM input, invalid Unicode, non-finite
  numbers, and values outside the JSON domain are rejected;
- signed 64-bit integers and exact finite binary64 values are distinct;
- floats use the reserved `$ludoweave.float` object with `float.hex()` text in
  canonical output, preserving numeric kind and signed zero;
- text code points are preserved rather than silently normalized;
- byte, nesting, node, collection, and string limits apply before domain
  handlers run.

This is a D1 serialization contract, not an assertion that arbitrary Python
floating-point simulation is cross-platform bit-identical.

## Atomic application

`WorldSession` owns the complete authority record used by persistent
transactions. Validation resolves every typed operation before cloning. Apply
then mutates only cloned world/resources/tick state and either discards that
record or adopts it with one pointer swap. A stale expected SHA-256 hash rejects
before decoding resource values or cloning. Dry-run returns a predicted result
without adoption.

The current built-in argument shapes are:

- `entity.spawn`: optional transaction-local `alias` and a `components` array;
- `entity.destroy`: an `entity` reference by alias or index/generation;
- `component.add`: an entity and full versioned component record;
- `component.remove`: an entity and component UUID;
- `component.patch`: an entity, component UUID/current version, and non-empty
  field changes;
- `resource.patch`: an authoritative resource UUID/current version and full
  replacement value decoded by its registered codec;
- `world.tick`: `count` exactly `1`, accepted only once as the final operation,
  only when a staged application tick executor is injected, and only for a
  state-only resource composition.

Component records use UUID, schema version, and field values. Spawn aliases are
transaction-local protocol data and are unrelated to M1 `DeferredEntity`
tokens. M119 scene planning uses this existing operation rather than adding a
scene operation to the persistent command registry.

Every session resource must have exactly one explicit role. Only `STATE`
resource schemas participate in authority hashes and patches. Input and
runtime/presentation resources remain outside the hash, are preserved when a
snapshot is loaded into an existing session, and make M2 persistent ticks
ineligible. M4 samples instead inject immutable tick-indexed action snapshots
into the staged executor and require replay callers to provide the equivalent
recorded stream; action snapshots are not silently persisted as resources.
Allocator churn and change epochs remain inside it because they affect future
allocation and changed-query behavior. See ADR-0009 for ownership, trusted
callback, and failure semantics.

## Receipts and semantic changes

`TransactionService.apply()` returns `ludoweave.receipt/1` for committed,
dry-run, and expected rejection paths. A rejection has identical pre/post
hashes, no changes or aliases, sanitized diagnostics, and rejected outcomes for
every command; partially mutated staged state is never described as committed.

A dry-run keeps its actual `post_hash` equal to `pre_hash` and records the
staged prediction in `proposed_post_hash`. Its semantic diff and alias mapping
match a later commit made against the unchanged pre-hash.

Diffs are computed from the complete pre/post authority images rather than
operation-handler claims. Net created, destroyed, and changed entities are
canonically sorted. Component additions, removals, changed field names and row
epochs; authoritative resource identities; allocator slot/free-list changes;
world/table epochs; and completed ticks are explicit. A spawn followed by a
destroy is absent from net entity lists but remains visible through command
outcomes, allocator/epoch changes, and the changed hashes. A write reverted to
its original value has no false field change but retains its row-epoch change.

Receipt and diff limits are checked before adoption. Receipts do not embed
component or resource values, reducing accidental disclosure; authoritative
hashes prove the exact state and query/snapshot services provide deliberate
state observation paths.

## M119 scene transaction planning

`ludoweave.scene/1` is a versioned data-only scene document. Its exact root
fields are `$schema`, `scene_id`, `entities`, and `dependencies`. Each entity
declares a stable transaction-alias-compatible local ID, a unique bounded name,
an optional parent local ID, and component records keyed by registered
module-qualified name. Component records contain an exact positive schema
version and canonical JSON object values. Dependencies are distinct canonical
`asset://` identities; planning reports them but does not load them.

`SceneDocument` applies the shared bounded canonical JSON profile, rejects
duplicate members and unknown fields, detaches nested caller input, sorts
entities/components/dependencies, and rejects repeated IDs/names, missing or
self parents, and parent cycles. Custom limits may tighten but never enlarge
the documented hard maxima. This produces a deterministic authoring input, not
a second world-state representation.

`compile_scene()` receives an explicit immutable `ComponentRegistry`. It
resolves every named schema, performs existing version migration and current-
value validation, and adds the compiler-owned `SceneNode` provenance component
before it constructs any world mutation. The complete result is one ordinary
transaction of ordinary `entity.spawn` commands. Applying it through
`TransactionService` preserves the established all-or-nothing staging rules;
receipt aliases provide the deterministic local-ID-to-runtime-entity mapping.
The stored `SceneNode` keeps `scene_id`, `instance_id`, local ID, name, and
parent local ID in canonical ECS state. Canonical runtime state remains in the
world store.

Compilation owns no world, renderer, asset loader, file handle, or background
resource and therefore has no close method. The caller owns the immutable
document and plan; `WorldSession` and `TransactionService` retain their existing
single-owner and atomic failure semantics. Unknown components, incompatible
values, a missing `SceneNode` registration, or an invalid plan raise structured
`SceneError` before a transaction can mutate authority.

M119 has no file I/O, no prefab inheritance, no live update/reimport semantics,
no implicit parent-to-runtime-handle relation, no arbitrary Python graph or
import, no new command operation, no root-package export, no dependency, and no
workflow or hosted runner change. M120 provides the separately assigned prefab
fragment planning slice; a runtime `EntityRef` facade remains deferred.

## M120 one-level prefab fragment planning

`ludoweave.prefab/1` is a versioned data-only scene fragment. Its exact root
fields are `$schema`, `prefab_id`, `entities`, and `dependencies`; entity,
hierarchy, component, asset, canonical ordering, ownership, and hard-limit
semantics are the M119 scene invariants.

`ludoweave.prefab-instance/1` names the exact `prefab_id`, one stable
`instance_id`, and a bounded override array. Each override contains exactly
`local_id`, `component`, `version`, and non-empty `changes`. The local entity
and named component must already exist in the fragment. `version` must equal
the registered current component schema, and every changed field/value passes
that schema. Overrides cannot add or remove entities, components, or parent
relationships.

`compile_prefab()` receives both detached immutable documents plus an explicit
`ComponentRegistry` and existing transaction identities. It migrates base
values, applies all schema-aware replacements before mutation, adds the
compiler-owned `PrefabNode`, and delegates to M119 planning. The returned plan
contains ordinary `entity.spawn` commands in one atomic `CommandTransaction`.
Receipt aliases provide the local-ID-to-runtime-entity mapping. Canonical
runtime state remains in the world store.

The source fragment and instance request remain caller-owned and unchanged.
Planning owns no resources and failures are structured `PrefabError` values.
A transaction stale-hash or later command rejection remains all-or-nothing.
Changing a source fragment has no effect on an existing runtime instance; a
caller must explicitly compile and apply another transaction.

M120 is one-level only: no nested prefab inheritance, variant chain, parameter
expression, file I/O, asset loading, live update, reimport, silent propagation,
source write-back, runtime link graph, or arbitrary Python import/evaluation.
There is no new persistent operation, root-package export, dependency,
workflow, or hosted runner change.

## M121 project-confined scene file loading

The existing headless composition root can load one scene explicitly:

```python
from pathlib import Path

from ludoweave.tools.headless_project import HeadlessProject

project = HeadlessProject.load(Path("my-game"))
scene = project.load_scene("scenes/main.json")
assert scene.protocol == "ludoweave.scene/1"
```

`load_scene()` requires one project-relative path and accepts an exact
`SceneLimits` when callers need tighter bounds. It reuses M2 path confinement,
regular-file validation, sanitized errors, and a handle read capped at one byte
beyond the limit. The handle closes inside the call. The resulting detached
immutable document uses the unchanged M119 decoder and canonical ordering.

The load performs no world mutation. Callers separately invoke
`compile_scene()` and apply the returned ordinary transaction to obtain a
receipt. Filesystem time and concurrent external edits are outside simulation
determinism; load source data before deterministic execution. Changing or
removing the source file cannot alter the returned document or existing world
state.

M121 has no directory discovery, prefab file loader, file URI, include/import
graph, asset loading, cache, watcher, live update/reimport, source write-back,
remote access, arbitrary Python import/evaluation, new persistent operation,
dependency, root-package export, workflow, or hosted runner change. Root
containment is not a race-free filesystem sandbox.

## M122 project-confined prefab file loading

The existing headless composition root loads prefab source and instance files
explicitly:

```python
from pathlib import Path

from ludoweave.tools.headless_project import HeadlessProject

project = HeadlessProject.load(Path("my-game"))
prefab = project.load_prefab("prefabs/scout.prefab.json")
instance = project.load_prefab_instance("prefabs/scout.instance.json")
assert prefab.protocol == "ludoweave.prefab/1"
assert instance.protocol == "ludoweave.prefab-instance/1"
```

These are two explicit files with no implicit pairing. Each synchronous call
uses the established project-confined bounded reader and returns detached
immutable data after closing its descriptor. `compile_prefab()` subsequently
checks that both records name the same prefab source. Loading performs no world
mutation; applying the compiled ordinary transaction remains the receipt
boundary.

M122 has no directory discovery, extension routing, manifest lookup, asset
loading, cache, watcher, live update, reimport, nested composition, write-back,
remote access, new persistent operation, dependency, root export, workflow, or
hosted runner change.

## M123 read-only source preflight

`ludoweave source check` provides a structured project-confined check before a
caller chooses to compile or instantiate source data. Scene mode accepts one
file; prefab mode accepts two explicit files and verifies exact source/instance
identity. A valid result uses `ludoweave.cli.source-check/1` and includes
canonical source hashes and bounded counts.

The check performs no compile, creates no session or world, applies no command,
and causes no world mutation, so there is no receipt. It does not prove that
component payloads match a later application-supplied registry. There is no
directory discovery, cache, live update, write-back, asset loading, remote
access, new persistent operation, dependency, root export, or workflow
allocation.

## M124 explicit source manifests

`ludoweave.source-manifest/1` is a bounded data-only list for source preflight.
Its exact root fields are `$schema`, `manifest_id`, and `entries`. Each nonempty
manifest has at most 256 entries. Entries contain an `entry_id`, `kind`, and
normalized portable project-relative `source`; prefab entries additionally
require one explicit `instance`. Entry IDs and exact references are unique, and
the normalized value orders entries by ID. `SourceManifestLimits` may tighten
the 64 KiB document, 256-entry, and 1,024-byte path bounds but cannot enlarge
them.

The focused types are experimental exports from `ludoweave.scene`.
`HeadlessProject.load_source_manifest()` is an internal composition method that
uses the same bounded project confinement as M121-M122. The manifest owns no
file handle, world, registry, renderer, or background resource after loading.

CLI `--manifest FILE` mode checks every explicit entry with the unchanged
scene/prefab readers and emits
`ludoweave.cli.source-manifest-check/1`. It reports normalized manifest and
source hashes plus per-entry and aggregate counts without paths. It performs no
compile or component semantic validation, causes no world mutation, writes no
project file, and produces no receipt. There is no directory discovery, glob,
implicit pairing, asset loading, cache, watcher, live update, remote access,
dependency, root export, persistent operation, or workflow allocation.

## M125 source-integrity locks

`ludoweave.source-lock/1` is a bounded path-independent record of one normalized
M124 manifest and the content identity observed for every explicit entry. Its
exact root fields are `$schema`, `manifest_id`, `manifest_sha256`, and
`entries`. Each entry repeats the stable manifest entry ID and kind, then binds
the accepted source protocol, stable source ID, and lowercase `sha256:`
identity. Prefab entries additionally bind the instance protocol, ID, and hash.
Entries normalize by ID and must be unique.

`SourceLockLimits` may tighten but not enlarge the 64 KiB and 256-entry hard
bounds. `SourceLock.verify()` compares manifest identity, the exact entry-ID
set, and each entry field in deterministic order. Mismatch errors contain only
the first differing field and optional entry ID; expected and actual hashes are
not disclosed. The focused lock values are experimental `ludoweave.scene`
exports. `HeadlessProject.load_source_lock()` remains an internal confined,
bounded, detached reader.

`ludoweave source lock PROJECT --manifest FILE` emits canonical lock bytes to
stdout without writing the project. `ludoweave source verify PROJECT --manifest
FILE --lock FILE` loads the confined expected lock, recomputes current
identities, and emits `ludoweave.cli.source-lock-verify/1` only after an exact
match. Existing `source check` output remains unchanged.

This is content integrity for explicit accepted JSON, not an atomic filesystem
snapshot, signature, provenance or authenticity proof, asset import, dependency
resolution, compile, registry lookup, or cache. It performs no world mutation,
writes no project file, and produces no receipt. There is no discovery,
watcher, live update, remote access, dependency, root export, workflow job, or
workflow allocation.

## M127 source-to-asset dependency checking

`AssetManifest.dependency_closure()` accepts an exact tuple of distinct direct
`AssetUri` roots and returns those roots plus all reachable dependencies as a
unique sorted tuple. Unknown roots and invalid root containers fail with typed
`AssetError` values. The existing manifest constructor has already required
every asset-to-asset edge to resolve and the graph to be acyclic.

`ludoweave source assets PROJECT --manifest FILE --assets FILE` uses the
unchanged M124 source inspection and M126 asset-manifest loader. Canonical
`ludoweave.cli.source-asset-check/1` output binds both normalized manifest
identities, preserves each source entry's direct declarations, and reports a
separate resolved closure. A missing direct URI returns exit 2 with the source
entry and logical dependency identity, writes no success document, and leaves
the project unchanged.

The checker does not infer application component references or reject unused
asset entries. It performs no asset source read, payload decode, asset build,
import, cache use or creation, compile, registry resolution, world mutation,
receipt, file write, discovery, watcher, live update, dependency, root export,
workflow job, or workflow allocation. Separate file reads are not an atomic
snapshot.

## M128 asset-source lock verification

`AssetSourceLock` is a frozen, slotted, bounded
`ludoweave.asset-source-lock/1` value. It binds canonical source-lock and asset-
manifest hashes, unique sorted direct roots, and exact URI-sorted resolved
entries containing logical URI, kind, source-byte count, and source SHA-256.
Tightening-only decode limits cap the JSON at 1 MiB and roots/entries at 4,096.

`ludoweave source asset-lock PROJECT --manifest FILE --assets FILE` reuses the
unchanged M124-M127 readers and closure, hashes only selected source files, and
writes the lock to stdout after complete success. Each source is streamed in
64 KiB blocks through one owned confined regular-file descriptor, with a
256 MiB per-source and 1 GiB accepted aggregate bound.

`ludoweave source asset-verify PROJECT --manifest FILE --assets FILE --lock
FILE` loads a confined expected lock and emits canonical
`ludoweave.cli.asset-source-lock-verify/1` only after exact comparison. A
mismatch returns exit 2 and only the first field plus optional logical URI; no
expected/current hash, byte count, or path is disclosed.

This is repeatable input identity, not an atomic snapshot, signature,
provenance, authenticity, imported artifact, build result, or cache key. There
is no asset decode, no asset build, no import, no cache write, no discovery,
watcher, live update, world mutation, receipt, dependency, root export,
workflow job, or workflow allocation.

## M129 deterministic verified asset build planning

`AssetBuildPlan` is a frozen, slotted, bounded
`ludoweave.asset-build-plan/1` value. It binds the canonical M128 lock and M126
manifest identities, unique sorted roots, the exact rooted closure, and
prospective actions in dependency-first order. URI order breaks ties between
ready actions. Tightening-only decoding caps the document at 8 MiB and roots or
entries at 4,096.

Every `AssetBuildPlanEntry` contains URI, kind, normalized settings, source
SHA-256/byte count, sorted direct dependency URIs, and cache key. Construction
and decoding require dependencies to precede their consumers, entries to equal
the rooted closure, and cache keys to match the exact existing M4 identity.
`ASSET_LOADER_PROTOCOL` names that unchanged identity; M4 artifact/cache bytes
do not change.

`ludoweave source asset-plan PROJECT --manifest FILE --assets FILE --lock FILE`
recomputes and verifies current M128 inputs before emitting canonical plan bytes
after complete success. Lock mismatch remains hash-, size-, and path-silent.

A plan is prospective work identity only. There is no asset decode, no asset
build, no cache read, no cache write, no artifact, import, scheduler, worker,
discovery, watcher, live update, world mutation, receipt, dependency, root
export, workflow job, or workflow allocation.

## M130 confined asset build-plan verification

`HeadlessProject.load_asset_build_plan()` reads one explicit project-relative
plan through the existing confined regular-file boundary and the plan's 8 MiB
decode limit. The returned value is detached and immutable; the loader retains
no descriptor.

`AssetBuildPlan.verify()` compares one saved plan with an exact current plan.
After exact type/protocol construction it checks source-lock identity, asset-
manifest identity, roots, entry URI sequence, then kind, settings, source hash/
size, dependencies, and cache key in stable order. A mismatch contains only the
first field and optional logical URI; compared content and paths are absent.

`ludoweave source asset-plan-verify PROJECT --manifest FILE --assets FILE
--lock FILE --plan FILE` loads the saved plan, recomputes and verifies current
M128 inputs, regenerates the M129 plan, and compares before emitting canonical
`ludoweave.cli.asset-build-plan-verify/1`. Success contains only protocol,
status, loader/plan protocols, and aggregate root/entry counts.

This is verification only. There is no asset decode, no asset build, no cache
read, no cache write, no artifact, import, execution, scheduler, worker,
discovery, watcher, live update, world mutation, receipt, dependency, root
export, workflow job, or workflow allocation.

## M131 bounded in-memory asset plan execution

`AssetBuildInput` is a frozen, slotted logical URI plus exact immutable source
bytes. `execute_asset_build_plan()` accepts an exact M129 plan and exact input
tuple in plan order. It validates the entire source set—URI sequence, sizes,
hashes, per-file limits, and aggregate limit—before decoding anything.

Only the existing built-in PNG, JSON, WGSL, and audio behavior executes. Each
payload is bounded, hashed, counted, and released after its result entry is
created. `AssetBuildResult` emits canonical
`ludoweave.asset-build-result/1` with the plan hash, loader protocol, aggregate
counts, and plan-ordered output identities. It never contains a decoded
payload or filesystem path.

`ludoweave source asset-build PROJECT --manifest FILE --assets FILE --lock FILE
--plan FILE` repeats the M130 saved/current verification chain, acquires exact
detached sources through project confinement, executes, and writes one result
only after complete success. Source drift, limits, and decoder failures are
structured and content-silent.

M131 has no cache read, no cache write, no persisted artifact, no project
write, no atomic publication, no scheduler, worker, process, thread, plugin,
decoder registration, discovery, watcher, reimport, renderer upload, world
mutation, receipt, dependency, root export, workflow job, or workflow
allocation.

## Canonical snapshots and random state

`SnapshotCodec` emits bounded canonical `ludoweave.snapshot/1` bytes for one
explicit component/resource composition. The wrapper contains the development
engine version, a SHA-256 authority hash, and the complete logical authority
image. Current-version encode/decode/encode is byte-identical.

Restore preserves allocator capacity, generations, exact free-list order,
world/table/row epochs, canonical components, explicit `STATE` resources,
completed ticks, and engine-owned random streams. It therefore preserves the
next entity allocation, changed-query behavior, and next random outputs, not
merely visible component values. Presentation/runtime resources, clocks,
paths, and storage internals are absent.

Snapshot decode rejects malformed, oversized, incompatible, hash-mismatched,
or structurally invalid input before returning a candidate. Historical
component/resource records move forward only through registered adjacent
migrations. `load_into()` fully constructs a candidate and then performs one
safe-point record adoption; a migration failure or active query leaves the
destination unchanged. Exact engine-version matching is intentionally strict
during community-alpha development.

`RandomStreams` owns explicit unsigned 64-bit seed state and independent named
PCG32/1 streams. Stream creation order does not couple sequences. Snapshot
state uses fixed-width lowercase hexadecimal values so the full unsigned range
is represented without weakening canonical JSON's signed 64-bit integer rule.

## Replay, checkpoints, and branches

`ReplayRecorder` owns one append-only `ludoweave.replay/1` timeline. Its header
records the exact engine/D1 profile, project-schema hash, dependency-lock hash,
caller-supplied platform profile, operation-registry fingerprint, random seed,
world identity, and initial tick/hash. The initial snapshot is embedded, so the
M2 format is self-contained and does not make domain services resolve paths or
artifact URIs.

Each recorded batch contains the original typed transaction plus exact
start/end completed ticks and pre/post authority hashes. Batch indexes and hash
chains are contiguous even when several non-tick transactions occur at the
same tick. Checkpoints name an `after_batch` boundary rather than an ambiguous
tick alone.

The recorder appends only committed transactions, never appends dry-runs or
rejections, returns rejected receipts, detects out-of-band authority changes,
and preflights replay limits before committing.
`ReplayRunner` restores a fresh session and submits every batch through the same
`TransactionService`; repeated runs either reach every recorded checkpoint or
raise a structured divergence naming the exact batch.

A branch is a new self-contained timeline initialized from all parent work at
an exact tick boundary. It records the complete parent timeline SHA-256 digest,
parent ID, batch boundary, tick, and state hash. The parent is never rewritten,
and a tick inside one indivisible transaction cannot be selected.
`replay_branch()` verifies the supplied immutable parent's ID and complete
timeline digest and reproduces its referenced boundary before running the child.

## Security boundary

The world package contains domain data and validation only. It may import core
and public ECS contracts, but not application, rendering, concrete backends,
tools, or transport/path code. Architecture tests also reject direct
`eval`, `exec`, and `compile` calls in this package.

## M5 agent adapters

M5 does not define another command language. `transaction_validate` and
`transaction_apply` accept the same `ludoweave.transaction/1` document described
above and return the same canonical receipt dictionaries as direct
`TransactionService` calls. The project-confined `ludoweave agent` adapter and
the local stdio MCP adapter both delegate to one transport-independent
`AgentCommandService`.

`world_tick` is convenience composition over ordinary transactions. It emits
one actor-attributed `world.tick` command and receipt per requested tick, stops
at the first rejected safe point, and records every committed transaction in
its replay timeline. It therefore preserves exact replay/branch boundaries but
does not make the entire requested count atomic.

Read, write, capture, and test behavior, quotas, concurrency, redaction, and
transport details are documented in the [agent control interface](agent-control.md)
and ADR-0019/ADR-0020.

## M20 stability decision

M20 evaluates command/receipt preview readiness. The installed same-version
path remains canonical, atomic, and transport-independent, but RFC-0003 retains
experimental status because the project lacks a public bounded receipt reader,
cross-version fixture history, external consumer feedback, field-evolution
policies, and a supported deprecation-capable release channel.

See the [stability decision](command-receipt-stability-decision.md). Do not
infer a preview promise from protocol `/1` identifiers or project-owned
conformance passes.

M21, M22, and M23 satisfy the bounded-reader, operation-argument-policy, and
receipt semantic-diff/diagnostic-policy gates, respectively. Cross-version
history, external feedback, and a supported deprecation release channel remain
absent, so the command/receipt surface stays experimental. See the
[receipt semantic compatibility guide](receipt-semantic-compatibility.md) for
the exact v1 meanings and unknown-code fallback rule.

M24's [cross-version corpus readiness guide](cross-version-corpus-readiness.md)
defines how gate-1 evidence is admitted. The current same-version reader and
empty supported-release set keep that gate false.

M25's [external consumer feedback readiness guide](external-consumer-feedback-readiness.md)
defines how gate-2 evidence is admitted. The reviewed manifest is empty, so
the current result remains false and no external adoption is claimed.

M26's [supported release channel readiness guide](supported-release-channel-readiness.md)
defines how gate-6 evidence is admitted. The reviewed release set is empty, so
the current result remains false and no support or publication is claimed.

## Reading receipts

M21 adds strict `TransactionReceipt.from_json` and `from_mapping` entry points.
Both apply canonical JSON and receipt-specific limits before returning detached
immutable values. They reject incompatible protocols, unknown fields,
malformed nested changes, and inconsistent status/hash/tick relationships with
structured receipt decode errors.

The [bounded receipt-reader guide](receipt-reader.md) lists the exact default
limits, invariants, failure codes, ownership boundary, and frozen v1 fixture
policy. Decoding proves schema validity, not authority authenticity or
cross-version compatibility.
