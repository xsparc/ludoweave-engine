# RFC-0119: Add saved cache-population verification

- **Status:** Accepted
- **Date:** 2026-08-27
- **Decision owners:** LudoWeave maintainers

## Context

M135 emits canonical path-free evidence after explicit complete realization and
per-entry cache publication. Callers can save stdout, but the engine has no
bounded reader or operation that compares that saved document with an exact
current plan and current cache. The next narrow step is read-only verification,
not another publication effect.

Current [Bazel remote-cache documentation](https://bazel.build/remote/caching)
separates action-result metadata from content-addressed output bytes and
describes download verification. Current [Python JSON documentation](https://docs.python.org/3.12/library/json.html#standard-compliance-and-interoperability)
notes that repeated object names are accepted by default and explains using
`object_pairs_hook` to select stricter behavior. Current [SLSA 1.2 artifact-
verification guidance](https://slsa.dev/spec/v1.2/verifying-artifacts) requires
an artifact/provenance subject match, configured expectations, and a root of
trust for authenticity claims. These sources support strict local integrity
checking while requiring M136 to say clearly that an unsigned M135 report is
not provenance, authenticity, or builder identity.

## Decision

Add a detached `AssetCachePopulationRecord` representation of
`ludoweave.asset-cache-population/1` plus:

- `AssetCachePopulationRecordEntry`, containing one existing validated result
  identity and exact historical `hit`/`decoded` and `published`/`reused`
  statuses;
- `AssetCachePopulationRecordLimits`, which can tighten but not exceed an
  8 MiB document and 4,096 entries;
- `AssetCachePopulationRecord.from_json()`, which accepts UTF-8 text or bytes,
  rejects duplicate fields, non-finite constants, unknown/missing fields,
  wrong exact types, invalid protocols/statuses/identities, duplicate URIs,
  inconsistent aggregate bytes, inconsistent status counts, and active-limit
  excess;
- canonical normalization back to the exact M135 report shape.

Add `verify_asset_cache_population(plan, population, cache_root, *,
project_root=None)`. It first validates the complete saved record against the
exact current plan hash, entry count/order, URI, kind, cache key, and source
byte count. Only after that complete preflight does it open the explicit cache
with `writable=False`. Every plan action must be present and must pass the
unchanged M133 canonical metadata, plan-field, ordinary-file, byte-count, and
CAS SHA-256 checks. Its complete result identity must then equal the saved
record identity.

Success returns frozen path-free
`ludoweave.asset-cache-population-verification/1` evidence with `valid` status,
the population protocol, plan hash, and entry count. It retains no payload.

## CLI composition

Add:

```console
ludoweave source asset-cache-population-verify PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE --population FILE --cache DIRECTORY
```

The command loads the saved plan and lock, recomputes current source identities,
requires the current lock and regenerated plan to match, then reads the
project-confined bounded population document. Only after strict decoding does
the verifier open the caller-selected external cache read-only. Success writes
one canonical verification report to stdout. Any failure writes no success
document and omits paths and compared hash values.

The command does not reacquire sources for decoding and invokes no decoder.
Current source bytes were already streamed for current-lock verification, and
the exact plan binds their hashes and sizes.

## Ownership, failure, and determinism

Project composition owns the bounded saved-report descriptor and closes it
before verification. The verifier constructs a read-only cache store for one
explicit root; the store owns no persistent descriptor, thread, worker, or
background lifecycle. Cache payloads are read and verified one at a time and
are not retained in the result.

Malformed or mismatched population data fails before the cache is opened.
Missing actions are explicit failures rather than misses eligible for decoding.
Present corruption propagates the existing structured M133 error. The operation
does not repair, delete, publish, recreate, or otherwise mutate an entry. A
missing cache remains absent.

Stable saved bytes, current source/manifest/lock/plan state, and cache contents
produce the same canonical success document. Sequential source and cache reads
are not an atomic filesystem snapshot; hostile concurrent replacement remains
outside the supported local single-caller model.

## Integrity is not provenance

M136 proves that a strictly decoded saved report agrees with the exact current
plan and the locally observed verified action/CAS mapping. Historical status
fields are validated as data but cannot prove that the reported decode or
publication events occurred. A malicious party able to replace both the report
and self-consistent cache can satisfy local digest checks.

The report has no signature, authenticated builder identity, root of trust,
trusted timestamp, or SLSA attestation envelope. M136 is therefore not
provenance, authenticity, non-repudiation, or supply-chain policy verification.

## Compatibility

M131 execution, M132 publication, M133 lookup, M134 realization, and M135
population remain unchanged and independently protected. The focused-package
exports and CLI subcommand are experimental and additive. The engine root,
loader/cache-key/population protocols, dependencies, version, workflows,
permissions, and release authority remain unchanged. There is no CI change.

## Non-scope

M136 has no cache publication, creation, write, repair, deletion, eviction,
garbage collection, quota, migration, remote cache, networking,
authentication, signature, attestation, root of trust, builder identity,
provenance, discovery, enumeration, watcher, reimport, decoder, worker,
scheduler, process, thread, parallelism, plugin, renderer upload, project
write-back, world/session, command, transaction, mutation, or receipt. It adds
no dependency, native code, backend object, engine-root API, version, workflow
job/allocation, permission, credential, release authority, or remote change.

## Consequences

- Saved M135 stdout can now be decoded under explicit hard bounds and compared
  with exact current plan/cache state.
- Complete plan/report mismatch fails before the first cache action read.
- A missing or corrupt current action fails without decoder fallback or repair.
- Historical status evidence remains useful for diagnostics but deliberately
  carries no provenance claim.
- CI remains unchanged; focused and installed-wheel evidence exercises the new
  boundary in existing local validation.

## Revisit triggers

- Authenticity requires a signed attestation format, configured roots of trust,
  identity policy, secure key lifecycle, and verification expectations.
- Cross-machine cache verification requires authenticated transport and
  separate read/write credentials plus poisoning and retry policy.
- Snapshot-consistent concurrent verification requires supported-filesystem
  evidence and an immutable generation or descriptor-pinning design.
- Repair, eviction, or garbage collection requires separate mutation authority
  and protection for entries used by other callers.

## Rejected alternatives

- Treat the M135 report as provenance. Rejected because it is unsigned local
  integrity evidence with no trusted builder identity or root of trust.
- Decode misses while verifying. Rejected because verification must describe
  current cache agreement and remain read-only.
- Accept unknown fields or duplicate names. Rejected because ambiguous saved
  evidence weakens exact schema and failure behavior.
- Open the cache before complete plan/report preflight. Rejected because a
  detached mismatch needs no cache authority or observation.
