# RFC-0065: Reject split-volume sample members before extraction

- **Status:** Accepted
- **Date:** 2026-08-14
- **Decision owners:** LudoWeave maintainers

## Context

The fixed release sample bundle is one small regular ZIP file. Its producer
emits 50 central-directory entries whose disk-number-start field is zero.
There is no product need for a member whose local header begins on another
archive volume.

PKWARE APPNOTE section 4.4.13 defines the two-byte central-directory disk
number start as the disk on which a file begins. CPython assigns that parsed
value to `ZipInfo.volume`. Supported CPython 3.12.13, 3.13.13, and 3.14.5 each
expose a patched value of one while still reading the same deflated payload
from the single supplied file; the probe has no extra field or general-purpose
flag. The value therefore widens the admitted release profile without helping
the fixed producer.

## Decision

Private complete release smoke rejects every parser-exposed nonzero
`ZipInfo.volume` with the stable content-silent error
`sample bundle uses a split-volume member`.

Complete release smoke first finishes every established M69/M75/M76 flag pass,
M78 descriptor policy, M79 Unicode Path policy, M80 ZIP64 policy, and both M81
comment passes. It then checks `ZipInfo.volume` for every member in a separate
archive-wide pass before M77 decoded-name policy, member metadata, exact
inventory validation, staging, or member reads. A ZIP64 extra field therefore
retains precedence over its `0xFFFF` disk-start sentinel, and archive/member
comments retain their established precedence over split-volume policy.

The existing `ExitStack` closes the source, checksum-admitted snapshot, and
archive before the error returns. No member is opened and no staging directory
or final sample root is created.

## Boundary

M82 inspects only the central-directory disk-start value already exposed by
the standard reader. It adds no raw end-record parser, no local-header parser,
and no multi-volume assembler. It does not inspect end-of-central-directory
disk numbers, find or join other archive volumes, rewrite member placement, or
claim general split/spanned-archive validation.

M82 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation, and this policy is not a
general archive sandbox.

## Consequences

- Every nonzero parser-exposed member volume fails before decoded-name policy,
  metadata, inventory, staging, or reads.
- Established flag, descriptor, exact extra-field, and comment categories
  retain archive-wide precedence.
- Volume zero remains admitted; the fixed producer remains unchanged.
- The error exposes neither member names nor archive-controlled values.
- Owned source, snapshot, and archive resources close before control returns.
- Raw end-record disk fields and multi-volume assembly remain deferred.

## Alternatives considered

- Continue ignoring `ZipInfo.volume` because CPython can read the patched
  single-file fixture. Rejected because a nonzero value claims a placement the
  fixed producer never emits and the consumer does not support.
- Reject only `0xFFFF`. Rejected because every nonzero disk start is outside
  the single-volume sample profile; M80 already handles an actual ZIP64 extra
  field earlier.
- Parse end-of-central-directory disk numbers too. Rejected because the exact
  evidenced gap is already exposed through `ZipInfo.volume`; raw record parsing
  would materially broaden this slice.
- Search for and combine neighboring volume files. Rejected because it would
  add filesystem discovery, ambiguous ownership, and unsupported multi-volume
  semantics.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [CPython `zipfile` implementation](https://github.com/python/cpython/blob/main/Lib/zipfile/__init__.py)
- [RFC-0064: reject ZIP comments](0064-reject-zip-comments.md)
- [RFC-0063: reject ZIP64 extra fields](0063-reject-zip64-extra-fields.md)
- [RFC-0060: reject NUL-suffixed sample-member names](0060-reject-nul-suffixed-sample-member-names.md)
- [RFC-0050: require the exact sample-bundle inventory](0050-exact-sample-bundle-inventory.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
