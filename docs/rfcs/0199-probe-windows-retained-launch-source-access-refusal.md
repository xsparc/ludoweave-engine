# RFC-0199: Probe Windows retained launch-source access refusal

**Status:** Accepted
**Milestone:** M216
**Decision class:** Direction-preserving

## Context

M215 executes the fixed participant source from a retained read-only handle and
opens that handle with read sharing only. Its stable snapshots show no observed
source drift, but it does not directly exercise whether the live handle refuses
competing write and delete access or whether those access classes become
available only after settlement.

Windows documents file sharing as an access compatibility contract that stays
effective until handle close regardless of process context. A competing open
can request an access right without exercising it, allowing refusal and
settlement to be observed without modifying the tracked source.

## Decision

Adopt the test-only [Windows retained launch-source access-refusal
probe](../security/windows-cache-cleanup-retained-launch-source-access-refusal-probe.md).

While the exact M215 source handle is retained, request `GENERIC_WRITE` and
`DELETE` through `CreateFileW` with a competing share mode that accepts read,
write, and delete access. Require both requests to fail with exact native
sharing error 32 before launch, after connection, and after ready. Any
successful handle or different error category fails closed; an unexpected
successful handle is closed first.

After participant settlement and retained source close, require both access
requests to succeed and close without using their rights. Reopen the source
read-only and require its private identity, bounded size, and SHA-256 to equal
the pre-launch snapshot. The probe performs no content or namespace mutation.

This decision is direction-preserving and makes no collection or cleanup
authority increase. No hostile competitor, distinct-principal or
independent-host run has occurred, criteria 6 and 7 remain unresolved, Windows
remains unadmitted, and cleanup remains unimplemented and unauthorized.

## Consequences

- A later private harness proposal can require retained-source write/delete
  refusal in addition to M212-M215's frozen identity observations.
- Exact error 32 distinguishes share-mode refusal from ACL, path, or other
  native failures.
- Post-settlement availability distinguishes live-handle refusal from an
  unrelated permanent access denial.
- Source-commit provenance, imported-module binding, hostile-process behavior,
  mapped views, filesystem filters, privileged bypasses, and hostile ABA
  resistance remain unproved.
- Local validation adds zero GitHub Actions jobs or hosted allocation.
- Fixture mutation, power interruption, collection custody, criteria 6/7, and
  Windows admission remain separate work.

## Alternatives rejected

### Rename, delete, truncate, or write the tracked participant source

Rejected because those operations would turn an access-boundary observation
into a destructive fixture mutation. Access-only `OPEN_EXISTING` handles answer
the narrower question without exercising granted rights.

### Accept access denied or any failed open as equivalent refusal

Rejected because ACL, path, capability, or environmental failures do not prove
the retained handle's sharing contract. Only `ERROR_SHARING_VIOLATION` is an
accepted live refusal.

### Add a product collector or hosted Windows job

Rejected because M216 is a local design-risk probe. It makes no collection or
cleanup authority increase and adds zero GitHub Actions jobs or hosted
allocation.
