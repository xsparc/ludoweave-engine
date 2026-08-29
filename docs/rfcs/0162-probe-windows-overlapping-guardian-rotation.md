# RFC-0162: probe Windows overlapping guardian rotation

- **Status:** Accepted
- **Milestone:** M179
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that overlaps two unchanged M178
guardian processes with one M175 protected participant on the same retained
coordination identity. Abruptly terminate and reap the first guardian, close
the participant, and require the second guardian alone to preserve namespace
protection without owning the cooperative range. Add no runtime or CI surface.

## Context

M178 proves that a protected participant survives abrupt loss of one
overlapping guardian. It does not observe multiple compatible guardians or
whether the surviving guardian can retain namespace protection after the
range participant later closes.

Microsoft documents that compatible `CreateFileW` opens may coexist and that
each handle's share options remain effective until that handle closes,
regardless of process context. This supports one bounded overlapping rotation
observation. It does not define guardian discovery, election, restart,
generation issuance, or recovery.

## Decision

Accept the [Windows overlapping guardian-rotation
probe](../security/cache-cleanup-windows-overlapping-guardian-rotation-probe.md)
as current-host, test-only evidence for one exact compatible ownership chain.

Reuse M178's unchanged fixed isolated guardian twice and M175's unchanged
protected participant once. Create M173's ordinary
`live/coordination.lock`, retain its exact `FILE_ID_INFO`, and start the first
guardian. Require exact `ready`, original identity, M174 substitution error
32, and M173 exclusive acquire/release success.

Start the participant and require exact `ready`, substitution error 32, and
exclusive-range error 33. Start the second guardian while both owners remain
live, require exact `ready`, and require a fresh handle to retain the original
identity with both refusals unchanged.

Kill and boundedly wait for the first guardian through M176's unchanged
helper. Require the second guardian and participant still live on the original
identity with substitution error 32 and exclusive-range error 33. Close the
participant exactly. With only the second guardian live, require original
identity and substitution error 32 while exact exclusive range acquire/release
succeeds.

Close the second guardian exactly. Require exclusive acquire/release and M174
substitution success, retain the displaced original identity and bytes, and
observe a distinct replacement identity with the same bytes. Settle every
process, pipe, handle, and range owner. Use no retry or sleep.

## Consequences

On the observed host, two compatible guardian processes can overlap on one
identity, and the surviving guardian continues its independently owned
namespace protection after the first is abruptly reaped and the participant
later closes. The guardian remains separate from cooperative range ownership.

This is overlapping rotation, not guardian restart, crash recovery,
generation authority, trusted placement, participant admission, leader
election, or cleanup authority. Both guardians are already live before the
first is killed; there is no zero-owner interval, startup recovery, or
replacement after failure.

Windows remains unadmitted. Hostile preexisting handles, arbitrary guardian
counts and process trees, simultaneous failure, mapped views,
filesystem/driver variation, durable generation issuance, use-time
revalidation, fail-closed policy, typed receipts, and independent-host proof
remain open.

No fixture, runtime API, adapter, public probe, production subprocess or
`ctypes`, cache access, cleanup authority, dependency, workflow, permission,
or hosted check is added.

## Alternatives considered

- Start the second guardian only after the first fails. Rejected because the
  resulting zero-owner/startup interval requires trusted placement, recovery,
  and generation design that test-only handle evidence cannot supply.
- Treat either guardian as a range owner. Rejected because guardians must
  preserve namespace identity without being counted as quiescence
  participants.
- Add a new child fixture. Rejected because M178's fixed guardian already owns
  the exact required compatible handle contract.
- Add another hosted matrix entry. Rejected because the existing Windows suite
  will collect the source test after the prerequisite stack is integrated.

## Validation

Focused validation must prove exact reuse of the fixed guardian and protected
participant, same-identity overlap, first-guardian abrupt wait, survivor and
participant protection, participant close with guardian-only namespace
protection and range availability, final release, identity split, byte
preservation, and complete cleanup. Architecture tests must preserve M178,
runtime, examples, scripts, dependencies, workflows, and the wheel package
boundary.

Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, and findings-first gates remain required.

## References

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [GitHub Actions matrix behavior](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [NIST SP 800-218 Rev. 1 IPD](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd)
- [RFC-0161](0161-probe-windows-guardian-abrupt-handoff.md)
