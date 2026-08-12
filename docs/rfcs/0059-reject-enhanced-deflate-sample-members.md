# RFC-0059: Reject enhanced-deflate sample members before extraction

- **Status:** Accepted
- **Date:** 2026-08-13
- **Milestone:** M76

## Context

M69 and M75 preflight every checksum-admitted sample member's ZIP general-
purpose flags for encryption and compressed patched data before member
metadata, inventory validation, staging, or reads. They intentionally do not
define a general flag allowlist.

The PKWARE ZIP Application Note reserves general-purpose bit 4 for enhanced
deflating when compression method 8 is used. Exact installed CPython 3.12.13,
3.13.13, and 3.14.5 `ZipFile.open` implementations do not inspect that bit.
A normally deflated member with the indicator therefore remains readable even
though its metadata requests a distinct processing mode. The fixed sample
profile admits only stored and ordinary deflated members and its producer does
not emit the indicator.

## Decision

Complete release smoke defines `_SAMPLE_ENHANCED_DEFLATE_FLAG = 0x0010` and
checks it in a separate `_validate_sample_compression_flags` call immediately
after the established processing-flag validator. A `ZipInfo` member carrying
central-directory bit 4 with compression method 8 raises the stable content-
silent policy error `sample bundle uses enhanced deflating`.

Because the existing loop checks every member before metadata and inventory
validation, a later enhanced-deflate indicator preempts an earlier member's
metadata error. The failure occurs before inventory validation, staging, or
member reads, and surrounding ownership contexts close the source, snapshot,
and archive first. M69 encryption and M75 compressed-patch errors retain their
earlier precedence.

Bit 4 on stored members remains outside this exact decision because PKWARE
assigns the indicator specifically to compression method 8. M76 deliberately
adds no broad flag allowlist, complement mask, or policy for other method/flag
combinations. The unchanged sample producer is admitted only after an
executable assertion proves it emits no enhanced-deflate indicator.

The check consumes the central-directory flags exposed by the standard reader.
M76 does not raw-parse or compare local-header flags, so local-header flag
inconsistencies remain outside this exact decision.

## Boundary

M76 is private complete-release-smoke behavior. It creates no public error
protocol, enhanced-deflate decoder, repair path, raw ZIP parser, content
scanner, malware detector, flag registry, or general archive sandbox. It does
not claim that unexamined general-purpose bits or method combinations are safe.

M76 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation.

## Consequences

- Method-8 members declaring enhanced deflating fail during all-member
  preflight.
- The error contains no archive-controlled member identity.
- Inventory validation, staging, and member reads do not begin.
- Owned source, snapshot, and archive resources close before control returns.
- Encryption and compressed-patch categories retain their error precedence.
- Stored-member bit 4, local-header inconsistencies, and unrelated flags remain
  outside this exact decision.

## Alternatives considered

- Reject bit 4 for every compression method. Rejected because the primary
  specification assigns its enhanced-deflate meaning specifically to method 8.
- Ignore bit 4 because current CPython reads ordinary deflate bytes carrying
  it. Rejected because permissive parser behavior is not evidence that the
  fixed sample profile should admit an explicitly different processing mode.
- Reject every unrecognized or reserved flag bit. Rejected because M76 has no
  evidence for a broad flag allowlist and would risk rejecting interoperable
  producer output.
- Add enhanced-deflate support or replace the standard ZIP parser. Rejected as
  unnecessary implementation and maintenance scope for a producer that does
  not emit the feature.

## References

- [PKWARE ZIP Application Note](https://www.pkware.com/documents/casestudies/APPNOTE.TXT)
- [CPython 3.12 `zipfile` implementation](https://github.com/python/cpython/blob/3.12/Lib/zipfile/__init__.py)
- [RFC-0052: reject encrypted sample members](0052-reject-encrypted-sample-members.md)
- [RFC-0058: reject compressed-patch sample members](0058-reject-compressed-patch-sample-members.md)
