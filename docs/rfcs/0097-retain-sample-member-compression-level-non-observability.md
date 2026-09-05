# RFC-0097: Retain sample-member compression-level non-observability

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

PKWARE assigns general-purpose bits 1 and 2 broad option categories for
Deflate methods: normal, maximum, fast, and super fast. Those categories are
not an exact numeric compressor-level field. M105 already requires every
sample member's complete general-purpose flag value to be zero after the
established specific-flag checks.

Python's `compresslevel` parameter controls writing. Deflate accepts levels
`0` through `9`. CPython 3.13 added public `ZipInfo.compress_level` as the
writer-configuration counterpart to the older protected `_compresslevel`
attribute. A newly parsed `ZipInfo` initializes that value as unknown rather
than reconstructing it from member bytes.

Exact CPython 3.12.13, 3.13.13, and 3.14.5 probes requested Deflate levels `0`,
`1`, `6`, and `9`. Every reopened member reported method `8`, extraction
version `20`, flags `0`, an unknown protected level, and readable payload bytes.
CPython 3.12 exposed no public level attribute; 3.13 and 3.14 exposed it as
unknown. The controlled levels `6` and `9` produced identical archive bytes on
all three supported runtimes, so those bytes do not distinguish even those two
requested settings for that payload.

The fixed 50-member LudoWeave producer explicitly passes `compresslevel=9`.
That source configuration is the producer contract. Its reopened members do
not carry an exact recovered level.

## Decision

Retain sample-member compression-level non-observability. Complete release
smoke does not inspect `ZipInfo.compress_level`, protected `_compresslevel`,
compressed payload bytes, or compressed size to admit, reject, or infer an
exact compressor level.

The fixed producer continues to request level `9`. M105's zero general-purpose
flags remain the exact stored-metadata profile, not proof of a numeric level.
M113's stored/deflated method compatibility and M95's local/central method
agreement remain unchanged.

This is one compression-level non-observability decision. It adds no error
category or precedence change.

## Boundary

M114 adds no exact level-9 verifier profile, no inferred compressor level, no
compression-ratio policy, no recompression, no raw Deflate parser, no payload-
content read, no repair, and no general ZIP validity claim. It is not a general
archive sandbox and is not a real public release observation.

M114 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, verifier, sample producer,
release mutation, release authority, tag, release, or publication.

## Consequences

- Standard-library Deflate members remain admitted across writer compression
  levels when every established check passes.
- The fixed producer's explicit level `9` remains reproducible writer
  configuration rather than verifier-visible provenance.
- M105's zero-flag policy remains authoritative for stored option bits without
  claiming an exact numeric level.
- No member is decompressed until all existing preflight and inventory checks
  have passed.

## Alternatives considered

- Require exact writer level `9`. Rejected because reopened member metadata
  does not recover that configuration and controlled levels can produce
  identical bytes.
- Infer a level from compressed size or compressed bytes. Rejected because that
  would make admission depend on payload, compressor implementation, and a
  non-unique result rather than an encoded exact field.
- Interpret zero option bits as numeric level `6`. Rejected because PKWARE
  defines a broad normal category, not Python's level value.
- Remove the producer's explicit level. Rejected because deterministic producer
  configuration is separate from verifier admission and remains useful.

## References

- [PKWARE APPNOTE](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `zipfile` documentation](https://docs.python.org/3/library/zipfile.html)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0088: require zero sample-member general-purpose flags](0088-require-zero-sample-member-general-purpose-flags.md)
- [RFC-0096: retain sample-member compression-method compatibility](0096-retain-sample-member-compression-method-compatibility.md)
