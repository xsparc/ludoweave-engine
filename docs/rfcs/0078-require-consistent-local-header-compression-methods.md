# RFC-0078: Require consistent local-header compression methods

- **Status:** Accepted
- **Date:** 2026-08-23
- **Decision owners:** LudoWeave maintainers

## Context

M94 proves that each already bounded two-byte local general-purpose flag equals
the corresponding parser-exposed central value. It intentionally does not
compare the compression method duplicated in the local and central records.

PKWARE APPNOTE 6.3.10 sections 4.3.7 and 4.3.12 define a two-byte compression
method in both records for a member. Python exposes the central record's value
as public `ZipInfo.compress_type` and its local-header location as
`ZipInfo.header_offset`.

On exact CPython 3.12.13, 3.13.13, and 3.14.5, changing only the second local
header's method from deflate 8 to stored 0 leaves central methods `[8, 8]`,
preserves offsets `[0, 54]`, and permits both payloads to be read. This decision
relies only on that observed admission gap, not on private Python names or
exception text.

## Decision

After M94 flag consistency, private complete release smoke reads exactly two
bytes at `ZipInfo.header_offset + 8` from the owned checksum-admitted snapshot.
The little-endian local value must equal the corresponding central
`ZipInfo.compress_type`. A mismatch raises stable, content-silent error
`sample bundle local header compression methods are inconsistent`.

This one two-byte local-compression-method consistency classifier runs before
decoded-name policy, member metadata, exact inventory, staging, or member
reads. Every established policy through M94 retains precedence. The M91 fixed-
prefix bound makes each two-byte read finite, the helper restores the snapshot
position, and the existing `ExitStack` closes the source, snapshot, and archive
before an error returns. An empty parsed inventory satisfies this aggregate
rule and retains the later exact-inventory behavior.

## Boundary

M95 performs no local extra-field comparison or parsing, no
version/time/CRC/size comparison, no method allowlist, no field-wide local/
central consistency check, no complete local-record or payload bound, no next-
header bound, no gap, adjacency, contiguity, physical non-overlap rule, or
inter-member layout validator, and no archive repair. Reading this fixed two-
byte field is not a general local-header or central-directory parser.

M95 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this fixed-producer
policy is not a general archive sandbox.

## Consequences

- Any local/central compression-method mismatch fails before decoded names,
  metadata, exact inventory, staging, or reads.
- Every established policy through M94 retains precedence.
- The fixed 50-member producer remains unchanged and compatible.
- The error exposes no archive-controlled name, method, bytes, or offset.
- Existing central compression-method policy retains responsibility for the
  admitted method profile; M95 does not broaden or duplicate that allowlist.
- There is no version/time/CRC/size comparison and no inter-member layout
  validator.
- Standard-library member reads retain responsibility for later local-header
  fields, payload extents, overlap checks, decompression, and CRC validation.

## Alternatives considered

- Defer local/central method mismatch to member reads. Rejected because
  supported Python versions ignore the demonstrated local-only stored value.
- Validate only the local method against the supported central allowlist.
  Rejected because that would admit contradictory supported values.
- Compare every remaining local and central fixed field. Rejected because
  version, time, CRC, and size consistency are materially broader policies with
  different descriptor and ZIP64 semantics.
- Parse raw central records. Rejected because public `ZipInfo.compress_type`
  and `header_offset` provide the required central value and local pointer.
- Bound payloads, next headers, gaps, adjacency, or overlap. Rejected because
  those require broader record parsing and inter-member layout policy.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `zipfile` documentation](https://docs.python.org/3/library/zipfile.html)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0077: require consistent local-header flags](0077-require-consistent-local-header-flags.md)
- [RFC-0059: reject enhanced-deflate sample members](0059-reject-enhanced-deflate-sample-members.md)
- [RFC-0047: bound sample-bundle extraction](0047-bounded-sample-bundle-extraction.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
