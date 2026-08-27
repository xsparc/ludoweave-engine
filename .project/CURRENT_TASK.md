# Current task

- **Task:** M151 - execute a test-only retained-parent namespace substitution
  without admitting a runtime adapter.
- **Status:** Local M151 acceptance is complete through primary-source
  direction, implementation, architecture protection, supported-Python
  behavior, full regression, packaging, release rehearsal, and findings-first
  review. Publication remains conditioned on a fresh audit of the final
  DCO-signed branch commit and the preceding local stack on hosted `main`.
- **Base:** Fully locally validated M150 DCO commit
  `42cac8b6ade92af3bb29bbd2e9781cb0799ddc58`, tree
  `08156f9bc9e8d86175c77c2ae15b4929e8096956`, sole parent exact M149.
- **Branch:** `release/m151-windows-retained-parent-substitution`.

## Acceptance boundary

- Accept RFC-0134 and retain one Windows-only, test-only NTFS namespace-
  substitution fixture confined to pytest temporary storage.
- Retain an opened parent across rename, rebind its former name to a junction,
  refuse fresh traversal, and prove relative opens remain bound to the renamed
  original identity rather than the substitution target.
- Protect exact runtime, scripts, dependencies, workflows, and M150's boundary
  with automated architecture tests.
- Add no runtime shelling or `ctypes`, concurrent timing, public probe,
  production adapter, cache access, cleanup authority, dependency, workflow,
  or CI allocation.

## Direction evidence

- Microsoft documents persistent opened file objects, handle-relative names,
  delete sharing for rename access, and volume/file identity comparison.
- The first corrected current-host test retains `live`, renames it to
  `displaced`, creates a junction at the former name, refuses that fresh name,
  and distinguishes the original and target file identities.
- Exact M150 history and clean worktree were established before this branch.
  Exact ancestry allowed the contained M150 branch to be pruned; only local
  `main` and active M151 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, source-tree `ctypes` or
  shelling, retained-root implementation, candidate list, cache read/write,
  remote cache, network, or trusted-time implementation.
- No concurrent/cross-process race, oplock protocol, dependency, version,
  workflow/CI, permission, credential, release, tag, or repository-publication
  implementation is added by this slice.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
