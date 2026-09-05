# RFC-0196: Probe Windows local control token binding

**Status:** Accepted
**Milestone:** M213
**Decision class:** Direction-preserving

## Context

M212 proves that one connected local named-pipe client is the retained,
suspended-then-contained participant process before a fresh challenge is sent.
That process binding does not yet prove which primary token remains attached to
the retained process or that native pipe, process, and token session evidence
agrees through the release barrier.

Windows exposes query-only process-token information and direct session
lookups without requiring server-thread impersonation. Impersonation would add
an unnecessary thread-security transition and a fail-stop obligation if
`RevertToSelf` failed.

## Decision

Adopt the test-only [Windows local control token-binding
probe](../security/windows-cache-cleanup-local-control-token-binding-probe.md).

Open the retained M212 participant process's primary token with `TOKEN_QUERY`
and keep the handle open across challenge/ready. Query private copies of user
SID, logon SID, token and authentication identifiers, modified identifier,
token type, and token session before the challenge and again after `ready` but
before `release`. Reject a non-primary token or any change between snapshots.

Require the participant user, logon, authentication, and session identity to
match the controller's query-only primary-token snapshot. Require
`GetNamedPipeClientSessionId`, `ProcessIdToSessionId`, and participant
`TokenSessionId` to agree. Re-read M212's exact pipe DACL against the copied
participant logon SID before advancing the barrier.

Impersonation is excluded. Identity fields remain private and are not retained
as evidence. This decision is direction-preserving and makes no collection or
cleanup authority increase. No distinct-principal or independent-host run has
occurred, criteria 6 and 7 remain unresolved, Windows remains unadmitted, and
cleanup remains unimplemented and unauthorized.

## Consequences

- A later private harness proposal can require a retained primary-token and
  session-binding check in addition to M212's retained process binding.
- A client PID, process handle, token query, or session lookup alone remains
  insufficient; the fixed native observations must agree.
- Same-logon and same-session success does not satisfy distinct-principal,
  hostile-channel, credential-custody, or independent-host requirements.
- M212's exact protocol and process/Job settlement remain separately protected.
- Local validation adds zero GitHub Actions jobs or hosted allocation.
- Fixture mutation, power interruption, collection custody, criteria 6/7, and
  Windows admission remain separate work.

## Alternatives rejected

### Impersonate the named-pipe client

Rejected because query-only retained-token and session APIs answer the bounded
question without altering the controller thread's security context. A failed
reversion would create a materially more dangerous failure mode.

### Trust only the process or pipe session identifier

Rejected because one identifier does not bind the retained primary token. The
pipe, process, token, and controller observations must agree.

### Serialize token identity as evidence

Rejected because stable SID, LUID, session, process, handle, or pipe values are
unnecessary disclosure. The result is a local pass/fail observation only.

### Add cross-principal launch or collection now

Rejected because this same-logon probe does not authorize account or credential
management, a privileged collector, fixture mutation, or a public runner.
