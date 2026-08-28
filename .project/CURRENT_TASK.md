# Current task

- **Task:** M170 - prove abrupt-exit isolation for two concurrently created
  Windows explicit-handle-list children.
- **Status:** Local M170 acceptance, DCO closeout, scratch cleanup, and hosted
  publication audit are complete. Hosted `main` still lacks M100-M170, so push
  and PR publication are safely withheld.
- **Base:** Fully locally validated M169 DCO commit
  `3707e1bfe38b3fa21f66183dbe827888bb6e24ea`, tree
  `0eaaa689072049f80bafc65d289e2d1eede80339`, sole parent exact M168.
- **Branch:** `release/m170-concurrent-abrupt-child-isolation`; exact
  containment allowed the redundant M169 branch to be pruned.

## Acceptance boundary

- Accept RFC-0153 and retain one Windows-only, test-only, event-controlled
  concurrent explicit-list abrupt-termination observation beneath pytest
  temporary storage.
- Preserve M156's forced-termination boundary, M163's helper and child fixture,
  M167's pairwise isolation boundary, and M169's complete boundary byte-for-
  byte.
- Start two real children simultaneously with distinct one-handle lists and
  require both parent flags to remain inheritable through both creations and
  both restoration entries.
- Restore both flags, close both parent handles, and require both roots to
  remain denied while both children remain live.
- Kill one assigned child with real Windows `Popen.kill()`, establish its
  nonzero exit with a bounded wait, require pipe EOF with no graceful `closed`
  acknowledgement, and require only that root to rename.
- Keep the survivor live and its root denied until its existing acknowledged
  zero-exit close. Cover both A/B abrupt/survivor assignments and preserve both
  payloads.
- Settle every event, queue, thread, handle, process, and stream through bounded
  cleanup.
- Add no runtime subprocess or `ctypes`, public probe, process-global launch
  lock, dependency, workflow, job, permission, or CI allocation.

## Direction evidence

- Python documents that Windows `Popen.kill()` aliases `terminate()`, which
  calls `TerminateProcess`, while bounded `wait()` establishes termination and
  records the return code.
- Microsoft documents external `TerminateProcess` as asynchronous and requires
  a process wait to establish completion. Its process-creation guidance
  recommends explicit handle lists when inheritance is required.
- M156 proves abrupt termination for one child-owned blocker and M167 proves
  graceful isolation for two inherited blockers. Their controlled combination
  resolves the remaining pairwise abrupt-exit ownership question without
  changing production code.
- GitHub documents one job per matrix combination. M170 preserves the existing
  essential workflow and creates no new hosted allocation.
- NIST SSDF supports the bounded risk-driven evidence slice.

## Development evidence so far

- Exact M169 was clean. The M149-M169 baseline passed 138 assertions with one
  established skip; static and dated strict governance returned zero findings.
  Hosted `main` remained exact M99 with no open PR.
- The final focused gate passes seven architecture guards plus two live A/B
  cases. The M149-M170 boundary passes 147 assertions with one established
  skip. Twenty consecutive invocations pass all 40 live cases.
- The unchanged lock and exact graphics environment pass. All 522 Python files
  pass formatting, Ruff, and strict Pyright.
- CPython 3.12.13 passes 3,840 tests with 17 skips; isolated CPython 3.13.13 and
  3.14.5 each pass 3,830 tests with 18 skips.
- Ten real-wgpu tests, both one-repeat profile schemas, Clockwork Arena, and
  Agent World Builder pass with established deterministic identities.
- Two development builds are byte-identical: a 360,806-byte pure wheel at
  SHA-256 `882adb7a7f000ac1c59a4a18c3fbf21852fcdbb0f16b5b8e0683b03c9537caa1`
  and a 2,068,678-byte source archive at SHA-256
  `d74a8c6eaf0258fe30cc0143ad7b564eaa5416521362e0cd6612f4a53b43c2f2`.
  All 28 installed-wheel consumers pass.
- Two ten-artifact release stages are byte-identical and pass complete release
  smoke. Inventory is 114 wheel and 839 source entries with no public
  development-tool disclosure and all four M170 sources source-only.
- Static and dated strict governance return zero findings. Protected runtime,
  helpers, fixtures, examples, scripts, workflows, metadata, dependencies, and
  prior milestone boundaries have zero diff; no actionable finding is known.

## Closeout

- The initial DCO commit has exact M169 parent, 16 intended paths, configured
  maintainer identity, one sign-off, no merge, clean objects, and a clean
  worktree; this factual record is folded into that same local commit.
- Fresh fetch and authenticated GitHub queries confirm hosted `main` remains
  M99, no PR is open, and PR #251 is the newest merge. Publishing would expose
  M100-M170, so no push or PR occurs.
- M170 is complete locally. Continue with only one separately bounded,
  explicitly governed milestone.
