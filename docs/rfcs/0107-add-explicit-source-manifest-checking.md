# RFC-0107: Add explicit source-manifest checking

- **Status:** Accepted
- **Date:** 2026-08-26
- **Decision owners:** LudoWeave maintainers

## Context

M119-M122 define versioned scene/prefab data and project-confined explicit file
loading. M123 checks one scene or one prefab source/instance pair from the CLI.
Checking several known project inputs still requires separate commands and
caller-owned aggregation. Recursive discovery is intentionally absent because
its ordering, conflict, exclusion, and cache policy are undefined.

Current game-engine command lines support explicit project and headless/batch
boundaries. Godot documents explicit `--path`, `--headless`, and import
operation. Unity documents `-projectPath`, `-batchmode`, and an explicit saved
build-profile asset. Neither establishes that LudoWeave should run arbitrary
project scripts or discover every file. JSON Schema Draft 2020-12 supplies
structural object/array bounds and uniqueness assertions but distinguishes
structural validity from application-owned semantic validation.

## Decision

Add one versioned data-only contract:

```json
{
  "$schema": "ludoweave.source-manifest/1",
  "manifest_id": "game-sources",
  "entries": [
    {"entry_id": "main", "kind": "scene", "source": "scenes/main.json"},
    {
      "entry_id": "scout",
      "kind": "prefab",
      "source": "prefabs/scout.json",
      "instance": "prefabs/scout-one.json"
    }
  ]
}
```

The exact root fields are `$schema`, `manifest_id`, and `entries`. A manifest
has 1-256 entries. Each stable unique entry ID selects exact kind `scene` or
`prefab`, uses normalized forward-slash project-relative paths, and has a
1,024-byte path limit. Scene entries have one `source`; prefab entries also
require one explicit `instance`. Exact repeated references fail. Entries
normalize by ID, and canonical bytes provide a stable manifest identity.

`SourceManifestLimits` may tighten but not enlarge the 64 KiB document,
256-entry, and 1,024-byte path maxima. The focused experimental values are
exported from `ludoweave.scene`; the root package is unchanged.

Add one CLI mode:

```console
ludoweave source check PROJECT --manifest FILE
```

It is mutually exclusive with M123's single-source modes. The composition root
loads the manifest through the established bounded project-relative reader.
Each entry then uses the unchanged M121 scene or M122 prefab readers; prefab
pairs require exact `prefab_id` agreement.

Success emits canonical `ludoweave.cli.source-manifest-check/1` JSON. It
contains manifest protocol/ID/hash, entry-ID-ordered source results, and
aggregate entry/kind/entity/override/dependency counts. It never contains the
project root, manifest path, or source paths.

## Failure, ownership, and determinism

Manifest JSON, protocol, field, ID, limit, and portable-path failures are
structured `SceneError` values with stable `source_manifest.*` codes and
content-silent context. Existing project/source failures retain their codes and
cause chains. A failed entry emits no success document, returns exit 2, and
does not mutate the project.

Each synchronous reader closes its owned descriptor before returning its
detached immutable value. The command owns no persistent handle or background
resource. For the same stable project files and limits, normalization and
output bytes are deterministic. Sequential reads do not form an atomic
filesystem snapshot; concurrent external changes and filesystem timing remain
outside simulation determinism.

## Boundary

The explicit manifest is not directory discovery, globbing, extension routing,
an asset database, a component registry, or an import graph. The command
performs no compile or application-specific component semantic validation,
creates no world or session, calls no planner or transaction service, applies
no command, performs no world mutation, writes no project or report file, and
produces no receipt. Asset dependencies remain unresolved logical identities.

M124 adds no recursion, implicit pairing, nested prefab composition,
dependency traversal, asset loading, cache, watcher, live update/reimport,
write-back, arbitrary script/import/evaluation, remote/file URI, persistent
operation, runtime dependency, lock change, engine-root export, version change,
provider, renderer, workflow job, workflow allocation, permission, credential,
release authority, tag, release, publication, push, or public remote change.
There is no workflow allocation.

## Alternatives considered

- Run one command per source. Retained for focused checks, but rejected as the
  only batch path because callers would have to invent ordering and aggregation.
- Discover all matching files. Rejected because recursion, exclusions,
  duplicate source identity, extension policy, and resource bounds are not
  defined by the project.
- Use the project manifest as an implicit source registry. Rejected because the
  M2 project manifest identifies runtime composition and should not become a
  second evolving authoring database.
- Compile every entry. Rejected because the data-only headless project has no
  application component registry and compilation changes the trust boundary.
- Persist the report. Rejected because standard output keeps the operation
  demonstrably read-only and avoids overwrite/atomicity policy.
- Hash raw files. Rejected because accepted semantically equivalent JSON should
  share the normalized canonical identity already used by M123.

## References

- [Godot command-line tutorial](https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html)
- [Unity command-line build documentation](https://docs.unity3d.com/Manual/build-command-line.html)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)
- [JSON Schema validation vocabulary](https://json-schema.org/draft/2020-12/json-schema-validation)
- [Python argparse documentation](https://docs.python.org/3/library/argparse.html)
- [Python hashlib documentation](https://docs.python.org/3/library/hashlib.html)
- [Python JSON documentation](https://docs.python.org/3/library/json.html)
- [RFC-0104: project-confined scene file loading](0104-add-project-confined-scene-file-loading.md)
- [RFC-0105: project-confined prefab file loading](0105-add-project-confined-prefab-file-loading.md)
- [RFC-0106: read-only source-check CLI](0106-add-read-only-source-check-cli.md)
