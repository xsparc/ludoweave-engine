# RFC-0166: probe Windows post-admission hard-link creation

- **Status:** Accepted
- **Milestone:** M183
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe showing that M181's matching
expected-identity guardian does not freeze the file's link set. A file admitted
with one link can gain a peer hard-link entry while the guardian remains live.
Preserve this as a negative ownership boundary. Add no runtime or CI surface.

## Context

M182 proves that a preexisting hard-link alias can be renamed while the
guardian protects its exact opened pathname. It deliberately leaves
post-admission link creation unresolved.

Microsoft documents hard links as multiple same-volume directory entries for
one file. `CreateHardLinkW` creates another entry, and CreateFile sharing is
per-file. The `FILE_LINK_INFORMATION` driver contract states that creating a
hard link through that information class requires no specific file access
right. These contracts do not prove the behavior of Python's user-mode
`os.link` while this guardian's particular share mode is live, so a controlled
observation is required.

## Decision

Accept the [Windows post-admission hard-link creation
probe](../security/cache-cleanup-windows-post-admission-hard-link-creation-probe.md)
as current-host, test-only negative evidence.

Create M173's ordinary `live/coordination.lock` and a peer directory, but no
alias. Open the coordination file through the existing capability helper,
retain its `FILE_ID_INFO`, and require link count one before guardian launch.
Start M181's expected-identity guardian and require exact `ready`.

While the guardian remains live, first require rename of the exact opened
coordination pathname to fail with Windows sharing error 32. Then create
`peer/coordination.alias` with standard-library `os.link`. Require the guardian
to remain live, both handles to report the original identity, and both handles
to report link count two. Require exact bytes and exclusive byte-range
availability through both names. A second rename attempt against the protected
coordination pathname must still fail with error 32.

After the exact release token, require `closed`, then rename the coordination
entry successfully. Both remaining names must retain the original identity,
link count two, exact bytes, and complete process, stream, handle, and range
cleanup. Use no retry or sleep.

## Consequences

On the observed host, successful guardian admission does not freeze the link
set. The guardian protects the name it opened while a same-user caller can add
another directory entry for that file. A sampled identity and link count
therefore cannot become durable root-ownership authority merely because the
guardian remains live.

This compounds M182's negative boundary: a future Windows cleanup design must
define trusted-root authorization, multiple-link policy, and use-time
link-count revalidation. It must also decide what happens if the count changes
after admission and before any prospective mutation. M183 does not make that
policy decision.

This result does not prove cross-process or cross-principal creation behavior,
enumerate links, authenticate either directory, test alias deletion, cross a
volume, or establish identical behavior on ReFS, SMB, other drivers, Windows
versions, or independent hosts. It does not authorize mutation.

Windows remains unadmitted. Trusted identity/generation provenance, durable
state, root placement, link enumeration, link-count policy, simultaneous owner
loss, failed launch, file-ID reuse, hostile handles, arbitrary process trees,
mapped views, recovery, fail-closed policy, typed receipts, and
independent-host proof remain open.

No runtime API, adapter, public probe, production subprocess or `ctypes`, cache
access, cleanup authority, dependency, workflow, permission, or hosted check
is added.

## Alternatives considered

- Infer that no-delete sharing freezes the link set. Rejected because the live
  observation disproves it on the current host.
- Add native link creation to the runtime. Rejected because standard-library
  `os.link` is sufficient for this test and production cleanup is unadmitted.
- Immediately reject link count changes in runtime policy. Rejected because
  trusted root, migration, recovery, receipt, and compatibility behavior are
  not yet designed.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  will collect this source test after its prerequisite stack is integrated.

## Validation

Focused validation must prove the pre-launch one-link state, matching guardian
admission, exact-name sharing refusal, successful post-admission link creation,
guardian liveness, same identity, exact two-link growth, range availability,
persistent exact-name refusal, exact close, post-close rename, retained bytes,
and complete cleanup.

Architecture tests must preserve M182, runtime, examples, scripts,
dependencies, workflows, and the wheel package boundary. Supported-Python,
full regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [Microsoft: `CreateHardLinkW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createhardlinkw)
- [Microsoft: Hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Microsoft: `FILE_LINK_INFORMATION`](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/ns-ntifs-_file_link_information)
- [Microsoft: `BY_HANDLE_FILE_INFORMATION`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/ns-fileapi-by_handle_file_information)
- [Python: `os.link`](https://docs.python.org/3/library/os.html#os.link)
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [NIST Secure Software Development Framework publications](https://csrc.nist.gov/Projects/ssdf/publications)
- [RFC-0165](0165-probe-windows-hard-link-alias-non-exclusion.md)
