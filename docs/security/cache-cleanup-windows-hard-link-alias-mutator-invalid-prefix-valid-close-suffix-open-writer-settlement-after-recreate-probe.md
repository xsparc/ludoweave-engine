# Windows hard-link alias mutator invalid-prefix open-writer settlement after recreation probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M193
- **Date:** 2026-08-29
- **Baseline:** M192's invalid prefix with valid close suffix boundary

## Decision

Retain one Windows-only, test-only NTFS observation showing that M186's
unchanged fixture rejects a fixed invalid prefix with one valid close suffix
after recreation and settles independently of control-pipe EOF. The parent
writer remains open before and after the child exits 5. The child emits no
`closed` event, and the writer is closed only after stdout EOF and empty stderr
are observed. The peer alias retains the original identity, bytes, and
two-link count while M181's matching guardian remains live. This controlled
test-only protocol condition is not a production cleanup action, and Windows
is not admitted.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_hard_link_alias_mutator_invalid_prefix_valid_close_suffix_open_writer_settlement_after_recreate_probe.py`:

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
   flushes, requires the parent writer open, and waits with M186's fixed bound;
7. requires exit 5 while the parent writer remains open, stdout EOF without a
   `closed` event, and empty stderr, then closes the parent writer; and
8. requires the guardian still live, the alias still present, shared identity
   and bytes unchanged, link count two, range availability, rename refusal,
   exact guardian release, post-release rename, and complete resource cleanup.

The probe uses no retry or sleep, no second close-phase write, and no
`communicate()`. It reuses M186's byte-for-byte fixed-name, argument-free,
shell-free child. That bounded-output fixture emits no data after `recreated`
on the invalid path, so the bounded wait cannot fill its stdout or stderr pipes
in this exact sequence. This is not permission to wait before draining
arbitrary subprocess output.

## Security consequence

The unchanged child consumes the invalid first byte, rejects it, and exits
without needing EOF from the still-open control pipe. The trailing valid close
byte does not override rejection. The observed two-link state persists and the
guardian's live no-delete-share handle still refuses rename of the original
name. This establishes only fixed leading-byte rejection and open-writer
settlement for one fixture.

This is a three-process, same-principal observation under one parent-owned
process tree: parent coordinator, guardian child, and mutator child. It is not
general framing, arbitrary malformed-input, partial/separate-write,
unbounded-output, duplicated/inherited-writer, cross-principal,
unrelated-session, hostile-process, simultaneous-race, crash-consistency,
power-loss, or durable-commit evidence.

A future design must still decide authenticated root ownership, explicit
framing, bounded I/O, link enumeration and policy, use-time identity/count
revalidation, durable intent and generation provenance, quarantine,
idempotency, rollback/reconciliation, and typed recovery receipts. ReFS, SMB,
other drivers and hosts, cross-volume behavior, file-ID reuse, other failure
phases, and independent-host proof remain unresolved.

No runtime or package surface changes. No production subprocess, native API,
cache mutation, dependency, workflow, permission, or hosted allocation is
added. No hosted check is added. Windows is not admitted.

## Revisit criteria

Revisit Windows admission only after a design supplies authenticated authority,
explicit framing, bounded I/O, trusted root ownership, a hard-link policy,
use-time identity and link-count revalidation, durable generation and recovery
state, typed receipts, cross-principal adversarial evidence, and independent-
host proof.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: named-pipe type and read modes](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-type-read-and-wait-modes)
- [Microsoft: `WriteFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [Python: `io`](https://docs.python.org/3/library/io.html)
- [RFC-0176](../rfcs/0176-probe-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-open-writer-settlement-after-recreate.md)
