# RFC-0192: Adopt the Windows independent-host collection-authority policy

**Status:** Accepted
**Milestone:** M209
**Decision class:** Direction-preserving

## Context

M207 defines criterion-7 host, capability, refusal, interruption, and custody
requirements. M208 validates the resulting public document and its M206
companion, but deliberately adds no collector. The next boundary must specify
who may control a future privileged fixture, what each action may affect, and
how private evidence moves into the sanitized M208 envelope before any harness
is considered.

That control plane cannot live in public CI. GitHub documents persistent
compromise risk for public self-hosted runners. Windows isolation also exposes
network, clipboard, mapped-folder, checkpoint, and power semantics that must be
constrained explicitly. Evidence digests establish byte identity but do not
authenticate an operator or replace a custody record.

## Decision

Adopt the [Windows independent-host collection-authority
policy](../security/windows-cache-cleanup-independent-host-collection-authority-policy.md)
as a policy-only M209 boundary.

A future trusted offline coordinator may mint only private, non-serializable,
single-run and single-use collection actions bound to one host, fixture, lane,
trial, barrier, interruption class, source/executable/contract/evidence/recipe/
capability identity, and closed operation. Product input, public artifacts,
paths, environment values, participant claims, or digests alone cannot mint or
widen that authority.

Collection authority remains separate from M201 cleanup authority and from
canonical world commands. Offline hosts have networking and clipboard
redirection disabled, no writable live sharing, no public runner attachment,
and no repository credential. Process termination targets only bound fixture
participants. VM power cuts preserve the current disk and use neither guest
shutdown nor checkpoint restore. Physical power loss remains operator-only.

Private evidence uses a pre-run manifest, chronological custody record, atomic
same-volume staging, separately retained SHA-256, post-settlement sanitization,
and the unchanged M208 validator. Any ambiguity or teardown failure invalidates
the affected trial and quarantines the fixture rather than normalizing a pass.

This decision makes no executable authority increase. It adds no privileged
harness and no qualifying evidence, host provisioning, process or power control,
native API, credential handling, cleanup, filesystem mutation, runtime command,
dependency, workflow, permission, or secret, and there is no new hosted allocation. Criteria 6
and 7 remain unresolved; Windows stays unadmitted and cleanup remains
unimplemented and unauthorized.

## Consequences

- Future privileged work has a reviewable least-authority envelope before any
  executable host control is proposed.
- Public CI, live network channels, writable host sharing, guest-managed power
  transitions, and checkpoint restoration cannot produce qualifying evidence.
- Private raw observations and custody records remain outside the repository;
  only the sanitized canonical M208 artifact may be retained publicly.
- Evidence identity, operator authentication, collection authority, cleanup
  authority, and Windows admission remain separate concepts.
- A later harness milestone must demonstrate these controls on disposable
  offline fixtures before any qualifying execution can be claimed.

## Alternatives rejected

### Implement the privileged harness with the policy

Rejected because a policy review does not authorize native process control,
hypervisor or physical power actions, account custody, or fixture mutation.

### Run the collector on a public self-hosted runner

Rejected because untrusted workflow code can persistently compromise the host
and access secrets or other sensitive resources.

### Use Windows Sandbox as an independent host

Rejected because it is a container rather than a separately provisioned host,
and its default networking, clipboard, and sharing channels require explicit
hardening even for auxiliary use.

### Restore a checkpoint after each power trial

Rejected because rollback replaces the interrupted state and cannot prove
recovery of the current affected storage.

### Treat SHA-256 as operator authentication

Rejected because a digest detects byte changes but does not prove who created,
handled, reviewed, or transferred the artifact.
