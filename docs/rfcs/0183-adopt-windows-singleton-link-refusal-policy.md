# RFC-0183: adopt Windows singleton-link refusal policy

- **Status:** Accepted
- **Milestone:** M200
- **Date:** 2026-08-30

## Summary

Resolve M199 admission criterion 2 as policy by refusing every Windows cache-
cleanup candidate unless its retained opened object reports a handle-derived
link count of exactly one both at admission and immediately before mutation.
Zero, multiple, changed, unavailable, invalid, or unsupported counts fail
closed before mutation.

Do not enumerate hard-link names. Win32 name enumeration is pathname-based,
raceable observation rather than authority over every alias. A stable
singleton count is necessary but not sufficient for future cleanup admission.
Windows cleanup remains unimplemented and unauthorized.

## Context

RFC-0129 and RFC-0130 require exact identity, retained-root policy,
quiescence, no-follow mutation, receipts, recovery, and adversarial evidence
before asset-cache cleanup can exist. RFC-0131 rejects partial platform
capability and requires fail-closed engine-owned adapters. M149-M198 then
recorded current-host Windows identity, sharing, guardian, alias, process, and
control observations without adding production authority.

M199 consolidated that evidence into seven admission criteria. Criterion 2
required a complete hard-link refusal or quarantine policy. Windows exposes a
link count on an opened file through `BY_HANDLE_FILE_INFORMATION` and
`FILE_STANDARD_INFO`. Microsoft also documents hard links as multiple names
for one file. The M182-M193 probes demonstrate why pathname protection alone
does not exclude aliases.

Windows also exposes `FindFirstFileNameW`, but that function enumerates names
from a pathname and volume. An enumeration is not an atomic proof that no
other link can exist at later use. Making it authoritative would add changing
path disclosure, bounds, root-classification, ACL, and race questions without
closing the mutation boundary.

## Decision

Adopt the [Windows singleton-link refusal
policy](../security/windows-cache-cleanup-singleton-link-refusal-policy.md).

A future Windows cleanup design may consider a candidate only while all of the
following are true:

1. an engine-owned adapter retains the exact opened object;
2. the adapter obtains the link count from that retained handle, not from a
   pathname or previously saved record;
3. the handle-derived link count equals exactly one at candidate admission;
4. the same retained object reports exactly one again immediately before the
   first quarantine or mutation operation; and
5. every zero, greater-than-one, changed, unavailable, invalid, or unsupported
   result refuses before mutation and produces a future typed failure receipt.

Do not enumerate hard-link names as part of admission or authority. In
particular, do not use `FindFirstFileNameW` to justify cleanup. A later bounded
diagnostic may treat enumeration only as a non-authoritative, changing
pathname-based observation if a separately approved design proves its need,
privacy boundary, confinement, and limits.

This decision resolves M199 criterion 2 as policy only. It does not implement
the production adapter or use-time check, so criterion 3 remains unresolved.
Criterion 1 and criteria 4 through 7 also remain unresolved. A stable link
count of one is necessary but not sufficient: authenticated authority,
trusted-root/generation binding, exact identity and type, use-time root
relationship, protocol acknowledgement, durable recovery, cross-principal
evidence, and independent-host support must still pass together.

This is a direction-preserving refinement under ADR-0017 and RFC-0129 through
RFC-0131. It is a no authority increase decision. Use no new hosted
allocation. Preserve the M149-M199 evidence, runtime, integration fixtures,
examples, scripts, dependencies, metadata, workflows, permissions, and package
surface exactly.

## Consequences

Reviewers now have an unambiguous hard-link rule: candidates with any observed
alias or any uncertain link count are ineligible; enumeration cannot turn them
eligible. The rule avoids an unbounded, pathname-disclosing enumeration
protocol and retains fail-closed behavior.

The decision deliberately accepts false refusals. A filesystem or platform
that cannot provide a trustworthy handle-derived count is unsupported for the
future operation. No pathname fallback, saved-count fallback, quarantine of
multi-link objects, or best-effort deletion is accepted.

M200 adds one architecture guard and source documentation. It adds no
production adapter, runtime API, command, protocol, decoder, public capability,
cache access, candidate disclosure, quarantine, mutation, native code,
dependency, compiler requirement, version, workflow, job, matrix entry,
permission, credential, release authority, tag, package publication, or CI
change. No new hosted allocation is added.

## Alternatives considered

- Enumerate every known hard-link name and admit the file if all names appear
  confined. Rejected because enumeration is pathname-based, time-varying, and
  non-atomic; it adds disclosure and bounds without proving the use-time state.
- Quarantine files with multiple links. Rejected because moving one name does
  not remove or isolate other names for the same object and no durable recovery
  protocol exists.
- Check link count only once. Rejected because another process can create or
  delete an alias after admission; criterion 3 still requires use-time
  revalidation on the retained object.
- Treat count one as admission of Windows cleanup. Rejected because link count
  is only one of seven joint criteria and supplies neither authority nor
  recovery.
- Add a Windows hosted job. Rejected because M200 changes policy and an
  architecture guard only; it adds no production behavior for another runner
  to validate.

## Validation

Architecture validation must:

- preserve exact M199, runtime, examples, scripts, dependencies, lock,
  metadata, fixtures, and workflows;
- require exactly-one handle-derived link counts at admission and immediately
  before mutation;
- require fail-closed refusal for zero, multiple, changed, unavailable,
  invalid, and unsupported results;
- reject hard-link name enumeration as authority and state that singleton
  stability is necessary but not sufficient;
- mark only criterion 2 resolved as policy while criteria 1 and 3 through 7
  remain unresolved;
- retain Windows non-admission and the absence of cleanup commands or adapters;
  and
- require public registration of RFC-0183 and the policy decision.

Run focused architecture tests, whole-tree static checks, strict docs, static
and current-date governance, supported-Python regression, reproducible package
and release rehearsals, findings-first review, and exact scratch cleanup before
local closeout. Claim no hosted result without an actual safely published run.

## References

- [Microsoft: `FILE_STANDARD_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_standard_info)
- [Microsoft: `BY_HANDLE_FILE_INFORMATION`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/ns-fileapi-by_handle_file_information)
- [Microsoft: hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Microsoft: `FindFirstFileNameW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-findfirstfilenamew)
- [MITRE CWE-367](https://cwe.mitre.org/data/definitions/367.html)
- [RFC-0129](0129-defer-asset-cache-cleanup.md)
- [RFC-0130](0130-asset-cache-cleanup-threat-model.md)
- [RFC-0131](0131-defer-portable-cache-cleanup-capability.md)
- [RFC-0182](0182-refresh-windows-cache-cleanup-readiness.md)
