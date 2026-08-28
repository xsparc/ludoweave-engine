# Windows cache-cleanup concurrent explicit-list isolation probe

- **Status:** Accepted current-host pairwise isolation evidence; Windows is not admitted
- **Milestone:** M167
- **Date:** 2026-08-29
- **Baseline:** M166's concurrent broad-inheritance leak observation

## Decision

Retain one Windows-only, test-only controlled observation in which two distinct
no-delete-share handles are simultaneously inheritable while two real fixed
children are created. Each child receives only its own explicit handle list.
After both parent handles close, releasing either child permits rename only for
its corresponding root; the reverse order proves the same pairwise isolation.
Windows is not admitted.

## Why simultaneous explicit lists matter

M166 proves the adverse case: a concurrent broad-inheritance creator can
acquire an unrelated temporarily inheritable blocker. Python warns about that
combination, while Microsoft recommends explicit handle lists for callers that
create processes simultaneously and need different inherited handles.

M167 observes the narrower recommended mechanism directly. Both no-delete-
share handles remain inheritable across both real process-creation calls, so a
serial launch cannot explain the result. Ordered native rename outcomes then
identify which child owns which blocker rather than inferring ownership from
process readiness.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_concurrent_explicit_inheritance_probe.py`:

1. creates two distinct ordinary `live/candidate.bin` trees beneath one
   pytest-owned root, binds the root to handle-reported NTFS, and opens one
   noninheritable no-delete-share parent handle for each `live` directory;
2. replaces only M163's module-local `os` and subprocess references with
   bounded coordination proxies while preserving its helper and child fixture;
3. requires both parent handles inheritable, delegates two real `Popen` calls
   with separate one-handle lists and `close_fds=True`, and prevents either
   helper from returning or restoring until both creations complete;
4. requires both helpers waiting at restoration while both flags remain true,
   then releases restoration, joins both threads, and requires both flags false;
5. requires both children ready/live and M154's false/error 32 result for each
   root before and after both parent handles close;
6. releases the children in both A-to-B and B-to-A orders, requiring the first
   root's rename true/code zero while the second root remains false/error 32;
   and
7. releases the second child, requires its rename true/code zero, and preserves
   both distinct payloads beneath ordinary `displaced` directories.

The release-order outcome is the pairwise isolation proof. If either child had
inherited the other root's blocker, closing the intended owner would not permit
that root's immediate rename while the other child remained live.

## Safety boundary

- The observation is confined to two fixed children, two exact handles, two
  pytest-owned roots, and bounded events, queues, pipes, joins, and waits.
- Each process creation uses the captured real `Popen`, a one-handle explicit
  list, `close_fds=True`, fixed interpreter/path arguments, `shell=False`, its
  trusted pytest root, and owned standard pipes.
- No broad inheritance, `os.system`, environment override, arbitrary command,
  cache access, cleanup command, credential, or network authority is present.
- Process owners are captured immediately after each real creation and before
  the coordination wait, so failure cleanup can close/reap them.
- `finally` releases every gate, joins both threads, restores any still-owned
  parent flag, releases any still-owned parent handle, and closes every child.
- Runtime, examples, scripts, dependencies, workflows, M163's helper/fixture,
  and the complete M166 boundary remain unchanged.

## Missing admission evidence

This is pairwise isolation for one controlled successful overlap, not a
concurrency-safe process-creation contract. Windows admission still requires a
design covering every broad and explicit creator, lock or coordinator
participation, cancellation, launch and restoration failures, reentrancy,
invalid handles, child crashes, cross-process duplication/transfer, native
close failures, and general leak-freedom.

Admission also remains blocked on the previously recorded oplock, lease,
share-mode stress, competing descendant/reader/writer/publisher/cleanup actor,
filesystem/driver variation, durable recovery, private adapter, candidate,
retained-root, trusted-time, receipt, and independent-host evidence gaps.

## Scope and CI restraint

M167 adds no runtime subprocess or `ctypes`, adapter, public capability, cache
access, candidate disclosure, cleanup authority, recovery, mutation command,
dependency, native extension, compiler requirement, API, workflow, job,
permission, or CI allocation. The probe participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Python: Windows subprocess startup information](https://docs.python.org/3/library/subprocess.html#windows-popen-helpers)
- [Microsoft: process and handle inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance)
- [Microsoft: `CreateProcessW`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [M166 concurrent broad-inheritance leak probe](cache-cleanup-windows-concurrent-inheritance-leak-probe.md)
