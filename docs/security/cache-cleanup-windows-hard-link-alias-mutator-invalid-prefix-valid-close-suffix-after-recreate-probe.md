# Windows hard-link alias mutator invalid prefix with valid close suffix after recreation probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M192
- **Date:** 2026-08-29
- **Baseline:** M191's valid close prefix with trailing invalid byte boundary

## Decision

Retain one Windows-only, test-only NTFS observation showing that a fixed
invalid prefix with one valid close suffix after recreation is rejected by
M186's unchanged fixture. The child emits no `closed` event and exits 5 after
the single flushed write contains `?!`. This leaves the peer alias present with
the original identity, bytes, and two-link count while M181's matching guardian
remains live and continues protecting the exact name. Treat this as
three-process, same-principal leading-byte rejection evidence. It is not
general message framing, Windows is not admitted, and no cleanup authority is
created.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_invalid_prefix_valid_close_suffix_after_recreate_probe.py`:

1. creates M173's exact ordinary coordination file and peer hard-link alias;
2. opens both entries through the existing capability helper, retains their
   shared `FILE_ID_INFO`, requires link count two, and closes initial handles;
3. starts M181's matching guardian child, requires exact `ready`, and confirms
   exact-name rename refusal with Windows sharing error 32;
4. starts M186's unchanged fixed mutator child, requires exact `deleted`, sends
   the exact recreate token, and requires exact `recreated` with both children
   live;
5. requires alias presence, shared identity and bytes, link count two, and
   exclusive byte-range availability through both names;
6. writes `?!` exactly once, requires the buffered write to accept both bytes,
   flushes and closes the writer, then waits with M186's fixed bound for exit 5,
   stdout EOF without a close event, and empty stderr;
7. requires the guardian still live, the alias still present, shared identity
   and bytes unchanged, link count still two, range availability through both
   names, and exact-name rename refusal; and
8. releases the guardian exactly, renames the original successfully, and
   verifies displaced and alias identities, two-link counts, bytes, process/
   stream closure, and complete native/range ownership cleanup.

The probe uses no retry or sleep. It performs no second close-phase write. The
fixture remains byte-for-byte M186's fixed-name, argument-free, shell-free
child. The two-byte sequence is a controlled test-only protocol condition, not
a production cleanup action.

## Security consequence

The unchanged child consumes the invalid first byte, rejects it, and exits
without treating the trailing valid close byte as an overriding command. The
observed two-link state persists and the guardian's live no-delete-share handle
still refuses rename of the original name. This proves only one fixture's fixed
leading-byte rejection; it does not supply framing, ownership, rollback, or
recovery.

This is a three-process, same-principal observation under one parent-owned
process tree: parent coordinator, guardian child, and mutator child. It is not
general message framing, not arbitrary malformed input, not partial or
separate-write evidence, and not cross-principal, duplicated/inherited-writer,
unrelated-session, hostile-process, simultaneous-race, crash-consistency,
power-loss, or durable-commit evidence.

A future design must still decide authenticated root ownership, explicit
message framing, link enumeration and policy, use-time identity/count
revalidation, durable intent, generation provenance, quarantine, idempotency,
rollback/reconciliation, and typed recovery receipts. ReFS, SMB, other drivers
and hosts, cross-volume behavior, file-ID reuse, other failure phases, and
independent-host proof remain unresolved.

No runtime or package surface changes. No production subprocess, native API,
cache mutation, dependency, workflow, permission, or hosted allocation is
added. No hosted check is added. Windows is not admitted.

## Revisit criteria

Revisit Windows admission only after a design supplies authenticated authority,
explicit framing, trusted root ownership, a hard-link policy, use-time identity
and link-count revalidation, durable generation and recovery state, typed
receipts, cross-principal adversarial evidence, and independent-host proof.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: named-pipe type and read modes](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-type-read-and-wait-modes)
- [Microsoft: `WriteFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [Python: `io`](https://docs.python.org/3/library/io.html)
- [RFC-0175](../rfcs/0175-probe-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-after-recreate.md)
