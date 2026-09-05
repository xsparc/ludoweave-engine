# RFC-0169: probe Windows independent hard-link alias mutator ABA

- **Status:** Accepted
- **Milestone:** M186
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that moves M185's peer-alias
delete/recreate actor out of the parent coordinator and into a separate child
process. While M181's matching expected-identity guardian child remains live,
the sibling mutator child deletes the alias, waits for an exact token, recreates
the same alias pathname, waits again, and closes exactly. Preserve the observed
`2 -> 1 -> 2` pathname-membership ABA as a three-process, same-principal
boundary. Add no runtime or CI surface.

## Context

M185 records the ABA transition with the parent process performing both
namespace mutations and one guardian child retaining the protecting handle.
That proves cross-process protection does not freeze alias membership, but it
does not show the same result when a separate process owns the mutation calls.

Microsoft documents hard links as multiple directory entries for one file,
permits their deletion in any creation order, and applies CreateFile access and
sharing per file across process contexts. Python documents bounded binary pipes,
argument sequences, `sys.executable`, `shell=False`, and `close_fds=True` for a
controlled child. Those contracts support a focused probe but do not prove this
exact three-process interleaving on the current host.

## Decision

Accept the [Windows independent hard-link alias mutator ABA
probe](../security/cache-cleanup-windows-independent-hard-link-alias-mutator-aba-probe.md)
as current-host, test-only negative evidence.

Create M173's ordinary coordination file and peer alias, retain their matching
`FILE_ID_INFO`, require link count two, and close the initial handles. Start
M181's guardian child with that exact identity and require `ready`. Reopen the
original and require exact-name rename to fail with Windows sharing error 32.

Then start a distinct mutator child from a fixed repository fixture with no
arguments, shell, environment controls, network access, or inherited handles.
The fixture may operate only on `live/coordination.lock` and
`peer/coordination.alias`. It deletes the alias, emits bounded canonical
`deleted` JSON, and waits. The parent requires both children live, alias
absence, unchanged identity and bytes, link count one, and range availability.

After one exact recreate token, the child creates the same alias with
standard-library `os.link`, emits `recreated`, and waits. The parent requires
both children live, matching identity, link count two and exact bytes through
both names, range availability through both names, and persistent exact-name
rename refusal. The parent then sends one exact close token to the mutator,
requires `closed` and exit zero, verifies that the guardian still refuses the
rename, and finally releases the guardian with its existing exact protocol.

After both children close, rename the original successfully and require the
displaced name and peer alias to retain identity, link count two, bytes, and
complete process, pipe, native-handle, and range cleanup. Use no retry or sleep.

## Consequences

The current host reproduces M185's alias-membership ABA when mutation is owned
by a distinct sibling child rather than by the parent coordinator. Guardian
liveness, identity match, exact-name exclusion, and a link-count sample still
do not establish root-confined ownership.

This is a three-process observation under one principal and one parent-owned
process tree: parent coordinator, guardian child, and mutator child. It does
not establish cross-principal behavior, an unrelated process tree or user
session, uncontrolled simultaneous racing, or security isolation from the
mutator. The child is independent only as an operating-system process and
mutation actor.

A future Windows cleanup design still requires authenticated root ownership,
link enumeration and policy, use-time identity and count revalidation,
generation provenance, recovery, and typed refusal receipts. M186 does not
make those decisions and does not authorize cleanup.

Windows remains unadmitted. Cross-volume behavior, ReFS, SMB, other drivers or
Windows versions, file-ID reuse, failed launch, simultaneous owner loss,
hostile handles, mapped views, durable recovery, and independent-host proof
remain open.

No runtime API, adapter, public probe, production subprocess or `ctypes`, cache
access, cleanup authority, dependency, workflow, permission, or hosted check
is added.

## Alternatives considered

- Treat M185's parent mutation as sufficient. Rejected because process
  ownership of the mutation remained an explicit evidence gap.
- Accept this as cross-principal evidence. Rejected because both children run
  under the same principal and parent-owned process tree.
- Pass arbitrary source and alias paths to the fixture. Rejected because fixed
  relative names keep the test authority narrow and reviewable.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  is the only future hosted execution path needed for this source test.

## Validation

Focused validation must prove distinct guardian and mutator process identities,
exact phase/token ordering, initial and restored shared identity/count state,
the live one-link interval, retained bytes, range availability, guardian
liveness and rename refusal, exact child closure, post-close rename, and
complete cleanup. Architecture tests must preserve M185, runtime, examples,
scripts, dependencies, workflows, and the wheel boundary.

Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, findings-first, and guarded-cleanup gates remain
required.

## References

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `CreateHardLinkW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createhardlinkw)
- [Microsoft: `DeleteFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-deletefilew)
- [Microsoft: Hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [Python: `os.link`](https://docs.python.org/3/library/os.html#os.link)
- [GitHub Actions matrix jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [NIST Secure Software Development Framework publications](https://csrc.nist.gov/Projects/ssdf/publications)
- [RFC-0168](0168-probe-windows-hard-link-alias-delete-recreate-aba.md)
