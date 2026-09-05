# RFC-0161: probe Windows guardian abrupt handoff

- **Status:** Accepted
- **Milestone:** M178
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that starts a fixed non-range-
locking guardian process over M173's coordination identity, admits M175's
unchanged protected participant, kills and boundedly waits for the guardian,
and requires the live participant to retain namespace and range protection.
Add no runtime or CI surface.

## Context

M177 proves a graceful parent-owned guardian-to-participant handoff. It does
not observe abrupt guardian process loss. Microsoft documents that file-sharing
options remain effective until each handle closes regardless of process
context, and that `TerminateProcess` is asynchronous until the process object
is waited to termination.

The observation must remain narrower than recovery. A participant is already
live on the same identity before the guardian is killed. If no compatible
owner survived, the pathname would again become replaceable. The probe does
not restart a guardian, issue a generation, reconstruct state, or protect a
startup interval.

## Decision

Accept the [Windows guardian abrupt-handoff
probe](../security/cache-cleanup-windows-guardian-abrupt-handoff-probe.md) as
current-host, test-only evidence for one exact overlapping ownership chain.

Add one fixed isolated child fixture. It opens only
`live/coordination.lock` for generic read with read/write sharing, deliberately
omits delete sharing, uses null security attributes, opens the final component
without following a reparse point, rejects reparse identity, proves its handle
noninheritable, takes no byte-range lock, and emits bounded versioned
`ready`/`closed` events. It accepts only one fixed release byte and no argument
or environment-selected value.

Create M173's ordinary file and retain its exact `FILE_ID_INFO`. Start the
guardian and require exact `ready`, M174 substitution error 32, and M173
exclusive acquire/release success. Start M175's unchanged participant, require
exact `ready`, the original identity, substitution error 32, and exclusive-
range error 33.

Kill the guardian and wait with M176's existing bounded helper. Only after the
nonzero abrupt exit is reaped, require the participant still live, a fresh
handle still observing the original identity, substitution error 32, and
exclusive-range error 33. Then close the participant exactly, require
exclusive acquire/release and M174 substitution success, retain the displaced
original identity and bytes, and observe a distinct replacement identity with
the same bytes. Settle every process, pipe, handle, and range owner. Use no
retry or sleep.

## Consequences

On the observed host, abrupt loss of a non-range-locking guardian after a
protected participant has joined does not interrupt the participant's own
namespace or range protection. The conclusion begins only after bounded
process wait and depends on the survivor already owning a compatible handle.

This is not crash recovery, generation authority, trusted placement,
participant admission, or cleanup authority. It does not prove a portable
termination deadline, guardian restart, a zero-owner interval, arbitrary
process trees, complete handle settlement at every instant, or durability.

Windows remains unadmitted. Multiple guardians, hostile preexisting handles,
startup races, mapped views, filesystem/driver variation, durable generation
issuance, use-time revalidation, fail-closed policy, typed receipts, and
independent-host proof remain open.

No runtime API, adapter, public probe, production subprocess or `ctypes`, cache
access, cleanup authority, dependency, workflow, permission, or hosted check
is added.

## Alternatives considered

- Promote the guardian to runtime recovery infrastructure. Rejected because
  trusted placement, startup, restart, generation, admission, and durable
  state remain undesigned.
- Kill the guardian before any participant joins. Rejected because that only
  reopens M177's known zero-owner gap and proves no handoff property.
- Add a retry for delayed release. Rejected because the asserted protection is
  owned by the live participant and retry would hide the exact post-wait state.
- Add another hosted matrix entry. Rejected because the existing Windows suite
  will collect the source test after the prerequisite stack is integrated.

## Validation

Focused validation must prove fixed child inputs, guard the exact final-
component no-follow and reparse-check construction, exercise noninheritability
and acknowledged close, prove guardian-only namespace protection without range
ownership, same-identity participant admission, exact post-wait survivor
protection, final settlement, identity split, byte preservation, and complete
cleanup. Architecture tests must preserve M177, runtime, examples, scripts,
dependencies, workflows, and the wheel package boundary.

Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, and findings-first gates remain required.

## References

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Microsoft: `WaitForSingleObject`](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject)
- [Microsoft: `LockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex)
- [RFC-0160](0160-probe-windows-protected-guardian-handoff.md)
