# RFC-0132: probe Windows cache-cleanup capability

- **Status:** Accepted
- **Milestone:** M149
- **Date:** 2026-08-28

## Summary

Add one test-only Windows native-capability probe to reduce uncertainty around
M148's prospective platform adapter. Preserve the no-admission decision: the
probe is feasibility evidence, not runtime cleanup or a supported capability.

## Context

RFC-0131 rejected a portable standard-library implementation and required
private platform adapters plus real-host adversarial evidence. The current
Windows host can contribute a bounded first experiment without weakening that
gate or spending another hosted workflow allocation.

Microsoft documents user-mode `NtCreateFile` with directory-handle-relative
names and final-component reparse suppression. Handle queries expose stable
comparison material for open objects, and native file-information operations
can rename or dispose the object represented by a DELETE-authorized handle.
Exact supported CPython runtimes expose the required system entry points, but
symbol availability alone is not admission.

## Decision

Accept the [Windows cache-cleanup capability
probe](../security/cache-cleanup-windows-capability-probe.md) as test-only
feasibility evidence.

The probe may create, hard-link, rename, and delete only files beneath a
pytest-owned temporary directory. It must retain native handles privately,
accept only single relative components, refuse reparse components, avoid
replacement, preserve identity across quarantine, and close owned handles
deterministically. It must be skipped outside Windows and excluded from the
installed wheel.

Do not add a production adapter, `ctypes` import under `src/ludoweave`, public
capability flag, command, cleanup authority, dependency, workflow, or platform
admission. A privilege-dependent reparse skip remains missing evidence, not a
pass for that threat.

## Consequences

The executed probe establishes that one current Windows host can open ordinary
components relative to a root handle while requesting the documented
final-component reparse-suppression option, inspect identity and hard-link
count, move the same opened identity to a retained destination without
replacement, reopen it by the quarantined name, and apply deletion disposition.
It also records that the initially selected Win32 rename class returned error
87 while the explicit native `FileRenameInformation` path succeeded. The
privilege-skipped reparse case is not evidence that suppression or refusal
worked against a reparse point.

This reduces ABI uncertainty but increases the proof burden: a future runtime
adapter would own a Native System Services boundary rather than rely solely on
portable Python or high-level Win32 calls. ABI layout, NTSTATUS mapping,
filesystem support, and close ordering require dedicated review.

Windows is not admitted. Reparse/junction execution, namespace races,
cross-process exclusion, filesystem coverage, crash recovery, policy,
quiescence, durable receipts, and installed independent-host proof remain open.

## Alternatives considered

- Implement the runtime adapter now. Rejected because M147's adversarial and
  recovery gates remain incomplete.
- Add a public boolean probe. Rejected because one successful host experiment
  cannot authorize mutation on another filesystem or host.
- Add a dedicated GitHub Actions job. Rejected because the existing Windows
  test matrix will already execute the test when the unpublished stack is
  safely integrated; another allocation would duplicate evidence and consume
  quota.
- Keep only documentation research. Rejected because the current host can
  safely produce stronger, bounded, temporary-directory evidence.

## Validation

Focused validation must execute the Windows handle chain, identity and
hard-link checks, collision refusal, single-component validation, close
semantics, and the privilege-gated reparse case. Architecture tests must prove
that native imports remain test-only and that runtime, scripts, dependencies,
workflows, and M148's boundary are unchanged. Complete supported-Python,
installed-wheel, reproducibility, release, documentation, governance, and
findings-first gates remain required before closeout.

## References

- [`NtCreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/winternl/nf-winternl-ntcreatefile)
- [`NtSetInformationFile`](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/nf-ntifs-ntsetinformationfile)
- [`FILE_RENAME_INFORMATION`](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/ns-ntifs-_file_rename_information)
- [`GetFileInformationByHandleEx`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex)
- [`SetFileInformationByHandle`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfileinformationbyhandle)
- [RFC-0130](0130-asset-cache-cleanup-threat-model.md)
- [RFC-0131](0131-defer-portable-cache-cleanup-capability.md)
