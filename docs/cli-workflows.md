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
