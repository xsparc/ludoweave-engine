# RFC-0069: Require the first local-header offset at zero

- **Status:** Accepted
- **Date:** 2026-08-14
- **Decision owners:** LudoWeave maintainers

## Context

The fixed release sample producer writes its first local file header at byte
zero. Its 50 central-directory entries expose parser-adjusted
`ZipInfo.header_offset` values, with the earliest value equal to zero.

PKWARE APPNOTE sections 4.3.2, 4.3.6, 4.3.7, and 4.3.12 define local file
headers, their overall ordering before the central directory, and each central
header's relative local-header offset. Supported CPython 3.12.13, 3.13.13, and
3.14.5 each read the same payload when one or eleven bytes are inserted before
the first local header and both relevant relative offsets are updated. These
fixtures have zero M85 central-directory concatenation adjustment, while the
parser exposes an earliest local-header offset of one or eleven.

That broader leading-gap compatibility is unnecessary for the fixed producer.

## Decision

Private complete release smoke checks the parsed `ZipInfo` inventory after M85
and requires its minimum `header_offset` to equal zero. Any nonzero earliest
offset raises stable content-silent error `sample bundle first local header
placement is inconsistent`.

Complete release smoke first finishes every established policy through M85.
M86 then validates the parser-exposed offset before M77 decoded-name policy,
member metadata, exact inventory, staging, or member reads. The existing
`ExitStack` closes the source, snapshot, and archive before an error returns.

An empty parsed inventory retains the established later exact-inventory error;
M86 does not replace or reorder that policy.

## Boundary

M86 checks one aggregate property of public parser metadata. It adds no local-
header parser, no central-directory parser, no inter-member layout validator,
no local/central field-consistency validator, no record-signature classifier,
no prepended executable support, and no archive repair.

M86 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this policy is not a
general archive sandbox.

## Consequences

- A parser-exposed leading gap fails before decoded names, metadata, exact
  inventory, staging, or reads.
- Every established policy through M85 retains precedence.
- The fixed 50-member producer remains unchanged and compatible.
- The error exposes no archive-controlled offset, member name, or path.
- Exact adjacency among later local headers remains deferred.
- Actual local-header signature and name consistency remains enforced by the
  standard reader during the later bounded member reads.

## Alternatives considered

- Continue accepting a leading local-header gap. Rejected because the fixed
  producer starts at byte zero and needs no gap.
- Parse the first local file header. Rejected because the public parser offset
  is sufficient for this bounded profile rule.
- Validate every local-header boundary and inter-member gap. Rejected because
  that requires a materially broader record-layout parser.
- Treat M85 as proof of byte-zero local-header placement. Rejected because
  adjusted relative offsets can preserve zero concatenation adjustment.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [CPython `zipfile` implementation](https://github.com/python/cpython/blob/main/Lib/zipfile/__init__.py)
- [RFC-0068: require exact conventional central-directory placement](0068-require-exact-central-directory-placement.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
