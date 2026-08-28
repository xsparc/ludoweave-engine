# Windows cache-cleanup cooperative-lock probe

- **Status:** Accepted current-host cooperative capability evidence; Windows is not admitted
- **Milestone:** M173
- **Date:** 2026-08-29
- **Baseline:** M172's directory/descendant non-exclusion result

## Decision

Retain one Windows-only, test-only controlled observation showing that
multiple shared owners of one fixed coordination-file range coexist and
collectively refuse an exclusive owner until the last shared owner closes.
Also require the exclusive owner to refuse a late shared participant until
exact release. Treat this only as a cooperative participant primitive, not
cleanup authority. Windows is not admitted.

## Why a separate coordination object matters

M172 proves that holding a directory does not recursively exclude handles to
its descendants. A future cleanup therefore cannot infer participant
quiescence from a root-directory handle. Every relevant engine participant
would instead need to join one explicit protocol over a stable identity and
generation.

Microsoft documents overlapping shared `LockFileEx` regions and incompatible
exclusive regions on the same file. It also documents fail-immediate requests,
explicit unlock, delayed release after process termination, and the fact that
mapped views bypass byte-range locking. M173 exercises only the smallest
positive shared/exclusive boundary and retains every caveat.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_cooperative_lock_probe.py`:

1. creates one ordinary `live/coordination.lock` below an NTFS pytest root;
2. starts two fixed isolated children that open only that file with generic
   read access, read/write/delete sharing, null security attributes, and
   noninheritable handles;
3. requires both children to hold overlapping shared fail-immediate locks over
   byte zero with length one and emit exact bounded `ready`;
4. requires an exclusive parent request for the identical range to fail with
   native error 33 while both shared owners remain live;
5. closes one child exactly and requires the remaining child alone to preserve
   the same refusal;
6. closes the last child exactly, acquires the exclusive owner, proves it
   noninheritable, then explicitly unlocks and closes it;
7. reverses ownership, requiring an exclusive owner to make a late shared
   child emit exact `refused`/33 until release, after which a fresh shared child
   completes exact `ready`/`closed`; and
8. preserves coordination bytes and settles every handle, process, pipe, and
   temporary owner with fixed bounds and zero leaked ownership.

`tests/fixtures/windows_coordination_lock_participant_child.py` accepts no
argument, path, command, or environment value. It owns only the fixed ordinary
file handle and range lock. It never returns a native handle or filesystem
path.

## Executed evidence

On the current Windows CPython 3.12 NTFS host, two distinct child processes
hold the same shared range concurrently. The parent-exclusive request fails
with error 33 until the second and final child explicitly unlocks and closes.
With the exclusive parent held first, a late child reports error 33; after
exact parent unlock/close, a fresh child acquires and closes normally. Every
process exits zero, every parent owner settles, and the coordination bytes are
unchanged.

## Security consequence

The result provides positive evidence for a cooperative shared/exclusive
participant barrier over one known object and range. It does not control any
process that fails to participate. It does not prove stable coordination-file
identity, generation binding, complete retained roots, mapped views,
substitution resistance, arbitrary cancellation, abrupt process death,
delayed operating-system unlock, native close/unlock failure, wait fairness,
filesystem variation, recovery, policy, receipts, or independent hosts.

Any later design must admit the exact coordination identity beneath a retained
cache-root capability, bind all readers/writers/leases/pins and publication
state to a generation, fail closed when participation is incomplete, and
revalidate those bindings through mutation. M173 is not cleanup authority and
does not admit Windows.

## Scope and CI restraint

M173 adds no runtime subprocess or `ctypes`, adapter, lock API, public probe,
cache access, candidate disclosure, cleanup authority, mutation command,
dependency, native extension, compiler requirement, workflow, job,
permission, or CI allocation. The fixture participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Microsoft: `LockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex)
- [Microsoft: `UnlockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-unlockfileex)
- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [M147 cleanup threat model](cache-cleanup-threat-model.md)
- [M172 descendant non-exclusion probe](cache-cleanup-windows-descendant-non-exclusion-probe.md)
