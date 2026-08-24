# RFC-0084: Require consistent local-header uncompressed sizes

- **Status:** Accepted
- **Date:** 2026-08-24
- **Decision owners:** LudoWeave maintainers

## Context

M100 proves equality between each bounded local compressed-size field and
public central `ZipInfo.compress_size`. It intentionally does not compare the
adjacent four-byte uncompressed-size values in corresponding local and central
member records.

PKWARE APPNOTE 6.3.10 sections 4.3.3, 4.3.7, and 4.3.12 define little-endian
ZIP fields and a four-byte uncompressed-size field in both records. Python
exposes the central result as public `ZipInfo.file_size` and the local-header
location as public `ZipInfo.header_offset`.

On exact CPython 3.12.13, 3.13.13, and 3.14.5, changing only the second
member's local uncompressed size from `9` to `10` leaves both central sizes at
`9` and permits both payloads to be read. This decision uses only that observed
admission gap, public attributes, and the documented record structure.

## Decision

After M100 compressed-size consistency, private complete release smoke reads
exactly four bytes at `ZipInfo.header_offset + 22`. Those local bytes must equal
public central `ZipInfo.file_size` encoded as an unsigned four-byte little-
endian value.

- Stable error: `sample bundle local header uncompressed sizes are inconsistent`.

This one four-byte local-uncompressed-size consistency classifier runs before
decoded-name policy, member metadata, exact inventory, staging, or member
reads. Every established policy through M100 retains precedence. M91 already
bounds the complete fixed local-header prefix, the helper restores the caller's
snapshot position, and the existing `ExitStack` closes the source, snapshot,
and archive before an error returns. An empty parsed inventory satisfies this
aggregate rule and retains the later exact-inventory behavior.

## Boundary

M101 defines duplicate-field equality only. It performs no decompression or
recompression, no payload-content read during preflight, no compression-ratio
policy, no archive-bomb classification, no payload-integrity certification, no
field-wide local/central comparison, no complete local-record bound, no payload
or next-header bound, and no gap, adjacency, contiguity, physical non-overlap
rule, or inter-member layout validator. Exact equality is a fixed-producer
profile, not a claim that every valid ZIP producer must use matching local and
central values.

APPNOTE's data-descriptor and ZIP64 exceptions are outside this admitted
profile: established policy rejects general-purpose bit 3 and ZIP64 extra
fields before M101 runs. Established central-directory-encryption policy also
rejects bit 13 before this classifier.

M101 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this fixed-producer
policy is not a general archive sandbox.

## Consequences

- Any local/central four-byte uncompressed-size mismatch fails before decoded
  names, metadata, exact inventory, staging, or reads.
- Every established policy through M100 retains precedence.
- Equal uncompressed-size fields remain admitted without reading or
  interpreting payload content during preflight.
- The fixed 50-member producer remains unchanged with matching local and
  central uncompressed-size bytes.
- The error exposes no archive-controlled name, size, offset, or member
  position.
- Standard-library member reads retain responsibility for decompression and
  CRC validation against the admitted central metadata.

## Alternatives considered

- Decompress members to count their bytes during preflight. Rejected because
  that would read payload content before exact inventory and duplicate
  extraction work.
- Derive a compression-ratio or archive-bomb policy from both size fields.
  Rejected because that requires separately chosen limits and threat-model
  evidence.
- Derive payload boundaries from compressed sizes. Rejected because that is a
  separate physical-layout policy involving the next header or central
  directory.
- Parse raw central records. Rejected because public `ZipInfo.file_size` and
  `header_offset` provide the required central value and local pointer.
- Repair the local field. Rejected because release smoke is a validator and
  has no archive-mutation authority.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0083: require consistent local-header compressed sizes](0083-require-consistent-local-header-compressed-sizes.md)
- [RFC-0074: bound local-header prefixes](0074-bound-local-header-prefixes.md)
- [RFC-0063: reject ZIP64 extra fields](0063-reject-zip64-extra-fields.md)
- [RFC-0061: reject data-descriptor sample members](0061-reject-data-descriptor-sample-members.md)
- [RFC-0052: reject encrypted sample members before extraction](0052-reject-encrypted-sample-members.md)
- [RFC-0053: bind sample-archive parsing and publication to its checksum](0053-bind-sample-archive-checksum.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
- [RFC-0055: normalize sample ZIP failures content-silently](0055-content-silent-sample-zip-failures.md)
- [RFC-0056: normalize sample ZIP text failures content-silently](0056-content-silent-sample-zip-text-failures.md)
- [RFC-0057: normalize sample ZIP decompression failures content-silently](0057-content-silent-sample-zip-decompression-failures.md)
