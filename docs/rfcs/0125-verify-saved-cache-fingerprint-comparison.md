# RFC-0125: Verify saved cache-fingerprint comparison evidence

- **Status:** Accepted
- **Date:** 2026-08-27
- **Decision owners:** LudoWeave maintainers

## Context

M140 defines one canonical path-free comparison report. M141 can derive that
report from two admitted saved fingerprints without a cache. The engine cannot
yet safely admit a saved comparison document or prove that it matches a
particular plan and pair of fingerprints.

[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html) explains that repeatable
hashing depends on invariant representation. Python 3.12's
[JSON guidance](https://docs.python.org/3.12/library/json.html) recommends input
size limits for untrusted documents and exposes hooks needed to reject duplicate
names and non-finite constants. Those constraints support a bounded exact-schema
decoder that accepts only the engine's existing canonical bytes.

[NIST FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) describes
message digests as change-detection evidence. That supports binding the exact
admitted comparison bytes in verification output. It does not establish who
created the record. Current
[SLSA verification guidance](https://slsa.dev/spec/v1.2/verifying-artifacts)
requires a signature, subject match, root of trust, builder identity, and
expected provenance fields before an authenticity claim.

OpenTelemetry's
[sensitive-data guidance](https://opentelemetry.io/docs/security/handling-sensitive-data/)
recommends collecting only what serves the diagnostic purpose and considering
aggregated data instead of detailed attributes. M142 therefore retains M140's
fixed aggregate disclosure and adds no object identities.

## Decision

Add strict decoding for one saved
`ludoweave.asset-cache-fingerprint-comparison/1` document and add a pure
verification operation:

```python
verify_asset_cache_fingerprint_comparison(plan, expected, current, comparison)
```

The operation:

1. requires exact plan, fingerprint, and comparison value types;
2. invokes M141's pure comparison so both fingerprints are bound to the exact
   supplied plan;
3. requires every field of the supplied comparison to equal the recomputed
   frozen value; and
4. emits deterministic path-free
   `ludoweave.asset-cache-fingerprint-comparison-verification/1` evidence.

Verification output contains valid status, the fingerprint and comparison
protocols, plan digest, comparison status, and SHA-256 of the exact canonical
comparison report. It contains neither fingerprint observation digest nor any
cache/object identity. A `different` comparison can verify successfully: valid
means that the report was derived correctly, not that the two observations are
equal.

## Saved-record admission

`decode_asset_cache_fingerprint_comparison()` accepts only `str` or `bytes`
under a tightening-only 4,096-byte hard limit. It rejects invalid UTF-8/JSON,
duplicate names, non-finite numbers, overlong integer tokens, missing or extra
fields, wrong protocols, wrong primitive types, inconsistent status, booleans
or floats in integer fields, out-of-range signed deltas, and noncanonical bytes.

The top-level fields are exactly `$schema`, `status`, `fingerprint_protocol`,
`plan_sha256`, `observation_equal`, and `deltas`. The nested delta object has
exactly the twelve M137 aggregate fields. Reconstruction uses the unchanged
frozen M140 value and requires the original bytes to equal its canonical bytes.

## CLI composition

Add:

```console
ludoweave source asset-cache-fingerprint-comparison-verify PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE --expected-fingerprint FILE --current-fingerprint FILE --comparison FILE
```

The command verifies current source identities, the saved lock, and the exact
regenerated plan before any of its three project-confined record reads. Each
fingerprint retains M139's independent 65,536-byte bound and strict decoder.
The comparison receives its independent 4,096-byte bound and M142 decoder.

Successful recomputation writes canonical M142 verification evidence to
standard output and exits 0, including when `comparison_status` is `different`.
Malformed, noncanonical, plan-mismatched, or semantically altered input remains
a structured error on standard error with exit 2. The command has no cache
argument and performs no cache access.

## Disclosure and trust boundary

The comparison digest binds only the already-admitted aggregate report. It is
not a digest of either cache observation and reveals no expected/current
observation digest, cache key, URI, artifact/action/blob identity, filename,
record path, or payload. Plan and comparison digests plus aggregate status can
still be sensitive in a caller's context; callers own retention and transport.

Successful local recomputation detects accidental or unauthorised record
change only under the caller's assumption that the supplied plan and both
fingerprints are the intended inputs. It is not authenticity or provenance.
There is no signature, key identity, root of trust, authenticated builder or
channel, trusted timestamp, attestation, transparency log, revocation policy,
or independent subject registry.

## Failure, ownership, and determinism

Exact-value checks and M141 plan binding complete before a verification report
is created. Any mismatch fails without partial success. The pure operation has
no filesystem, cache, source, environment, clock, process, thread, or network
access and cannot mutate any input.

The CLI owns only three bounded project-confined reads after current-input
preflight. It performs no write. Stable admitted values produce stable
verification bytes across supported platforms. This does not upgrade either
original sequential fingerprint into an atomic snapshot.

## Compatibility and CI

M137 inventory, M138 fingerprint, M139 decoding/verification, M140 comparison,
and M141 offline comparison protocols and canonical bytes remain unchanged.
The new decoder, verification value, pure function, focused export, CLI
composition, tests, installed-wheel smoke, and documentation are experimental
and additive.

Cache layout, engine root, dependencies, package version, workflows,
permissions, release authority, and prior evidence remain unchanged. The
existing trusted-base CI qualification already covers substantive Python and
installed-wheel changes with three runner allocations. There is no CI change.

## Non-scope

M142 adds no cache construction/read/write, fresh observation, source payload
acquisition, detailed diff/list, JSON Patch, object/path/payload disclosure,
record store, naming, retention, write-back, publication, repair, deletion,
eviction, garbage collection, quota/age policy, lease, pin, generation, atomic
snapshot, signature, key management, attestation, trusted timestamp,
provenance, authentication, remote cache, network, telemetry export, discovery,
watcher, worker, process, thread, parallelism, plugin, renderer upload,
world/session, command, transaction, mutation, or receipt. It adds no
dependency, native/backend surface, engine-root API, version, workflow
allocation, permission, credential, release authority, or remote change.

## Consequences

- A saved M140 report can be admitted and checked after both originating caches
  are absent.
- Successful verification binds the exact current plan, two fingerprint
  values, and comparison bytes without detailed identity disclosure.
- A correctly derived `different` report verifies with exit 0; equality remains
  data inside the verified report, not verifier process status.
- Verification cost is constant in cache size after the three records exist.
- Results inherit the substitution, provenance, and sequential-observation
  limitations of all unsigned inputs.
- CI and hosted runner allocation remain unchanged.

## Revisit triggers

- Authenticated comparison evidence requires a separately approved trust root,
  signature/attestation format, subject binding, distribution, and revocation
  design.
- Detailed diagnosis requires a separate disclosure and privacy review.
- Record persistence requires explicit naming, confinement, overwrite,
  retention, cleanup, and migration semantics.
- Cache cleanup still requires generations or leases, quiescence, grace/age
  policy, crash recovery, and cross-platform filesystem evidence.
