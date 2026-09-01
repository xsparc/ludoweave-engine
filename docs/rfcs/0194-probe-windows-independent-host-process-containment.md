# RFC-0194: Probe Windows independent-host process containment

**Status:** Accepted
**Milestone:** M211
**Decision class:** Direction-preserving

## Context

M209 permits a future `forced_process_termination` action only against the exact
spawned participant and descendants bound by retained private process identity.
M210 validates the sanitized plan shape but deliberately adds no native harness.
PID-only targeting and assigning an already-running participant both leave
identity or pre-assignment races unresolved.

Microsoft documents suspended process creation, retained process/thread
handles, Job Object descendant inheritance, nested jobs, no-breakaway limits,
bounded process waits, and kill-on-last-job-handle close. The current repository
has not yet exercised those primitives as one containment sequence.

## Decision

Adopt the test-only [Windows independent-host process-containment
probe](../security/windows-cache-cleanup-independent-host-process-containment-probe.md).

The controller creates one unnamed no-breakaway Job Object with
`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`; creates one fixed direct interpreter
suspended with a one-handle inheritance list; assigns the retained process
handle; proves no fixture instruction ran; then resumes the retained primary
thread. The participant creates one fixed direct descendant, and the controller
retains and validates that process handle plus the exact two-member Job list.

The probe separately proves explicit Job-scoped termination with zero-member
accounting and last-handle-close fail-safe settlement. Unexpected membership,
unbounded waits, incompatible nested-job assignment, malformed output, or
identity mismatch cannot be converted into a pass. There is no PID-only or
ordinary unsuspended fallback.

This decision is direction-preserving and makes no collection or cleanup
authority increase. It adds test evidence for one current-host process-control
primitive only. No independent-host run has occurred, criteria 6 and 7 remain
unresolved, Windows remains unadmitted, and cleanup remains unimplemented and
unauthorized.

## Consequences

- A later private harness proposal can reuse a reviewed containment sequence
  rather than inventing PID-based termination.
- The direct interpreter requirement prevents a virtual-environment launcher
  handle from being mistaken for participant identity.
- Exact membership rejects console helpers or other unexpected descendants
  instead of silently widening the target tree.
- Local test validation adds zero GitHub Actions jobs or hosted allocation.
- VM and physical power actions, offline hosts, credentials, collection
  authority, evidence custody, recovery, and admission remain separate work.

## Alternatives rejected

### Assign an ordinary running process

Rejected because the participant could execute or create an escaping child
before Job assignment.

### Terminate by process identifier

Rejected because a PID is not retained process identity and may be stale or
reused. Termination remains scoped to the retained Job Object.

### Accept every inherited descendant

Rejected because M209 invalidates unexpected processes. The probe requires the
private Job membership to equal the fixed retained root and descendant.

### Add a public self-hosted Windows runner

Rejected because public-repository workflows can expose persistent self-hosted
runners to untrusted code. M211 adds no workflow, runner, secret, permission, or
hosted allocation.
