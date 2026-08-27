# Current task

- **Task:** M154 - directly capture one Windows native sharing-violation result
  without admitting a runtime adapter.
- **Status:** Local M154 acceptance is complete through primary-source
  direction, implementation, architecture protection, supported-Python
  behavior, full regression, packaging, release rehearsal, and findings-first
  review. Publication remains conditioned on a fresh audit of the final
  DCO-signed branch commit and the preceding local stack on hosted `main`.
- **Base:** Fully locally validated M153 DCO commit
  `f34bf8032c523a60e80711745c2776b5ca6d99ab`, tree
  `df3c460b8afa8ad3ab84327a7ba9685b89436da5`, sole parent exact M152.
- **Branch:** `release/m154-windows-native-sharing-violation`.

## Acceptance boundary

- Accept RFC-0137 and retain one Windows-only, test-only isolated native-rename
  child confined to pytest temporary storage.
- Reuse M153's ordinary NTFS directory handle opened without delete sharing;
  keep that native handle private to the parent process.
- Execute a fixed repository-owned helper with the current interpreter under
  `-I -B`, no `-c`, no caller inputs, no environment-selected behavior, and no
  inherited native handle.
- Capture one strict bounded success/error JSON result directly from
  `MoveFileExW`; require false/32 before close and true/0 after close.
- Preserve namespace/content through denial, prove the post-close rename, and
  close all parent handles deterministically.
- Protect exact runtime, examples, scripts, dependencies, workflows, and
  M153's boundary with automated architecture tests.
- Add no runtime subprocess or `ctypes`, public probe, production adapter,
  cache access, cleanup authority, dependency, workflow, or CI allocation.

## Direction evidence

- Microsoft documents `MoveFileExW`'s zero/nonzero result and immediate
  `GetLastError` path; system error 32 is `ERROR_SHARING_VIOLATION`.
- Microsoft also warns that exact error returns may vary by operating system or
  driver, so M154 records one current-host observation only.
- Python documents `-I` isolation and `close_fds=True` non-inheritance on
  Windows. The fixed child uses a script file rather than inline evaluation.
- The focused current-host probe observed false/32 with the blocker open and
  true/0 after deterministic close, with unchanged candidate bytes.
- Exact M153 history and a clean worktree were established before this branch.
  Exact ancestry allowed the contained M153 branch to be pruned; only local
  `main` and active M154 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, source-tree `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No universal Windows error-code contract, general cross-process exclusion,
  controlled concurrent race, selected native-call interleaving, oplock
  protocol, quiescence, dependency, version, workflow/CI, permission,
  credential, release, tag, or repository-publication implementation.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
