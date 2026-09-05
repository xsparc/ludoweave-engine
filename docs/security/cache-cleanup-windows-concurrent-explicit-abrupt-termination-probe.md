# Windows cache-cleanup concurrent explicit-list abrupt-termination probe

- **Status:** Accepted current-host failure-isolation evidence; Windows is not admitted
- **Milestone:** M170
- **Date:** 2026-08-29
- **Baseline:** M169's concurrent explicit-list restoration-failure probe

## Decision

Retain one Windows-only, test-only controlled observation in which two copies
of M163's fixed child start concurrently with distinct explicit handle lists.
After both parents close, forcibly terminate and wait for one child. Only the
abruptly terminated root becomes renameable while the survivor stays live and
blocks only its own root. Windows is not admitted.

## Why the abrupt concurrent path matters

M156 observes forced termination for a child that opens its own blocker. M167
observes graceful release for two children that inherit distinct blockers.
The unresolved ownership question is whether abrupt termination of one
inherited-handle child releases only its blocker while a concurrent survivor
remains unaffected.

The abruptly terminated root's successful rename after the bounded process
wait proves that terminated-side child ownership settled. Continued false/
error 32 on the survivor root at the same moment proves the remaining child
retains its own distinct blocker and did not acquire the terminated side's
handle.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_concurrent_explicit_abrupt_termination_probe.py`:

1. creates independent A and B `live/candidate.bin` trees beneath one pytest-
   owned, handle-reported NTFS root and opens a distinct noninheritable no-
   delete-share parent handle for each;
2. assigns abrupt and survivor roles in both A/B orientations while preserving
   M156, M163, M167, M169, and the fixed child fixture byte-for-byte;
3. replaces only M163's module-local `os` and subprocess references, requires
   both flags true, starts two real one-handle-list children, captures both
   processes, and holds both restoration entries while both flags remain true;
4. releases both exact native resets, joins both launch threads, requires exact
   `ready`, live children, and false parent inheritability;
5. requires false/error 32 for both roots before and after both parent handles
   close;
6. calls `kill()` only on the abrupt child, waits with the fixed bound, requires
   nonzero status, EOF after `ready`, empty stderr, and no graceful closed
   acknowledgement;
7. requires the abruptly terminated root to return true/code zero while the
   survivor remains live and its root remains false/error 32;
8. closes the survivor through the accepted acknowledgement path, requires
   zero exit and true/code zero for its root; and
9. preserves both payloads beneath ordinary `displaced` directories and
   settles every event, thread, handle, process, and stream.

The asymmetric post-termination result is the distinguishing proof. If the
survivor had inherited the abrupt side's blocker, the abruptly terminated root
would remain denied after its child and both parents closed.

## Safety boundary

- The observation is confined to two exact handles, one fixed local child
  program, two pytest-owned roots, and bounded events, queues, joins, pipes,
  and process waits.
- Both launches use one exact handle list, `close_fds=True`, `shell=False`,
  trusted roots, and owned pipes.
- Python's Windows `kill()` path invokes `TerminateProcess`; an exact bounded
  wait orders the post-termination rename observation.
- The abrupt side receives no release token and produces no graceful closed
  acknowledgement.
- No retry, broad inheritance, `os.system`, environment override, arbitrary
  command, cache access, cleanup command, credential, or network authority is
  present.
- Both created processes are captured before coordination waits so cleanup can
  close or reap them even if later assertions fail.
- `finally` releases every gate, joins both threads, repairs and releases every
  still-owned parent, and closes or reaps every captured process.
- Runtime, examples, scripts, dependencies, workflows, the fixture, all reused
  helpers, and the complete M169 boundary remain unchanged.

## Missing admission evidence

This is not crash recovery and not a concurrency-safe process-creation
contract. Windows admission still requires cancellation semantics, arbitrary
termination timing, every broad and explicit creator, invalid handles, process
trees, cross-process transfer, native close failure, a participation design,
durable recovery, and general leak-freedom.

The previously recorded oplock, lease, share-mode stress, competing actors,
filesystem/driver variation, private adapter, candidate, retained-root,
trusted-time, receipt, and independent-host gaps also remain.

## Scope and CI restraint

M170 adds no runtime subprocess or `ctypes`, adapter, public capability, cache
access, cleanup authority, recovery, mutation command, dependency, native
extension, compiler requirement, API, workflow, job, permission, or CI
allocation. The probe participates only in the existing Windows test suite;
no hosted check is added.

## References

- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Microsoft: creating processes](https://learn.microsoft.com/en-us/windows/win32/procthread/creating-processes)
- [M156 abrupt blocker-owner termination probe](cache-cleanup-windows-abrupt-blocker-termination-probe.md)
- [M169 concurrent restoration-failure probe](cache-cleanup-windows-concurrent-explicit-restore-failure-probe.md)
