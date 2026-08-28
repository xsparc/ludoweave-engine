# Current task

- **Task:** M163 - prove one explicitly inherited child handle retains a
  Windows no-delete-share rename denial after the parent closes its handle,
  without admitting broad or concurrency-safe inheritance, cleanup policy, or
  platform support.
- **Status:** Local M163 acceptance is complete through primary-source
  direction, architecture protection, supported-Python behavior, full
  regression, 40 repeated live-host executions, real graphics, all installed-
  wheel consumers, release rehearsal, findings-first review, and final
  evidence-inclusive source/package closure and DCO object audit. The fresh
  publication-safety recheck still finds hosted `main` at M99, so push and PR
  publication are withheld rather than exposing the absent M100-M163 stack.
- **Base:** Fully locally validated M162 DCO commit
  `82f39fcccae309db6fde508ed04b468661fcaa6e`, tree
  `a4403cc41c8747581f67e550d57ff80f86b00c39`, sole parent exact M161.
- **Branch:** `release/m163-inherited-handle-retention`.
- **Initial DCO object:** Commit
  `3e27efade29170976695b21a6c7cec09796319ed`, tree
  `96b240f0eac0a3750275e64520e1996009d8371a`, sole parent exact M162, exact
  maintainer author/committer identity, one sign-off, 17 intended paths, no
  merge commit, clean worktree, and expected `0 64` divergence from local M99
  main. This factual closeout is folded into the same local commit before the
  publication audit.
- **Pre-record amended object:** Commit
  `3c1e5f525f3f901c8a7ed5b839e34c446c4624c3`, tree
  `7c39b21a9ce662b1695b5f6c120e6af4351aaf23`, sole parent exact M162, one
  sign-off, the same 17 intended paths, no merge commit, clean worktree, and
  expected `0 64` divergence. This factual closeout is folded into the same
  local commit before the final hosted-state check.

## Acceptance boundary

- Accept RFC-0146 and retain one Windows-only, test-only, serial explicit-
  handle-list observation confined to pytest temporary storage.
- Add one fixed child fixture that accepts exactly one canonical positive
  decimal inherited handle, waits behind an exact byte protocol, and closes
  only that owned handle; preserve every earlier fixture unchanged.
- Place only the blocker handle in `STARTUPINFO.lpAttributeList`, require
  `close_fds=True`, and restore the parent handle to noninheritable immediately
  after process creation.
- Require exact `ready`, M154's unchanged false/error 32 native rename, and
  namespace/content preservation before parent close.
- Close the parent handle exactly once; require owned count zero, a live child,
  and the identical second false/error 32 result while only the inherited
  child handle remains.
- Send fixed byte `!` once; require exact `closed`, child exit zero, output EOF,
  and the identical third native rename's true/code-zero result with content
  preserved.
- If inheritability restoration fails after launch, close and reap the child
  before propagating the failure.
- Protect exact runtime, examples, scripts, dependencies, workflows, and
  M162's boundary with automated architecture tests.
- Add no runtime subprocess or `ctypes`, public probe, timeout or recovery
  policy, production adapter, cache access, cleanup authority, dependency,
  workflow, or CI allocation.

## Direction evidence

- Python documents that Windows `STARTUPINFO.lpAttributeList["handle_list"]`
  explicitly selects inheritable handles for a child, requires
  `close_fds=True`, and requires listed handles to be temporarily inheritable.
- Microsoft documents that an inherited handle refers to the same object with
  the same access and value in the child, and recommends explicit handle lists
  instead of broad inheritance when inheritance is required.
- Python warns that temporary inheritability can leak during concurrent process
  creation. M163 therefore accepts only a serial test observation and rejects
  a concurrency-safe inheritance claim.
- GitHub documents that matrix combinations create job allocations. M163 uses
  only the existing Windows suite and adds no hosted allocation.
- Exact M162 history and a clean worktree were established before this branch.
  Exact ancestry allowed the contained M162 branch to be pruned; only local
  `main` and active M163 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, package `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No broad or concurrent inheritance contract, cross-process duplication or
  transfer, invalid inherited-handle or native close-failure result, leak-
  freedom under concurrent launches, crash/restart recovery, retry, concurrent
  race, general cross-process exclusion, oplock protocol, quiescence,
  dependency, version, workflow/CI, permission, credential, release, tag, or
  repository-publication implementation.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
- The M163 preimplementation audit found hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, no open PR, PR #251 as the
  newest merge, and no hosted milestone branch. The final postcommit refresh
  found the same state and exact `0 64` divergence, so no push, PR, workflow
  allocation, tag, or release is created.
