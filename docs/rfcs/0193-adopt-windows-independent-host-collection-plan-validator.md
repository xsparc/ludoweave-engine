# RFC-0193: Adopt the Windows independent-host collection-plan validator

**Status:** Accepted
**Milestone:** M210
**Decision class:** Direction-preserving

## Context

M209 defines the authority envelope for a future private offline collector and
requires a pre-run manifest, but it deliberately adds no privileged harness.
Before native process containment, hypervisor control, credentials, or fixture
mutation can be reviewed, the exact planned matrix and fail-closed declarations
need a bounded machine-checkable form that cannot itself become authority.

Windows Job Objects and retained process handles can scope a future process tree,
but PID-only targeting is insufficient. Hypervisor operations distinguish power
control from guest shutdown and checkpoint restore. Evidence custody also needs
separate digest retention, and public self-hosted runners remain inappropriate
for this work.

## Decision

Adopt the source-only [Windows independent-host collection-plan
validator](../security/windows-cache-cleanup-independent-host-collection-plan-validator.md).

The validator accepts one stable bounded canonical document containing only
sanitized classifications, exact ordered profile/barrier/interruption/operation
matrices, typed digest identities, requirement declarations, ephemeral host
ordinals, and derived totals. It derives `plan_complete` from structural inputs
and requires every execution, authority, criterion, and admission claim to remain
false and `not_run`.

The checked document is a structural companion to a future private run manifest,
not that manifest and not an authority object. It cannot authenticate identities,
mint or consume authority, execute an operation, validate a real host, or turn a
digest into provenance. The reviewed fixture is intentionally incomplete and
contains no host or stable identity.

This decision makes no executable authority increase. It adds no runtime API,
CLI command, privileged harness, native call, process or power control, account
or credential handling, filesystem mutation, network access, cleanup authority,
dependency, workflow, permission, secret, hosted allocation, or qualifying
evidence. Criteria 6 and 7 remain unresolved; Windows stays unadmitted and
cleanup remains unimplemented and unauthorized.
There is no qualifying evidence and no qualifying run.

## Consequences

- A future private harness proposal has a deterministic, reviewable plan shape
  and a closed operation matrix before any privileged code is considered.
- Structural completeness remains explicitly separate from authentication,
  authority issuance, execution, evidence sufficiency, and admission.
- Stable machine, storage, process, principal, session, path, credential, and
  operator identifiers remain outside the public schema.
- Local validation exercises only source tooling and adds zero GitHub Actions
  jobs or hosted allocation.

## Alternatives rejected

### Implement the privileged harness now

Rejected because this repository has no independently provisioned disposable
offline host cohort, reviewed credential custody, external power boundary, or
proven teardown environment. Those capabilities require a separate authority
review and real-host validation.

### Treat a complete plan as authority

Rejected because serializable repository data, declarations, and digests cannot
authenticate an operator, bind a live host, or mint M209's private single-use
capability.

### Put private host identities in the plan

Rejected because public review needs only ephemeral ordinals and bounded
classifications. Stable identifiers remain in separately controlled private
custody records.

### Run collection through public repository CI

Rejected because public self-hosted runners can be persistently compromised and
the M209 boundary forbids repository credentials and live network channels on
collection hosts.
