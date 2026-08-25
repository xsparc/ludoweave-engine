# RFC-0109: Add project-confined asset-manifest loading

- **Status:** Accepted
- **Date:** 2026-08-26
- **Decision owners:** LudoWeave maintainers

## Context

LudoWeave already has an experimental `ludoweave.assets/1` manifest and a
synchronous `AssetPipeline`, but file loading is owned only by
`AssetManifest.load(Path)`. The headless project composition root cannot apply
its established portable path confinement and bounded handle reader to this
existing manifest. M119-M125 scene and prefab documents may declare logical
`asset://` dependencies, but connecting those declarations to an asset
manifest is a separate semantic operation.

Current game engines make the same boundary visible even though their complete
systems are broader. Godot exposes resource dependency inspection separately
from loading, importing, caching, and directory listing. Unity distinguishes
direct from recursive dependency queries; its Asset Database also owns import
and cached derived data. Those systems support preserving an explicit
dependency-document boundary, but do not justify bringing discovery, import,
or caching into this loader.

JSON Schema Draft 2020-12 supplies structural assertions while explicitly
leaving application semantics to application code. The current PyPA lockfile
specification similarly uses explicit format versions and consistent ordering
for reproducible dependency documents. M126 therefore establishes only a safe
loader foundation; source-to-asset dependency checking remains a later
decision.

## Decision

Retain the exact existing manifest shape:

```json
{
  "protocol": "ludoweave.assets/1",
  "assets": [
    {
      "uri": "asset://textures/player.png",
      "kind": "png",
      "source": "assets/player.png",
      "settings": {"srgb": true},
      "dependencies": []
    }
  ]
}
```

Add focused experimental `ASSET_MANIFEST_PROTOCOL` and
`AssetManifestLimits`. Limits may tighten but not enlarge these hard maxima:

- 4 MiB of UTF-8 JSON;
- 4,096 asset entries;
- 256 dependencies per asset; and
- 128 scalar settings per asset.

Root and entry fields remain exact. JSON object keys are unique, numeric
constants are finite, asset URIs and project-relative sources retain their
existing validation, logical URIs remain unique, declared dependencies must
exist, and dependency cycles fail. Empty manifests remain accepted for
compatibility with the existing constructor.

`AssetManifest.from_json()` decodes caller-owned detached bytes or text.
`AssetManifest.load()` retains its public path-based API, performs a bounded
handle read, and delegates to the same decoder. `as_dict()` and
`canonical_bytes()` normalize entries by logical URI, settings by key, and
dependencies by logical URI without reading an asset source.

The internal composition root adds:

```python
HeadlessProject.load_asset_manifest(relative, *, limits=...)
```

It resolves the caller-selected file through the existing project-confined
regular-file reader, caps the open descriptor at `max_bytes`, closes it, and
then returns the manifest value. The manifest retains the resolved project root
because the pre-existing `source_path()` and `AssetPipeline` APIs require that
composition context; it retains no open descriptor.

## Failure, ownership, and determinism

Limit, JSON, protocol, field, URI, source-path, dependency, and cycle failures
remain structured `AssetError` or composition-root errors with stable codes and
content-silent path context. Project confinement rejects traversal, absolute,
drive-relative, alternate-stream, reserved-device, trailing-space/dot, and
escaping symlink forms before the asset-manifest decoder.

Each manifest descriptor closes inside its synchronous reader. M126 performs
no asset source read, no asset build, no cache creation or write, and owns no
watcher, world, renderer, process, network connection, or background task.
For a stable project root and accepted manifest bytes, decoded entries and
canonical output are deterministic.

Project confinement is a cooperative local-project boundary, not a race-free
filesystem sandbox. The returned manifest can later resolve caller-requested
source paths through the existing API; M126 itself neither requests nor opens
one.

## Boundary and compatibility

M126 adds no directory discovery, recursion, glob, extension routing,
source-manifest integration, source-to-asset dependency resolution, asset
source read, import, decode, build, cache use, cache write, watcher, reimport,
live update, source write-back, remote or file URI, component schema
resolution, scene/prefab compile, world/session, command, transaction, world
mutation, receipt, runtime dependency, lock dependency, engine-root export,
version change, CLI command, workflow job, workflow allocation, permission,
credential, release authority, tag, release, publication, push, PR, or remote
change. There is no workflow allocation.

The exact `ludoweave.assets/1` fields and meanings do not change. The existing
path-based loader remains. The new protocol constant, limits, detached decoder,
canonical methods, and focused project loader are experimental. A future
incompatible manifest shape requires a new protocol identity rather than
changing v1 in place.

## Alternatives considered

- Add source dependency checking in the same milestone. Rejected because
  direct-versus-transitive policy, unused declarations, report shape, and
  failure disclosure require their own decision and evidence.
- Build every declared asset while loading. Rejected because loading a manifest
  is structural input validation, not import or cache mutation.
- Discover the default asset manifest. Rejected because callers already own
  project-relative input selection and discovery policy is undefined.
- Replace `AssetManifest.load()`. Rejected because the existing public API can
  delegate to the bounded decoder without a parallel format.
- Move asset manifests into `ludoweave.scene`. Rejected because logical assets,
  their sources, and their dependency graph remain an independent focused
  package.

## References

- [Godot `ResourceLoader`](https://docs.godotengine.org/en/stable/classes/class_resourceloader.html)
- [Unity `AssetDatabase.GetDependencies`](https://docs.unity3d.com/ScriptReference/AssetDatabase.GetDependencies.html)
- [PyPA `pylock.toml` specification](https://packaging.python.org/en/latest/specifications/pylock-toml/)
- [JSON Schema Draft 2020-12 validation vocabulary](https://json-schema.org/draft/2020-12/json-schema-validation)
- [Python `json`](https://docs.python.org/3/library/json.html)
- [Python `pathlib`](https://docs.python.org/3/library/pathlib.html)
- [ADR-0017: content-addressed project-confined assets](../adr/0017-content-addressed-project-confined-assets.md)
- [RFC-0108: source-integrity lock verification](0108-add-source-integrity-lock-verification.md)
