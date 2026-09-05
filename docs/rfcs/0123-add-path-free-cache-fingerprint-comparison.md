# RFC-0123: Add path-free cache-fingerprint comparison

- **Status:** Accepted
- **Date:** 2026-08-27
- **Decision owners:** LudoWeave maintainers

## Context

M139 can prove exact equality between one canonical saved fingerprint and one
fresh bounded cache observation. Its fail-closed mismatch intentionally emits no
success document, so an operator cannot distinguish aggregate growth, shrinkage,
or identity-only substitution without separately handling sensitive cache
structure.

The [NIST Privacy Framework](https://www.nist.gov/privacy-framework/privacy-framework)
frames privacy risk management around controlling data processing and the
observability and linkability of people and systems. OpenTelemetry's
[sensitive-data guidance](https://opentelemetry.io/docs/security/handling-sensitive-data/)
recommends data minimization and aggregation where detailed telemetry is not
needed. JSON Patch ([RFC 6902](https://www.rfc-editor.org/rfc/rfc6902)) requires
operation paths and can carry values; a generic patch would therefore widen the
existing path-free disclosure boundary.

M137 already defines twelve bounded, path-independent inventory metrics. M138
separately binds exact action/CAS identity without publishing those identities.
Those existing surfaces are sufficient for a fixed diagnostic report.

## Decision

Add `compare_asset_cache_fingerprint(plan, fingerprint, cache_root, *,
project_root=None, limits=...)`. The operation:

1. requires exact plan and fingerprint value types;
2. binds the saved nested plan digest to the exact supplied plan before cache
   construction;
3. invokes the unchanged bounded M138 observation exactly once; and
4. subtracts each saved M137 aggregate from its current counterpart.

The frozen `ludoweave.asset-cache-fingerprint-comparison/1` report contains:

- status `equal` or `different`;
- the existing fingerprint protocol and plan digest;
- one `observation_equal` boolean; and
- signed integer deltas for exactly the twelve existing M137 aggregate fields.

Status is `equal` only when the observation digest matches and every aggregate
delta is zero. This retains identity-only change detection: replacing one valid
same-size unreferenced blob with another produces `different`, a false
`observation_equal`, and twelve zero deltas.

## CLI composition

Add:

```console
ludoweave source asset-cache-fingerprint-compare PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE --fingerprint FILE --cache DIRECTORY
```

The command verifies current source identities, the saved lock, and the exact
regenerated plan before reading the project-confined canonical saved record.
The saved plan is preflighted before one read-only external-cache observation.

An equal report is written to standard output with exit status 0. A diagnostic
different report is also written to standard output but uses exit status 1, so
shell automation can distinguish difference from equality. Malformed,
noncanonical, stale-plan, corrupt-cache, or over-limit input remains a structured
error on standard error with exit status 2.

## Disclosure boundary

The report does not contain a cache key, asset URI, artifact digest, action
identity, filename, path, payload, expected observation digest, or current
observation digest. It is a fixed aggregate report, not a generic object diff or
JSON Patch. Signed deltas say how the already-public M137 metrics changed; the
boolean says whether exact observed membership also remained identical.

Aggregate output can still reveal coarse cache activity. Callers should retain
or transmit it only where those counts and byte totals are appropriate. M140
does not add a policy engine, redaction configuration, telemetry exporter, or
remote transport.

## Integrity equality is not authenticity

An equal report means one fresh sequential observation equals the supplied saved
record under the exact plan. A different report means at least one aggregate or
the exact observation digest changed. Neither outcome proves who produced the
record, when either state existed, whether the record and cache were substituted
together, or whether either should be trusted.

There is no signature, key identity, root of trust, authenticated builder,
trusted timestamp, attestation, transparency log, or authenticated channel.
This remains local comparison evidence, not authenticity or provenance.

## Failure, determinism, and concurrency

Invalid values and plan mismatch fail before cache access. Cache corruption,
layout drift, concurrent scan change, and active-limit exhaustion fail without a
comparison report. The operation never repairs or normalizes storage. An absent
cache compares deterministically and remains absent.

Stable saved bytes, plan bytes, and verified storage produce stable canonical
comparison bytes independent of project/cache paths and enumeration order. The
underlying M138 scan remains sequential rather than atomic; no report claims all
entries coexisted at one instant.

## Compatibility

M137 inventory, M138 fingerprint, and M139 saved-record/verification protocols
remain unchanged. M132-M139 cache behavior and layout stay protected. The new
value objects, function, export, protocol, and CLI subcommand are experimental
and additive. Dependencies, package version, workflows, permissions, release
authority, and engine-root API remain unchanged. There is no CI change.

## Non-scope

M140 has no per-object diff, path or identity disclosure, JSON Patch, write,
publication, repair, deletion, eviction, garbage collection, quota/age policy,
retention root, lease, pin, generation, atomic snapshot, signature, key
management, attestation, trusted timestamp, provenance, authentication, remote
cache, network, telemetry export, discovery, watcher, decoder registration,
worker, process, thread, parallelism, plugin, renderer upload, project
write-back, world/session, command, transaction, mutation, or receipt. It adds
no dependency, native/backend surface, engine-root API, version, workflow
allocation, permission, credential, release authority, or remote change.

## Consequences

- Operators gain a stable coarse diagnosis without disclosing cache object
  identities or granting mutation authority.
- Identity-only substitution remains detectable even when all aggregate values
  are unchanged.
- Every comparison retains the complete bounded whole-cache verification cost.
- Exit status 1 is a normal diagnostic difference, while exit status 2 remains
  invalid or failed processing.
- Authenticity, retention, cleanup, and detailed diffing remain explicit future
  decisions.

## Revisit triggers

- A request for detailed object diagnosis requires an explicit disclosure and
  redaction threat model rather than extending this report opportunistically.
- Authentic saved evidence requires a key/root-of-trust lifecycle, signed
  subject binding, trusted distribution, and revocation behavior.
- Cleanup requires atomic/generation evidence, leases or retention roots,
  concurrency semantics, failure recovery, and separate mutation authority.
