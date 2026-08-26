# Headless command workflow

M2 provides a deliberately data-only CLI composition for exercising the typed
command, snapshot, replay, and diff protocols. It is not yet a general game
project format: components, resources, scenes, assets, and Python plugins are
not loaded from the manifest.

Create `ludoweave.project.json` in a project directory:

```json
{
  "dependency_lock_hash": "sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "platform_profile": "cpython-portable-empty-v1",
  "protocol": "ludoweave.headless-project/1",
  "seed": "000000000000002a",
  "world_id": "example-world"
}
```

Create a project-relative `transaction.json` using the canonical command
protocol. This example spawns one empty entity and advances one deterministic
no-op tick:

```json
{
  "commands": [
    {
      "actor": {"id": "example", "kind": "human"},
      "arguments": {"alias": "subject", "components": []},
      "command_id": "example-spawn",
      "operation": "entity.spawn",
      "operation_version": 1,
      "protocol": "ludoweave.command/1",
      "transaction_id": "example-transaction"
    },
    {
      "actor": {"id": "example", "kind": "human"},
      "arguments": {"count": 1},
      "command_id": "example-tick",
      "operation": "world.tick",
      "operation_version": 1,
      "protocol": "ludoweave.command/1",
      "transaction_id": "example-transaction"
    }
  ],
  "dry_run": false,
  "protocol": "ludoweave.transaction/1",
  "world_id": "example-world"
}
```

Run the workflow from any directory. Artifact arguments remain relative to the
selected project:

```console
ludoweave apply PROJECT transaction.json --snapshot-out after.lws --receipt-out receipt.json --replay-out run.lwr
ludoweave snapshot PROJECT run.lwr --tick 0 --out before.lws
ludoweave replay PROJECT run.lwr --verify-hashes --snapshot-out replayed.lws
ludoweave snapshot PROJECT run.lwr --tick 1 --out tick-1.lws
ludoweave diff PROJECT before.lws after.lws
```

`apply` writes snapshot/replay outputs only for a committed receipt and exits 2
for a rejected receipt. A dry-run returns its canonical proposed receipt with
exit 0 and does not write state or replay output. `replay --verify-hashes` verifies every reached batch
and checkpoint. `snapshot` requires an exact recorded tick boundary and includes
all ordered work at that tick. Success documents are canonical JSON on stdout;
expected failures are versioned JSON diagnostics on stderr.

Absolute artifact paths, traversal outside `PROJECT`, Windows drive-relative
paths, and symlink escapes are rejected. The selected project directory itself
may be absolute because it is the explicit confinement root.

CLI snapshots carry the manifest-derived project-schema, dependency-lock, and
platform-profile binding and are rejected by a different selected project.
Inputs are read from one open file handle with a `limit + 1` cap, so stale size
metadata cannot trigger an unbounded allocation. The confinement policy assumes
the selected project tree is not being concurrently replaced by a hostile local
principal; see the security policy.

## Programmatic scene-file loading

M121 reuses this exact project-root policy for explicit Python composition:

```python
from pathlib import Path

from ludoweave.tools.headless_project import HeadlessProject

project = HeadlessProject.load(Path("PROJECT"))
scene = project.load_scene("scenes/main.json")
```

This does not add a CLI subcommand and does not load scenes from the project
manifest. The caller supplies one relative path. The synchronous read is
bounded by the exact scene limits, closes its handle, and returns a detached
immutable `ludoweave.scene/1` document. It performs no world mutation; explicit
planning and transaction application remain separate. There is no directory
discovery, prefab file loader, file URI, watcher, live update, write-back, or
remote path support.

M122 applies the same policy to two explicit prefab files:

```python
prefab = project.load_prefab("prefabs/scout.prefab.json")
instance = project.load_prefab_instance("prefabs/scout.instance.json")
```

There is no implicit pairing or directory discovery. Both loads are detached
and perform no world mutation; callers separately compile the pair and apply
the ordinary transaction. There is no cache, live update, or CLI workflow
change.

## Read-only source preflight

M123 exposes the bounded readers as a structured CLI check:

```console
ludoweave source check PROJECT --scene scenes/main.json
ludoweave source check PROJECT --prefab prefabs/scout.json --instance prefabs/scout-one.json
```

Scene mode checks one `ludoweave.scene/1` document. Prefab mode takes two
explicit files, checks both M120 protocols, and rejects a mismatched
`prefab_id`. Success writes one canonical `ludoweave.cli.source-check/1` JSON
document to standard output with stable source identities, canonical SHA-256
identities, and bounded counts. Structured project/path/protocol failures use
the normal exit code 2 and JSON error document on standard error.

The preflight has no compile, component-registry resolution, asset loading,
world mutation, or receipt. It writes no project file and adds no directory
discovery, implicit pairing, cache, watcher, live update, arbitrary script, or
workflow allocation. It is suitable for local hooks and existing CI commands
without adding a hosted job. There is no workflow allocation.

M124 adds an explicit batch-shaped input without adding discovery:

```console
ludoweave source check PROJECT --manifest config/sources.json
```

The bounded `ludoweave.source-manifest/1` file contains one stable manifest ID
and a nonempty list of entries. Each entry has a stable ID and names either one
normalized project-relative scene or one explicit prefab source/instance pair.
Entries normalize by ID; duplicate IDs and exact duplicate references fail.
Manifest, scene, and prefab paths are never emitted.

Success writes canonical `ludoweave.cli.source-manifest-check/1` JSON with the
manifest protocol/ID/hash, ordered per-entry source results, and aggregate
entry, kind, entity, override, and dependency counts. Any invalid or missing
entry returns exit 2 with the existing structured error and no success report.
Every opened file is closed before return, and the project tree is unchanged.

This explicit manifest is not a directory scan, glob, implicit pairing,
compile/import, component-registry check, or asset load. It creates no world or
session, applies no command or transaction, performs no world mutation, writes
no report file, and produces no receipt. Multiple reads are not an atomic
filesystem snapshot, so deterministic output requires stable inputs during the
check. There is no cache, watcher, live update, dependency, new hosted job, or
workflow allocation.

## Source-integrity lock and verification

M125 turns the normalized M124 content identity into an explicit reusable
document without adding file discovery or an import database:

```console
ludoweave source lock PROJECT --manifest config/sources.json
ludoweave source verify PROJECT --manifest config/sources.json --lock config/sources.lock.json
```

`source lock` checks every explicit source exactly as M124 does and writes one
canonical `ludoweave.source-lock/1` document to standard output. The document
contains the manifest ID/hash and entry-ID-ordered source protocol, stable ID,
and SHA-256 identity fields. Prefab entries also bind the explicit instance
protocol, ID, and hash. It contains no project root or source path. The CLI does
not write the lock file; callers choose whether and where to persist stdout.

`source verify` loads one project-confined bounded lock, computes the current
lock through the same readers, and requires an exact field match. Success emits
canonical `ludoweave.cli.source-lock-verify/1` JSON. A mismatch returns exit 2,
emits no success document, and identifies only the entry and field, never an
expected/current hash or path.

The lock records content identity; it is not an atomic filesystem snapshot,
signature, authenticity proof, dependency resolver, or asset import result.
Sequential reads require stable inputs. Both commands close every descriptor,
perform no import or compile, use no cache, create no world/session, perform no
world mutation, produce no receipt, and add no workflow allocation.

## Source-to-asset dependency checking

M127 connects the explicit source list to one explicit asset manifest without
loading an asset source:

```console
ludoweave source assets PROJECT --manifest config/sources.json --assets config/assets.json
```

The command checks every M124 source entry through the unchanged readers, then
loads the bounded M126 `ludoweave.assets/1` document. Every source-declared
direct `asset://` URI must exist. Canonical
`ludoweave.cli.source-asset-check/1` output lists each source entry's direct
declarations and a separate `resolved` list containing those roots plus all
reachable asset-to-asset dependencies. Entry IDs and URI lists are stable and
sorted; aggregate direct and resolved counts are unique across entries.

This is declared-graph checking, not asset-use inference. Application-defined
component values are not inspected for hidden references, indirect assets need
not be repeated in the scene or prefab, and unused asset-manifest entries do
not fail. There is no asset source read, payload decode, build, import, cache,
compile, world/session, mutation, receipt, write, discovery, watcher, live
update, or workflow allocation. Sequential reads require stable inputs and are
not an atomic filesystem snapshot.

## Asset-source lock generation and verification

M128 records the raw input identity of only the M127-selected asset closure:

```console
ludoweave source asset-lock PROJECT --manifest config/sources.json --assets config/assets.json > config/assets.lock.json
ludoweave source asset-verify PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json
```

The first command writes canonical `ludoweave.asset-source-lock/1` to stdout;
the CLI does not choose or write the redirected file. The document binds the
canonical source lock and asset manifest, unique direct roots, and URI-sorted
resolved entries with kind, byte count, and SHA-256. An empty selected closure
produces empty roots and entries.

The second command loads one project-confined expected lock, recomputes the
same current identities, and emits `ludoweave.cli.asset-source-lock-verify/1`
only after an exact match. Mismatch output contains only the first stable field
and optional logical URI, never expected/actual hashes, sizes, or source paths.

Each source is a confined regular file streamed through an owned descriptor in
64 KiB blocks, limited to 256 MiB with 1 GiB accepted aggregate. There is no
asset decode, no asset build, no import, no cache write, no artifact creation,
no world mutation, and no workflow allocation. Sequential reads are not an
atomic filesystem snapshot; locks are input identity, not provenance,
authenticity, freshness, imported artifacts, or build reproducibility.

## Verified asset build-plan generation

M129 turns the verified M128 inputs into prospective dependency-first work:

```console
ludoweave source asset-plan PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json
```

The command reloads the expected project-confined lock, recomputes current
source and asset identities through M124-M128, and requires an exact match
before planning. Canonical `ludoweave.asset-build-plan/1` output binds the lock
and manifest hashes, sorted direct roots, and every selected asset once after
its dependencies. Logical URI breaks ready-set ties.

Each entry records kind, settings, source identity/size, direct dependency
URIs, and the exact prospective M4 cache key. Output is emitted only after the
complete plan validates. This is not asset decode, asset build, cache read,
cache write, artifact creation, scheduler execution, provenance, or build-
success proof. The project remains unchanged and there is no workflow
allocation.

## Saved asset build-plan verification

M130 verifies an explicit saved M129 plan against freshly recomputed inputs:

```console
ludoweave source asset-plan-verify PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json
```

The plan loads through project confinement and strict bounded decoding. The CLI
then recomputes M128 source identities, requires the supplied lock to match,
regenerates the M129 plan, and performs an exact content-silent comparison.
Success is canonical `ludoweave.cli.asset-build-plan-verify/1` with only
protocol/status and aggregate counts. Failure emits no success bytes and no
compared hash, size, key, settings value, or path.

The CLI does not execute the plan, decode or build an asset, consult or write a
cache, create an artifact, import/reimport, schedule work, discover files, or
mutate the project. Sequential source verification remains non-atomic and
there is no workflow allocation.

## Bounded in-memory asset plan execution

M131 executes only the built-in decoders after the M130 verification chain:

```console
ludoweave source asset-build PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json
```

The saved plan loads first. Current sources are then hashed for M128 lock
verification, the M129 plan is regenerated and compared, and every selected
source is acquired again through the confined bounded reader into immutable
bytes. The executor verifies exact URI order, source counts, hashes, and
aggregate bounds before any built-in decoder runs. A change between hashing
and acquisition therefore fails without success output.

Success is canonical `ludoweave.asset-build-result/1`. It binds the plan hash,
loader protocol, aggregate byte counts, and each plan-ordered URI/kind/cache
key plus decoded artifact SHA-256 and byte count. Payload bytes are not
retained or printed. Repeated stable inputs produce byte-identical output.

There is no cache read, no cache write, no persisted artifact, no project
write, no atomic publication, no worker, plugin, discovery, watcher, reimport,
renderer upload, world mutation, receipt, or workflow allocation. Sequential
source acquisition is not an atomic filesystem snapshot.

## Verified local asset cache publication

M132 adds an explicit local cache effect after complete M131 materialization:

```console
ludoweave source asset-cache PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --cache ../ludoweave-cache
```

`--cache` is caller authority and must identify a root outside and not above the
project. No cache location is read from project data. The command loads the
saved plan, recomputes and verifies current inputs, verifies the regenerated
plan, acquires detached sources, and completes every bounded decoder before it
creates the cache store.

Payloads are stored once by artifact SHA-256 in the local CAS. Canonical
`ludoweave.asset-cache-entry/1` action metadata becomes visible afterward by
atomic per-entry directory replacement under the existing cache key. Existing
entries count as `reused` only after exact metadata, size, and payload-digest
verification. New entries count as `published`. Success is one path-free
canonical `ludoweave.asset-cache-publish/1` document.

Corrupt, incomplete, or aliased content fails closed without overwrite or
repair. Still-owned staging paths are removed. A valid unreferenced CAS blob or
an earlier valid entry can remain after a later filesystem failure, but neither
constitutes a partial cache hit. The project remains byte-for-byte unchanged.

There is no remote cache, network, authentication, eviction, deletion, quota,
watcher, reimport, worker, plugin, world mutation, receipt, or CI change.

## Verified read-only asset cache lookup

M133 inspects only cache actions from one exact current verified plan:

```console
ludoweave source asset-cache-check PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --cache ../ludoweave-cache
```

The command revalidates current sources, lock, manifest, and plan before it
opens `--cache` with no write authority. An absent cache root or action produces
a plan-ordered miss without creating a directory. A present action is a hit
only after duplicate-free exact canonical metadata matches the current plan
entry and its ordinary CAS payload matches the declared bounded byte count and
SHA-256. The path-free result uses `ludoweave.asset-cache-lookup/1`.

Present corruption fails closed and produces no success document. The command
does not rewrite, repair, delete, publish, or intentionally update cache data;
the project also remains unchanged. This is verified lookup evidence only:
there is no cache-assisted execution, decoder bypass, remote cache, discovery,
worker, plugin, world mutation, receipt, or CI change.

## Read-only cache-assisted asset realization

M134 reuses verified hits and decodes exact misses without publishing them:

```console
ludoweave source asset-realize PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --cache ../ludoweave-cache
```

The complete current lock and plan are verified and all detached sources are
acquired before the cache is opened read-only. Every source is preflighted
before the first cache read; every current-plan cache candidate is verified
before the first miss decoder. Success is path-free canonical
`ludoweave.asset-build-realization/1` evidence with plan-ordered `hit` or
`decoded` statuses. A missing cache remains absent and no cache or project
write occurs.

## Explicit post-realization cache population

M135 makes the later cache effect a separate explicit command:

```console
ludoweave source asset-cache-populate PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --cache ../ludoweave-cache
```

The command completes the same current lock/plan verification and confined
source acquisition, opens the explicit cache without write authority, and
finishes M134 realization. Only then does it open the resolved cache root with
write authority and invoke the unchanged M132 publisher. Cold runs report
decoded/published entries; warm runs report verified hit/reused entries; mixed
runs preserve exact plan order. Success is canonical
`ludoweave.asset-cache-population/1` evidence and the project remains
unchanged.

A source, cache-integrity, decoder, or limit failure before publication leaves
an absent cache absent. Publication remains atomic per entry, not across the
whole plan: if a later filesystem publication fails, earlier valid entries or
valid unreferenced CAS blobs may remain and no M135 success report is emitted.
There is no rollback, repair, deletion, eviction, remote cache, worker, plugin,
world mutation, receipt, or CI change.

## Saved cache-population verification

M136 verifies saved M135 evidence against exact current source, plan, and cache
state without changing any of them:

```console
ludoweave source asset-cache-population-verify PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --population config/population.json --cache ../ludoweave-cache
```

The project-confined population file is limited to 8 MiB and 4,096 entries.
Its JSON decoder rejects duplicate, unknown, missing, wrongly typed, or
inconsistent fields and normalizes valid input back to the canonical
`ludoweave.asset-cache-population/1` shape. Current source-lock and saved-plan
verification completes first. The verifier then checks the report's complete
plan/order/input identity before opening the explicit cache read-only.

Every action must exist and pass canonical metadata, current-plan field,
ordinary-file, bounded byte-count, and CAS SHA-256 validation. Its complete
result identity must equal the saved entry. Success is path-free canonical
`ludoweave.asset-cache-population-verification/1`; missing, corrupt, or
mismatched entries emit no success document and trigger no decoder, fallback,
repair, or write. A missing cache remains absent.

The saved report is unsigned local integrity evidence. Verification does not
prove that its historical statuses occurred and is not provenance,
authenticity, a builder identity, or a trusted timestamp. There is no remote
cache, signature/attestation policy, worker, world mutation, receipt, or CI
change.

## Bounded local-cache inventory

M137 verifies and classifies the complete engine-owned local cache without
changing it:

```console
ludoweave source asset-cache-inventory PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --cache ../ludoweave-cache
```

Current source-lock and exact saved-plan verification completes before the
external cache is opened read-only. The scan admits at most 16,384 actions,
16,384 CAS blobs, 64 MiB of canonical metadata, and 1,073,741,832 CAS bytes—the
existing maximum valid single artifact. It rejects unknown layout, symlinks/
junctions/reparse objects, ambiguous or noncanonical action JSON, location/key
drift, CAS name/content mismatch, missing action blobs, current-plan identity
drift, and active-limit excess.

Success emits aggregate path-free
`ludoweave.asset-cache-inventory/1` current/missing/other action and CAS storage
evidence. Every admitted CAS blob is streamed and hashed once. An absent cache
is a valid empty observation and remains absent.

`unreferenced_blobs` means no action record observed in this sequential scan
referenced those blobs. It is not deletion eligibility: there is no atomic
snapshot, lease, retention policy, last-use evidence, or concurrent-writer
guarantee. The command has no cleanup, write, repair, eviction, decoder,
fallback, remote cache, or CI effect.
