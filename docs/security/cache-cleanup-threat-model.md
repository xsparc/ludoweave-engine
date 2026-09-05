# Asset-cache cleanup threat model

- **Status:** Accepted design constraint; cleanup remains unimplemented
- **Milestone:** M147
- **Date:** 2026-08-27
- **Scope:** A future local asset-cache cleanup boundary

## Purpose and current boundary

This threat model defines what must be true before LudoWeave can design an
asset-cache mutation. It grants no cleanup authority. M137-M145 produce
read-only aggregate evidence and M146 explains why that evidence cannot
identify safe deletion candidates. There is currently no cleanup command,
candidate API, retention engine, background collector, or delete path.

The protected outcome is narrow: a future cleanup must never delete a retained
or newly published object, escape the selected cache root, silently lose
recovery evidence, or turn path-free diagnostics into sensitive path output.

## Assets

- the exact selected cache root and its separation from the project root;
- content-addressed blobs and action metadata, including objects being read or
  published;
- retained roots: current actions, admitted generations, leases, pins,
  in-flight readers and writers, and recovery state;
- exact candidate identities and the policy inputs that made them eligible;
- future quarantine state, mutation receipts, and rollback evidence; and
- path-free public diagnostics and the confidentiality of local filesystem
  layout.

## Actors and trust boundaries

The initiating caller and composition root may request a future bounded
operation but must not choose arbitrary deletion paths. The engine process
owns validation, policy, locking, mutation, receipts, and recovery. Same-user
processes may concurrently read or publish cache entries and cannot be assumed
quiescent. Filesystem namespace components, symlinks, hard links, Windows
junctions and other reparse points may change after observation. Existing cache
files and saved evidence are inputs, not trusted authority.

No remote attacker or remote cache is assumed. Local influence still matters:
an untrusted or concurrently modified cache tree can cross the validation-to-
use boundary. Operating-system path and handle semantics differ across Windows,
macOS, and Linux, so a portable string-prefix check is not a safety proof.

## Entry points and data flow

Today, cache planning, publication, inspection, realization, population,
inventory, fingerprints, comparisons, and previews are explicit and bounded.
The M137-M145 outputs omit candidate paths and never invoke mutation. A future
design would add a separate authority flow:

1. admit an exact cache root, complete observation, retained roots, and policy;
2. acquire an exclusive writer/quiescence capability;
3. derive bounded identity-bearing candidates without granting path authority;
4. revalidate root, generation, identity, and eligibility at use;
5. move eligible objects into same-filesystem quarantine before reclamation;
6. durably record a typed mutation receipt and recovery state; and
7. finalize or roll back using an explicit idempotent state machine.

Every step remains prospective. Dry-run evidence and mutation authority must be
different types and commands.

## Threats and required controls

| ID | Threat or misuse case | Required control and verification |
| --- | --- | --- |
| CCT-01 | A time-of-check/time-of-use race changes reachability or identity between observation and mutation. | Hold an exclusive writer or generation-bound quiescence capability through candidate derivation and use; revalidate identity and retained roots at the mutation point; fail closed on any change. |
| CCT-02 | A symlink, junction, mount, or other reparse point is substituted so deletion escapes the cache root. | Use platform-proven handle-relative, no-follow traversal and deletion; reject unsupported namespace components. String normalization or `resolve()` alone is insufficient. |
| CCT-03 | Hard links or filesystem aliases make one apparent cache object refer to data outside the intended ownership boundary. | Specify ownership and link-count policy, reject ambiguous aliases, and test platform-specific behavior before mutation is admitted. |
| CCT-04 | A concurrent reader or writer races cleanup, losing an in-use object or publishing metadata that refers to reclaimed content. | Include readers, writers, leases, pins, and publication/recovery state in retained roots; enforce a cross-process exclusion protocol and adversarial interleavings. |
| CCT-05 | Missing, malformed, duplicate, or corrupt metadata makes the retained-root set incomplete. | Strictly bound and validate every admitted record; reject the whole mutation on incomplete or inconsistent metadata rather than guessing. |
| CCT-06 | Stale, replayed, forged, or unauthenticated saved evidence is mistaken for current authorization. | Bind evidence to exact protocol, cache generation, root identity, policy, and operation nonce; saved evidence remains advisory unless freshly admitted under the mutation capability. |
| CCT-07 | Clock rollback, skew, or an untrusted timestamp makes an object appear older than it is. | Define one explicit trusted-time source and monotonicity/rollback policy; age alone never grants eligibility; test discontinuity and unavailable-time behavior. |
| CCT-08 | Crash, cancellation, disk-full, access denial, or power loss leaves half-applied deletion or false success. | Use a durable staged state machine, same-filesystem quarantine, write-ahead recovery evidence, typed per-object outcomes, and restart tests at every transition. |
| CCT-09 | An overbroad root, case-folding error, alternate data stream, reserved name, or normalization mismatch expands scope. | Admit one canonical root capability, enforce platform-specific component rules, bound candidate count/bytes, and reject project/cache overlap or ambiguous paths. |
| CCT-10 | Retry or replay double-deletes, reclaims a replacement object, or emits conflicting receipts. | Bind idempotency to operation and object identity, compare the object at use, and make repeated terminal recovery deterministic. |
| CCT-11 | Quarantine or rollback state is tampered with, replaced, or garbage-collected prematurely. | Authenticate and bind recovery records, confine quarantine to the selected filesystem, define retention, and require explicit restore/finalize receipts. |
| CCT-12 | Candidate identities, project paths, environment values, or user data leak through diagnostics and receipts. | Keep public output path-free and bounded, expose only necessary content identities, and apply existing credential-shaped value redaction. |

## Security invariants

All of these invariants are mandatory; no individual control is sufficient.

1. Read-only M137-M145 aggregate evidence never authorizes mutation.
2. Dry-run and mutation are separately typed, capability-gated operations.
3. Every candidate is identity-bearing and bound to an exact admitted cache
   root, generation, retained-root set, policy, and operation.
4. The implementation holds exclusive writer/quiescence authority and
   revalidates with handle-relative, no-follow semantics at use. A platform
   without proven semantics fails closed.
5. Candidate count, aggregate bytes, record sizes, and work are bounded before
   mutation begins.
6. Reclamation stages through same-filesystem quarantine and emits durable,
   immutable, canonical receipts for success, refusal, partial failure,
   recovery, restore, and finalize outcomes.
7. Project/cache separation, deterministic ordering, privacy/redaction, and
   explicit ownership/close behavior remain intact.
8. Cleanup adds no ambient network access, arbitrary Python evaluation, global
   engine singleton, or unowned background thread.

## Verification requirements

An implementation RFC must map every threat and invariant to focused tests and
must include, at minimum:

- Windows, macOS, and Linux installed-wheel tests using each platform's actual
  link/reparse and handle semantics;
- adversarial swaps before and after observation, retained-root computation,
  quarantine, receipt persistence, restore, and finalize;
- concurrent readers, writers, leases, pins, publication, retry, and crash
  schedules with deterministic coordination rather than timing sleeps;
- malformed and stale evidence, generation mismatch, trusted-time rollback,
  quota/grace boundaries, candidate limits, disk-full, and permission failure;
- proof that mutation never follows a link, crosses the cache root, overlaps
  the project root, or deletes a replacement object;
- deterministic, canonical, path-free receipts and bounded diagnostics; and
- recovery from every durable phase with no success claim before durable
  completion.

The implementation review must also preserve exact dependency direction,
engine-owned backend isolation, least-privilege CI, reproducible pure-Python
artifacts, and the full supported-Python acceptance matrix.

## Residual risk and admission status

Same-user adversaries may have authority that cannot be safely contained by a
portable Python deletion implementation. Platform support must therefore be an
evidence-backed capability, not an assumption. Filesystem or process failure
can also prevent progress; safe refusal and recoverable quarantine are valid
outcomes.

M147 accepts this model as a future design constraint and does not implement
cleanup. Candidate disclosure, retention policy, locking, trusted time,
quarantine, receipts, mutation, repair, remote cache, or background collection
remain deferred.

## References

- [MITRE CWE-367: Time-of-check Time-of-use Race Condition](https://cwe.mitre.org/data/definitions/367.html)
- [Python 3.12 `shutil.rmtree` documentation](https://docs.python.org/3.12/library/shutil.html#shutil.rmtree)
- [Microsoft reparse points](https://learn.microsoft.com/en-us/windows-hardware/drivers/ifs/reparse-points)
- [Bazel remote caching](https://bazel.build/remote/caching)
