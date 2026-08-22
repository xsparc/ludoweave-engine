# RFC-0081: Require consistent local-header timestamps

- **Status:** Accepted
- **Date:** 2026-08-23
- **Decision owners:** LudoWeave maintainers

## Context

M97 proves equality between each bounded local extraction-version pair and
public central `ZipInfo.extract_version` plus `ZipInfo.reserved`. It
intentionally does not compare the adjacent four timestamp bytes in
corresponding local and central member records.

PKWARE APPNOTE 6.3.10 sections 4.3.7, 4.3.12, and 4.4.6 define a two-byte
MS-DOS modification time followed by a two-byte MS-DOS modification date in
both records. Python exposes the central result as public `ZipInfo.date_time`
and the local-header location as public `ZipInfo.header_offset`. The documented
central tuple represents local time, has two-second precision, and is not UTC.

On exact CPython 3.12.13, 3.13.13, and 3.14.5, changing only the low byte of
the second member's local time from `c4` to `e4` leaves both central tuples at
`(2026, 8, 23, 4, 6, 8)` and permits both payloads to be read. This decision
uses only that observed admission gap, public attributes, and documented
record structure.

## Decision

After M97 extraction-version consistency, private complete release smoke reads
exactly four bytes at `ZipInfo.header_offset + 10`. It reconstructs the
corresponding central MS-DOS bytes from public `ZipInfo.date_time` using the
documented two-second representation. The local and central bytes must be
equal.

- Stable error: `sample bundle local header timestamps are inconsistent`.

This one four-byte local-timestamp consistency classifier runs before decoded-
name policy, member metadata, exact inventory, staging, or member reads. Every
established policy through M97 retains precedence. M91 already bounds the
complete fixed local-header prefix, the helper restores the caller's snapshot
position, and the existing `ExitStack` closes the source, snapshot, and archive
before an error returns. An empty parsed inventory satisfies this aggregate
rule and retains the later exact-inventory behavior.

## Boundary

M98 defines duplicate-field equality only. It is no timestamp semantics
validator and performs no timezone or UTC conversion, wall-clock comparison,
calendar validation, reproducibility rule, canonical-date policy, extended-
timestamp or NTFS-extra interpretation, or sub-second recovery. Exact equality
is a fixed-producer profile, not a claim that every valid ZIP producer must use
matching local and central values.

APPNOTE's masked-local-header exception when central-directory encryption bit
13 is set is outside this admitted profile: the established encryption-flag
policy rejects that bit before M98 runs.

M98 performs no CRC/size comparison, field-wide local/central comparison,
complete local-record or payload bound, next-header bound, gap, adjacency,
contiguity, physical non-overlap rule, or inter-member layout validator, and no
archive repair. It adds no workflow, runner allocation, action, permission,
credential, dependency, lock, version, runtime package/API, sample producer,
release mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this fixed-producer
policy is not a general archive sandbox.

## Consequences

- Any local/central four-byte timestamp mismatch fails before decoded names,
  metadata, exact inventory, staging, or reads.
- Every established policy through M97 retains precedence.
- Equal DOS timestamps remain admitted without assigning UTC meaning or
  validating alternate timestamp extra fields.
- The fixed 50-member producer remains unchanged with matching local and
  central timestamp bytes.
- The error exposes no archive-controlled name, timestamp, offset, or member
  position.
- Standard-library member reads retain responsibility for payload extents,
  overlap checks, decompression, and CRC validation.

## Alternatives considered

- Convert both values to UTC before comparison. Rejected because the central
  DOS tuple is documented as local time and M98 needs no timezone policy.
- Validate calendar semantics or require one reproducible timestamp. Rejected
  because M98 addresses duplicate-field consistency, not timestamp meaning.
- Compare extended timestamp or NTFS extra fields. Rejected because those
  formats require separate parsing and precedence policy.
- Defer local-only changes to member reads. Rejected because every supported
  Python version ignores the demonstrated mutation.
- Compare CRC, sizes, or every remaining fixed field. Rejected because each
  needs separate policy, including data-descriptor and ZIP64 interactions.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0080: require consistent local-header extraction versions](0080-require-consistent-local-header-extraction-versions.md)
- [RFC-0074: bound local-header prefixes](0074-bound-local-header-prefixes.md)
