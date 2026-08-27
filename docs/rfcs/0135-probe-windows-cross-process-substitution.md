# RFC-0135: probe Windows cross-process retained-parent substitution

- **Status:** Accepted
- **Milestone:** M152
- **Date:** 2026-08-28

## Summary

Add one test-only NTFS fixture in which a child command process renames a
directory and replaces its former name with a junction while the parent process
retains the original directory handle. Preserve the no-admission decision and
add no runtime or CI surface.

## Context

M151 proves a retained directory handle stays bound after same-process rename
and junction substitution. It does not execute the namespace change from a
separate process or prove that M149's all-sharing open permits that process to
perform the rename while the parent keeps the handle open.

Microsoft documents that `FILE_SHARE_DELETE` permits later opens that request
delete access, which includes rename, and that sharing remains effective until
the handle closes regardless of process context. Microsoft also documents
`cmd /d /c`, success-gated `&&`, directory `ren`, and `mklink /j`. One fixed
child command can therefore execute a deterministic cross-process substitution
without adding scheduling or production behavior.

## Decision

Accept the [Windows cross-process substitution
probe](../security/cache-cleanup-windows-cross-process-substitution-probe.md)
as current-host, test-only feasibility evidence.

The parent fixture must open and retain an ordinary directory beneath an NTFS
pytest root. A child `cmd.exe` process must receive no retained native handle
and may execute only the fixed relative command
`ren live displaced && mklink /j live target` from that trusted root. After the
child exits successfully, the parent must refuse a fresh root-relative open of
the junction, preserve the retained directory identity, and distinguish its
candidate from the same-named target candidate. Cleanup may remove only the
junction entry and must preserve both files.

Do not add polling, sleeps, concurrent timing, handle inheritance, runtime
shelling, production `ctypes`, a platform adapter, public capability value,
cleanup authority, dependency, workflow, or Windows admission.

## Consequences

The current host now executes one namespace substitution from a distinct child
process while the parent retains a non-inherited directory handle. The child
can rename the shared-open directory and install a junction. The parent still
rejects the rebound name and reaches the renamed original through its retained
handle.

This is cross-process namespace-change evidence, not concurrency, exclusion,
locking, or platform admission. The parent waits for one child command; there
is no controlled race, overlap at a chosen native call, competing cleanup,
oplock, lease, quiescence, or inherited-handle behavior. Filesystem variation,
recovery, policy, receipts, and independent hosts remain open.

Windows is not admitted.

## Alternatives considered

- Treat M151's same-process substitution as cross-process evidence. Rejected
  because the mutating operation never leaves the parent process.
- Add sleeps or unsynchronized worker processes. Rejected because timing does
  not prove a controlled interleaving and would make the fixture flaky.
- Inherit the retained handle into the child. Rejected because the question is
  whether an independent namespace actor can mutate while the parent owns it.
- Add a dedicated hosted job. Rejected because the existing Windows suite can
  execute this source test after the unpublished stack is safely integrated.
- Implement the runtime adapter. Rejected because M147's wider admission and
  recovery requirements remain incomplete.

## Validation

Focused validation must prove handle-bound NTFS/reparse capability, a fixed
non-inheriting child command, successful cross-process rename plus junction
creation, fresh-name refusal, retained/original-versus-target identity,
deterministic close, target preservation, and link-only cleanup. Architecture
tests must preserve M151, runtime, scripts, dependencies, workflows, and wheel
contents. Supported-Python, full regression, installed-wheel, reproducibility,
release, documentation, governance, and findings-first gates remain required.

## References

- [`CreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)
- [Process handle inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance)
- [`CreateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa)
- [`cmd`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd)
- [`ren`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ren)
- [`mklink`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mklink)
- [Python `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [RFC-0134](0134-probe-windows-retained-parent-substitution.md)
