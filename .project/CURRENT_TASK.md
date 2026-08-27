# Current task

- **Task:** M155 - prove one explicitly synchronized child-owned Windows
  share-delete denial/release transition without admitting a runtime adapter.
- **Status:** Local M155 acceptance is complete through primary-source
  direction, implementation, architecture protection, supported-Python
  behavior, full regression, packaging, release rehearsal, repeated live-host
  execution, and findings-first review. Publication remains conditioned on a
  fresh audit of the final DCO-signed branch commit and the preceding local
  stack on hosted `main`.
- **Base:** Fully locally validated M154 DCO commit
  `e831a1cc098ea22d94cd87c7f7d9cf785012d97e`, tree
  `4a48a85386eae6745c32ee16ccd6e0a583143b5e`, sole parent exact M153.
- **Branch:** `release/m155-child-owned-share-delete-handshake`.

## Acceptance boundary

- Accept RFC-0138 and retain one Windows-only, test-only child-owned blocker
  confined to pytest temporary storage.
- Open ordinary `live` in the child with M153's exact nonzero directory access
  mask, read/write sharing, and no delete sharing.
- Emit bounded exact-schema `ready`, accept exactly one fixed release byte,
  close the non-inheritable native handle in `finally`, and emit bounded
  exact-schema `closed` only after successful close.
- Keep every parent wait bounded; terminate, wait for, and close the child on
  every failure path.
- Reuse M154's unchanged native rename child; require false/32 while the blocker
  owner remains alive and true/0 only after acknowledged close.
- Preserve namespace/content through denial and after the successful rename.
- Protect exact runtime, examples, scripts, dependencies, workflows, and
  M154's boundary with automated architecture tests.
- Add no runtime subprocess or `ctypes`, public probe, production adapter,
  cache access, cleanup authority, dependency, workflow, or CI allocation.

## Direction evidence

- Microsoft documents that each handle's share options remain effective until
  close regardless of process context and that delete access includes rename.
- Microsoft documents the two conditions required for handle inheritance; the
  child supplies `NULL` security attributes and the parent uses
  `close_fds=True`.
- Python documents bounded subprocess timeouts and pipe behavior. The child
  emits only two bounded lines and reads one fixed byte rather than a command.
- An initial metadata-only prototype allowed the rename. The corrected child
  uses M153's exact nonzero access mask and observes false/32 before its
  acknowledged close and true/0 afterward.
- Exact M154 history and a clean worktree were established before this branch.
  Exact ancestry allowed the contained M154 branch to be pruned; only local
  `main` and active M155 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, source-tree `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No concurrent race, selected native-call interleaving, universal Windows
  error-code contract, general cross-process exclusion, duplicated-handle
  behavior, oplock protocol, quiescence, recovery, dependency, version,
  workflow/CI, permission, credential, release, tag, or repository-publication
  implementation.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
