# Windows cache-cleanup capability probe

- **Status:** Accepted feasibility evidence; Windows is not admitted for cleanup
- **Milestone:** M149
- **Date:** 2026-08-28
- **Baseline:** M148's platform-capability decision

## Decision

Retain one test-only Windows native-capability probe. It demonstrates a narrow
owned-handle chain on the current host without adding a runtime adapter,
cleanup command, public probe, or Windows support claim.

The result is promising but incomplete. Windows remains unadmitted because the
probe does not yet establish reparse behavior on this host, filesystem coverage,
cross-process exclusion, race safety, recovery, durable receipts, or the policy
and retained-root requirements from M146 and M147.

## Why this path is technically plausible

Python's portable `os` surface still supplies no Windows directory-descriptor
mutation chain. The documented Windows native surface is materially different:

- user-mode [`NtCreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/winternl/nf-winternl-ntcreatefile)
  can resolve a name relative to a preceding directory handle and can open the
  final reparse point without normal reparse processing;
- [`FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
  combines a volume serial number and 128-bit file identifier to compare two
  open handles on one computer;
- [`NtSetInformationFile`](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/nf-ntifs-ntsetinformationfile)
  accepts `FileRenameInformation` for a DELETE-authorized handle, while
  [`FILE_RENAME_INFORMATION`](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/ns-ntifs-_file_rename_information)
  documents a destination directory handle for a relative new name; and
- [`SetFileInformationByHandle`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfileinformationbyhandle)
  can mark the opened file for deletion when the handle has DELETE access.

Availability does not imply correctness. Microsoft documents filesystem and
operating-system variation for handle information classes, and reparse points
need explicit treatment. M149 therefore records executed feasibility evidence,
not adapter admission.

## Test-only probe contract

`tests/integration/test_windows_cache_cleanup_capability_probe.py` owns every
native handle and closes them in reverse acquisition order. It accepts only one
non-special relative component per native open or rename. Within pytest-owned
temporary directories it exercises:

1. an absolute root open with reparse processing disabled;
2. single-component directory and file opens relative to retained handles;
3. reparse-attribute refusal before a component can become a traversal root;
4. volume/file-identity comparison and hard-link-count observation;
5. non-replacing rename of the opened identity into a retained quarantine
   directory;
6. reopening the quarantined name relative to that directory and proving both
   handles identify the same object;
7. deletion disposition on the already-opened quarantined identity; and
8. deterministic, idempotent close of all probe-owned handles.

The probe is skipped outside Windows. It is not installed in the wheel, has no
engine import, emits no public capability value, and is not a fallback used by
runtime code.

## Executed evidence

Exact CPython 3.12.13, 3.13.13, and 3.14.5 on Windows 10.0.26200 each expose
the required `kernel32` and `ntdll` entry points. On the current CPython 3.12
host, the corrected focused probe passes nine cases. The reparse-component case
is skipped because this non-administrator host does not grant symbolic-link
creation privilege.

The successful chain preserves exact volume/file identity across quarantine,
detects a hard-link alias by equal identity and link count, refuses a populated
destination instead of replacing it, deletes only after disposition and close,
and leaves the test root removable by pytest.

Development evidence also narrowed the ABI boundary: two
`SetFileInformationByHandle(FileRenameInfo)` attempts returned Win32 error 87,
including a same-directory diagnostic. The corrected probe uses the documented
`NtSetInformationFile(FileRenameInformation)` class, after which handle-relative
quarantine succeeds. This is evidence that a production boundary would need
explicit ABI ownership and cannot treat superficially similar calls as
interchangeable.

## Missing admission evidence

Windows admission still requires all of the following:

- executed symbolic-link, junction, mount-point, unknown-reparse-tag, and
  all-component substitution cases without a privilege-dependent skip;
- NTFS, ReFS, Dev Drive, removable-media, and explicitly supported remote-share
  semantics, with safe refusal for every other filesystem;
- concurrent reader/writer, share-mode, oplock, rename race, file-ID reuse,
  hard-link policy, and quarantine-collision stress;
- crash, cancellation, disk-full, access-denial, retry, restore, and finalize
  evidence at every state transition;
- an accepted private adapter ABI and error model, with no raw handle or native
  status entering public APIs, commands, or receipts;
- bounded candidate, retained-root, quiescence, policy, trusted-time, durable
  receipt, and recovery designs; and
- installed-wheel execution on independent supported Windows hosts.

## Scope and CI restraint

M149 adds no production `ctypes`, runtime adapter, cache access, candidate
disclosure, cleanup authority, mutation command, dependency, native extension,
compiler requirement, public API, environment probe, workflow, job, permission,
or CI allocation. The test participates only in the already-required test
suite; no hosted check is added.

## References

- [Python filesystem capability documentation](https://docs.python.org/3/library/os.html#files-and-directories)
- [Windows reparse-point operations](https://learn.microsoft.com/en-us/windows/win32/fileio/reparse-points-and-file-operations)
- [M147 cleanup threat model](cache-cleanup-threat-model.md)
- [M148 platform-capability decision](cache-cleanup-platform-capability-decision.md)
