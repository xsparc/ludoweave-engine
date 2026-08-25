# RFC-0110: Add source-to-asset dependency checking

- **Status:** Accepted
- **Date:** 2026-08-26
- **Decision owners:** LudoWeave maintainers

## Context

LudoWeave scene and prefab documents already declare direct logical
`asset://` dependencies. M124 supplies one explicit project-confined list of
those source documents, while M126 supplies one explicit bounded
`ludoweave.assets/1` graph. The missing operation is semantic: prove that every
declared source root exists and expose which additional asset-to-asset
dependencies are reachable without reading or building any asset source.

Current primary references make the direct/transitive distinction explicit.
Unity's dependency API offers direct-only and recursive modes, and its current
asset guidance describes loading a complete graph from direct references.
Bazel defines direct and transitive dependencies separately, requires actual
direct dependencies to be declared, and computes a transitive closure for
downstream work. Godot exposes resource dependency inspection separately from
loading and caching. JSON Schema leaves cross-document semantic validation to
the application. These support a declared-graph checker, not inference from
arbitrary application component payloads or an import database.

## Decision

Add this experimental method to the existing `AssetManifest`:

```python
manifest.dependency_closure(roots: tuple[AssetUri, ...]) -> tuple[AssetUri, ...]
```

`roots` must be an exact tuple of distinct exact `AssetUri` values. Every root
must be declared by the manifest. The result contains the roots and all asset
dependencies reachable by any path, exactly once in logical-URI order. Empty
roots produce an empty result. The existing manifest constructor has already
required all asset edges to resolve and the graph to be acyclic; the maximum
graph remains 4,096 assets with 256 dependencies per entry.

Add the read-only CLI composition:

```console
ludoweave source assets PROJECT --manifest config/sources.json --assets config/assets.json
```

The command checks the explicit M124 source manifest and every scene or prefab
through the unchanged project-confined readers, then loads the explicit M126
asset manifest. For each source entry it keeps the source document's direct
declarations separate from the resolved closure. It emits one canonical
document only after all entries succeed:

```json
{
  "protocol": "ludoweave.cli.source-asset-check/1",
  "status": "valid",
  "source_manifest_protocol": "ludoweave.source-manifest/1",
  "source_manifest_id": "game-sources",
  "source_manifest_sha256": "sha256:...",
  "asset_manifest_protocol": "ludoweave.assets/1",
  "asset_manifest_sha256": "sha256:...",
  "entries": [
    {
      "entry_id": "main",
      "kind": "scene",
      "direct": ["asset://materials/player.json"],
      "resolved": [
        "asset://materials/player.json",
        "asset://textures/player.png"
      ]
    }
  ],
  "entry_count": 1,
  "direct_asset_count": 1,
  "resolved_asset_count": 2
}
```

The source-manifest SHA-256 identifies only the normalized explicit source
list. Each reported direct list carries the dependency semantics read from its
source document. The asset-manifest SHA-256 binds the normalized graph used for
resolution. The report is not a replacement for M125 source locks.

## Failure, ownership, and determinism

Invalid roots fail as structured `AssetError` values. If a source document
declares a root absent from the asset manifest, the CLI returns exit 2 with
`tools.missing_asset_dependency`, the first entry ID, and the logical asset
URI. Source entries and their direct dependencies are already normalized, so
failure precedence is deterministic. No success bytes are written on failure.

The existing synchronous readers close each descriptor before the next stage.
No file handle, asset payload, cache entry, watcher, world, renderer, process,
network connection, or background task is retained. The project tree is
unchanged. For stable accepted inputs, report bytes are deterministic.

The command performs several separate reads and is not an atomic filesystem
snapshot. Concurrent external changes remain outside the deterministic
contract. Logical asset URIs may appear in diagnostics; project paths and asset
source paths do not.

## Boundary and compatibility

Direct source declarations mean exactly the `dependencies` field already
present in `ludoweave.scene/1` and `ludoweave.prefab/1`. M127 cannot infer
actual references hidden in application-defined component values. A source
does not repeat indirect asset dependencies: the asset manifest owns those
edges. Extra asset-manifest entries are admitted and there is no unused-asset
rejection or build-inclusion claim.

M127 performs no asset source read, payload decode, asset build, import, cache
use or creation, automatic reimport, component-registry resolution, scene or
prefab compilation, world/session creation, command, transaction, world
mutation, receipt, project write, directory discovery, glob, watcher, live
update, remote access, dependency addition, lock change, metadata or version
change, engine-root export, workflow job, workflow allocation, permission,
credential, release authority, tag, release, publication, push, PR, or remote
change. There is no workflow allocation.

Existing source-check and lock/verify commands and their output protocols are
unchanged. The new method and CLI output are experimental. Any incompatible
report change requires a new protocol identity.

## Alternatives considered

- Require scenes and prefabs to list every transitive asset. Rejected because
  direct declarations and asset-owned graph edges have different ownership;
  repeating indirect edges creates drift.
- Reject unused asset-manifest entries. Rejected because build inclusion,
  shared catalogs, entry points, and dead-asset policy are undefined.
- Infer asset use from component values. Rejected because application schemas
  own those values and there is no universal reference contract.
- Build or open every resolved asset. Rejected because graph checking is a
  read-only semantic preflight, not import, decode, cache, or build execution.
- Add directory discovery. Rejected because both manifests are already
  explicit caller-selected project-relative inputs.

## References

- [Unity `AssetDatabase.GetDependencies`](https://docs.unity3d.com/ScriptReference/AssetDatabase.GetDependencies.html)
- [Unity direct reference asset management](https://docs.unity3d.com/Manual/assets-direct-reference.html)
- [Bazel dependencies](https://bazel.build/concepts/dependencies)
- [Godot `ResourceLoader`](https://docs.godotengine.org/en/stable/classes/class_resourceloader.html)
- [JSON Schema Draft 2020-12 validation vocabulary](https://json-schema.org/draft/2020-12/json-schema-validation)
- [Python `graphlib`](https://docs.python.org/3/library/graphlib.html)
- [ADR-0017: content-addressed project-confined assets](../adr/0017-content-addressed-project-confined-assets.md)
- [RFC-0109: project-confined asset-manifest loading](0109-add-project-confined-asset-manifest-loading.md)
