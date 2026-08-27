# Current task

- **Task:** M149 - add a test-only Windows cache-cleanup capability probe
  without admitting a runtime adapter.
- **Status:** Implementation, architecture protection, supported-Python and
  installed-package validation, reproducible distribution/release rehearsal,
  archive inspection, findings-first review, final separation, bounded cleanup,
  initial DCO commit, exact local audit, and hosted-state audit are complete.
  Publication is held because authoritative hosted `main` remains exact M99.
- **Base:** Fully locally validated M148 DCO commit
  `4f6b59ef37877ba3575ca19e0f15cfdadcc6a253`, tree
  `6eacc1a7d0a85d66916c011e544a991fd8e7afae`, sole parent exact M147.
- **Branch:** `release/m149-windows-cleanup-capability-probe`.

## Acceptance boundary

- Accept RFC-0132 and retain one Windows-only, test-only native-capability
  probe confined to pytest temporary storage.
- Exercise owned relative opens, reparse refusal, file identity, hard-link
  observation, non-replacing quarantine, disposition, and close semantics.
- Protect exact runtime, scripts, dependencies, workflows, and M148's no-
  admission boundary with automated architecture tests.
- Add no runtime API, public probe, production adapter, cache access, cleanup
  authority, dependency, native extension, compiler requirement, workflow, or
  CI allocation.

## Direction evidence

- Microsoft documents user-mode `NtCreateFile` relative to a retained directory
  handle, `FILE_ID_INFO` identity, native rename information, and handle
  disposition. Exact supported runtimes expose every required system symbol.
- The corrected current-host test preserves identity across quarantine, detects
  hard-link aliases, refuses replacement, deletes on close, and passes nine
  cases. The reparse case skips because symlink creation privilege is absent.
- Exact M148 history, clean worktree, DCO, and object integrity were established
  before this branch. Exact ancestry allowed the contained M148 branch to be
  pruned; only local `main` and active M149 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, source-tree `ctypes`,
  retained-root implementation, candidate list, cache read/write, remote cache,
  network, or trusted-time implementation.
- No dependency, version, workflow/CI, permission, credential, release, tag,
  push, or PR change.

## Remaining acceptance work

- No local M149 acceptance work remains. Keep the milestone unpublished until
  a fresh hosted audit proves the required preceding stack is present; continue
  the next approved research-gated milestone from the exact committed M149 tip.
