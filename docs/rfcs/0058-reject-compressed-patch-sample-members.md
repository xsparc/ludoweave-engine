# RFC-0058: Reject compressed-patch sample members before extraction

- **Status:** Accepted
- **Date:** 2026-08-13
- **Milestone:** M75

## Context

M69 preflights every checksum-admitted sample member's ZIP general-purpose
flags for encryption before member metadata, inventory validation, staging, or
reads. It intentionally does not define a general flag allowlist.

The PKWARE ZIP Application Note assigns general-purpose bit 5 to compressed
patched data. Exact installed CPython 3.12.13, 3.13.13, and 3.14.5
`ZipFile.open` implementations reject that bit with `NotImplementedError`
containing the feature and flag identity. Before M75, a matching-checksum ZIP
with the exact expected inventory could pass all-member flag preflight and
reach inventory and staging before that unsupported processing request failed
at member open.

## Decision

Complete release smoke defines `_SAMPLE_COMPRESSED_PATCH_FLAG = 0x0020` and
checks it in `_validate_sample_member_flags` immediately after the established
encryption check. Any member carrying bit 5 raises the stable content-silent
policy error `sample bundle uses compressed patched data`.

Because the existing loop checks every member before metadata and inventory
validation, a later compressed-patch indicator preempts an earlier member's
metadata error. The failure occurs before inventory validation, staging, or
member reads, and the surrounding ownership contexts close the source,
snapshot, and archive first. When encryption and compressed-patch indicators
coexist, M69's encryption error retains precedence.

Other general-purpose bits remain outside this decision. M75 deliberately adds
no broad flag allowlist, complement mask, or reserved-bit policy. The unchanged
sample producer is admitted only after an executable assertion proves it emits
no compressed-patch indicator.

## Boundary

M75 is private complete-release-smoke behavior. It creates no public error
protocol, patch decoder, repair path, raw ZIP parser, content scanner, malware
detector, flag registry, or general archive sandbox. It does not claim that
unexamined general-purpose bits are safe.

M75 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation.

## Consequences

- Compressed patched data fails during all-member preflight.
- The error contains no archive-controlled member identity.
- Inventory validation, staging, and member reads do not begin.
- Owned source, snapshot, and archive resources close before control returns.
- Encryption retains its existing error precedence.
- Unrelated general-purpose flags remain outside this exact decision.

## Alternatives considered

- Catch `NotImplementedError` at the outer ZIP boundary. Rejected because the
  exact unsupported feature is visible in central-directory metadata and can
  fail earlier without catching unrelated implementation failures.
- Reject every unrecognized or reserved flag bit. Rejected because M75 has no
  evidence for a broad flag allowlist and would risk rejecting interoperable
  producer output.
- Add compressed-patch support. Rejected because the deterministic sample
  producer does not emit it and a patch decoder would add unnecessary scope.
- Replace the standard ZIP parser. Rejected as a materially larger security
  and maintenance surface.

## References

- [PKWARE ZIP Application Note](https://www.pkware.com/documents/casestudies/APPNOTE.TXT)
- [CPython 3.12 `zipfile` implementation](https://github.com/python/cpython/blob/3.12/Lib/zipfile/__init__.py)
- [RFC-0047: bound sample-bundle extraction](0047-bounded-sample-bundle-extraction.md)
- [RFC-0052: reject encrypted sample members](0052-reject-encrypted-sample-members.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
