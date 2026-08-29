# RFC-0167: probe Windows hard-link alias deletion non-exclusion

- **Status:** Accepted
- **Milestone:** M184
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe showing that M181's matching
expected-identity guardian does not exclude removal of a peer hard-link entry.
The guardian continues protecting the exact pathname it opened while the
alias is deleted and the link count falls from two to one. Preserve this as a
negative ownership boundary. Add no runtime or CI surface.

## Context

M182 shows that a peer hard-link alias can be renamed while the guardian
protects the exact pathname it opened. M183 shows that a peer alias can be
created after admission. Alias deletion remained unresolved.

Microsoft documents `DeleteFileW` as failing when another handle opened the
file for normal I/O without `FILE_SHARE_DELETE`, and documents hard links as
independent names which can be deleted in any order. Python documents
`os.remove` and the identical `os.unlink` operation as raising on Windows when
the file is in use. These broad descriptions did not determine whether this
guardian's share mode blocks removal through a different hard-link entry, so
the behavior required a controlled observation.

## Decision

Accept the [Windows hard-link alias deletion non-exclusion
probe](../security/cache-cleanup-windows-hard-link-alias-deletion-non-exclusion-probe.md)
as current-host, test-only negative evidence.

Create M173's ordinary coordination file and a peer hard-link alias before
guardian launch. Open both through the existing capability helper, retain the
shared `FILE_ID_INFO`, require both link counts to equal two, and close those
initial handles. Start M181's matching guardian and require exact `ready`.

While the guardian remains live, reopen the original through the capability
helper and first require rename of the exact coordination pathname to fail
with Windows sharing error 32. Delete the peer entry with `Path.unlink`.
Require that entry to be absent, the guardian to remain live, the original
bytes to remain exact, and the retained original handle to report link count
one. Require exclusive byte-range availability and a second exact-name rename
failure with error 32.

After the exact release token, require `closed`. Reopen the original, require
the same identity and link count one, then rename that entry successfully.
Require the displaced entry to retain identity, link count one, exact bytes,
and complete process, stream, native-handle, and range cleanup. Use no retry
or sleep.

The initial hypothesis expected `Path.unlink` to raise sharing error 32 while
the guardian was live. The first focused live run falsified that hypothesis:
the alias entry was removed. The accepted test and documentation preserve the
narrower observed deletion non-exclusion instead of converting documentation
language into a stronger claim.

## Consequences

On the observed host, the guardian's protection of one opened pathname does
not exclude removal of another entry naming the same file. Link removal is not
excluded, even though the guardian remains live and continues rejecting
rename of the exact name it opened. Identity match and a later link count of
one are therefore not root-confined ownership.

This compounds M182 and M183. A future Windows cleanup design must define
trusted-root authorization, multiple-link policy, use-time identity and link
count revalidation, and the disposition of links created or removed across
admission and use. A count of one after alias deletion does not prove that an
unknown alias cannot exist or that a new alias cannot immediately be created.
M184 does not make that policy decision.

This result does not prove behavior for another process or principal,
enumerate links, authenticate either directory, cover POSIX-delete flags,
cross a volume, or establish identical behavior on ReFS, SMB, other drivers,
Windows versions, or independent hosts. It does not authorize mutation.

Windows remains unadmitted. Trusted identity and generation provenance,
durable state, root placement, link enumeration, link-count policy,
simultaneous owner loss, failed launch, file-ID reuse, hostile handles,
arbitrary process trees, mapped views, recovery, fail-closed policy, typed
receipts, and independent-host proof remain open.

No runtime API, adapter, public probe, production subprocess or `ctypes`, cache
access, cleanup authority, dependency, workflow, permission, or hosted check
is added.

## Alternatives considered

- Infer that no-delete sharing blocks every hard-link deletion. Rejected
  because the live observation disproves the initial hypothesis on the current
  host.
- Add native alias deletion to the runtime. Rejected because standard-library
  `Path.unlink` is sufficient for this test and production cleanup is
  unadmitted.
- Treat the surviving one-link state as ownership admission. Rejected because
  links are not enumerated or frozen and trusted root, recovery, receipt, and
  compatibility behavior are not designed.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  will collect this source test after its prerequisite stack is integrated.

## Validation

Focused validation must prove the pre-launch shared identity and two-link
state, matching guardian admission, exact-name sharing refusal, successful
alias deletion, guardian liveness, exact one-link reduction, retained bytes,
range availability, persistent exact-name refusal, exact close, post-close
rename, retained identity, and complete cleanup.

Architecture tests must preserve M183, runtime, examples, scripts,
dependencies, workflows, and the wheel package boundary. Supported-Python,
full regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [Microsoft: `DeleteFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-deletefilew)
- [Microsoft: Hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Python: `os.remove` and `os.unlink`](https://docs.python.org/3/library/os.html#os.remove)
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [NIST Secure Software Development Framework publications](https://csrc.nist.gov/Projects/ssdf/publications)
- [RFC-0166](0166-probe-windows-post-admission-hard-link-creation.md)
