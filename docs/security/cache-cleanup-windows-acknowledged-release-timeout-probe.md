# Windows cache-cleanup acknowledged-release timeout probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M161
- **Date:** 2026-08-28
- **Baseline:** M160's live-blocker immediate-wait timeout probe

## Decision

Retain one Windows-only, test-only acknowledged-release observation. A fixed
two-token child acknowledges release intent while retaining its no-delete-
share directory handle. One immediate process wait raises `TimeoutExpired`
and the identical native rename remains false/error 32. Only a distinct close
token orders native handle close, exact `closed`, exit zero, and the identical
rename's true/code-zero result with content preserved. This is current-host
evidence, not a graceful-close timeout contract, cleanup authority, or
platform admission.

## Why the acknowledgement matters

M155's single release byte immediately enters handle close, while M160 times
out before sending that byte. Neither exposes a synchronized phase between
request acceptance and native resource release.

The new fixed fixture uses pipe messages as explicit protocol boundaries.
Python documents `Popen.wait(timeout)` and `TimeoutExpired`; Microsoft
documents byte-stream pipe behavior and that share options remain effective
until the handle closes. `release-held` therefore proves only that the child
accepted the fixed request while intentionally retaining the blocker. No wall-
clock delay is used.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_acknowledged_release_timeout_probe.py`:

1. creates ordinary `live` and candidate entries beneath one pytest-owned root,
   binds that root to handle-reported NTFS, and closes the parent root handle;
2. starts the fixed M161 child under the current interpreter with `-I -B`,
   explicit pipes, `shell=False`, `close_fds=True`, and the trusted temporary
   root as working directory;
3. requires bounded exact-schema `ready`, a live child, and M154's unchanged
   false/error 32 result;
4. writes and flushes only the fixed `!` release-intent byte;
5. requires bounded exact-schema `release-held` while the child remains live;
6. invokes exactly one `Popen.wait(timeout=0.0)` and requires
   `TimeoutExpired` with the exact child arguments and timeout value;
7. requires the return code to remain unset and the identical native rename to
   remain false/error 32 with namespace/content unchanged;
8. writes and flushes the distinct fixed `.` close byte and closes the parent
   writer;
9. requires bounded exact-schema `closed`, child exit zero, and both output
   streams at EOF; and
10. requires the identical native rename to return true/code zero while the
    candidate remains preserved under ordinary `displaced`.

The fixed child and integration module remain excluded from the wheel.

## Executed evidence

Execution results are recorded only after the live current-host test runs.

## Missing admission evidence

Windows admission still requires:

- controlled concurrent interleavings inside every acquisition, mutation,
  wait, pipe, cancellation, termination, and native close boundary;
- nonzero process-wait, readiness, actual graceful-close, and post-termination
  timeout behavior, native close failure, cancellation, process restart, and
  durable restart recovery;
- arbitrary pipe failures, Python exception-mapping variation, partial or
  multiple writes, invalid second tokens, and write retry;
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

This single acknowledged release intent is not a graceful-close timeout
contract.

## Scope and CI restraint

M161 adds no runtime subprocess or `ctypes`, adapter, public probe, cache
access, candidate disclosure, cleanup authority, recovery, mutation command,
dependency, native extension, compiler requirement, API, workflow, job,
permission, or CI allocation. The probe participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Python: `Popen.wait`](https://docs.python.org/3/library/subprocess.html#subprocess.Popen.wait)
- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: pipe handle inheritance](https://learn.microsoft.com/en-us/windows/win32/ipc/pipe-handle-inheritance)
- [Microsoft: `CreateFile` sharing](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [M160 live-blocker wait-timeout probe](cache-cleanup-windows-live-wait-timeout-probe.md)
