# Current task

- **Task:** M167 - prove pairwise isolation for one controlled pair of
  simultaneous Windows explicit-handle-list launches.
- **Status:** Local M167 acceptance, DCO closeout, and hosted publication audit
  are complete. Exact scratch artifacts are removed. Hosted `main` still lacks
  M100-M167, so push and PR publication are safely withheld.
- **Base:** Fully locally validated M166 DCO commit
  `86b0e49d0d91ab2e134a8d7b9cb247012883fe7e`, tree
  `cb12cc6c6f196d1ee3c605ce94cbbe6b91572316`, sole parent exact M165.
- **Branch:** `release/m167-concurrent-explicit-isolation`; exact containment
  allowed the redundant M166 branch to be pruned.

## Acceptance boundary

- Accept RFC-0150 and retain one Windows-only, test-only, event-controlled
  simultaneous explicit-list isolation observation beneath pytest temporary
  storage.
- Preserve M163's helper and fixed child fixture plus M166's complete boundary
  byte-for-byte.
- Open two distinct noninheritable no-delete-share handles to ordinary
  `a/live` and `b/live` directories beneath one handle-reported NTFS root.
- Use a module-local `os` proxy to require both handles inheritable before
  either worker continues, without changing process-wide `os` bindings.
- Use a separate module-local subprocess proxy to validate a one-handle list,
  `close_fds=True`, `shell=False`, corresponding trusted root, and owned pipes,
  then allow both captured-real `Popen` calls to complete while both parent
  flags remain true.
- Require both helpers waiting at restoration while both flags are still true,
  release both exact restore calls, join both threads, and require both flags
  false plus both children ready/live.
- Require M154's false/error 32 rename for both roots before and after both
  parent handles close.
- Exercise child release orders A-to-B and B-to-A; after the first child closes,
  require only its root to rename successfully while the other remains denied,
  then require the second root to succeed after its child closes.
- Preserve both distinct payloads and settle every thread, parent handle,
  child process, and pipe stream through bounded cleanup.
- Add no runtime subprocess or `ctypes`, global launch lock, public probe,
  dependency, workflow, job, permission, or CI allocation.

## Direction evidence

- Python documents that a non-empty Windows `handle_list` requires
  `close_fds=True`, temporarily inheritable handles, and caution around
  concurrent broad-inheritance creators.
- Microsoft documents that broad `CreateProcessW` inheritance is problematic
  for simultaneous creators that need different handles and recommends
  `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` for explicit selection.
- M166 proves the adverse broad-inheritance case. One controlled simultaneous
  explicit-list pair can now resolve pairwise isolation for the exact blocker,
  but cannot establish a general concurrency-safe process-creation contract.
- GitHub documents one job per matrix combination. M167 uses only the existing
  Windows suite and adds no hosted allocation.
- NIST SSDF guidance supports this risk-driven bounded evidence slice instead
  of unrelated CI expansion.

## Development evidence so far

- M166 was clean at exact DCO commit `86b0e49d0d91ab2e134a8d7b9cb247012883fe7e`.
  A first baseline selector omitted the accepted child-owned blocker module and
  passed 112 assertions with one skip; the corrected complete M149-M166 group
  passed 113 assertions with one established skip. Both governance modes
  returned zero findings.
- A fresh fetch and authenticated query still found hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, no open PR, and PR #251 as
  the newest merge. Only local `main` and the active M167 branch remain.
- Initial static validation requested formatting, reported one unused loop
  label, and found two partially unknown handle-list values. An explicit typed
  cast, exact one-key/list checks, and removal of the unused label corrected
  those findings. The formatted live probe then passed both release orders.
- The six architecture guards plus two live cases pass. Strict docs build with
  only the known Material notice. The complete M149-M167 boundary passes 121
  assertions with one established skip.
- `pytest-repeat` is intentionally absent, so an exploratory `--count=20`
  command was rejected before collection. Twenty explicit consecutive pytest
  invocations then passed all 40 parametrized live cases.
- The unchanged 46-package lock resolves; the 45-package graphics environment
  checks; all 516 Python files pass Ruff formatting, Ruff, and strict Pyright.
- Exact CPython 3.12.13 passes 3,814 tests with 17 skips. Exact CPython 3.13.13
  and 3.14.5 each pass 3,804 tests with 18 skips from isolated 39-package
  frozen environments.
- Ten real-wgpu tests, both one-repeat profiles, Clockwork Arena, and Agent
  World Builder pass with their established deterministic identities. An
  exploratory Agent World Builder `--help` invocation ran the fixed sample
  because it has no parser; the explicit invocation reproduced the same
  result.
- Two development builds are byte-identical: a 360,595-byte pure wheel at
  SHA-256 `474eccf6c1d8f6aeba7a1b43c5445b25fbd77980a000c4a715d1444ce6372508`
  and a 2,044,435-byte source archive at SHA-256
  `a5353c6380cc9fb22ae4e9990e829b1866fdfdcf1c0793a9fb49748c0a01987a`.
  All 28 installed-wheel consumers pass. Two ten-artifact release stages are
  byte-identical and pass complete release smoke.
- Archive inspection finds 114 wheel entries and 827 source entries, no
  native/WASM/bytecode, no M167 wheel entry, and all four exact M167 sources in
  the source archive. The first selector omitted the underscore-named
  integration module; the corrected selector found all four.
- After the evidence record, the frozen source closure passes again. Two final
  evidence-inclusive builds reproduce the same 360,595-byte wheel and a
  2,046,312-byte source archive at SHA-256
  `508a9fa7925fe9413e2a38aaafab33de4d06669fe99eb4319b1c3cf920e51196`.
  Primary isolated-wheel smoke passes; two final ten-artifact release stages
  are byte-identical and both complete release smokes pass. Final inventory
  remains 114/827 with exact M167 confinement.
- Findings-first scope review finds exactly 16 intended paths, zero protected
  runtime/helper/fixture/workflow/metadata changes, clean whitespace, and no
  public development-tool identity or high-confidence credential match.
  Twelve exact M167 scratch targets were verified directly beneath repository
  `.tmp`, verified non-reparse, removed, and confirmed absent.
- The final two-file format/Ruff/Pyright gate and all eight focused assertions
  pass. Strict docs build with only the known Material notice, both governance
  modes return zero findings, and whitespace passes on the factual record.

## Explicit non-scope

- No runtime cleanup, adapter, public capability probe, package `ctypes` or
  subprocess invocation, retained-root implementation, candidate list, cache
  read/write, remote cache, network, or trusted-time implementation.
- No general concurrency-safe inheritance contract, global launch coordinator,
  every-creator participation rule, general leak-freedom, cancellation,
  reentrancy, launch/restore failure interleaving, invalid handle, child crash,
  cross-process transfer, native close failure, recovery, retry, oplock, lease,
  quiescence, dependency, version, workflow/CI, permission, credential,
  release, tag, or platform-admission implementation.

## Publication condition

- Keep the final branch commit DCO-signed. Push or open a PR only when a fresh
  hosted-state audit proves the preceding local milestone stack is already on
  hosted `main`; otherwise preserve the locally validated branch without
  exposing a partial stack.
- The M167 preimplementation audit found hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, no open PR, and PR #251 as the
  newest merge. The user-reported squash merge is not visible on this remote,
  so the publication condition is not currently met.
- Initial DCO commit `4c1765fadeaa422e361727174ef330eac01d5cef`
  has tree `7281d26fbc4949402c8d6027f8e329301faa4d2e`, sole parent exact M166,
  exact configured maintainer author/committer identity, one DCO sign-off,
  exactly 16 intended paths, no merge commit, a clean worktree, expected
  `0 68` divergence from local M99 main, and only local `main` plus M167.
  Full object verification exits zero with no corruption or missing object;
  it reports only historical dangling objects from prior amended milestones.
  This factual checkpoint is folded into the same local commit before
  publication.
- Final fetch/prune leaves hosted `main` at exact M99, the sole hosted branch.
  Authenticated queries report no open PR and PR #251 as the newest merge.
  Publishing M167 would expose the absent M100-M167 stack, so no push, PR,
  workflow allocation, tag, or release occurred.
