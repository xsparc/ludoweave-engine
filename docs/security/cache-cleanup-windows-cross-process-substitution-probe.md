# Windows cache-cleanup cross-process substitution probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M152
- **Date:** 2026-08-28
- **Baseline:** M151's same-process retained-parent substitution probe

## Decision

Retain one Windows-only, test-only cross-process namespace-substitution fixture.
It verifies what the parent process's retained directory handle addresses after
a child process renames the directory and rebinds its former name to a junction.
The result is feasibility evidence, not cleanup authority or platform admission.

## Why a process boundary matters

M151 executes a controlled namespace change but performs the rename in the
same Python process that owns the retained handle. M149 opens with all three
documented share modes. Microsoft states that `FILE_SHARE_DELETE` permits later
delete-access opens, including rename, and that a handle's sharing options stay
in effect until close regardless of process context.

M152 therefore gives the namespace mutation to a distinct `cmd.exe` process.
Python's `close_fds=True` prevents the retained native handle from being passed
to the child; only captured standard streams are redirected. The test observes
the parent's handle after the child exits. It does not claim simultaneous
execution at a selected native boundary or mutual exclusion.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_cross_process_probe.py`:

1. creates ordinary `live` and `target` directories below one pytest-owned
   temporary root, with distinct same-named candidate contents;
2. opens the root and requires handle-bound NTFS plus reparse support;
3. opens and retains `live`, records its directory identity, and keeps that
   handle private to the parent process;
4. starts one child `cmd.exe` directly with `shell=False`, `close_fds=True`, a
   bounded timeout, the trusted pytest root as its working directory, and only
   the fixed command `ren live displaced && mklink /j live target`;
5. requires successful child exit, an ordinary `displaced` directory, a
   junction at `live`, and unchanged retained-parent identity;
6. requires a fresh root-relative `live` open to refuse the junction;
7. opens `candidate.bin` through the retained parent, the fresh `displaced`
   name, and the ordinary `target` parent;
8. proves retained and displaced opens identify the original file and differ
   from the target file;
9. closes all seven accepted native handles deterministically; and
10. removes only the junction entry and proves both files remain unchanged.

No caller-derived path, environment value, or candidate name enters the child
command string. The module is skipped outside Windows, excluded from the wheel,
and imports only retained test support.

## Executed evidence

On the current Windows 10.0.26200 CPython 3.12 host, the opened pytest root
reports NTFS and reparse support. The fixed child command renames the directory
while its non-inherited handle remains open in the parent and creates the
junction without elevation. After child exit, the parent refuses the fresh name
while its retained handle identifies the original file under `displaced`, not
the target. Link-only cleanup preserves both contents.

## Missing admission evidence

Windows admission still requires:

- controlled concurrent and cross-process interleavings at every acquisition
  and mutation boundary, including explicit synchronization and oplock/share
  behavior;
- demonstrated exclusion or quiescence against competing readers, writers,
  publishers, cleanup actors, and handle duplication or inheritance;
- ancestor substitution before acquisition, mounted folders, symbolic links,
  unknown tags, and every supported component depth;
- NTFS variation plus ReFS, Dev Drive, removable media, remote shares, and safe
  refusal for every unsupported filesystem;
- hard-link policy, file-ID reuse, leases, pins, and publication interleavings;
- crash, cancellation, timeout, disk-full, denial, retry, restore, and finalize
  evidence;
- an accepted private adapter ABI with bounded backend-neutral errors; and
- candidate, retained-root, policy, trusted-time, durable receipt, and recovery
  designs plus independent installed-host proof.

## Scope and CI restraint

M152 adds no runtime subprocess or `ctypes`, adapter, public probe, cache access,
candidate disclosure, cleanup authority, mutation command, dependency, native
extension, compiler requirement, API, workflow, job, permission, or CI
allocation. The fixture participates only in the existing Windows test suite;
no hosted check is added.

## References

- [Microsoft: `CreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)
- [Microsoft: process handle inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance)
- [Microsoft: `CreateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa)
- [Microsoft: `cmd`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd)
- [Microsoft: `ren`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ren)
- [Microsoft: `mklink`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mklink)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [M151 retained-parent probe](cache-cleanup-windows-retained-parent-substitution-probe.md)
