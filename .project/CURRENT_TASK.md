# Current task

- **Task:** M168 - prove concurrent explicit-list isolation when one real
  Windows launch succeeds and one real missing-executable launch fails.
- **Status:** Local M168 acceptance, DCO closeout, and hosted publication audit
  are complete. Exact scratch artifacts are removed. Hosted `main` still lacks
  M100-M168, so push and PR publication are safely withheld.
- **Base:** Fully locally validated M167 DCO commit
  `dc3a1d154b4706518a0abb7e09f0531230e7de11`, tree
  `d46020c720b5890d2959a7f0dab3a526c752d196`, sole parent exact M166.
- **Branch:** `release/m168-concurrent-launch-failure-isolation`; exact
  containment allowed the redundant M167 branch to be pruned.

## Acceptance boundary

- Accept RFC-0151 and retain one Windows-only, test-only, event-controlled
  successful/missing-executable explicit-list interleaving beneath pytest
  temporary storage.
- Preserve M163's fixed child helper and fixture, M164's real launch-failure
  helper, and M167's complete boundary byte-for-byte.
- Use distinct no-delete-share parent handles for two ordinary roots and cover
  both A/B success/failure assignments.
- Require both handles inheritable before either launch, both real outcomes
  before either helper returns, and both restoration entries while both flags
  remain true.
- Capture the successful process immediately and preserve the exact returned
  `FileNotFoundError` with `errno.ENOENT` and Windows error 2.
- After both parent handles close, require the failed-launch root to rename
  immediately while the successful child's distinct root remains denied until
  that child acknowledges close and exits zero.
- Preserve both payloads and settle every event, thread, handle, process, and
  stream through bounded cleanup.
- Add no runtime subprocess or `ctypes`, public probe, global launch lock,
  dependency, workflow, job, permission, or CI allocation.

## Direction evidence

- Python documents parent-side child-start failures, temporary inheritability
  for Windows `handle_list`, and the public `close_fds=True` requirement.
- Current CPython delegates to Win32 process creation and closes parent-side
  pipe copies in `finally`; Microsoft documents failure as a zero return and
  recommends explicit handle lists for simultaneous creators needing distinct
  handles.
- M167 proves only the all-success pair. One controlled success/failure pair
  can resolve the exact ownership question without implying general concurrent
  process-creation safety.
- GitHub documents one job per matrix combination. M168 preserves the existing
  essential workflow and creates no new hosted allocation.
- NIST SSDF supports the bounded risk-driven evidence slice.

## Development evidence so far

- Exact M167 was clean. The corrected M149-M167 baseline passed 121 assertions
  with one established skip; static and dated governance returned zero
  findings. Hosted `main` remained exact M99 with no open PR.
- Initial formatting requested one mechanical change. Ruff and strict Pyright
  passed; the first combined documentation guard rejected an ambiguous split
  nonclaim phrase, which was reflowed. The corrected focused gate passed eight
  architecture/live assertions and strict docs.
- The complete M149-M168 group passes 129 assertions with one established skip.
  Twenty explicit consecutive invocations pass all 40 parametrized live cases.
- The unchanged lock and exact graphics environment pass. All 518 Python files
  pass formatting, Ruff, and strict Pyright.
- An accidentally overlapping broad pytest invocation left `.pytest-tmp`
  inaccessible and produced one setup error after 3,821 passes. The verified
  non-reparse scratch directory was removed; the serial rerun on CPython
  3.12.13 passes 3,822 tests with 17 skips. Isolated CPython 3.13.13 and 3.14.5
  pass 3,812 tests with 18 skips each.
- Ten real-wgpu tests pass. Fresh one-repeat base and graphics profiles validate
  two and three workloads. Clockwork Arena and Agent World Builder reproduce
  their established deterministic identities.
- Two development builds are byte-identical: a 360,675-byte pure wheel at
  SHA-256 `c25614dc8a6b46923b68acfdea738eee79ae496d293badefcdeda6c66eff4e48`
  and a 2,054,633-byte source archive at SHA-256
  `b4905073c762ea4875126c7ec6e3d2dc8b53cb5885e23c0524b611997e088aa5`.
  All 28 installed-wheel consumers pass.
- Two independent ten-artifact release stages are byte-identical and pass
  complete release smoke. Inventory is 114 wheel and 831 source entries with
  no native/WASM/bytecode, no M168 wheel entry, and all four M168 sources in the
  source archive.

## Closeout

- The initial DCO commit has exact M167 parent, 16 intended paths, configured
  maintainer identity, one sign-off, no merge, clean objects, and a clean
  worktree; this factual record is folded into that same local commit.
- Fresh fetch and authenticated GitHub queries confirm hosted `main` remains
  M99, no PR is open, and PR #251 is the newest merge. Publishing would expose
  M100-M168, so no push or PR occurs.
- M168 is complete locally. Do not begin M169 in this milestone.
