# Windows cooperative-lock pathname-substitution probe

- **Status:** Accepted current-host negative capability evidence; Windows is not admitted
- **Milestone:** M174
- **Date:** 2026-08-29
- **Baseline:** M173's same-object cooperative shared/exclusive barrier

## Decision

Retain one Windows-only, test-only controlled observation showing that a live
M173 participant remains bound to the original file object after the
coordination pathname is renamed and replaced, while a fresh participant joins
the replacement object and an independent lock generation. Treat pathname
substitution as a fail-closed design requirement. This is not cleanup
authority. Windows is not admitted.

## Why pathname reuse matters

M173's participants open `live/coordination.lock` with read/write/delete
sharing. Microsoft documents that delete sharing permits later rename or
delete access. It also documents byte-range locks through file handles and a
volume/file identifier for comparing open handles on one computer.

An attacker, stale process, or recovery path that can rename and replace the
coordination file may therefore cause later participants to resolve a
different object. Same pathname spelling and identical bytes do not prove same
identity or same lock generation.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_cooperative_lock_substitution_probe.py`:

1. creates M173's exact ordinary `live/coordination.lock` beneath an NTFS
   pytest root and retains its `FILE_ID_INFO` identity;
2. starts M173's unchanged fixed child and requires its shared lock to remain
   live;
3. runs one fixed isolated child that uses `MoveFileExW` to rename the file to
   `live/coordination.displaced`, creates a new ordinary file at the original
   pathname, writes the exact original bytes, closes, and emits a bounded
   `substituted` result;
4. proves the retained original and displaced handles have the same identity,
   while the replacement has a different identity;
5. starts a second unchanged M173 child through the original pathname and
   requires both old and replacement participants to remain live;
6. requires each file identity to refuse a fail-immediate exclusive lock with
   native error 33;
7. closes the replacement participant and acquires/releases exclusive
   ownership there while the original participant remains live and still
   blocks only the displaced original; and
8. closes the original participant, then acquires/releases exclusive ownership
   of the displaced original, preserving both files' exact bytes and settling
   every handle, process, pipe, and parent owner.

`tests/fixtures/windows_coordination_lock_substitution_child.py` accepts no
argument, path, command, or environment value. It mutates only the two fixed
relative names and creates one noninheritable handle with null security
attributes. It emits no path, payload, or native handle.

## Executed evidence

On the current Windows CPython 3.12 NTFS host, rename and replacement succeed
while the original shared participant remains live. The retained and displaced
original identities match; the replacement identity differs. A fresh shared
participant locks the replacement concurrently. After that new participant
closes, the replacement accepts an exclusive owner while the old participant
still refuses exclusive ownership of the displaced original. Closing the old
participant then permits exclusive ownership there. Both contents remain
identical and every observed owner settles.

## Security consequence

A reusable coordination pathname is not a stable authority boundary. The
cooperative protocol can split into independently quiescent generations unless
every participant binds the same trusted root identity, coordination file
identity, and generation and revalidates them around mutation.

This probe does not define that binding or prove protection from an actor that
can replace the coordination namespace. It does not establish participant
completeness, mapped-view coverage, abrupt-exit settlement, delayed unlock
behavior, filesystem variation, recovery, policy, receipts, or independent-
host behavior. M174 is negative capability evidence, not cleanup authority,
and Windows is not admitted.

## Scope and CI restraint

M174 adds no runtime subprocess or `ctypes`, adapter, lock API, public probe,
cache access, candidate disclosure, cleanup authority, mutation command,
dependency, native extension, compiler requirement, workflow, job,
permission, or CI allocation. The fixture participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Microsoft: `LockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex)
- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `MoveFileExW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [Microsoft: `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [M147 cleanup threat model](cache-cleanup-threat-model.md)
- [M173 cooperative-lock probe](cache-cleanup-windows-cooperative-lock-probe.md)
