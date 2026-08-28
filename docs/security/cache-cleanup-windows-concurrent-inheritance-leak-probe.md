# Windows cache-cleanup concurrent broad-inheritance leak probe

- **Status:** Accepted current-host hazard evidence; Windows is not admitted
- **Milestone:** M166
- **Date:** 2026-08-29
- **Baseline:** M165's inherited-handle restoration-failure probe

## Decision

Retain one Windows-only, test-only controlled observation in which a broad-
inheritance child acquires the no-delete-share blocker while M163's explicit-
list launch is paused inside its documented temporary-inheritability window.
Require native rename denial to persist after parent close and intended-child
close, then require success only after the broad child closes. This records a
real current-host hazard, not a concurrency solution. Windows is not admitted.

## Why the concurrent window matters

M163 safely confines its own intended child to one explicit handle list and
restores noninheritability immediately after process creation. M164 and M165
exercise serial failure ownership. Python nevertheless warns that another
thread can leak any temporarily inheritable handle by concurrently launching a
process that inherits all handles. Win32 documents the same all-inheritable
behavior when `CreateProcess` receives `bInheritHandles=TRUE`.

The warning affects cleanup correctness because closing the parent and the
intended child is insufficient if an uncoordinated process has inherited the
same directory handle. M166 makes that retained ownership observable through
the already accepted native rename boundary.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_concurrent_inheritance_leak_probe.py`:

1. creates ordinary `live` and candidate entries beneath one pytest-owned
   root, binds that root to handle-reported NTFS, and closes the root probe;
2. opens one noninheritable no-delete-share parent handle and captures the real
   `Popen` class and inheritability setter;
3. replaces only M163's module-local subprocess reference with a bounded proxy
   that verifies and pauses the exact explicit-list `Popen` call after the
   parent flag becomes inheritable;
4. while that launch thread is event-blocked, requires the flag true and uses
   the captured real class to start M163's fixed child with
   `close_fds=False`, fixed interpreter/path arguments, `shell=False`, trusted
   pytest cwd, and owned pipes;
5. requires the broad child ready and live, releases the intended launch,
   requires its child ready and live, and requires the parent flag restored;
6. requires M154's unchanged false/error 32 native rename before parent close,
   after parent close, and after the intended child closes and exits zero while
   the broad child remains live; and
7. closes the broad child, requires its exit zero, and requires the identical
   fourth rename true/code zero with content preserved beneath ordinary
   `displaced`.

The third denial after intended-child close is the ownership proof: at that
point only the concurrently created broad child can retain the blocker. The
test does not infer leakage from readiness alone.

## Safety boundary

- The hazard is confined to one serial pytest process, one temporary root, one
  exact handle, two fixed local child commands, and bounded events/pipes/waits.
- The test deliberately invokes broad inheritance only while the exact blocker
  is known inheritable; it is not a reusable spawning API.
- The broad child receives no path, credential, environment override, shell,
  network authority, cleanup command, or arbitrary code.
- The module-local proxy leaves the process-wide `subprocess.Popen` binding
  unchanged, so the native rename observer continues to use the real class.
- `finally` always releases the event gate, joins the launch thread, repairs
  the parent flag when the parent handle remains owned, and closes/reaps every
  captured child.
- The accepted M163 helper and fixture, M165 boundary, runtime, examples,
  scripts, dependencies, workflows, and packaged wheel remain unchanged.

This controlled use can transiently inherit other handles that an external
actor has independently marked inheritable in the same pytest process. The
repository does not run tests concurrently or mark unrelated handles
inheritable by contract. That current harness fact bounds this observation; it
does not prove general isolation and is one reason the probe cannot authorize
runtime use or Windows admission.

## Missing admission evidence

Windows admission still requires:

- a concurrency-safe process-creation design covering every broad and explicit
  creator, lock participation, cancellation, failures, and reentrancy;
- controlled simultaneous explicit-list launches and leak-freedom rather than
  the deliberately demonstrated broad-inheritance leak;
- real native restoration failure, invalid inherited values, child crash,
  cross-process duplication/transfer, partial ownership transfer, and native
  close failure;
- other process-creation failures, nonzero wait, actual graceful-close timeout,
  cancellation, process restart, and durable recovery;
- arbitrary pipe failures, partial or multiple writes, retry, and Python
  exception-mapping variation;
- oplock, lease, share-mode stress, competing descendants, readers, writers,
  publishers, cleanup actors, and general quiescence/exclusion;
- cross-version, cross-filesystem, cross-driver, alternate-rename, and exact
  native-error variation evidence;
- NTFS variation plus ReFS, Dev Drive, removable media, remote shares, and safe
  refusal for every unsupported filesystem;
- crash, disk-full, denial, retry, restore, finalize, and durable recovery;
- an accepted private adapter ABI with bounded backend-neutral errors; and
- candidate, retained-root, policy, trusted-time, durable receipt, and recovery
  designs plus independent installed-host proof.

This is one controlled real leak observation, not a safe concurrency contract
or a complete leak-freedom evaluation.

## Scope and CI restraint

M166 adds no runtime subprocess or `ctypes`, adapter, public probe, cache
access, candidate disclosure, cleanup authority, recovery, mutation command,
dependency, native extension, compiler requirement, API, workflow, job,
permission, or CI allocation. The probe participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Python: Windows subprocess startup information](https://docs.python.org/3/library/subprocess.html#windows-popen-helpers)
- [Python: inheritance of file descriptors and handles](https://docs.python.org/3/library/os.html#inheritance-of-file-descriptors)
- [Microsoft: process and handle inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance)
- [Microsoft: `CreateProcessW`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [M165 inherited-handle restoration-failure probe](cache-cleanup-windows-inherited-restore-failure-probe.md)
