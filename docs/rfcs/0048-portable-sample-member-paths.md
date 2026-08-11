# RFC-0048: Constrain sample-bundle member paths portably

- **Status:** Accepted
- **Date:** 2026-08-12
- **Owners:** LudoWeave maintainers
- **Milestone:** M65

## Context

M64 bounds the count, declared expansion, compression methods, and streamed
copy size of the staged sample ZIP before extraction. Its path check confines
members beneath the expected bundle root and rejects traversal, backslashes,
and symbolic links, but it intentionally deferred filename portability.

A ZIP central directory can contain the same path more than once, paths that
differ only by ASCII case, different spellings of one case-insensitive
directory, or one file path that is an ancestor of another file. Those inputs
do not have one extraction identity across supported Windows, macOS, and Linux
filesystems. A member can also use a classic Windows device stem, a trailing
period, Unicode, an empty or dot component, or an overlong spelling. Depending
on the host, extraction can overwrite an earlier file, merge directories, fail
after earlier writes, or interpret a spelling differently.

The sample producer is project-owned and already emits regular files beneath
one expected root with portable ASCII components. The verifier can therefore
admit a narrow deterministic subset without rewriting names or probing the
runner filesystem.

## Decision

Before extraction creates any path, every sample member must be a regular file
whose path has the exact expected root followed by one or more portable sample
member components. Explicit directory entries are rejected because directories
are derived from admitted file ancestors. When ZIP Unix mode type bits are
present, they must identify a regular file; explicit FIFO, socket, device,
directory, and symbolic-link types are rejected. Missing type bits remain
admitted because common ZIP producers encode permissions without a file type.

A portable sample member path has at most **255 ASCII characters** after the
root, including `/` separators. Every component:

- is 1 through 255 ASCII characters;
- begins with an ASCII alphanumeric character;
- otherwise contains only ASCII alphanumerics, period, underscore, plus, or
  hyphen;
- does not end with a trailing period; and
- has no case-insensitive first period-delimited stem equal to the Windows
  device names `CON`, `PRN`, `AUX`, `NUL`, `COM1` through `COM9`, or `LPT1`
  through `LPT9`.

The complete preflight also requires:

1. no duplicate complete path under ASCII case-insensitive comparison;
2. one exact spelling for each case-insensitive directory ancestor; and
3. no case-insensitive file/directory prefix collision.

Any violation fails with a stable content-silent category before extraction.
The already-admitted `ZipInfo` objects and validated component tuples are then
paired for M64's bounded streaming pass; paths are not normalized or rewritten.

## Boundary

M65 is a private release-smoke policy for the project-owned staged sample
bundle. It is not a general ZIP path validator, archive sandbox, filesystem
portability guarantee, or validation of every platform-reserved spelling. It
performs no Unicode normalization, locale-sensitive comparison, filesystem
probing, case-preservation inference, path resolution, or race isolation.

The 255-character relative-path cap does not guarantee that an arbitrary
checkout plus temporary-directory prefix remains below every host-specific
absolute-path limit. ZIP metadata remains protected by the existing release
checksum and manifest boundary, not authenticated by this lexical policy.
M64's lack of transactional cleanup after a successful preflight also remains.

M65 adds no workflow, runner allocation, action, permission, trigger,
credential, dependency, lock, version, runtime package/API, sample producer,
release mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation.

## Consequences

- Duplicate, case-insensitive, directory-spelling, and prefix collision paths
  fail before extraction writes any member.
- Explicit non-regular ZIP mode types fail before extraction; omitted type bits
  remain compatible with common producers.
- Windows device stems, trailing periods, non-ASCII components, empty/dot
  components, explicit directory entries, and overlong paths fail preflight.
- Existing project-produced nested sample members retain their exact spellings
  and remain admitted.
- The policy is deterministic across supported Python versions and operating
  systems and does not depend on host filesystem behavior.

## Alternatives considered

- Depend on each host filesystem to reject or merge conflicting paths.
  Rejected because failure ordering and extracted identity would vary by host
  and could occur after earlier writes.
- Reject only exact duplicate ZIP names. Rejected because case-only and prefix
  collisions remain ambiguous on supported filesystems.
- Normalize Unicode or case before extraction. Rejected because sample member
  names are exact staged identities and must never be silently rewritten.
- Permit explicit directory entries and validate them separately. Rejected
  because the project producer emits only files and extraction can derive all
  required directories from admitted file ancestors.
- Reuse a host-specific reserved-name API. Rejected because M65 requires one
  version-stable lexical policy rather than filesystem probing.

## References

- [RFC-0047: bound sample-bundle extraction](0047-bounded-sample-bundle-extraction.md)
- [RFC-0045: constrain public release asset names portably](0045-portable-public-release-asset-names.md)
- [Microsoft: Naming Files, Paths, and Namespaces](https://learn.microsoft.com/windows/win32/fileio/naming-a-file)
- [Python 3.14 `zipfile` documentation](https://docs.python.org/3/library/zipfile.html)
