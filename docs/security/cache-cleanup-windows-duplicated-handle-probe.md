# Windows cache-cleanup duplicated-handle retention probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M162
- **Date:** 2026-08-28
- **Baseline:** M161's acknowledged-release timeout probe

## Decision

Retain one Windows-only, test-only same-process duplicate observation. A fixed
child opens a no-delete-share directory handle, duplicates it with the same
access and inheritance disabled, and closes each owned handle behind a
separate token. Closing the original leaves the identical native rename
false/error 32. Closing the final duplicate permits true/code zero with
content preserved. This is current-host evidence, not inherited-handle
evidence, cleanup authority, or platform admission.

## Why the duplicate matters

M153-M161 use one blocker handle. Process exit or the fixture's explicit close
releases that sole owner, so those probes cannot distinguish one handle's
closure from the underlying object's final handle-count transition.

Microsoft documents that a duplicate is a unique handle referring to the same
object. It also documents per-handle closure and object retention until the
last handle closes. The fixed child therefore duplicates before readiness,
then exposes two explicit close boundaries without a wall-clock delay.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_duplicated_handle_probe.py`:

1. creates ordinary `live` and candidate entries beneath one pytest-owned root,
   binds that root to handle-reported NTFS, and closes the parent root handle;
2. starts the fixed M162 child under the current interpreter with `-I -B`,
   explicit pipes, `shell=False`, `close_fds=True`, and the trusted temporary
   root as working directory;
3. requires bounded exact-schema `ready`, a live child, and M154's unchanged
   false/error 32 result;
4. writes and flushes only fixed byte `1`;
5. requires bounded exact-schema `original-closed`, a live child, and the
   identical native rename's second false/error 32 result with namespace and
   content unchanged;
6. writes and flushes only fixed byte `2` and closes the parent writer;
7. requires bounded exact-schema `closed`, child exit zero, and both output
   streams at EOF; and
8. requires the identical native rename to return true/code zero while the
   candidate remains preserved under ordinary `displaced`.

The fixed child creates a same-process, noninheritable,
`DUPLICATE_SAME_ACCESS` handle before `ready`, closes the original exactly once
before `original-closed`, and closes the duplicate exactly once before
`closed`. Failure cleanup closes only still-owned handles. The fixture and
integration module remain excluded from the wheel.

## Executed evidence

Execution results are recorded only after the live current-host test runs.

## Missing admission evidence

Windows admission still requires:

- controlled concurrent interleavings inside every acquisition, duplication,
  mutation, wait, pipe, cancellation, termination, and native close boundary;
- inherited handles, cross-process duplication/transfer, duplicate-creation
  failure, native close failure, and partial ownership transfer;
- nonzero process-wait, readiness, actual graceful-close, and post-termination
  timeout behavior, cancellation, process restart, and durable recovery;
- arbitrary pipe failures, Python exception-mapping variation, partial or
  multiple writes, invalid second tokens, and write retry;
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

This same-process duplicate is not inherited-handle evidence and does not
admit a general handle-reference policy.

## Scope and CI restraint

M162 adds no runtime subprocess or `ctypes`, adapter, public probe, cache
access, candidate disclosure, cleanup authority, recovery, mutation command,
dependency, native extension, compiler requirement, API, workflow, job,
permission, or CI allocation. The probe participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Microsoft: `DuplicateHandle`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-duplicatehandle)
- [Microsoft: `CloseHandle`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle)
- [Microsoft: `GetCurrentProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getcurrentprocess)
- [Microsoft: handle inheritance](https://learn.microsoft.com/en-us/windows/win32/sysinfo/handle-inheritance)
- [Microsoft: `CreateFileW` sharing](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [M161 acknowledged-release timeout probe](cache-cleanup-windows-acknowledged-release-timeout-probe.md)
