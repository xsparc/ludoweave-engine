# Windows cache-cleanup concurrent explicit-list restoration-failure probe

- **Status:** Accepted current-host failure-isolation evidence; Windows is not admitted
- **Milestone:** M169
- **Date:** 2026-08-29
- **Baseline:** M168's concurrent successful/failed explicit-list launch probe

## Decision

Retain one Windows-only, test-only controlled observation in which two copies
of M163's fixed child start concurrently with distinct explicit handle lists,
then one M165-style injected restoration error occurs. Both blocker handles
remain inheritable through both real child creations and both restoration
entries. The failed side's child is reaped before the error escapes while the
surviving child continues to block only its own root. Windows is not admitted.

## Why the mixed restoration outcome matters

M168's failed side never creates a process owner. A restoration failure occurs
after process creation, so the helper must settle a real child while leaving
the parent handle's inheritability repair to its caller. Meanwhile, another
successful helper may still own a live child and a separate blocker.

The failed-restoration root's immediate successful rename after repair and
parent close proves that failed-side child ownership settled. Continued false/
error 32 on the survivor root at the same moment proves the remaining child
retains only its own distinct blocker.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_concurrent_explicit_restore_failure_probe.py`:

1. creates independent A and B `live/candidate.bin` trees beneath one pytest-
   owned, handle-reported NTFS root and opens a distinct noninheritable no-
   delete-share parent handle for each;
2. assigns survivor and injected-failure roles in both A/B orientations while
   preserving M163, M165, M168, and the fixed child fixture byte-for-byte;
3. replaces only M163's module-local `os` and subprocess references, requires
   both flags true and both launch wrappers ready, then releases both real
   one-handle-list `Popen` calls;
4. captures both returned processes before holding both outcomes and both
   restoration entries while both handles remain inheritable;
5. injects the exact M165 failure for one handle, requires M163 to close and
   reap only that child before returning the same error, and requires the
   survivor child to emit `ready` and remain live;
6. explicitly repairs the failed parent flag, requires false/error 32 for both
   roots before parent close, then releases both parents;
7. requires the failed-restoration root to return true/code zero immediately
   while the survivor root remains false/error 32, then closes the survivor
   child and requires its root to return true/code zero; and
8. preserves both payloads beneath ordinary `displaced` directories and
   settles every event, thread, handle, process, and stream.

The failed-restoration root result is the distinguishing proof. If the live
survivor had inherited the failed side's blocker, that root would remain
denied after the failed child and both parents closed.

## Safety boundary

- The observation is confined to two exact handles, one fixed local child
  program, two pytest-owned roots, and bounded events, queues, joins, pipes,
  and process waits.
- Both launches use one exact handle list, `close_fds=True`, `shell=False`,
  trusted roots, and owned pipes.
- The injected setter error is deterministic and acts before one exact native
  reset. It is not a real native restoration failure.
- No broad inheritance, `os.system`, environment override, arbitrary command,
  cache access, cleanup command, credential, or network authority is present.
- Both created processes are captured before the outcome gate so cleanup can
  close or reap them even if later coordination fails.
- `finally` releases every gate, joins both threads, repairs and releases every
  still-owned parent, and closes or reaps every captured process.
- Runtime, examples, scripts, dependencies, workflows, the fixture, all reused
  helpers, and the complete M168 boundary remain unchanged.

## Missing admission evidence

This is not a concurrency-safe process-creation contract. Windows admission
still requires real native and arbitrary restoration failures, arbitrary
launch failures, cancellation, reentrancy, every broad and explicit creator,
invalid handles, child crashes, cross-process transfer, native close failure,
a participation design, and general leak-freedom.

The previously recorded oplock, lease, share-mode stress, competing actors,
filesystem/driver variation, durable recovery, private adapter, candidate,
retained-root, trusted-time, receipt, and independent-host gaps also remain.

## Scope and CI restraint

M169 adds no runtime subprocess or `ctypes`, adapter, public capability, cache
access, cleanup authority, recovery, mutation command, dependency, native
extension, compiler requirement, API, workflow, job, permission, or CI
allocation. The probe participates only in the existing Windows test suite;
no hosted check is added.

## References

- [Python: Windows subprocess startup information](https://docs.python.org/3/library/subprocess.html#windows-popen-helpers)
- [Python: inheritable handles](https://docs.python.org/3/library/os.html#os.set_handle_inheritable)
- [CPython: subprocess implementation](https://github.com/python/cpython/blob/main/Lib/subprocess.py)
- [Microsoft: `SetHandleInformation`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-sethandleinformation)
- [Microsoft: `CreateProcessW`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [M165 restoration-failure probe](cache-cleanup-windows-inherited-restore-failure-probe.md)
- [M168 concurrent launch-failure probe](cache-cleanup-windows-concurrent-explicit-launch-failure-probe.md)
