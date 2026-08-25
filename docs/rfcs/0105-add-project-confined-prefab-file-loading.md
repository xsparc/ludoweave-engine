# RFC-0105: Add project-confined prefab file loading

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

M120 defines bounded immutable prefab source and instance records plus explicit
deterministic compilation. M121 establishes one project-confined scene-file
reader in the existing headless composition root. Prefab callers still need ad
hoc filesystem code to supply the two M120 records.

General resource loaders commonly accumulate registered format handlers,
directory listing, dependency traversal, caching, and threaded loading. Godot's
current `ResourceLoader` documents those capabilities and also warns that one
directory-listing result is not deterministically ordered. Unity's current
prefab overview likewise describes source-instance relationships and nested or
variant composition. Those are useful editor/resource-system capabilities, but
they exceed this bounded headless slice. RFC 8089 also reinforces that local
file identifiers require an explicit authority boundary.

## Decision

Add two explicit methods to `HeadlessProject`:

- `load_prefab(relative, *, limits=...)` loads one
  `ludoweave.prefab/1` source.
- `load_prefab_instance(relative, *, limits=...)` loads one
  `ludoweave.prefab-instance/1` instance.

Each accepts one exact relative path and exact immutable `PrefabLimits`. Each
reuses the M121 project-root resolver and bounded reader with a sanitized role,
then delegates detached bytes to the unchanged M120 decoder. The caller
supplies two explicit files. There is no implicit pairing, discovery, suffix
routing, manifest lookup, or source cache. Existing `compile_prefab()` remains
the single authority that checks exact `prefab_id` agreement.

The internal `$schema` field, not the filename, remains the format and version
identity. JSON Schema's separation between schema identity and instance data is
consistent with retaining explicit protocol identifiers in each detached
record rather than inferring type from a path.

## Security, ownership, and failure behavior

Both methods inherit M121 rejection of absolute, drive-relative,
parent-traversal, alternate-stream, reserved-device, overlong, and resolved
root-escape paths. Only existing regular files are accepted. Metadata size and
one-handle read caps use `limits.scene.max_bytes`. Structured path/read failures
include only role and bound context; malformed or incompatible data retains the
existing structured `PrefabError` chain.

Each synchronous call owns one descriptor until the bounded read returns and
retains no open handle afterward. The result is detached immutable data. There
is no cache, watcher, provider, renderer, world, thread, or closeable background
resource. As with M121, project confinement is a cooperative local-project
boundary, not a descriptor-confined race-free sandbox against a hostile actor
concurrently replacing filesystem objects.

## Determinism and mutation

The same accepted bytes and exact limits normalize to the same prefab or
instance record. Filesystem timing, external changes, and selection order are
outside simulation determinism. Applications select and load both source files
before deterministic execution.

Loading performs no world mutation and produces no receipt. The caller must
explicitly invoke `compile_prefab()` and apply its ordinary transaction. That
application is the sole world mutation and receipt boundary. Changing or
deleting either source file cannot alter an already returned record or an
existing runtime entity.

## Boundary

M122 adds no directory discovery, implicit pairing, extension routing, manifest
registration, dependency traversal, asset loading, cache, watcher, live update,
reimport, silent propagation, source write-back, nested prefab inheritance,
variant chain, remote/file URI access, arbitrary Python import or evaluation,
new persistent operation, dependency, lock, metadata, version, root export,
workflow, hosted allocation, release authority, tag, release, publication, or
public remote change.

The scene and prefab contracts remain path-agnostic and unchanged. A standalone
installed-wheel verifier covers two explicit files, detached decoding, exact
source matching, compilation, transaction application, and receipt aliases.

## Consequences

- Python composition can load both M120 record types without duplicating path,
  size, handle, or diagnostic policy.
- Format identity remains explicit and independent of filename conventions.
- Source and instance selection stays caller-visible; mismatches fail during
  explicit compilation.
- Discovery, caching, dependency traversal, nested composition, and live update
  remain separate future decisions.

## Alternatives considered

- Add a polymorphic resource loader. Rejected because handler discovery,
  extensions, cache keys, dependency traversal, and lifetime policy are not
  required for two bounded formats.
- Infer an instance path from a prefab path. Rejected because hidden naming
  policy creates implicit pairing and ambiguous failure behavior.
- Scan the project for matching `prefab_id` values. Rejected because directory
  ordering, duplicates, resource bounds, stale results, and conflict precedence
  require a separate design.
- Watch and propagate source changes. Rejected because update identity,
  conflict resolution, rollback, receipts, ownership, and failure atomicity are
  not defined.

## References

- [Godot ResourceLoader](https://docs.godotengine.org/en/stable/classes/class_resourceloader.html)
- [Unity prefab introduction](https://docs.unity3d.com/ja/current/Manual/prefabs-introduction.html)
- [RFC 8089: The file URI Scheme](https://datatracker.ietf.org/doc/html/rfc8089)
- [JSON Schema Core 2020-12](https://json-schema.org/draft/2020-12/json-schema-core)
- [RFC-0103: one-level prefab fragment planning](0103-add-one-level-prefab-fragment-planning.md)
- [RFC-0104: project-confined scene file loading](0104-add-project-confined-scene-file-loading.md)
- [ADR-0012: data-only CLI composition and path confinement](../adr/0012-data-only-cli-composition-and-path-confinement.md)
