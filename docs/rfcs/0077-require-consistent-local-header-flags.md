# RFC-0077: Require consistent local-header flags

- **Status:** Accepted
- **Date:** 2026-08-23
- **Decision owners:** LudoWeave maintainers

## Context

M93 proves that each already bounded local file-name byte-matches the
corresponding parser-exposed central name. It intentionally does not compare
the general-purpose flags duplicated in the local and central records.

PKWARE APPNOTE 6.3.10 sections 4.3.7, 4.3.12, and 4.4.4 define a two-byte
general-purpose bit flag in both records for a member. Python exposes the
central record's value as public `ZipInfo.flag_bits` and its local-header
location as `ZipInfo.header_offset`.

On exact CPython 3.12.13, 3.13.13, and 3.14.5, changing only the second local
header's flag field from zero to encryption bit 0 leaves both central flags at
zero, preserves offsets `[0, 54]`, and permits both payloads to be read. This
decision relies only on that observed admission gap, not on private Python
names or exception text.

## Decision

After M93 name consistency, private complete release smoke reads exactly two
bytes at `ZipInfo.header_offset + 6` from the owned checksum-admitted snapshot.
The little-endian local value must equal the corresponding central
`ZipInfo.flag_bits`. A mismatch raises stable, content-silent error
`sample bundle local header flags are inconsistent`.

This one two-byte local-flag consistency classifier runs before decoded-name
policy, member metadata, exact inventory, staging, or member reads. Every
established policy through M93 retains precedence. The M91 fixed-prefix bound
makes each two-byte read finite, the helper restores the snapshot position,
and the existing `ExitStack` closes the source, snapshot, and archive before an
error returns. An empty parsed inventory satisfies this aggregate rule and
retains the later exact-inventory behavior.

## Boundary

M94 performs no local compression-method comparison and no extra-field
comparison or parsing, version/time/CRC/size comparison, broad flag allowlist,
field-wide local/central consistency check, complete local-record or payload
bound, next-header bound, gap, adjacency, contiguity, physical non-overlap
rule, or inter-member layout validator, and no archive repair. Reading this
fixed two-byte field is not a general local-header or central-directory parser.

M94 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this fixed-producer
policy is not a general archive sandbox.

## Consequences

- Any local/central general-purpose flag mismatch fails before decoded names,
  metadata, exact inventory, staging, or reads.
- Every established policy through M93 retains precedence.
- The fixed 50-member producer remains unchanged and compatible.
- The error exposes no archive-controlled name, flag, bytes, or offset.
- Existing central flag policies retain responsibility for the admitted flag
  profile; M94 does not broaden or duplicate their semantic allowlists.
- Standard-library member reads retain responsibility for later local-header
  fields, payload extents, overlap checks, decompression, and CRC validation.

## Alternatives considered

- Defer local/central flag mismatch to member reads. Rejected because supported
  Python versions ignore the demonstrated local-only encryption indicator.
- Reject only local encryption or UTF-8 bits. Rejected because the fixed
  producer emits exact duplicate flag fields and a partial semantic allowlist
  would leave other contradictory representations admitted.
- Compare every local and central fixed field. Rejected because compression
  method, version, time, CRC, and size consistency are materially broader
  policies with different descriptor and ZIP64 semantics.
- Parse raw central records. Rejected because public `ZipInfo.flag_bits` and
  `header_offset` provide the required central value and local pointer.
- Bound payloads, next headers, gaps, adjacency, or overlap. Rejected because
  those require broader record parsing and inter-member layout policy.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `zipfile` documentation](https://docs.python.org/3/library/zipfile.html)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0076: require consistent local-header names](0076-require-consistent-local-header-names.md)
- [RFC-0052: reject encrypted sample members](0052-reject-encrypted-sample-members.md)
- [RFC-0061: reject data-descriptor sample members](0061-reject-data-descriptor-sample-members.md)
- [RFC-0047: bound sample-bundle extraction](0047-bounded-sample-bundle-extraction.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
