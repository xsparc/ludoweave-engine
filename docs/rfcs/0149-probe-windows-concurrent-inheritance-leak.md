# RFC-0149: probe Windows concurrent broad-inheritance leakage

- **Status:** Accepted
- **Milestone:** M166
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that deterministically pauses M163's
explicit-list launch after its blocker handle becomes inheritable, starts a
second fixed child with broad handle inheritance, and proves that the second
child retains the blocker after both parent close and intended-child close.
Require native rename to succeed only after the broad-inheritance child closes.
Add no runtime or CI surface.

## Context

M163 follows Python's documented explicit-handle-list pattern: it marks one
handle inheritable immediately around process creation and restores the flag in
`finally`. M164 covers a failed process creation, and M165 covers child
reclamation after an injected restoration failure. Those serial observations
do not establish concurrent-launch safety.

Python explicitly warns that a temporarily inheritable Windows handle can leak
when another thread concurrently invokes a process-creation function that
inherits all handles. Microsoft likewise documents that `CreateProcess` with
`bInheritHandles=TRUE` transfers every inheritable handle and calls out the
multithreaded hazard. One event-controlled current-host observation can prove
that the warning is material to the exact blocker used by the cache-cleanup
evaluation without inventing a production solution.

## Decision

Accept the [Windows concurrent broad-inheritance leak
probe](../security/cache-cleanup-windows-concurrent-inheritance-leak-probe.md)
as current-host, test-only hazard evidence.

The test binds its pytest-owned root to handle-reported NTFS and opens one
noninheritable no-delete-share handle to ordinary relative `live`. It preserves
M163's helper and child fixture byte-for-byte. A module-local subprocess proxy
delegates the exact explicit-list `Popen` call but pauses it with two bounded
`threading.Event` objects after M163 has made the blocker inheritable and before
the intended child is created.

While the explicit-launch thread is paused, the caller verifies the parent
flag is inheritable and uses the captured real `Popen` class to create the same
fixed child with `close_fds=False`, a fixed executable, `shell=False`, trusted
pytest working directory, and owned standard pipes. The broad child must emit
exact `ready` while live. The caller then releases the explicit launch, requires
its exact fixed child to become ready, and requires M163's unchanged `finally`
to restore the parent handle to noninheritable.

Require M154's unchanged native rename to remain false/error 32 in each of
these ordered states:

1. parent and both child handles are live;
2. the parent handle has closed and both children remain live; and
3. the intended explicit-list child has acknowledged close, exited zero, and
   only the broad-inheritance child remains live.

The third denial is the distinguishing evidence that the concurrently created
broad child acquired the temporarily inheritable blocker. After that child
acknowledges close and exits zero, require the identical fourth rename to
return true/code zero with content preserved beneath ordinary `displaced`.

All waits are event-, pipe-, or process-bounded. A `finally` boundary releases
the paused thread, restores noninheritability if the parent still owns the
handle, and closes/reaps any created child. Do not modify an accepted helper or
fixture, use sleeps, use `os.system`, claim broad inheritance is safe, add a
global process-launch lock, add runtime subprocess or `ctypes`, add a
dependency, or add workflow/CI allocation.

## Consequences

The current host now demonstrates the exact leak hazard described by Python
and Win32 documentation: an explicit handle list does not protect a temporarily
inheritable handle from a concurrent process creation that deliberately
inherits all handles.

This is one controlled adverse interleaving. It is not a concurrency-safe
inheritance contract, a general leak census, a production lock or spawn
coordinator, arbitrary process-creator coverage, cancellation/failure
coverage, recovery, general exclusion, or platform admission.

Windows is not admitted.

## Alternatives considered

- Add a process-global runtime lock. Rejected because a lock is effective only
  if every process creator participates; that ownership and compatibility
  contract has not been designed or admitted.
- Run two concurrent explicit-list launches. Rejected because it would not
  isolate the documented all-inheritable-handle leak boundary.
- Add a new child fixture. Rejected because M163's fixed child already proves
  ownership through ordered denial and successful close.
- Use `os.system`. Rejected because fixed executable selection, owned pipes,
  bounded cleanup, and `shell=False` provide a narrower test boundary.
- Add another hosted job. Rejected because the existing Windows suite can run
  the probe after the unpublished stack is safely integrated.

## Validation

Focused validation must prove the event-controlled pause occurs while the
parent flag is true; both fixed children become ready; the helper restores the
parent flag; all four native rename results occur in exact order; the parent
owned count reaches zero; the intended child closes before the third denial;
the broad child is still live at that denial; both children exit zero; and
content remains unchanged until the final successful rename. Architecture
tests must preserve M165, the reused M163 helper and fixture, runtime, examples,
scripts, dependencies, workflows, and wheel contents. Supported-Python, full
regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [Python: Windows subprocess startup information](https://docs.python.org/3/library/subprocess.html#windows-popen-helpers)
- [Python: inheritance of file descriptors and handles](https://docs.python.org/3/library/os.html#inheritance-of-file-descriptors)
- [Microsoft: process and handle inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance)
- [Microsoft: `CreateProcessW`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [RFC-0148](0148-probe-windows-inherited-restore-failure.md)
