# Windows hard-link alias mutator abrupt-loss-after-recreate probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M188
- **Date:** 2026-08-29
- **Baseline:** M187's abrupt-loss-before-recreation boundary

## Decision

Retain one Windows-only, test-only NTFS observation showing that abrupt process
loss after M186's mutator child emits `recreated`, but before it receives the
close token, leaves the peer alias present. The original and alias retain their
shared identity, bytes, and two-link count while M181's matching guardian
remains live and continues protecting the exact name. Treat this as three-
process, same-principal negative rollback evidence. There is no automatic
rollback to one link, Windows is not admitted, and no cleanup authority is
created.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_abrupt_loss_after_recreate_probe.py`:

1. creates M173's exact ordinary coordination file and peer hard-link alias;
2. opens both entries through the existing capability helper, retains their
   shared `FILE_ID_INFO`, requires link count two, and closes initial handles;
3. starts M181's matching guardian child, requires exact `ready`, and confirms
   exact-name rename refusal with Windows sharing error 32;
4. starts M186's unchanged fixed mutator child, requires exact `deleted`, sends
   the exact recreate token, and requires exact `recreated` with both children
   live;
5. before any close token, requires alias presence, shared identity and bytes,
   link count two, and exclusive byte-range availability through both names;
6. terminates and reaps the mutator through the existing bounded test helper,
   requiring a nonzero exit and empty remaining output;
7. requires the guardian still live, the alias still present, shared identity
   and bytes unchanged, link count still two, range availability through both
   names, and exact-name rename refusal;
8. releases the guardian exactly, renames the original successfully, and
   verifies displaced and alias identities, two-link counts, bytes, process/
   stream closure, and complete native/range ownership cleanup.

The probe uses no retry or sleep. It sends no close token to the mutator after
`recreated`. The fixture remains byte-for-byte M186's fixed-name, argument-
free, shell-free child. Abrupt termination is confined to a controlled test
child whose exact phase is known; it is not a production cleanup action.

## Security consequence

The observed two-link state persists after the mutation actor is reaped. The
guardian's live no-delete-share handle still refuses rename of the original
name, but it neither owns nor rolls back the peer directory entry. Exact-name
exclusion is therefore neither root-confined ownership nor failure recovery.

This is a three-process, same-principal observation under one parent-owned
process tree: parent coordinator, guardian child, and mutator child. It is not
cross-principal, unrelated-session, hostile-process, simultaneous-race, crash-
consistency, power-loss, or durable-commit evidence.

A future design must still decide authenticated root ownership, link
enumeration and policy, use-time identity/count revalidation, durable intent,
generation provenance, quarantine, idempotency, rollback/reconciliation, and
typed recovery receipts. ReFS, SMB, other drivers and hosts, cross-volume
behavior, file-ID reuse, other failure phases, and independent-host proof
remain unresolved.

No runtime or package surface changes. No production subprocess, native API,
cache mutation, dependency, workflow, permission, hosted allocation, or hosted
check is added. No hosted check is added. Windows is not admitted.

## Revisit criteria

Revisit Windows admission only after a design supplies trusted root ownership,
an explicit hard-link policy, use-time identity and link-count revalidation,
durable generation and recovery state, typed receipts, cross-principal
adversarial evidence, and independent-host proof.

## References

- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Microsoft: hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [RFC-0171](../rfcs/0171-probe-windows-hard-link-alias-mutator-abrupt-loss-after-recreate.md)
