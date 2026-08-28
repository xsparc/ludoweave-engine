# Current task

- **Task:** M174 - prove whether pathname substitution splits M173's
  cooperative Windows coordination barrier across file identities.
- **Status:** Direction, implementation, supported-Python regression,
  rendering, distribution, release rehearsal, documentation, and governance
  gates pass. Evidence-inclusive closure and findings-first review pass; final
  record separator and exact scratch cleanup pass. Commit and publication-
  safety gates pass. The exact 17-path pre-commit scope and hygiene gate passes.
  Publication is correctly withheld because hosted `main` still lacks
  M100-M173; the final amended-object audit follows this factual record.
- **Base:** Fully locally validated M173 DCO commit
  `767337f7ea8138bdc14455296c54d0261cd20e9e`, tree
  `114a874eb76a920b334fbf26190efc4cf63a0f97`, sole parent exact M172.
- **Branch:** `release/m174-windows-lock-substitution`; exact containment
  allowed the redundant local M173 branch to be pruned.

## Acceptance boundary

- Accept RFC-0157 and retain one Windows-only, test-only, current-host NTFS
  observation that renaming and replacing `live/coordination.lock` splits old
  and new M173 participants across independent file identities and lock
  generations.
- Preserve M173, runtime, examples, scripts, dependencies, workflows,
  metadata, and lock byte-for-byte.
- Use one fixed isolated namespace child with no argument or environment
  behavior. Require exact `MoveFileExW` rename, ordinary replacement creation,
  exact bytes, a noninheritable handle, bounded canonical output, and
  deterministic close.
- Prove retained-original identity equals displaced identity and differs from
  replacement identity using `FILE_ID_INFO`.
- Keep unchanged M173 participants live on both identities. Require independent
  exclusive refusal, then prove replacement exclusive ownership succeeds while
  the original participant remains live and the displaced original still
  refuses ownership.
- Record the result as negative capability evidence. It is not participant
  completeness, substitution resistance, Windows admission, or cleanup
  authority.
- Add no runtime adapter, lock API, cleanup authority, dependency, workflow,
  job/allocation, permission, release authority, or CI change.

## Direction evidence

- Microsoft documents `LockFileEx` as a handle/file-range primitive and
  `FILE_ID_INFO` as the volume/file identity for same-computer comparisons.
- Microsoft documents that `FILE_SHARE_DELETE` permits later rename/delete
  access and `MoveFileExW` moves an existing object to another name.
- GitHub documents that each matrix combination creates another job. M174 uses
  only the existing Windows suite and creates no hosted allocation.
- NIST SSDF remains outcome- and risk-oriented; version 1.2 is still a draft.
  The bounded substitution observation is adopted without claiming a newer
  final standard or promoting runtime authority.

## Development evidence so far

- Exact M173 was clean with expected `0 74` divergence from hosted/local M99
  main. Its ten focused architecture/live assertions pass in 0.45 seconds.
  Static and dated strict governance each return zero findings.
- The fixed namespace child and parent integration probe pass strict Pyright.
  The first Ruff run identified only mechanical import ordering; the exact
  correction passes Ruff. The first live observation passes in 0.37 seconds.
- Six new architecture guards plus the live observation pass seven assertions
  in 0.49 seconds. Strict documentation builds in 2.70 seconds with only the
  known Material notice. Ruff formatting requested one mechanical architecture
  wrap; the corrected focused gate passes seven assertions in 0.46 seconds and
  strict docs in 2.47 seconds.
- All 534 Python files pass Ruff formatting, Ruff, and strict Pyright. Exact
  CPython 3.12.13 passes 3,875 tests with 17 skips; exact CPython 3.13.13 and
  3.14.5 each pass 3,865 tests with 18 skips.
- The complete M149-M174 Windows boundary passes 182 tests with one established
  skip. Twenty consecutive live substitutions pass. Ten real-wgpu tests, both
  one-repeat profiles, Clockwork Arena, and Agent World Builder pass.
- Two development builds are byte-identical: a 361,088-byte pure wheel at
  SHA-256 `b6a6f5e75861d3b483533b0abbb110aa058b7b1d9c880948cbdd4f6e96d47acc`
  and a 2,105,817-byte source archive at SHA-256
  `b7d6ea6be098cd0ce3257c99c732a42f6f455232bdb08c218abe5a37c54dc777`.
  Installed-wheel smoke passes; two ten-artifact release stages are identical
  and both complete release smokes pass.
- Final static and dated strict governance checks return zero findings. The
  evidence-inclusive reproduction retains the exact wheel and produces two
  identical 2,107,218-byte source archives at SHA-256
  `8e68012e170376d26657e5d0b0f47568b094bf24fa920123da7041ccf6ca89a9`.
  Installed-wheel smoke, two identical ten-artifact release stages, and both
  release smokes pass.
- Findings-first review found no remaining actionable defect. Public identity,
  added credential/local-path, protected-surface, package-boundary, and scope
  scans pass after replacing two unnecessarily explicit control-pattern names
  with neutral wording.

## Publication boundary

- Fresh hosted `main` is exact M99, no PR is open, and PR #251 is the latest
  merge. M174 is 75 commits ahead and contains the unpublished M100-M173
  prerequisite stack. No branch was pushed, no PR was opened, and no hosted
  workflow allocation was started.
- Publication must not create a new workflow, job, matrix allocation, or
  redundant predecessor branch.

## Explicit non-scope

- A production identity/generation protocol, trusted-root placement,
  uncooperative actors, complete participant admission, mapped views,
  multiple ranges, wait/fairness policy, cancellation, abrupt exit, delayed
  operating-system unlock, native close/unlock failure, filesystem variation,
  recovery, policy, receipts, or independent-host proof.
- Cache-root integration, candidate policy, cleanup authority, Windows
  admission, or a private production adapter.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, dependency,
  native-extension, compiler, workflow, permission, CI-allocation, tag,
  release, publication, or version changes.
