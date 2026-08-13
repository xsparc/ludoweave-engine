# RFC-0060: Reject NUL-suffixed sample-member names before extraction

- **Status:** Accepted
- **Date:** 2026-08-13
- **Milestone:** M77

## Context

M65 validates portable paths and M67 requires the exact sample inventory using
the normalized name exposed by `ZipInfo.filename`. M69, M75, and M76 separately
preflight unsupported member-processing flags before metadata, inventory,
staging, or reads.

Supported CPython versions preserve the complete decoded central-directory
name in `ZipInfo.orig_filename`, then sanitize `ZipInfo.filename` by truncating
at the first NUL byte. Python's `zipfile` documentation also states that an
archive name containing a null byte is truncated there. Installed CPython
3.12.13, 3.13.13, and 3.14.5 each read a member whose original name is
`root/README.md\0hidden`, expose the visible name as `root/README.md`, and
return its payload. Before M77, that hidden suffix was not validated even when
the visible name satisfied the exact inventory.

## Decision

Complete release smoke first checks the established processing/compression
flags for every member, then calls a private `_validate_sample_member_name` for
every member in a separate archive-wide pass. The validator performs one exact
NUL check on decoded `ZipInfo.orig_filename`. A match raises the stable
content-silent policy error `sample bundle member name contains a NUL byte`.

Because the check remains in the all-member preflight, a later NUL-suffixed
member preempts an earlier member's metadata error. Failure occurs before
metadata or exact-inventory validation, staging, or member reads. Surrounding
ownership contexts close the source, snapshot, and archive before control
returns. Because all flag checks complete before name checks begin, M69
encryption, M75 compressed-patch, and M76 enhanced-deflate errors retain their
existing precedence even when the flagged member follows the NUL-suffixed
member.

M77 deliberately does not reject every difference between `orig_filename` and
`filename`. The standard reader can normalize platform separators and may
replace a legacy name from an admitted Unicode Path extra field; those cases
require separate evidence and decisions. The unchanged sample producer is
admitted only after an executable assertion proves it emits no NUL-suffixed
name.

## Boundary

M77 is private complete-release-smoke behavior. It is an exact NUL check, with
no general normalized-name comparison and no raw parser. It does not compare
central-directory and local-header bytes, authenticate metadata, rewrite or
repair names, scan content, or create a general archive sandbox. It makes no
claim that every other original/normalized-name difference is safe.

M77 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation.

## Consequences

- Decoded original member names containing NUL fail during all-member
  preflight.
- The error contains no archive-controlled member identity or hidden suffix.
- Member metadata, inventory validation, staging, and member reads do not
  begin.
- Owned source, snapshot, and archive resources close before control returns.
- Established processing-flag categories retain error precedence.
- Other original-versus-normalized name differences and raw-header
  inconsistencies remain outside this exact decision.

## Alternatives considered

- Continue validating only `ZipInfo.filename`. Rejected because the standard
  reader intentionally hides the NUL suffix while retaining it in an already
  available decoded field.
- Reject every difference between `orig_filename` and `filename`. Rejected
  because it would silently define policy for unrelated standard-library name
  normalization without evidence.
- Raw-parse and compare central-directory and local-header names. Rejected as a
  materially larger parser and metadata-consistency boundary than the observed
  defect requires.
- Rewrite the name or discard the suffix. Rejected because the fixed sample
  producer emits canonical names and consumer-side repair would conceal an
  invalid release artifact.

## References

- [Python 3.14 `zipfile` documentation](https://docs.python.org/3.14/library/zipfile.html)
- [CPython `zipfile` implementation](https://github.com/python/cpython/blob/main/Lib/zipfile/__init__.py)
- [RFC-0048: constrain sample member paths](0048-portable-sample-member-paths.md)
- [RFC-0050: require the exact sample inventory](0050-exact-sample-bundle-inventory.md)
- [RFC-0059: reject enhanced-deflate sample members](0059-reject-enhanced-deflate-sample-members.md)
