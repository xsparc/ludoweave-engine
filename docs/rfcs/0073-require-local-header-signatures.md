# RFC-0073: Require local-header signatures

- **Status:** Accepted
- **Date:** 2026-08-14
- **Decision owners:** LudoWeave maintainers

## Context

The fixed release sample producer writes every member with the four-byte
local-header signature `PK\x03\x04` at its parser-exposed `ZipInfo.header_offset`.
M89 proves only that those public offsets remain before the conventional central
directory; it does not prove that they identify local headers.

PKWARE APPNOTE 6.3.10 assigns an identifying signature to each ZIP record type
and defines `0x04034b50` for a local file header. Python documents
`ZipInfo.header_offset` as the byte offset to the file header.

Supported CPython 3.12.13, 3.13.13, and 3.14.5 expose a two-member fixture whose
second central pointer alone is shifted by one byte as `[0, 47]`. The first
payload remains readable. Opening the malformed second member raises public
`BadZipFile`; the decision does not depend on that exception's message.

## Decision

Private complete release smoke checks each parser-exposed offset against the
owned checksum-admitted snapshot after the M89 bounds rule. The next four bytes
must equal `PK\x03\x04`. Any mismatch or short read raises the stable,
content-silent error `sample bundle local header signature is inconsistent`.

This is a four-byte local-header signature classifier. It runs before decoded
name policy, member metadata, exact inventory, staging, or member reads. Every
established policy through M89 retains precedence, and the existing
`ExitStack` closes the source, snapshot, and archive before an error returns.
An empty parsed inventory satisfies this aggregate rule and retains the later
exact-inventory behavior.

## Boundary

M90 adds no local-header field parser, central-directory record parser, record
extent, gap, adjacency, contiguity, payload-bound, or physical non-overlap rule,
and no inter-member layout validator or archive repair.

M90 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this fixed-producer
policy is not a general archive sandbox.

## Consequences

- A public offset that does not identify the expected local-header record type
  fails before decoded names, metadata, exact inventory, staging, or reads.
- Every established policy through M89 retains precedence.
- The fixed 50-member producer remains unchanged and compatible.
- The error exposes no archive-controlled bytes, offset, member name, or path.
- The classifier does not establish local-header fields or physical member
  layout; standard-library reads retain their later bounded validation role.

## Alternatives considered

- Defer every malformed pointer to member reads. Rejected because that permits
  a known fixed-producer violation past aggregate metadata preflight.
- Parse local-header fields. Rejected because the record-type signature alone
  establishes the narrow property selected for M90.
- Validate record extents, adjacency, gaps, and overlap. Rejected because that
  requires a materially broader inter-member layout validator.
- Depend on CPython's current `BadZipFile` text. Rejected because public error
  wording is not part of this policy.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo.header_offset` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo.header_offset)
- [RFC-0072: bound local-header offsets before the central directory](0072-bound-local-header-offsets.md)
