# Current task

- **Task:** M157 - probe one child-owned Windows share-delete blocker's
  control-pipe EOF cleanup without admitting arbitrary pipe recovery.
- **Status:** Local M157 acceptance is complete through primary-source
  direction, implementation, architecture protection, supported-Python
  behavior, full regression, packaging, release rehearsal, repeated live-host
  execution, and findings-first review. Publication remains conditioned on a
  fresh audit of the final DCO-signed branch commit and the preceding local
  stack on hosted `main`.
- **Base:** Fully locally validated M156 DCO commit
  `b0076e48e6538744a8ffc1909c725d1293d56eba`, tree
  `a3205dd9f139748e9331dd316ed8c9548bb52834`, sole parent exact M155.
- **Branch:** `release/m157-control-pipe-eof-close`.

## Acceptance boundary

- Accept RFC-0140 and retain one Windows-only, test-only control-pipe EOF
  observation confined to pytest temporary storage.
- Reuse M155's exact child-owned blocker, fixed launch, bounded readiness, and
  failure cleanup without modifying the helper.
- Reuse M154's unchanged native rename child; require false/32 while the
  blocker owner remains alive.
- Write no control byte, close only the parent `Popen.stdin`, confirm it is
  closed, and wait with M155's fixed timeout.
- Require the helper's existing fixture exit 4 with no `closed`
  acknowledgement or stderr, then invoke the identical rename once and
  require true/0.
- Preserve namespace/content through denial and after the successful rename.
- Protect exact runtime, examples, scripts, dependencies, workflows, and
  M156's boundary with automated architecture tests.
- Add no helper, runtime subprocess or `ctypes`, public probe, recovery,
  production adapter, cache access, cleanup authority, dependency, workflow,
  or CI allocation.

## Direction evidence

- Microsoft documents that anonymous-pipe reads return when all writer handles
  close and that a child-inherited writer prevents EOF.
- Python documents that `stdin=PIPE` creates a child standard-input pipe,
  `close_fds=True` blocks unrelated Windows handle inheritance while retaining
  explicit standard streams, and `wait(timeout=...)` supplies a bound.
- GitHub documents that matrix combinations create job allocations. M156 uses
  only the existing Windows suite and adds no hosted allocation.
- Exact M156 history and a clean worktree were established before this branch.
  Exact ancestry allowed the contained M156 branch to be pruned; only local
  `main` and active M157 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, source-tree `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No concurrent race, selected native-call interleaving, universal Windows
  error-code contract, general cross-process exclusion, duplicated-handle
  behavior, oplock protocol, quiescence, wrong-token or broken-pipe write,
  timeout, close-failure, cancellation, or restart recovery, dependency,
  version, workflow/CI, permission, credential, release, tag, or repository-
  publication implementation.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
