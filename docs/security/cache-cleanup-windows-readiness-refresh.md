# Windows cache-cleanup readiness refresh

- **Status:** Accepted decision
- **Milestone:** M199
- **Date:** 2026-08-30

## Decision

Windows is not admitted for asset-cache cleanup. The M149-M198 current-host
probe sequence is complete as a 50-milestone threat-model evidence set, but it
does not supply production cleanup authority. M199 consolidates what that set
proves and retains the M146-M148 deferral. The method-by-method closed-stream
probe tail is closed.

A future milestone must resolve a named admission criterion. Another isolated
stream inquiry, exception disposition, share-mode result, or same-principal
fixture observation is insufficient unless it directly closes one of the
criteria in this decision and retains every earlier boundary.

M199 is a no-authority-increase decision. It adds no cleanup command, adapter,
native implementation, cache access, mutation, dependency, workflow,
permission, release effect, or hosted allocation.

## Evidence reviewed

| Milestones | Evidence family | Bounded result |
| --- | --- | --- |
| M149-M154 | capability, namespace substitution, share-delete, and native sharing | Windows exposes useful handle-relative identity and sharing primitives, but portable CPython does not provide the complete safe mutation chain. |
| M155-M170 | child ownership, control settlement, duplicated/inherited handles, and concurrent launch failure | Parent-owned subprocess and handle cleanup can be bounded for the exact fixtures; this is not authorization or hostile-process isolation. |
| M171-M181 | root acquisition, cooperative ranges, guardian handoff/rotation, and expected identity | An expected-identity guardian can retain an exact local object under cooperative same-principal conditions; descendants and aliases require separate treatment. |
| M182-M198 | hard-link aliases, delete/recreate substitution, guardian protection, mutator settlement, and closed-stream disposition | Aliases remain the same file, sharing protection does not exclude every alias operation, and late control delivery has concrete local failure states. These results do not create a secure cleanup protocol. |

The evidence is test-only and tied to one current host, NTFS, three or fewer
cooperating processes per probe, one principal, and parent-owned process trees.
The architecture tests preserve the exact M149-M198 milestone inventory and
the 50 corresponding Windows integration and security records.

## What the evidence establishes

- Windows file handles can expose stable identity and link-count observations
  for the exact opened objects used by the probes.
- Share modes and cooperative byte ranges can retain particular handles and
  reject particular exact-name operations while matching participants remain
  live.
- Explicit handle lists, bounded control channels, exact settlement, and
  parent-owned cleanup avoid the tested inheritance and liveness leaks.
- Hard links are multiple names for one file. Creating, deleting, and
  recreating an alias can change namespace and link count without changing the
  original open file identity.
- The concrete buffered subprocess stream has the M194-M198 delivery, close,
  flush, and write dispositions recorded by those milestones.

These are implementation observations, not a portable API guarantee. The
closed-stream sequence does not establish portable behavior and does not
establish native-call suppression. It supplies no acknowledgement from the
settled child and no cleanup authority.

## Unresolved admission criteria

Windows cleanup remains unimplemented and unauthorized until one coherent
design and adversarial validation supply all of the following:

1. **Authenticated authority and trusted root.** Bind every request to an
   authenticated project/cache identity, an owned trusted root, a durable
   generation, and a least-privilege actor. Same-principal cooperation is not
   an authorization model.
2. **Complete hard-link policy.** Define whether candidates with multiple
   links are refused or quarantined. If enumeration is used, hard-link
   enumeration must be bounded, root-confined, and treated as a changing
   observation rather than proof that no other name exists.
3. **Use-time identity and link-count revalidation.** Hold an exact admitted
   object through mutation, re-check volume/file identity, link count, type,
   root relationship, and generation immediately at the mutation boundary,
   and fail closed on any mismatch.
4. **Explicit protocol and acknowledgement.** Use typed, versioned, bounded
   messages and typed receipts. Local buffered-write acceptance is not peer
   delivery, acknowledgement, authorization, or commit.
5. **Durable intent and recovery.** Record durable intent before mutation,
   stage same-filesystem quarantine, define crash and power-loss behavior, and
   provide idempotent recovery, reconciliation, and rollback-tamper handling.
6. **Cross-principal adversarial evidence.** Test a distinct untrusted local
   principal, unrelated processes and sessions, hostile simultaneous racing,
   ACL changes, inherited handles, aliases, reparse points, and denial paths.
7. **Independent-host proof.** Reproduce the complete admitted design on
   independent supported Windows hosts and versions. ReFS, SMB, CSVFS,
   cross-volume behavior, file-ID reuse, and unsupported capability refusal
   need explicit classification.

No single probe can substitute for this joint design. Failure to prove any
criterion keeps cleanup disabled and unavailable through public APIs or CLI.

## Closed-stream investigation boundary

The M194-M198 sequence distinguishes local buffer acceptance, failed delivery,
first and repeated close, closed flush, and closed write for one concrete
`Popen.stdin` stream. Python documents closed-stream method behavior as
implementation-dependent, including inquiries. Therefore `writable()`,
`fileno()`, `seekable()`, `isatty()`, larger or repeated writes, exact messages,
and raw/native tracing are not accepted as standalone follow-on milestones.

This does not prohibit a future diagnostic needed by an approved protocol. It
requires that diagnostic to name the admission criterion it resolves, explain
why existing evidence is insufficient, and preserve the no-authority boundary
until the complete design passes.

## CI and publication boundary

M199 changes only source documentation and one architecture guard. Existing
local supported-Python, documentation, package, release-rehearsal, governance,
and diff checks remain the acceptance path. The existing Windows suite remains
the only future hosted execution path for the preserved probes; no hosted check
is added.

No workflow, job, matrix entry, permission, cache, artifact retention setting,
credential, tag, release, package publication, or remote cleanup effect is
authorized. Least-privilege workflow defaults remain unchanged.

## References

- [Microsoft: hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Microsoft: file security and access rights](https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights)
- [Microsoft: file identity and link count](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/ns-fileapi-by_handle_file_information)
- [Microsoft: `GetFileInformationByHandleEx`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex)
- [Python: core I/O tools](https://docs.python.org/3/library/io.html)
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)
- [NIST SP 800-218 Rev. 1 initial public draft](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd)
- [SLSA 1.2 specification](https://slsa.dev/spec/v1.2/)
- [RFC-0182](../rfcs/0182-refresh-windows-cache-cleanup-readiness.md)
