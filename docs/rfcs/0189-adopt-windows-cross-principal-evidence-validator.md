# RFC-0189: Adopt the Windows cross-principal evidence validator

**Status:** Accepted
**Milestone:** M206
**Decision class:** Direction-preserving

## Context

M205 defines the exact evidence required for M199 criterion 6, but it performs
no qualifying run. Before a privileged fixture is considered, reviewers need a
strict way to distinguish a well-formed incomplete record from a valid
all-passed claim. The project already owns a bounded canonical JSON contract;
creating a second serialization or authentication scheme would increase scope
without producing Windows security evidence.

Current Microsoft token documentation supports keeping raw token statistics as
private observer inputs and exposing only qualification booleans. Ordinary
GitHub-hosted Windows virtual machines use an administrator account with UAC
disabled, so that environment cannot supply the independently authenticated,
non-administrator hostile principal required by M205.

## Decision

Adopt the
[Windows cache-cleanup cross-principal evidence
validator](../security/windows-cache-cleanup-cross-principal-evidence-validator.md)
as a source-only, offline, read-only M206 boundary.

The script accepts exactly one stable regular-file artifact, enforces existing
canonical JSON and explicit resource limits, validates every fixed lane,
barrier, count, sanitized qualification, control, outcome, digest identity, and
claim relationship, and emits only path-free canonical results. A reviewed
all-`not_run` fixture demonstrates incomplete evidence handling.

This decision is direction-preserving and makes no authority increase. It adds
no qualifying evidence, process launcher, native Windows call, credential or
account management, cleanup operation, runtime command, dependency, or
workflow. Because the hosted topology remains nonqualifying, M206 adds no new
hosted allocation.

Criterion 6 remains unresolved. Windows is not admitted. Cleanup remains
unimplemented and unauthorized.

## Consequences

- Structurally valid evidence can still be incomplete, failed, or unsupported.
- Only exact all-passed evidence can set the criterion 6 field true, while the
  Windows-admission field remains false until criterion 7 is separately met.
- The reviewed fixture is a parser and policy fixture, not a run result.
- Future qualifying execution remains a separately reviewed privileged slice
  under the M205 account, token, process, ACL, handle, fixture, and teardown
  contract.
- No credential, raw principal identifier, machine pathname, or platform error
  text may enter retained evidence.

## Alternatives rejected

### Add a privileged Windows launcher now

Rejected because schema review does not authorize credential custody, account
lifecycle, process creation, or filesystem mutation.

### Use a normal hosted Windows runner as evidence

Rejected because the administrator topology is not the distinct untrusted
principal required by M205 and therefore produces no qualifying evidence.

### Accept ordinary JSON with best-effort field handling

Rejected because duplicate fields, unknown fields, unbounded values, and
noncanonical encodings would make exact evidence review ambiguous.
