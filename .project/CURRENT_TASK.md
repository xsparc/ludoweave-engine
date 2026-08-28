# Current task

- **Task:** M159 - probe one native late write to a child-owned Windows
  blocker's closed control pipe without admitting a recovery or error-code
  contract.
- **Status:** Local M159 acceptance is complete through primary-source
  direction, implementation, architecture protection, supported-Python
  behavior, full regression, packaging, release rehearsal, repeated live-host
  execution, findings-first review, DCO commit, and exact object audit. A fresh
  hosted audit still exposes only M99 `main`, so publication is withheld rather
  than exposing the absent local stack.
- **Base:** Fully locally validated M158 DCO commit
  `9061edfe4fd04685a57425bb049834a9fc1bffd5`, tree
  `e182978ba1e735d014205b04b24853951bae950e`, sole parent exact M157.
- **Branch:** `release/m159-broken-control-pipe-write`.

## Acceptance boundary

- Accept RFC-0142 and retain one Windows-only, test-only native late-write
  observation confined to pytest temporary storage.
- Reuse M155's exact child-owned blocker, fixed launch, bounded readiness, and
  failure cleanup without modifying the helper.
- Reuse M154's unchanged native rename child; require false/32 while the
  blocker owner remains alive.
- Kill the blocker once, complete M155's bounded wait with a nonzero result,
  and require stdout/stderr EOF before the late write.
- Map the existing parent stdin descriptor to its Windows handle and call
  `WriteFile` exactly once with M155's one-byte release token. Require false,
  exact `ERROR_NO_DATA` 232, and zero bytes written.
- Close the parent writer explicitly, then invoke the identical native rename
  once and require true/0 with content preserved.
- Protect exact runtime, examples, scripts, dependencies, workflows, and
  M158's boundary with automated architecture tests.
- Add no helper, runtime subprocess or `ctypes`, public probe, recovery,
  production adapter, cache access, cleanup authority, dependency, workflow,
  or CI allocation.

## Direction evidence

- Microsoft documents `WriteFile` pipe failure and separately defines
  `ERROR_NO_DATA` 232 as "the pipe is being closed."
- Python documents `BrokenPipeError`, subprocess pipes, and buffered binary
  I/O, but the live buffered fixture produced `OSError(errno.EINVAL)` rather
  than the hypothesized exception. M159 records only the direct native result.
- GitHub documents that matrix combinations create job allocations. M159 uses
  only the existing Windows suite and adds no hosted allocation.
- Exact M158 history and a clean worktree were established before this branch.
  Exact ancestry allowed the contained M158 branch to be pruned; only local
  `main` and active M159 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, source-tree `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No Python exception-mapping contract, universal Windows error-code contract,
  arbitrary pipe failure, partial or multiple writes, retry or recovery,
  concurrent race, selected native-call interleaving, general cross-process
  exclusion, duplicated-handle behavior, oplock protocol, quiescence, timeout,
  close failure, cancellation, restart recovery, dependency, version,
  workflow/CI, permission, credential, release, tag, or repository-publication
  implementation.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
- The M159 postcommit audit found hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, no open PR, and no hosted
  milestone branch. The condition is not met, so no push or PR is created.
