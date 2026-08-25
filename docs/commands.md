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
