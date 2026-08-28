# Current task

- **Task:** M164 - prove one real missing-executable Windows process-creation
  failure restores a temporarily allowlisted blocker handle to
  noninheritable while preserving parent ownership and denial until close.
- **Status:** Local M164 acceptance and DCO closeout are complete. Exact M164
  scratch artifacts are removed. The final hosted-state audit still exposes
  only M99, so push and PR publication are safely withheld.
- **Base:** Fully locally validated M163 DCO commit
  `86ba05218f8bae79153677e8c6fae200a61f019f`, tree
  `c945019b831f2e13e1afb8046ab5f6664ee1cbfd`, sole parent exact M162.
- **Branch:** `release/m164-inherited-launch-failure`.

## Acceptance boundary

- Accept RFC-0147 and retain one Windows-only, test-only, serial real process-
  creation failure observation confined to pytest temporary storage.
- Prove the fixed executable path is absent; do not create a child fixture or
  executable and preserve every earlier fixture unchanged.
- Open one noninheritable no-delete-share directory handle, place only that
  handle in `STARTUPINFO.lpAttributeList`, and require `close_fds=True`.
- Temporarily mark the handle inheritable, call the fixed missing executable as
  both sole argument and explicit executable with `shell=False`, trusted
  working directory, and `DEVNULL` standard streams, then restore
  noninheritability in `finally`.
- Require exact current-host `FileNotFoundError`, errno `ENOENT`, Windows error
  2, no returned process owner, restored noninheritability, parent owned count
  one, and the missing path still absent.
- Require M154's unchanged false/error 32 native rename with namespace/content
  preserved until the parent handle closes exactly once, then owned count zero
  and the identical second rename's true/code-zero result.
- Close and reap any unexpectedly created process before failing, including if
  restoration then raises.
- Protect exact runtime, examples, scripts, dependencies, workflows, and
  M163's boundary with automated architecture tests.
- Add no runtime subprocess or `ctypes`, public probe, timeout or recovery
  policy, production adapter, cache access, cleanup authority, dependency,
  workflow, or CI allocation.

## Direction evidence

- Python documents that a non-empty Windows explicit handle list requires
  `close_fds=True`, listed handles must be temporarily inheritable, and process-
  creation inputs can raise `OSError` subclasses.
- Microsoft documents that `CreateProcessW` returns zero on failure and exposes
  extended error information, while explicit handle lists avoid broad
  inheritance.
- Python warns that temporary inheritability can leak during concurrent process
  creation. M164 therefore accepts only one serial failure observation and
  rejects concurrency-safe inheritance or general rollback claims.
- GitHub documents that matrix combinations create job allocations. M164 uses
  only the existing Windows suite and adds no hosted allocation.
- Exact M163 history and a clean worktree were established before this branch.
  Exact ancestry allowed the contained M163 branch to be pruned; only local
  `main` and active M164 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, package `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No restoration-failure injection, arbitrary process-creation failure
  coverage, broad or concurrent inheritance contract, invalid inherited-
  handle result, child crash, cross-process duplication/transfer, native close
  failure, leak-freedom under concurrent launches, recovery, retry, general
  exclusion, oplock protocol, quiescence, dependency, version, workflow/CI,
  permission, credential, release, tag, or repository-publication
  implementation.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
- The M164 preimplementation audit found hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, no open PR, PR #251 as the
  newest merge, and no hosted milestone branch. The condition was not met at
  implementation start.
- Initial DCO commit `a7bdea7cf7a988678b7fe21d21ce0b189213f504`
  has tree `e59fcfb77afd1cc10fe005a275afab70f76f4170`, sole parent exact M163,
  exact configured maintainer identity, one DCO sign-off, exactly 16 intended
  paths, no merge commit, clean worktree, expected `0 65` divergence from
  local M99 main, and only local `main` plus M164. Full object checking exited
  zero and reported historical dangling objects only. This factual closeout
  is being folded into the same local commit before publication.
- Pre-record amended commit
  `0381c5b59d1b1b92eba6dff28b4149783626d622` has tree
  `a563a087e1f95f234b9c5c7e4927d7e648389b8d`, sole parent exact M163,
  exact maintainer identity, one DCO sign-off, the same 16 intended paths, no
  merge commit, clean worktree, expected `0 65` divergence, and only local
  `main` plus M164. Whitespace passes. This factual checkpoint is being folded
  into the same local commit before publication.
- Post-record checkpoint `d89c77deb474a86907e5858ad36f8ed0828c5013`
  has tree `97b11680ef9b14339801a2d60eb21f466542e636`, sole parent exact M163,
  exact maintainer identity, one DCO sign-off, the same 16 intended paths, no
  merge commit, clean worktree, expected `0 65` divergence, and only local
  `main` plus M164. All ten exact M164 scratch targets were resolved beneath
  repository `.tmp`, removed, and verified absent.
- A final fetch/prune leaves hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, the sole hosted branch.
  Authenticated GitHub queries report no open PR and PR #251 as the newest
  merge at that exact commit. Publishing M164 would expose the absent M100-
  M164 stack, so no push, PR, workflow allocation, tag, or release occurred.
