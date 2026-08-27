# Current task

- **Task:** M156 - probe one abrupt child-owned Windows share-delete blocker
  termination without admitting runtime recovery or a platform adapter.
- **Status:** Local M156 acceptance is complete through primary-source
  direction, implementation, architecture protection, supported-Python
  behavior, full regression, packaging, release rehearsal, repeated live-host
  execution, and findings-first review. Publication remains conditioned on a
  fresh audit of the final DCO-signed branch commit and the preceding local
  stack on hosted `main`.
- **Base:** Fully locally validated M155 DCO commit
  `40aee9c75a8d10bc9876869788b9e39db73c1151`, tree
  `1383b854ba3bc10c79dec0b01894500b459368c4`, sole parent exact M154.
- **Branch:** `release/m156-abrupt-blocker-termination`.

## Acceptance boundary

- Accept RFC-0139 and retain one Windows-only, test-only forced-termination
  observation confined to pytest temporary storage.
- Reuse M155's exact child-owned blocker, fixed launch, bounded readiness, and
  failure cleanup without modifying the helper.
- Reuse M154's unchanged native rename child; require false/32 while the
  blocker owner remains alive.
- Send no release token, force termination, wait with M155's fixed timeout,
  require a nonzero but not numerically standardized exit, and receive no
  `closed` acknowledgement.
- Invoke the identical rename once after the bounded wait and require true/0.
- Preserve namespace/content through denial and after the successful rename.
- Protect exact runtime, examples, scripts, dependencies, workflows, and
  M155's boundary with automated architecture tests.
- Add no helper, runtime subprocess or `ctypes`, public probe, recovery,
  production adapter, cache access, cleanup authority, dependency, workflow,
  or CI allocation.

## Direction evidence

- Microsoft documents that open kernel-object handles close automatically when
  a process terminates and that `TerminateProcess` is asynchronous for an
  external caller, requiring an explicit process wait.
- Python documents that `Popen.kill()` maps to `TerminateProcess` on Windows
  and supports bounded `wait(timeout=...)`.
- GitHub documents that matrix combinations create job allocations. M156 uses
  only the existing Windows suite and adds no hosted allocation.
- Exact M155 history and a clean worktree were established before this branch.
  Exact ancestry allowed the contained M155 branch to be pruned; only local
  `main` and active M156 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, source-tree `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No concurrent race, selected native-call interleaving, universal Windows
  error-code contract, general cross-process exclusion, duplicated-handle
  behavior, oplock protocol, quiescence, close-failure or restart recovery,
  dependency, version, workflow/CI, permission, credential, release, tag, or
  repository-publication implementation.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
