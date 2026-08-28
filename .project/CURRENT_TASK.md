# Current task

- **Task:** M165 - prove an already-created inherited-handle blocker child is
  closed and reaped before one injected noninheritability-restoration error
  escapes, while the parent retains explicit repair duty and denial until
  close.
- **Status:** Local M165 acceptance and DCO closeout are complete. Exact M165
  scratch artifacts are removed. The final hosted-state audit still exposes
  only M99, so push and PR publication are safely withheld.
- **Base:** Fully locally validated M164 DCO commit
  `70ca584aeda0f0f718ef83438e67b3422acde184`, tree
  `1e20cd0aaa929c2ce35b604834b24798e266e4b4`, sole parent exact M163.
- **Branch:** `release/m165-inherited-restore-failure`.

## Acceptance boundary

- Accept RFC-0148 and retain one Windows-only, test-only, serial injected
  restoration-failure ownership observation confined to pytest temporary
  storage.
- Use M163's unchanged successful-child fixture and launch helper; preserve
  M164 and every earlier accepted fixture byte-for-byte.
- Delegate the initial inheritable transition to the real setter, permit one
  real child creation with exactly the already-approved handle allowlist, and
  inject one fixed exception before the first native `False` transition for
  the exact parent blocker handle.
- Observe and delegate M163's unchanged close-and-reap call exactly once before
  the helper re-raises the identical injected exception and returns no process.
- Require one terminal child, closed stdin/stdout/stderr streams, the parent
  handle still inheritable, and parent owned count one after propagation.
- In caller `finally`, use the captured original setter to repair
  noninheritability and close any unexpectedly returned process.
- Require repaired noninheritability, M154's unchanged false/error 32 native
  rename with namespace/content preserved until the parent handle closes
  exactly once, then owned count zero and the identical second rename's
  true/code-zero result.
- Protect exact runtime, examples, scripts, dependencies, workflows, and
  M164's boundary with automated architecture tests.
- Add no runtime subprocess or `ctypes`, public probe, timeout or recovery
  policy, production adapter, cache access, cleanup authority, dependency,
  workflow, or CI allocation.

## Direction evidence

- Python documents explicit Windows handle-inheritability access and mutation.
- Microsoft documents that `SetHandleInformation` can fail with extended error
  information; M165 injects before that call because no safe deterministic real
  failure is available for a valid owned handle.
- Process reclamation and parent-flag repair remain separate ownership duties;
  observing a terminal child does not imply restored parent inheritability.
- Python's concurrent-process warning leaves concurrent inheritance and leak-
  freedom unresolved. M165 accepts only one serial injected observation.
- GitHub documents that matrix combinations create job allocations. M165 uses
  only the existing Windows suite and adds no hosted allocation.
- Exact M164 history and a clean worktree were established before this branch.
  Exact ancestry allowed the contained M164 branch to be pruned; only local
  `main` and active M165 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, package `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No real native restoration failure, arbitrary restoration or process-
  creation failure coverage, broad or concurrent inheritance contract,
  invalid inherited-handle result, child crash, cross-process duplication or
  transfer, native close failure, leak-freedom under concurrent launches,
  recovery, retry, general exclusion, oplock protocol, quiescence, dependency,
  version, workflow/CI, permission, credential, release, tag, or repository-
  publication implementation.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
- The M165 preimplementation audit found hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, no open PR, PR #251 as the
  newest merge, and no hosted milestone branch. The condition was not met at
  implementation start.
- Initial DCO commit `b8892a75006c55f003faddd0a68ae50f79a75eb9`
  has tree `9f2c7a7cfa19920a544c511eb5b994c748e6bcd6`, sole parent exact M164,
  exact configured maintainer identity, one DCO sign-off, exactly 16 intended
  paths, no merge commit, clean worktree, expected `0 66` divergence from
  local M99 main, and only local `main` plus M165. Full object checking exited
  zero, reported historical dangling objects only, and found no corruption or
  missing object. This factual closeout is being folded into the same local
  commit before publication.
- Pre-record amended commit
  `12977dacfa8744632312f1b679b95cb185b78a88` has tree
  `83243e90f3eb00fac6db3475795b40bd6d555587`, sole parent exact M164,
  exact maintainer identity, one DCO sign-off, the same 16 intended paths, no
  merge commit, clean worktree, expected `0 66` divergence, and only local
  `main` plus M165. Whitespace passes. This factual checkpoint is being folded
  into the same local commit before publication.
- Post-record checkpoint `dd99c222e064aacf53aa3d0c3d53ecf485c1445f`
  has tree `b7c42dc9c1ce6e6b45dd7a4408340563ef28b3d6`, sole parent exact M164,
  exact maintainer identity, one DCO sign-off, the same 16 intended paths, no
  merge commit, clean worktree, expected `0 66` divergence, and only local
  `main` plus M165. All fourteen exact M165 scratch targets were resolved
  beneath repository `.tmp`, removed, and verified absent.
- A final fetch/prune leaves hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, the sole hosted branch.
  Authenticated GitHub queries report no open PR and PR #251 as the newest
  merge at that exact commit. Publishing M165 would expose the absent M100-
  M165 stack, so no push, PR, workflow allocation, tag, or release occurred.
