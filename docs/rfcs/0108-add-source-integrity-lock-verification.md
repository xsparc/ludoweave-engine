# RFC-0108: Add source-integrity lock verification

- **Status:** Accepted
- **Date:** 2026-08-26
- **Decision owners:** LudoWeave maintainers

## Context

M124 checks an explicit bounded manifest and emits normalized source identities,
but its aggregate report is a transient CLI result. A later invocation has no
focused input contract for requiring that the manifest, scene, prefab, and
instance identities remain exactly those previously reviewed. The several
confined reads also do not form an atomic filesystem snapshot.

Current engines distinguish stable resource identity from file location. Godot
documents project resource UIDs and separately documents checksum-triggered
reimport plus version-controlled import metadata. Unity documents stable asset
IDs stored in adjacent metadata so paths may move without breaking references.
Those import systems are broader than this milestone and do not justify adding
discovery, an asset database, or a cache to LudoWeave.

The current PyPA lockfile specification supplies the narrower pattern: an
explicit format version, consistent ordering to minimize diff noise, and exact
hash validation before use. JSON Schema Draft 2020-12 `uniqueItems` validates
structural equality but does not compare derived source identities across two
documents, so exact manifest-to-lock matching remains application logic.

## Decision

Add one versioned data-only contract:

```json
{
  "$schema": "ludoweave.source-lock/1",
  "manifest_id": "game-sources",
  "manifest_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
  "entries": [
    {
      "entry_id": "main",
      "kind": "scene",
      "source_protocol": "ludoweave.scene/1",
      "source_id": "main-scene",
      "source_sha256": "sha256:1111111111111111111111111111111111111111111111111111111111111111"
    }
  ]
}
```

The exact root fields are `$schema`, `manifest_id`, `manifest_sha256`, and
`entries`. A lock has 1-256 entries. Each entry repeats one stable M124 entry
ID, has exact kind `scene` or `prefab`, and binds the accepted source protocol,
stable source ID, and lowercase SHA-256 identity. A prefab entry additionally
requires `instance_protocol`, `instance_id`, and `instance_sha256`; a scene
entry forbids them. Entry IDs are unique and normalize in ascending order.

`SourceLockLimits` may tighten but not enlarge the 64 KiB document and
256-entry hard maxima. `SourceLock.verify()` compares manifest ID/hash, the
entry-ID sequence, then each entry field in a documented deterministic order.
It succeeds silently or raises structured `source_lock.*` errors. The focused
experimental values are exported from `ludoweave.scene`; the engine root is
unchanged.

Add two read-only CLI adapters:

```console
ludoweave source lock PROJECT --manifest FILE
ludoweave source verify PROJECT --manifest FILE --lock LOCK
```

`source lock` invokes the unchanged M124 manifest/source checks and emits only
canonical lock bytes on standard output. It does not choose or write a file.
`source verify` loads one confined bounded expected lock, recomputes the current
lock through the same readers, and requires an exact match. Success emits one
canonical `ludoweave.cli.source-lock-verify/1` document containing status,
manifest ID/hash, and entry count. Existing M123/M124 check output is unchanged.

## Failure, ownership, and determinism

Malformed protocol, field, identity, hash, limit, and conditional-entry values
raise stable content-silent `SceneError` codes. A verification mismatch reports
only the first differing field plus an entry ID when applicable. It never emits
an expected or current hash, project root, lock path, manifest path, or source
path. CLI failure emits no success document and retains exit code 2.

Every project, lock, manifest, scene, prefab, and instance descriptor closes
inside its synchronous reader before a detached immutable value is used. The
commands own no persistent handle, world, renderer, cache, watcher, or
background task and leave the project tree unchanged.

For stable accepted inputs, lock generation and verification are byte-
deterministic. This is not an atomic filesystem snapshot: the expected lock and
current source set are separate sequential reads, so concurrent external
changes remain outside simulation determinism. The SHA-256 values are content
identities, not signatures, provenance, authenticity, authorization, freshness,
or artifact-security proof.

## Boundary and compatibility

M125 adds no directory discovery, recursion, glob, extension routing, implicit
pairing, asset database, import graph, asset/dependency load, compile,
application component schema registration or resolution, cache, reimport,
watcher, live update, write-back, arbitrary script/import/evaluation, remote or
file URI, world/session, command, transaction, world mutation, receipt, runtime
dependency, lock dependency, engine-root export, version change, provider,
renderer, workflow job, workflow allocation, permission, credential, release
authority, tag, release, publication, push, or public remote change. There is no
workflow allocation.

The new persistent protocol and focused Python exports are experimental. A
future incompatible lock shape requires a new protocol identity; existing v1
field meanings cannot change in place. Limits may tighten per call. Supporting
another scene/prefab protocol requires an explicit compatible lock revision or
additive decision rather than accepting unknown values silently.

## Alternatives considered

- Reuse `ludoweave.cli.source-manifest-check/1` as the lock. Rejected because
  aggregate entity/dependency counts are diagnostics, while a focused lock
  should contain only identities required for exact verification.
- Add expected hashes to `ludoweave.source-manifest/1`. Rejected because that
  would change an accepted exact v1 schema in place and mix source selection
  with one observation of its contents.
- Write the lock automatically. Rejected because stdout preserves a read-only
  adapter and lets the caller own persistence, overwrite, and review policy.
- Add an import cache or file watcher. Rejected because identity verification
  needs neither imported artifacts nor persistent lifecycle ownership.
- Sign the lock. Rejected because signer identity, trust roots, key rotation,
  verification policy, and threat model are not defined by this milestone.

## References

- [Godot ResourceUID documentation](https://docs.godotengine.org/en/latest/classes/class_resourceuid.html)
- [Godot import process](https://docs.godotengine.org/en/latest/tutorials/assets_pipeline/import_process.html)
- [Unity asset metadata](https://docs.unity3d.com/Manual/AssetMetadata.html)
- [PyPA `pylock.toml` specification](https://packaging.python.org/en/latest/specifications/pylock-toml/)
- [JSON Schema Draft 2020-12 validation vocabulary](https://json-schema.org/draft/2020-12/json-schema-validation)
- [RFC-0107: explicit source-manifest checking](0107-add-explicit-source-manifest-checking.md)
