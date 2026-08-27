# Windows cache-cleanup retained-parent substitution probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M151
- **Date:** 2026-08-28
- **Baseline:** M149's owned-handle probe and M150's junction fixture

## Decision

Retain one Windows-only, test-only namespace substitution fixture. It verifies
what an already retained parent handle addresses after the parent's former
name is rebound to a directory junction. The result remains current-host
feasibility evidence rather than a cleanup capability or admission decision.

## Why retained-parent evidence matters

M147 requires identity-at-use and no-follow traversal across namespace changes.
Microsoft documents that an opened file object persists until its handles are
closed and that a non-null `OBJECT_ATTRIBUTES.RootDirectory` makes the next
name relative to that opened directory. `FILE_SHARE_DELETE` permits later
rename access, while `FILE_ID_INFO` supplies the volume and file identity used
to compare open objects on one computer.

M151 executes these relationships rather than inferring safety from paths. It
does not claim that one same-process substitution proves concurrent-race or
cross-process exclusion behavior.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_retained_parent_probe.py`:

1. creates ordinary `live` and `target` directories below one pytest-owned
   temporary root, with distinct same-named candidate contents;
2. opens the root and requires handle-bound NTFS plus reparse support;
3. opens and retains `live`, records its open-object identity, renames it to
   `displaced`, and proves the retained parent identity is unchanged;
4. invokes fixed `cmd.exe /d /c mklink /j live target` component arguments from
   the trusted pytest root, with no caller-controlled command argument;
5. requires a fresh root-relative `live` open to observe and refuse the
   junction, closing the rejected handle;
6. opens `candidate.bin` through the retained parent, through the fresh
   `displaced` name, and through the ordinary `target` parent;
7. proves the retained-parent identity equals the displaced-file identity and
   differs from the target-file identity;
8. closes all seven accepted native handles deterministically; and
9. removes only the junction entry and proves both candidate contents remain
   unchanged.

The module is skipped outside Windows and excluded from the wheel. It imports
only retained test support and is not a runtime fallback, capability API,
cleanup implementation, or admission decision.

## Executed evidence

On the current Windows 10.0.26200 CPython 3.12 host, the opened pytest root
reports NTFS and reparse support. The directory rename succeeds while the
original parent handle remains open with delete sharing. Junction substitution
succeeds without elevation. The fresh name is refused, while the retained
parent opens the exact file identity now reachable under `displaced`, not the
distinct file under `target`. Link-only cleanup preserves both contents.

## Missing admission evidence

Windows admission still requires:

- deterministic concurrent and cross-process swaps at every acquisition and
  mutation boundary, including oplock/share-mode behavior;
- ancestor substitution before acquisition, mounted folders, symbolic links,
  unknown tags, and every supported component depth;
- NTFS variation plus ReFS, Dev Drive, removable media, remote shares, and safe
  refusal for every unsupported filesystem;
- hard-link policy, file-ID reuse, quiescence, readers, writers, leases, pins,
  and publication interleavings;
- crash, cancellation, disk-full, denial, retry, restore, and finalize evidence;
- an accepted private adapter ABI with bounded backend-neutral errors; and
- candidate, retained-root, policy, trusted-time, durable receipt, and recovery
  designs plus independent installed-host proof.

## Scope and CI restraint

M151 adds no runtime `ctypes`, shell invocation, adapter, public probe, cache
access, candidate disclosure, cleanup authority, mutation command, dependency,
native extension, compiler requirement, API, workflow, job, permission, or CI
allocation. The fixture participates only in the existing Windows test suite;
no hosted check is added.

## References

- [Microsoft: opening a handle to a file](https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/opening-a-handle-to-a-file)
- [Microsoft: `OBJECT_ATTRIBUTES`](https://learn.microsoft.com/en-us/windows/win32/api/ntdef/ns-ntdef-_object_attributes)
- [Microsoft: `NtCreateFile`](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/nf-ntifs-ntcreatefile)
- [Microsoft: `CreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)
- [Microsoft: `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [M150 Windows junction probe](cache-cleanup-windows-junction-probe.md)
