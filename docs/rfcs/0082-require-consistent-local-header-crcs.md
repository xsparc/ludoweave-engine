# RFC-0082: Require consistent local-header CRC-32 values

- **Status:** Accepted
- **Date:** 2026-08-23
- **Decision owners:** LudoWeave maintainers

## Context

M98 proves equality between each bounded local DOS timestamp and public central
`ZipInfo.date_time`. It intentionally does not compare the adjacent four-byte
CRC-32 values in corresponding local and central member records.

PKWARE APPNOTE 6.3.10 sections 4.1.5, 4.3.7, 4.3.12, and 4.4.7 define CRC-32
integrity and a four-byte CRC-32 field in both records. Python exposes the
central result as public `ZipInfo.CRC` and the local-header location as public
`ZipInfo.header_offset`. CPython member reads use the central value as their
expected CRC.

On exact CPython 3.12.13, 3.13.13, and 3.14.5, changing only the low bit of the
second member's local CRC from `2868864084` to `2868864085` leaves central CRCs
at `[3724039362, 2868864084]` and permits both payloads to be read. This
decision uses only that observed admission gap, public attributes, and the
documented record structure.

## Decision

After M98 timestamp consistency, private complete release smoke reads exactly
four bytes at `ZipInfo.header_offset + 14`. Those local bytes must equal public
central `ZipInfo.CRC` encoded as an unsigned four-byte little-endian value.

- Stable error: `sample bundle local header CRC-32 values are inconsistent`.

This one four-byte local-CRC-32 consistency classifier runs before decoded-name
policy, member metadata, exact inventory, staging, or member reads. Every
established policy through M98 retains precedence. M91 already bounds the
complete fixed local-header prefix, the helper restores the caller's snapshot
position, and the existing `ExitStack` closes the source, snapshot, and archive
before an error returns. An empty parsed inventory satisfies this aggregate
rule and retains the later exact-inventory behavior.

## Boundary

M99 defines duplicate-field equality only. It performs no CRC recomputation,
payload read, payload-integrity certification, polynomial selection, CRC
repair, no compressed/uncompressed size comparison, no field-wide local/central
comparison, complete local-record bound, payload or next-header bound, gap,
adjacency, contiguity, physical non-overlap rule, or inter-member layout
validator. Exact equality is a fixed-producer profile, not a claim that every
valid ZIP producer must use matching local and central values.

APPNOTE's data-descriptor and masked-local-header exceptions are outside this
admitted profile: established policy rejects general-purpose bit 3 and central-
directory-encryption bit 13 before M99 runs. Established ZIP64 extra-field
policy also rejects the fixed sample profile's ZIP64 alternative before M99.

M99 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this fixed-producer
policy is not a general archive sandbox.

## Consequences

- Any local/central four-byte CRC-32 mismatch fails before decoded names,
  metadata, exact inventory, staging, or reads.
- Every established policy through M98 retains precedence.
- Equal CRC fields remain admitted without recomputing or certifying payload
  integrity during preflight.
- The fixed 50-member producer remains unchanged with matching local and
  central CRC bytes.
- The error exposes no archive-controlled name, CRC, offset, or member
  position.
- Standard-library member reads retain responsibility for decompression and
  CRC validation against the admitted central value.

## Alternatives considered

- Recompute each CRC during preflight. Rejected because that would read payload
  content before exact inventory and duplicate extraction work.
- Trust member reads alone. Rejected because every supported Python version
  ignores the demonstrated local-only mutation.
- Compare CRC and both sizes in one step. Rejected because size equality and
  payload extent each require their own boundary, precedence, and ZIP64
  analysis.
- Parse raw central records. Rejected because public `ZipInfo.CRC` and
  `header_offset` provide the required central value and local pointer.
- Repair the local field. Rejected because release smoke is a validator and has
  no archive-mutation authority.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0081: require consistent local-header timestamps](0081-require-consistent-local-header-timestamps.md)
- [RFC-0074: bound local-header prefixes](0074-bound-local-header-prefixes.md)
- [RFC-0063: reject ZIP64 extra fields](0063-reject-zip64-extra-fields.md)
- [RFC-0061: reject data-descriptor sample members](0061-reject-data-descriptor-sample-members.md)
- [RFC-0052: reject encrypted sample members before extraction](0052-reject-encrypted-sample-members.md)
- [RFC-0053: bind sample-archive parsing and publication to its checksum](0053-bind-sample-archive-checksum.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
- [RFC-0055: normalize sample ZIP failures content-silently](0055-content-silent-sample-zip-failures.md)
- [RFC-0056: normalize sample ZIP text failures content-silently](0056-content-silent-sample-zip-text-failures.md)
- [RFC-0057: normalize sample ZIP decompression failures content-silently](0057-content-silent-sample-zip-decompression-failures.md)
