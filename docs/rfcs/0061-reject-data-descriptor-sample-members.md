# RFC-0061: Reject data-descriptor sample members before extraction

- **Status:** Accepted
- **Date:** 2026-08-13
- **Milestone:** M78

## Context

PKWARE assigns ZIP general-purpose bit 3 to the data-descriptor representation.
When the bit is set, the local header does not carry the final CRC-32,
compressed size, and uncompressed size; those values follow the member data in
a descriptor. CPython exposes the central-directory indicator through
`ZipInfo.flag_bits` and reads this representation. Installed CPython 3.12.13,
3.13.13, and 3.14.5 each produced and read a genuine descriptor-backed member
when writing to an unseekable stream.

LudoWeave's fixed private sample producer writes a complete deterministic
archive to a seekable file and emits no bit 3. The complete-release consumer
therefore does not need this second, deferred-size representation. M69, M75,
and M76 already reject three processing/compression flag categories in an
archive-wide pass, and M77 separately checks decoded names.

## Decision

Add exact constant `_SAMPLE_DATA_DESCRIPTOR_FLAG = 0x0008` and a private
`_validate_sample_descriptor_flags` helper. Complete release smoke first checks
all members for established M69/M75/M76 flag categories. It then checks all
members for exact bit 3 in a separate pass, before the M77 name pass, member
metadata, exact-inventory validation, staging, or member reads.

A match raises stable content-silent error `sample bundle uses a data
descriptor`. Because every established flag check completes first, encryption,
compressed-patch, and enhanced-deflate errors retain archive-wide precedence
even when their member follows a descriptor-marked member. Descriptor policy
then precedes NUL-name policy. Existing ownership contexts close the source,
snapshot, and archive before control returns.

The executable producer guard proves current output contains no descriptor-
marked member. The exact flag check does not reject unrelated flag bits.

## Boundary

M78 is private complete-release-smoke behavior. It adds no raw descriptor
parser, no broad flag allowlist, central-directory/local-header comparison,
authentication, decoder, rewriting, repair, or content scanner. It makes no
claim that unrelated or unexamined ZIP flag combinations are safe and is not a
general archive sandbox.

M78 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation.

## Consequences

- Every descriptor-marked member fails during archive-wide preflight.
- The error includes no archive-controlled identity or payload.
- Established processing/compression flag errors retain precedence.
- Descriptor policy precedes NUL-name and metadata policy.
- Inventory validation, staging, and member reads do not begin.
- Owned source, snapshot, and archive resources close before control returns.
- Unrelated flags and raw descriptor structure remain outside this decision.

## Alternatives considered

- Accept data descriptors because CPython can read them. Rejected because the
  fixed producer has no need for deferred sizes and the extra representation
  broadens the private release-consumer input boundary.
- Parse and validate raw descriptors. Rejected because it adds a second ZIP
  parser and metadata-consistency policy without an admitted producer need.
- Define a broad allowed-bit mask. Rejected because unexamined flag semantics
  require separate evidence and exact decisions.
- Rewrite descriptor-backed members into the fixed representation. Rejected
  because consumer-side repair would conceal an invalid release artifact.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [CPython `zipfile` implementation](https://github.com/python/cpython/blob/main/Lib/zipfile/__init__.py)
- [RFC-0052: reject encrypted sample members](0052-reject-encrypted-sample-members.md)
- [RFC-0058: reject compressed-patch sample members](0058-reject-compressed-patch-sample-members.md)
- [RFC-0059: reject enhanced-deflate sample members](0059-reject-enhanced-deflate-sample-members.md)
- [RFC-0060: reject NUL-suffixed sample-member names](0060-reject-nul-suffixed-sample-member-names.md)
