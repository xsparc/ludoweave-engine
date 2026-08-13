# RFC-0062: Reject Unicode Path extra fields before extraction

- **Status:** Accepted
- **Date:** 2026-08-13
- **Milestone:** M79

## Context

Info-ZIP extra-field ID `0x7075` stores a UTF-8 Unicode Path corresponding to
the legacy ZIP filename. Supported CPython versions walk the central-directory
extra fields and, when the field version and legacy-name CRC are valid, replace
`ZipInfo.filename` with that UTF-8 path. `ZipInfo.orig_filename` continues to
hold the decoded legacy name used to construct the object.

Installed CPython 3.12.13, 3.13.13, and 3.14.5 each read one genuine archive
whose legacy name was `ludoweave-samples-0.1.0a1/legacy.txt`, exposed
`ludoweave-samples-0.1.0a1/README.md` from `0x7075` as `filename`, retained the
legacy `orig_filename`, and returned the payload. LudoWeave's fixed private
sample producer emits 50 members with no extra fields, so it does not need this
alternate-name representation.

## Decision

Add exact constant `_SAMPLE_UNICODE_PATH_EXTRA_FIELD = 0x7075` and a private
`_validate_sample_extra_fields` helper. The helper performs a bounded extra-
field walk over the central-directory bytes already exposed by `ZipInfo.extra`
and rejects only the exact extra-field ID. A match raises stable content-silent
error `sample bundle uses a Unicode Path extra field`.

Complete release smoke finishes the established M69/M75/M76 flag pass and M78
descriptor pass for every member, then checks every member's extra fields in a
separate archive-wide pass. M77 decoded-name checks, member metadata, exact-
inventory validation, staging, and member reads begin only afterward. A later
established flag or descriptor error therefore preempts an earlier Unicode
Path field; Unicode Path policy preempts NUL-name policy. Existing ownership
contexts close the source, snapshot, and archive before control returns.

Malformed extra-field structure remains CPython parser policy. The private
helper does not create new errors for an incomplete trailing header or an
unrelated field whose data contains the `0x7075` byte sequence.

## Boundary

M79 is private complete-release-smoke behavior. It is an exact extra-field ID
check and no broad extra-field ban. It adds no general original-versus-
normalized name comparison, raw ZIP header parser, arbitrary extra-field
validator, local-header/central-directory comparison, authentication,
rewriting, repair, or content scanner. It makes no claim that every unrelated
extra field or alternate representation is safe and is not a general archive
sandbox.

M79 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation.

## Consequences

- Every central-directory Unicode Path field fails during all-member preflight.
- The error includes neither the legacy nor replacement archive-controlled
  name.
- Established processing, compression, and descriptor categories retain
  archive-wide precedence.
- Unicode Path policy precedes decoded-name and metadata policy.
- Inventory validation, staging, and member reads do not begin.
- Owned source, snapshot, and archive resources close before control returns.
- Unrelated fields and malformed-extra handling remain outside this decision.

## Alternatives considered

- Continue accepting `0x7075` because the substituted path receives normal
  path and inventory checks. Rejected because the fixed producer has no need
  for two independently encoded names and the alternate representation widens
  the private release-consumer boundary.
- Reject every non-empty extra field. Rejected as a broad extra-field ban that
  would define policy for unrelated standard extensions without evidence.
- Compare `filename` with `orig_filename`. Rejected because that is a broad
  normalization policy and can conflate platform separator normalization with
  the exact observed field.
- Search raw bytes for `0x7075`. Rejected because an unrelated field's data may
  contain that byte sequence; field boundaries must be honored.
- Rewrite or discard the alternate name. Rejected because consumer-side repair
  would conceal an invalid release artifact.

## References

- [PKWARE APPNOTE.TXT](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [CPython `zipfile` implementation](https://github.com/python/cpython/blob/main/Lib/zipfile/__init__.py)
- [RFC-0060: reject NUL-suffixed sample-member names](0060-reject-nul-suffixed-sample-member-names.md)
- [RFC-0061: reject data-descriptor sample members](0061-reject-data-descriptor-sample-members.md)
