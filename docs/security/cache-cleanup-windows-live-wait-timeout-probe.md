# Windows cache-cleanup live-blocker wait-timeout probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M160
- **Date:** 2026-08-28
- **Baseline:** M159's blocker broken-control-pipe probe

## Decision

Retain one Windows-only, test-only zero-duration wait observation. It verifies
false/error 32 while M155's unchanged blocker owns the no-delete-share
directory handle, requires exact `TimeoutExpired` from one immediate wait,
proves the child and denial remain live, then uses the unchanged graceful
release/acknowledgement path before the identical native rename returns
true/code zero with content preserved. This is current-host evidence, not a
timeout recovery contract, cleanup authority, or platform admission.

## Why the timeout matters

M155 orders graceful release and M156 orders forced termination. Neither
observes a bounded parent wait that expires while the already-ready child
continues to own the native blocker.

Python documents that `Popen.wait(timeout)` raises `TimeoutExpired` when the
child remains live and can be caught before retrying the wait. Microsoft
documents that a zero-duration wait returns immediately for a nonsignaled
process object. M160 uses the fixture's explicit ready/live assertions and
performs no timing sleep, nonzero wait, kill, or cancellation.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_live_wait_timeout_probe.py`:

1. creates ordinary `live` and candidate entries beneath one pytest-owned root,
   binds that root to handle-reported NTFS, and closes the parent root handle;
2. starts M155's exact child under the current interpreter with `-I -B`,
   explicit pipes, `shell=False`, `close_fds=True`, and the trusted temporary
   root as working directory;
3. requires bounded exact-schema `ready` and a live blocker;
4. runs M154's unchanged isolated rename child and requires false/error 32,
   unchanged namespace/content, and a still-live blocker;
5. invokes exactly one `Popen.wait(timeout=0.0)` and requires
   `TimeoutExpired` with the exact child arguments and timeout value;
6. requires the return code to remain unset and the child to remain live;
7. runs the identical rename child again and requires the same false/error 32
   with namespace/content unchanged;
8. invokes M155's unchanged release helper once and requires exact `closed`
   acknowledgement and child exit zero;
9. runs the identical rename child once more and requires true/code zero; and
10. closes all subprocess streams and preserves the candidate under ordinary
    `displaced`.

The new module remains excluded from the wheel.

## Executed evidence

Execution results are recorded only after the live current-host test runs.

## Missing admission evidence

Windows admission still requires:

- controlled concurrent interleavings inside every acquisition, mutation,
  wait, pipe, cancellation, termination, and close boundary;
- readiness, nonzero process-wait, graceful-close, and post-termination timeout
  behavior, native close failure, cancellation, process restart, and durable
  restart recovery;
- arbitrary pipe failures, Python exception-mapping variation, partial or
  multiple writes, and write retry;
- duplicated/inherited handles, oplock, lease, share-mode stress, competing
  descendants, readers, writers, publishers, cleanup actors, and general
  quiescence/exclusion;
- cross-version, cross-filesystem, cross-driver, alternate-rename, and exact
  native-error variation evidence;
- ancestor substitution, mounted folders, symbolic links, unknown tags, hard-
  link policy, file-ID reuse, pins, and publication interleavings;
- NTFS variation plus ReFS, Dev Drive, removable media, remote shares, and safe
  refusal for every unsupported filesystem;
- crash, disk-full, denial, retry, restore, finalize, and durable recovery;
- an accepted private adapter ABI with bounded backend-neutral errors; and
- candidate, retained-root, policy, trusted-time, durable receipt, and recovery
  designs plus independent installed-host proof.

This single immediate wait is not a timeout recovery contract.

## Scope and CI restraint

M160 adds no runtime subprocess or `ctypes`, helper, adapter, public probe,
cache access, candidate disclosure, cleanup authority, recovery, mutation
command, dependency, native extension, compiler requirement, API, workflow,
job, permission, or CI allocation. The probe participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Python: `Popen.wait`](https://docs.python.org/3/library/subprocess.html#subprocess.Popen.wait)
- [Microsoft: `WaitForSingleObject`](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject)
- [M159 broken-control-pipe probe](cache-cleanup-windows-broken-control-pipe-probe.md)
