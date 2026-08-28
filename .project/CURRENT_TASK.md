# Current task

- **Task:** M169 - prove concurrent explicit-list isolation when both Windows
  launches succeed but one helper's handle restoration is injected to fail.
- **Status:** Local M169 acceptance, DCO closeout, scratch cleanup, and hosted
  publication audit are complete. Hosted `main` still lacks M100-M169, so push
  and PR publication are safely withheld.
- **Base:** Fully locally validated M168 DCO commit
  `54a123e59e8d5905750c2946786dedd534181884`, tree
  `d874891d313de33d0924717d0d88cef7e027f985`, sole parent exact M167.
- **Branch:** `release/m169-concurrent-restore-failure-isolation`; exact
  containment allowed the redundant M168 branch to be pruned.

## Acceptance boundary

- Accept RFC-0152 and retain one Windows-only, test-only, event-controlled
  concurrent explicit-list restoration-failure observation beneath pytest
  temporary storage.
- Preserve M163's helper and child fixture, M165's restoration-failure boundary,
  and M168's complete boundary byte-for-byte.
- Use distinct no-delete-share parent handles for two ordinary roots and cover
  both A/B survivor/failure assignments.
- Require both handles inheritable through both real child creations and both
  restoration entries; inject one exact failure before its native reset.
- Require M163 to close and reap only the failed side's created child before
  propagating the same error; the survivor must remain ready and live.
- Explicitly repair the failed parent flag. After both parent handles close,
  require the failed-restoration root to rename immediately while the
  survivor's root remains denied until that child acknowledges close and exits
  zero.
- Preserve both payloads and settle every event, thread, handle, process, and
  stream through bounded cleanup.
- Add no runtime subprocess or `ctypes`, public probe, global launch lock,
  dependency, workflow, job, permission, or CI allocation.

## Direction evidence

- Python documents temporary inheritability and `close_fds=True` for a nonempty
  Windows explicit handle list, while `os.set_handle_inheritable` owns the
  parent-side flag transition.
- Current CPython brackets platform process creation with the caller's flag
  changes. Microsoft documents `SetHandleInformation` failure independently
  from successful `CreateProcessW` ownership and recommends explicit handle
  lists for concurrent creators needing distinct handles.
- M165 proves one synthetic post-creation restore failure in isolation; M168
  proves one concurrent launch failure. Neither resolves the exact two-created-
  child, one-restore-failure ownership question.
- GitHub documents one job per matrix combination. M169 preserves the existing
  essential workflow and creates no new hosted allocation.
- NIST SSDF supports the bounded risk-driven evidence slice.

## Development evidence so far

- Exact M168 was clean. The M149-M168 baseline passed 129 assertions with one
  established skip; static and dated strict governance returned zero findings.
  Hosted `main` remained exact M99 with no open PR.
- The final focused gate passes seven architecture guards plus two live A/B
  cases. The M149-M169 boundary passes 138 assertions with one established
  skip. Twenty confirmed consecutive invocations pass all 40 live cases.
- The unchanged lock and exact graphics environment pass. All 520 Python files
  pass formatting, Ruff, and strict Pyright.
- CPython 3.12.13 passes 3,831 tests with 17 skips; isolated CPython 3.13.13 and
  3.14.5 each pass 3,821 tests with 18 skips.
- Ten real-wgpu tests, both one-repeat profile schemas, Clockwork Arena, and
  Agent World Builder pass with established deterministic identities.
- Two development builds are byte-identical: a 360,741-byte pure wheel at
  SHA-256 `9ff47422741836517d580f90316e48adca7f14091da9beb315f05ea2bc6db346`
  and a 2,061,195-byte source archive at SHA-256
  `7100a495e860f2a48b1fd1f6efa3c3fddc24d15860382f40168452f1f6090ed0`.
  All 28 installed-wheel consumers pass.
- Two ten-artifact release stages are byte-identical and pass complete release
  smoke. Inventory is 114 wheel and 835 source entries with no native, WASM,
  or bytecode, no M169 wheel entry, and all four M169 sources in the archive.

## Closeout

- The initial DCO commit has exact M168 parent, 16 intended paths, configured
  maintainer identity, one sign-off, no merge, clean objects, and a clean
  worktree; this factual record is folded into that same local commit.
- Fresh fetch and authenticated GitHub queries confirm hosted `main` remains
  M99, no PR is open, and PR #251 is the newest merge. Publishing would expose
  M100-M169, so no push or PR occurs.
- M169 is complete locally. Continue with only one separately bounded,
  explicitly governed milestone.
