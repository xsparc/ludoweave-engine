# RFC-0063: Reject ZIP64 extra fields before extraction

- **Status:** Accepted
- **Date:** 2026-08-14
- **Milestone:** M80

## Context

PKWARE extra-field ID `0x0001` is the ZIP64 extended-information field. Its
central-directory form can provide alternate 64-bit uncompressed size,
compressed size, local-header offset, and a 32-bit disk-start value when the
corresponding ordinary fields contain sentinel values. Supported CPython
versions apply those values while constructing `ZipInfo`, before LudoWeave's
private complete-release consumer receives the member records.

A genuine central-directory fixture on installed CPython 3.12.13, 3.13.13,
and 3.14.5 exposed the same 13-byte payload with ZIP64 size and offset values,
retained the 28-byte `0x0001` extra field, and read the payload successfully.
LudoWeave's fixed small sample producer emits 50 members with no extra fields,
so it has no need for this alternate metadata representation.

## Decision

Add exact constant `_SAMPLE_ZIP64_EXTRA_FIELD = 0x0001` and private helper
`_validate_sample_zip64_extra_fields`. The helper performs a bounded extra-
field walk over central-directory bytes already exposed by `ZipInfo.extra`
and rejects only the exact extra-field ID. A match raises stable content-
silent error `sample bundle uses a ZIP64 extra field`.

Complete release smoke finishes every established M69/M75/M76 flag pass, the
M78 descriptor pass, and the M79 Unicode Path pass for all members. It then
checks every member for ZIP64 in a separate archive-wide pass before M77
decoded-name policy, member metadata, exact-inventory validation, staging, or
member reads. A later established flag, descriptor, or Unicode Path error
therefore preempts an earlier ZIP64 field. Existing ownership contexts close
the source, snapshot, and archive before control returns.

Malformed extra-field structure remains CPython parser policy. The private
helper does not create a new error for an incomplete trailing header or an
unrelated field whose data contains the `0x0001` byte sequence.

## Boundary

M80 is private complete-release-smoke behavior and an exact extra-field ID
check. It adds no broad extra-field ban, raw ZIP64 parser, ZIP64 end-record or
locator validation, arbitrary extra-field validator, large-file support,
local-header/central-directory comparison, rewriting, repair, authentication,
or content scanner. It makes no claim that every unrelated extra field or
alternate archive representation is safe and is not a general archive
sandbox.

In exact boundary terms, M80 adds no raw ZIP64 parser and no workflow change.
The preflight completes before member reads and before staging.

M80 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation.

## Consequences

- Every central-directory ZIP64 extended-information field fails during all-
  member preflight.
- The error contains no archive-controlled field data or member name.
- Established processing, compression, descriptor, and Unicode Path
  categories retain archive-wide precedence.
- ZIP64 policy precedes decoded-name and metadata policy.
- Inventory validation, staging, and member reads do not begin.
- Owned source, snapshot, and archive resources close before control returns.
- Unrelated fields and malformed-extra handling remain outside this decision.

## Alternatives considered

- Continue accepting `0x0001` because CPython resolves its values. Rejected
  because the fixed producer has no need for two size/offset representations
  and the alternate representation widens the private consumer boundary.
- Reject every non-empty extra field. Rejected as a broad extra-field ban that
  would define policy for unrelated standard extensions without evidence.
- Parse raw local and central ZIP64 records. Rejected because no raw ZIP64
  parser or general archive validator is needed for this exact policy.
- Reject only when a decoded size differs from the ordinary field. Rejected
  because sentinel substitution has already happened before preflight and a
  comparison would broaden the contract beyond the observed field identity.
- Rewrite or strip ZIP64 metadata. Rejected because consumer-side repair would
  conceal an invalid release artifact.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [CPython `zipfile` implementation](https://github.com/python/cpython/blob/main/Lib/zipfile/__init__.py)
- [RFC-0060: reject NUL-suffixed sample-member names](0060-reject-nul-suffixed-sample-member-names.md)
- [RFC-0061: reject data-descriptor sample members](0061-reject-data-descriptor-sample-members.md)
- [RFC-0062: reject Unicode Path extra fields](0062-reject-unicode-path-extra-fields.md)
- [RFC-0050: require the exact sample-bundle inventory](0050-exact-sample-bundle-inventory.md)
- [RFC-0051: bound the sample-archive container before parsing](0051-bounded-sample-archive-container.md)
- [RFC-0052: reject encrypted sample members before extraction](0052-reject-encrypted-sample-members.md)
- [RFC-0053: bind sample-archive parsing and publication to its checksum](0053-bind-sample-archive-checksum.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
- [RFC-0055: normalize sample ZIP failures content-silently](0055-content-silent-sample-zip-failures.md)
- [RFC-0056: normalize sample ZIP text failures content-silently](0056-content-silent-sample-zip-text-failures.md)
- [RFC-0057: normalize sample ZIP decompression failures content-silently](0057-content-silent-sample-zip-decompression-failures.md)
- [RFC-0058: reject compressed-patch sample members](0058-reject-compressed-patch-sample-members.md)
- [RFC-0059: reject enhanced-deflate sample members](0059-reject-enhanced-deflate-sample-members.md)
