# Current task

- **Task:** M160 - probe one immediate wait timeout while a child-owned
  Windows blocker and its native rename denial remain live, without admitting
  timeout recovery or platform support.
- **Status:** Local M160 acceptance is complete through primary-source
  direction, implementation, architecture protection, supported-Python
  behavior, full regression, packaging, release rehearsal, repeated live-host
  execution, findings-first review, DCO commit, and exact object audit. A fresh
  hosted audit still exposes only M99 `main`, so publication is withheld rather
  than exposing the absent local stack.
- **Base:** Fully locally validated M159 DCO commit
  `78837a61695a38207f06ca474f50f58d9bb9c62e`, tree
  `0fcd74bfa70210e2944e7a43da45bddf136f7082`, sole parent exact M158.
- **Branch:** `release/m160-live-wait-timeout`.

## Acceptance boundary

- Accept RFC-0143 and retain one Windows-only, test-only zero-duration process
  wait observation confined to pytest temporary storage.
- Reuse M155's exact child-owned blocker, fixed launch, bounded readiness,
  graceful release/acknowledgement, and failure cleanup without modifying the
  helper.
- Reuse M154's unchanged native rename child; require false/32 before and after
  the immediate wait while the blocker owner remains alive.
- Call `Popen.wait(timeout=0.0)` exactly once and require exact
  `TimeoutExpired`, the fixed child arguments and timeout, an unset return
  code, and a still-live child.
- Use the existing graceful release exactly once, require `closed` and exit
  zero, then invoke the identical native rename a third time and require
  true/0 with content preserved.
- Protect exact runtime, examples, scripts, dependencies, workflows, and
  M159's boundary with automated architecture tests.
- Add no helper, runtime subprocess or `ctypes`, public probe, timeout policy,
  recovery, production adapter, cache access, cleanup authority, dependency,
  workflow, or CI allocation.

## Direction evidence

- Python documents that `Popen.wait(timeout)` raises `TimeoutExpired` while a
  process remains live and that catching the exception before another wait is
  safe.
- Microsoft documents that a zero-millisecond wait returns immediately with
  `WAIT_TIMEOUT` for a nonsignaled process object.
- GitHub documents that matrix combinations create job allocations. M160 uses
  only the existing Windows suite and adds no hosted allocation.
- Exact M159 history and a clean worktree were established before this branch.
  Exact ancestry allowed the contained M159 branch to be pruned; only local
  `main` and active M160 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, source-tree `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No timeout recovery contract, nonzero timeout guarantee, readiness or close
  timeout, cancellation, kill policy, native close failure, crash or restart
  recovery, retry, concurrent race, selected native-call interleaving, general
  cross-process exclusion, duplicated-handle behavior, oplock protocol,
  quiescence, dependency, version, workflow/CI, permission, credential,
  release, tag, or repository-publication implementation.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
- The M160 postcommit audit found hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, no open PR, and no hosted
  milestone branch. The condition is not met, so no push or PR is created.
