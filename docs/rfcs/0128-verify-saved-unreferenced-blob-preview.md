# RFC-0128: verify a saved unreferenced-blob preview

- **Status:** Accepted
- **Milestone:** M145
- **Date:** 2026-08-27

## Summary

Add strict, bounded admission for one saved M143/M144 unreferenced-blob preview
and a pure offline verifier that recomputes the preview from the exact asset
build plan and one already-admitted M138 fingerprint. Expose the operation
through one read-only CLI composition with no cache argument.

## Problem

M143 derives a path-free aggregate preview from a live verified cache
observation, and M144 derives the same preview from one saved fingerprint after
the cache is absent. A later consumer can store those bytes, but it has no
single strict entry point for admitting them and proving that they match the
exact plan and fingerprint it intends to use. Ad hoc JSON parsing would weaken
the existing exact-schema, bounded-input, and canonical-byte boundaries.

## Decision

M145 adds:

- a 2,048-byte hard maximum and tightening-only limits value for saved preview
  records;
- a duplicate-rejecting, non-finite-rejecting, UTF-8, exact-schema canonical
  decoder for `ludoweave.asset-cache-unreferenced-preview/1`;
- a pure verifier that accepts exact frozen plan, fingerprint, and preview
  values, invokes unchanged M143 derivation once, and requires exact equality;
- a fixed
  `ludoweave.asset-cache-unreferenced-preview-verification/1` success record
  binding the plan, observation, fingerprint protocol, preview protocol, and
  SHA-256 of the exact canonical preview bytes; and
- `source asset-cache-unreferenced-preview-verify`, which preflights current
  sources, lock, and regenerated plan before two project-confined bounded reads.

The CLI reads the fingerprint under M139's unchanged 65,536-byte bound and
strict decoder, then reads the preview under the new bound and decoder. It has
no cache argument, performs no cache access, and writes neither project nor
cache state.

## Failure behavior

Invalid limits or exact-value types fail during configuration. Oversized,
non-UTF-8, duplicate-key, non-finite, structurally invalid, or noncanonical
preview bytes fail during decoding. A valid preview that differs from pure
recomputation fails with a stable field-specific verification mismatch. The
CLI emits the existing structured error envelope on standard error and exits
2; success emits one canonical JSON document and exits 0.

Current-input preflight occurs before either saved-record path is resolved or
read. This prevents stale source or plan state from being hidden by an absent
or invalid evidence file.

## Security and trust boundary

Verification establishes internal integrity only: the admitted saved preview
equals the deterministic preview derived from the exact supplied plan and
fingerprint. It does not establish authenticity, provenance, writer identity,
chronology, freshness, a trusted timestamp, an atomic current-cache snapshot,
or deletion eligibility. Those properties require separate policy and trust
roots.

The fixed report contains no blob digest, cache key, URI, path, filename,
payload, timestamp, or age. It grants no retention, cleanup, prune, repair,
deletion, eviction, or mutation authority.

## Alternatives considered

- Re-read the cache during verification. Rejected because it changes an
  offline evidence check into a fresh observation and prevents use after the
  originating cache is absent.
- Accept ordinary parsed JSON. Rejected because duplicate keys, noncanonical
  encodings, widened schemas, and ambiguous numeric forms would weaken exact
  evidence identity.
- Sign or timestamp the record. Deferred because authenticity and trusted time
  require an explicit key, identity, and policy design outside this slice.
- Return candidate identities. Rejected because M145 verifies existing fixed
  aggregate evidence and grants no deletion authority.

## Compatibility and operations

All new Python exports remain experimental. Existing M137-M144 bytes and
protocols are unchanged. There is no runtime dependency, version, cache layout,
workflow, runner allocation, permission, credential, release, or CI change.

## Validation

Acceptance requires unit tests for canonical round-trip, strict schema and
limits, exact types, tampering, and stable errors; integration tests for
cache-absent success, tampering, and preflight ordering; architecture tests for
purity, bounded reads, preserved protected surfaces, documentation, and wheel
coverage; an isolated no-dependency installed-wheel smoke; strict docs; the
supported Python matrix; reproducible artifacts; and findings-first review.

## References

- [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html)
- [Python 3.12 `json` documentation](https://docs.python.org/3.12/library/json.html)
- [SLSA artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts)
- [GitHub Actions workflow triggers](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
