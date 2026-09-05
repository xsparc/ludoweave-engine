# RFC-0188: Adopt the Windows cross-principal validation contract

**Status:** Accepted
**Milestone:** M205
**Decision class:** Direction-preserving

## Context

The M199 readiness decision leaves Windows criterion 6 unresolved until the
project has real cross-principal, unrelated-process, hostile-race, ACL, alias,
inheritance, and reparse evidence. M200 through M204 define policy for refusal,
authority, intent, state-machine, and recovery behavior, but none performs a
qualifying adversarial run.

The remaining evidence needs a precise security boundary before any harness or
native adapter can be considered. In particular, a restricted form of the same
user is not a substitute for a distinct untrusted principal, and repository
automation must not become a credential or local-account manager.

## Decision

Adopt the
[Windows cache-cleanup cross-principal validation contract](../security/windows-cache-cleanup-cross-principal-validation-contract.md)
as the sole M205 change in direction.

The contract requires independently authenticated distinct-principal evidence,
unrelated process and session topologies, deterministic adversarial barriers,
explicit ACL and handle observations, real alias and reparse pressure, bounded
sanitized evidence, and fail-closed teardown. Account and credential custody
remain operator-owned and outside repository inputs and outputs.

This decision makes no authority increase. It adds no production adapter, no
principal launcher, no account-management behavior, and no qualifying evidence.
Windows cleanup remains unavailable. Because ordinary GitHub-hosted Windows
runners do not supply the required topology, M205 adds no new hosted allocation
and leaves the vital CI workflow unchanged.

## Consequences

- A future fixture must demonstrate every mandatory lane, not merely implement
  a compatible evidence schema.
- Same-user restricted tokens, integrity changes, and hosted administrator
  accounts cannot satisfy criterion 6.
- Credentials, account lifecycle, group membership, logon rights, and local
  security policy remain outside the repository contract.
- Unsupported or incomplete mandatory lanes preserve the unresolved readiness
  result.
- Future implementation work needs a separate accepted slice and must preserve
  the no-authority and no-secret boundaries defined here.

## Alternatives rejected

### Treat restricted same-user execution as cross-principal evidence

Rejected because it does not test the access token and ACL boundary of an
independently authenticated untrusted account.

### Put test-account credentials in CI secrets

Rejected because that would expand credential custody and still would not make
the default hosted administrator topology representative.

### Implement a launcher and fixture in the same milestone

Rejected because the trust, account, handle, ACL, evidence, and teardown
contracts must be reviewable before code gains any process-launch capability.
