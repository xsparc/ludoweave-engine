# RFC-0098: Scope sample-bundle byte reproducibility to the release environment

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

The release sample producer fixes its source inventory, member order,
timestamps, host marker, permissions, compression method, and requested
compression level. Repeating that producer within one resolved environment
therefore provides a useful byte-identity check.

The DEFLATE implementation is not fixed by the Python language version range.
Python 3.14 changed the implementation used by default Windows binaries from
zlib to zlib-ng. Python exposes build and runtime version constants and, from
3.14, `ZLIBNG_VERSION` when applicable. API compatibility does not require two
implementations to choose identical compressed representations.

Exact Windows probes staged the fixed 50-member sample bundle twice on each of
CPython 3.12.13, 3.13.13, and 3.14.5. Each runtime repeated identical bytes
within its own resolved environment. CPython 3.12 and 3.13 used zlib 1.3.1 and
emitted the same 111,168-byte archive. CPython 3.14 used zlib-ng 2.2.4 through
the zlib-compatible API and emitted a different 111,413-byte archive. The
result is cross-environment implementation variance, not nondeterminism within
one environment.

The existing tag workflow builds distributions and stages the sample bundle in
one baseline CPython 3.12 job. RFC-0021 separately scopes wheel/sdist byte
reproducibility to repeated same-source builds in one validated job and already
rejects a general cross-platform reproducible-build claim.

## Decision

Scope sample-bundle byte reproducibility to the release environment. Repeated
sample production within one fixed resolved release job environment must be
byte-identical. The existing baseline CPython 3.12 tag job remains the official
producer environment.

Supported CPython 3.12-3.14 runtimes remain compatible consumers, verifiers,
and local staging environments. Runtime support does not create a cross-runtime
byte-identity promise. Local staging is not rejected when it produces a
different valid compressed representation.

This is one sample-bundle reproducibility-scope decision. The fixed producer
continues to request `compresslevel=9`, and complete release smoke continues to
validate the archive independently of producer byte identity.

## Boundary

M115 adds no cross-runtime byte-identity claim, compressor allowlist,
compressor pin, compressor-identity manifest field, runtime rejection,
recompression, archive normalization pass, or new sample-byte verifier. It
does not widen RFC-0021's wheel/sdist claim.

M115 adds no workflow, runner allocation, matrix entry, action, permission,
credential, dependency, lock, version, runtime package/API, verifier, sample
producer, release mutation, release authority, tag, release, or publication.
It is not a general reproducible-build claim and is not a real public release
observation.

## Consequences

- Repeat sample production in the fixed release environment remains an exact
  byte-identity expectation.
- Supported runtimes may emit different valid compressed bytes while retaining
  the same source inventory and established complete-release acceptance.
- Public release manifests remain independent of compressor implementation
  identity.
- Changing the official producer environment requires renewed reproducibility
  qualification and documentation review.

## Alternatives considered

- Require cross-runtime identical sample bytes. Rejected because supported
  zlib-compatible implementations can select different valid compressed
  representations.
- Reject staging outside baseline CPython 3.12. Rejected because runtime
  compatibility and local release-tool usability do not require producer-byte
  identity.
- Publish compressor identity in the release manifest. Rejected because it
  would expand the public format without creating cross-runtime identity or
  improving complete-release verification.
- Add another CI matrix. Rejected because the existing fixed producer job and
  supported-runtime tests cover the accepted boundary without additional
  runner allocation.

## References

- [Python 3.14.0 release](https://www.python.org/downloads/release/python-3140/)
- [What's new in Python 3.14](https://docs.python.org/3.14/whatsnew/3.14.html#zlib)
- [Python `zlib` implementation-version constants](https://docs.python.org/3.14/library/zlib.html#module-zlib)
- [RFC-0021: enforce distribution reproducibility](0021-enforce-distribution-reproducibility.md)
- [RFC-0097: retain sample-member compression-level non-observability](0097-retain-sample-member-compression-level-non-observability.md)
