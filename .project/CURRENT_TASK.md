# Current task

- **Task:** M166 - prove one controlled concurrent broad-inheritance launch
  acquires M163's temporarily inheritable blocker and retains native rename
  denial after both parent and intended-child close.
- **Status:** Local M166 acceptance and DCO closeout are complete. Exact M166
  scratch artifacts are removed. The final hosted-state audit still exposes
  only M99, so push and PR publication are safely withheld.
- **Base:** Fully locally validated M165 DCO commit
  `5ec5e79330c5798e13424dfea5a11522b6c93f7a`, tree
  `4e10da2a5f9dcc012cd175362b716c1863902e8c`, sole parent exact M164.
- **Branch:** `release/m166-concurrent-inheritance-leak`; exact containment
  allowed the redundant M165 branch to be pruned.

## Acceptance boundary

- Accept RFC-0149 and retain one Windows-only, test-only, event-controlled
  concurrent broad-inheritance hazard observation beneath pytest temporary
  storage.
- Preserve M163's explicit-list helper and fixed child fixture plus M165's
  complete boundary byte-for-byte.
- Pause only M163's exact explicit-list `Popen` call after its parent blocker
  becomes inheritable and before the intended child is created, using a
  module-local proxy and bounded `threading.Event` coordination.
- During that window, use the captured real `Popen` class to start the same
  fixed child with `close_fds=False`, fixed executable/path arguments,
  `shell=False`, trusted pytest cwd, and owned standard pipes.
- Require the broad child ready/live, release the intended launch, require its
  child ready/live, and require M163's unchanged `finally` to restore the
  parent flag to noninheritable.
- Require M154's unchanged false/error 32 rename before parent close, after
  parent close, and after the intended child acknowledges close and exits zero
  while the broad child remains live.
- Require only the broad child's acknowledged close and zero exit to permit the
  identical fourth rename's true/code-zero result with content preserved.
- In `finally`, release the event gate, join the launch thread, repair
  noninheritability when the parent still owns the handle, and close/reap every
  created child.
- Protect exact runtime, examples, scripts, dependencies, workflows, accepted
  helper/fixture, and M165 boundary through automated architecture tests.
- Add no runtime subprocess or `ctypes`, public probe, global spawn lock,
  recovery policy, production adapter, cache access, cleanup authority,
  dependency, workflow, or CI allocation.

## Direction evidence

- Python warns that temporarily inheritable Windows handles can leak when a
  concurrent process-creation function inherits all handles.
- Microsoft documents that `CreateProcess` with `bInheritHandles=TRUE`
  transfers every inheritable handle and separately recommends explicit handle
  lists for multithreaded callers.
- A controlled real leak observation resolves whether that warning affects the
  exact no-delete-share blocker, but cannot establish a safe concurrency
  contract or select a production coordination design.
- GitHub documents one job per matrix combination. M166 uses only the existing
  Windows suite and adds no hosted allocation.
- NIST's SSDF guidance supports risk-driven scoped evidence rather than an
  unrelated checklist or CI expansion.
- Exact M165 history and a clean worktree were established before this branch.
  Exact ancestry allowed the contained M165 branch to be pruned; only local
  `main` and active M166 remain.

## Development evidence so far

- The baseline M149-M165 probe/boundary group passed 106 assertions with one
  established capability skip in 4.08 seconds. Static governance returned zero
  findings across three objectives, seven requirements, and four work items.
- Fresh fetch/prune and authenticated GitHub queries found hosted `main` at
  exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, no open PR, and PR #251
  as the newest merge at the same commit.
- The first focused implementation run passed formatting and Ruff but strict
  Pyright rejected two unnecessary casts; the same casts caused a runtime
  `TypeError` after a shared-module test double replaced `Popen`.
- Removing the casts cleared strict typing. The next live run reached the
  native observer but exposed that replacing `Popen` on the shared subprocess
  module also affected `subprocess.run`. A module-local `SimpleNamespace`
  proxy corrected that isolation defect.
- The first behaviorally complete run then reached every ordered ownership
  assertion but final cleanup queried the already-released parent handle and
  received expected Windows error 6. Tracking exact parent release avoids
  querying an invalid handle. The corrected live probe passes once in 0.66
  seconds and strict Pyright reports zero findings.
- Findings-first review then found that a body assertion could fail after the
  explicit launch succeeded but before its queued process owner was consumed.
  `finally` now drains that pending result and closes it. Post-probe assertions
  require the thread settled, both children at exit zero, and all streams
  closed. The final seven-assertion focused gate and 20 repeated live
  executions pass.
- All 514 Python files, Ruff, strict Pyright, strict docs, static and dated
  governance, the 113-assertion M149-M166 group with one established skip, and
  metadata/scope/public-hygiene checks pass.
- Exact CPython 3.12.13 passes 3,806 tests with 17 skips; 3.13.13 and 3.14.5
  each pass 3,796 tests with 18 skips. Real wgpu, both profiles, Clockwork
  Arena, and Agent World Builder pass with established deterministic
  identities.
- Two development builds are byte-identical. The primary and all 27 additional
  installed-wheel consumers pass. Two byte-identical ten-artifact release
  stages pass complete release smoke. Development archive inventory is 114
  wheel and 823 source entries, with zero native/WASM/bytecode and exactly the
  four M166 sources present only in the source archive.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, package `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No concurrency-safe inheritance contract, general leak census or leak-
  freedom claim, process-global lock, arbitrary process creator, simultaneous
  explicit-list launch, cancellation/failure interleaving, real restoration
  failure, invalid inherited value, child crash, cross-process duplication or
  transfer, native close failure, recovery, retry, general exclusion, oplock
  protocol, quiescence, dependency, version, workflow/CI, permission,
  credential, release, tag, or repository-publication implementation.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
- The M166 preimplementation audit found hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, no open PR, PR #251 as the
  newest merge, and no hosted milestone branch. The condition is not met at
  implementation start.
- Initial DCO commit `95a560d9b8a7ff89d724394ca1cd30fbd3578c07`
  has tree `7f1793047b73ac5a7ca83524cf6b19e1c87f7d04`, sole parent exact M165,
  exact configured maintainer identity, one DCO sign-off, exactly 16 intended
  paths, no merge commit, clean worktree, expected `0 67` divergence from local
  M99 main, and only local `main` plus M166. Full object checking exits zero
  with no reported corruption or missing object. This factual checkpoint is
  being folded into the same local commit before publication.
- A final fetch/prune leaves hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, the sole hosted branch.
  Authenticated GitHub queries report no open PR and PR #251 as the newest
  merge at that exact commit. Publishing M166 would expose the absent M100-
  M166 stack, so no push, PR, workflow allocation, tag, or release occurred.
