# Windows cooperative-lock abrupt-settlement probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M176
- **Date:** 2026-08-29
- **Baseline:** M175's continuous protected live-ownership interval

## Decision

Retain one Windows-only, test-only controlled observation showing that abrupt
termination and bounded process wait release only the terminated protected
coordination participant. A surviving participant continues to refuse
pathname substitution and exclusive range ownership. After the final
participant terminates and is reaped, both ownership classes settle. This is
not crash recovery or cleanup authority. Windows is not admitted.

## Why abrupt settlement matters

M175 observes graceful participant release. Microsoft documents that
`TerminateProcess` initiates termination asynchronously, so the parent must
wait for the process before relying on completion. Python's Windows
`Popen.kill()` path uses that termination primitive.

Microsoft also documents that the operating system unlocks outstanding
`LockFileEx` ranges after process termination or file close, while warning that
release can be delayed by available system resources. The probe therefore
records only the exact current host after bounded process wait. It does not
promise immediate release elsewhere.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_cooperative_lock_abrupt_settlement_probe.py`:

1. creates M173's exact ordinary `live/coordination.lock` beneath an NTFS
   pytest root and retains its `FILE_ID_INFO` identity;
2. starts two copies of M175's fixed protected child and requires both shared
   range locks and exact bounded `ready` records;
3. requires M174 substitution refusal/error 32 and M173 exclusive refusal/
   error 33 while both remain live;
4. kills and waits for the first child with the fixed bound, requiring nonzero
   status, stdout EOF after `ready`, empty stderr, and no `closed` record;
5. requires the survivor to remain live and preserve both exact refusals;
6. kills and waits for the survivor with the same abrupt-output checks;
7. without polling or sleeping, acquires/releases exact exclusive ownership
   and requires M174's unchanged substitution child to report `substituted`/0;
8. proves the displaced original retains the captured identity and the
   replacement differs; and
9. preserves exact bytes and settles every handle, process, stream, and parent
   lock owner, including assertion-failure paths.

The probe adds no fixture. It reuses M175's fixed no-argument,
no-environment-value child byte-for-byte.

## Executed evidence

On the current Windows CPython 3.12 NTFS host, both protected participants
first hold the shared range and refuse substitution and exclusive ownership.
After the first participant is killed and reaped, the survivor remains live
and both refusals persist. After the survivor is killed and reaped, exact
exclusive acquire/release succeeds immediately and the unchanged substitution
child renames and replaces the file. The displaced identity equals the
retained original, the replacement differs, both contents remain exact, and
all observed owners settle.

## Security consequence

The observation narrows M175's abrupt-exit gap for one exact current-host
sequence. It does not provide startup or crash recovery, authenticate a later
pathname resolution, bind later processes to a stable generation, or prove a
portable unlock deadline.

Trusted root and coordination identities, generation issuance and retention,
complete participant admission, arbitrary termination timing, process trees,
mapped views, filesystem/driver variation, durable recovery, fail-closed
policy, typed receipts, and independent hosts remain unresolved. The
zero-participant substitution window remains. Windows is not admitted.

## Scope and CI restraint

M176 adds no runtime subprocess or `ctypes`, adapter, lock API, public probe,
cache access, candidate disclosure, cleanup authority, mutation command,
dependency, native extension, compiler requirement, workflow, job,
permission, or CI allocation. The integration probe participates only in the
existing Windows test suite; no hosted check is added.

## References

- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Microsoft: `LockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex)
- [Python: `subprocess`](https://docs.python.org/3.14/library/subprocess.html)
- [M147 cleanup threat model](cache-cleanup-threat-model.md)
- [M170 concurrent abrupt-termination probe](cache-cleanup-windows-concurrent-explicit-abrupt-termination-probe.md)
- [M175 live substitution-exclusion probe](cache-cleanup-windows-cooperative-lock-live-substitution-exclusion-probe.md)
