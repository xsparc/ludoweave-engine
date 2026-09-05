# RFC-0191: Adopt the Windows independent-host evidence validator

**Status:** Accepted
**Milestone:** M208
**Decision class:** Direction-preserving

## Context

M207 defines the independent-host evidence required for M199 criterion 7 but
performs no run and supplies no validator. Reviewers need a strict source-only
boundary that distinguishes a canonical incomplete artifact from a complete
claim and that cannot satisfy criterion 7 by copying a criterion-6 boolean.

The project already has bounded canonical JSON and the M206 cross-principal
validator. Reusing those contracts avoids another serialization scheme and
makes the criterion dependency independently checkable. File identifiers and
canonical hashes remain scoped evidence values, not authentication or
provenance proof.

## Decision

Adopt the [Windows independent-host evidence
validator](../security/windows-cache-cleanup-independent-host-evidence-validator.md)
as a source-only, offline, read-only M208 boundary.

The validator accepts exactly two stable regular files. It first validates the
M206 companion, then checks the independent-host document's exact digest
binding and derives criterion 6 from the companion result. It validates exact
host independence, capability classifications, the eight profile lanes, three
interruption classes, status/count/outcome relationships, resource bounds,
sanitized identities, and the false admission claim. A reviewed all-`not_run`
fixture demonstrates incomplete evidence handling.

This decision is direction-preserving and makes no authority increase. It
adds no qualifying run, collector, coordinator, process launch, native API,
credential or account management, filesystem mutation, cleanup operation,
runtime command, dependency, workflow, permission, or hosted allocation.
M208 adds no hosted allocation.

Criteria 6 and 7 remain unresolved. Windows is not admitted. Cleanup remains
unimplemented and unauthorized.

## Consequences

- Criterion 7 is derived only from a separately valid, digest-bound criterion-
  6 artifact plus complete independent-host observations.
- Structurally valid evidence can remain failed, unsupported, incomplete, or
  not run.
- The reviewed fixture is a parser and policy fixture, not a Windows or
  interruption execution result.
- A complete criterion-7 artifact still cannot set Windows admission true;
  admission requires a later accepted decision.
- Future collection remains a separately reviewed privileged slice on offline
  operator-controlled hosts.
- No machine, storage, principal, credential, pathname, or platform error value
  may enter retained public evidence or validator output.

## Alternatives rejected

### Trust a criterion-6 field copied into the independent-host artifact

Rejected because a self-asserted field does not prove that the companion M206
artifact is structurally valid, complete, or the artifact whose digest was
reviewed.

### Add the privileged independent-host harness now

Rejected because schema validation does not authorize process control,
physical interruption, native filesystem calls, credential custody, or
filesystem mutation.

### Attach operator-controlled hosts to public CI

Rejected because the evidence contract requires offline custody and because a
public self-hosted runner would expose those machines to an unrelated workflow
trust boundary.

### Treat canonical SHA-256 values as signatures

Rejected because canonical digests establish byte identity, not operator
authentication or provenance.
