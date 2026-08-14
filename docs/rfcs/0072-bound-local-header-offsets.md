# RFC-0072: Bound local-header offsets before the central directory

- **Status:** Accepted
- **Date:** 2026-08-14
- **Decision owners:** LudoWeave maintainers

## Context

The fixed release sample producer writes 50 members whose parser-exposed
local-header offsets all fall strictly before the conventional central
directory recorded in the already-admitted final end record.

PKWARE APPNOTE 6.3.10 describes the local-header/data sequence before the
central-directory sequence and gives each central record a relative offset to
its corresponding local header. Python documents `ZipInfo.header_offset` as
the byte offset to that file header.

Supported CPython 3.12.13, 3.13.13, and 3.14.5 expose a fixture whose second
central pointer alone is changed to the conventional central-directory offset
as `[0, 94]`. Each interpreter reads the first payload and defers public
`BadZipFile` until the malformed second member is opened. The existing M88
order policy admits those strictly increasing offsets and would otherwise
begin decoded-name validation and later processing.

## Decision

Private complete release smoke checks parsed `ZipInfo` metadata after M88 and
requires every local-header offset to be strictly before the conventional
central directory from the final end record. An offset at or after that
boundary raises stable content-silent error `sample bundle local header offsets
are out of bounds`.

Complete release smoke first finishes every established policy through M88.
M89 then validates the upper bound before M77 decoded-name policy, member
metadata, exact inventory, staging, or member reads. M84 count, M85 placement,
M86 first-offset, M87 distinctness, and M88 ordering failures retain
precedence, and the existing `ExitStack` closes the source, snapshot, and
archive before an error returns.

An empty parsed inventory satisfies this aggregate rule and retains the
established later exact-inventory behavior.

## Boundary

M89 checks one upper-bound property of public parser metadata for a fixed
producer profile. It adds no local-header parser, no central-directory record
parser, no local-record extent, gap, adjacency, contiguity, or physical non-
overlap rule, and no inter-member layout validator or archive repair.

M89 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this policy is not a
general archive sandbox.

## Consequences

- A parser-exposed pointer into or beyond the conventional central directory
  fails before decoded names, metadata, exact inventory, staging, or reads.
- Every established policy through M88 retains precedence.
- The fixed 50-member producer remains unchanged and compatible.
- The error exposes no archive-controlled offset, member name, or path.
- The upper bound does not establish local-header signatures, record extents,
  gaps, adjacency, contiguity, payload bounds, or physical non-overlap.
- Standard-library member reads retain their later bounded validation role.

## Alternatives considered

- Defer every malformed pointer to member reads. Rejected because that permits
  a known producer-profile violation past aggregate metadata preflight.
- Parse local headers and central records directly. Rejected because the
  already-admitted final end record and public `header_offset` values suffice
  for this bounded rule.
- Validate record extents, adjacency, gaps, and overlap. Rejected because that
  requires a materially broader inter-member layout validator.
- Include the central-directory boundary. Rejected because that byte begins
  central metadata, not a producer-emitted local header.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo.header_offset` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo.header_offset)
- [RFC-0071: require local-header offset order](0071-require-local-header-offset-order.md)
- [RFC-0068: require exact conventional central-directory placement](0068-require-exact-central-directory-placement.md)
