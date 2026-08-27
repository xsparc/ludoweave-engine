# Current task

- **Task:** M150 - execute a test-only Windows directory-junction refusal
  without admitting a runtime adapter.
- **Status:** Local M150 acceptance is complete through primary-source
  direction, implementation, architecture protection, supported-Python
  behavior, full regression, packaging, release rehearsal, and findings-first
  review. Publication remains conditioned on a fresh audit of the final
  DCO-signed branch commit and the preceding local stack on hosted `main`.
- **Base:** Fully locally validated M149 DCO commit
  `b9c3a3b38b3cf22cf5351e13b362602d0c46d9eb`, tree
  `5ed1460fd133e81c3738a451f58437c88d9b63f8`, sole parent exact M148.
- **Branch:** `release/m150-windows-junction-refusal-probe`.

## Acceptance boundary

- Accept RFC-0133 and retain one Windows-only, test-only NTFS directory-
  junction fixture confined to pytest temporary storage.
- Bind filesystem/reparse capability to the opened root handle, execute M149's
  reparse refusal, close the rejected handle, and prove link-only cleanup leaves
  the target unchanged.
- Protect exact runtime, scripts, dependencies, workflows, and M149's boundary
  with automated architecture tests.
- Add no runtime shelling or `ctypes`, public probe, production adapter, cache
  access, cleanup authority, dependency, workflow, or CI allocation.

## Direction evidence

- Microsoft documents directory junctions as reparse points, `mklink /j` as the
  junction creator, and `GetVolumeInformationByHandleW` for handle-bound
  filesystem information.
- The corrected current-host test observes NTFS/reparse support, creates one
  junction without elevation, refuses it through M149's retained-handle open,
  closes the rejected handle, and preserves the target marker.
- Exact M149 history and clean worktree were established before this branch.
  Exact ancestry allowed the contained M149 branch to be pruned; only local
  `main` and active M150 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, source-tree `ctypes` or
  shelling, retained-root implementation, candidate list, cache read/write,
  remote cache, network, or trusted-time implementation.
- No dependency, version, workflow/CI, permission, credential, release, tag,
  or repository-publication implementation is added by this slice.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
