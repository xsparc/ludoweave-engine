# RFC-0133: probe Windows directory-junction refusal

- **Status:** Accepted
- **Milestone:** M150
- **Date:** 2026-08-28

## Summary

Add one test-only NTFS directory-junction fixture to execute M149's reparse-
refusal path on the current non-administrator host. Preserve the no-admission
decision and add no runtime or CI surface.

## Context

M149 requested final-component reparse suppression and implemented explicit
attribute refusal, but its symbolic-link fixture skipped because this host lacks
symbolic-link creation privilege. Microsoft documents directory junctions as
reparse points and supplies `mklink /j` for their creation. The opened pytest
root can also report its filesystem and capability flags directly through
`GetVolumeInformationByHandleW`.

One bounded junction fixture can therefore exercise the refusal branch without
weakening M149's private-handle boundary. It cannot establish safety for other
reparse tags, filesystems, or namespace races.

## Decision

Accept the [Windows junction-refusal
probe](../security/cache-cleanup-windows-junction-probe.md) as current-host,
test-only feasibility evidence.

The fixture may invoke only the fixed Windows `mklink /j` command from a trusted
pytest working directory with fixed literal component arguments. It must first
bind the observation to an opened root handle reporting NTFS and reparse
support. The M149 probe must open the junction relative to a retained parent
handle, refuse its reparse attribute, close the rejected handle, remove only
the junction entry, and prove the target remains unchanged.

Do not add runtime shelling, production `ctypes`, a platform adapter, public
capability value, cleanup command or authority, dependency, workflow, or
Windows admission.

## Consequences

The current host now executes one real reparse-refusal case without elevation.
This shows that M149's final-component suppression plus attribute check can
observe and reject an NTFS directory junction rather than traverse it. Explicit
junction removal leaves the target marker intact.

The result remains narrower than platform admission. The symbolic-link case is
still privilege-skipped, and mounted folders, unknown tags, other filesystems,
all-component substitution, concurrency, recovery, policy, receipts, and
independent hosts remain open.

Windows is not admitted.

## Alternatives considered

- Treat the skipped symbolic-link case as sufficient. Rejected because a skip
  is not security evidence.
- Set a reparse point directly through `DeviceIoControl`. Rejected for this
  slice because Microsoft documents privilege and filesystem variation for
  that lower-level operation, while the supported junction command provides a
  smaller fixture boundary.
- Add a runtime adapter. Rejected because the wider M147 admission gate remains
  incomplete.
- Add a dedicated hosted job. Rejected because the test can run in the existing
  Windows matrix after the unpublished stack is safely integrated.

## Validation

Focused validation must prove handle-bound NTFS/reparse capability observation,
junction creation, no-follow relative open, reparse refusal, rejected-handle
closure, target preservation, and explicit link-only cleanup. Architecture
tests must preserve M149, runtime, scripts, dependencies, workflows, and wheel
contents. Complete supported-Python, installed-wheel, reproducibility, release,
documentation, governance, and findings-first gates remain required.

## References

- [Hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [`mklink`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mklink)
- [Reparse points and file operations](https://learn.microsoft.com/en-us/windows/win32/fileio/reparse-points-and-file-operations)
- [`GetVolumeInformationByHandleW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getvolumeinformationbyhandlew)
- [RFC-0132](0132-probe-windows-cache-cleanup-capability.md)
