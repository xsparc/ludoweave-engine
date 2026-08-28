# Windows cache-cleanup descendant non-exclusion probe

- **Status:** Accepted current-host negative capability evidence; Windows is not admitted
- **Milestone:** M172
- **Date:** 2026-08-29
- **Baseline:** M171's exclusive-root acquisition probe

## Decision

Retain one Windows-only, test-only controlled observation showing that M171's
zero-sharing directory owner and a separate descendant file owner can coexist
in either acquisition order. Treat the directory primitive as object-specific,
not recursive quiescence. Windows is not admitted.

## Why descendant scope matters

M147 requires cleanup to exclude or account for every concurrent reader,
writer, lease, pin, publisher, and recovery participant. M171 proves that two
incompatible opens of the same directory object fail closed. It does not prove
that holding the directory affects a distinct file object below it.

Microsoft's `CreateFile` contract describes access/share compatibility for the
file or device being opened. The lower-level share checker receives a specific
file object and its associated share-access state. Neither contract grants a
directory open recursive authority over descendant objects.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_descendant_non_exclusion_probe.py`:

1. creates one ordinary `live/candidate.bin` below an NTFS pytest root;
2. reuses M171's unchanged noninheritable zero-sharing directory owner;
3. starts one fixed isolated child that opens only `live/candidate.bin` for
   generic read access with read/write/delete sharing and null security
   attributes;
4. requires the child handle to be noninheritable and consumes exact bounded
   `ready`/`closed` documents around one fixed release byte;
5. acquires the directory first and requires the late descendant holder to
   become ready without changing or releasing that directory owner;
6. starts the descendant holder first and requires the same directory
   acquisition to succeed without changing or releasing the child owner;
7. proves both owners are simultaneously live, candidate bytes remain exact,
   and either owner can close while the other remains live; and
8. settles every parent handle, child process, pipe, and temporary owner with
   fixed bounds and zero leaked ownership.

`tests/fixtures/windows_descendant_file_holder_child.py` accepts no argument,
path, command, or environment value. It opens only the fixed relative file,
emits bounded canonical phase documents, owns one native handle, and never
returns a handle or filesystem path.

## Executed evidence

On the current Windows CPython 3.12 NTFS host, both acquisition orders succeed.
The descendant child remains live while the zero-sharing directory owner is
acquired, and the descendant child can start while that owner is already held.
Each owner closes independently, both child processes exit zero, every parent
owner closes, and both candidate payloads remain unchanged.

## Security consequence

A zero-sharing directory handle is not a subtree lock on the observed host.
Using it alone as cleanup authority would leave descendant readers and writers
outside the proven exclusion boundary. Any later design must explicitly bind
participants or generations, maintain complete retained roots, and revalidate
them at the mutation point.

M172 remains negative capability evidence. It does not define that participant
protocol or prove write/delete handles, mappings, descendant directories,
multiple participants, oplocks, leases, cancellation, process death, native
close failure, filesystem variation, recovery, policy, receipts, or installed-
host behavior.

## Scope and CI restraint

M172 adds no runtime subprocess or `ctypes`, adapter, lock, public probe, cache
access, candidate disclosure, cleanup authority, mutation command, dependency,
native extension, compiler requirement, API, workflow, job, permission, or CI
allocation. The fixture participates only in the existing Windows test suite;
no hosted check is added.

## References

- [Microsoft: `CreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)
- [Microsoft: `IoCheckShareAccess`](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-iocheckshareaccess)
- [M147 cleanup threat model](cache-cleanup-threat-model.md)
- [M171 exclusive-root acquisition probe](cache-cleanup-windows-exclusive-root-acquisition-probe.md)
