# RFC-0136: probe Windows cross-process share-delete exclusion

- **Status:** Accepted
- **Milestone:** M153
- **Date:** 2026-08-28

## Summary

Add one test-only NTFS fixture in which a parent process retains a directory
handle opened without delete sharing. Require a fixed child command to fail to
rename that directory while the handle is open and require the identical
command to succeed after deterministic close. Preserve the no-admission
decision and add no runtime or CI surface.

## Context

M152 proves that a separate process can rename a directory whose retained
parent handle allows all documented sharing modes. It does not execute the
complementary exclusion case or show that closing the non-sharing handle
releases the block.

Microsoft documents that a handle's sharing options remain in effect until the
handle closes regardless of process context. `FILE_SHARE_DELETE` permits later
opens that request delete access, and delete access includes rename. Omitting
that share flag should therefore prevent a separate process from completing a
rename that requires delete access while the handle remains open.

## Decision

Accept the [Windows share-delete exclusion
probe](../security/cache-cleanup-windows-share-delete-exclusion-probe.md) as
current-host, test-only feasibility evidence.

The fixture must open an ordinary `live` directory beneath an NTFS pytest root
with read and write sharing but without delete sharing. A child `cmd.exe`
process must receive no retained native handle and may execute only the fixed
relative command `ren live displaced` from that trusted root. The first child
invocation must return nonzero while `live` and its candidate remain unchanged.
After the parent closes the blocking handle, the identical child invocation
must succeed and the candidate must be reachable only under `displaced`.

Do not parse localized command output or claim an exact native error code from
the child. Do not add polling, sleeps, concurrent timing, handle inheritance,
runtime shelling, production `ctypes`, a platform adapter, public capability
value, cleanup authority, dependency, workflow, or Windows admission.

## Consequences

The current host now executes one cross-process share-mode denial and release
transition. The observed namespace remains unchanged while the no-delete-share
handle is open, and the same rename succeeds after that handle closes.

This is exclusion evidence for one fixed command, directory, filesystem, and
host. It is not general cross-process exclusion, quiescence, a controlled race,
an interleaving at a selected native call, an oplock protocol, or platform
admission. Competing readers, writers, publishers, cleanup actors, duplicated
handles, filesystem variation, recovery, policy, receipts, and independent
hosts remain open.

Windows is not admitted.

## Alternatives considered

- Infer exclusion from M152's all-sharing success. Rejected because permitting
  a rename does not execute or observe the complementary denial path.
- Assert `ERROR_SHARING_VIOLATION` from localized `cmd.exe` output. Rejected
  because this fixture observes only the child exit and namespace result, not
  the underlying native error directly.
- Add sleeps or competing unsynchronized workers. Rejected because timing does
  not select a native boundary and would make the fixture flaky.
- Add a dedicated hosted job. Rejected because the existing Windows suite can
  execute this source test after the unpublished stack is safely integrated.
- Implement a runtime lock or cleanup adapter. Rejected because M147's wider
  admission and recovery requirements remain incomplete.

## Validation

Focused validation must prove NTFS binding, omission of delete sharing, a fixed
non-inheriting child command, failed rename with unchanged content, explicit
handle release, successful identical rename after release, and deterministic
close. Architecture tests must preserve M152, runtime, examples, scripts,
dependencies, workflows, and wheel contents. Supported-Python, full
regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [`CreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)
- [System error codes](https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-)
- [`cmd`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd)
- [`ren`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ren)
- [Python `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [RFC-0135](0135-probe-windows-cross-process-substitution.md)
