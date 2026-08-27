# Current task

- **Task:** M158 - probe one child-owned Windows share-delete blocker's fixed
  invalid control token without admitting arbitrary malformed input.
- **Status:** Local M158 acceptance is complete through primary-source
  direction, implementation, architecture protection, supported-Python
  behavior, full regression, packaging, release rehearsal, repeated live-host
  execution, and findings-first review. Publication remains conditioned on a
  fresh audit of the final DCO-signed branch commit and the preceding local
  stack on hosted `main`.
- **Base:** Fully locally validated M157 DCO commit
  `7c28ad99d2d13c64a7d45cdbd9d6f2181eb24c99`, tree
  `985c7a4a50dadb49805dd67a060641eee0dd8c1b`, sole parent exact M156.
- **Branch:** `release/m158-invalid-control-token`.

## Acceptance boundary

- Accept RFC-0141 and retain one Windows-only, test-only fixed invalid-token
  observation confined to pytest temporary storage.
- Reuse M155's exact child-owned blocker, fixed launch, bounded readiness, and
  failure cleanup without modifying the helper.
- Reuse M154's unchanged native rename child; require false/32 while the
  blocker owner remains alive.
- Write exactly one repository-fixed `?` byte, require the buffered write to
  accept it, flush and close `Popen.stdin`, confirm closure, and wait with
  M155's fixed timeout.
- Require the helper's existing fixture exit 4 with no `closed`
  acknowledgement or stderr, then invoke the identical rename once and
  require true/0.
- Preserve namespace/content through denial and after the successful rename.
- Protect exact runtime, examples, scripts, dependencies, workflows, and
  M157's boundary with automated architecture tests.
- Add no helper, runtime subprocess or `ctypes`, public probe, recovery,
  production adapter, cache access, cleanup authority, dependency, workflow,
  or CI allocation.

## Direction evidence

- Microsoft documents that anonymous pipes are byte streams and that writes
  complete after the requested byte count is written or an error occurs.
- Python documents bytes-only binary streams, buffered `flush()`, and
  idempotent stream close behavior.
- GitHub documents that matrix combinations create job allocations. M158 uses
  only the existing Windows suite and adds no hosted allocation.
- Exact M157 history and a clean worktree were established before this branch.
  Exact ancestry allowed the contained M157 branch to be pruned; only local
  `main` and active M158 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, source-tree `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No arbitrary malformed input, partial or multiple writes, broken-pipe write,
  concurrent race, selected native-call interleaving, universal Windows error-
  code contract, general cross-process exclusion, duplicated-handle behavior,
  oplock protocol, quiescence, timeout, close failure, cancellation, or restart
  recovery, dependency, version, workflow/CI, permission, credential, release,
  tag, or repository-publication implementation.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
