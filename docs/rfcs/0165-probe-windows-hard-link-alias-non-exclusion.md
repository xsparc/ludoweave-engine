# RFC-0165: probe Windows hard-link alias non-exclusion

- **Status:** Accepted
- **Milestone:** M182
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe showing that M181's matching
expected-identity guardian protects the exact coordination pathname it opened
but does not exclude rename through a preexisting hard-link alias. Preserve the
negative result as an ownership-boundary constraint. Add no runtime or CI
surface.

## Context

M181 compares the caller's expected `FILE_ID_INFO` on the same no-delete-share
handle that protects `live/coordination.lock`. That establishes object identity
for that handle. It does not establish that the pathname is the object's only
directory entry or that every entry is confined to a trusted root.

Microsoft documents hard links as multiple same-volume directory entries for
one file. Changes to file data are visible through every entry, while entries
can have different names and parent directories. `BY_HANDLE_FILE_INFORMATION`
exposes `NumberOfLinks`; `FILE_ID_INFO` exposes file identity rather than an
enumeration or ownership proof for those entries.

The failed initial hypothesis expected M181's no-delete-share handle to reject
rename through both the opened name and a preexisting alias. The first live
probe disproved that stronger claim on this host: rename of the opened name
failed with sharing error 32, while rename of the other hard-link entry
succeeded and the guardian remained live.

## Decision

Accept the [Windows hard-link alias non-exclusion
probe](../security/cache-cleanup-windows-hard-link-alias-non-exclusion-probe.md)
as current-host, test-only negative evidence.

Create M173's ordinary `live/coordination.lock`, add
`peer/coordination.alias` with `os.link`, and use the existing capability probe
to require equal `FILE_ID_INFO` values and link counts of at least two before
guardian launch. Start M181's expected-identity guardian with the original
identity and require exact `ready`.

While the guardian remains live, require both of these distinct observations:

1. renaming the exact opened coordination pathname fails with Windows sharing
   error 32; and
2. renaming the preexisting alias to `peer/coordination.moved` succeeds.

After the alias rename, require the guardian to remain live, the moved alias to
retain the original identity and a link count of at least two, and exclusive
byte-range acquisition to remain available through both names. Require a
second rename attempt against the protected coordination pathname to fail with
error 32. This separates namespace-name protection from byte-range ownership.

After the exact release token, require `closed`, then rename the coordination
entry successfully. Both remaining names must retain the original identity,
link count, exact bytes, and complete process, stream, handle, and range
cleanup. Use no retry or sleep.

## Consequences

The M181 identity comparison establishes which file the guardian opened. It
does not establish sole-name ownership or root-confined namespace control.
Consequently, a future Windows cleanup design cannot treat an identity match
alone as proof that every hard link is known, trusted, or confined. Link-count
and trusted-root ownership policy remain mandatory design work before
admission.

This result does not show that a new hard link can be created after the
guardian opens, that aliases can cross volumes, or that the observed behavior
is identical on ReFS, network filesystems, other Windows versions, or other
drivers. It does not enumerate links, decide whether multiple links are
acceptable, authenticate parent directories, or authorize mutation.

Windows remains unadmitted. Trusted expected-identity provenance, durable
generation state, root placement, link enumeration, link-count policy,
simultaneous owner loss, failed launch, file-ID reuse, hostile handles,
arbitrary process trees, mapped views, filesystem variation, fail-closed
policy, typed receipts, and independent-host proof remain open.

No runtime API, adapter, public probe, production subprocess or `ctypes`, cache
access, cleanup authority, dependency, workflow, permission, or hosted check
is added.

## Alternatives considered

- Preserve the initial all-names protection hypothesis. Rejected because the
  first live run falsified it.
- Reject every file whose link count exceeds one in runtime code. Rejected
  because M182 does not define a trusted-root, compatibility, migration, or
  recovery policy and Windows is not admitted.
- Enumerate every hard-link path and infer ownership. Rejected because path
  enumeration, authorization, races, filesystem support, and use-time
  revalidation remain undecided.
- Add a hosted matrix allocation. Rejected because this bounded test is
  collected by the existing Windows suite after its prerequisite stack is
  integrated.

## Validation

Focused validation must prove pre-launch shared identity and link count, exact
opened-name sharing refusal, successful alias rename, guardian liveness after
that rename, persistent opened-name refusal, range availability through both
names, exact close, post-close rename, retained identity and bytes, and exact
cleanup.

Architecture tests must preserve M181, runtime, examples, scripts,
dependencies, workflows, and the wheel package boundary. Supported-Python,
full regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [Microsoft: Hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Microsoft: `CreateHardLinkW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createhardlinkw)
- [Microsoft: `BY_HANDLE_FILE_INFORMATION`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/ns-fileapi-by_handle_file_information)
- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `DeleteFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-deletefilew)
- [Microsoft: `MoveFileExW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [NIST Secure Software Development Framework publications](https://csrc.nist.gov/Projects/ssdf/publications)
- [RFC-0164](0164-probe-windows-expected-identity-guardian-admission.md)
