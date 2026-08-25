# RFC-0111: Add asset-source lock verification

- **Status:** Accepted
- **Date:** 2026-08-26
- **Decision owners:** LudoWeave maintainers

## Context

M124-M125 provide an explicit source list and canonical content identities for
the selected scene and prefab documents. M126 provides one explicit normalized
asset manifest, and M127 resolves source-declared direct roots through that
asset graph. None of those operations reads the resolved asset sources. The M4
`AssetPipeline` can read, decode, build, and cache assets, but invoking a
mutating build solely to establish input identity would mix two responsibilities.

Current primary references separate these concerns. Unity 6.2 records original
source assets and imported counterparts separately; its dependency hash
aggregates source path/content, metadata, target platform, and importer version.
Godot checks source-asset content and automatically reimports when that checksum
changes. Bazel describes declared action inputs and content hashes separately
from action-cache and content-addressed output storage. Python's `hashlib`
supports binary file hashing while leaving handle closure to the caller. These
support one bounded input lock, not an import database, output artifact, or
automatic cache/reimport system.

## Decision

Add these experimental focused-assets contracts:

```python
ASSET_SOURCE_LOCK_PROTOCOL = "ludoweave.asset-source-lock/1"
AssetSourceLockLimits
AssetSourceLockEntry
AssetSourceLock
```

The exact lock document is:

```json
{
  "$schema": "ludoweave.asset-source-lock/1",
  "source_lock_sha256": "sha256:...",
  "asset_manifest_sha256": "sha256:...",
  "roots": ["asset://materials/player.json"],
  "entries": [
    {
      "uri": "asset://materials/player.json",
      "kind": "json",
      "source_sha256": "sha256:...",
      "source_bytes": 19
    }
  ]
}
```

`source_lock_sha256` hashes the canonical current M125 `SourceLock`, binding the
explicit list plus accepted scene/prefab and instance identities.
`asset_manifest_sha256` hashes the canonical M126 manifest, binding logical
URIs, source names, kinds, settings, and asset-to-asset edges. `roots` is the
unique URI-sorted union of source-declared direct assets. `entries` is the exact
M127 closure, unique and URI-sorted, with each source's raw-byte length and
SHA-256. Roots must be present in entries. A valid empty closure has empty roots
and entries.

The lock decoder accepts only exact fields, rejects duplicate JSON members,
requires canonical lowercase SHA-256 text, and has tightening-only limits of
1 MiB JSON, 4,096 roots, and 4,096 entries. Each source is limited to 256 MiB;
the accepted aggregate is limited to 1 GiB.

Add two read-only commands:

```console
ludoweave source asset-lock PROJECT --manifest config/sources.json --assets config/assets.json
ludoweave source asset-verify PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json
```

Generation reuses M124 source inspection, M125 canonical source identity, M126
asset-manifest loading, and M127 root/closure semantics. It hashes selected
asset sources in URI order through the existing project-confined regular-file
reader. Success writes the canonical lock to stdout only after every selected
source succeeds; the CLI does not persist it.

Verification loads one confined expected lock, recomputes current identity, and
compares source-lock hash, asset-manifest hash, roots, entry URIs, then per-entry
kind, source hash, and byte count. Success emits canonical
`ludoweave.cli.asset-source-lock-verify/1` with only protocol and counts.

## Ownership, limits, and failure behavior

Every asset source is opened read-only, required to be a regular confined file,
hashed in 64 KiB blocks, and closed before the next URI. Payload bytes are not
retained. A source that is missing/unavailable or over 256 MiB fails with its
logical URI and stable cause code but no path. Accepted bytes over 1 GiB fail
with the current URI and public limit. No success bytes precede full success.

Lock mismatch uses `asset_source_lock.mismatch`, the first stable field, and an
optional logical URI. It never discloses expected/actual hashes, byte counts,
or source paths. All values are immutable and caller-owned. The project remains
unchanged and no descriptor, payload, task, or process is retained.

Multiple source reads are not an atomic filesystem snapshot. Concurrent source
changes are outside the deterministic contract. For stable accepted inputs,
generation and verification bytes are deterministic.

## Boundary and compatibility

M128 is repeatable input identity only. It is not a signature, provenance,
authenticity, authorization, freshness, imported-artifact identity, build
reproducibility result, or cache key. The normalized manifest hash deliberately
binds source names, but the lock report and mismatch errors do not disclose
them.

There is no asset decode, no asset build, no import, no cache read, no cache
write, no artifact creation, no automatic reimport, no watcher, and no live
update. M128 adds no directory discovery, glob, default manifest, unused-asset
rejection, build-inclusion policy, component-reference inference, component
registry, scene/prefab compile, world/session, command, transaction, world
mutation, receipt, project write, remote access, dependency, metadata, version,
engine-root export, workflow job, workflow allocation, permission, credential,
release authority, tag, release, publication, push, PR, or remote change. There
is no workflow allocation.

Existing M125 locks, M127 reports, M4 pipeline artifacts, and their protocols
are unchanged. Any incompatible asset-source lock or verification-result change
requires a new protocol identity.

## Alternatives considered

- Run `AssetPipeline.build()` to obtain its source hash. Rejected because that
  also decodes payloads, creates directories, and writes cache artifacts.
- Put raw source paths in the lock. Rejected because manifest identity already
  binds them and portable diagnostics do not need host paths.
- Lock every manifest entry. Rejected because M127 deliberately distinguishes
  selected closure from admitted unused/shared catalog entries.
- Add automatic reimport or a watcher. Rejected because a persistent lifecycle,
  invalidation scheduling, safe points, and failure recovery are undefined.
- Claim an atomic input snapshot. Rejected because sources are opened
  sequentially; stable inputs remain a documented caller responsibility.

## References

- [Unity 6.2 Asset Database](https://docs.unity3d.com/6000.2/Documentation/Manual/AssetDatabase.html)
- [Unity 6.2 `AssetDatabase.GetAssetDependencyHash`](https://docs.unity3d.com/6000.2/Documentation/ScriptReference/AssetDatabase.GetAssetDependencyHash.html)
- [Godot stable import process](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html)
- [Bazel remote caching](https://bazel.build/remote/caching)
- [Python `hashlib`](https://docs.python.org/3/library/hashlib.html)
- [ADR-0017: content-addressed project-confined assets](../adr/0017-content-addressed-project-confined-assets.md)
- [RFC-0108: source-integrity lock verification](0108-add-source-integrity-lock-verification.md)
- [RFC-0110: source-to-asset dependency checking](0110-add-source-to-asset-dependency-checking.md)
