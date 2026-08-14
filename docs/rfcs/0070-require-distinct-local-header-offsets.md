# RFC-0070: Require distinct local-header offsets

- **Status:** Accepted
- **Date:** 2026-08-14
- **Decision owners:** LudoWeave maintainers

## Context

The fixed release sample producer writes 50 members whose central-directory
entries expose 50 distinct `ZipInfo.header_offset` values.

PKWARE APPNOTE sections 4.3.2, 4.3.6, 4.3.12, and 4.4.24 assign each stored
file a preceding local header, a corresponding central record, and a relative
offset identifying that local header. Supported CPython 3.12.13, 3.13.13, and
3.14.5 nevertheless expose offsets `[0, 0]` when two central entries point at
one local header. Reading the first entry succeeds with an overlap warning;
reading the aliased second entry later raises a local/central filename
mismatch.

That deferred failure is unnecessary for the fixed producer and occurs after
the current verifier has begun staging.

## Decision

Private complete release smoke checks the parsed `ZipInfo` inventory after M86
and requires every `header_offset` value to be distinct. Any duplicate raises
stable content-silent error `sample bundle local header offsets are
inconsistent`.

Complete release smoke first finishes every established policy through M86.
M87 then validates offset distinctness before M77 decoded-name policy, member
metadata, exact inventory, staging, or member reads. The existing `ExitStack`
closes the source, snapshot, and archive before an error returns.

Empty and single-member parsed inventories satisfy this aggregate rule and
retain the established later exact-inventory behavior.

## Boundary

M87 checks one aggregate property of public parser metadata. It adds no local-
header parser, no central-directory parser, no offset ordering, range,
contiguity, or non-overlap rule, no inter-member layout validator, no local/
central field-consistency validator, no record-signature classifier, and no
archive repair. It does not use CPython's private `_end_offset` bookkeeping.

M87 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this policy is not a
general archive sandbox.

## Consequences

- Parser-exposed local-header aliases fail before decoded names, metadata,
  exact inventory, staging, or reads.
- Every established policy through M86 retains precedence.
- The fixed 50-member producer remains unchanged and compatible.
- The error exposes no archive-controlled offset, member name, or path.
- Distinct offsets do not establish their ordering, bounds, adjacency, or
  physical non-overlap.
- Actual local-header signature and name consistency remains enforced by the
  standard reader during the later bounded member reads.

## Alternatives considered

- Continue deferring aliases to standard-reader member-open behavior. Rejected
  because the fixed producer has no aliases and the later failure begins only
  after staging exists.
- Use CPython's private `_end_offset` overlap bookkeeping. Rejected because it
  is not a public cross-version contract.
- Parse local headers and central records directly. Rejected because public
  `header_offset` values are sufficient for this bounded profile rule.
- Validate ordering, gaps, ranges, and overlap. Rejected because that requires
  a materially broader inter-member layout validator.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython `zipfile` implementation](https://github.com/python/cpython/blob/main/Lib/zipfile/__init__.py)
- [RFC-0069: require the first local-header offset at zero](0069-require-first-local-header-at-zero.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
