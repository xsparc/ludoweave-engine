# Windows cache-cleanup junction-refusal probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M150
- **Date:** 2026-08-28
- **Baseline:** M149's owned-handle capability probe

## Decision

Retain one Windows-only, test-only directory-junction fixture that executes
M149's reparse-refusal path without symbolic-link creation privilege. Bind the
observation to filesystem information queried from the already-open pytest root
handle.

This narrows one evidence gap only. Windows is not admitted because one NTFS
directory junction does not establish symbolic-link, mounted-folder,
unknown-tag, other-filesystem, race, recovery, or policy safety.

## Why a junction is useful evidence

Microsoft documents directory junctions as reparse points and documents
`mklink /j` as the Windows command for creating one. Microsoft also documents
that applications opening reparse points should use
`FILE_FLAG_OPEN_REPARSE_POINT`, and that filesystem type and capability flags
can be queried from an existing handle with `GetVolumeInformationByHandleW`.

M150 therefore uses the operating system's supported junction creator only for
a trusted pytest fixture. The cleanup probe still performs the security-relevant
open and classification through the M149 retained-handle chain.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_junction_probe.py`:

1. creates ordinary `live` and `target` directories below one pytest-owned
   temporary root;
2. writes one marker inside the target;
3. opens the temporary root with M149's owned native probe;
4. queries the opened root with `GetVolumeInformationByHandleW` and continues
   only for NTFS with the reparse-support flag;
5. sets the trusted `live` fixture as the process working directory and invokes
   `cmd.exe /d /c mklink /j` with fixed literal component arguments, so no
   absolute fixture path enters command parsing;
6. confirms the created object is a directory junction;
7. opens the junction relative to the retained `live` handle with final-
   component reparse processing suppressed;
8. requires reparse-attribute refusal and immediate closure of the rejected
   handle; and
9. removes the junction entry explicitly, then proves the target marker remains
   unchanged and all owned native handles close.

The module is skipped outside Windows and excluded from the wheel. It is not a
runtime fallback, capability API, or admission decision.

## Executed evidence

On the current Windows 10.0.26200 CPython 3.12 host, the pytest root's opened
handle reports `NTFS` and `FILE_SUPPORTS_REPARSE_POINTS`. Junction creation
succeeds without elevation. M149's relative open returns the junction object,
its reparse attribute is refused, the rejected handle closes, explicit junction
removal leaves the target marker intact, and the focused test passes.

The first implementation run passed before static acceptance but had typing and
lint defects. After those were corrected, a symbol lookup through the loaded
library's instance dictionary failed because `ctypes` resolves functions
lazily. The accepted helper resolves the named function through normal dynamic
attribute lookup, after which static checks and the probe pass.

## Missing admission evidence

Windows admission still requires:

- executed file and directory symbolic links, volume-mounted folders,
  unknown Microsoft and third-party reparse tags, and all-component
  substitution cases;
- NTFS variation plus ReFS, Dev Drive, removable-media, and supported remote-
  share behavior, with fail-closed treatment everywhere else;
- concurrent namespace replacement, hard-link policy, share-mode, oplock,
  file-ID reuse, cross-process exclusion, and stress evidence;
- crash, cancellation, disk-full, denial, retry, restore, and finalize evidence;
- a reviewed private adapter ABI and typed error boundary;
- complete retained roots, quiescence, policy, trusted time, bounded receipts,
  and recovery; and
- installed-wheel proof on independent supported Windows hosts.

The earlier privilege-skipped symbolic-link case remains missing evidence. A
directory junction is not a substitute for every reparse implementation.

## Scope and CI restraint

M150 adds no runtime `ctypes`, shell invocation, adapter, public probe, cache
access, candidate disclosure, cleanup authority, mutation command, dependency,
native extension, compiler requirement, API, workflow, job, permission, or CI
allocation. The fixture participates only in the existing Windows test suite;
no hosted check is added.

## References

- [Microsoft: hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Microsoft: `mklink`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mklink)
- [Microsoft: reparse points and file operations](https://learn.microsoft.com/en-us/windows/win32/fileio/reparse-points-and-file-operations)
- [Microsoft: `GetVolumeInformationByHandleW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getvolumeinformationbyhandlew)
- [M149 Windows capability probe](cache-cleanup-windows-capability-probe.md)
