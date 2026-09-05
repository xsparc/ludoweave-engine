# RFC-0134: probe Windows retained-parent substitution safety

- **Status:** Accepted
- **Milestone:** M151
- **Date:** 2026-08-28

## Summary

Add one test-only NTFS namespace-substitution fixture to execute a retained-
parent handle after the parent's former name is replaced by a directory
junction. Preserve the no-admission decision and add no runtime or CI surface.

## Context

M149 demonstrates component-by-component relative opens through retained
directory handles. M150 executes junction refusal for a fresh final-component
open. Neither directly proves what the retained M149 parent handle addresses
after its directory entry is renamed and the old name is rebound to a junction.

Microsoft documents that an opened file object persists until its handles
close, that `OBJECT_ATTRIBUTES.RootDirectory` makes a name relative to an
existing directory handle, that delete sharing permits later rename access,
and that volume serial plus file ID compares open-object identity. One bounded
same-process substitution can therefore test the intended binding without
introducing timing or production behavior.

## Decision

Accept the [Windows retained-parent substitution
probe](../security/cache-cleanup-windows-retained-parent-substitution-probe.md)
as current-host, test-only feasibility evidence.

The fixture must open and retain an ordinary parent beneath an NTFS pytest
root, rename that parent, replace its former name with a fixed directory
junction, and then compare opened-object identities. A fresh root-relative open
must refuse the junction. An open relative to the retained parent must identify
the file under the renamed original directory and must differ from the file in
the substitution target. Cleanup may remove only the junction entry and must
prove both files remain unchanged.

Do not add concurrent timing, runtime shelling, production `ctypes`, a platform
adapter, public capability value, cleanup command or authority, dependency,
workflow, or Windows admission.

## Consequences

The current host now executes one deterministic namespace-substitution case:
the retained parent remains bound to the renamed directory object, while a
fresh open of the rebound name observes and refuses the junction. Exact file
identity distinguishes the original candidate from the target candidate.

The result is not a race, locking, or platform-admission proof. It does not
establish concurrent interleavings, ancestor replacement before acquisition,
oplock/share stress, other reparse tags or filesystems, cross-process
exclusion, identity reuse, recovery, policy, receipts, or independent hosts.

Windows is not admitted.

## Alternatives considered

- Infer retained-handle behavior from API documentation. Rejected because the
  current host can safely provide stronger executed evidence.
- Add sleeps and a competing thread. Rejected because timing-dependent tests
  would not prove a controlled interleaving or cross-process exclusion.
- Implement the runtime adapter. Rejected because M147's broader admission and
  recovery requirements remain incomplete.
- Add a dedicated hosted job. Rejected because the existing Windows matrix will
  execute the test after the unpublished stack is safely integrated.

## Validation

Focused validation must prove handle-bound NTFS/reparse capability, retained-
parent identity before and after rename, fixed junction substitution, fresh-
name refusal, original-versus-target file identity, deterministic handle close,
target preservation, and link-only cleanup. Architecture tests must preserve
M150, runtime, scripts, dependencies, workflows, and wheel contents. Complete
supported-Python, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [Opening a handle to a file](https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/opening-a-handle-to-a-file)
- [`OBJECT_ATTRIBUTES`](https://learn.microsoft.com/en-us/windows/win32/api/ntdef/ns-ntdef-_object_attributes)
- [`NtCreateFile`](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/nf-ntifs-ntcreatefile)
- [`CreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)
- [`FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [RFC-0133](0133-probe-windows-junction-refusal.md)
