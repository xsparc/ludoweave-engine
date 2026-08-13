# RFC-0064: Reject ZIP comments before extraction

- **Status:** Accepted
- **Date:** 2026-08-14
- **Milestone:** M81

## Context

The ZIP format defines a per-member file-comment field in each central-
directory header and an archive-comment field in the end-of-central-directory
record. Supported CPython versions preserve these bytes as `ZipInfo.comment`
and `ZipFile.comment`; they are not required to read the corresponding member
payload.

A standard-library fixture on installed CPython 3.12.13, 3.13.13, and 3.14.5
preserved exact archive and member comments, exposed no member extra field or
general-purpose flag, and read the deflated payload successfully. LudoWeave's
fixed sample producer emits 50 members with neither archive nor member
comments. These comment surfaces therefore provide metadata outside the fixed
release profile without supporting an intended sample-consumer behavior.

## Decision

Add private validators `_validate_sample_archive_comment` and
`_validate_sample_member_comment`. Empty bytes are the only admitted value.
A parser-exposed non-empty archive comment raises stable content-silent error
`sample bundle uses an archive comment`; a non-empty member comment raises
`sample bundle uses a member comment`. Neither error includes archive-
controlled bytes or a member name.

Complete release smoke finishes every established M69/M75/M76 flag pass, M78
descriptor policy, M79 Unicode Path policy, and M80 ZIP64 policy for all
members. It then checks `ZipFile.comment` once and `ZipInfo.comment` for every
member in a separate archive-wide pass before M77 decoded-name policy, member
metadata, exact-inventory validation, staging, or member reads. Established
categories therefore preempt comments across members; archive-comment policy
preempts member-comment policy. Existing ownership contexts close the source,
checksum-admitted snapshot, and archive before control returns.

Malformed end-record or central-directory structure remains CPython parser
policy behind the existing content-silent ZIP boundary. M81 does not scan raw
records for comment-like bytes or reinterpret a comment.

## Boundary

M81 is private complete-release-smoke behavior over comment bytes already
exposed by the standard reader. It adds no raw ZIP parser, comment decoder,
raw end-record validator, local-header comparison, rewriting, repair,
authentication, or content scanner. It adds no general comment scanner. It
makes no claim that every unrelated ZIP metadata representation is safe and is
not a general archive sandbox.

M81 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation.

## Consequences

- Every parser-exposed non-empty archive comment fails before any member comment, decoded-
  name check, metadata check, inventory validation, staging operation, or
  member read.
- Every parser-exposed non-empty member comment fails during a separate all-
  member preflight.
- Established processing, compression, descriptor, Unicode Path, and ZIP64
  categories retain archive-wide precedence.
- Both errors are stable and content-silent.
- Owned source, snapshot, and archive resources close before control returns.
- Empty comments and existing malformed-ZIP normalization remain unchanged.

## Alternatives considered

- Continue ignoring comments because they do not alter extracted payloads.
  Rejected because the fixed producer has no comment use and the extra metadata
  widens the exact private release profile.
- Reject only archive comments. Rejected because per-member comments provide
  the same unnecessary metadata surface on every central-directory entry.
- Decode or sanitize comments. Rejected because comments have no defined
  sample behavior and repair would conceal a nonconforming release artifact.
- Scan raw ZIP bytes for comment records or signature-like content. Rejected
  because the exact policy needs only the comment values already exposed by
  CPython and is not a general comment scanner.
- Reject every non-empty extra field along with comments. Rejected because
  RFC-0062 and RFC-0063 deliberately define only evidenced exact extra-field
  identities.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [CPython `zipfile` implementation](https://github.com/python/cpython/blob/main/Lib/zipfile/__init__.py)
- [RFC-0060: reject NUL-suffixed sample-member names](0060-reject-nul-suffixed-sample-member-names.md)
- [RFC-0061: reject data-descriptor sample members](0061-reject-data-descriptor-sample-members.md)
- [RFC-0062: reject Unicode Path extra fields](0062-reject-unicode-path-extra-fields.md)
- [RFC-0063: reject ZIP64 extra fields](0063-reject-zip64-extra-fields.md)
- [RFC-0050: require the exact sample-bundle inventory](0050-exact-sample-bundle-inventory.md)
- [RFC-0051: bound the sample-archive container before parsing](0051-bounded-sample-archive-container.md)
- [RFC-0053: bind sample-archive parsing and publication to its checksum](0053-bind-sample-archive-checksum.md)
- [RFC-0054: parse a checksum-admitted sample snapshot](0054-checksum-admitted-sample-snapshot.md)
- [RFC-0055: normalize sample ZIP failures content-silently](0055-content-silent-sample-zip-failures.md)
