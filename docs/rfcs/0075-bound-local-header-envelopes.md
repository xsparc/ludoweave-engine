# RFC-0075: Bound local-header variable envelopes

- **Status:** Accepted
- **Date:** 2026-08-22
- **Decision owners:** LudoWeave maintainers

## Context

M91 proves that each parser-exposed `ZipInfo.header_offset` leaves room for the
30-byte fixed local-header prefix. It does not prove that the file-name and
extra-field byte ranges declared by that prefix fit before the conventional
central directory.

PKWARE APPNOTE 6.3.10 section 4.3.7 defines two little-endian 16-bit local-
header fields at bytes 26-29: file-name length and extra-field length. Their
variable bytes follow the fixed prefix. Python documents `ZipInfo.header_offset`
as the byte offset to the file header.

Supported CPython 3.12.13, 3.13.13, and 3.14.5 expose a two-member fixture with
local-header offsets `[0, 46]` and central-directory offset `94`. Changing only
the final local file-name length to 65,535 leaves both signatures and fixed
prefixes valid, makes that local-header variable envelope end at byte 65,611,
and leaves the first payload readable. Opening the malformed second member
raises public `BadZipFile`; this decision does not depend on its message.

## Decision

Private complete release smoke reads exactly four bytes from each owned,
checksum-admitted local-header prefix after M91 policy. It interprets the two
16-bit little-endian file-name and extra-field lengths and requires
`header_offset + 30 + file_name_length + extra_field_length` to be no greater
than the conventional central-directory offset. A crossing local-header
variable envelope raises stable, content-silent error
`sample bundle local header envelopes are out of bounds`.

This two-field envelope-bound classifier runs before decoded-name policy,
member metadata, exact inventory, staging, or member reads. Every established
policy through M91 retains precedence. The shared end-record helper and the new
field reader restore the snapshot position, and the existing `ExitStack`
closes the source, snapshot, and archive before an error returns. An empty
parsed inventory satisfies this aggregate rule and retains the later exact-
inventory behavior.

## Boundary

M92 performs no local-name comparison, extra-field parsing, field-value
consistency check, complete local-record or payload bound, next-header bound,
gap, adjacency, contiguity, physical non-overlap rule, or inter-member layout
validator, and no archive repair. Reading the two declared lengths is not a
general local-header parser.

M92 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this fixed-producer
policy is not a general archive sandbox.

## Consequences

- A local-header variable envelope that crosses the conventional central
  directory fails before names, metadata, exact inventory, staging, or reads.
- Every established policy through M91 retains precedence.
- The fixed 50-member producer remains unchanged and compatible.
- The error exposes no archive-controlled length, offset, name, or path.
- Standard-library member reads retain responsibility for later local-header
  consistency and payload validation.

## Alternatives considered

- Defer malformed variable envelopes to member reads. Rejected because that
  permits a known fixed-producer violation past aggregate metadata preflight.
- Compare local and central names or extras. Rejected because M92 needs only
  the two declared lengths to establish its selected bound.
- Bound each envelope against the next local header. Rejected because that is
  a materially broader inter-member layout rule.
- Validate complete records, payloads, gaps, adjacency, or overlap. Rejected
  because those require broader record parsing and layout policy.
- Depend on CPython's current `BadZipFile` text. Rejected because public error
  wording is not part of this policy.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo.header_offset` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo.header_offset)
- [CPython `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0074: bound fixed local-header prefixes](0074-bound-local-header-prefixes.md)
- [RFC-0047: bound sample-bundle extraction](0047-bounded-sample-bundle-extraction.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
