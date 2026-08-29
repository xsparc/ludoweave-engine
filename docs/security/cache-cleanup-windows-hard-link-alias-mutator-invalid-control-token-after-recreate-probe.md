# Windows hard-link alias mutator invalid control token after recreation probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M190
- **Date:** 2026-08-29
- **Baseline:** M189's control-pipe EOF after recreation boundary

## Decision

Retain one Windows-only, test-only NTFS observation showing that a fixed invalid
control token after recreation, after M186's mutator child emits `recreated`
but before it receives the close token, leaves the peer alias present. The
original and alias retain their shared identity, bytes, and two-link count
while M181's matching guardian remains live and continues protecting the exact
name. Treat this as three-process, same-principal negative rollback evidence.
There is no automatic rollback to one link, Windows is not admitted, and no
cleanup authority is created.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_invalid_control_token_after_recreate_probe.py`:

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
6. writes the repository-fixed invalid `?` byte, requires the buffered write to
   accept exactly one byte, flushes it, closes the parent `Popen.stdin`, and
   waits with M186's fixed bound for existing fixture exit 5, stdout EOF, and
   empty stderr;
7. requires the guardian still live, the alias still present, shared identity
   and bytes unchanged, link count still two, range availability through both
   names, and exact-name rename refusal; and
8. releases the guardian exactly, renames the original successfully, and
   verifies displaced and alias identities, two-link counts, bytes, process/
   stream closure, and complete native/range ownership cleanup.

The probe uses no retry or sleep. It sends no close token after `recreated` and
observes no `closed` event. The fixture remains byte-for-byte M186's fixed-
name, argument-free, shell-free child. The invalid byte is a controlled
test-only protocol condition, not a production cleanup action.

## Security consequence

The observed two-link state persists after the mutation actor settles through
its invalid-control path. The guardian's live no-delete-share handle still
refuses rename of the original name, but it neither owns nor rolls back the
peer directory entry. Exact-name exclusion is therefore neither root-confined
ownership nor failure recovery.

This is a three-process, same-principal observation under one parent-owned
process tree: parent coordinator, guardian child, and mutator child. It is not
control-pipe EOF, not abrupt process termination, and not arbitrary malformed-
input, cross-principal, duplicated/inherited-writer, unrelated-session,
hostile-process, simultaneous-race, crash-consistency, power-loss, or durable-
commit evidence.

A future design must still decide authenticated root ownership, link
enumeration and policy, use-time identity/count revalidation, durable intent,
generation provenance, quarantine, idempotency, rollback/reconciliation, and
typed recovery receipts. ReFS, SMB, other drivers and hosts, cross-volume
behavior, file-ID reuse, other failure phases, and independent-host proof
remain unresolved.

No runtime or package surface changes. No production subprocess, native API,
cache mutation, dependency, workflow, permission, or hosted allocation is
added. No hosted check is added. Windows is not admitted.

## Revisit criteria

Revisit Windows admission only after a design supplies trusted root ownership,
an explicit hard-link policy, use-time identity and link-count revalidation,
durable generation and recovery state, typed receipts, cross-principal
adversarial evidence, and independent-host proof.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [Python: `io`](https://docs.python.org/3/library/io.html)
- [RFC-0173](../rfcs/0173-probe-windows-hard-link-alias-mutator-invalid-control-token-after-recreate.md)
