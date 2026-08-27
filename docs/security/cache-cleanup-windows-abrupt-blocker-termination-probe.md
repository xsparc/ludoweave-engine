# Windows cache-cleanup abrupt blocker-owner termination probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M156
- **Date:** 2026-08-28
- **Baseline:** M155's child-owned share-delete handshake

## Decision

Retain one Windows-only, test-only abrupt blocker-owner termination probe. It
verifies false/error 32 while M155's unchanged blocker child owns the
no-delete-share directory handle, forces that process to terminate without the
release token, waits with a fixed bound, observes no closed acknowledgement,
and requires the identical native rename child to return true/code zero with
content preserved. This is current-host evidence, not cleanup authority or
platform admission.

## Why the abrupt path matters

M155 orders acquisition and cooperative close but deliberately leaves abrupt
owner termination unresolved. The child closes its handle in `finally` only
when it receives the fixed release byte. M156 does not send that byte, so the
child cannot execute its normal closure acknowledgement.

Microsoft documents that open kernel-object handles are closed automatically
when a process terminates. Because it also documents forced termination as
asynchronous for another process, the parent uses Python's Windows
`Popen.kill()` mapping and waits with M155's existing timeout before retrying
the rename. The test has no retry loop or timing sleep.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_abrupt_blocker_termination_probe.py`:

1. creates ordinary `live` and candidate entries beneath one pytest-owned root,
   binds that root to handle-reported NTFS, and closes the parent root handle;
2. starts M155's exact child under the current interpreter with `-I -B`,
   explicit pipes, `shell=False`, `close_fds=True`, and the trusted temporary
   root as working directory;
3. requires bounded exact-schema `ready` and a live blocker;
4. runs M154's unchanged isolated rename child and requires false/error 32,
   unchanged namespace/content, and a still-live blocker;
5. sends no release token, calls `kill()`, and waits with the existing fixed
   timeout;
6. requires a nonzero but not numerically standardized return code, EOF with no
   `closed` acknowledgement, and empty stderr;
7. runs the identical rename child once and requires true/code zero; and
8. closes all subprocess streams and preserves the candidate under ordinary
   `displaced`.

The post-wait pipe reads are bounded and safe because the fixed child has
already terminated and its only possible stdout documents are tiny and
schema-bounded. The new module remains excluded from the wheel.

## Executed evidence

Execution results are recorded only after the live current-host test runs.

## Missing admission evidence

Windows admission still requires:

- controlled concurrent interleavings inside every acquisition, mutation,
  termination, cancellation, and close boundary;
- duplicated/inherited handles, pipe failure, readiness/termination timeout,
  close failure, cancellation, process restart, and durable restart recovery;
- oplock, lease, share-mode stress, competing descendants, readers, writers,
  publishers, cleanup actors, and general quiescence/exclusion;
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

This single forced-termination observation is not crash recovery.

## Scope and CI restraint

M156 adds no runtime subprocess or `ctypes`, helper, adapter, public probe,
cache access, candidate disclosure, cleanup authority, mutation command,
dependency, native extension, compiler requirement, API, workflow, job,
permission, or CI allocation. The probe participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Microsoft: terminating a process](https://learn.microsoft.com/en-us/windows/win32/procthread/terminating-a-process)
- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [M155 child-owned handshake](cache-cleanup-windows-child-owned-share-delete-handshake.md)
