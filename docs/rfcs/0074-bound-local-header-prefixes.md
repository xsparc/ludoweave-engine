# RFC-0074: Bound fixed local-header prefixes

- **Status:** Accepted
- **Date:** 2026-08-15
- **Decision owners:** LudoWeave maintainers

## Context

M90 proves only that each parser-exposed `ZipInfo.header_offset` identifies the
four-byte local-header signature. It does not prove that the complete fixed
local-header prefix fits before the conventional central directory.

PKWARE APPNOTE 6.3.10 section 4.3.7 defines 30 fixed bytes in a local file
header before the variable file name and extra field. Python documents
`ZipInfo.header_offset` as the byte offset to the file header.

Supported CPython 3.12.13, 3.13.13, and 3.14.5 expose a two-member fixture whose
second central pointer identifies `PK\x03\x04` only four bytes before directory
offset 94. The first payload remains readable. Opening the malformed second
member raises public `BadZipFile`; the decision does not depend on that
exception's message.

## Decision

Private complete release smoke checks every parser-exposed offset against the
owned checksum-admitted snapshot after M90 signature policy. Each offset plus
the 30-byte fixed local-header prefix must be no greater than the conventional
central-directory offset. A crossing prefix raises stable, content-silent error
`sample bundle local header prefixes are out of bounds`.

This is one arithmetic prefix-bound classifier. It runs before decoded-name
policy, member metadata, exact inventory, staging, or member reads. Every
established policy through M90 retains precedence. The shared end-record helper
restores the snapshot position, and the existing `ExitStack` closes the source,
snapshot, and archive before an error returns. An empty parsed inventory
satisfies this aggregate rule and retains the later exact-inventory behavior.

## Boundary

M91 adds no local-header field parser, filename/extra-length interpretation,
complete local-record extent, payload-bound, gap, adjacency, contiguity,
physical non-overlap rule, or inter-member layout validator, and no archive
repair.

M91 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request evidence
is not a real public release observation, and this fixed-producer policy is not
a general archive sandbox.

## Consequences

- A purported local header whose fixed prefix crosses the conventional central
  directory fails before names, metadata, exact inventory, staging, or reads.
- Every established policy through M90 retains precedence.
- The fixed 50-member producer remains unchanged and compatible.
- The error exposes no archive-controlled bytes, offset, member name, or path.
- Standard-library member reads retain responsibility for later local-header
  field and payload validation.

## Alternatives considered

- Defer malformed short prefixes to member reads. Rejected because that permits
  a known fixed-producer violation past aggregate metadata preflight.
- Parse local-header fields. Rejected because the arithmetic fixed-prefix bound
  establishes the narrow property selected for M91.
- Validate complete records, payloads, gaps, adjacency, or overlap. Rejected
  because that requires a materially broader inter-member layout validator.
- Depend on CPython's current `BadZipFile` text. Rejected because public error
  wording is not part of this policy.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo.header_offset` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo.header_offset)
- [CPython `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0073: require local-header signatures](0073-require-local-header-signatures.md)
- [RFC-0047: bound sample-bundle extraction](0047-bounded-sample-bundle-extraction.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
