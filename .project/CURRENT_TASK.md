# Current task

- **Task:** M161 - probe one acknowledged release intent while a child-owned
  Windows blocker deliberately retains its native rename denial, without
  admitting graceful-close recovery or platform support.
- **Status:** Local M161 acceptance is complete through primary-source
  direction, implementation, architecture protection, supported-Python
  behavior, full regression, packaging, release rehearsal, repeated live-host
  execution, findings-first review, DCO commit, and exact object audit. A fresh
  hosted audit still exposes only M99 `main`, so publication is withheld rather
  than exposing the absent local stack.
- **Base:** Fully locally validated M160 DCO commit
  `2ef87449a23b05e637b876cdee238cc58b10bd10`, tree
  `88ebbabe1115d78c72791a1a81c08b4356d5f957`, sole parent exact M159.
- **Branch:** `release/m161-acknowledged-release-timeout`.

## Acceptance boundary

- Accept RFC-0144 and retain one Windows-only, test-only acknowledged-release
  process-wait observation confined to pytest temporary storage.
- Add one fixed child fixture with separate `!` release-intent and `.` close
  tokens; preserve every earlier fixture unchanged.
- Require exact `ready`, M154's false/32, exact `release-held` while the native
  handle remains open, one `Popen.wait(timeout=0.0)` yielding exact
  `TimeoutExpired`, and the identical false/32 denial afterward.
- Require the child return code to remain unset and the child to remain alive
  throughout the held phase.
- Send the distinct close token once, require exact `closed`, child exit zero,
  output EOF, and the identical third native rename's true/0 result with
  content preserved.
- Protect exact runtime, examples, scripts, dependencies, workflows, and
  M160's boundary with automated architecture tests.
- Add no runtime subprocess or `ctypes`, public probe, timeout or recovery
  policy, production adapter, cache access, cleanup authority, dependency,
  workflow, or CI allocation.

## Direction evidence

- Python documents that `Popen.wait(timeout)` raises `TimeoutExpired` while a
  process remains live and that catching the exception before a later wait is
  safe.
- Microsoft documents anonymous pipes as byte streams requiring an application
  protocol, and that share options remain effective until the associated
  handle closes.
- GitHub documents that matrix combinations create job allocations. M161 uses
  only the existing Windows suite and adds no hosted allocation.
- Exact M160 history and a clean worktree were established before this branch.
  Exact ancestry allowed the contained M160 branch to be pruned; only local
  `main` and active M161 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, package `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No actual graceful-close timeout contract, nonzero timeout guarantee,
  cancellation, kill policy, native close-failure result, crash or restart
  recovery, retry, concurrent race, general cross-process exclusion,
  duplicated-handle behavior, oplock protocol, quiescence, dependency,
  version, workflow/CI, permission, credential, release, tag, or repository-
  publication implementation.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
- The M161 postcommit audit found hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, no open PR, and no hosted
  milestone branch. The condition is not met, so no push or PR is created.
