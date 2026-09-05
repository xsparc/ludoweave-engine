# Windows hard-link alias mutator buffered-close delivery failure after invalid settlement probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M195
- **Date:** 2026-08-29
- **Baseline:** M194's late valid-close flush-delivery boundary

## Decision

Retain one Windows-only, test-only NTFS observation showing that one late valid
close byte can be accepted into a parent-side buffer after M186's unchanged
child has already settled, while delivery fails on direct stream close without
a preceding failed late flush. Buffer acceptance is not peer receipt. The
exact Python exception subtype and numeric translation are deliberately
outside the boundary: require only generic `OSError`, with no exact Python
exception code, and require the stream closed afterward. The child emits no
`closed` event, and the peer alias retains the original identity, bytes, and
two-link count while M181's matching guardian remains live. This controlled
test-only protocol condition is not a production cleanup action, and Windows
is not admitted.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_buffered_close_delivery_failure_after_invalid_settlement_probe.py`:

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
6. writes and flushes `?!` exactly once, leaves the writer open, and requires
   bounded child exit 5, stdout EOF, empty stderr, and no `closed` event;
7. after the child has already settled, writes one late valid close byte and
   requires the parent buffer to accept one byte;
8. without an intervening late `flush()`, calls `close()` directly, requires
   delivery to fail with generic `OSError`, makes no exact code assertion, and
   requires the stream closed; then requires the guardian live, alias present,
   shared identity/bytes/count/ranges unchanged, and exact-name rename still
   refused; and
9. releases the guardian exactly, renames the original successfully, and
   verifies displaced and alias identities, two-link counts, bytes, process/
   stream closure, and complete native/range ownership cleanup.

The probe uses no retry or sleep, no pre-settlement second write, and no
`communicate()`. It reuses M186's byte-for-byte fixed-name, argument-free,
shell-free child and M193's bounded-output ordering. It observes only one late
buffered byte after terminal settlement.

## Security consequence

The buffered `write()` byte count establishes only local buffer acceptance.
The direct close failure establishes that pending-byte delivery was attempted
after the child's read handle closed. The final closed state establishes local
resource disposition despite the delivery exception. None of these results is
an acknowledgement, receipt, or proof of child execution. The observed
two-link state persists and the guardian's live no-delete-share handle still
refuses rename of the original name.

This is a three-process, same-principal observation under one parent-owned
process tree: parent coordinator, guardian child, and mutator child. It is not
general framing, arbitrary buffered-input, partial-write, unbounded-output,
duplicated/inherited-writer, cross-principal, unrelated-session,
hostile-process, simultaneous-race, crash-consistency, power-loss, or durable-
commit evidence.

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
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [Python: buffered I/O](https://docs.python.org/3/library/io.html)
- [Python: built-in exceptions](https://docs.python.org/3/library/exceptions.html)
- [RFC-0178](../rfcs/0178-probe-windows-hard-link-alias-mutator-buffered-close-delivery-failure-after-invalid-settlement.md)
