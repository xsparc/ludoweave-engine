# Windows hard-link alias mutator repeated buffered close after delivery failure probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M196
- **Date:** 2026-08-29
- **Baseline:** M195's direct buffered-close delivery-failure boundary

## Decision

Retain one Windows-only, test-only NTFS observation showing local stream
disposition after M195's direct buffered-close delivery failure. M195's first
`close()` remains the delivery attempt: it raises generic `OSError` and leaves
the parent stream closed. A second `close()` on that already closed stream
returns `None`, raises no further error, and leaves the stream closed. It does
not retry delivery and provides no acknowledgement from the child. The peer
alias retains the original identity, bytes, and two-link count while M181's
matching guardian remains live. This controlled test-only stream condition is
not a production cleanup action, and Windows is not admitted.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_repeated_buffered_close_after_delivery_failure_probe.py`:

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
6. delegates M195's exact `?!` invalid settlement, terminal output, late `!`
   buffer acceptance, generic first-close `OSError`, and final closed state to
   the byte-for-byte protected M195 helper;
7. requires the stream already closed, calls `close()` exactly once more,
   requires the second `close()` to return `None`, and requires the stream
   still closed; then requires the guardian live, alias present, shared
   identity/bytes/count/ranges unchanged, and exact-name rename still refused;
   and
8. releases the guardian exactly, renames the original successfully, and
   verifies displaced and alias identities, two-link counts, bytes, process/
   stream closure, and complete native/range ownership cleanup.

The probe uses no retry or sleep, no operation other than `close()` after the
first close, and no `communicate()`. It reuses M195's helper, M186's byte-for-
byte fixed-name, argument-free, shell-free child, and M193's bounded-output
ordering.

## Security consequence

The first `close()` error establishes failed pending-byte delivery and the
first closed-state observation establishes local resource disposition. The
second `close()` returns `None` only because the stream is already closed; it
does not retry delivery, restore the lost byte, or establish peer receipt. No
acknowledgement is created. The observed two-link state persists and the
guardian's live no-delete-share handle still refuses rename of the original
name.

This is a three-process, same-principal observation under one parent-owned
process tree: parent coordinator, guardian child, and mutator child. It is not
general framing, arbitrary buffered-input, partial-write, arbitrary closed-
stream-operation, unbounded-output, duplicated/inherited-writer, cross-
principal, unrelated-session, hostile-process, simultaneous-race, crash-
consistency, power-loss, or durable-commit evidence.

A future design must still decide authenticated root ownership, explicit
framing, bounded I/O, acknowledgements/receipts, link enumeration and policy,
use-time identity/count revalidation, durable intent and generation
provenance, quarantine, idempotency, rollback/reconciliation, and typed
recovery receipts. ReFS, SMB, other drivers and hosts, cross-volume behavior,
file-ID reuse, other failure phases, and independent-host proof remain
unresolved.

No runtime or package surface changes. No production subprocess, native API,
cache mutation, dependency, workflow, permission, or hosted allocation is
added. No hosted check is added. Windows is not admitted.

## Revisit criteria

Revisit Windows admission only after a design supplies authenticated
authority, explicit framing, bounded I/O, acknowledged delivery, trusted root
ownership, a hard-link policy, use-time identity and link-count revalidation,
durable generation and recovery state, typed receipts, cross-principal
adversarial evidence, and independent-host proof.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: pipe handle inheritance](https://learn.microsoft.com/en-us/windows/win32/ipc/pipe-handle-inheritance)
- [Microsoft: `WriteFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile)
- [Python: buffered I/O](https://docs.python.org/3/library/io.html)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [RFC-0179](../rfcs/0179-probe-windows-hard-link-alias-mutator-repeated-buffered-close-after-delivery-failure.md)
