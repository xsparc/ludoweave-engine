# Current task

- **Task:** M162 - prove one same-process duplicate retains a child-owned
  Windows no-delete-share rename denial after the original handle closes,
  without admitting inherited handles, cleanup policy, or platform support.
- **Status:** Local M162 acceptance is complete through
  primary-source direction, implementation, architecture protection,
  supported-Python behavior, full regression, packaging, release rehearsal,
  40 repeated live-host executions, findings-first review, and final
  evidence-inclusive source/package closure, DCO commit, exact object audit,
  and the final publication-safety recheck. Hosted `main` still ends at M99,
  so push and PR publication are withheld rather than exposing the absent
  M100-M162 stack.
- **Base:** Fully locally validated M161 DCO commit
  `d0cac5376e4c67c2e1609b1e2119df28a8e057e3`, tree
  `8a79445ed45c39b6c1bcbc3a4bbef31f6886a850`, sole parent exact M160.
- **Branch:** `release/m162-duplicated-handle-retention`.

## Acceptance boundary

- Accept RFC-0145 and retain one Windows-only, test-only same-process
  duplicated-handle observation confined to pytest temporary storage.
- Add one fixed child fixture that opens a no-delete-share directory handle and
  creates a noninheritable same-access duplicate; preserve every earlier
  fixture unchanged.
- Require exact `ready` only after both handles exist and M154's unchanged
  native rename returns false/error 32.
- Send fixed byte `1` once, require the original handle to close exactly once,
  exact `original-closed`, a live child, and the identical false/error 32
  denial with namespace and content unchanged.
- Send fixed byte `2` once, require the duplicate to close exactly once, exact
  `closed`, child exit zero, output EOF, and the identical third native
  rename's true/code-zero result with content preserved.
- Protect exact runtime, examples, scripts, dependencies, workflows, and
  M161's boundary with automated architecture tests.
- Add no runtime subprocess or `ctypes`, public probe, timeout or recovery
  policy, production adapter, cache access, cleanup authority, dependency,
  workflow, or CI allocation.

## Direction evidence

- Microsoft documents that `DuplicateHandle` creates a distinct handle to the
  same object, `DUPLICATE_SAME_ACCESS` preserves access, and duplication
  increases the object's reference count.
- Microsoft documents that `CloseHandle` decrements the handle count, each
  opened handle should be closed once, and share options remain effective
  until the associated handle closes.
- GitHub documents that matrix combinations create job allocations. M162 uses
  only the existing Windows suite and adds no hosted allocation.
- Exact M161 history and a clean worktree were established before this branch.
  Exact ancestry allowed the contained M161 branch to be pruned; only local
  `main` and active M162 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, package `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No inherited-handle behavior, cross-process duplication or transfer, general
  handle-count contract, native duplicate/close-failure result, crash or
  restart recovery, retry, concurrent race, general cross-process exclusion,
  oplock protocol, quiescence, dependency, version, workflow/CI, permission,
  credential, release, tag, or repository-publication implementation.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
- The M162 preimplementation and postcommit audits found hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, no open PR, and no hosted
  milestone branch. PR #251 remains the newest merge. The condition is not
  met, so no push, PR, workflow allocation, tag, or release is created.
