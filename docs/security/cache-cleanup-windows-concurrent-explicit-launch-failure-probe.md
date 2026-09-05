# Windows cache-cleanup concurrent explicit-list launch-failure probe

- **Status:** Accepted current-host failure-isolation evidence; Windows is not admitted
- **Milestone:** M168
- **Date:** 2026-08-29
- **Baseline:** M167's simultaneous successful explicit-list isolation probe

## Decision

Retain one Windows-only, test-only controlled observation in which M163's fixed
child starts while M164's distinct explicit-list launch fails on its fixed
missing executable. Both blocker handles remain inheritable through both real
outcomes and both restoration entries. After both parents close, the failed-
launch root becomes renameable while the successful child still blocks only
its own root. Windows is not admitted.

## Why the mixed outcome matters

M167 observes two successful one-handle-list launches. A failed creator has a
different ownership transition: no process object returns, but its parent
handle was temporarily inheritable during the real Win32 call. The unresolved
question is whether a simultaneously successful explicit-list child remains
confined to its own list across that failure window.

Readiness alone cannot answer the question. The failed-launch root's immediate
successful rename after both parents close proves that no child retains its
blocker. Continued false/error 32 on the successful root at the same moment
proves that only the intended live child owns that distinct blocker.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_concurrent_explicit_launch_failure_probe.py`:

1. creates independent A and B `live/candidate.bin` trees beneath one pytest-
   owned, handle-reported NTFS root and opens a distinct noninheritable no-
   delete-share parent handle for each;
2. assigns success and failure roles in both A/B orientations while preserving
   M163, M164, and the fixed child fixture byte-for-byte;
3. replaces only each helper's module-local `os` and subprocess references,
   requires both flags true and both launch wrappers ready, then releases both
   captured-real `Popen` calls;
4. captures the successful process before waiting, captures the real
   `FileNotFoundError`, and holds both outcomes while both flags remain true;
5. requires both helpers waiting at restoration, releases both flag resets,
   joins both threads, and requires the exact returned failure, successful
   child readiness, and both parent flags false;
6. requires false/error 32 for both roots before parent close, releases both
   parents, then requires the failed-launch root true/code zero while the live
   successful-child root remains false/error 32; and
7. closes the successful child, requires its root true/code zero, and preserves
   both payloads beneath ordinary `displaced` directories.

The failed-launch root result is the distinguishing proof. If the successful
child had inherited the failure handle, that root would remain denied after
both parent handles closed.

## Safety boundary

- The observation is confined to two exact handles, two fixed local launch
  paths, two pytest-owned roots, and bounded events, queues, joins, pipes, and
  process waits.
- The successful path uses M163's fixed child, one exact handle list,
  `close_fds=True`, `shell=False`, its trusted root, and owned pipes.
- The failure path uses M164's fixed absent executable, one distinct handle
  list, `close_fds=True`, `shell=False`, its trusted root, and `DEVNULL`.
- No broad inheritance, `os.system`, environment override, arbitrary command,
  cache access, cleanup command, credential, or network authority is present.
- A successfully created process is captured before the outcome gate, including
  an unexpected process on the nominal failure path, so cleanup can reap it.
- `finally` releases every gate, joins both threads, repairs and releases every
  still-owned parent, and closes/reaps every captured process.
- Runtime, examples, scripts, dependencies, workflows, the fixture, both reused
  helpers, and the complete M167 boundary remain unchanged.

## Missing admission evidence

This successful/missing-executable pair is not a concurrency-safe
process-creation contract. Windows admission still requires arbitrary launch and
restoration failures, cancellation, reentrancy, every broad and explicit
creator, invalid handles, child crashes, cross-process transfer, native close
failure, a participation design, and general leak-freedom.

The previously recorded oplock, lease, share-mode stress, competing actors,
filesystem/driver variation, durable recovery, private adapter, candidate,
retained-root, trusted-time, receipt, and independent-host gaps also remain.

## Scope and CI restraint

M168 adds no runtime subprocess or `ctypes`, adapter, public capability, cache
access, cleanup authority, recovery, mutation command, dependency, native
extension, compiler requirement, API, workflow, job, permission, or CI
allocation. The probe participates only in the existing Windows test suite; no
hosted check is added.

## References

- [Python: Windows subprocess startup information](https://docs.python.org/3/library/subprocess.html#windows-popen-helpers)
- [CPython: subprocess implementation](https://github.com/python/cpython/blob/main/Lib/subprocess.py)
- [Microsoft: `CreateProcessW`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [Microsoft: creating processes](https://learn.microsoft.com/en-us/windows/win32/procthread/creating-processes)
- [M167 concurrent explicit-list isolation probe](cache-cleanup-windows-concurrent-explicit-inheritance-probe.md)
