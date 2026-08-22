# RFC-0080: Require consistent local-header extraction versions

- **Status:** Accepted
- **Date:** 2026-08-23
- **Decision owners:** LudoWeave maintainers

## Context

M96 proves exact equality between each bounded local extra field and public
central `ZipInfo.extra`. It intentionally does not compare the adjacent
two-byte "version needed to extract" values in corresponding local and central
member records.

PKWARE APPNOTE 6.3.10 sections 4.3.7 and 4.3.12 define the two bytes in both
records: one extraction-version byte and one reserved byte. Python
exposes the central pair as public `ZipInfo.extract_version` and
`ZipInfo.reserved`, and exposes the local-header location as
`ZipInfo.header_offset`. CPython reads the local fixed header during member
open but does not compare its local pair with those central values.

On exact CPython 3.12.13, 3.13.13, and 3.14.5, changing only the second member's
local extraction-version byte from 20 to 21 leaves both central pairs at
`(20, 0)`, preserves offsets `[0, 54]`, and permits both payloads to be read.
This decision relies only on that observed admission gap, public attributes,
and documented record structure.

## Decision

After M96 local-extra consistency, private complete release smoke reads exactly
two bytes at `ZipInfo.header_offset + 4`. Those local bytes must equal
`bytes((info.extract_version, info.reserved))` for the corresponding central
record. A mismatch raises a stable, content-silent error.

- Stable error: `sample bundle local header extraction versions are inconsistent`.

This one two-byte local-extraction-version consistency classifier runs before
decoded-name policy, member metadata, exact inventory, staging, or member
reads. Every established policy through M96 retains precedence. M91 already
bounds the complete fixed local-header prefix, the helper restores the caller's
snapshot position, and the existing `ExitStack` closes the source, snapshot,
and archive before an error returns. An empty parsed inventory satisfies this
aggregate rule and retains the later exact-inventory behavior.

## Boundary

M97 defines equality only. It adds no supported-version allowlist, minimum
extractor-capability rule, reserved-byte policy, or interpretation of the two
bytes. Exact equality is a fixed-producer profile, not a claim that every valid
ZIP producer must use these central values.

M97 performs no time/CRC/size comparison, field-wide local/central comparison,
complete local-record or payload bound, next-header bound, gap, adjacency,
contiguity, physical non-overlap rule, or inter-member layout validator, and no
archive repair. It adds no workflow, runner allocation, action, permission,
credential, dependency, lock, version, runtime package/API, sample producer,
release mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this fixed-producer
policy is not a general archive sandbox.

## Consequences

- Any local/central extraction-version or reserved-byte mismatch
  fails before decoded names, metadata, exact inventory, staging, or reads.
- Every established policy through M96 retains precedence.
- Equal values remain admitted regardless of their semantic support; later
  standard-library operations retain responsibility for actual extraction
  capability.
- The fixed 50-member producer remains unchanged with matching `(20, 0)`
  local and central pairs.
- The error exposes no archive-controlled name, byte value, offset, or member
  position.
- Standard-library member reads retain responsibility for payload extents,
  overlap checks, decompression, and CRC validation.

## Alternatives considered

- Add a supported-version allowlist. Rejected because M97 addresses duplicate-
  field consistency, not a new extractor-capability policy.
- Validate only the low extraction-version byte. Rejected because PKWARE and
  Python expose the full corresponding two-byte pair.
- Defer local-only changes to member reads. Rejected because every supported
  Python version ignores the demonstrated mutation.
- Compare time, CRC, sizes, or every remaining fixed field. Rejected because
  each needs separate policy, including data-descriptor and ZIP64 interactions.
- Bound payloads, next headers, gaps, adjacency, or overlap. Rejected because
  those require broader record parsing and inter-member layout policy.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0079: require consistent local-header extra fields](0079-require-consistent-local-header-extra-fields.md)
- [RFC-0074: bound local-header prefixes](0074-bound-local-header-prefixes.md)
