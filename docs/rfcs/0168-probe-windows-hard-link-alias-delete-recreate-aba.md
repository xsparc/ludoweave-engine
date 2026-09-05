# RFC-0168: probe Windows hard-link alias delete/recreate ABA

- **Status:** Accepted
- **Milestone:** M185
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe showing that a peer hard-link name
can be deleted and recreated while M181's matching expected-identity guardian
remains live. The file's observed link count changes from two to one and back
to two without changing `FILE_ID_INFO`, bytes, guardian liveness, or the
guardian's exact-name rename refusal. Preserve this as a pathname-membership
ABA boundary. Add no runtime or CI surface.

Also correct the process classification carried into M184: the mutation actor
is the parent process and the guardian is a child process. The evidence is
cross-process under one principal, not single-process and not cross-principal.

## Context

M183 shows that a peer hard link can be added after guardian admission. M184
shows that a preexisting peer hard link can be removed while the guardian
remains live. Neither probe combines those operations at the same pathname or
observes the resulting `2 -> 1 -> 2` transition during one guardian lifetime.

Microsoft documents hard links as multiple directory entries for one file,
permits link deletion in any creation order, and applies CreateFile access and
sharing per file. Those contracts support treating link membership as live
namespace state, but they do not prove the exact delete/recreate interleaving
used by this guardian on the current host.

## Decision

Accept the [Windows hard-link alias delete/recreate ABA
probe](../security/cache-cleanup-windows-hard-link-alias-delete-recreate-aba-probe.md)
as current-host, test-only negative evidence.

Create M173's ordinary coordination file and a peer alias before guardian
launch. Open both through the existing capability helper, retain their shared
`FILE_ID_INFO`, require link count two through both names, and close those
initial handles. Start M181's matching guardian child and require exact
`ready` while the parent remains the mutation actor.

While the guardian remains live, reopen the original and first require rename
of the exact coordination pathname to fail with Windows sharing error 32.
Delete the peer alias, require its absence, guardian liveness, unchanged
identity and bytes, and link count one. Then recreate the same alias pathname
with standard-library `os.link`. Reopen it, require both handles to retain the
original identity and report link count two, require exact bytes and exclusive
byte-range availability through both names, and require a second exact-name
rename failure with error 32.

After the exact release token, require `closed`. Rename the original entry
successfully, reopen the displaced name and peer alias, and require the same
identity, link count two, exact bytes, and complete process, stream, native-
handle, and range cleanup. Use no retry or sleep.

## Consequences

On the observed host, a matching guardian does not freeze alias-path
membership. The same peer pathname can move from present to absent to present
while the guardian remains live, the guarded object's identity and bytes stay
constant, and exact-name rename remains excluded. An observed link count of
one is therefore a transient sample, not durable root-confined ownership.

This result supplies a two-process, same-principal observation: the parent
deletes and recreates the link while the child guardian holds the protecting
handle. It supersedes M184's single-process wording and the narrower statement
that another process was untested. It does not establish cross-principal
behavior, an independent third mutation actor, controlled concurrent racing,
or behavior across unrelated process trees.

A future Windows cleanup design must define trusted-root authorization,
multiple-link history and policy, use-time identity and link-count
revalidation, and a fail-closed receipt when namespace membership changes.
M185 does not make that policy decision and does not authorize mutation.

Windows remains unadmitted. Link enumeration, authenticated parent
directories, POSIX-delete flags, cross-volume behavior, ReFS, SMB, other
drivers or Windows versions, file-ID reuse, durable generation provenance,
failed launch, simultaneous owner loss, hostile handles, mapped views,
recovery, typed receipts, and independent-host proof remain open.

No runtime API, adapter, public probe, production subprocess or `ctypes`, cache
access, cleanup authority, dependency, workflow, permission, or hosted check
is added.

## Alternatives considered

- Treat M183 and M184 as sufficient without combining them. Rejected because
  neither records restoration of the same alias pathname during one guardian
  lifetime.
- Admit a one-link sample as a cleanup precondition. Rejected because the live
  ABA observation shows that sample can immediately become stale.
- Add native link operations to the runtime. Rejected because standard-library
  `os.link` and `Path.unlink` are sufficient for the test and cleanup remains
  unadmitted.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  will collect this source test after its prerequisite stack is integrated.

## Validation

Focused validation must prove the initial shared identity and two-link state,
guardian admission, exact-name sharing refusal, alias deletion, exact one-link
state, same-path recreation, exact two-link restoration, guardian liveness,
retained bytes, range availability, persistent exact-name refusal, exact
close, post-close rename, retained identity, and complete cleanup.

Architecture tests must preserve M184, runtime, examples, scripts,
dependencies, workflows, and the wheel package boundary. Supported-Python,
full regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `CreateHardLinkW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createhardlinkw)
- [Microsoft: `DeleteFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-deletefilew)
- [Microsoft: Hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Python: `os.link`](https://docs.python.org/3/library/os.html#os.link)
- [Python: `os.remove` and `os.unlink`](https://docs.python.org/3/library/os.html#os.remove)
- [GitHub Actions matrix jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [NIST Secure Software Development Framework publications](https://csrc.nist.gov/Projects/ssdf/publications)
- [RFC-0167](0167-probe-windows-hard-link-alias-deletion-non-exclusion.md)
