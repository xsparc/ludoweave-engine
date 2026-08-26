# RFC-0122: Add saved cache-fingerprint verification

- **Status:** Accepted
- **Date:** 2026-08-27
- **Decision owners:** LudoWeave maintainers

## Context

M138 produces a deterministic digest for one bounded, verified sequential cache
observation, but deliberately provides no saved-record decoder or comparison
operation. Operators need to compare canonical saved evidence with one fresh
observation without widening the cache's read-only authority or treating a
matching digest as provenance.

Python's [JSON documentation](https://docs.python.org/3.12/library/json.html)
warns that untrusted JSON should be size-limited and documents that the default
decoder accepts repeated object names and non-finite numbers. The decoder must
therefore enforce its own byte bound, unique names, finite values, exact fields,
exact types, and canonical encoding.

[NIST FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) describes
secure-hash digests as a way to detect whether messages changed after digest
generation. It does not turn an unsigned digest into an authenticated claim.
Current [SLSA artifact-verification guidance](https://slsa.dev/spec/v1.2/verifying-artifacts)
requires a configured root of trust, signature verification, subject/digest
binding, and expectation checks for provenance authenticity. M139 introduces
none of those facilities.

## Decision

Add `decode_asset_cache_fingerprint(document, *, limits=...)` for one exact
canonical `ludoweave.asset-cache-fingerprint/1` record. The decoder:

- admits at most 65,536 bytes, with a tightening-only limit;
- rejects invalid UTF-8, duplicate names, non-finite numbers, recursion failure,
  unknown or missing fields, non-exact types, unsupported protocols, invalid
  hashes, and inconsistent inventory aggregates; and
- reconstructs the existing frozen M138 value and requires its canonical bytes
  to equal the admitted record bytes.

Add `verify_asset_cache_fingerprint(plan, fingerprint, cache_root, *,
project_root=None, limits=...)`. It first requires exact value types and binds
the saved nested inventory to the exact current plan digest. Only after that
preflight can it invoke `fingerprint_asset_cache_observation()` once. The fresh
M138 pass retains every M137 bound and integrity check. Exact nested inventory
and observation digest equality returns frozen path-free
`ludoweave.asset-cache-fingerprint-verification/1` evidence.

## CLI composition

Add:

```console
ludoweave source asset-cache-fingerprint-verify PROJECT --manifest FILE --assets FILE --lock FILE --plan FILE --fingerprint FILE --cache DIRECTORY
```

The command verifies current source identities, the saved lock, and the exact
regenerated plan before reading the project-confined fingerprint under its hard
byte limit. Record/plan preflight completes before the external cache is
constructed or read. The command acquires no source payload for decoding and
opens no writable cache.

Saved input is the canonical JSON record itself, without pretty-printing or
terminal line framing. Success emits status, fingerprint protocol, plan digest,
and observation digest only. Errors expose stable field/code context without
paths, cache identities, stored hashes, or payloads.

## Integrity equality is not authenticity

Success means the exact saved M138 value equals one newly computed sequential
observation under the supplied exact plan. It can detect observed cache change
relative to that saved value. It does not prove who produced the saved record,
when it was produced, whether it was substituted with the cache, or whether the
observer should trust it.

The record is unsigned and has no key identity, root of trust, authenticated
builder, timestamp, transparency log, attestation envelope, or trusted channel.
Therefore local digest agreement is integrity equality, not authenticity,
provenance, ownership, retention, or deletion authority.

## Failure, determinism, and concurrency

Malformed, noncanonical, incompatible, oversized, plan-mismatched,
inventory-mismatched, digest-mismatched, corrupt, or over-limit input fails
closed with no success report or mutation. An absent cache verifies only
against the exact absent-cache fingerprint and remains absent.

Stable saved bytes, plan bytes, and verified cache storage produce stable
verification bytes independent of paths and enumeration order. M138 remains a
sequential observation rather than an atomic snapshot. Concurrent hostile
replacement is outside the supported local single-caller model and no matching
report claims simultaneous coexistence of all entries.

## Compatibility

M138 fingerprint and M137 inventory protocols and canonical bytes remain
unchanged. M132-M138 storage and observation behavior stays protected. The
decoder, verifier, export, report protocol, and CLI subcommand are experimental
and additive. The cache layout, engine root, dependencies, package version,
workflows, permissions, and release authority remain unchanged. There is no CI
change.

## Non-scope

M139 has no write, publication, repair, deletion, eviction, garbage collection,
quota/age policy, retention root, lease, pin, generation, atomic snapshot,
structured diff, path/identity disclosure, signature, key management,
attestation, transparency log, trusted timestamp, provenance, authentication,
remote cache, network, discovery, watcher, decoder registration, worker,
process, thread, parallelism, plugin, renderer upload, project write-back,
world/session, command, transaction, mutation, or receipt. It adds no
dependency, native/backend surface, engine-root API, version, workflow
allocation, permission, credential, release authority, or remote change.

## Consequences

- Operators can verify a canonical saved fingerprint against current local
  cache state without exposing cache identities or granting mutation authority.
- Strict decoding rejects alternate encodings and ambiguous JSON before cache
  observation.
- Every comparison retains the full bounded whole-cache verification cost.
- Authenticity and cleanup remain explicit future decisions rather than implied
  by digest equality.
- CI remains unchanged; local tests and installed-wheel evidence exercise the
  boundary.

## Revisit triggers

- Authentic saved evidence requires an explicit threat model, key/root-of-trust
  lifecycle, signature/attestation format, trusted distribution channel, and
  revocation behavior.
- Useful change diagnosis requires a privacy-reviewed bounded diff contract; a
  mismatch alone deliberately identifies no cache object.
- Retention planning still requires complete explicit roots, generations, or
  leases from every relevant owner.
- Deletion still requires quiescence, grace/age policy, crash recovery,
  rollback evidence, and cross-platform filesystem semantics.

## Rejected alternatives

- Accept arbitrary equivalent JSON. Rejected because one exact canonical saved
  representation is simpler to bound, compare, test, and preserve.
- Compare only `observation_sha256`. Rejected because the saved plan-relative
  inventory is part of the M138 evidence and must match exactly as well.
- Call the result authenticated or trusted. Rejected because no root of trust or
  signature exists.
- Repair or clean the cache after mismatch. Rejected because verification grants
  no mutation or retention authority.
