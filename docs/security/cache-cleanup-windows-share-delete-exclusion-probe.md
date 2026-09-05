# Windows cache-cleanup share-delete exclusion probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M153
- **Date:** 2026-08-28
- **Baseline:** M152's cross-process retained-parent substitution probe

## Decision

Retain one Windows-only, test-only cross-process share-delete fixture. It
verifies that omitting delete sharing from a retained directory handle blocks
one fixed child-process rename until the parent closes that handle. The result
is narrow exclusion evidence, not cleanup authority or platform admission.

## Why the complementary share mode matters

M152 opens the retained directory with read, write, and delete sharing, then
observes a successful rename from a distinct process. Microsoft states that a
handle's sharing options stay in effect until close regardless of process
context, and that omitting `FILE_SHARE_DELETE` prevents later delete-access
opens while the handle remains open. Delete access includes rename.

M153 omits only delete sharing from a separate `live` directory handle. The
first child rename must fail without changing either name or content. The
parent then closes that exact blocking handle and executes the same child
command again. Success after release provides a direct paired observation
without parsing locale-dependent command output or inferring a native error
code the fixture does not read. It is not general cross-process exclusion.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_share_delete_probe.py`:

1. creates an ordinary `live` directory and candidate below one pytest-owned
   temporary root;
2. opens the root and requires handle-bound NTFS;
3. opens and retains `live` with read and write sharing but without delete
   sharing, while rejecting a reparse entry;
4. starts one child `cmd.exe` directly with `shell=False`, `close_fds=True`, a
   bounded timeout, the trusted pytest root as its working directory, and only
   the fixed command `ren live displaced`;
5. requires nonzero child exit, unchanged `live`, absent `displaced`, unchanged
   candidate bytes, and both accepted native handles still owned;
6. deterministically closes the blocking `live` handle while retaining the
   opened root;
7. executes the identical child command and requires successful exit;
8. requires `live` to be absent and an ordinary `displaced` directory to hold
   the unchanged candidate; and
9. closes the remaining root handle and proves zero native handles remain.

No caller-derived path, environment value, or candidate name enters the child
command string. The module is skipped outside Windows, excluded from the
wheel, and imports only retained test support.

## Executed evidence

On the current Windows CPython 3.12 host, the opened pytest root reports NTFS.
The first fixed child command returns nonzero while the parent owns the
no-delete-share handle and leaves the directory and candidate unchanged. After
the parent closes that handle, the identical command returns zero and the
unchanged candidate is present under `displaced`. Both native handles close.

## Missing admission evidence

Windows admission still requires:

- controlled concurrent interleavings at every acquisition and mutation
  boundary, with direct native error capture and explicit synchronization;
- exclusion or quiescence against competing readers, writers, publishers,
  cleanup actors, handle duplication/inheritance, and descendant activity;
- oplock, lease, share-mode, cancellation, timeout, and close-failure behavior;
- ancestor substitution before acquisition, mounted folders, symbolic links,
  unknown tags, and every supported component depth;
- NTFS variation plus ReFS, Dev Drive, removable media, remote shares, and safe
  refusal for every unsupported filesystem;
- hard-link policy, file-ID reuse, pins, and publication interleavings;
- crash, disk-full, denial, retry, restore, finalize, and durable recovery
  evidence;
- an accepted private adapter ABI with bounded backend-neutral errors; and
- candidate, retained-root, policy, trusted-time, durable receipt, and recovery
  designs plus independent installed-host proof.

## Scope and CI restraint

M153 adds no runtime subprocess or `ctypes`, adapter, public probe, cache access,
candidate disclosure, cleanup authority, mutation command, dependency, native
extension, compiler requirement, API, workflow, job, permission, or CI
allocation. The fixture participates only in the existing Windows test suite;
no hosted check is added.

## References

- [Microsoft: `CreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)
- [Microsoft: system error codes](https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-)
- [Microsoft: `cmd`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd)
- [Microsoft: `ren`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ren)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [M152 cross-process substitution probe](cache-cleanup-windows-cross-process-substitution-probe.md)
