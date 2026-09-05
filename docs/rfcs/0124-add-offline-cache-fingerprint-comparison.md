# RFC-0124: Add offline cache-fingerprint comparison

- **Status:** Accepted
- **Date:** 2026-08-27
- **Decision owners:** LudoWeave maintainers

## Context

M140 diagnoses one canonical saved fingerprint against one fresh bounded cache
observation. Operators who already possess two admitted canonical fingerprints
cannot compare them without retaining or reconstructing the cache, even though
M140's fixed aggregate-only report needs only the two fingerprint values.

[NIST FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)
describes message digests as change-detection mechanisms. OpenTelemetry's
[sensitive-data guidance](https://opentelemetry.io/docs/security/handling-sensitive-data/)
recommends collecting only what serves the observability purpose and considering
aggregated data instead of detailed attributes. Those principles support
reusing M140's fixed path-free report rather than exposing stored identities.

Offline comparison does not authenticate either saved record. Current
[SLSA verification guidance](https://slsa.dev/spec/v1.2/verifying-artifacts)
requires roots of trust, signature/subject checks, and expected provenance
fields. GitHub likewise documents artifact attestations for released artifacts
and advises against signing frequent test builds. M141 adds no such trust or
hosted workflow.

## Decision

Add `compare_asset_cache_fingerprint_records(plan, expected, current)`. It:

1. requires exact plan and fingerprint value types;
2. binds both nested fingerprint plan digests to the exact supplied plan;
3. compares the two already-admitted observations entirely in memory; and
4. returns the unchanged frozen M140
   `ludoweave.asset-cache-fingerprint-comparison/1` value.

Every delta remains `current - expected` for exactly the twelve M137 aggregate
fields. `observation_equal` compares the two stored M138 observation digests.
Status is equal only when that flag is true and all aggregate deltas are zero.
Identity-only substitution therefore remains detectable with twelve zero
deltas.

The operation takes no cache root and performs no filesystem, cache, source,
clock, environment, or network access. The caller owns admission of the two
canonical values; the existing strict M139 decoder remains the sole record
decoder.

## CLI composition

Add:

```console
ludoweave source asset-cache-fingerprint-record-compare PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE --expected-fingerprint FILE --current-fingerprint FILE
```

The command verifies current source identities, the saved lock, and the exact
regenerated plan before either fingerprint read. Both project-confined records
are independently limited to 65,536 bytes and decoded through the unchanged
canonical M139 decoder. The pure comparison then binds both saved records to
the current exact plan.

Equal writes the canonical M140 report to standard output and exits 0.
Different writes the same report shape to standard output and exits 1.
Malformed, noncanonical, plan-mismatched, missing, or oversized input remains a
structured error on standard error with exit 2.

The command has no cache argument and performs no cache access. Once the two
records exist, their originating cache may be absent without affecting the
comparison.

## Disclosure boundary

The reused report contains status, fingerprint protocol, plan digest, one
observation-equality boolean, and twelve signed aggregate deltas. It contains no
cache key, URI, artifact/action/blob identity, filename, record path, payload,
expected observation digest, or current observation digest.

The command labels its two input roles only in argument names. It does not emit
their filenames or infer chronology, trust, origin, ownership, or retention.
Aggregate counts and byte totals can still reveal coarse activity, so callers
remain responsible for where reports are retained or transmitted.

## Integrity comparison is not authenticity

An equal result says that the two supplied admitted values contain equal exact
observation identity and aggregate inventory under one exact plan. A different
result says that at least one of those properties changed. Neither result proves
who created a record, when it was created, whether the pair was substituted
together, whether either cache ever existed as an atomic snapshot, or whether
either value should be trusted.

There is no signature, key identity, root of trust, authenticated builder,
trusted timestamp, attestation, transparency log, or authenticated channel.
Offline digest comparison is local integrity evidence, not authenticity or
provenance.

## Failure and determinism

Exact-value and both-plan preflight completes before comparison. Any mismatch
fails without a report. The pure function cannot create, read, repair, or change
a cache or project. The CLI's only reads are the already-required current input
preflight and two bounded project-confined records.

Stable plan and admitted fingerprint values produce stable canonical report
bytes independent of paths, cache availability, platform, enumeration order,
or wall-clock time. Determinism of the comparison does not upgrade the original
M138 sequential observations into atomic snapshots.

## Compatibility

M137 inventory, M138 fingerprint, M139 decoding/verification, and M140
comparison protocols and canonical bytes remain unchanged. The new pure
function, export, CLI composition, tests, and documentation are experimental
and additive. Cache layout, engine root, dependencies, package version,
workflows, permissions, release authority, and prior evidence remain unchanged.
There is no CI change.

## Non-scope

M141 has no cache construction/read/write, fresh observation, source payload
acquisition, decoder registration, per-object diff/list, JSON Patch, path or
identity disclosure, record storage, write-back, publication, repair, deletion,
eviction, garbage collection, quota/age policy, retention root, lease, pin,
generation, atomic snapshot, signature, key management, attestation, trusted
timestamp, provenance, authentication, remote cache, network, telemetry export,
discovery, watcher, worker, process, thread, parallelism, plugin, renderer
upload, world/session, command, transaction, mutation, or receipt. It adds no
dependency, native/backend surface, engine-root API, version, workflow
allocation, permission, credential, release authority, or remote change.

## Consequences

- Two canonical saved observations can be compared after their cache is gone.
- The report retains M140's fixed path-free disclosure and exit semantics.
- Comparison cost is constant in cache size after records have been admitted.
- Results inherit any substitution, provenance, and sequential-observation
  limitations of the unsigned inputs.
- CI remains unchanged; local and installed-wheel evidence exercise the new
  composition.

## Revisit triggers

- Authenticated evidence requires a separately approved root-of-trust,
  signature/attestation, subject binding, trusted distribution, and revocation
  design.
- Detailed object diagnosis requires a separate privacy and disclosure review.
- Record retention or naming requires explicit storage ownership, confinement,
  overwrite, cleanup, and migration semantics.
- Cache cleanup still requires generations or leases, quiescence, grace/age
  policy, crash recovery, and cross-platform filesystem evidence.
