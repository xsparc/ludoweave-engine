# RFC-0104: Add project-confined scene file loading

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

M119 defines bounded immutable `ludoweave.scene/1` documents and deterministic
transaction planning. M120 adds one-level prefab fragment planning. Python
callers can decode supplied bytes, but loading a scene from a project currently
requires ad hoc filesystem code outside the established M2 path policy.

Local file access is a privilege boundary. RFC 8089 warns that treating local
or non-local file identifiers incorrectly can create privilege-escalation
risks. Python documents that `Path.resolve(strict=True)` removes parent
components and resolves symbolic links, while low-level no-follow facilities
vary across supported operating systems. LudoWeave already has a bounded,
project-relative reader in the `HeadlessProject` composition root; duplicating
that policy in the path-agnostic scene package would create a second and less
tested filesystem boundary.

## Decision

Add `HeadlessProject.load_scene(relative, *, limits=...)`. It accepts one exact
relative path string and one exact immutable `SceneLimits`. The method reuses
the existing project-root resolver and bounded reader with the sanitized role
`scene`, then passes the detached bytes to the unchanged
`SceneDocument.from_json()` decoder.

The file's internal `$schema` value remains the complete format/version
identity. No filename suffix, file URI, manifest registration, directory scan,
or host path becomes canonical state. The loader does not add another scene
schema, parser, component registry, or asset-resolution mechanism.

## Security, failure, and ownership

The established reader rejects absolute, drive-relative, parent-traversal,
alternate-stream, reserved-device, overlong, and resolved root-escape paths.
It accepts only an existing regular file, checks size metadata, and reads at
most `limits.max_bytes + 1` from one descriptor. The descriptor is closed inside
the call. Structured tools errors retain sanitized role/limit context without
including the project root or source path. Malformed and incompatible scene
contents retain the structured M119 `SceneError` and cause chain.

`HeadlessProject` owns only its immutable resolved root and existing
composition records. The load owns one descriptor for the duration of the
synchronous call and owns no persistent handle, source cache, watcher, world,
renderer, provider, thread, or closeable resource afterward. The returned
scene is detached immutable data. Changing or deleting the file cannot alter
that document or any already instantiated entity.

Project-root resolution and bounded reads defend the intended cooperative local
project workflow. They are not a descriptor-confined, race-free sandbox against
a hostile principal concurrently replacing filesystem objects. A future
adversarial multi-principal loader would require a separate platform-specific
security design.

## Determinism and mutation

The same accepted file bytes and exact limits produce the same normalized scene
document and canonical bytes. Filesystem timing, external file changes, and
load order are outside simulation determinism. Applications load source data
before deterministic execution and explicitly choose when to replace their
caller-owned document.

Loading performs no world mutation and produces no receipt because there is no
mutation to acknowledge. A caller must separately invoke `compile_scene()` and
apply the existing ordinary transaction. That later application remains the
only instantiation boundary and produces the standard atomic receipt and local
ID aliases. Asset dependencies remain logical `asset://` identities and are not
loaded.

## Boundary

M121 adds no directory discovery, prefab file loader, include/import graph,
file URI handling, remote path, asset loading, source cache, watcher, live
update, reimport, silent propagation, write-back, arbitrary Python import or
evaluation, new persistent operation, renderer, provider, dependency, lock,
metadata, version, root-package export, workflow, hosted allocation, release
authority, tag, release, publication, or public remote change.
There is no prefab file loader, no file URI handling, no live update, and no
workflow or hosted runner change.

The scene and prefab modules remain unchanged and filesystem-agnostic. The new
method stays in the existing tools composition root and is not promoted into
the deliberately small root API. A standalone installed-wheel verifier
exercises file read, scene decode, explicit planning, transaction application,
and receipt aliases without changing the inherited workflow.

## Consequences

- Python composition can load a project-confined scene file without duplicating
  traversal, regular-file, size, handle, or diagnostic policy.
- Scene format compatibility remains identified by `ludoweave.scene/1`, not a
  platform path or extension.
- A loaded scene remains caller-owned detached data and cannot silently mutate
  world authority.
- Prefab file loading and all source-update semantics remain separate future
  decisions.
- The filesystem confinement claim remains explicitly cooperative rather than
  race-free or multi-principal.

## Alternatives considered

- Put `Path` and file opening in `ludoweave.scene`. Rejected because it would
  violate the path-agnostic downward dependency and duplicate M2 policy.
- Accept arbitrary absolute paths or `file:` URIs. Rejected because the selected
  project root is the explicit authority boundary.
- Discover every scene beneath the project root. Rejected because ambient
  enumeration adds naming, conflict, resource, and stale-cache policy.
- Watch and reimport loaded files. Rejected because live propagation requires
  explicit source identity, conflict, rollback, receipt, and ownership rules.
- Load prefab and scene files through one polymorphic parser. Rejected because
  prefab source/instance pairing and update policy require a separate bounded
  decision.

## References

- [RFC 8089: The file URI Scheme](https://datatracker.ietf.org/doc/html/rfc8089)
- [Python pathlib documentation](https://docs.python.org/3/library/pathlib.html)
- [Python os documentation](https://docs.python.org/3/library/os.html)
- [RFC-0102: data-only scene transaction planning](0102-add-data-only-scene-transaction-planning.md)
- [RFC-0103: one-level prefab fragment planning](0103-add-one-level-prefab-fragment-planning.md)
- [ADR-0012: data-only CLI composition and path confinement](../adr/0012-data-only-cli-composition-and-path-confinement.md)
- [Headless command workflow](../cli-workflows.md)
