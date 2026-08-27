# RFC-0127: Add an offline unreferenced-blob preview

- **Status:** Accepted
- **Date:** 2026-08-27
- **Decision owners:** LudoWeave maintainers

## Context

M143 produces a minimized path-free preview from one freshly observed M138
fingerprint. M139 already defines strict, bounded admission for saved canonical
M138 fingerprints, and M141 proves that admitted fingerprints can support pure
offline diagnostics after their originating caches are absent. There is no
composition that applies M143 directly to one saved fingerprint.

[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html) requires duplicate-free,
deterministically serialized JSON for invariant hashing. Python's
[JSON decoder](https://docs.python.org/3.12/library/json.html) exposes hooks for
detecting duplicate object names and rejecting non-finite constants. M139
already implements those requirements, exact schema validation, hard aggregate
bounds, canonical-byte equality, and structured failure. Duplicating that
decoder would create a second admission policy with no additional safety.

Offline deterministic derivation is local integrity evidence only. SLSA's
[artifact-verification guidance](https://slsa.dev/spec/v1.2/verifying-artifacts)
requires trusted provenance and explicit verification policy for authenticity;
an unsigned local fingerprint provides neither. M144 therefore reuses the
existing admitted value without adding trust claims.

## Decision

Add one CLI composition:

```console
ludoweave source asset-cache-fingerprint-record-preview PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE --fingerprint FILE
```

The command:

1. loads the headless project and preflights current source identities;
2. verifies the saved source lock and exact regenerated asset-build plan;
3. reads exactly one project-confined fingerprint record under M139's existing
   65,536-byte hard maximum;
4. reuses `decode_asset_cache_fingerprint()` for strict canonical admission;
5. passes the exact plan and admitted fingerprint to
   `preview_asset_cache_unreferenced_blobs()`; and
6. emits the unchanged canonical M143 preview bytes with exit 0.

There is no cache argument or cache access. The originating cache may be
absent. M144 introduces no new runtime value, protocol, decoder, or root API.

## Admission, determinism, and failure

Current inputs are verified before the fingerprint path is resolved or read.
The existing project-relative reader rejects absolute paths, traversal,
links/reparse points, non-files, and over-limit input. The existing M139 decoder
rejects invalid UTF-8/JSON, duplicate names, non-finite values, unknown or
missing fields, invalid primitives/protocols/aggregates, noncanonical bytes,
and oversized records.

The pure M143 function recomputes exact plan identity and rejects a fingerprint
whose nested inventory binds another plan. Identical admitted plan and
fingerprint values therefore produce identical M143 bytes on every supported
platform. Invalid processing remains structured standard error with exit 2 and
no partial output.

## Safety and trust boundary

The command performs no fresh observation and cannot show whether a cache has
changed since the record was produced. The unsigned record establishes no
chronology, freshness, authenticity, provenance, writer identity, or trusted
timestamp. Its unreferenced count remains evidence that one saved sequential
observation found no admitted action reference; it is not deletion eligibility.

The output retains M143's fixed aggregate-only disclosure. It exposes no
candidate digest, cache/action key, URI, artifact identity, filename, path,
payload, timestamp, age, or policy beyond the already-public exact plan and
complete-observation SHA-256 values.

## Compatibility and CI

M137-M143 protocols, record limits, canonical bytes, cache layout, package
version, dependencies, workflows, permissions, release authority, and
engine-root APIs remain unchanged. M144 only adds a CLI composition, tests,
installed-wheel proof, architecture enforcement, and documentation.

The existing quota-conscious trusted-base CI already covers substantive Python
and installed-wheel changes. There is no CI change.

## Non-scope

M144 adds no saved-preview format or decoder, preview verification protocol,
fresh cache observation, cache argument, candidate list, detailed diff,
filename/path/payload disclosure, timestamp, age/grace or quota policy,
retention root, lease, pin, generation, quiescence, lock, atomic snapshot,
cleanup, garbage collection, prune, repair, deletion, eviction, mutation,
remote cache, authentication, signature, attestation, provenance, network,
telemetry, watcher, scheduler, worker, process, thread, parallelism, plugin,
renderer upload, project/world mutation, command receipt, dependency,
native/backend surface, version, workflow allocation, permission, credential,
release, publication, or remote change.

## Consequences

- Operators can derive the existing small M143 preview after the originating
  cache has been removed or is intentionally unavailable.
- One strict fingerprint admission policy remains authoritative.
- The command cannot be mistaken for a current observation because its name and
  documentation explicitly identify a saved record and offline behavior.
- Future authenticity or cleanup work still requires separate explicit design
  and authority.

## Revisit triggers

- Saved-preview persistence or verification requires a separately bounded
  record contract and a demonstrated consumer need.
- Authenticity requires trusted signing/provenance policy independent of this
  local unsigned record.
- Any cache mutation still requires retained roots, grace/age policy,
  quiescence or locking, revalidation, and crash-recovery semantics.
