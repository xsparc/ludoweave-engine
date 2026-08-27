# Current task

- **Task:** M153 - execute a test-only cross-process share-delete exclusion and
  release probe without admitting a runtime adapter.
- **Status:** Local M153 acceptance is complete through primary-source
  direction, implementation, architecture protection, supported-Python
  behavior, full regression, packaging, release rehearsal, and findings-first
  review. Publication remains conditioned on a fresh audit of the final
  DCO-signed branch commit and the preceding local stack on hosted `main`.
- **Base:** Fully locally validated M152 DCO commit
  `44953ff23ed84a50cdeed47c4564ebbc45c8447a`, tree
  `163d5b6568e2f117dbe98c859e5ae93c1d1f6f6b`, sole parent exact M151.
- **Branch:** `release/m153-windows-share-delete-exclusion`.

## Acceptance boundary

- Accept RFC-0136 and retain one Windows-only, test-only NTFS share-delete
  fixture confined to pytest temporary storage.
- Open one ordinary directory with read/write sharing but without delete
  sharing; keep that native handle private to the parent process.
- Require one fixed, direct, non-inheriting child rename to fail while that
  handle is open and leave namespace/content unchanged.
- Close the blocking handle deterministically and require the identical child
  command to succeed, with the unchanged candidate under the renamed parent.
- Protect exact runtime, examples, scripts, dependencies, workflows, and
  M152's boundary with automated architecture tests.
- Add no runtime subprocess or `ctypes`, concurrent timing, public probe,
  production adapter, cache access, cleanup authority, dependency, workflow,
  or CI allocation.

## Direction evidence

- Microsoft documents that sharing options remain effective until handle close
  regardless of process context; omitting `FILE_SHARE_DELETE` prevents later
  delete-access opens, and delete access includes rename.
- Microsoft documents fixed directory `ren` behavior and `cmd /d /c`; Python
  documents `close_fds=True` as preventing retained handle inheritance.
- The current focused test reports NTFS, observes nonzero child exit with the
  blocker open, closes that handle, and observes zero exit from the identical
  child command with unchanged candidate bytes.
- Exact M152 history and a clean worktree were established before this branch.
  Exact ancestry allowed the contained M152 branch to be pruned; only local
  `main` and active M153 remain.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, source-tree `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No general cross-process exclusion, controlled concurrent race, selected
  native-call interleaving, direct child native-error capture, oplock protocol,
  quiescence, dependency, version, workflow/CI, permission, credential,
  release, tag, or repository-publication implementation is added by this
  slice.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
