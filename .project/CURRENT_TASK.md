# Current task

- **Task:** M152 - execute a test-only cross-process retained-parent namespace
  substitution without admitting a runtime adapter.
- **Status:** Local M152 acceptance is complete through primary-source
  direction, implementation, architecture protection, supported-Python
  behavior, full regression, packaging, release rehearsal, and findings-first
  review. Publication remains conditioned on a fresh audit of the final
  DCO-signed branch commit and the preceding local stack on hosted `main`.
- **Base:** Fully locally validated M151 DCO commit
  `3df94f419f14e230275d4dd38ee9f0bcb53b49f6`, tree
  `f1035e580e2f827390c99ef9b15690c003229bde`, sole parent exact M150.
- **Branch:** `release/m152-windows-cross-process-substitution`.

## Acceptance boundary

- Accept RFC-0135 and retain one Windows-only, test-only NTFS child-process
  substitution fixture confined to pytest temporary storage.
- Keep the retained directory handle private to the parent; use one fixed,
  direct, non-inheriting child command to rename and install the junction.
- Refuse fresh traversal and prove the retained parent remains bound to the
  renamed original identity rather than the substitution target.
- Protect exact runtime, scripts, dependencies, workflows, and M151's boundary
  with automated architecture tests.
- Add no runtime subprocess or `ctypes`, concurrent timing, public probe,
  production adapter, cache access, cleanup authority, dependency, workflow,
  or CI allocation.

## Direction evidence

- Microsoft documents delete sharing across process contexts, handle
  inheritance controls, direct process creation, `cmd /d /c`, success-gated
  `&&`, directory `ren`, and junction `mklink /j`.
- The corrected current-host test uses `shell=False`, `close_fds=True`, a fixed
  command string, a trusted working directory, and a bounded timeout.
- The parent retains `live`; the child renames it to `displaced` and creates the
  junction; fresh traversal refuses it; retained/original and target file
  identities remain distinct.
- Exact M151 history and clean worktree were established before this branch.
  Exact ancestry allowed the contained M151 branch to be pruned; only local
  `main` and active M152 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, source-tree `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No controlled concurrent race, cross-process exclusion, oplock protocol,
  quiescence, dependency, version, workflow/CI, permission, credential,
  release, tag, or repository-publication implementation is added by this
  slice.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
