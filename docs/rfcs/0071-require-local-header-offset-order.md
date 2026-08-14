# RFC-0071: Require local-header offset order

- **Status:** Accepted
- **Date:** 2026-08-14
- **Decision owners:** LudoWeave maintainers

## Context

The fixed release sample producer writes 50 members whose parser-exposed local-
header offsets are strictly increasing in the same order returned by
`ZipFile.infolist()`.

PKWARE APPNOTE 6.3.10 permits files to appear in arbitrary order generally and
describes corresponding local-header/data and central-directory records.
Python documents that `ZipFile.infolist()` returns `ZipInfo` objects in the
actual archive-entry order. Supported CPython 3.12.13, 3.13.13, and 3.14.5
therefore expose a fixture whose first two central-directory records alone are
swapped as names `second.txt`, `first.txt` and offsets `[46, 0]`; both payloads
remain readable.

That archive is not claimed to violate ZIP generally. It deviates from the
fixed LudoWeave sample-producer profile and the current verifier otherwise
begins staging before any later behavior distinguishes it.

## Decision

Private complete release smoke checks parsed `ZipInfo` metadata after M87 and
requires strictly increasing local-header offsets in `infolist()` order. Any
non-increasing adjacent pair raises stable content-silent error `sample bundle
local header offsets are out of order`.

Complete release smoke first finishes every established policy through M87.
M88 then validates offset order before M77 decoded-name policy, member
metadata, exact inventory, staging, or member reads. M87 distinctness retains
precedence over equality, and the existing `ExitStack` closes the source,
snapshot, and archive before an error returns.

Empty and single-member parsed inventories satisfy this aggregate rule and
retain the established later exact-inventory behavior.

## Boundary

M88 checks one aggregate property of public parser metadata for a fixed
producer profile. It adds no local-header parser, no central-directory record
parser, no offset range, gap, adjacency, contiguity, or physical non-overlap
rule, and no inter-member layout validator or archive repair.

M88 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this policy is not a
general archive sandbox.

## Consequences

- Central-directory order that disagrees with physical local-header order
  fails before decoded names, metadata, exact inventory, staging, or reads.
- Every established policy through M87 retains precedence.
- The fixed 50-member producer remains unchanged and compatible.
- The error exposes no archive-controlled offset, member name, or path.
- Strict order does not establish offset bounds, gaps, adjacency, local-record
  size, payload extent, or physical non-overlap.
- Actual local-header signature and name consistency remains enforced by the
  standard reader during later bounded member reads.

## Alternatives considered

- Permit any central-directory ordering supported by ZIP. Rejected for the
  fixed sample profile because the sole producer emits one deterministic order.
- Sort the parsed members by offset. Rejected because that silently repairs an
  unexpected candidate rather than enforcing the producer contract.
- Parse local headers and central records directly. Rejected because public
  `header_offset` values suffice for this bounded aggregate rule.
- Validate gaps, ranges, adjacency, and overlap. Rejected because that requires
  a materially broader inter-member layout validator.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipFile.infolist()` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.infolist)
- [RFC-0070: require distinct local-header offsets](0070-require-distinct-local-header-offsets.md)
- [RFC-0069: require the first local-header offset at zero](0069-require-first-local-header-at-zero.md)
