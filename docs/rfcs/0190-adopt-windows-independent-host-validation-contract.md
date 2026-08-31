# RFC-0190: Adopt the Windows independent-host validation contract

**Status:** Accepted
**Milestone:** M207
**Decision class:** Direction-preserving

## Context

The M199 readiness decision leaves criterion 7 unresolved until the Windows
cleanup design has been reproduced on independent supported hosts and has
explicit safe-refusal evidence for unsupported filesystem and volume
capabilities. M205 defines the cross-principal experiment, and M206 validates
that evidence envelope, but neither establishes host independence, storage
capability coverage, or interruption durability.

Default hosted automation is not a substitute. GitHub-hosted Windows runners
use an administrator account with UAC disabled and do not expose the required
physical storage and interruption controls. Connecting operator-controlled
self-hosted machines to a public-repository workflow would create an unrelated
trust risk.

## Decision

Adopt the
[Windows cache-cleanup independent-host validation contract](../security/windows-cache-cleanup-independent-host-validation-contract.md)
as the sole M207 change in direction.

The contract requires at least two independently provisioned hosts for every
profile, observed filesystem and volume capabilities, a complete positive and
safe-refusal matrix, separate process/VM/physical interruption classes,
recovery reconciliation, and a bounded sanitized evidence envelope. It reserves
the envelope for later implementation but produces no qualifying evidence.

This decision makes no authority increase. It adds no implementation or
validator, no cleanup or process launcher, no native filesystem call, no
credential custody, and no production adapter. Collection remains offline on
operator-controlled fixtures. M207 adds no new hosted allocation and leaves the
vital CI workflows unchanged.

## Consequences

- Criterion 6 must pass independently before criterion 7 can pass.
- NTFS success cannot substitute for observed refusal on ReFS, SMB, CsvFS,
  cross-volume, unknown, or missing-capability profiles.
- A graceful run, VM stop, or successful flush call cannot be overstated as
  physical power-loss evidence.
- Unsupported, incomplete, shared-ancestry, or unsafe host results keep
  criterion 7 unresolved and Windows cleanup unadmitted.
- A future harness and offline validator each require a separate accepted
  milestone and must preserve this no-authority boundary.

## Alternatives rejected

### Reuse the default hosted Windows job

Rejected because its administrator topology, virtual storage, and lifecycle do
not satisfy the principal, independent-host, or physical-interruption contract.

### Attach private hardware as a public self-hosted runner

Rejected because untrusted public workflow code would gain an execution path to
operator-controlled machines and because hosted execution is unnecessary for
offline evidence review.

### Admit every filesystem that reports the expected feature flags

Rejected because flags describe individual capabilities, not the complete
cleanup, recovery, security, clustering, remote-storage, or durability
semantics.

### Implement the harness and policy together

Rejected because host identity, storage profiles, interruption classes,
evidence sanitization, and fail-closed admission must be independently
reviewable before code gains any additional process or filesystem authority.
