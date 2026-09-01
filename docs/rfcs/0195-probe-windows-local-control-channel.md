# RFC-0195: Probe a Windows local control channel

**Status:** Accepted
**Milestone:** M212
**Decision class:** Direction-preserving

## Context

M205 requires authenticated, replay-resistant, sequenced local coordination at
every deterministic fixture barrier. M209 reserves `advance_barrier` as a
separate private collection action. M211 proves that a fixed participant tree
can be assigned to a retained Job Object before execution, but its output-only
readiness pipe cannot authenticate a connecting client or release a barrier.

Microsoft documents named-pipe DACL enforcement, logon-SID session isolation,
first-instance ownership, remote-client refusal, server-side client process
identity, and overlapped I/O settlement. The default named-pipe descriptor is
too broad for M205 because it grants access beyond the creator's logon context.

## Decision

Adopt the test-only [Windows local control-channel
probe](../security/windows-cache-cleanup-local-control-channel-probe.md).

The controller creates one randomized, one-instance, remote-rejecting duplex
named pipe under an explicit protected DACL containing one allow ACE for the
current logon SID. It reads the resulting DACL back and rejects any defaulted,
unprotected, extra-ACE, wrong-SID, or wrong-mask result. A second server
instance must be refused.

One fixed direct participant is created suspended with no inherited handles,
assigned to a no-breakaway kill-on-close Job Object, and resumed only after
containment. The server binds the connected named-pipe client to both the
retained process handle and exact one-member Job before sending a fresh 256-bit
challenge. Four bounded canonical messages advance exactly one release. Replay,
wrong challenge, disconnect, timeout, malformed shape, and unexpected process
membership cannot become a pass.

This decision is direction-preserving and makes no collection or cleanup
authority increase. It adds current-host test evidence for one same-logon local
control primitive only. No distinct-principal or independent-host run has
occurred, criteria 6 and 7 remain unresolved, Windows remains unadmitted, and
cleanup remains unimplemented and unauthorized.

## Consequences

- A later private harness proposal can reuse a reviewed local endpoint,
  retained-client identity check, challenge, sequence, and bounded I/O pattern.
- The default named-pipe security descriptor and a participant-reported PID are
  explicitly insufficient.
- Same-logon success does not satisfy M205's distinct authenticated-principal,
  cross-session, hostile-channel, or credential requirements.
- M211's exact process-tree settlement remains a separate required primitive.
- Local validation adds zero GitHub Actions jobs or hosted allocation.
- VM/physical power, fixture mutation, collection custody, criteria 6/7, and
  Windows admission remain separate work.

## Alternatives rejected

### Reuse the M211 output-only anonymous pipe

Rejected because it has no controller-to-participant release path, connection
authentication, replay challenge, or sequence validation.

### Use the default named-pipe security descriptor

Rejected because Windows grants broader default access than the exact logon-
scoped boundary requires.

### Trust a client-reported process identifier

Rejected because participant self-report is not identity evidence. The server
must compare native client identity with the retained process handle.

### Add the private collector or public runner now

Rejected because same-host control-channel evidence does not authorize
credentials, cross-principal execution, fixture mutation, power control,
collection, cleanup, or a public self-hosted runner.
