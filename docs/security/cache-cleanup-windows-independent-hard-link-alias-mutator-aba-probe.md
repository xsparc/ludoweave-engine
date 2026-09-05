# Windows independent hard-link alias mutator ABA probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M186
- **Date:** 2026-08-29
- **Baseline:** M185's parent-owned hard-link alias delete/recreate ABA boundary

## Decision

Retain one Windows-only, test-only NTFS observation showing that a distinct
mutator child process can delete and recreate a peer hard-link alias while
M181's matching no-delete-share guardian child remains live. The parent only
coordinates and observes. The exact guarded name remains protected while the
shared file's observed link count changes `2 -> 1 -> 2`. Treat this as a
three-process, same-principal negative ownership boundary, not root-confined
ownership and not cleanup authority. Windows is not admitted.

## Test-only contract

`tests/fixtures/windows_hard_link_alias_mutator_child.py` has no arguments and
can address only the fixed relative names `live/coordination.lock` and
`peer/coordination.alias`. It deletes the alias, emits exact bounded `deleted`
JSON, waits for one recreate byte, recreates the alias with `os.link`, emits
`recreated`, waits for one close byte, emits `closed`, and exits zero. Invalid
platform, arguments, or control input fail closed.

`tests/integration/test_windows_cache_cleanup_independent_hard_link_alias_mutator_aba_probe.py`:

1. creates M173's exact ordinary coordination file and peer hard-link alias;
2. opens both entries through the existing capability helper, retains their
   shared `FILE_ID_INFO`, requires link count two, and closes initial handles;
3. starts M181's matching guardian child, requires exact `ready`, and confirms
   exact-name rename refusal with Windows sharing error 32;
4. starts the distinct mutator child with `sys.executable -I -B`, fixed fixture,
   `close_fds=True`, `shell=False`, bounded binary pipes, and no child arguments;
5. requires `deleted`, both children live, alias absence, unchanged identity
   and bytes, link count one, and exclusive byte-range availability;
6. sends the exact recreate byte, requires `recreated`, both children live,
   matching identity, link count two and exact bytes through both names, range
   availability, and persistent exact-name rename refusal;
7. sends the exact close byte, requires mutator `closed` and exit zero, then
   proves the still-live guardian continues refusing the exact-name rename;
8. releases the guardian exactly, renames the original successfully, and
   verifies displaced and alias identities, counts, bytes, process/stream
   closure, and complete native/range ownership cleanup.

The probe uses no retry or sleep. The child inherits only its redirected
standard streams and receives no arbitrary path, operation, environment, shell,
network, production import, or native handle.

## Security consequence

Moving the namespace calls into a distinct child process does not strengthen
the guardian into root ownership. On the observed host, a sibling process can
remove and restore the same alias pathname while the guardian stays live, the
guarded identity and bytes remain stable, and the exact opened name continues
rejecting rename. A one-link observation remains transient.

This is three processes under one principal and one parent-owned process tree.
It is not cross-principal, unrelated-session, hostile-process, or simultaneous-
race evidence. “Independent mutator” means only that a separate operating-
system process owns the delete and recreate calls.

A future design must still decide trusted-root authority, link enumeration and
policy, identity/count revalidation, ABA refusal, durable generation, recovery,
and typed receipts. Cross-volume behavior, ReFS, SMB, other drivers, other
Windows versions, file-ID reuse, failed launch, simultaneous loss, hostile
handles, mapped views, recovery, cleanup authority, and independent-host proof
remain unresolved.

No runtime or package surface changes. No production subprocess, native API,
cache mutation, dependency, workflow, permission, hosted allocation, or hosted
check is added. No hosted check is added. Windows is not admitted.

## Revisit criteria

Revisit Windows admission only after a design supplies trusted root ownership,
an explicit hard-link policy, use-time identity and link-count revalidation,
generation provenance, failure-safe launch and recovery, typed receipts,
cross-principal adversarial evidence, and independent-host proof.

## References

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `CreateHardLinkW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createhardlinkw)
- [Microsoft: `DeleteFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-deletefilew)
- [Microsoft: Hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [RFC-0169](../rfcs/0169-probe-windows-independent-hard-link-alias-mutator-aba.md)
