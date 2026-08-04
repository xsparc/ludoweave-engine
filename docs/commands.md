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
tokens. Scene operations remain explicitly unsupported because no scene schema
exists yet.

Every session resource must have exactly one explicit role. Only `STATE`
resource schemas participate in authority hashes and patches. Input and
runtime/presentation resources remain outside the hash, are preserved when a
snapshot is loaded into an existing session, and make M2 persistent ticks
ineligible until M4 supplies canonical recorded input.
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
during pre-alpha development.

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
