# RFC-0083: Require consistent local-header compressed sizes

- **Status:** Accepted
- **Date:** 2026-08-24
- **Decision owners:** LudoWeave maintainers

## Context

M99 proves equality between each bounded local CRC-32 field and public central
`ZipInfo.CRC`. It intentionally does not compare the adjacent four-byte
compressed-size values in corresponding local and central member records.

PKWARE APPNOTE 6.3.10 sections 4.3.3, 4.3.7, and 4.3.12 define little-endian
ZIP fields and a four-byte compressed-size field in both records. Python
exposes the central result as public `ZipInfo.compress_size` and the local-
header location as public `ZipInfo.header_offset`.

On exact CPython 3.12.13, 3.13.13, and 3.14.5, changing only the second
member's local compressed size from `11` to `12` leaves both central sizes at
`11` and permits both payloads to be read. This decision uses only that
observed admission gap, public attributes, and the documented record
structure.

## Decision

After M99 CRC-32 consistency, private complete release smoke reads exactly
four bytes at `ZipInfo.header_offset + 18`. Those local bytes must equal public
central `ZipInfo.compress_size` encoded as an unsigned four-byte little-endian
value.

- Stable error: `sample bundle local header compressed sizes are inconsistent`.

This one four-byte local-compressed-size consistency classifier runs before
decoded-name policy, member metadata, exact inventory, staging, or member
reads. Every established policy through M99 retains precedence. M91 already
bounds the complete fixed local-header prefix, the helper restores the
caller's snapshot position, and the existing `ExitStack` closes the source,
snapshot, and archive before an error returns. An empty parsed inventory
satisfies this aggregate rule and retains the later exact-inventory behavior.

## Boundary

M100 defines duplicate-field equality only. It performs no decompression or
recompression, no uncompressed-size comparison, no compression-ratio or
archive-bomb policy, no payload-integrity certification, no field-wide local/
central comparison, no complete local-record bound, no payload or next-header
bound, and no gap, adjacency, contiguity, physical non-overlap rule, or inter-
member layout validator. Exact equality is a fixed-producer profile, not a
claim that every valid ZIP producer must use matching local and central
values.

APPNOTE's data-descriptor and ZIP64 exceptions are outside this admitted
profile: established policy rejects general-purpose bit 3 and ZIP64 extra
fields before M100 runs. Established central-directory-encryption policy also
rejects bit 13 before this classifier.

M100 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this fixed-producer
policy is not a general archive sandbox.

## Consequences

- Any local/central four-byte compressed-size mismatch fails before decoded
  names, metadata, exact inventory, staging, or reads.
- Every established policy through M99 retains precedence.
- Equal compressed-size fields remain admitted without reading or interpreting
  payload content during preflight.
- The fixed 50-member producer remains unchanged with matching local and
  central compressed-size bytes.
- The error exposes no archive-controlled name, size, offset, or member
  position.
- Standard-library member reads retain responsibility for decompression and
  CRC validation against the admitted central metadata.

## Alternatives considered

- Decompress or recompress members during preflight. Rejected because that
  would read payload content before exact inventory and duplicate extraction
  work.
- Compare both compressed and uncompressed sizes in one step. Rejected because
  each duplicated field requires an independently evidenced boundary and
  precedence rule.
- Derive payload boundaries from compressed sizes. Rejected because that is a
  separate physical-layout policy involving the next header or central
  directory.
- Parse raw central records. Rejected because public `ZipInfo.compress_size`
  and `header_offset` provide the required central value and local pointer.
- Repair the local field. Rejected because release smoke is a validator and
  has no archive-mutation authority.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0082: require consistent local-header CRC-32 values](0082-require-consistent-local-header-crcs.md)
- [RFC-0074: bound local-header prefixes](0074-bound-local-header-prefixes.md)
- [RFC-0063: reject ZIP64 extra fields](0063-reject-zip64-extra-fields.md)
- [RFC-0061: reject data-descriptor sample members](0061-reject-data-descriptor-sample-members.md)
- [RFC-0052: reject encrypted sample members before extraction](0052-reject-encrypted-sample-members.md)
- [RFC-0053: bind sample-archive parsing and publication to its checksum](0053-bind-sample-archive-checksum.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
- [RFC-0055: normalize sample ZIP failures content-silently](0055-content-silent-sample-zip-failures.md)
- [RFC-0056: normalize sample ZIP text failures content-silently](0056-content-silent-sample-zip-text-failures.md)
- [RFC-0057: normalize sample ZIP decompression failures content-silently](0057-content-silent-sample-zip-decompression-failures.md)
